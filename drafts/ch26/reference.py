"""EVOD-26: affine schedule and gradient oracles; no global dtype mutation or speed claim."""

import json
import torch


def validate(a, b, h0):
    if not all(isinstance(x, torch.Tensor) for x in (a, b, h0)):
        raise ValueError("Tensor inputs required")
    if a.ndim < 2 or a.shape != b.shape or a.shape[1:] != h0.shape or h0.numel() == 0:
        raise ValueError("a,b: [T,*state], h0: [*state] with nonempty state")
    if not all(x.is_floating_point() for x in (a, b, h0)):
        raise ValueError("Real floating tensors required")
    if (
        len({x.dtype for x in (a, b, h0)}) != 1
        or len({x.device for x in (a, b, h0)}) != 1
    ):
        raise ValueError("Matching dtype/device required")
    if not all(torch.isfinite(x).all() for x in (a, b, h0)):
        raise ValueError("Finite inputs required")


def compose(left, right):
    """Chronological left then right; noncommutative affine composition."""
    a_left, b_left = left
    a_right, b_right = right
    if (
        a_left.shape != b_left.shape
        or a_right.shape != b_right.shape
        or a_left.shape != a_right.shape
    ):
        raise ValueError("Equal affine state shapes required")
    return a_right * a_left, a_right * b_left + b_right


def effective_maps(a, b, h_reset, resets=None, valid=None):
    """Fold reset-before-valid-step and padding identity into affine coefficients."""
    validate(a, b, h_reset)
    t = a.shape[0]
    if resets is None:
        resets = torch.zeros(t, dtype=torch.bool, device=a.device)
    if valid is None:
        valid = torch.ones(t, dtype=torch.bool, device=a.device)
    for mask in (resets, valid):
        if (
            not isinstance(mask, torch.Tensor)
            or mask.shape != (t,)
            or mask.dtype != torch.bool
            or mask.device != a.device
        ):
            raise ValueError("Boolean time masks on coefficient device required")
    if (resets & ~valid).any():
        raise ValueError("Padding cannot request a reset")
    shape = (t,) + (1,) * (a.ndim - 1)
    r, v = resets.reshape(shape), valid.reshape(shape)
    aa = torch.where(r, torch.zeros_like(a), a)
    bb = torch.where(r, a * h_reset + b, b)
    return torch.where(v, aa, torch.ones_like(a)), torch.where(
        v, bb, torch.zeros_like(b)
    )


def sequential(a, b, h0, resets=None, valid=None, h_reset=None):
    """Independent literal reset/update loop; T=0 returns empty states and h0."""
    validate(a, b, h0)
    h_reset = h0 if h_reset is None else h_reset
    effective_maps(
        a, b, h_reset, resets, valid
    )  # validate masks without using transformed maps
    resets = (
        torch.zeros(a.shape[0], dtype=torch.bool, device=a.device)
        if resets is None
        else resets
    )
    valid = torch.ones_like(resets) if valid is None else valid
    states, h = [], h0
    for index in range(a.shape[0]):
        if bool(valid[index]):
            if bool(resets[index]):
                h = h_reset
            h = a[index] * h + b[index]
        states.append(h)
    return torch.stack(states) if states else a.clone(), h


def hillis_steele_scan(a, b):
    """Inclusive scan: every stage reads the previous stage, never partially updated data."""
    if a.ndim < 2:
        raise ValueError("Time and state dimensions required")
    validate(a, b, a.new_zeros(a.shape[1:]))
    aa, bb = a, b
    offset = 1
    while offset < a.shape[0]:
        tail_a = aa[offset:] * aa[:-offset]
        tail_b = aa[offset:] * bb[:-offset] + bb[offset:]
        aa = torch.cat((aa[:offset], tail_a), dim=0)
        bb = torch.cat((bb[:offset], tail_b), dim=0)
        offset *= 2
    return aa, bb


def scan_states(a, b, h0, resets=None, valid=None, h_reset=None):
    validate(a, b, h0)
    maps = effective_maps(a, b, h0 if h_reset is None else h_reset, resets, valid)
    aa, bb = hillis_steele_scan(*maps)
    states = aa * h0 + bb
    return states, states[-1] if len(states) else h0


def chunked(a, b, h0, chunk, resets=None, valid=None, h_reset=None, detach=False):
    """Chunk boundaries carry state; optional detach is an explicit gradient-changing mutant."""
    validate(a, b, h0)
    if type(chunk) is not int or chunk <= 0:
        raise ValueError("Positive integer chunk size required")
    if type(detach) is not bool:
        raise ValueError("Detach intervention must be Boolean")
    h_reset = h0 if h_reset is None else h_reset
    effective_maps(a, b, h_reset, resets, valid)
    states, h = [], h0
    for start in range(0, a.shape[0], chunk):
        end = start + chunk
        xx, h = sequential(
            a[start:end],
            b[start:end],
            h,
            None if resets is None else resets[start:end],
            None if valid is None else valid[start:end],
            h_reset,
        )
        states.append(xx)
        if detach and end < a.shape[0]:
            h = h.detach()
    return torch.cat(states) if states else a.clone(), h


def closed_form(a, b, h0):
    """O(T^2 D) product/sum oracle, with no division and no scan composition."""
    validate(a, b, h0)
    states = []
    for end in range(1, len(a) + 1):
        value = a[:end].prod(dim=0) * h0
        suffix = torch.ones_like(h0)
        for start in range(end - 1, -1, -1):
            value = value + suffix * b[start]
            suffix = suffix * a[start]
        states.append(value)
    return torch.stack(states) if states else a.clone()


def analytic_adjoint(a, b, h0, weights):
    """Independent reverse derivative for L=sum_t,d weights[t,d]*h[t,d]."""
    states, _ = sequential(a, b, h0)
    if weights.shape != states.shape:
        raise ValueError("One loss weight per state element required")
    lam = torch.zeros_like(h0)
    ga, gb = [], []
    for index in range(len(a) - 1, -1, -1):
        lam = weights[index] + (a[index + 1] * lam if index + 1 < len(a) else 0)
        prior = h0 if index == 0 else states[index - 1]
        ga.append(lam * prior)
        gb.append(lam)
    if not len(a):
        return a.clone(), b.clone(), torch.zeros_like(h0)
    return torch.stack(ga[::-1]), torch.stack(gb[::-1]), a[0] * lam


def work_depth(length):
    if type(length) is not int or length < 0:
        raise ValueError("Nonnegative integer length required")
    offsets, offset = [], 1
    while offset < length:
        offsets.append(offset)
        offset *= 2
    return {
        "length": length,
        "stages": len(offsets),
        "pair_compositions": sum(length - x for x in offsets),
        "sequential_depth": length,
    }


def parity(seed=26, length=17, dimensions=5):
    generator = torch.Generator().manual_seed(seed)
    a = (
        0.8
        + 0.1 * torch.rand(length, dimensions, generator=generator, dtype=torch.float64)
    ).requires_grad_()
    b = (
        torch.randn(length, dimensions, generator=generator, dtype=torch.float64) * 0.1
    ).requires_grad_()
    h0 = torch.randn(
        dimensions, generator=generator, dtype=torch.float64
    ).requires_grad_()
    sequential_states, _ = sequential(a, b, h0)
    parallel, _ = scan_states(a, b, h0)
    chunks, _ = chunked(a, b, h0, 4)
    direct = closed_form(a, b, h0)
    weights = torch.randn(length, dimensions, generator=generator, dtype=torch.float64)
    gradients = []
    for value in (sequential_states, parallel, chunks, direct):
        gradients.append(
            torch.autograd.grad((weights * value).sum(), (a, b, h0), retain_graph=True)
        )
    analytic = analytic_adjoint(a.detach(), b.detach(), h0.detach(), weights)
    return {
        "forward_max_abs": max(
            (value - sequential_states).abs().max().item()
            for value in (parallel, chunks, direct)
        ),
        "gradient_max_abs": max(
            (x - y).abs().max().item()
            for group in gradients[1:]
            for x, y in zip(gradients[0], group)
        ),
        "analytic_adjoint_max_abs": max(
            (x - y).abs().max().item() for x, y in zip(gradients[0], analytic)
        ),
    }


def results():
    a = torch.tensor([[0.5], [2.0], [0.0], [-1.0]], dtype=torch.float64)
    b = torch.tensor([[1.0], [0.5], [3.0], [2.0]], dtype=torch.float64)
    h0 = torch.tensor([2.0], dtype=torch.float64)
    states, _ = sequential(a, b, h0)
    aa, bb = hillis_steele_scan(a, b)
    trace = [
        {
            "step": i + 1,
            "a": a[i].item(),
            "b": b[i].item(),
            "A": aa[i].item(),
            "B": bb[i].item(),
            "h": states[i].item(),
        }
        for i in range(4)
    ]
    rounding_a = torch.ones(3, 1, dtype=torch.float64)
    rounding_b = torch.tensor([[1e16], [-1e16], [1]], dtype=torch.float64)
    seq, _ = sequential(rounding_a, rounding_b, torch.zeros(1, dtype=torch.float64))
    scan, _ = scan_states(rounding_a, rounding_b, torch.zeros(1, dtype=torch.float64))
    return {
        **parity(),
        "trace": trace,
        "work": [work_depth(t) for t in (0, 1, 4, 17, 1024)],
        "cancellation_sequential_final": seq[-1].item(),
        "cancellation_scan_final": scan[-1].item(),
        "scope": "reference algebra/gradients, not trained DOGMA, Hermon KV or hardware benchmark",
    }


TABLES = [
    (
        "trace",
        ["Step", "$a$", "$b$", "$A$", "$B$", "$h$"],
        ["step", "a", "b", "A", "B", "h"],
        "rrrrrr",
    ),
    (
        "work",
        ["Length", "Scan stages", "Pair ops", "Loop depth"],
        ["length", "stages", "pair_compositions", "sequential_depth"],
        "rrrr",
    ),
]
PLOTS = []
LISTINGS = [
    "compose",
    "effective_maps",
    "hillis_steele_scan",
    "chunked",
    "analytic_adjoint",
]

if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
