import importlib.util
import json
import math
from pathlib import Path
import pytest
import torch
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evo08", ROOT / "drafts/ch08/reference.py"
)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def data(n=5):
    gen = torch.Generator().manual_seed(808)
    return [
        torch.randn(
            (n, d), generator=gen, dtype=torch.float64, requires_grad=True
        )
        for d in [3, 3, 2]
    ]


def test_hand_retrieval():
    r = M.results()
    assert r["weights"][0] == pytest.approx([2 / 3, 1 / 3])
    assert r["output"][0] == pytest.approx([2, 2])


def test_packed_mask_and_zero_row():
    q, k, v = data()
    mask = M.packed_mask(
        torch.tensor([0, 0, 1, 1, 2]),
        torch.tensor([True, True, True, True, False]),
    )
    out, w = M.attention(q, k, v, mask)
    assert mask.int().tolist() == [
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    assert torch.equal(out[-1], torch.zeros_like(out[-1]))
    assert torch.equal(w[-1], torch.zeros_like(w[-1]))
    grads = torch.autograd.grad(out[-1].sum(), (q, k, v))
    assert all(torch.equal(g, torch.zeros_like(g)) for g in grads)


@pytest.mark.parametrize("packed", [False, True])
def test_library_forward_and_gradient_oracle(packed):
    q, k, v = data()
    mask = (
        M.packed_mask(
            torch.tensor([0, 0, 1, 1, 2]),
            torch.tensor([1, 1, 1, 1, 0], dtype=torch.bool),
        )
        if packed
        else M.offset_mask(5, 0)
    )
    ours, _ = M.attention(q, k, v, mask)
    theirs = F.scaled_dot_product_attention(
        q[None, None],
        k[None, None],
        v[None, None],
        attn_mask=mask,
        dropout_p=0.0,
    )[0, 0]
    torch.testing.assert_close(ours, theirs, rtol=1e-12, atol=1e-12)
    ga = torch.autograd.grad(
        ours.square().sum(), (q, k, v), retain_graph=True
    )
    gb = torch.autograd.grad(theirs.square().sum(), (q, k, v))
    for a, b in zip(ga, gb):
        torch.testing.assert_close(a, b, rtol=1e-11, atol=1e-12)


def test_mask_before_normalization_and_shift_invariance():
    scores = torch.tensor(
        [[math.log(2), 0.0, 1000.0], [1.0, 2.0, 3.0]],
        dtype=torch.float64,
        requires_grad=True,
    )
    mask = torch.tensor([[1, 1, 0], [0, 0, 0]], dtype=torch.bool)
    w = M.masked_softmax(scores, mask)
    assert w[0].tolist() == pytest.approx([2 / 3, 1 / 3, 0])
    torch.testing.assert_close(w, M.masked_softmax(scores + 10000, mask))
    assert torch.autograd.grad(w[:, 0].sum(), scores)[0][0, 2] == 0


def test_gradcheck():
    q, k, v = data(3)
    mask = M.offset_mask(3, 0)
    assert torch.autograd.gradcheck(
        lambda q, k, v: M.attention(q, k, v, mask)[0], (q, k, v)
    )


def test_future_and_record_isolation():
    q, k, v = data()
    mask = M.packed_mask(
        torch.tensor([0, 0, 1, 1, 1]), torch.ones(5, dtype=torch.bool)
    )
    before, _ = M.attention(q, k, v, mask)
    kk, vv = k.clone(), v.clone()
    kk[4] += 100
    vv[4] -= 100
    after, _ = M.attention(q, kk, vv, mask)
    torch.testing.assert_close(before[:4], after[:4])
    kk[:2] += 50
    vv[:2] += 50
    other, _ = M.attention(q, kk, vv, mask)
    torch.testing.assert_close(after[2:], other[2:])


@pytest.mark.parametrize("chunks", [[1, 1, 1, 1, 1], [2, 3], [3, 2], [5]])
def test_cached_chunks_forward_and_backward(chunks):
    q, k, v = data()
    full, _ = M.attention(q, k, v, M.offset_mask(5, 0))
    outputs = []
    cache = None
    start = 0
    for size in chunks:
        stop = start + size
        part, cache = M.cached_chunk(
            q[start:stop], k[start:stop], v[start:stop], cache
        )
        outputs.append(part)
        start = stop
    joined = torch.cat(outputs)
    torch.testing.assert_close(joined, full, rtol=1e-12, atol=1e-12)
    a = torch.autograd.grad(
        joined.square().sum(), (q, k, v), retain_graph=True
    )
    b = torch.autograd.grad(full.square().sum(), (q, k, v))
    for left, right in zip(a, b):
        torch.testing.assert_close(left, right, rtol=1e-11, atol=1e-12)


def test_rectangular_causal_negative_control():
    q, k, v = data()
    correct, _ = M.attention(q[3:], k, v, M.offset_mask(2, 3))
    wrong = F.scaled_dot_product_attention(
        q[3:][None, None],
        k[None, None],
        v[None, None],
        is_causal=True,
        dropout_p=0.0,
    )[0, 0]
    assert (correct - wrong).abs().max() > 0.01


@pytest.mark.parametrize("h", [1, 2, 4])
def test_head_mapping(h):
    x = torch.arange(2 * 3 * 8).reshape(2, 3, 8)
    split = M.split_heads(x, h)
    assert split.shape == (2, h, 3, 8 // h)
    assert torch.equal(M.merge_heads(split), x)
    assert torch.equal(split[1, h - 1, 2], x[1, 2, (h - 1) * (8 // h) :])


def test_invalid_contracts():
    q, k, v = data()
    with pytest.raises(ValueError):
        M.attention(q, k, v, torch.ones(5, 5))
    with pytest.raises(ValueError):
        M.masked_softmax(
            torch.tensor([[float("inf")]]),
            torch.ones(1, 1, dtype=torch.bool),
        )
    with pytest.raises(ValueError):
        M.split_heads(torch.ones(1, 2, 7), 2)


def test_record_matches_reference():
    assert (
        json.loads((ROOT / "drafts/ch08/results.json").read_text())
        == M.results()
    )
