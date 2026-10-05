from pathlib import Path
import importlib.util
import json
import math
import sys
import torch
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evo20", ROOT / "drafts/ch20/reference.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def fixture():
    x = torch.tensor(
        [[1.0, -1.0], [0.0, 2.0], [-1.0, 1.0], [2.0, 0.0], [1.0, 1.0]],
        dtype=torch.float64,
    )
    tau = torch.tensor([1.0, 3.0, 10.0], dtype=torch.float64)
    return x, tau


def equal(a, b):
    for field in ("bank", "coarse", "pending"):
        torch.testing.assert_close(getattr(a, field), getattr(b, field))
    assert a.phase == b.phase


def test_results():
    assert m.results() == json.loads(
        (ROOT / "drafts/ch20/results.json").read_text()
    )


@pytest.mark.parametrize("n", range(6))
def test_bank_matches_independent_convolution(n):
    x, tau = fixture()
    x = x[:n]
    final, history = m.multiscale(x, tau)
    torch.testing.assert_close(final.bank, m.convolution(x, tau))
    assert len(history) == n + 1
    assert final.bank.abs().max() <= 2


@pytest.mark.parametrize("block_size", [1, 2, 4, 8])
def test_every_chunk_split_and_clock(block_size):
    x, tau = fixture()
    whole, _ = m.multiscale(x, tau, block_size)
    for split in range(len(x) + 1):
        left, _ = m.multiscale(x[:split], tau, block_size)
        right, _ = m.multiscale(x[split:], tau, block_size, carry=left)
        equal(whole, right)
    assert whole.phase == len(x) % block_size
    remain = len(x) % block_size
    expected = x[-remain:].sum(0) if remain else torch.zeros_like(x[0])
    torch.testing.assert_close(whole.pending, expected)


def test_padding_holds_phase_and_all_state_and_no_alias_mutation():
    x, tau = fixture()
    carry, _ = m.multiscale(x[:2], tau)
    copies = [
        t.clone() for t in (carry.bank, carry.coarse, carry.pending)
    ]
    masked, _ = m.multiscale(x, tau, mask=[False] * 5, carry=carry)
    equal(carry, masked)
    m.multiscale(x, tau, carry=carry)
    for t, before in zip(
        (carry.bank, carry.coarse, carry.pending), copies
    ):
        torch.testing.assert_close(t, before)
    partial, _ = m.multiscale(
        x, tau, mask=[True, False, True, False, True]
    )
    expected, _ = m.multiscale(x[[0, 2, 4]], tau)
    equal(partial, expected)


def test_block_mean_aliasing_and_fast_state_separation():
    tau = torch.tensor([-1 / math.log(0.5)], dtype=torch.float64)
    first, _ = m.multiscale(
        torch.tensor([[1.0], [-1.0]], dtype=torch.float64), tau, 2
    )
    second, _ = m.multiscale(
        torch.tensor([[-1.0], [1.0]], dtype=torch.float64), tau, 2
    )
    assert first.coarse.item() == second.coarse.item() == 0
    assert first.bank.item() == -0.25 and second.bank.item() == 0.25


def test_gradcheck_and_chunk_gradient_parity():
    x, tau = fixture()
    x.requires_grad_()
    tau.requires_grad_()

    def output(x, tau):
        s, _ = m.multiscale(x, tau)
        return torch.cat([s.bank.flatten(), s.coarse, s.pending])

    assert torch.autograd.gradcheck(output, (x, tau))
    whole = output(x, tau).square().sum()
    grad1 = torch.autograd.grad(whole, (x, tau))
    left, _ = m.multiscale(x[:3], tau)
    right, _ = m.multiscale(x[3:], tau, carry=left)
    joined = torch.cat(
        [right.bank.flatten(), right.coarse, right.pending]
    )
    grad2 = torch.autograd.grad(joined.square().sum(), (x, tau))
    for a, b in zip(grad1, grad2):
        torch.testing.assert_close(a, b)


def test_discarded_partial_block_is_a_real_failure():
    x, tau = fixture()
    left, _ = m.multiscale(x[:3], tau)
    broken = m.Memory(
        left.bank, left.coarse, torch.zeros_like(left.pending), 0
    )
    wrong, _ = m.multiscale(x[3:], tau, carry=broken)
    correct, _ = m.multiscale(x, tau)
    assert not torch.allclose(wrong.coarse, correct.coarse)
    assert wrong.phase != correct.phase


def test_clock_semigroup_and_precision():
    tau = torch.tensor([1.0, 8.0, 1e18], dtype=torch.float64)
    a, b = m.retention(tau, 3)
    c, d = m.retention(tau, 5)
    whole, write = m.retention(tau, 8)
    torch.testing.assert_close(a * c, whole)
    torch.testing.assert_close(c * b + d, write)
    assert (
        m.retention(tau, 1)[1][-1] > 0
    )  # expm1 avoids 1-exp cancellation
    assert m.retention(tau, 0)[1].count_nonzero() == 0


def test_future_changes_cannot_alter_prefix_states():
    x, tau = fixture()
    _, original = m.multiscale(x, tau)
    changed = x.clone()
    changed[3:] = 1000
    _, alternative = m.multiscale(changed, tau)
    prefix, _ = m.multiscale(x[:3], tau)
    for before, after in zip(original[:4], alternative[:4]):
        equal(before, after)
    equal(prefix, original[3])


def test_coarse_gradient_is_committed_block_weight():
    x = torch.arange(8, dtype=torch.float64).reshape(8, 1)
    x.requires_grad_()
    tau = torch.tensor([2.0], dtype=torch.float64)
    final, history = m.multiscale(x, tau, block_size=4, rho=0.5)
    assert history[3].coarse.item() == 0
    first = torch.autograd.grad(
        history[4].coarse.sum(), x, retain_graph=True
    )[0]
    last = torch.autograd.grad(final.coarse.sum(), x)[0]
    torch.testing.assert_close(
        first[:, 0], torch.tensor([0.125] * 4 + [0.0] * 4, dtype=x.dtype)
    )
    torch.testing.assert_close(
        last[:, 0],
        torch.tensor([0.0625] * 4 + [0.125] * 4, dtype=x.dtype),
    )


def test_record_reset_and_invalid_contracts():
    x, tau = fixture()
    first, _ = m.multiscale(x, tau)
    isolated, _ = m.multiscale(x, tau)
    equal(first, isolated)
    leaked, _ = m.multiscale(x, tau, carry=first)
    assert not torch.allclose(first.bank, leaked.bank)
    for kwargs in ({"block_size": 0}, {"rho": 1.1}, {"mask": [1] * 5}):
        with pytest.raises(ValueError):
            m.multiscale(x, tau, **kwargs)
    with pytest.raises(ValueError):
        m.multiscale(x, -tau)
    with pytest.raises(ValueError):
        m.multiscale(
            x,
            tau,
            carry=m.Memory(
                first.bank,
                first.coarse,
                torch.ones_like(first.pending),
                0,
            ),
        )
