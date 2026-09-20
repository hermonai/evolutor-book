"""Single-head attention and explicit packed/offset masks; CPU teaching reference."""

import json
import math
import torch


def packed_mask(records, valid):
    """One sequence; IDs are unique per record; True means an allowed edge."""
    if records.ndim != 1 or valid.shape != records.shape:
        raise ValueError(
            "record and validity vectors must have matching shape"
        )
    if records.dtype != torch.long or valid.dtype != torch.bool:
        raise ValueError("int64 record IDs and boolean validity required")
    if records.device != valid.device:
        raise ValueError("matching devices required")
    pos = torch.arange(len(records), device=records.device)
    return (
        (pos[None, :] <= pos[:, None])
        & (records[None, :] == records[:, None])
        & valid[None, :]
        & valid[:, None]
    )


def masked_softmax(scores, allowed):
    """Empty rows return zeros with zero gradient; no softmax(-inf,...,-inf)."""
    if scores.ndim != 2 or scores.shape != allowed.shape:
        raise ValueError("scores and mask must be [queries,keys]")
    if allowed.dtype != torch.bool or allowed.device != scores.device:
        raise ValueError("boolean mask on score device required")
    if not scores.is_floating_point() or not torch.isfinite(scores).all():
        raise ValueError("finite floating scores required")
    if scores.shape[1] == 0:
        raise ValueError("at least one key required")
    has_key = allowed.any(dim=-1, keepdim=True)
    masked = scores.masked_fill(~allowed, -torch.inf)
    safe = torch.where(has_key, masked, torch.zeros_like(masked))
    weights = torch.softmax(safe, dim=-1)
    return torch.where(allowed, weights, torch.zeros_like(weights))


def attention(q, k, v, allowed):
    """Q[L,D], K[S,D], V[S,Dv] -> output[L,Dv], weights[L,S]."""
    if any(x.ndim != 2 for x in (q, k, v)):
        raise ValueError("rank-two tensors required")
    if (
        q.shape[1] == 0
        or q.shape[1] != k.shape[1]
        or k.shape[0] != v.shape[0]
    ):
        raise ValueError("query/key width and key/value length must agree")
    if any(x.dtype != q.dtype or x.device != q.device for x in (k, v)):
        raise ValueError("matching dtype and device required")
    if not q.is_floating_point() or not all(
        torch.isfinite(x).all() for x in (q, k, v)
    ):
        raise ValueError("finite floating tensors required")
    scores = (q @ k.T) / math.sqrt(q.shape[1])
    weights = masked_softmax(scores, allowed)
    return weights @ v, weights


def offset_mask(query_length, past, device=None):
    """Current chunk queries are at absolute positions past,...,past+L-1."""
    if any(type(n) is not int or n < 0 for n in (query_length, past)):
        raise ValueError("nonnegative integer lengths required")
    qpos = past + torch.arange(query_length, device=device)
    kpos = torch.arange(past + query_length, device=device)
    return kpos[None, :] <= qpos[:, None]


def cached_chunk(q, new_k, new_v, cache=None):
    """One record, fixed parameters/positions, no dropout; immutable concatenation."""
    if cache is None:
        old_k, old_v = new_k[:0], new_v[:0]
    else:
        old_k, old_v = cache
    if q.shape[0] != new_k.shape[0] or new_k.shape[0] != new_v.shape[0]:
        raise ValueError("one new key/value for each current query")
    if old_k.shape[0] != old_v.shape[0]:
        raise ValueError("cache key/value lengths must agree")
    keys = torch.cat((old_k, new_k), dim=0)
    values = torch.cat((old_v, new_v), dim=0)
    mask = offset_mask(q.shape[0], old_k.shape[0], q.device)
    output, _ = attention(q, keys, values, mask)
    return output, (keys, values)


def split_heads(x, heads):
    """[B,T,H*D] -> [B,H,T,D]; transpose, do not just reshape."""
    if (
        x.ndim != 3
        or type(heads) is not int
        or heads <= 0
        or x.shape[-1] % heads
    ):
        raise ValueError("rank three and width divisible by positive heads")
    b, t, width = x.shape
    return x.reshape(b, t, heads, width // heads).transpose(1, 2)


def merge_heads(x):
    """[B,H,T,D] -> [B,T,H*D]."""
    if x.ndim != 4:
        raise ValueError("rank four required")
    b, h, t, d = x.shape
    return x.transpose(1, 2).reshape(b, t, h * d)


def results():
    q = torch.tensor([[math.log(2)]], dtype=torch.float64)
    k = torch.tensor([[1.0], [0.0]], dtype=torch.float64)
    v = torch.tensor([[3.0, 0.0], [0.0, 6.0]], dtype=torch.float64)
    output, weights = attention(
        q, k, v, torch.ones((1, 2), dtype=torch.bool)
    )
    records = torch.tensor([0, 0, 1, 1, 2])
    valid = torch.tensor([True, True, True, True, False])
    return {
        "weights": weights.tolist(),
        "output": output.tolist(),
        "packed_mask": packed_mask(records, valid).int().tolist(),
        "offset_mask": offset_mask(2, 3).int().tolist(),
        "wrong_upper_left": torch.ones(2, 5, dtype=torch.bool)
        .tril()
        .int()
        .tolist(),
        "work": [
            dict(
                t=t,
                score_cells=t * t,
                causal_pairs=t * (t + 1) // 2,
                kv_scalars=2 * t * 64,
            )
            for t in [16, 64, 256, 1024]
        ],
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
