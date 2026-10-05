"""Proposed input-conditioned DOGMA operator; no trained capability claim."""

import json
import math
import torch

BASES = "ACGT"
PAIRS = tuple(a + b for a in BASES for b in BASES)
LISTINGS = [
    "pair_ids",
    "coefficients",
    "selective_scan",
    "feedback_step",
]
TABLES = [
    (
        "trace",
        ["Pair", "Write gate", "Retention", "State"],
        ["pair", "gate", "retention", "state"],
        "lrrr",
    ),
    (
        "ablation",
        ["Variant", "AACA", "ACAA", "Difference"],
        ["variant", "first", "second", "difference"],
        "lrrr",
    ),
]
PLOTS = [
    ("feedback-plot", "feedback", "h", ["mapped", "identity"]),
    ("ablation-plot", "trajectories", "step", ["first", "second"]),
]


def pair_ids(sequence, previous=""):
    """Compile record symbols to causal adjacent-pair row IDs; -1 means first base."""
    if previous not in ("", *BASES) or any(
        x not in BASES for x in sequence
    ):
        raise ValueError("canonical DNA symbols required")
    ids = []
    for x in sequence:
        ids.append(PAIRS.index(previous + x) if previous else -1)
        previous = x
    return tuple(ids), previous


def coefficients(write_logits, retention_logits):
    """Input-only gates: a in (0,1), fresh-candidate weight 1-a."""
    if write_logits.shape != retention_logits.shape:
        raise ValueError("matching gate shapes required")
    gate = torch.sigmoid(write_logits)
    retention = torch.sigmoid(retention_logits)
    a = 1 - gate * (1 - retention)
    return a, gate, retention


def selective_scan(
    ids, candidates, write_logits, retention_logits, state=None
):
    """One record, tables [16,D], state [D]. -1 is the exact no-pair identity."""
    ids = tuple(ids)
    if candidates.ndim != 2 or candidates.shape[0] != 16:
        raise ValueError("candidate table must have shape [16,D]")
    if any(
        t.shape != candidates.shape
        or t.dtype != candidates.dtype
        or t.device != candidates.device
        for t in (write_logits, retention_logits)
    ):
        raise ValueError("tables must share shape, dtype and device")
    if not candidates.is_floating_point() or any(
        not torch.isfinite(t).all()
        for t in (candidates, write_logits, retention_logits)
    ):
        raise ValueError("finite floating tables required")
    if any(type(i) is not int or not -1 <= i < 16 for i in ids):
        raise ValueError("pair IDs must be -1 or 0..15")
    h = (
        candidates.new_zeros(candidates.shape[1])
        if state is None
        else state
    )
    if (
        h.shape != candidates.shape[1:]
        or h.dtype != candidates.dtype
        or h.device != candidates.device
        or not torch.isfinite(h).all()
    ):
        raise ValueError(
            "state must match table channels, dtype and device"
        )
    a, _, _ = coefficients(write_logits, retention_logits)
    history = [h]
    for i in ids:
        if i >= 0:
            h = a[i] * h + (1 - a[i]) * candidates[i]
        history.append(h)
    return h, tuple(history)


def feedback_step(h, weight=8.0):
    """Counterexample: bounded candidate, state-dependent gate, noncontracting map."""
    gate = torch.sigmoid(weight * h)
    return (1 - gate) * h + gate


def tables():
    candidate = torch.zeros(16, 1, dtype=torch.float64)
    for pair, value in (("AA", 0), ("AC", 1), ("CA", -1)):
        candidate[PAIRS.index(pair), 0] = value
    zeros = torch.zeros_like(candidate)
    return candidate, zeros.clone(), zeros.clone()


def results():
    v, u, r = tables()
    first, h1 = selective_scan(pair_ids("AACA")[0], v, u, r)
    second, h2 = selective_scan(pair_ids("ACAA")[0], v, u, r)
    rows = []
    for name, uu, rr in (
        ("baseline", u, r),
        ("write near zero", u - 12, r),
        ("retention near one", u, r + 12),
    ):
        x = selective_scan(pair_ids("AACA")[0], v, uu, rr)[0].item()
        y = selective_scan(pair_ids("ACAA")[0], v, uu, rr)[0].item()
        rows.append(
            dict(
                variant=name,
                first=f"{x:.6g}",
                second=f"{y:.6g}",
                difference=f"{x - y:.6g}",
            )
        )
    return {
        "trace": [
            dict(
                pair=PAIRS[i],
                gate=0.5,
                retention=0.5,
                state=round(h.item(), 6),
            )
            for i, h in zip(pair_ids("AACA")[0], h1[1:])
            if i >= 0
        ],
        "ablation": rows,
        "trajectories": [
            dict(step=i, first=a.item(), second=b.item())
            for i, (a, b) in enumerate(zip(h1, h2))
        ],
        "feedback": [
            dict(
                h=i / 100,
                mapped=feedback_step(
                    torch.tensor(i / 100, dtype=torch.float64)
                ).item(),
                identity=i / 100,
            )
            for i in range(-50, 51)
        ],
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
