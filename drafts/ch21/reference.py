"""Exact strand-action teaching reference; no trained genomic model."""

import json
import torch

COMP = (3, 2, 1, 0)  # channels A,C,G,T
LISTINGS = ["rc", "causal", "dual", "strand_head", "chunked_dual"]
TABLES = [
    (
        "trace",
        ["Position", "Base", "Forward", "Aligned reverse", "Sum"],
        ["position", "base", "forward", "reverse", "sum"],
        "rlrrr",
    ),
]
PLOTS = []


def encode(sequence):
    if not isinstance(sequence, str) or any(
        b not in "ACGT" for b in sequence
    ):
        raise ValueError("canonical uppercase DNA string required")
    ids = torch.tensor(
        ["ACGT".index(b) for b in sequence], dtype=torch.long
    )
    return torch.nn.functional.one_hot(ids, num_classes=4).to(
        torch.float64
    )


def matrix(x, width=None):
    if (
        x.ndim != 2
        or not x.is_floating_point()
        or not torch.isfinite(x).all()
    ):
        raise ValueError("finite floating matrix required")
    if width is not None and x.shape[1] != width:
        raise ValueError("wrong channel count")


def rc(x):
    """Reverse positions and complement canonical base coordinates."""
    matrix(x, 4)
    return x.flip(0)[:, COMP]


def swap_reverse(z):
    matrix(z)
    if z.shape[1] == 0 or z.shape[1] % 2:
        raise ValueError("two equally sized hidden blocks required")
    left, right = z.flip(0).chunk(2, dim=1)
    return torch.cat((right, left), dim=1)


def causal(x, weight, retention, carry=None):
    """h_t = a*h_(t-1) + x_t W; this is NOT a convex-average update."""
    matrix(x, 4)
    matrix(weight)
    d = weight.shape[1]
    if weight.shape[0] != 4 or d == 0 or retention.shape != (d,):
        raise ValueError("W[4,D], a[D], D>0 required")
    if (
        not torch.isfinite(retention).all()
        or ((retention < 0) | (retention >= 1)).any()
    ):
        raise ValueError("retention must lie in [0,1)")
    if any(
        t.dtype != x.dtype or t.device != x.device
        for t in (weight, retention)
    ):
        raise ValueError("shared floating dtype/device required")
    h = x.new_zeros(d) if carry is None else carry
    if (
        h.shape != (d,)
        or h.dtype != x.dtype
        or h.device != x.device
        or not torch.isfinite(h).all()
    ):
        raise ValueError("incompatible carry")
    rows = []
    for row in x:
        h = retention * h + row @ weight
        rows.append(h)
    return (torch.stack(rows) if rows else x.new_empty((0, d))), h


def dual(x, weight, retention):
    """Full-record operator: second half uses suffix information."""
    forward, _ = causal(x, weight, retention)
    reverse, _ = causal(rc(x), weight, retention)
    return torch.cat((forward, reverse.flip(0)), dim=1)


def strand_head(z, u, v):
    """Tied two-channel head; RC reverses positions and swaps labels."""
    matrix(z)
    if z.shape[1] == 0 or z.shape[1] % 2:
        raise ValueError("even nonzero hidden dimension required")
    d = z.shape[1] // 2
    for p in (u, v):
        if (
            p.shape != (d,)
            or p.dtype != z.dtype
            or p.device != z.device
            or not torch.isfinite(p).all()
        ):
            raise ValueError(
                "one compatible weight vector per branch required"
            )
    f, b = z.chunk(2, dim=1)
    return torch.stack((f @ u + b @ v, f @ v + b @ u), dim=1)


def chunked_dual(chunks, weight, retention):
    """Offline: reverse global chunk order AND each chunk's coordinates."""
    if not chunks:
        raise ValueError("provide at least one chunk, which may be empty")
    forward, backward = [], []
    carry = None
    for part in chunks:
        out, carry = causal(part, weight, retention, carry)
        forward.append(out)
    carry = None
    for part in reversed(chunks):
        out, carry = causal(rc(part), weight, retention, carry)
        backward.append(out)
    return torch.cat(
        (torch.cat(forward), torch.cat(backward).flip(0)), dim=1
    )


def results():
    x = encode("ACGA")
    w = torch.tensor([[1.0], [2.0], [3.0], [4.0]], dtype=torch.float64)
    a = torch.tensor([0.5], dtype=torch.float64)
    z = dual(x, w, a)
    return dict(
        trace=[
            dict(
                position=i + 1,
                base="ACGA"[i],
                forward=z[i, 0].item(),
                reverse=z[i, 1].item(),
                sum=z[i].sum().item(),
            )
            for i in range(len(x))
        ]
    )


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
