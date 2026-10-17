"""Actual Chapter 23 Hermon causal Transformer with explicit per-layer KV.

CPU float64 inference, learned absolute positions and fresh concatenated storage.
Trusted serialized objects; content seals detect mutation, not authenticate it.
"""

from dataclasses import dataclass
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

import torch

MODE = "evod23-causal-acgt-learned-absolute-v1"


def hermon_module():
    name = "evod35_actual_hermon"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, Path(__file__).parent.parent / "ch23/reference.py"
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def owner_pair(owner):
    if (
        type(owner) is not tuple
        or len(owner) != 2
        or any(type(v) is not str or not 1 <= len(v) <= 128 for v in owner)
    ):
        raise ValueError("bounded tenant/request pair")


def artifact_id(model):
    m = hermon_module()
    if type(model) is not m.HermonDNA or any(x.training for x in model.modules()):
        raise ValueError("actual Chapter 23 model in evaluation mode required")
    if (
        not 1 <= model.max_len <= 512
        or not 1 <= model.d <= 128
        or not 1 <= len(model.blocks) <= 8
    ):
        raise ValueError("bounded reference geometry")
    params = {}
    for name, value in model.state_dict().items():
        if (
            value.device.type != "cpu"
            or value.dtype != torch.float64
            or not bool(torch.isfinite(value).all())
        ):
            raise ValueError("finite CPU float64 parameters")
        params[name] = value.detach().tolist()
    config = [
        (b.attn.h, b.attn.dh, b.n1.eps, b.n2.eps, b.ff[1].approximate)
        for b in model.blocks
    ]
    return digest(
        {
            "mode": MODE,
            "d": model.d,
            "max_len": model.max_len,
            "blocks": config,
            "norm_eps": model.norm.eps,
            "parameters": params,
        }
    )


def tokens_copy(tokens, maximum):
    if (
        type(tokens) not in (tuple, list)
        or len(tokens) > maximum
        or any(type(t) is not int or not 0 <= t <= 3 for t in tokens)
    ):
        raise ValueError("bounded concrete ACGT token sequence")
    return tuple(tokens)


@dataclass(frozen=True)
class LayerKV:
    k: torch.Tensor
    v: torch.Tensor


@dataclass(frozen=True)
class Cache:
    owner: tuple
    artifact: str
    mode: str
    tokens: tuple
    layers: tuple
    seal: str


def seal_for(cache):
    return digest(
        {
            "owner": cache.owner,
            "artifact": cache.artifact,
            "mode": cache.mode,
            "tokens": cache.tokens,
            "layers": [(x.k.tolist(), x.v.tolist()) for x in cache.layers],
        }
    )


def sealed(owner, artifact, tokens, layers):
    cache = Cache(owner, artifact, MODE, tokens, tuple(layers), "")
    return Cache(owner, artifact, MODE, tokens, tuple(layers), seal_for(cache))


def empty(model, owner):
    owner_pair(owner)
    artifact = artifact_id(model)
    layers = [
        LayerKV(
            torch.empty(b.attn.h, 0, b.attn.dh, dtype=torch.float64),
            torch.empty(b.attn.h, 0, b.attn.dh, dtype=torch.float64),
        )
        for b in model.blocks
    ]
    return sealed(owner, artifact, (), layers)


def validate(model, cache, owner):
    owner_pair(owner)
    artifact = artifact_id(model)
    if not isinstance(cache, Cache) or cache.owner != owner:
        raise PermissionError("cache owner mismatch")
    if cache.artifact != artifact or cache.mode != MODE:
        raise ValueError("cache artifact/mode mismatch")
    if type(cache.tokens) is not tuple:
        raise ValueError("immutable consumed-token metadata")
    tokens_copy(cache.tokens, model.max_len)
    if type(cache.layers) is not tuple or len(cache.layers) != len(model.blocks):
        raise ValueError("exact per-layer cache")
    for layer, block in zip(cache.layers, model.blocks):
        if not isinstance(layer, LayerKV):
            raise ValueError("KV record required")
        for value in (layer.k, layer.v):
            if (
                not isinstance(value, torch.Tensor)
                or value.shape != (block.attn.h, len(cache.tokens), block.attn.dh)
                or value.device.type != "cpu"
                or value.dtype != torch.float64
                or value.requires_grad
                or not bool(torch.isfinite(value).all())
            ):
                raise ValueError("finite inference KV with declared geometry")
    if type(cache.seal) is not str or cache.seal != seal_for(cache):
        raise ValueError("cache content mutated; seal is not authentication")


def allowed_mask(past, chunk):
    if type(past) is not int or past < 0 or type(chunk) is not int or chunk < 1:
        raise ValueError("nonnegative prefix, positive chunk")
    return torch.arange(past + chunk)[None, :] <= (past + torch.arange(chunk))[:, None]


@torch.no_grad()
def consume(model, cache, owner, tokens):
    """Append a whole causal chunk; old cache remains untouched on every path."""
    validate(model, cache, owner)
    tokens = tokens_copy(tokens, model.max_len - len(cache.tokens))
    if not tokens:
        return torch.empty(0, 4, dtype=torch.float64), cache
    past, count = len(cache.tokens), len(tokens)
    ids = torch.tensor(tokens, dtype=torch.long)
    z = model.tok(ids) + model.pos(torch.arange(past, past + count))
    allowed = allowed_mask(past, count)
    layers = []
    for block, old in zip(model.blocks, cache.layers):
        a = block.attn
        raw = a.qkv(block.n1(z))
        q, k, v = raw.view(count, 3, a.h, a.dh).permute(1, 2, 0, 3)
        k = torch.cat((old.k, k), dim=1)
        v = torch.cat((old.v, v), dim=1)
        scores = (q @ k.transpose(-2, -1)) / math.sqrt(a.dh)
        weights = scores.masked_fill(~allowed, float("-inf")).softmax(-1)
        y = (weights @ v).transpose(0, 1).reshape(count, model.d)
        z = z + a.out(y)
        z = z + block.ff(block.n2(z))
        layers.append(LayerKV(k.clone(), v.clone()))
    logits = model.lm(model.norm(z))
    candidate = sealed(owner, cache.artifact, cache.tokens + tokens, layers)
    validate(model, candidate, owner)
    if not bool(torch.isfinite(logits).all()):
        raise ValueError("nonfinite model logits")
    return logits, candidate


def prefill(model, owner, tokens):
    return consume(model, empty(model, owner), owner, tokens)


def decode_one(model, cache, owner, token):
    return consume(model, cache, owner, (token,))


@torch.no_grad()
def full_oracle(model, tokens):
    artifact_id(model)
    tokens = tokens_copy(tokens, model.max_len)
    if not tokens:
        return torch.empty(0, 4, dtype=torch.float64)
    # Original full causal path: no cache, append helper or rectangular mask reuse.
    return model.causal_logits(torch.tensor([tokens], dtype=torch.long))[0]


def kv_bytes(layers, tokens, heads, head_width, element_bytes):
    if any(
        type(v) is not int or v < (0 if i == 1 else 1)
        for i, v in enumerate((layers, tokens, heads, head_width, element_bytes))
    ):
        raise ValueError("integer KV geometry; zero tokens allowed")
    return 2 * layers * tokens * heads * head_width * element_bytes


def append_copy_bytes(prompt, generated, layers, heads, head_width, element_bytes):
    if type(generated) is not int or generated < 0:
        raise ValueError("nonnegative generated count")
    per = kv_bytes(layers, 1, heads, head_width, element_bytes)
    kv_bytes(layers, prompt, heads, head_width, element_bytes)
    # Old K/V read plus equal-length destination writes, excluding new-row writes.
    return per * (2 * generated * prompt + generated * (generated - 1))


def tiny_model(seed=35):
    with torch.random.fork_rng():
        torch.manual_seed(seed)
        return hermon_module().HermonDNA(max_len=16, d=8, h=2, layers=2).double().eval()


def results():
    model, owner, tokens = tiny_model(), ("tenant-a", "record-a"), (0, 1, 2, 3, 0, 2)
    full = full_oracle(model, tokens)
    rows = []
    for split in range(1, len(tokens) + 1):
        first, cache = prefill(model, owner, tokens[:split])
        outputs = [first]
        for token in tokens[split:]:
            y, cache = decode_one(model, cache, owner, token)
            outputs.append(y)
        rows.append(
            {
                "split": split,
                "error": (torch.cat(outputs) - full).abs().max().item(),
                "position": len(cache.tokens),
                "payload": sum((x.k.numel() + x.v.numel()) * 8 for x in cache.layers),
            }
        )
    return {
        "parity": rows,
        "memory": [
            {
                "tokens": t,
                "bytes": kv_bytes(24, t, 8, 128, 2),
                "mib": kv_bytes(24, t, 8, 128, 2) / 2**20,
            }
            for t in (512, 1024, 2048, 4096, 8192)
        ],
        "mask": allowed_mask(3, 2).int().tolist(),
        "copy_bytes_example": append_copy_bytes(3, 3, 2, 2, 4, 8),
    }


TABLES = [
    (
        "parity",
        ["Prefill", "Max logit error", "Final $t$", "KV bytes"],
        ["split", "error", "position", "payload"],
        "rrrr",
    ),
    ("memory", ["Tokens", "KV bytes", "MiB"], ["tokens", "bytes", "mib"], "rrr"),
]
PLOTS = [("growth", "memory", "tokens", ["mib"])]
LISTINGS = ["allowed_mask", "consume", "validate", "full_oracle"]
