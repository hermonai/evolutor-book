from pathlib import Path
from itertools import product
import importlib.util
import json
import math
import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evo19", ROOT / "drafts/ch19/reference.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
torch.set_num_threads(1)


def test_results_reproduce():
    assert m.results() == json.loads(
        (ROOT / "drafts/ch19/results.json").read_text()
    )


def test_collision_repaired_without_claiming_capability():
    v, u, r = m.tables()
    x = m.selective_scan(m.pair_ids("AACA")[0], v, u, r)[0].item()
    y = m.selective_scan(m.pair_ids("ACAA")[0], v, u, r)[0].item()
    assert x == -1 / 16 and y == -3 / 64
    assert sorted(zip("AACA", "ACA")) == sorted(zip("ACAA", "CAA"))


def test_every_short_chunk_boundary_and_prefix_causality():
    v, u, r = m.tables()
    for n in range(5):
        for chars in product("AC", repeat=n):
            s = "".join(chars)
            whole, history = m.selective_scan(m.pair_ids(s)[0], v, u, r)
            for split in range(n + 1):
                ids, previous = m.pair_ids(s[:split])
                h, _ = m.selective_scan(ids, v, u, r)
                tail, last = m.pair_ids(s[split:], previous)
                joined, _ = m.selective_scan(tail, v, u, r, h)
                assert torch.equal(joined, whole)
                assert torch.equal(h, history[split])
                assert last == (s[-1] if s else "")
            mutated = s + "GT"
            _, longer = m.selective_scan(m.pair_ids(mutated)[0], v, u, r)
            assert all(torch.equal(a, b) for a, b in zip(history, longer))


def test_mask_identity_and_record_reset_are_distinct():
    v, u, r = m.tables()
    state = torch.tensor([0.3], dtype=torch.float64)
    final, h = m.selective_scan((-1, -1), v, u, r, state)
    assert final is state and all(x is state for x in h)
    split = m.pair_ids("C")[0]
    carried = m.pair_ids("C", "A")[0]
    assert split == (-1,) and carried == (m.PAIRS.index("AC"),)


def test_expanded_recurrence_and_range():
    gen = torch.Generator().manual_seed(19)
    v = torch.randn(16, 3, dtype=torch.float64, generator=gen)
    u = torch.randn(16, 3, dtype=torch.float64, generator=gen)
    r = torch.randn(16, 3, dtype=torch.float64, generator=gen)
    ids = m.pair_ids("AACGTTACAG")[0]
    start = torch.randn(3, dtype=torch.float64, generator=gen)
    a = 1 - torch.sigmoid(u) * (1 - torch.sigmoid(r))
    selected = [i for i in ids if i >= 0]
    expected = start * torch.prod(a[selected], dim=0)
    for j, i in enumerate(selected):
        expected = expected + (1 - a[i]) * v[i] * torch.prod(
            a[selected[j + 1 :]], dim=0
        )
    got, history = m.selective_scan(ids, v, u, r, start)
    assert torch.allclose(got, expected, rtol=1e-12, atol=1e-12)
    bound = max(v.abs().max(), start.abs().max())
    assert all((h.abs() <= bound + 1e-12).all() for h in history)


def test_scalar_analytic_gradients_and_feedback_counterexample():
    h = torch.tensor(0.0, dtype=torch.float64, requires_grad=True)
    v = torch.tensor(1.0, dtype=torch.float64, requires_grad=True)
    u = torch.tensor(0.0, dtype=torch.float64, requires_grad=True)
    r = torch.tensor(0.0, dtype=torch.float64, requires_grad=True)
    a, _, _ = m.coefficients(u, r)
    grads = torch.autograd.grad(a * h + (1 - a) * v, (h, v, u, r))
    assert [x.item() for x in grads] == pytest.approx(
        [0.75, 0.25, 0.125, -0.125]
    )
    derivative = torch.autograd.grad(m.feedback_step(h), h)[0]
    assert derivative.item() == pytest.approx(2.5)
    eps = 1e-6
    fd = (
        m.feedback_step(torch.tensor(eps, dtype=torch.float64))
        - m.feedback_step(torch.tensor(-eps, dtype=torch.float64))
    ) / (2 * eps)
    assert fd.item() == pytest.approx(2.5, rel=1e-8)


def test_gradcheck_and_chunk_gradient_parity():
    v, u, r = [t.requires_grad_() for t in m.tables()]
    ids = m.pair_ids("AACAA")[0]
    fn = lambda vv, uu, rr: m.selective_scan(ids, vv, uu, rr)[0]
    assert torch.autograd.gradcheck(fn, (v, u, r), eps=1e-6, atol=1e-5)
    whole = fn(v, u, r).sum()
    expected = torch.autograd.grad(whole, (v, u, r))
    h = m.selective_scan(ids[:3], v, u, r)[0]
    split = m.selective_scan(ids[3:], v, u, r, h)[0].sum()
    actual = torch.autograd.grad(split, (v, u, r))
    assert all(torch.allclose(a, b) for a, b in zip(actual, expected))
    h = m.selective_scan(ids[:3], v, u, r)[0].detach()
    truncated = m.selective_scan(ids[3:], v, u, r, h)[0].sum()
    broken = torch.autograd.grad(truncated, (v, u, r))
    assert any(not torch.allclose(a, b) for a, b in zip(broken, expected))


def test_distinct_gates_are_functionally_nonidentifiable():
    v, u, r = m.tables()
    for seq in ("", "AACA", "ACAA", "AACACA"):
        ids = m.pair_ids(seq)[0]
        one = m.selective_scan(ids, v, u, r)[0]
        two = m.selective_scan(ids, v, u + math.log(3), r + math.log(2))[0]
        assert torch.allclose(one, two, atol=1e-14, rtol=1e-14)


@pytest.mark.parametrize("ids", [(16,), (-2,), (True,), (1.5,)])
def test_invalid_ids_do_not_mutate_caller(ids):
    v, u, r = m.tables()
    h = torch.tensor([0.3], dtype=torch.float64)
    before = h.clone()
    with pytest.raises(ValueError):
        m.selective_scan(ids, v, u, r, h)
    assert torch.equal(h, before)


def test_invalid_shapes_and_symbols():
    v, u, r = m.tables()
    with pytest.raises(ValueError):
        m.selective_scan((1,), v, u[:2], r)
    with pytest.raises(ValueError):
        m.pair_ids("ANC")
    with pytest.raises(ValueError):
        m.selective_scan((1,), v, u, r, torch.zeros(2, dtype=torch.float64))
