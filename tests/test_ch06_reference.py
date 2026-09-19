import importlib.util
from pathlib import Path
import json
import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evo06", ROOT / "drafts/ch06/reference.py"
)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def test_gru_forward_and_all_gradient_parity():
    result = M.parity()
    assert result["max_forward_error"] < 1e-12
    assert result["max_gradient_error"] < 1e-12


def test_gru_hand_case():
    p = tuple(torch.zeros_like(v) for v in M.assigned_parameters())
    x = torch.tensor([[0.2, 0.8]], dtype=torch.float64)
    h = torch.tensor([[0.6, -0.2]], dtype=torch.float64, requires_grad=True)
    y = M.gru_step(x, h, p)
    assert torch.equal(y, 0.5 * h)
    assert torch.equal(
        torch.autograd.grad(y.sum(), h)[0], torch.full_like(h, 0.5)
    )


def test_finite_difference_gru_gradients():
    x = torch.tensor([[0.2, -0.1]], dtype=torch.float64, requires_grad=True)
    h = torch.tensor([[0.1, 0.4]], dtype=torch.float64, requires_grad=True)
    p = M.assigned_parameters()
    assert torch.autograd.gradcheck(
        lambda x, h, *p: M.gru_step(x, h, p), (x, h, *p)
    )


def test_lstm_forward_and_gradient_parity():
    p = M.assigned_parameters(gates=4)
    cell = torch.nn.LSTMCell(2, 2, dtype=torch.float64)
    q = (cell.weight_ih, cell.weight_hh, cell.bias_ih, cell.bias_hh)
    with torch.no_grad():
        for dst, src in zip(q, p):
            dst.copy_(src)
    x = torch.tensor([[0.2, -0.1]], dtype=torch.float64, requires_grad=True)
    h = torch.tensor([[0.1, 0.4]], dtype=torch.float64, requires_grad=True)
    c = torch.tensor([[0.7, -0.2]], dtype=torch.float64, requires_grad=True)
    actual = M.lstm_step(x, (h, c), p)
    expected = cell(x, (h, c))
    for a, b in zip(actual, expected):
        assert torch.allclose(a, b, atol=1e-12, rtol=0)
    a = torch.autograd.grad(
        sum(v.square().sum() for v in actual), (x, h, c, *p)
    )
    b = torch.autograd.grad(
        sum(v.square().sum() for v in expected), (x, h, c, *q)
    )
    for ga, gb in zip(a, b):
        assert torch.allclose(ga, gb, atol=1e-12, rtol=0)


def test_reset_order_counterexample():
    w = torch.tensor([[1.0, 1.0], [1.0, -1.0]], dtype=torch.float64)
    r = torch.tensor([0.2, 0.8], dtype=torch.float64)
    h = torch.tensor([1.0, 2.0], dtype=torch.float64)
    assert (r * (w @ h)).tolist() == pytest.approx([0.6, -0.8])
    assert (w @ (r * h)).tolist() == pytest.approx([1.8, -1.4])


@pytest.mark.parametrize("cut", range(5))
def test_all_streaming_boundaries(cut):
    x = torch.arange(8, dtype=torch.float64).reshape(1, 4, 2) / 8
    h = torch.zeros(1, 2, dtype=torch.float64)
    p = M.assigned_parameters()
    y, last = M.scan_gru(x, h, p)
    a, boundary = M.scan_gru(x[:, :cut], h, p)
    b, final = M.scan_gru(x[:, cut:], boundary, p)
    assert torch.equal(torch.cat((a, b), 1), y)
    assert torch.equal(final, last)


def test_padding_holds_state_and_blocks_finite_padding_gradients():
    x = (
        torch.arange(12, dtype=torch.float64)
        .reshape(2, 3, 2)
        .requires_grad_()
    )
    p = M.assigned_parameters()
    h = torch.zeros(2, 2, dtype=torch.float64)
    y, last = M.scan_gru(x, h, p, torch.tensor([1, 0]))
    assert torch.equal(y[0, 0], y[0, 2])
    assert torch.equal(last[1], h[1])
    (gx,) = torch.autograd.grad(last.sum(), x)
    assert torch.equal(gx[0, 1:], torch.zeros_like(gx[0, 1:]))
    assert torch.equal(gx[1], torch.zeros_like(gx[1]))


@pytest.mark.parametrize(
    "lengths", [torch.tensor([-1]), torch.tensor([4]), torch.tensor([1.0])]
)
def test_invalid_lengths(lengths):
    with pytest.raises(ValueError):
        M.scan_gru(
            torch.zeros(1, 3, 2, dtype=torch.float64),
            torch.zeros(1, 2, dtype=torch.float64),
            M.assigned_parameters(),
            lengths,
        )


@pytest.mark.parametrize("z", [0.5, 0.9, 0.99])
def test_retention_derivative(z):
    for steps in (0, 1, 10, 100):
        r = M.scalar_retention(z, steps)
        assert r["state"] == pytest.approx(z**steps)
        assert r["gradient"] == pytest.approx(z**steps)


def test_chunk_values_and_distinct_gradients():
    full = M.chunk_experiment()
    detach = M.chunk_experiment(detach=True)
    reset = M.chunk_experiment(reset=True)
    assert full == {
        "final": 6.125,
        "input_gradient": [0.125, 0.25, 0.5, 1.0],
        "parameter_gradient": 5.75,
    }
    assert detach == {
        "final": 6.125,
        "input_gradient": [0.0, 0.0, 0.5, 1.0],
        "parameter_gradient": 5.5,
    }
    assert reset == {
        "final": 5.5,
        "input_gradient": [0.0, 0.0, 0.5, 1.0],
        "parameter_gradient": 3.0,
    }


def test_future_inputs_do_not_change_prefix_states():
    p = M.assigned_parameters()
    x = torch.zeros(1, 4, 2, dtype=torch.float64)
    changed = x.clone()
    changed[:, 2:] = 100
    h = torch.zeros(1, 2, dtype=torch.float64)
    assert torch.equal(
        M.scan_gru(x, h, p)[0][:, :2], M.scan_gru(changed, h, p)[0][:, :2]
    )


def test_generated_results():
    assert (
        json.loads((ROOT / "drafts/ch06/results.json").read_text())
        == M.results()
    )
