import importlib.util
import json
from pathlib import Path
import pytest
import torch

torch.set_num_threads(1)
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evo10", ROOT / "drafts/ch10/reference.py"
)
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def fixture():
    x = (
        torch.linspace(-1, 2, 24, dtype=torch.float64)
        .reshape(6, 4)
        .requires_grad_()
    )
    logits = torch.tensor(
        [
            [3.0, 1, 0],
            [2, 1, 0],
            [4, 0, 1],
            [0, 1, 3],
            [1, 4, 0],
            [0, 3, 1],
        ],
        dtype=torch.float64,
        requires_grad=True,
    )
    return x, logits, ref.expert_weights(), torch.ones(6, dtype=torch.bool)


def test_plan_explicit_demand_admission_and_ties():
    x, logits, w, valid = fixture()
    p = ref.plan(logits, valid, 2)
    assert p["selected"].tolist() == [0, 0, 0, 2, 1, 1]
    assert p["accepted"].tolist() == [True, True, False, True, True, True]
    assert p["demand"] == [3, 2, 1] and p["used"] == [2, 2, 1]
    tied = ref.plan(torch.zeros_like(logits), valid, 2)
    assert tied["selected"].tolist() == [0] * 6
    assert tied["accepted"].tolist() == [
        True,
        True,
        False,
        False,
        False,
        False,
    ]


@pytest.mark.parametrize("capacity", [0, 1, 2, 6])
def test_sparse_dense_values_and_all_gradients(capacity):
    x, logits, weights, valid = fixture()
    p = ref.plan(logits, valid, capacity)
    a, b = ref.dispatch(x, weights, p), ref.dense_oracle(x, weights, p)
    assert torch.allclose(a, b, atol=1e-12, rtol=1e-12)
    leaves = [x, logits] + list(weights.values())
    ga = torch.autograd.grad(
        a.square().sum(), leaves, retain_graph=True, allow_unused=True
    )
    gb = torch.autograd.grad(b.square().sum(), leaves, allow_unused=True)
    for left, right, leaf in zip(ga, gb, leaves):
        left = torch.zeros_like(leaf) if left is None else left
        right = torch.zeros_like(leaf) if right is None else right
        assert torch.allclose(left, right, atol=1e-11, rtol=1e-11)


def test_selected_probability_gradient_and_renormalization_trap():
    logits = torch.tensor(
        [[1.0, 0.0, -1.0]], dtype=torch.float64, requires_grad=True
    )
    p = torch.softmax(logits, -1)
    value = 2 * p[0, 0]
    g = torch.autograd.grad(value, logits, retain_graph=True)[0]
    expected = 2 * p[0, 0] * (torch.tensor([[1.0, 0, 0]]) - p)
    assert torch.allclose(g, expected)
    broken = 2 * p[0, 0] / p[0, 0]
    assert torch.equal(
        torch.autograd.grad(broken, logits)[0], torch.zeros_like(logits)
    )


def test_gradcheck_away_from_switch_surfaces():
    x, logits, w, valid = fixture()
    assert torch.autograd.gradcheck(
        lambda z: ref.dispatch(x, w, ref.plan(z, valid, 2)), (logits,)
    )


def test_expert_permutation_away_from_ties():
    x, logits, w, valid = fixture()
    order = torch.tensor([2, 0, 1])
    a = ref.dispatch(x, w, ref.plan(logits, valid, 2))
    b = ref.dispatch(
        x,
        {k: v[order] for k, v in w.items()},
        ref.plan(logits[:, order], valid, 2),
    )
    assert torch.allclose(a, b, atol=1e-12)


def test_padding_does_not_consume_slots_or_balance_denominator():
    _, logits, _, valid = fixture()
    valid[0] = False
    p = ref.plan(logits, valid, 2)
    assert not p["accepted"][0] and p["accepted"][2]
    assert p["demand"] == [2, 2, 1]
    short = ref.plan(logits[1:], valid[1:], 2)
    assert torch.allclose(
        ref.balance_loss(p, valid), ref.balance_loss(short, valid[1:])
    )


def test_chunk_reset_breaks_parity_and_carried_capacity_restores_it():
    x, logits, w, valid = fixture()
    full = ref.dispatch(x, w, ref.plan(logits, valid, 2))
    first = ref.plan(logits[:2], valid[:2], 2)
    reset = ref.plan(logits[2:], valid[2:], 2)
    carried = ref.plan(logits[2:], valid[2:], 2, first["used"])
    wrong = torch.cat(
        (ref.dispatch(x[:2], w, first), ref.dispatch(x[2:], w, reset))
    )
    right = torch.cat(
        (ref.dispatch(x[:2], w, first), ref.dispatch(x[2:], w, carried))
    )
    assert not torch.allclose(full, wrong)
    assert torch.allclose(full, right, atol=1e-12)


def test_token_order_changes_overflow_not_routing_scores():
    x, logits, w, valid = fixture()
    order = torch.tensor([2, 1, 0, 3, 4, 5])
    a = ref.plan(logits, valid, 2)
    b = ref.plan(logits[order], valid, 2)
    assert a["accepted"][0] and not b["accepted"][2]


def test_balance_gradient_has_analytic_oracle():
    _, logits, _, valid = fixture()
    r = ref.plan(logits, valid, 2)
    g = torch.autograd.grad(ref.balance_loss(r, valid), logits)[0]
    p = r["probability"].detach()
    f = torch.tensor(r["demand"], dtype=p.dtype) / 6
    expected = (
        0.01 * 3 / 6 * p * (f[None, :] - (p * f).sum(-1, keepdim=True))
    )
    assert torch.allclose(g, expected, atol=1e-12)
    tied = ref.plan(torch.zeros_like(logits), valid, 2)
    assert ref.balance_loss(tied, valid).item() == pytest.approx(0.01)
    assert tied["demand"] == [
        6,
        0,
        0,
    ]  # numeric baseline is not balance proof


def test_sparse_block_replaces_only_ffn_and_keeps_residual_on_overflow():
    x, _, experts, valid = fixture()
    b = ref.base.parameters()["blocks"][0]
    router = (
        torch.linspace(-0.3, 0.5, 12, dtype=torch.float64)
        .reshape(4, 3)
        .requires_grad_()
    )
    result, p = ref.sparse_block(x, b, router, experts, valid, 0)
    attention, _ = ref.base.multihead(
        ref.base.layer_norm(x, b["g1"], b["n1"]), b, heads=2
    )
    assert torch.equal(result, x + attention)
    result, p = ref.sparse_block(x, b, router, experts, valid, 6)
    u = x + attention
    z = ref.base.layer_norm(u, b["g2"], b["n2"])
    oracle = u + ref.dense_oracle(z, experts, p)
    assert torch.allclose(result, oracle, atol=1e-12)
    leaves = [x, router] + list(experts.values()) + list(b.values())
    ga = torch.autograd.grad(
        result.sum(), leaves, retain_graph=True, allow_unused=True
    )
    gb = torch.autograd.grad(oracle.sum(), leaves, allow_unused=True)
    for a, c, leaf in zip(ga, gb, leaves):
        a = torch.zeros_like(leaf) if a is None else a
        c = torch.zeros_like(leaf) if c is None else c
        assert torch.allclose(a, c, atol=1e-10)


@pytest.mark.parametrize("capacity", [-1, 1.5, True])
def test_invalid_capacity(capacity):
    with pytest.raises(ValueError):
        ref.plan(
            torch.zeros(2, 3), torch.ones(2, dtype=torch.bool), capacity
        )


def test_one_expert_limit_recovers_chapter9_dense_block():
    x, _, _, valid = fixture()
    b = ref.base.parameters()["blocks"][0]
    expert = {k: b[k].unsqueeze(0) for k in ("w1", "b1", "w2", "b2")}
    router = torch.zeros(4, 1, dtype=torch.float64)
    sparse, _ = ref.sparse_block(x, b, router, expert, valid, 6)
    dense, _ = ref.base.block(x, b)
    assert torch.allclose(sparse, dense, atol=1e-12, rtol=1e-12)


def test_cost_and_record():
    assert ref.cost(6, 3, 4, 8, 5) == dict(
        router_macs=72,
        expert_macs=320,
        all_expert_macs=1152,
        expert_parameters=228,
    )
    assert ref.results() == json.loads(
        (ROOT / "drafts/ch10/results.json").read_text()
    )


def test_capacity_state_is_copied_and_zero_valid_balance_rejected():
    _, logits, _, valid = fixture()
    used = [1, 0, 0]
    ref.plan(logits, valid, 2, used)
    assert used == [1, 0, 0]
    invalid = torch.zeros_like(valid)
    r = ref.plan(logits, invalid, 2)
    assert r["used"] == [0, 0, 0] and r["demand"] == [0, 0, 0]
    with pytest.raises(ValueError):
        ref.balance_loss(r, invalid)
