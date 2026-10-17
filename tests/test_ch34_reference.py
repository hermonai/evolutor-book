import importlib.util
from pathlib import Path
import sys
from dataclasses import replace
from fractions import Fraction
import itertools

import pytest
import torch

SPEC = importlib.util.spec_from_file_location(
    "evod34_tests", Path(__file__).parents[1] / "drafts/ch34/reference.py"
)
r = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = r
SPEC.loader.exec_module(r)


def fixture(capacity=4):
    p, n = r.pool_module(), r.native_module()
    model = n.tiny_model()
    pool = p.Pool("tests", capacity, 2, n.artifact_id(model))
    owners = [("tenant-a", str(i)) for i in range(capacity)]
    handles = [pool.allocate(o) for o in owners]
    return model, pool, owners, handles, r.Engine(pool, model)


@pytest.mark.parametrize("batch", [1, 2, 7, 16])
@pytest.mark.parametrize("seed", [2, 19, 81])
def test_vector_lift_matches_actual_scalar(seed, batch):
    n = r.native_module()
    g = torch.Generator().manual_seed(seed)
    model = n.Model(
        tuple("ACGT"),
        torch.randn(4, 5, generator=g, dtype=torch.float64),
        torch.rand(5, generator=g, dtype=torch.float64),
        torch.randn(5, generator=g, dtype=torch.float64),
        torch.randn(5, 4, generator=g, dtype=torch.float64),
    )
    hidden = torch.randn(batch, 5, generator=g, dtype=torch.float64)
    original = hidden.clone()
    tokens = [i % 4 for i in range(batch)]
    active = [i % 3 != 1 for i in range(batch)]
    h, z = r.batched_step(model, hidden, tokens, active)
    assert torch.equal(hidden, original)
    for i in range(batch):
        if active[i]:
            owner = ("t", str(i))
            state = n.State(owner, n.artifact_id(model), 7, hidden[i])
            scalar = n.native_step(model, state, tokens[i], owner)
            torch.testing.assert_close(
                h[i], scalar.state.hidden, atol=1e-14, rtol=1e-14
            )
            torch.testing.assert_close(z[i], scalar.logits, atol=1e-14, rtol=1e-14)
        else:
            assert torch.equal(h[i], hidden[i]) and torch.equal(z[i], torch.zeros(4))
    h[0, 0] += 1
    assert torch.equal(hidden, original)


def test_rational_all_short_streams_and_mixed_positions():
    # Independent exact rational update, no native_step reuse.
    for seq in itertools.product(range(3), repeat=4):
        model, pool, owners, handles, engine = fixture(2)
        a, b = Fraction(0), Fraction(0)
        for token in seq:
            a = a / 2 + Fraction(token == 1, 2)
            b = b / 4 + Fraction(token == 2, 2)
            job = engine.prepare(
                [
                    r.Lane(handles[1], owners[1], token),
                    r.Lane(handles[0], owners[0], object(), False),
                ]
            )
            ok, z = engine.finish(job)
            assert ok == (True, False) and z[1] is None
        snap = pool.read(handles[1], owners[1])
        assert snap.hidden == (float(a), float(b)) and snap.position == 4
        assert pool.read(handles[0], owners[0]).position == 0


@pytest.mark.parametrize("bad", [True, -1, 3, 1.0, None])
def test_bad_live_token_preflight_has_no_effect(bad):
    model, pool, owners, handles, engine = fixture()
    before = [pool.read(h, o) for h, o in zip(handles, owners)]
    with pytest.raises(ValueError):
        engine.prepare(
            [r.Lane(handles[0], owners[0], 1), r.Lane(handles[1], owners[1], bad)]
        )
    assert pool.stats()["pins"] == 0
    assert before == [pool.read(h, o) for h, o in zip(handles, owners)]


def test_nonfinite_result_preflight_before_pin():
    model, pool, owners, handles, _ = fixture()
    model.embedding[1] = torch.finfo(torch.float64).max
    model.head.fill_(torch.finfo(torch.float64).max)
    pool.artifact = r.native_module().artifact_id(model)
    # Fresh pool ensures handles bind the changed artifact.
    p = r.pool_module()
    pool = p.Pool("overflow", 1, 2, pool.artifact)
    h = pool.allocate(owners[0])
    with pytest.raises(ValueError):
        r.Engine(pool, model).prepare([r.Lane(h, owners[0], 1)])
    assert pool.stats()["pins"] == 0 and pool.read(h, owners[0]).position == 0


@pytest.mark.parametrize("active", [True, False])
def test_duplicate_even_if_inactive(active):
    _, pool, o, h, e = fixture()
    with pytest.raises(ValueError):
        e.prepare([r.Lane(h[0], o[0], 1), r.Lane(h[0], o[0], None, active)])
    assert pool.stats()["pins"] == 0


def test_cancellation_retires_until_ack_and_sibling_commits():
    _, pool, o, h, e = fixture(2)
    job = e.prepare([r.Lane(h[i], o[i], i + 1) for i in range(2)])
    pool.release(h[0], o[0])
    with pytest.raises(MemoryError):
        pool.allocate(("other", "new"))
    ok, outputs = e.finish(job)
    assert ok == (False, True) and outputs[0] is None
    assert pool.stats()["pins"] == 0 and pool.stats()["free"] == 1
    fresh = pool.allocate(("other", "new"))
    assert fresh.generation == h[0].generation + 1
    assert pool.read(fresh, fresh.owner).hidden == (0, 0)
    assert pool.read(h[1], o[1]).hidden == (0, 0.5)


def test_model_change_discards_all_pins():
    model, pool, o, h, e = fixture(2)
    job = e.prepare([r.Lane(h[i], o[i], 1) for i in range(2)])
    model.head[0, 0] += 0.01
    with pytest.raises(ValueError):
        e.finish(job)
    assert pool.stats()["pins"] == 0
    assert all(pool.read(handle, owner).position == 0 for handle, owner in zip(h, o))


def test_external_version_winner_rejects_stale_batch_completion():
    _, pool, o, h, e = fixture(1)
    job = e.prepare([r.Lane(h[0], o[0], 1)])
    competitor = pool.pin(h[0], o[0])
    assert pool.complete(competitor, o[0], r.pool_module().Snapshot(1, (0, 0.5)))
    assert e.finish(job) == ((False,), (None,))
    assert pool.read(h[0], o[0]).hidden == (0, 0.5) and pool.stats()["pins"] == 0


@pytest.mark.parametrize("size", range(1, 10))
def test_fixed_ready_cohort_sweep_bound(size):
    import math

    for limit in range(1, size + 1):
        scheduler = r.RoundRobin()
        visited = set()
        for _ in range(math.ceil(size / limit)):
            visited.update(scheduler.choose([True] * size, limit))
        assert visited == set(range(size))


def test_busy_forged_duplicate_and_discard():
    _, pool, o, h, e = fixture()
    job = e.prepare([r.Lane(h[0], o[0], 1)])
    with pytest.raises(RuntimeError):
        e.prepare([r.Lane(h[0], o[0], 2)])
    with pytest.raises(RuntimeError):
        e.finish(replace(job))
    assert e.finish(job, discard=True) == ((False,), (None,))
    with pytest.raises(RuntimeError):
        e.finish(job)
    assert pool.stats()["pins"] == 0


@pytest.mark.parametrize("kind", ["caller", "generation", "pool", "artifact"])
def test_invalid_handle(kind):
    _, pool, o, h, e = fixture()
    handle, owner = h[0], o[0]
    if kind == "caller":
        owner = ("other", "request")
    else:
        handle = replace(
            handle,
            **{kind: {"generation": 99, "pool": "x", "artifact": "f" * 64}[kind]},
        )
    with pytest.raises((RuntimeError, PermissionError)):
        e.prepare([r.Lane(handle, owner, 1)])
    assert pool.stats()["pins"] == 0


def test_permutation_and_cross_tenant_lane_separation():
    for order in itertools.permutations(range(3)):
        model, pool, owners, handles, engine = fixture(3)
        job = engine.prepare([r.Lane(handles[i], owners[i], i) for i in order])
        accepted, _ = engine.finish(job)
        assert all(accepted)
        assert [pool.read(h, o).hidden for h, o in zip(handles, owners)] == [
            (0, 0),
            (0.5, 0),
            (0, 0.5),
        ]
    p = r.pool_module()
    pool = p.Pool("mixed", 2, 2, r.native_module().artifact_id(model))
    owners = [("tenant-a", "same"), ("tenant-b", "same")]
    h = [pool.allocate(o) for o in owners]
    job = r.Engine(pool, model)
    result = job.prepare([r.Lane(h[0], owners[0], 1), r.Lane(h[1], owners[1], 2)])
    job.finish(result)
    assert pool.read(h[0], owners[0]).hidden != pool.read(h[1], owners[1]).hidden


def test_checkpoint_restored_branches_can_batch():
    cp, p, n = r.checkpoint_module(), r.pool_module(), r.native_module()
    model = n.tiny_model()
    context = cp.context_for(model, "tenant-a")
    pool = p.Pool("restore-batch", 3, 2, context.artifact)
    owner = ("tenant-a", "prefix")
    h = pool.allocate(owner)
    prefix, _ = cp.advance(pool, h, owner, model, context, (), (1, 2, 1))
    checkpoint = cp.capture(pool, h, owner, context, prefix)
    owners = (("tenant-a", "left"), ("tenant-a", "right"))
    a, b = cp.restore_many(checkpoint, pool, owners, context, prefix)
    engine = r.Engine(pool, model)
    engine.finish(engine.prepare([r.Lane(a, owners[0], 0), r.Lane(b, owners[1], 2)]))
    assert pool.read(a, owners[0]).hidden == (5 / 16, 1 / 32)
    assert pool.read(b, owners[1]).hidden == (5 / 16, 17 / 32)
    assert cp.replay_audit(checkpoint, model, context)


def test_round_robin_finite_cohort_fairness_and_churn():
    s = r.RoundRobin()
    assert s.choose([True] * 5, 2) == (0, 1)
    assert s.choose([True] * 5, 2) == (2, 3)
    assert s.choose([True] * 5, 2) == (4, 0)
    assert s.choose([False, True, False], 2) == (1,)
    assert s.choose([], 2) == () and s.choose([False], 1) == ()
    assert [x["members"] for x in r.results()["trace"]] == ["A,B", "A,C", "A,C"]
    assert r.results()["final_hidden"] == [[0.625, 0.125], [0, 0.5], [0.75, 0]]


@pytest.mark.parametrize("mask", [[1], [None], [], [True, False]])
def test_invalid_activity(mask):
    with pytest.raises(ValueError):
        r.batched_step(
            r.native_module().tiny_model(),
            torch.zeros(1, 2, dtype=torch.float64),
            [1],
            mask,
        )


def test_all_inactive_no_pin_no_clock_and_zero_input_counterexample():
    model, pool, o, h, e = fixture(1)
    p = r.pool_module()
    pool.write(h[0], o[0], p.Snapshot(7, (1, 2)))
    job = e.prepare([r.Lane(h[0], o[0], float("nan"), False)])
    assert pool.stats()["pins"] == 0
    assert e.finish(job) == ((False,), (None,))
    assert pool.read(h[0], o[0]) == p.Snapshot(7, (1, 2))
    hidden = torch.tensor([[1.0, 2.0]], dtype=torch.float64)
    decayed, _ = r.batched_step(model, hidden, [0], [True])
    assert not torch.equal(decayed, hidden)


def test_payload_accounting_and_domains():
    resident = r.traffic(8, 64, 4, staged=False)
    staged = r.traffic(8, 64, 4)
    unfused = r.traffic(8, 64, 4, fused=False)
    assert resident["total"] == 12544
    assert staged["total"] == 28928 and unfused["total"] == 37120
    assert unfused["total"] - staged["total"] == 2 * 8 * 64 * 8
    assert resident["arithmetic"] == 6144
    with pytest.raises(ValueError):
        r.traffic(True, 64, 4)
