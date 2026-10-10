"""Independent scalar/derivative and shell/native-state falsifiers."""

from dataclasses import replace
import importlib.util
import itertools
from pathlib import Path
import sys
import math
import pytest
import torch

PATH = Path(__file__).resolve().parents[1] / "drafts/ch31/reference.py"
spec = importlib.util.spec_from_file_location("evo31", PATH)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
OWNER = ("tenant-a", "request-a")


@pytest.mark.parametrize("tokens", list(itertools.product(range(3), repeat=3)))
def test_all_short_sequences_against_scalar_expansion(tokens):
    model = m.tiny_model()
    state, _ = m.ingest(model, m.construct(model, OWNER), tokens, OWNER)
    # Independent rational fixture: gate exactly 1/2, no reference oracle call.
    h = [
        sum(
            ([0, 1, 0][q] if j == 0 else [0, 0, 1][q]) * 0.5 * a ** (2 - k)
            for k, q in enumerate(tokens)
        )
        for j, a in enumerate([0.5, 0.25])
    ]
    assert state.hidden.tolist() == pytest.approx(h)
    h2, z = m.scalar_closed_form(model, tokens)
    assert h2 == pytest.approx(h)
    assert z == pytest.approx([0, h[0] - h[1], -h[0] + h[1]])


@pytest.mark.parametrize("split", [0, 1, 2, 3])
def test_chunk_forward_and_graph_continuity(split):
    model = m.tiny_model()
    model.write.requires_grad_()
    first, _ = m.ingest(model, m.construct(model, OWNER), [1, 2, 1][:split], OWNER)
    final, _ = m.ingest(model, first, [1, 2, 1][split:], OWNER)
    final.hidden.sum().backward()
    # d b/d w = e^2 * 1/4 at w=0. Transport by retention.
    assert model.write.grad.tolist() == pytest.approx(
        [0.25 * (0.5**2 + 1), 0.25 * 0.25]
    )


@pytest.mark.parametrize("w", [-3.0, 0.0, 2.0])
def test_autograd_vs_manual_and_finite_difference(w):
    model = m.tiny_model()
    with torch.no_grad():
        model.write.fill_(w)
    model.write.requires_grad_()
    final, _ = m.ingest(model, m.construct(model, OWNER), [1, 2, 1], OWNER)
    final.hidden.sum().backward()
    s = 1 / (1 + math.exp(-w))
    manual = [s * (1 - s) * (1 + 0.5**2), s * (1 - s) * 0.25]
    assert model.write.grad.tolist() == pytest.approx(manual, abs=1e-12)
    eps = 1e-5
    for j in range(2):
        values = []
        for direction in [-1, 1]:
            other = m.tiny_model()
            with torch.no_grad():
                other.write.fill_(w)
                other.write[j] += direction * eps
            values.append(sum(m.scalar_closed_form(other, [1, 2, 1])[0]))
        assert (values[1] - values[0]) / (2 * eps) == pytest.approx(
            manual[j], abs=1e-10
        )


@pytest.mark.parametrize("prefix", [[], [1], [1, 2], [1, 2, 1]])
def test_suffix_does_not_change_prefix(prefix):
    model = m.tiny_model()
    _, base = m.ingest(model, m.construct(model, OWNER), prefix, OWNER)
    for suffix in [[0, 0], [1, 2], [2, 1]]:
        _, extended = m.ingest(model, m.construct(model, OWNER), prefix + suffix, OWNER)
        for a, b in zip(base, extended):
            assert torch.equal(a, b)


@pytest.mark.parametrize("field", ["embedding", "retention", "write", "head"])
def test_artifact_detects_parameter_mutation(field):
    model = m.tiny_model()
    state = m.construct(model, OWNER)
    with torch.no_grad():
        getattr(model, field).view(-1)[0] += 0.01
    with pytest.raises(ValueError):
        m.native_step(model, state, 1, OWNER)


def test_vocab_order_is_artifact_semantics():
    model = m.tiny_model()
    state = m.construct(model, OWNER)
    model = replace(model, vocabulary=("1", "0", "2"))
    with pytest.raises(ValueError):
        m.ingest(model, state, [], OWNER)


@pytest.mark.parametrize(
    "owner", [("tenant-b", "request-a"), ("tenant-a", "request-b"), ("", "r")]
)
def test_owner_enforced_on_empty_and_nonempty(owner):
    model = m.tiny_model()
    state = m.construct(model, OWNER)
    for tokens in [[], [1]]:
        with pytest.raises(ValueError):
            m.ingest(model, state, tokens, owner)


@pytest.mark.parametrize(
    "change",
    [
        {"position": -1},
        {"position": True},
        {"hidden": torch.zeros(3, dtype=torch.float64)},
        {"hidden": torch.zeros(2, dtype=torch.float32)},
        {"hidden": torch.tensor([float("nan"), 0.0], dtype=torch.float64)},
    ],
)
def test_bad_state(change):
    model = m.tiny_model()
    with pytest.raises(ValueError):
        m.native_step(model, replace(m.construct(model, OWNER), **change), 1, OWNER)


@pytest.mark.parametrize("token", [True, -1, 3, 1.0, None])
def test_invalid_tail_is_failure_atomic(token):
    model = m.tiny_model()
    state = m.construct(model, OWNER)
    with pytest.raises(ValueError):
        m.ingest(model, state, [1, token], OWNER)
    assert state.position == 0 and torch.equal(
        state.hidden, torch.zeros(2, dtype=torch.float64)
    )


def test_mask_holds_position_and_has_zero_output():
    model = m.tiny_model()
    state, outputs = m.ingest(
        model, m.construct(model, OWNER), [1, None, 2], OWNER, [True, False, True]
    )
    expected, _ = m.ingest(model, m.construct(model, OWNER), [1, 2], OWNER)
    assert state.position == 2 and torch.equal(state.hidden, expected.hidden)
    assert torch.equal(outputs[1], torch.zeros(3, dtype=torch.float64))


def test_snapshot_clone_vs_detach():
    x = torch.tensor([1.0], dtype=torch.float64, requires_grad=True)
    alias = x.detach()
    copied = x.clone()
    with torch.no_grad():
        x.add_(1)
    assert alias.item() == 2 and copied.item() == 1
    copied.sum().backward()
    assert x.grad.item() == 1


def session(deadline=100, items=2):
    model = m.tiny_model()
    state, _ = m.ingest(model, m.construct(model, OWNER), [1, 2], OWNER)
    result = m.native_step(model, state, 1, OWNER)
    shell = m.runtime_module()
    req = shell.Request(
        OWNER[1],
        OWNER[0],
        m.artifact_id(model),
        deadline,
        max_tokens=3,
        queue_items=items,
    )
    runtime = shell.Runtime(req, shell.StateRegistry())
    runtime.admit("worker", 0)
    runtime.allocate("slot-a", 0)
    return m.Session(model, result, OWNER, runtime)


def test_commit_installs_state_and_correct_next_token():
    s = session()
    before = s.result.state.position
    p = s.prepare(1)
    assert p.token == 1 and s.result.state.position == before
    assert s.finish(p, 2)
    assert s.result.state.position == before + 1
    assert s.runtime.generated == s.runtime.revision == 1
    assert s.runtime.queue[0][1] == b"1"


@pytest.mark.parametrize("reason", ["cancelled", "deadline"])
def test_late_work_cannot_advance_native_state(reason):
    s = session(deadline=10)
    before = m.state_stamp(s.result.state)
    p = s.prepare(1)
    if reason == "cancelled":
        s.runtime.terminate("cancelled", 2)
        now = 3
    else:
        now = 10
    assert not s.finish(p, now)
    assert m.state_stamp(s.result.state) == before
    assert s.runtime.revision == 0 and not s.runtime.queue
    assert s.runtime.settled == 1 and s.runtime.discarded_work == 1


def test_backpressure_does_not_compute_or_advance():
    s = session(items=1)
    p = s.prepare(1)
    s.finish(p, 2)
    before = m.state_stamp(s.result.state)
    assert s.prepare(3) is None
    assert m.state_stamp(s.result.state) == before
    assert s.runtime.launched == 1


def test_duplicate_completion_rejected():
    s = session()
    p = s.prepare(1)
    s.finish(p, 2)
    with pytest.raises(RuntimeError):
        s.finish(p, 3)


def test_parameter_change_while_pending_fails_without_installation():
    s = session()
    p = s.prepare(1)
    before = m.state_stamp(s.result.state)
    with torch.no_grad():
        s.model.write[0] += 0.1
    with pytest.raises(ValueError):
        s.finish(p, 2)
    assert m.state_stamp(s.result.state) == before
    assert s.runtime.reason == "failed" and s.runtime.pending is None


def test_shell_identity_mismatch():
    s = session()
    with pytest.raises(ValueError):
        m.Session(s.model, s.result, ("tenant-b", "request-a"), s.runtime)


def test_staged_candidate_mutation_rejected():
    s = session()
    pending = s.prepare(1)
    before = m.state_stamp(s.result.state)
    with torch.no_grad():
        pending.candidate.state.hidden[0] += 0.1
    with pytest.raises(ValueError):
        s.finish(pending, 2)
    assert m.state_stamp(s.result.state) == before
    assert s.runtime.reason == "failed"


def test_bounded_state():
    model = m.tiny_model()
    state, _ = m.ingest(model, m.construct(model, OWNER), [1, 2] * 200, OWNER)
    assert state.hidden[0] <= 0.5 / (1 - 0.5) + 1e-12
    assert state.hidden[1] <= 0.5 / (1 - 0.25) + 1e-12
