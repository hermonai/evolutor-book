import importlib.util
from pathlib import Path
import sys
import torch
import pytest

path = Path(__file__).parents[1] / "drafts/ch26/reference.py"
spec = importlib.util.spec_from_file_location("evo26", path)
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def sample(t=19, shape=(4,), dtype=torch.float64):
    g = torch.Generator().manual_seed(9)
    return (
        torch.rand((t,) + shape, generator=g, dtype=dtype) * 1.8 - 0.9,
        torch.randn((t,) + shape, generator=g, dtype=dtype) * 0.1,
        torch.randn(shape, generator=g, dtype=dtype),
    )


def assert_close(x, y, atol=1e-12):
    torch.testing.assert_close(x, y, atol=atol, rtol=atol)


def test_no_global_dtype_side_effect():
    before = torch.get_default_dtype()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert torch.get_default_dtype() == before


def test_composition_order_noncommutative_and_identity():
    x = (torch.tensor([2.0]), torch.tensor([1.0]))
    y = (torch.tensor([3.0]), torch.tensor([4.0]))
    assert r.compose(x, y)[1].item() == 7
    assert r.compose(y, x)[1].item() == 9
    identity = (torch.ones(1), torch.zeros(1))
    for side in (r.compose(x, identity), r.compose(identity, x)):
        assert_close(side[0], x[0])
        assert_close(side[1], x[1])


def test_associativity_against_homogeneous_matrices():
    # Independently constructed 2x2 homogeneous matrices for scalar affine maps.
    x, y, z = ((0.7, 0.2), (0.8, -0.1), (0.9, 0.3))
    tensors = [
        tuple(torch.tensor([v], dtype=torch.float64) for v in pair)
        for pair in (x, y, z)
    ]

    def matrix(pair):
        return torch.tensor([[pair[0], pair[1]], [0.0, 1.0]], dtype=torch.float64)

    target = matrix(z) @ matrix(y) @ matrix(x)
    for result in (
        r.compose(r.compose(tensors[0], tensors[1]), tensors[2]),
        r.compose(tensors[0], r.compose(tensors[1], tensors[2])),
    ):
        assert_close(result[0], target[0, 0].reshape(1))
        assert_close(result[1], target[0, 1].reshape(1))


@pytest.mark.parametrize("t", [0, 1, 2, 3, 4, 7, 17, 33])
def test_all_schedules_against_closed_form(t):
    a, b, h = sample(t)
    seq, final = r.sequential(a, b, h)
    direct = r.closed_form(a, b, h)
    scan, scan_last = r.scan_states(a, b, h)
    assert_close(seq, direct)
    assert_close(scan, direct)
    assert_close(final, scan_last)
    for chunk in (1, 2, 3, 5, 19, 64):
        got, last = r.chunked(a, b, h, chunk)
        assert_close(got, direct)
        assert_close(last, final)


def test_zero_negative_and_expansive_coefficients():
    a = torch.tensor([[0.5], [2.0], [0.0], [-1.0]], dtype=torch.float64)
    b = torch.tensor([[1.0], [0.5], [3.0], [2.0]], dtype=torch.float64)
    h = torch.tensor([2.0], dtype=torch.float64)
    expected = torch.tensor([[2.0], [4.5], [3.0], [-1.0]], dtype=torch.float64)
    assert_close(r.scan_states(a, b, h)[0], expected)
    assert_close(r.closed_form(a, b, h), expected)


def test_gradient_parity_against_manual_adjoint():
    a, b, h = (x.requires_grad_() for x in sample(9))
    weights = torch.arange(36, dtype=torch.float64).reshape(9, 4) / 17 - 1
    expected = r.analytic_adjoint(a.detach(), b.detach(), h.detach(), weights)
    for states in (
        r.sequential(a, b, h)[0],
        r.scan_states(a, b, h)[0],
        r.chunked(a, b, h, 3)[0],
        r.closed_form(a, b, h),
    ):
        grads = torch.autograd.grad(
            (states * weights).sum(), (a, b, h), retain_graph=True
        )
        for actual, oracle in zip(grads, expected):
            assert_close(actual, oracle)


def test_finite_difference_gradient_with_zero_coefficients():
    a, b, h = (x.requires_grad_() for x in sample(5, (2,)))
    with torch.no_grad():
        a[2, 0] = 0

    def loss(aa, bb, hh):
        return r.scan_states(aa, bb, hh)[0].square().sum()

    gradients = torch.autograd.grad(loss(a, b, h), (a, b, h))
    inputs = (a.detach(), b.detach(), h.detach())
    eps = 1e-6
    for which, index in [(0, (2, 0)), (0, (0, 1)), (1, (3, 0)), (2, (1,))]:
        plus, minus = [x.clone() for x in inputs], [x.clone() for x in inputs]
        plus[which][index] += eps
        minus[which][index] -= eps
        fd = (loss(*plus) - loss(*minus)) / (2 * eps)
        assert gradients[which][index].item() == pytest.approx(
            fd.item(), abs=1e-8, rel=1e-7
        )


def test_reset_and_padding_literal_oracle_all_chunks():
    a, b, initial = sample(11, (2, 3))
    reset_state = torch.full_like(initial, 0.25)
    valid = torch.tensor(
        [True, False, True, True, False, True, True, True, False, True, True]
    )
    reset = torch.tensor(
        [True, False, False, True, False, False, True, False, False, False, True]
    )
    state, expected = initial, []
    for i in range(11):
        if valid[i]:
            if reset[i]:
                state = reset_state
            state = a[i] * state + b[i]
        expected.append(state)
    expected = torch.stack(expected)
    assert_close(r.scan_states(a, b, initial, reset, valid, reset_state)[0], expected)
    assert_close(r.sequential(a, b, initial, reset, valid, reset_state)[0], expected)
    for k in (1, 2, 3, 5, 20):
        assert_close(
            r.chunked(a, b, initial, k, reset, valid, reset_state)[0], expected
        )


def test_reset_zeroes_cross_record_gradient_and_future_perturbation():
    a, b, h = (x.requires_grad_() for x in sample(8, (2,)))
    reset = torch.tensor([False, False, False, False, True, False, False, False])
    zero = torch.zeros_like(h)
    states, _ = r.scan_states(a, b, h, reset, h_reset=zero)
    gradient = torch.autograd.grad(states[-1].sum(), b)[0]
    assert torch.count_nonzero(gradient[:4]) == 0
    changed = b.detach().clone()
    changed[6:] += 3
    other, _ = r.scan_states(a.detach(), changed, h.detach(), reset, h_reset=zero)
    assert_close(states.detach()[:6], other[:6])


def test_gradient_parity_for_reset_state_and_padding():
    a, b, h = (x.requires_grad_() for x in sample(8, (2,)))
    hr = torch.tensor([0.2, -0.3], dtype=torch.float64, requires_grad=True)
    reset = torch.tensor([False, False, True, False, False, True, False, False])
    valid = torch.tensor([True, False, True, True, True, True, False, True])
    reference = r.sequential(a, b, h, reset, valid, hr)[0]
    target = torch.autograd.grad(
        reference.square().sum(), (a, b, h, hr), retain_graph=True
    )
    for states in (
        r.scan_states(a, b, h, reset, valid, hr)[0],
        r.chunked(a, b, h, 3, reset, valid, hr)[0],
    ):
        gradients = torch.autograd.grad(
            states.square().sum(), (a, b, h, hr), retain_graph=True
        )
        for got, expected in zip(gradients, target):
            assert_close(got, expected)
    assert torch.count_nonzero(target[0][~valid]) == 0
    assert torch.count_nonzero(target[1][~valid]) == 0


def test_detach_mutant_preserves_values_not_gradients():
    a, b, h = (x.requires_grad_() for x in sample(8, (2,)))
    full, _ = r.chunked(a, b, h, 4)
    broken, _ = r.chunked(a, b, h, 4, detach=True)
    assert_close(full, broken)
    good_grad = torch.autograd.grad(full[-1].sum(), b, retain_graph=True)[0]
    bad_grad = torch.autograd.grad(broken[-1].sum(), b)[0]
    assert torch.count_nonzero(bad_grad[:4]) == 0
    assert torch.count_nonzero(good_grad[:4]) > 0


def test_stage_snapshot_mutant_fails():
    # Deliberately update left-to-right within a stage, reusing changed prefix values.
    a, b, h = sample(7, (1,))
    aa, bb = a.clone(), b.clone()
    offset = 1
    while offset < len(a):
        for i in range(offset, len(a)):
            bb[i] = aa[i] * bb[i - offset] + bb[i]
            aa[i] = aa[i] * aa[i - offset]
        offset *= 2
    bad = aa * h + bb
    assert not torch.allclose(bad, r.closed_form(a, b, h), atol=1e-12, rtol=1e-12)


def test_cancellation_is_a_declared_numerical_counterexample():
    values = r.results()
    assert values["cancellation_sequential_final"] == 1
    assert values["cancellation_scan_final"] == 0


@pytest.mark.parametrize(
    "dtype,tolerance", [(torch.float64, 1e-12), (torch.float32, 3e-6)]
)
def test_long_contracting_input_dtype_tolerance(dtype, tolerance):
    a, b, h = sample(1024, (3,), dtype)
    assert_close(r.scan_states(a, b, h)[0], r.sequential(a, b, h)[0], tolerance)


def test_batch_rows_are_independent():
    a, b, h = sample(9, (2, 3))
    result, _ = r.scan_states(a, b, h)
    changed = b.clone()
    changed[:, 1] += 10
    other, _ = r.scan_states(a, changed, h)
    assert_close(other[:, 0], result[:, 0])


def test_work_count_independent_nested_loop():
    for t in range(40):
        count = sum(1 for k in range(t.bit_length()) for i in range(t) if i >= 2**k)
        assert r.work_depth(t)["pair_compositions"] == count
    assert r.work_depth(1024)["pair_compositions"] == 9217


@pytest.mark.parametrize("chunk", [0, -1, True, 1.5])
def test_invalid_chunk(chunk):
    with pytest.raises(ValueError):
        r.chunked(*sample(), chunk)


def test_invalid_shape_dtype_and_nonfinite_inputs():
    a, b, h = sample()
    for inputs in [
        (a, b[:-1], h),
        (a, b, h[:-1]),
        (a.float(), b, h),
        (a.long(), b.long(), h.long()),
        (a + float("nan"), b, h),
    ]:
        with pytest.raises(ValueError):
            r.scan_states(*inputs)


def test_mask_contracts():
    a, b, h = sample(4)
    for mask in (torch.ones(4), torch.ones(3, dtype=torch.bool)):
        with pytest.raises(ValueError):
            r.scan_states(a, b, h, resets=mask)
    with pytest.raises(ValueError, match="Padding"):
        r.scan_states(
            a, b, h, torch.ones(4, dtype=torch.bool), torch.zeros(4, dtype=torch.bool)
        )
