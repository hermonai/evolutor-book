"""Independent loss, derivative, optimizer and stochastic-replay oracles."""

import importlib.util
from pathlib import Path
import sys
import pytest
import torch

path = Path(__file__).parents[1] / "drafts/ch27/reference.py"
spec = importlib.util.spec_from_file_location("evo27", path)
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
torch.set_num_threads(1)


def error(a, b):
    return max((x - y).abs().max().item() for x, y in zip(a, b))


@pytest.mark.parametrize("micro", [1, 2, 5, 12, 20])
def test_accumulated_loss_and_gradient(micro):
    m = r.make_model()
    x, y, w = r.data()
    lf, gf = r.full_grad(m, x, y, w)
    la, ga = r.accumulated_grad(m, x, y, w, micro)
    assert abs(lf - la) < 1e-12 and error(gf, ga) < 1e-12


def test_independent_loop_loss_and_manual_last_layer_derivative():
    m = r.make_model()
    x, y, w = r.data()
    loss, g = r.full_grad(m, x, y, w)
    h = torch.tanh(m.l1(x)).detach()
    p = m(x).detach()
    mass = sum(float(w[i, j]) for i in range(len(x)) for j in range(y.shape[1]))
    oracle = (
        sum(
            float(w[i, j]) * (float(p[i, j]) - float(y[i, j])) ** 2
            for i in range(len(x))
            for j in range(y.shape[1])
        )
        / mass
    )
    derivative = 2 * w * (p - y) / mass
    assert abs(loss - oracle) < 1e-12
    assert torch.allclose(g[2], derivative.T @ h, atol=1e-12, rtol=0)
    assert torch.allclose(g[3], derivative.sum(0), atol=1e-12, rtol=0)


def test_first_layer_central_difference():
    m = r.make_model()
    x, y, w = r.data()
    _, g = r.full_grad(m, x, y, w)
    original = m.l1.weight[0, 0].item()
    values = []
    with torch.no_grad():
        for delta in (1e-6, -1e-6):
            m.l1.weight[0, 0] = original + delta
            values.append((((m(x) - y) ** 2 * w).sum() / w.sum()).item())
        m.l1.weight[0, 0] = original
    assert abs((values[0] - values[1]) / 2e-6 - g[0][0, 0].item()) < 1e-8


def test_weight_scaling_invariant_and_zero_mass_micro():
    m = r.make_model()
    x, y, w = r.data()
    w[:5] = 0
    lf, gf = r.full_grad(m, x, y, w)
    la, ga = r.accumulated_grad(m, x, y, w, 5)
    ls, gs = r.full_grad(m, x, y, w * 7)
    assert abs(lf - la) < 1e-12 and abs(lf - ls) < 1e-12
    assert error(gf, ga) < 1e-12 and error(gf, gs) < 1e-12


@pytest.mark.parametrize("micro", [0, -1, True, 1.5])
def test_invalid_micro(micro):
    with pytest.raises(ValueError):
        r.accumulated_grad(r.make_model(), *r.data(), micro)


@pytest.mark.parametrize(
    "kind", ["negative", "zero", "nan", "shape", "grad", "overflow"]
)
def test_invalid_weights(kind):
    x, y, w = r.data()
    if kind == "negative":
        w[0, 0] = -1
    if kind == "zero":
        w.zero_()
    if kind == "nan":
        w[0, 0] = float("nan")
    if kind == "shape":
        w = w[:, :1]
    if kind == "grad":
        w.requires_grad_()
    if kind == "overflow":
        w.fill_(1e308)
    with pytest.raises(ValueError):
        r.validate_batch(x, y, w)


def test_no_silent_target_broadcasting():
    x, y, w = r.data()
    with pytest.raises(ValueError):
        r.weighted_sum(r.make_model()(x), y[:, :1], w[:, :1])


def test_initialization_restores_rng_and_dtype():
    state = torch.get_rng_state().clone()
    dtype = torch.get_default_dtype()
    a = r.make_model()
    b = r.make_model()
    r.data()
    assert torch.equal(torch.get_rng_state(), state)
    assert torch.get_default_dtype() == dtype
    assert all(torch.equal(x, y) for x, y in zip(a.parameters(), b.parameters()))


def test_checkpoint_all_gradients():
    m = r.make_model()
    x, y, w = r.data()
    lf, gf = r.full_grad(m, x, y, w)
    lc, gc = r.checkpoint_grad(m, x, y, w)
    assert lf == lc and error(gf, gc) < 1e-12


def test_rng_replay_preserves_gradient_and_caller_trajectory():
    m = r.make_model()
    x, y, w = r.data()
    with torch.random.fork_rng(devices=[]):
        start = torch.get_rng_state().clone()
        lp, gp = r.ordinary_dropout_grad(m, x, y, w, 0.4)
        after = torch.get_rng_state().clone()
        torch.set_rng_state(start)
        lc, gc = r.checkpoint_grad(m, x, y, w, 0.4, True)
        assert torch.equal(after, torch.get_rng_state())
        torch.set_rng_state(start)
        lb, gb = r.checkpoint_grad(m, x, y, w, 0.4, False)
    assert lp == lc == lb and error(gp, gc) < 1e-12 and error(gp, gb) > 0.01


def test_wrong_local_mean_mutant_detected():
    assert r.parity()["wrong_local_mean_gradient_error"] > 0.1


@pytest.mark.parametrize("micro", [1, 5, 20])
def test_actual_adam_update_and_moments_match(micro):
    sf, mf, gf = r.update_probe(None)
    sa, ma, ga = r.update_probe(micro)
    assert error(tuple(sf.values()), tuple(sa.values())) < 1e-12
    assert error(gf, ga) < 1e-12
    assert (
        error(
            tuple(x for pair in mf for x in pair), tuple(x for pair in ma for x in pair)
        )
        < 1e-12
    )
    initial = r.make_model()
    for theta, g, (moment, variance), updated in zip(
        initial.parameters(), gf, mf, sf.values()
    ):
        oracle, mm, vv = r.adam_step(
            theta.detach(), g, torch.zeros_like(g), torch.zeros_like(g), 1
        )
        assert torch.allclose(oracle, updated, atol=1e-12, rtol=0)
        assert torch.allclose(mm, moment, atol=1e-12, rtol=0)
        assert torch.allclose(vv, variance, atol=1e-12, rtol=0)


def test_two_step_scalar_adam_independent_arithmetic():
    theta = torch.tensor([2.0], dtype=torch.float64)
    m = torch.zeros_like(theta)
    v = m.clone()
    scalar = 2.0
    mm = vv = 0.0
    for step, gradient in enumerate((0.5, -0.25), 1):
        theta, m, v = r.adam_step(
            theta, torch.tensor([gradient], dtype=torch.float64), m, v, step
        )
        mm = 0.9 * mm + 0.1 * gradient
        vv = 0.999 * vv + 0.001 * gradient**2
        scalar -= (
            0.01 * (mm / (1 - 0.9**step)) / ((vv / (1 - 0.999**step)) ** 0.5 + 1e-8)
        )
        assert abs(theta.item() - scalar) < 1e-14


@pytest.mark.parametrize(
    "kwargs",
    [
        {"step": 0},
        {"step": True},
        {"lr": -1},
        {"beta1": 1},
        {"beta2": -1},
        {"epsilon": 0},
    ],
)
def test_adam_domains(kwargs):
    t = torch.ones(1, dtype=torch.float64)
    args = dict(step=1)
    args.update(kwargs)
    with pytest.raises(ValueError):
        r.adam_step(t, t, t, t, **args)


def test_static_accounting_not_runtime_peak():
    assert sum(p.numel() for p in r.make_model().parameters()) == 195
    assert r.adam_bytes(195) == 3120
    assert r.adam_bytes(195, 8, 8, 8) == 6240
    assert r.adam_bytes(195, 2, 2, 4, 4) == 3120
    assert r.chain_checkpoint_inventory(64, 8)["toy_live_slots"] == 16


def test_declared_microbatch_weight_masses_and_clipping_order():
    _, _, w = r.data()
    assert [w[a:b].sum().item() for a, b in ((0, 5), (5, 10), (10, 12))] == [12, 13, 6]

    def clip(v):
        return max(-1, min(1, v))

    assert clip(2) + clip(-1.5) == 0
    assert clip(2 - 1.5) == 0.5


@pytest.mark.parametrize("layers,block", [(0, 1), (1, 0), (True, 1), (1, 1.5)])
def test_inventory_domains(layers, block):
    with pytest.raises(ValueError):
        r.chain_checkpoint_inventory(layers, block)
