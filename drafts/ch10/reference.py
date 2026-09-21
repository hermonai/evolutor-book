"""Deterministic top-1 teaching reference, not an optimized MoE runtime."""

import importlib.util
import math
from pathlib import Path
import torch
from torch.nn import functional as F

_spec = importlib.util.spec_from_file_location(
    "chapter9_for_routing", Path(__file__).parents[1] / "ch09/reference.py"
)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)


def plan(logits, valid, capacity, used=None):
    """Top-1, first-index ties, first-arrival admission; padding excluded."""
    if (
        logits.ndim != 2
        or min(logits.shape) < 1
        or not logits.is_floating_point()
        or not torch.isfinite(logits).all()
    ):
        raise ValueError("finite floating logits[T,E] required")
    t, e = logits.shape
    if valid.shape != (t,) or valid.dtype != torch.bool:
        raise ValueError("boolean validity[T] required")
    if type(capacity) is not int or capacity < 0:
        raise ValueError("nonnegative integer capacity required")
    used = [0] * e if used is None else list(used)
    if len(used) != e or any(
        type(n) is not int or not 0 <= n <= capacity for n in used
    ):
        raise ValueError("one bounded integer counter per expert required")
    p = torch.softmax(logits, dim=-1)
    selected = p.argmax(-1)
    accepted = torch.zeros(t, dtype=torch.bool, device=logits.device)
    demand = [0] * e
    for i in range(t):
        if bool(valid[i]):
            j = int(selected[i])
            demand[j] += 1
            if used[j] < capacity:
                accepted[i] = True
                used[j] += 1
    return dict(
        probability=p,
        selected=selected,
        accepted=accepted,
        demand=demand,
        used=used,
    )


def expert(x, weights, j):
    return (
        F.gelu(x @ weights["w1"][j] + weights["b1"][j], approximate="none")
        @ weights["w2"][j]
        + weights["b2"][j]
    )


def dispatch(x, weights, routing):
    """Gather admitted rows only; scatter weighted results to original rows."""
    p, chosen, keep = (
        routing[k] for k in ("probability", "selected", "accepted")
    )
    if x.ndim != 2 or x.shape[0] != p.shape[0]:
        raise ValueError("matching token axis required")
    out = x * 0 + p.sum() * 0
    for j in range(p.shape[1]):
        ids = torch.where(keep & (chosen == j))[0]
        if len(ids):
            values = expert(x[ids], weights, j) * p[ids, j, None]
            out = out.index_copy(0, ids, values)
    return out


def dense_oracle(x, weights, routing):
    """Compute every expert, then mask. Correctness oracle, not sparse execution."""
    p, chosen, keep = (
        routing[k] for k in ("probability", "selected", "accepted")
    )
    all_values = torch.stack(
        [expert(x, weights, j) for j in range(p.shape[1])], dim=1
    )
    gate = F.one_hot(chosen, p.shape[1]) * keep[:, None] * p
    return (all_values * gate[:, :, None]).sum(1)


def balance_loss(routing, valid, alpha=0.01):
    """Demand fractions before overflow; discrete assignment is not differentiated."""
    if not math.isfinite(alpha) or alpha < 0 or not bool(valid.any()):
        raise ValueError(
            "nonnegative coefficient and valid tokens required"
        )
    p = routing["probability"][valid]
    chosen = routing["selected"][valid]
    fraction = F.one_hot(chosen, p.shape[1]).to(p.dtype).mean(0)
    return alpha * p.shape[1] * (fraction * p.mean(0)).sum()


def expert_weights(e=3, d=4, hidden=8):
    gen = torch.Generator().manual_seed(17)
    shapes = dict(
        w1=(e, d, hidden), b1=(e, hidden), w2=(e, hidden, d), b2=(e, d)
    )
    return {
        k: (
            torch.randn(shape, generator=gen, dtype=torch.float64) * 0.2
        ).requires_grad_()
        for k, shape in shapes.items()
    }


def sparse_block(
    x,
    block_weights,
    router,
    experts,
    valid,
    capacity,
    allowed=None,
    used=None,
):
    """Replace only Chapter 9's FFN branch; no dropout in this reference."""
    normalized = base.layer_norm(
        x, block_weights["g1"], block_weights["n1"]
    )
    attention, _ = base.multihead(
        normalized, block_weights, heads=2, allowed=allowed
    )
    u = x + attention
    z = base.layer_norm(u, block_weights["g2"], block_weights["n2"])
    routing = plan(z @ router, valid, capacity, used)
    return u + dispatch(z, experts, routing), routing


def cost(tokens, experts, width, hidden, admitted):
    """Matrix MACs; excludes bias, activation, selection, and transfers."""
    for value in (tokens, experts, width, hidden, admitted):
        if type(value) is not int or value < 0:
            raise ValueError("nonnegative integer sizes required")
    if min(experts, width, hidden) == 0 or admitted > tokens:
        raise ValueError(
            "positive dimensions and admitted <= tokens required"
        )
    return dict(
        router_macs=tokens * width * experts,
        expert_macs=2 * admitted * width * hidden,
        all_expert_macs=2 * tokens * experts * width * hidden,
        expert_parameters=experts * (2 * width * hidden + hidden + width),
    )


def results():
    probability = torch.tensor(
        [
            [0.8, 0.15, 0.05],
            [0.7, 0.2, 0.1],
            [0.6, 0.3, 0.1],
            [0.1, 0.2, 0.7],
            [0.15, 0.75, 0.1],
            [0.1, 0.8, 0.1],
        ],
        dtype=torch.float64,
    )
    logits, valid = probability.log(), torch.ones(6, dtype=torch.bool)
    r = plan(logits, valid, 2)
    trace = [
        dict(
            token=i,
            expert=int(r["selected"][i]),
            gate=round(float(r["probability"][i].max()), 8),
            admitted=bool(r["accepted"][i]),
        )
        for i in range(6)
    ]
    sweep = []
    for c in range(5):
        q = plan(logits, valid, c)
        admitted = int(q["accepted"].sum())
        sweep.append(
            dict(
                capacity=c,
                admitted=admitted,
                dropped=6 - admitted,
                unused=3 * c - admitted,
            )
        )
    tied = plan(torch.zeros(6, 3, dtype=torch.float64), valid, 2)
    return dict(
        trace=trace,
        sweep=sweep,
        demand=r["demand"],
        admitted=r["used"],
        balance=float(balance_loss(r, valid)),
        tied_balance=float(balance_loss(tied, valid)),
        tied_demand=tied["demand"],
        cost=cost(6, 3, 4, 8, 5),
    )
