"""Cross-batch execution using real chapter interfaces, not copied toy models."""

from dataclasses import replace
import importlib.util
from pathlib import Path
import sys

import pytest
import torch

SPEC = importlib.util.spec_from_file_location(
    "evod_integrated_spine",
    Path(__file__).parents[1] / "examples/integrated_spine/paged_runtime.py",
)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)
OWNER = ("tenant", "parent")
CHILD = ("tenant", "child")
TOKENS = (0, 1, 2, 3, 2, 0)


def tensor(value):
    return torch.tensor(value.data, dtype=torch.float64)


@pytest.mark.parametrize("split", range(1, 6))
def test_paged_runtime_chunk_continuation_matches_actual_full_model(split):
    adapter = m.PagedEngineAdapter()
    h = adapter.open(OWNER)
    first = adapter.execute(h, OWNER, TOKENS[:split])
    last = adapter.execute(h, OWNER, TOKENS[split:])
    actual = torch.cat((tensor(first), tensor(last)))
    expected = m.paging.native.full_oracle(adapter.model, TOKENS)
    torch.testing.assert_close(actual, expected, atol=2e-12, rtol=2e-12)
    adapter.close(h, OWNER)
    assert adapter.pool.audit()["used_pages"] == 0
    assert not adapter._states


def test_shared_tail_cow_prefix_eviction_and_two_suffix_oracles():
    adapter = m.PagedEngineAdapter()
    h = adapter.open(OWNER)
    adapter.execute(h, OWNER, TOKENS[:3])
    native_handle = adapter._states[h.serial][1]
    cache = m.paging.PrefixCache(adapter.pool, entries=1)
    key = cache.put(native_handle, OWNER)
    child = adapter.fork(h, OWNER, CHILD)
    before = adapter.pool.flatten(native_handle, OWNER)
    child_z = adapter.execute(child, CHILD, (3,))
    after = adapter.pool.flatten(native_handle, OWNER)
    for x, y in zip(before.layers, after.layers):
        torch.testing.assert_close(x.k, y.k, atol=0, rtol=0)
        torch.testing.assert_close(x.v, y.v, atol=0, rtol=0)
    cache.evict(key)  # live parent and child still own their pages
    parent_z = adapter.execute(h, OWNER, (1,))
    for value, suffix in ((child_z, (3,)), (parent_z, (1,))):
        torch.testing.assert_close(
            tensor(value),
            m.paging.native.full_oracle(adapter.model, TOKENS[:3] + suffix)[-1:],
            atol=2e-12,
            rtol=2e-12,
        )
    adapter.close(child, CHILD)
    adapter.close(h, OWNER)
    assert adapter.pool.audit()["references"] == 0


def test_runtime_owner_instance_and_stale_handle_fences():
    a, b = m.PagedEngineAdapter(), m.PagedEngineAdapter()
    h = a.open(OWNER)
    with pytest.raises(RuntimeError):
        a.execute(h, CHILD, (0,))
    with pytest.raises(RuntimeError):
        b.execute(h, OWNER, (0,))
    with pytest.raises(RuntimeError):
        a.execute(replace(h, artifact="0" * 64), OWNER, (0,))
    with pytest.raises(PermissionError):
        a.fork(h, OWNER, ("other-tenant", "child"))
    a.close(h, OWNER)
    with pytest.raises(RuntimeError):
        a.execute(h, OWNER, (0,))
    assert not a._states and not b._states


@pytest.mark.parametrize("tokens", [(), [0], (True,), (1.5,), (0, 99)])
def test_invalid_append_preserves_native_state(tokens):
    adapter = m.PagedEngineAdapter()
    h = adapter.open(OWNER)
    adapter.execute(h, OWNER, TOKENS[:3])
    native_handle = adapter._states[h.serial][1]
    before = adapter.pool.state(native_handle, OWNER)
    with pytest.raises(ValueError):
        adapter.execute(h, OWNER, tokens)
    assert adapter.pool.state(native_handle, OWNER) == before
    adapter.close(h, OWNER)


def plan(adapter, tokens=TOKENS):
    r = m.runtime
    return r.Plan(
        OWNER,
        (("t", r.Value(r.Ty.TOKENS, tokens)),),
        (
            r.Step(
                "h",
                "engine",
                ("t",),
                "z",
                r.Ty.LOGITS,
                adapter.artifact,
                adapter.capability,
            ),
        ),
        ("z",),
    )


def test_actual_runtime_routes_paged_engine_and_cleans_up():
    adapter = m.PagedEngineAdapter()
    r = m.runtime
    (value,) = r.Runtime((adapter,), r.Policy()).execute(plan(adapter))
    torch.testing.assert_close(
        tensor(value),
        m.paging.native.full_oracle(adapter.model, TOKENS),
        atol=2e-12,
        rtol=2e-12,
    )
    assert value.provenance[0] == "hermon-paged"
    assert not adapter._states and adapter.pool.audit()["used_pages"] == 0
    contiguous = r.EngineAdapter("hermon", model=adapter.model)
    with pytest.raises(RuntimeError, match="uniquely"):
        r.Runtime((adapter, contiguous), r.Policy()).execute(plan(adapter))


def test_runtime_allocation_failure_releases_issued_handle():
    adapter = m.PagedEngineAdapter(capacity=1, page_size=2)
    r = m.runtime
    with pytest.raises(MemoryError):
        r.Runtime((adapter,), r.Policy()).execute(plan(adapter))
    assert not adapter._states and adapter.pool.audit()["free_pages"] == 1


def test_runtime_trace_failure_still_releases_actual_page_state():
    adapter = m.PagedEngineAdapter()
    r = m.runtime
    # plan_start, step_start, route precede engine execution; fail on result.
    with pytest.raises(OSError):
        r.Runtime((adapter,), r.Policy(), trace=r.Trace(fail_at=3)).execute(
            plan(adapter)
        )
    assert not adapter._states and adapter.pool.audit()["used_pages"] == 0


def test_compiler_retains_unused_paged_effect_and_native_outputs():
    c, r = m.compiler, m.runtime
    p = c.Program(
        (("t", c.Ty.TOKENS),),
        (
            c.Op(
                "engine",
                "engine",
                ("t",),
                "unused_logits",
                c.Ty.LOGITS,
                (
                    ("capability", "addressable_kv"),
                    ("artifact", m.PagedEngineAdapter().artifact),
                ),
                c.EFFECTS["engine"],
            ),
            c.Op("constant", "const", (), "answer", c.Ty.INT, (("value", 7),)),
        ),
        ("answer",),
    )
    q = c.dce(c.constant_fold(p))
    assert any(op.kind == "engine" for op in q.ops)
    observations = []
    for program in (p, q):
        adapter = m.PagedEngineAdapter()
        schedule = c.lower(program, (adapter,))
        assert schedule[0]["backend"] == "hermon-paged"
        out, effects = c.interpret(
            program, {"t": TOKENS}, c.Effects((adapter,), OWNER, r.Policy())
        )
        assert not adapter._states and adapter.pool.audit()["used_pages"] == 0
        observations.append((out, effects))
    assert observations[0] == observations[1]
    expected = m.paging.native.full_oracle(m.PagedEngineAdapter().model, TOKENS)
    torch.testing.assert_close(
        torch.tensor(observations[0][1][0][3], dtype=torch.float64),
        expected,
        atol=2e-12,
        rtol=2e-12,
    )
