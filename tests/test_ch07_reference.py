import importlib.util
import json
from pathlib import Path
import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evo07", ROOT / "drafts/ch07/reference.py"
)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def sample(n):
    a = (
        torch.linspace(0.1, 0.9, max(1, n * 3), dtype=torch.float64)[
            : n * 3
        ]
        .reshape(n, 3)
        .requires_grad_()
    )
    b = (
        torch.linspace(-0.5, 0.7, max(1, n * 3), dtype=torch.float64)[
            : n * 3
        ]
        .reshape(n, 3)
        .requires_grad_()
    )
    h = torch.tensor(
        [0.3, -0.1, 0.8], dtype=torch.float64, requires_grad=True
    )
    return a, b, h


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5, 8, 17, 64])
def test_prefix_forward_backward_and_all_lengths(n):
    a, b, h = sample(n)
    seq = M.sequential(a, b, h)
    scan = M.parallel_form(a, b, h)
    torch.testing.assert_close(seq, scan, rtol=1e-12, atol=1e-12)
    gs = torch.autograd.grad(
        seq.square().sum(), (a, b, h), retain_graph=True, allow_unused=True
    )
    gp = torch.autograd.grad(
        scan.square().sum(), (a, b, h), allow_unused=True
    )
    for left, right in zip(gs, gp):
        if left is None or right is None:
            assert n == 0
        else:
            torch.testing.assert_close(left, right, rtol=1e-12, atol=1e-12)


def test_associative_not_commutative_and_identity():
    p, q, r = (0.5, 1.0), (0.25, 2.0), (0.8, -1.0)
    assert M.compose(M.compose(p, q), r) == pytest.approx(
        M.compose(p, M.compose(q, r))
    )
    assert M.compose(p, q) == (0.125, 2.25)
    assert M.compose(q, p) == (0.125, 2.0)
    assert M.compose(p, (1.0, 0.0)) == p == M.compose((1.0, 0.0), p)


def test_hand_trace_nonzero_initial():
    assert [r["state"] for r in M.results()["trace"]] == pytest.approx(
        [2, 2, 2.5, 1]
    )


def test_gradcheck_scan_and_input_selection():
    a, b, h = sample(3)
    assert torch.autograd.gradcheck(M.parallel_form, (a, b, h))
    x = torch.tensor(
        [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]],
        dtype=torch.float64,
        requires_grad=True,
    )
    w = torch.tensor(
        [[0.2, -0.1], [0.3, 0.4]], dtype=torch.float64, requires_grad=True
    )
    bias = torch.zeros(2, dtype=torch.float64, requires_grad=True)
    decay = torch.tensor(
        [0.3, 1.0], dtype=torch.float64, requires_grad=True
    )

    def run(x, w, bias, decay):
        a, b = M.selected_coefficients(x, w, bias, decay)
        return M.parallel_form(a, b, torch.zeros(2, dtype=x.dtype))

    assert torch.autograd.gradcheck(run, (x, w, bias, decay))


@pytest.mark.parametrize("delta", [0.0, 1e-15, 0.1, 2.0, 100.0])
def test_zoh_exact_limits(delta):
    decay = torch.tensor(2.0, dtype=torch.float64)
    a, gain = M.zoh(decay, torch.tensor(delta, dtype=torch.float64))
    assert 0 <= a <= 1 and gain >= 0
    assert a + 2 * gain == pytest.approx(1, abs=1e-15)
    if 0 < delta < 1e-10:
        assert float(gain) == pytest.approx(delta, rel=1e-12, abs=0)


def test_padding_identity_and_record_reset():
    a, b, h = sample(5)
    pad_a = torch.cat([a, torch.ones((2, 3), dtype=a.dtype)])
    pad_b = torch.cat([b, torch.zeros((2, 3), dtype=b.dtype)])
    out = M.parallel_form(pad_a, pad_b, h)
    torch.testing.assert_close(out[-1], out[4])
    reset_a = torch.cat([a[:2], torch.zeros_like(a[2:3]), a[3:]])
    out = M.parallel_form(reset_a, b, h)
    torch.testing.assert_close(
        out[2:], M.sequential(reset_a[2:], b[2:], torch.zeros_like(h))
    )


@pytest.mark.parametrize("cut", [0, 1, 3, 7])
def test_chunk_carry_equivalence(cut):
    a, b, h = sample(7)
    left = M.parallel_form(a[:cut], b[:cut], h)
    carry = left[-1] if cut else h
    right = M.parallel_form(a[cut:], b[cut:], carry)
    torch.testing.assert_close(
        torch.cat([left, right]), M.sequential(a, b, h)
    )


def test_lti_convolution_and_selectivity_breaks_linearity():
    assert M.results()["lti_max_error"] == 0

    # y(x)=(1-exp(-softplus(x)))*x for a one-step, zero-state toy.
    def f(x):
        x = torch.tensor(float(x), dtype=torch.float64)
        return (1 - torch.exp(-torch.nn.functional.softplus(x))) * x

    assert abs(float(f(2) - 2 * f(1))) > 0.1


def test_work_count_linear_bound_and_invalid_shape():
    for n in range(1, 200):
        assert M.operation_count(n) < 2 * n
    assert M.operation_count(8) == 11
    with pytest.raises(ValueError):
        M.parallel_form(torch.ones(2), torch.ones(2), torch.ones(1))


def test_results_reproducible():
    assert (
        json.loads((ROOT / "drafts/ch07/results.json").read_text())
        == M.results()
    )
