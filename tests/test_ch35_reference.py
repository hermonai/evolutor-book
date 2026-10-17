import importlib.util
from pathlib import Path
import sys
from dataclasses import replace

import pytest
import torch

SPEC = importlib.util.spec_from_file_location(
    "evod35_tests", Path(__file__).parents[1] / "drafts/ch35/reference.py"
)
r = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = r
SPEC.loader.exec_module(r)
OWNER = ("tenant-a", "record-a")
TOKENS = (0, 1, 2, 3, 0, 2)


def test_assigned_retrieval_arithmetic():
    import math

    weights = torch.tensor([0.0, math.log(2), 0.0], dtype=torch.float64).softmax(0)
    values = torch.tensor([[1.0, 0.0], [0.0, 2.0], [2.0, 1.0]], dtype=torch.float64)
    torch.testing.assert_close(
        weights, torch.tensor([0.25, 0.5, 0.25], dtype=torch.float64)
    )
    torch.testing.assert_close(
        weights @ values, torch.tensor([0.75, 1.25], dtype=torch.float64)
    )


@pytest.mark.parametrize("seed", [5, 35, 71])
@pytest.mark.parametrize("split", range(1, 7))
def test_actual_full_model_all_splits(seed, split):
    model = r.tiny_model(seed)
    full = r.full_oracle(model, TOKENS)
    first, cache = r.prefill(model, OWNER, TOKENS[:split])
    parts = [first]
    for t in TOKENS[split:]:
        y, cache = r.decode_one(model, cache, OWNER, t)
        parts.append(y)
    torch.testing.assert_close(torch.cat(parts), full, atol=2e-12, rtol=2e-12)
    assert cache.tokens == TOKENS and not parts[-1].requires_grad


@pytest.mark.parametrize("cut_bits", range(32))
def test_every_chunk_composition(cut_bits):
    model = r.tiny_model()
    ends = [i + 1 for i in range(5) if cut_bits & (1 << i)] + [6]
    cache, start, outputs = r.empty(model, OWNER), 0, []
    for end in ends:
        y, cache = r.consume(model, cache, OWNER, TOKENS[start:end])
        outputs.append(y)
        start = end
    torch.testing.assert_close(
        torch.cat(outputs), r.full_oracle(model, TOKENS), atol=2e-12, rtol=2e-12
    )


def test_per_layer_keys_values_match_full_projection_hooks():
    model = r.tiny_model()
    projected = []
    hooks = [
        b.attn.qkv.register_forward_hook(
            lambda mod, args, out: projected.append(out.detach().clone())
        )
        for b in model.blocks
    ]
    r.full_oracle(model, TOKENS)
    for h in hooks:
        h.remove()
    _, cache = r.prefill(model, OWNER, TOKENS)
    for block, raw, layer in zip(model.blocks, projected, cache.layers):
        _, k, v = raw[0].view(6, 3, block.attn.h, block.attn.dh).permute(1, 2, 0, 3)
        torch.testing.assert_close(k, layer.k, atol=2e-12, rtol=2e-12)
        torch.testing.assert_close(v, layer.v, atol=2e-12, rtol=2e-12)


@pytest.mark.parametrize("d,heads,layers", [(4, 1, 1), (12, 3, 3), (16, 4, 2)])
def test_geometry_variants_preserve_full_model(d, heads, layers):
    with torch.random.fork_rng():
        torch.manual_seed(137)
        model = (
            r.hermon_module()
            .HermonDNA(max_len=12, d=d, h=heads, layers=layers)
            .double()
            .eval()
        )
    first, cache = r.prefill(model, OWNER, TOKENS[:2])
    last, cache = r.consume(model, cache, OWNER, TOKENS[2:])
    torch.testing.assert_close(
        torch.cat([first, last]), r.full_oracle(model, TOKENS), atol=2e-12, rtol=2e-12
    )
    assert len(cache.layers) == layers


def test_rectangular_offset_mask_and_sdpa_oracle():
    expected = torch.tensor([[1, 1, 1, 1, 0], [1, 1, 1, 1, 1]], dtype=torch.bool)
    assert torch.equal(r.allowed_mask(3, 2), expected)
    g = torch.Generator().manual_seed(91)
    q = torch.randn(2, 2, 4, generator=g, dtype=torch.float64)
    k = torch.randn(2, 5, 4, generator=g, dtype=torch.float64)
    v = torch.randn(2, 5, 4, generator=g, dtype=torch.float64)
    direct = ((q @ k.transpose(-2, -1)) / 2).masked_fill(
        ~expected, float("-inf")
    ).softmax(-1) @ v
    api = torch.nn.functional.scaled_dot_product_attention(
        q, k, v, attn_mask=expected, dropout_p=0
    )
    torch.testing.assert_close(api, direct, atol=2e-12, rtol=2e-12)
    wrong = torch.nn.functional.scaled_dot_product_attention(
        q, k, v, is_causal=True, dropout_p=0
    )
    assert not torch.allclose(wrong, direct)


@pytest.mark.parametrize("prefix", [1, 2, 4])
def test_future_perturbation_cannot_change_prefix(prefix):
    model = r.tiny_model()
    changed = TOKENS[:prefix] + tuple((t + 1) % 4 for t in TOKENS[prefix:])
    torch.testing.assert_close(
        r.full_oracle(model, TOKENS)[:prefix],
        r.full_oracle(model, changed)[:prefix],
        atol=0,
        rtol=0,
    )


def test_fresh_storage_empty_identity_and_failure_preserves_cache():
    model = r.tiny_model()
    _, cache = r.prefill(model, OWNER, TOKENS[:3])
    old = tuple((x.k.clone(), x.v.clone()) for x in cache.layers)
    y, same = r.consume(model, cache, OWNER, ())
    assert y.shape == (0, 4) and same is cache
    _, new = r.consume(model, cache, OWNER, TOKENS[3:5])
    for before, after, snapshot in zip(cache.layers, new.layers, old):
        assert (
            before.k.data_ptr() != after.k.data_ptr()
            and before.v.data_ptr() != after.v.data_ptr()
        )
        assert torch.equal(before.k, snapshot[0]) and torch.equal(before.v, snapshot[1])
    with pytest.raises(ValueError):
        r.consume(model, cache, OWNER, (1, 99))
    r.validate(model, cache, OWNER)


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact", "f" * 64),
        ("mode", "offline"),
        ("tokens", (0, 1)),
        ("layers", ()),
        ("seal", "bad"),
        ("owner", ("tenant-b", "record-a")),
    ],
)
def test_metadata_rejection(field, value):
    model = r.tiny_model()
    _, cache = r.prefill(model, OWNER, TOKENS[:3])
    with pytest.raises((ValueError, PermissionError)):
        r.consume(model, replace(cache, **{field: value}), OWNER, (2,))


@pytest.mark.parametrize(
    "kind", ["nan", "shape", "dtype", "gradient", "finite_mutation"]
)
def test_payload_rejection(kind):
    model = r.tiny_model()
    _, cache = r.prefill(model, OWNER, TOKENS[:3])
    k, v = cache.layers[0].k.clone(), cache.layers[0].v.clone()
    if kind == "nan":
        k[0, 0, 0] = float("nan")
    if kind == "shape":
        k = k[:, :2]
    if kind == "dtype":
        k = k.float()
    if kind == "gradient":
        k.requires_grad_()
    if kind == "finite_mutation":
        k[0, 0, 0] += 1
    bad = replace(cache, layers=(r.LayerKV(k, v), *cache.layers[1:]))
    with pytest.raises(ValueError):
        r.validate(model, bad, OWNER)


@pytest.mark.parametrize("bad", [True, -1, 4, 1.0, None])
def test_token_domain(bad):
    model = r.tiny_model()
    with pytest.raises(ValueError):
        r.prefill(model, OWNER, (bad,))


@pytest.mark.parametrize(
    "change", ["parameter", "position", "epsilon", "training", "dtype"]
)
def test_model_context_change_rejected(change):
    model = r.tiny_model()
    _, cache = r.prefill(model, OWNER, TOKENS[:2])
    with torch.no_grad():
        if change == "parameter":
            model.blocks[0].attn.qkv.weight[0, 0] += 1
        if change == "position":
            model.pos.weight[2, 0] += 1
    if change == "epsilon":
        model.blocks[0].n1.eps *= 2
    if change == "training":
        model.train()
    if change == "dtype":
        model.float()
    with pytest.raises(ValueError):
        r.decode_one(model, cache, OWNER, 2)


def test_wrong_absolute_position_negative_control():
    model = r.tiny_model()
    _, cache = r.prefill(model, OWNER, TOKENS[:3])
    normal, _ = r.decode_one(model, cache, OWNER, 3)
    other = r.tiny_model()
    with torch.no_grad():
        other.pos.weight[3].copy_(other.pos.weight[0])
    # Fresh cache under the modified artifact isolates a wrong next position.
    _, bad_cache = r.prefill(other, OWNER, TOKENS[:3])
    wrong, _ = r.decode_one(other, bad_cache, OWNER, 3)
    assert not torch.allclose(normal, wrong)


def test_rehash_is_not_authentication_or_replay_proof():
    model = r.tiny_model()
    _, cache = r.prefill(model, OWNER, TOKENS[:3])
    cache.layers[0].k[0, 0, 0] += 1
    forged = replace(cache, seal=r.seal_for(cache))
    r.validate(
        model, forged, OWNER
    )  # Trusted producer can forge internally consistent metadata.
    bad, _ = r.decode_one(model, forged, OWNER, 3)
    good = r.full_oracle(model, TOKENS[:4])[-1:]
    assert not torch.allclose(bad, good)


def test_maximum_capacity_no_truncation():
    model = r.tiny_model()
    _, cache = r.prefill(model, OWNER, (0,) * model.max_len)
    with pytest.raises(ValueError):
        r.decode_one(model, cache, OWNER, 1)
    assert len(cache.tokens) == model.max_len


def test_memory_copy_cost_and_rng_purity():
    state = torch.random.get_rng_state().clone()
    r.tiny_model()
    assert torch.equal(state, torch.random.get_rng_state())
    assert r.kv_bytes(24, 4096, 8, 128, 2) == 402653184
    assert r.kv_bytes(2, 6, 2, 4, 8) == 1536
    assert r.append_copy_bytes(3, 3, 2, 2, 4, 8) == 6144
    assert r.append_copy_bytes(0, 0, 2, 2, 4, 8) == 0
    with pytest.raises(ValueError):
        r.kv_bytes(24, True, 8, 128, 2)
    with pytest.raises(ValueError):
        r.allowed_mask(True, 2)
