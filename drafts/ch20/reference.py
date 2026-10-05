"""Structured-memory teaching reference, not a trained DOGMA model."""

import json
import math
from dataclasses import dataclass
import torch

LISTINGS = ["retention", "Memory", "validate", "multiscale"]
TABLES = [
    (
        "trace",
        ["Position", "Fast", "Slow bank", "Block state", "Phase"],
        ["position", "fast", "bank", "coarse", "phase"],
        "rrrrr",
    ),
    (
        "timescales",
        ["Retention", "e-fold time", "Half-life", "Weight now"],
        ["a", "tau", "half", "weight"],
        "rrrr",
    ),
]
PLOTS = [("kernel-plot", "kernel", "lag", ["fast", "slow"])]


def retention(taus, delta=1.0):
    """taus and delta are measured in the same declared clock units."""
    if (
        taus.ndim != 1
        or taus.numel() == 0
        or not taus.is_floating_point()
    ):
        raise ValueError("nonempty floating timescale vector required")
    if not torch.isfinite(taus).all() or (taus <= 0).any():
        raise ValueError("positive finite timescales required")
    if not math.isfinite(delta) or delta < 0:
        raise ValueError("finite nonnegative elapsed distance required")
    exponent = -delta / taus
    return torch.exp(exponent), -torch.expm1(exponent)


@dataclass(frozen=True)
class Memory:
    bank: torch.Tensor  # [K,D]
    coarse: torch.Tensor  # [D]
    pending: torch.Tensor  # [D], sum since last complete block
    phase: int  # valid positions since last commit


def validate(values, taus, block_size, rho, mask, carry):
    if (
        values.ndim != 2
        or not values.is_floating_point()
        or values.shape[1] == 0
    ):
        raise ValueError("floating values [T,D] with D > 0 required")
    if not torch.isfinite(values).all():
        raise ValueError("finite values required, including masked slots")
    if values.device != taus.device or values.dtype != taus.dtype:
        raise ValueError("values and timescales must share dtype/device")
    retention(taus)
    if type(block_size) is not int or block_size <= 0:
        raise ValueError("positive integer block size required")
    if not math.isfinite(rho) or not 0 <= rho <= 1:
        raise ValueError("coarse retention must lie in [0,1]")
    if len(mask) != len(values) or any(type(v) is not bool for v in mask):
        raise ValueError("one Boolean validity flag per slot required")
    if carry is not None:
        shapes = [(len(taus), values.shape[1]), (values.shape[1],)]
        for tensor, shape in zip(
            (carry.bank, carry.coarse, carry.pending),
            (shapes[0], shapes[1], shapes[1]),
        ):
            if (
                tensor.shape != shape
                or tensor.dtype != values.dtype
                or tensor.device != values.device
                or not torch.isfinite(tensor).all()
            ):
                raise ValueError("incompatible carried tensor")
        if (
            type(carry.phase) is not int
            or not 0 <= carry.phase < block_size
        ):
            raise ValueError("invalid block phase")
        if carry.phase == 0 and torch.count_nonzero(carry.pending):
            raise ValueError("an empty block must have zero pending sum")


def multiscale(
    values, taus, block_size=4, rho=0.5, mask=None, carry=None
):
    """Valid-token clock. Padding holds all fields; a chunk never flushes."""
    mask = (True,) * len(values) if mask is None else tuple(mask)
    validate(values, taus, block_size, rho, mask, carry)
    k, d = len(taus), values.shape[1]
    state = (
        carry
        if carry is not None
        else Memory(
            values.new_zeros(k, d),
            values.new_zeros(d),
            values.new_zeros(d),
            0,
        )
    )
    a, write = retention(taus)
    history = [state]
    for value, valid in zip(values, mask):
        if valid:
            bank = a[:, None] * state.bank + write[:, None] * value
            pending, phase = state.pending + value, state.phase + 1
            coarse = state.coarse
            if phase == block_size:
                coarse = rho * coarse + (1 - rho) * (pending / block_size)
                pending, phase = torch.zeros_like(pending), 0
            state = Memory(bank, coarse, pending, phase)
        history.append(state)
    return state, tuple(history)


def convolution(values, taus):
    """Independent closed-form bank from zero state; no masking."""
    a, write = retention(taus)
    n = len(values)
    exponents = torch.arange(
        n - 1, -1, -1, dtype=values.dtype, device=values.device
    )
    weights = write[:, None] * a[:, None] ** exponents[None, :]
    return weights @ values


def results():
    taus = torch.tensor(
        [-1 / math.log(a) for a in (0.5, 0.875)], dtype=torch.float64
    )
    values = torch.tensor([[1.0]] + [[0.0]] * 7, dtype=torch.float64)
    _, history = multiscale(values, taus)
    return {
        "trace": [
            dict(
                position=i,
                fast=round(s.bank[0, 0].item(), 6),
                bank=round(s.bank[1, 0].item(), 6),
                coarse=round(s.coarse[0].item(), 6),
                phase=s.phase,
            )
            for i, s in enumerate(history)
        ],
        "timescales": [
            dict(
                a=a,
                tau=round(-1 / math.log(a), 6),
                half=round(-math.log(2) / math.log(a), 6),
                weight=1 - a,
            )
            for a in (0.5, 0.875)
        ],
        "kernel": [
            dict(lag=l, fast=0.5 * 0.5**l, slow=0.125 * 0.875**l)
            for l in range(41)
        ],
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
