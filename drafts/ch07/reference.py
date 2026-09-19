"""Original diagonal affine scan lessons; not a Mamba/S4 implementation."""

import json
import math
import torch


def compose(earlier, later):
    """Chronological composition: later(earlier(h))."""
    a, b = earlier
    c, d = later
    return c * a, c * b + d


def check_shapes(a, b, h):
    if a.ndim != 2 or b.shape != a.shape or h.shape != a.shape[1:]:
        raise ValueError("a,b: [time,state]; h: [state]")
    if not a.is_floating_point() or any(
        v.dtype != a.dtype or v.device != a.device for v in (b, h)
    ):
        raise ValueError("matching floating dtype and device required")
    if not all(torch.isfinite(v).all() for v in (a, b, h)):
        raise ValueError("finite inputs required")


def sequential(a, b, h):
    check_shapes(a, b, h)
    outputs = []
    for at, bt in zip(a, b):
        h = at * h + bt
        outputs.append(h)
    return torch.stack(outputs) if outputs else b + h[None, :]


def prefix_pairs(a, b):
    """Work-efficient inclusive prefix DAG; Python executes its nodes serially."""
    size = a.shape[0]
    if size <= 1:
        return a, b
    paired = size // 2
    ra, rb = compose(
        (a[: 2 * paired : 2], b[: 2 * paired : 2]),
        (a[1 : 2 * paired : 2], b[1 : 2 * paired : 2]),
    )
    pa, pb = prefix_pairs(ra, rb)
    out_a, out_b = [a[0]], [b[0]]
    for i in range(1, size):
        if i % 2:
            ca, cb = pa[i // 2], pb[i // 2]
        else:
            ca, cb = compose((pa[i // 2 - 1], pb[i // 2 - 1]), (a[i], b[i]))
        out_a.append(ca)
        out_b.append(cb)
    return torch.stack(out_a), torch.stack(out_b)


def parallel_form(a, b, h):
    check_shapes(a, b, h)
    pa, pb = prefix_pairs(a, b)
    return pa * h[None, :] + pb


def zoh(decay, delta):
    """dh/ds=-decay*h+u, piecewise constant u; decay>0, delta>=0."""
    if not isinstance(decay, torch.Tensor) or not isinstance(
        delta, torch.Tensor
    ):
        raise ValueError("tensors required")
    if (
        not torch.isfinite(decay).all()
        or not torch.isfinite(delta).all()
        or torch.any(decay <= 0)
        or torch.any(delta < 0)
    ):
        raise ValueError(
            "finite positive decay and nonnegative interval required"
        )
    z = -decay * delta
    return torch.exp(z), -torch.expm1(z) / decay


def selected_coefficients(x, weights, bias, decay):
    """x [T,D], weights [D,N], bias/decay [N]; current-input selection only."""
    delta = torch.nn.functional.softplus(x @ weights + bias)
    a, gain = zoh(decay, delta)
    # Original teaching input projection, not an architecture reproduction.
    drive = x @ weights
    return a, gain * drive


def convolution_form(x, a, gain, readout):
    """Scalar LTI zero-state causal convolution, implemented directly."""
    return (
        torch.stack(
            [
                sum(
                    readout * gain * a ** (t - j) * x[j]
                    for j in range(t + 1)
                )
                for t in range(len(x))
            ]
        )
        if len(x)
        else x.clone()
    )


def operation_count(n):
    if type(n) is not int or n < 0:
        raise ValueError("nonnegative length required")
    if n <= 1:
        return 0
    return n // 2 + (n - 1) // 2 + operation_count(n // 2)


def results():
    dtype = torch.float64
    a = torch.tensor([[0.5], [1.0], [0.25], [0.8]], dtype=dtype)
    b = torch.tensor([[1.0], [0.0], [2.0], [-1.0]], dtype=dtype)
    h = torch.tensor([2.0], dtype=dtype)
    pa, pb = prefix_pairs(a, b)
    x = torch.tensor([1.0, 2.0, -1.0, 3.0], dtype=dtype)
    lti = convolution_form(x, 0.5, 1.0, 1.0)
    states = sequential(
        torch.full((4, 1), 0.5, dtype=dtype),
        x[:, None],
        torch.zeros(1, dtype=dtype),
    )
    decay = torch.tensor(1.0, dtype=dtype)
    ds = [0.0, 0.01, 0.1, 1.0, 3.0]
    return {
        "trace": [
            {
                "t": i + 1,
                "a": float(a[i, 0]),
                "b": float(b[i, 0]),
                "prefix_a": float(pa[i, 0]),
                "prefix_b": float(pb[i, 0]),
                "state": float(parallel_form(a, b, h)[i, 0]),
            }
            for i in range(4)
        ],
        "lti": lti.tolist(),
        "lti_max_error": float((lti - states[:, 0]).abs().max()),
        "zoh": [
            {
                "delta": d,
                "a": float(zoh(decay, torch.tensor(d, dtype=dtype))[0]),
                "gain": float(zoh(decay, torch.tensor(d, dtype=dtype))[1]),
            }
            for d in ds
        ],
        "work": [
            {"n": n, "compositions": operation_count(n)}
            for n in [1, 2, 4, 8, 16, 32, 64]
        ],
        "memory_curve": [
            {"step": n, "fast": math.exp(-n), "slow": math.exp(-0.1 * n)}
            for n in range(0, 41)
        ],
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
