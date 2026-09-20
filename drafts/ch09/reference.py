"""Transparent pre-LN causal Transformer reference; CPU float64 checks."""

import math
import torch
from torch.nn import functional as F


def layer_norm(x, gamma, beta, eps=1e-5):
    """Normalize features only, separately at every token."""
    if (
        x.ndim != 2
        or gamma.shape != x.shape[-1:]
        or beta.shape != gamma.shape
    ):
        raise ValueError("expected x[T,D] and affine vectors [D]")
    if not math.isfinite(eps) or eps <= 0:
        raise ValueError("positive finite epsilon required")
    centered = x - x.mean(-1, keepdim=True)
    variance = centered.square().mean(-1, keepdim=True)
    return centered * torch.rsqrt(variance + eps) * gamma + beta


def norm_vjp(x, gamma, upstream, eps=1e-5):
    """Analytic derivative with respect to x; affine parameters fixed."""
    centered = x - x.mean(-1, keepdim=True)
    scale = torch.rsqrt(centered.square().mean(-1, keepdim=True) + eps)
    z = centered * scale
    g = upstream * gamma
    return scale * (
        g - g.mean(-1, keepdim=True) - z * (g * z).mean(-1, keepdim=True)
    )


def positions(length, width, offset=0, *, dtype=torch.float64, device=None):
    for value in (length, width, offset):
        if type(value) is not int or value < 0:
            raise ValueError(
                "nonnegative integer position dimensions required"
            )
    if width == 0 or width % 2:
        raise ValueError("positive even width required")
    pos = torch.arange(offset, offset + length, dtype=dtype, device=device)
    freq = torch.exp(
        -math.log(10000)
        * torch.arange(0, width, 2, dtype=dtype, device=device)
        / width
    )
    angle = pos[:, None] * freq[None, :]
    return torch.stack((angle.sin(), angle.cos()), dim=-1).flatten(1)


def packed_mask(records, valid):
    if records.ndim != 1 or records.shape != valid.shape:
        raise ValueError(
            "matching one-dimensional record and validity vectors"
        )
    if records.dtype != torch.int64 or valid.dtype != torch.bool:
        raise ValueError("int64 records and boolean validity required")
    pos = torch.arange(len(records), device=records.device)
    return (
        (pos[:, None] >= pos[None, :])
        & (records[:, None] == records[None, :])
        & valid[:, None]
        & valid[None, :]
    )


def multihead(x, p, heads, cache=None, allowed=None):
    """Projected K,V cache [H,S,d]; immutable append preserves gradients."""
    t, width = x.shape
    if type(heads) is not int or heads <= 0 or width % heads:
        raise ValueError("heads must divide model width")
    d = width // heads
    qkv = (x @ p["wqkv"] + p["bqkv"]).reshape(t, 3, heads, d)
    q, k, v = (qkv[:, i].transpose(0, 1) for i in range(3))
    past = 0
    if cache is not None:
        old_k, old_v = cache
        if old_k.shape != old_v.shape or old_k.shape[::2] != (heads, d):
            raise ValueError("cache must contain matching [H,S,d] tensors")
        past = old_k.shape[1]
        k, v = torch.cat((old_k, k), 1), torch.cat((old_v, v), 1)
    if allowed is None:
        qi = past + torch.arange(t, device=x.device)
        kj = torch.arange(past + t, device=x.device)
        allowed = kj[None, :] <= qi[:, None]
    if allowed.dtype != torch.bool or allowed.shape != (t, past + t):
        raise ValueError("boolean mask must be [current queries, all keys]")
    scores = (q @ k.transpose(-2, -1)) / math.sqrt(d)
    masked = scores.masked_fill(~allowed, -torch.inf)
    active = allowed.any(-1, keepdim=True)
    safe = torch.where(active, masked, torch.zeros_like(masked))
    weights = torch.softmax(safe, -1).masked_fill(~allowed, 0)
    joined = (weights @ v).transpose(0, 1).reshape(t, width)
    return joined @ p["wo"] + p["bo"], (k, v)


def feed_forward(x, p):
    return (
        F.gelu(x @ p["w1"] + p["b1"], approximate="none") @ p["w2"]
        + p["b2"]
    )


def block(
    x, p, heads=2, cache=None, allowed=None, dropout=0.0, training=False
):
    """Pre-LN; dropout only on the two residual-branch outputs."""
    if not 0 <= dropout < 1 or type(training) is not bool:
        raise ValueError("dropout in [0,1), explicit boolean training mode")
    normalized = layer_norm(x, p["g1"], p["n1"])
    branch, new_cache = multihead(normalized, p, heads, cache, allowed)
    u = x + F.dropout(branch, p=dropout, training=training)
    branch = feed_forward(layer_norm(u, p["g2"], p["n2"]), p)
    return u + F.dropout(branch, p=dropout, training=training), new_cache


def model(
    tokens,
    p,
    heads=2,
    caches=None,
    allowed=None,
    dropout=0.0,
    training=False,
    position_offset=None,
):
    """One sequence/chunk; default absolute offset inferred from cache."""
    if tokens.ndim != 1 or tokens.dtype != torch.int64 or len(tokens) == 0:
        raise ValueError("nonempty int64 token vector required")
    if (tokens < 0).any() or (tokens >= p["embedding"].shape[0]).any():
        raise ValueError("token IDs must lie within the vocabulary")
    if caches is None:
        caches = [None] * len(p["blocks"])
    if len(caches) != len(p["blocks"]):
        raise ValueError("one cache slot per block required")
    lengths = [0 if c is None else c[0].shape[1] for c in caches]
    if len(set(lengths)) != 1:
        raise ValueError("all block histories must have the same length")
    past = lengths[0]
    offset = past if position_offset is None else position_offset
    x = p["embedding"][tokens]
    x = x + positions(
        len(tokens), x.shape[-1], offset, dtype=x.dtype, device=x.device
    )
    updated = []
    for weights, cache in zip(p["blocks"], caches):
        x, cache = block(
            x, weights, heads, cache, allowed, dropout, training
        )
        updated.append(cache)
    x = layer_norm(x, p["gf"], p["nf"])
    return x @ p["head"] + p["head_bias"], updated


def next_token_loss(logits, tokens, valid, records):
    """Valid adjacent targets within one record; mean over legal edges."""
    t = len(tokens)
    if logits.ndim != 2 or logits.shape[0] != t or t < 2:
        raise ValueError(
            "logits[T,V] and at least two token positions required"
        )
    if tokens.shape != valid.shape or tokens.shape != records.shape:
        raise ValueError("token/validity/record vectors must match")
    if (
        tokens.dtype != torch.int64
        or records.dtype != torch.int64
        or valid.dtype != torch.bool
    ):
        raise ValueError(
            "int64 token/record vectors and boolean validity required"
        )
    keep = valid[:-1] & valid[1:] & (records[:-1] == records[1:])
    if not keep.any():
        raise ValueError("no legal next-token targets")
    return F.cross_entropy(logits[:-1][keep], tokens[1:][keep])


def parameters(width=4, hidden=8, vocab=5, depth=2, seed=9):
    if width <= 0 or width % 2 or hidden <= 0 or vocab <= 0 or depth <= 0:
        raise ValueError("positive dimensions and even width required")
    generator = torch.Generator().manual_seed(seed)

    def rand(*shape):
        return (
            torch.randn(*shape, generator=generator, dtype=torch.float64)
            * 0.15
        ).requires_grad_()

    def ones():
        return torch.ones(width, dtype=torch.float64, requires_grad=True)

    def zeros(*shape):
        return torch.zeros(*shape, dtype=torch.float64, requires_grad=True)

    blocks = []
    for _ in range(depth):
        blocks.append(
            dict(
                wqkv=rand(width, 3 * width),
                bqkv=zeros(3 * width),
                wo=rand(width, width),
                bo=zeros(width),
                w1=rand(width, hidden),
                b1=zeros(hidden),
                w2=rand(hidden, width),
                b2=zeros(width),
                g1=ones(),
                n1=zeros(width),
                g2=ones(),
                n2=zeros(width),
            )
        )
    return dict(
        embedding=rand(vocab, width),
        blocks=blocks,
        gf=ones(),
        nf=zeros(width),
        head=rand(width, vocab),
        head_bias=zeros(vocab),
    )


def leaves(p):
    for key, value in p.items():
        if key == "blocks":
            for weights in value:
                yield from weights.values()
        else:
            yield value


def training_trace(steps=30):
    p = parameters()
    tokens = torch.tensor([0, 1, 2, 3, 0, 1, 2, 3, 0, 0])
    valid = torch.tensor([True] * 9 + [False])
    records = torch.zeros(10, dtype=torch.int64)
    mask = packed_mask(records, valid)
    trace = []
    for step in range(steps + 1):
        logits, _ = model(tokens, p, allowed=mask)
        loss = next_token_loss(logits, tokens, valid, records)
        trace.append(dict(step=step, loss=round(loss.item(), 10)))
        if step == steps:
            break
        loss.backward()
        with torch.no_grad():
            for value in leaves(p):
                value -= 0.1 * value.grad
                value.grad = None
    return trace


def results():
    x = torch.tensor([[1.0, 2.0, 3.0, 4.0]], dtype=torch.float64)
    p = parameters()
    tokens = torch.tensor([0, 1, 2, 3, 4])
    full, _ = model(tokens, p)
    first, cache = model(tokens[:3], p)
    last, _ = model(tokens[3:], p, caches=cache)
    wrong, _ = model(tokens[3:], p, caches=cache, position_offset=0)
    return {
        "normalization": layer_norm(
            x, torch.ones(4), torch.zeros(4)
        ).tolist()[0],
        "positions": positions(4, 4).tolist(),
        "parameter_count": sum(v.numel() for v in leaves(p)),
        "cache_max_error": round(
            (full - torch.cat((first, last))).abs().max().item(), 12
        ),
        "wrong_position_error": round(
            (full[3:] - wrong).abs().max().item(), 8
        ),
        "training": training_trace(),
    }


if __name__ == "__main__":
    import json

    torch.set_num_threads(1)
    print(json.dumps(results(), indent=2))
