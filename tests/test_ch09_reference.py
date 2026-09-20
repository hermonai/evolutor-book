import importlib.util
import json
from pathlib import Path
import pytest
import torch
from torch.nn import functional as F

torch.set_num_threads(1)
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evo_ch09", ROOT / "drafts/ch09/reference.py"
)
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


@pytest.mark.parametrize("constant", [False, True])
def test_normalization_forward_backward_and_vjp(constant):
    x = torch.arange(12, dtype=torch.float64).reshape(3, 4)
    if constant:
        x = torch.full_like(x, 2)
    x.requires_grad_()
    g = torch.tensor(
        [1.0, 2.0, 0.5, -1.0], dtype=torch.float64, requires_grad=True
    )
    b = torch.zeros(4, dtype=torch.float64, requires_grad=True)
    upstream = torch.arange(12, dtype=torch.float64).reshape(3, 4) / 7
    ours = ref.layer_norm(x, g, b)
    oracle = F.layer_norm(x, (4,), g, b, 1e-5)
    assert torch.allclose(ours, oracle, atol=1e-12, rtol=1e-12)
    a = torch.autograd.grad(
        (ours * upstream).sum(), (x, g, b), retain_graph=True
    )
    z = torch.autograd.grad((oracle * upstream).sum(), (x, g, b))
    for left, right in zip(a, z):
        assert torch.allclose(left, right, atol=1e-10, rtol=1e-10)
    assert torch.allclose(a[0], ref.norm_vjp(x, g, upstream), atol=1e-10)
    assert torch.allclose(
        a[0].sum(-1), torch.zeros(3, dtype=torch.float64), atol=1e-10
    )


def test_normalization_gradcheck_and_shift():
    x = torch.tensor(
        [[1.0, 2.0, 4.0, 8.0]], dtype=torch.float64, requires_grad=True
    )
    g, b = (
        torch.ones(4, dtype=torch.float64),
        torch.zeros(4, dtype=torch.float64),
    )
    assert torch.autograd.gradcheck(lambda v: ref.layer_norm(v, g, b), (x,))
    assert torch.allclose(
        ref.layer_norm(x, g, b), ref.layer_norm(x + 7, g, b)
    )
    # Positive epsilon breaks exact scale invariance.
    assert not torch.equal(
        ref.layer_norm(x, g, b), ref.layer_norm(2 * x, g, b)
    )


def test_zero_branches_preserve_identity_and_gradient():
    p = ref.parameters()["blocks"][0]
    with torch.no_grad():
        p["wo"].zero_()
        p["bo"].zero_()
        p["w2"].zero_()
        p["b2"].zero_()
    x = torch.arange(12, dtype=torch.float64).reshape(3, 4).requires_grad_()
    out, _ = ref.block(x, p)
    assert torch.equal(out, x)
    assert torch.equal(
        torch.autograd.grad(out.sum(), x)[0], torch.ones_like(x)
    )


def test_block_against_pytorch_forward_and_all_parameter_gradients():
    p = ref.parameters()["blocks"][0]
    layer = torch.nn.TransformerEncoderLayer(
        4,
        2,
        8,
        dropout=0,
        activation="gelu",
        batch_first=True,
        norm_first=True,
        dtype=torch.float64,
    )
    mapping = [
        (layer.self_attn.in_proj_weight, p["wqkv"], True),
        (layer.self_attn.in_proj_bias, p["bqkv"], False),
        (layer.self_attn.out_proj.weight, p["wo"], True),
        (layer.self_attn.out_proj.bias, p["bo"], False),
        (layer.linear1.weight, p["w1"], True),
        (layer.linear1.bias, p["b1"], False),
        (layer.linear2.weight, p["w2"], True),
        (layer.linear2.bias, p["b2"], False),
        (layer.norm1.weight, p["g1"], False),
        (layer.norm1.bias, p["n1"], False),
        (layer.norm2.weight, p["g2"], False),
        (layer.norm2.bias, p["n2"], False),
    ]
    with torch.no_grad():
        for dest, source, transpose in mapping:
            dest.copy_(source.T if transpose else source)
    x = (
        torch.linspace(-1, 2, 20, dtype=torch.float64)
        .reshape(5, 4)
        .requires_grad_()
    )
    ours, _ = ref.block(x, p)
    # TransformerEncoderLayer mask True means forbidden, unlike our allowed mask.
    forbidden = torch.ones(5, 5, dtype=torch.bool).triu(1)
    oracle = layer(x.unsqueeze(0), src_mask=forbidden).squeeze(0)
    assert torch.allclose(ours, oracle, atol=2e-12, rtol=2e-12)
    go = torch.autograd.grad(
        ours.square().sum(), [x] + [s for _, s, _ in mapping]
    )
    gr = torch.autograd.grad(
        oracle.square().sum(), [x] + [d for d, _, _ in mapping]
    )
    assert torch.allclose(go[0], gr[0], atol=1e-10, rtol=1e-10)
    for a, b, (_, _, trans) in zip(go[1:], gr[1:], mapping):
        assert torch.allclose(
            a, b.T if trans else b, atol=1e-10, rtol=1e-10
        )


@pytest.mark.parametrize("chunks", [[5], [1, 1, 1, 1, 1], [2, 3], [3, 2]])
def test_two_layer_model_full_chunk_logits_and_gradients(chunks):
    p = ref.parameters()
    tokens = torch.tensor([0, 1, 2, 3, 4])
    full, _ = ref.model(tokens, p)
    cache, start, parts = None, 0, []
    for length in chunks:
        part, cache = ref.model(
            tokens[start : start + length], p, caches=cache
        )
        start += length
        parts.append(part)
        assert len(cache) == 2 and all(
            k.shape == (2, start, 2) for k, v in cache
        )
    joined = torch.cat(parts)
    assert torch.allclose(full, joined, atol=1e-12, rtol=1e-12)
    gf = torch.autograd.grad(
        full.square().sum(), list(ref.leaves(p)), retain_graph=True
    )
    gc = torch.autograd.grad(joined.square().sum(), list(ref.leaves(p)))
    for a, b in zip(gf, gc):
        assert torch.allclose(a, b, atol=1e-10, rtol=1e-10)


def test_positions_and_rotation():
    p = ref.positions(7, 4)
    assert torch.equal(
        p[:1], torch.tensor([[0.0, 1.0, 0.0, 1.0]], dtype=torch.float64)
    )
    assert torch.equal(p[3:], ref.positions(4, 4, 3))
    delta = torch.tensor(2.0, dtype=torch.float64)
    rot = torch.stack(
        (
            torch.stack((delta.cos(), delta.sin())),
            torch.stack((-delta.sin(), delta.cos())),
        )
    )
    assert torch.allclose(p[3, :2], rot @ p[1, :2], atol=1e-12)


def test_wrong_positions_and_dropout_are_detected():
    p = ref.parameters()
    t = torch.tensor([0, 1, 2, 3, 4])
    full, _ = ref.model(t, p)
    _, cache = ref.model(t[:3], p)
    wrong, _ = ref.model(t[3:], p, caches=cache, position_offset=0)
    assert (wrong - full[3:]).abs().max() > 0.01
    torch.manual_seed(1)
    a, _ = ref.model(t, p, dropout=0.5, training=True)
    torch.manual_seed(2)
    b, _ = ref.model(t, p, dropout=0.5, training=True)
    assert not torch.allclose(a, b)
    eval_a, _ = ref.model(t, p, dropout=0.5, training=False)
    assert torch.equal(eval_a, full)


def test_causality_and_record_isolation_through_model():
    p = ref.parameters()
    t = torch.tensor([0, 1, 2, 3, 4])
    records = torch.tensor([0, 0, 1, 1, 1])
    valid = torch.ones(5, dtype=torch.bool)
    mask = ref.packed_mask(records, valid)
    a, _ = ref.model(t, p, allowed=mask)
    changed = t.clone()
    changed[:2] = 4
    b, _ = ref.model(changed, p, allowed=mask)
    assert torch.equal(a[2:], b[2:])
    changed = t.clone()
    changed[-1] = 0
    c, _ = ref.model(changed, p)
    d, _ = ref.model(t, p)
    assert torch.equal(c[:-1], d[:-1])


def test_shifted_loss_denominator_boundaries_and_padding():
    logits = torch.zeros(7, 5, dtype=torch.float64, requires_grad=True)
    tokens = torch.tensor([0, 1, 2, 3, 4, 0, 0])
    valid = torch.tensor([True] * 5 + [False] * 2)
    records = torch.tensor([0, 0, 0, 1, 1, 1, 1])
    loss = ref.next_token_loss(logits, tokens, valid, records)
    assert loss.item() == pytest.approx(float(torch.log(torch.tensor(5.0))))
    loss.backward()
    assert torch.equal(
        logits.grad[[2, 4, 5, 6]], torch.zeros(4, 5, dtype=torch.float64)
    )
    assert logits.grad[0, 1] == pytest.approx(-0.8 / 3)
    with pytest.raises(ValueError):
        ref.next_token_loss(
            logits, tokens, torch.zeros(7, dtype=torch.bool), records
        )


@pytest.mark.parametrize("bad", [-1, 5])
def test_out_of_vocabulary_ids_are_not_python_indexing(bad):
    with pytest.raises(ValueError, match="vocabulary"):
        ref.model(torch.tensor([bad]), ref.parameters())


def test_synthetic_training_and_results():
    r = ref.results()
    assert r["training"][-1]["loss"] < r["training"][0]["loss"] * 0.7
    assert r["cache_max_error"] == 0
    assert r["wrong_position_error"] > 0.01
    assert r["parameter_count"] == 397
    assert r == json.loads((ROOT / "drafts/ch09/results.json").read_text())
