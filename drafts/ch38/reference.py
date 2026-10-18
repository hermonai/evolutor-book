"""Exact-law speculation and online attention, with actual layered KV parity.

CPU teaching references; no native GPU kernel, learned draft, device timings or
performance claim. Probability tables are finite normalized distributions.
"""
import math
import numpy as np
import torch
from pathlib import Path
import importlib.util
import sys


def load_paging():
    name = "evod_batch_a_36"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, Path(__file__).parent.parent / "ch36/reference.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


paging = load_paging()
native = paging.native


def normalize(x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 1 or len(x) == 0 or np.any(x < 0) or not np.isfinite(x).all() or x.max() <= 0:
        raise ValueError("finite nonnegative distribution")
    x = x/x.max()  # avoid overflowing a finite unnormalized sum
    return x/x.sum()


def pair(p, q):
    p, q = normalize(p), normalize(q)
    if p.shape != q.shape:
        raise ValueError("same vocabulary IDs and cardinality required")
    return p, q


def acceptance_probabilities(p, q):
    p, q = pair(p, q)
    a = np.ones_like(p)
    np.divide(p, q, out=a, where=q > 0)
    return np.minimum(a, 1)


def correction_distribution(p, q):
    p, q = pair(p, q)
    residual = np.maximum(p-q, 0)
    # p=q: rejection has zero mass; this fallback is never sampled ideally.
    return normalize(residual) if np.any(residual > 0) else p.copy()


def output_distribution(p, q):
    p, q = pair(p, q)
    accepted = np.minimum(p, q)
    # Positive-difference sum avoids cancellation in 1-sum(min(p,q)).
    return accepted+np.maximum(p-q, 0).sum()*correction_distribution(p, q)


def propose(draft, prefix, k, rng):
    paging.positive(k)
    tokens, qs = [], []
    for _ in range(k):
        q = normalize(draft(tuple(prefix)+tuple(tokens)))
        tokens.append(int(rng.choice(len(q), p=q)))
        qs.append(q)
    return tuple(tokens), qs


def verify(proposals, ps, qs, rng):
    if not proposals or len(proposals) != len(ps) or len(ps) != len(qs):
        raise ValueError("nonempty aligned verification block")
    out = []
    for i, (x, p, q) in enumerate(zip(proposals, ps, qs)):
        p, q = pair(p, q)
        if type(x) is not int or not 0 <= x < len(q) or q[x] <= 0:
            raise ValueError("proposal must have positive draft mass")
        if rng.random() < min(1.0, p[x]/q[x]):
            out.append(x)
        else:
            r = correction_distribution(p, q)
            out.append(int(rng.choice(len(r), p=r)))
            return tuple(out), i
    return tuple(out), len(out)


def speculative_block(target, draft, prefix, k, rng):
    proposals, qs = propose(draft, prefix, k, rng)
    ps = [target(tuple(prefix)+proposals[:i]) for i in range(k)]
    return verify(proposals, ps, qs, rng)


def native_speculative(pool, handle, owner, draft, k, rng):
    """Verify on a fork; discard tentative pages; recompute only committed rows.

    No bonus token in this variant. Every returned token is also consumed into
    KV. A caller must not consume it a second time. Prefix must be nonempty.
    """
    s = pool.state(handle, owner)
    if not s.tokens or k > pool.model.max_len-len(s.tokens):
        raise ValueError("nonempty prefix and bounded draft block")
    proposals, qs = propose(draft, s.tokens, k, rng)
    proposals = native.tokens_copy(proposals, k)
    branch_owner = (owner[0], "@verify-"+owner[1])
    branch = pool.fork(handle, owner, branch_owner)
    try:
        initial = native.full_oracle(pool.model, s.tokens)[-1]
        rows = pool.consume(branch, branch_owner, proposals)
        ps = torch.cat((initial[None], rows[:-1])).softmax(-1).numpy()
        committed, accepted = verify(proposals, ps, qs, rng)
    finally:
        pool.release(branch, branch_owner)
    pool.consume(handle, owner, committed)
    return committed, accepted


def attention_inputs(q, k, v, allowed):
    if (q.ndim != 3 or k.ndim != 3 or v.ndim != 3 or q.shape[0] != k.shape[0]
            or k.shape[:2] != v.shape[:2] or q.shape[2] != k.shape[2]
            or min(*q.shape, *k.shape, *v.shape) < 1
            or any(x.dtype != torch.float64 or x.device.type != "cpu"
                   or not bool(torch.isfinite(x).all()) for x in (q,k,v))
            or allowed.dtype != torch.bool or allowed.device.type != "cpu"
            or allowed.shape != (q.shape[1], k.shape[1])):
        raise ValueError("finite CPU float64 H,N,d / H,T,d / H,T,dv; bool N,T")


def dense_attention(q, k, v, allowed):
    attention_inputs(q,k,v,allowed)
    scores = q@k.transpose(-2,-1)/math.sqrt(q.shape[-1])
    if not bool(torch.isfinite(scores).all()):
        raise ValueError("score overflow")
    active = allowed.any(-1)[None,:,None]
    scores = scores.masked_fill(~allowed, -torch.inf)
    safe = torch.where(active, scores, torch.zeros_like(scores))
    return (safe.softmax(-1)*active)@v


def online_attention(q, tiles):
    """Tiles are (K,V,allowed) in logical order, independent of physical IDs."""
    if q.ndim != 3 or min(q.shape) < 1:
        raise ValueError("nonempty H,N,d queries")
    maximum = torch.full(q.shape[:2], -torch.inf, dtype=torch.float64)
    normalizer = torch.zeros_like(maximum)
    accumulator, seen = None, False
    for k, v, allowed in tiles:
        attention_inputs(q,k,v,allowed)
        if accumulator is None:
            accumulator = torch.zeros(*q.shape[:2], v.shape[-1], dtype=torch.float64)
        elif accumulator.shape[-1] != v.shape[-1]:
            raise ValueError("value width changed")
        scores = q@k.transpose(-2,-1)/math.sqrt(q.shape[-1])
        if not bool(torch.isfinite(scores).all()):
            raise ValueError("score overflow")
        scores = scores.masked_fill(~allowed, -torch.inf)
        new_max = torch.maximum(maximum, scores.max(-1).values)
        safe_max = torch.where(torch.isfinite(new_max), new_max, torch.zeros_like(new_max))
        rescale = torch.exp(maximum-safe_max)
        weights = torch.exp(scores-safe_max[...,None])
        accumulator = rescale[...,None]*accumulator+weights@v
        normalizer = rescale*normalizer+weights.sum(-1)
        maximum, seen = new_max, True
    if not seen:
        raise ValueError("at least one nonempty tile")
    # Explicit all-masked policy: return zero, avoiding 0/0 and -inf-(-inf).
    return accumulator/normalizer.clamp_min(torch.finfo(torch.float64).tiny)[...,None]


@torch.no_grad()
def online_consume(model, cache, owner, tokens, tile=2):
    """Actual complete Hermon stack with online attention and offset masks."""
    paging.positive(tile)
    native.validate(model, cache, owner)
    tokens = native.tokens_copy(tokens, model.max_len-len(cache.tokens))
    if not tokens:
        return torch.empty(0,4,dtype=torch.float64), cache
    past, count = len(cache.tokens), len(tokens)
    z = model.tok(torch.tensor(tokens))+model.pos(torch.arange(past,past+count))
    allowed = native.allowed_mask(past,count)
    layers = []
    for block, old in zip(model.blocks, cache.layers):
        a = block.attn
        q,k,v = a.qkv(block.n1(z)).view(count,3,a.h,a.dh).permute(1,2,0,3)
        k,v = torch.cat((old.k,k),1), torch.cat((old.v,v),1)
        tiles = ((k[:,i:i+tile],v[:,i:i+tile],allowed[:,i:i+tile])
                 for i in range(0,past+count,tile))
        y = online_attention(q, tiles).transpose(0,1).reshape(count,model.d)
        z = z+a.out(y)
        z = z+block.ff(block.n2(z))
        layers.append(native.LayerKV(k.clone(),v.clone()))
    result = native.sealed(owner,cache.artifact,cache.tokens+tokens,layers)
    native.validate(model,result,owner)
    logits = model.lm(model.norm(z))
    if not bool(torch.isfinite(logits).all()):
        raise ValueError("nonfinite logits")
    return logits, result


def paged_attention(pool, handle, owner, layer, q, query_positions):
    state = pool.state(handle,owner)
    if (type(layer) is not int or not 0 <= layer < len(pool.model.blocks)
            or len(query_positions) != q.shape[1]
            or any(type(p) is not int or not 0 <= p < len(state.tokens) for p in query_positions)):
        raise ValueError("layer and logical query ordinals")
    tiles = []
    for b,ref in enumerate(state.pages):
        kv = pool.page(ref).layers[layer]
        keys = torch.arange(b*pool.page_size,b*pool.page_size+kv.k.shape[1])
        allowed = keys[None,:] <= torch.tensor(query_positions)[:,None]
        tiles.append((kv.k,kv.v,allowed))
    return online_attention(q,tiles)


def traffic_model(T,dq,dv,b=2,tiled=False):
    for x in (T,dq,dv,b):
        paging.positive(x)
    base = (dq+T*dq+T*dv+dv)*b
    return {"base":base,"score_read_write":0 if tiled else 2*T*b,
            "total":base+(0 if tiled else 2*T*b)}


def results():
    p,q = np.array([.55,.25,.15,.05]), np.array([.45,.35,.15,.05])
    model,owner = native.tiny_model(), ("tenant","online")
    tokens = (0,1,2,3,0,2)
    rows = []
    for tile in (1,2,4,32):
        _,cache = native.prefill(model,owner,tokens[:3])
        y,cache = online_consume(model,cache,owner,tokens[3:],tile)
        rows.append({"tile":tile,"error":(y-native.full_oracle(model,tokens)[3:]).abs().max().item()})
    return {"acceptance":[{"token":i,"p":p[i],"q":q[i],"accepted":min(p[i],q[i]),
                           "residual":max(p[i]-q[i],0)} for i in range(4)],
            "output":output_distribution(p,q).tolist(),"expected_acceptance":float(np.minimum(p,q).sum()),
            "attention":rows,
            "traffic":[{"method":"scores","bytes":traffic_model(4096,128,128)["total"]},
                       {"method":"online","bytes":traffic_model(4096,128,128,tiled=True)["total"]}]}


TABLES = [("acceptance",["Token","Target p","Draft q","Accepted mass","Missing mass"],
           ["token","p","q","accepted","residual"],"rrrrr"),
          ("attention",["Tile tokens","Max full-model logit error"],["tile","error"],"rr"),
          ("traffic",["One-query model","Bytes"],["method","bytes"],"lr")]
PLOTS = []
LISTINGS = ["verify","native_speculative","online_attention","online_consume"]
