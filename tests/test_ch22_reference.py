import importlib.util
from pathlib import Path
import torch
import pytest

P = Path(__file__).parents[1] / "drafts/ch22/reference.py"
s = importlib.util.spec_from_file_location("r", P)
r = importlib.util.module_from_spec(s)
s.loader.exec_module(r)


def test_reverse_complement_involution():
    x = torch.tensor([[0, 1, 2, 3, 0, 2]])
    assert torch.equal(r.rc_ids(r.rc_ids(x)), x)


def test_causal_prefix_invariance():
    torch.manual_seed(2)
    m = r.DOGMA(d=8, k=2)
    a = torch.tensor([[0, 1, 2, 3, 0, 0]])
    b = torch.tensor([[0, 1, 2, 3, 3, 3]])
    assert torch.allclose(
        m.causal_logits(a)[:, :4], m.causal_logits(b)[:, :4], atol=1e-7
    )


def test_offline_dual_rc_invariance():
    torch.manual_seed(2)
    m = r.DOGMA(d=8, k=2)
    x = torch.tensor([[0, 1, 2, 3, 0, 2]])
    assert torch.allclose(
        m.offline_dual_logits(x), m.offline_dual_logits(r.rc_ids(x)), atol=1e-6
    )


def test_gradients_reach_memory_and_gate_parameters():
    torch.manual_seed(2)
    m = r.DOGMA(d=8, k=2)
    x = torch.tensor([[0, 1, 2, 3]])
    m.causal_logits(x).square().mean().backward()
    assert m.cell.write_gate.weight.grad.abs().sum() > 0
    assert m.cell.gate.weight.grad.abs().sum() > 0


def test_state_reset_is_deterministic():
    torch.manual_seed(2)
    m = r.DOGMA(d=8, k=2)
    x = torch.tensor([[0, 1, 2, 3]])
    assert torch.allclose(m.causal_logits(x), m.causal_logits(x))


@pytest.mark.parametrize("split", range(7))
def test_full_chunk_state_and_parameter_gradient_parity(split):
    torch.manual_seed(5)
    model = r.DOGMA(d=3, k=2).double()
    x = torch.tensor([[0, 1, 2, 3, 1, 0], [3, 2, 0, 1, 0, 2]])
    full, state, _ = model.run(x)
    full_grad = torch.autograd.grad(
        model.head(full).square().sum(), tuple(model.parameters())
    )
    left, carry, _ = model.run(x[:, :split])
    h_before, m_before = carry.h.clone(), carry.memory.clone()
    right, final, _ = model.run(x[:, split:], carry)
    chunk = torch.cat((left, right), dim=1)
    chunk_grad = torch.autograd.grad(
        model.head(chunk).square().sum(), tuple(model.parameters())
    )
    assert torch.equal(carry.h, h_before) and torch.equal(carry.memory, m_before)
    torch.testing.assert_close(chunk, full, rtol=1e-12, atol=1e-12)
    for a, b in zip(final, state):
        torch.testing.assert_close(a, b, rtol=1e-12, atol=1e-12)
    for a, b in zip(full_grad, chunk_grad):
        torch.testing.assert_close(a, b, rtol=1e-12, atol=1e-12)


def test_empty_chunk_is_identity_not_empty_offline_mean():
    model = r.DOGMA(d=3, k=2)
    state = model.initial_state(2)
    y, after, tr = model.run(torch.empty((2, 0), dtype=torch.long), state)
    assert (
        y.shape == (2, 0, 3)
        and after.h is state.h
        and after.memory is state.memory
        and tr == []
    )
    with pytest.raises(ValueError, match="at least one"):
        model.offline_dual_logits(torch.empty((2, 0), dtype=torch.long))


def test_assigned_transition_against_closed_form():
    # This oracle does not call the model or its affine maps.
    for row in r.assigned_trace():
        t = row["t"]
        assert row["h"] == pytest.approx(0.5 * (1 - 0.5**t))
        assert row["old_memory"] == pytest.approx(0.8 * (1 - 0.75 ** (t - 1)))
        assert row["new_memory"] == pytest.approx(0.8 * (1 - 0.75**t))
        assert row["y"] == pytest.approx(
            __import__("math").tanh(row["h"] + row["old_memory"])
        )


def test_differentiable_cell_state_against_finite_differences():
    torch.manual_seed(9)
    cell = r.DOGMACell(d=2, k=2).double()
    h = torch.randn((1, 2), dtype=torch.float64, requires_grad=True)
    mem = torch.randn((1, 2, 2), dtype=torch.float64, requires_grad=True)
    assert torch.autograd.gradcheck(
        lambda a, b: cell.step(torch.tensor([0]), a, b)[:3],
        (h, mem),
        eps=1e-6,
        atol=1e-5,
        rtol=1e-4,
    )


def test_batch_partition_does_not_cross_contaminate_requests():
    torch.manual_seed(10)
    model = r.DOGMA(d=3, k=2).double()
    x = torch.tensor([[0, 0, 0, 1], [3, 3, 3, 2]])
    y, state, _ = model.run(x)
    for i in range(2):
        solo, carry, _ = model.run(x[i : i + 1])
        torch.testing.assert_close(solo, y[i : i + 1])
        torch.testing.assert_close(carry.h, state.h[i : i + 1])
        torch.testing.assert_close(carry.memory, state.memory[i : i + 1])


def test_missing_memory_carry_changes_the_function():
    torch.manual_seed(10)
    model = r.DOGMA(d=3, k=2).double()
    x = torch.tensor([[0, 1, 2, 3]])
    _, carry, _ = model.run(x[:, :2])
    correct, _, _ = model.run(x[:, 2:], carry)
    incomplete = r.DOGMAState(carry.h, torch.zeros_like(carry.memory))
    wrong, _, _ = model.run(x[:, 2:], incomplete)
    assert not torch.allclose(correct, wrong, rtol=1e-10, atol=1e-10)


def test_offline_feature_really_uses_suffix():
    torch.manual_seed(10)
    model = r.DOGMA(d=4, k=2).double()
    a = torch.tensor([[0, 1, 2, 3, 0, 1]])
    b = torch.tensor([[0, 1, 2, 3, 3, 3]])
    assert not torch.allclose(
        model.offline_dual_logits(a), model.offline_dual_logits(b)
    )


def test_memory_intervention_changes_readout_but_not_fast_transition():
    torch.manual_seed(10)
    model = r.DOGMA(d=3, k=2)
    x = torch.tensor([[0, 1, 2, 3]])
    normal, state, _ = model.run(x)
    erased, other, _ = model.run(x, disable_read=True)
    assert torch.equal(state.h, other.h) and torch.equal(state.memory, other.memory)
    assert not torch.allclose(normal, erased)


@pytest.mark.parametrize(
    "x",
    [
        torch.tensor([[4]]),
        torch.tensor([[-1]]),
        torch.tensor([[0.0]]),
        torch.tensor([0]),
        torch.empty((0, 2), dtype=torch.long),
    ],
)
def test_invalid_input_rejected(x):
    with pytest.raises(ValueError):
        r.DOGMA(d=2, k=1).run(x)


def test_invalid_carry_and_rc_rejected():
    model = r.DOGMA(d=2, k=1)
    for state in [
        torch.zeros(2),
        r.DOGMAState(torch.zeros((1, 3)), torch.zeros((1, 1, 2))),
        r.DOGMAState(torch.zeros((1, 2), dtype=torch.float64), torch.zeros((1, 1, 2))),
        r.DOGMAState(torch.full((1, 2), float("nan")), torch.zeros((1, 1, 2))),
    ]:
        with pytest.raises(ValueError):
            model.run(torch.tensor([[0]]), state)
    with pytest.raises(ValueError):
        r.rc_ids(torch.tensor([[4]]))


@pytest.mark.parametrize("seed", [137, 139, 141])
def test_labels_have_independent_motif_oracle(seed):
    x, y = r.make_data(40, 24, seed)
    assert torch.equal(y, r.motif_oracle(x))
    assert torch.equal(y, r.motif_oracle(r.rc_ids(x)))


def test_data_split_is_reverse_complement_disjoint():
    tr, _ = r.make_data(512, 24, 137)
    te, _ = r.make_data(128, 24, 139)
    assert not r.record_keys(tr) & r.record_keys(te)


@pytest.mark.parametrize("d,k,c", [(1, 1, 2), (12, 3, 2), (5, 4, 4)])
def test_parameter_count_against_symbolic_derivation(d, k, c):
    assert r.params(r.DOGMA(d=d, k=k, classes=c)) == 7 * d * d + 8 * d + 2 * k * (
        d + 1
    ) + c * (d + 1)
