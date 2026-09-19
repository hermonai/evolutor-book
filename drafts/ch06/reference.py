"""Explicit recurrent cell arithmetic and controlled state/gradient experiments."""

import json
import math
import torch
from torch.nn import functional as F


def gru_step(x, h, parameters):
    """PyTorch reset-after convention; gate packing r,z,n."""
    wi, wh, bi, bh = parameters
    ir, iz, inn = F.linear(x, wi, bi).chunk(3, dim=-1)
    hr, hz, hn = F.linear(h, wh, bh).chunk(3, dim=-1)
    r = torch.sigmoid(ir + hr)
    z = torch.sigmoid(iz + hz)
    n = torch.tanh(inn + r * hn)
    return (1 - z) * n + z * h


def lstm_step(x, state, parameters):
    """Modern forget-gate LSTM, no peepholes or projection; i,f,g,o."""
    h, c = state
    wi, wh, bi, bh = parameters
    i, f, g, o = (F.linear(x, wi, bi) + F.linear(h, wh, bh)).chunk(
        4, dim=-1
    )
    c_new = torch.sigmoid(f) * c + torch.sigmoid(i) * torch.tanh(g)
    h_new = torch.sigmoid(o) * torch.tanh(c_new)
    return h_new, c_new


def scan_gru(x, h, parameters, lengths=None):
    """x is [batch,time,input]; padding holds state but is not a target mask."""
    if x.ndim != 3 or h.ndim != 2 or x.shape[0] != h.shape[0]:
        raise ValueError(
            "batch/time/input and batch/hidden tensors required"
        )
    batch, time, _ = x.shape
    if lengths is None:
        lengths = torch.full(
            (batch,), time, dtype=torch.long, device=x.device
        )
    if (
        lengths.shape != (batch,)
        or lengths.dtype != torch.long
        or torch.any(lengths < 0)
        or torch.any(lengths > time)
    ):
        raise ValueError("integer valid lengths required")
    states = []
    for t in range(time):
        candidate = gru_step(x[:, t], h, parameters)
        h = torch.where((t < lengths)[:, None], candidate, h)
        states.append(h)
    output = torch.stack(states, 1) if states else h[:, None, :][:, :0, :]
    return output, h


def assigned_parameters(inputs=2, hidden=2, gates=3):
    shapes = [
        (gates * hidden, inputs),
        (gates * hidden, hidden),
        (gates * hidden,),
        (gates * hidden,),
    ]
    return tuple(
        (
            torch.linspace(
                -0.4, 0.5, math.prod(shape), dtype=torch.float64
            ).reshape(shape)
            + 0.03 * i
        ).requires_grad_()
        for i, shape in enumerate(shapes)
    )


def scalar_retention(z, steps, initial=1.0):
    if not 0 <= z <= 1 or type(steps) is not int or steps < 0:
        raise ValueError(
            "retention in [0,1], nonnegative integer steps required"
        )
    h = torch.tensor(initial, dtype=torch.float64, requires_grad=True)
    start = h
    for _ in range(steps):
        h = z * h  # candidate is zero; gate independent of state
    (gradient,) = torch.autograd.grad(h, start)
    return {"state": float(h.detach()), "gradient": float(gradient)}


def chunk_experiment(detach=False, reset=False):
    x = torch.tensor(
        [1.0, 2.0, 3.0, 4.0], dtype=torch.float64, requires_grad=True
    )
    a = torch.tensor(0.5, dtype=torch.float64, requires_grad=True)
    h = torch.zeros((), dtype=torch.float64)
    for t in range(4):
        if t == 2:
            h = (
                torch.zeros_like(h)
                if reset
                else h.detach()
                if detach
                else h
            )
        h = a * h + x[t]
    gx, ga = torch.autograd.grad(h, (x, a))
    return {
        "final": float(h.detach()),
        "input_gradient": gx.tolist(),
        "parameter_gradient": float(ga),
    }


def parity():
    x = torch.tensor(
        [[0.2, -0.1], [0.7, 0.3]], dtype=torch.float64, requires_grad=True
    )
    h = torch.tensor(
        [[0.4, -0.2], [0.1, 0.6]], dtype=torch.float64, requires_grad=True
    )
    p = assigned_parameters()
    cell = torch.nn.GRUCell(2, 2, dtype=torch.float64)
    with torch.no_grad():
        for dst, src in zip(
            (cell.weight_ih, cell.weight_hh, cell.bias_ih, cell.bias_hh), p
        ):
            dst.copy_(src)
    actual = gru_step(x, h, p)
    expected = cell(x, h)
    ours = torch.autograd.grad(
        actual.square().sum(), (x, h, *p), retain_graph=True
    )
    theirs = torch.autograd.grad(
        expected.square().sum(),
        (x, h, cell.weight_ih, cell.weight_hh, cell.bias_ih, cell.bias_hh),
    )
    return {
        "max_forward_error": float(
            (actual - expected).abs().max().detach()
        ),
        "max_gradient_error": max(
            float((a - b).abs().max()) for a, b in zip(ours, theirs)
        ),
    }


def results():
    p = assigned_parameters()
    x = torch.tensor(
        [[[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0]]],
        dtype=torch.float64,
    )
    h0 = torch.zeros(1, 2, dtype=torch.float64)
    y, final = scan_gru(x, h0, p)
    y1, boundary = scan_gru(x[:, :2], h0, p)
    y2, last = scan_gru(x[:, 2:], boundary, p)
    return {
        "scope": "assigned cell weights and synthetic memory probes; no trained genomic model",
        "parity": parity(),
        "states": y.detach().tolist(),
        "streaming_max_error": float(
            (torch.cat((y1, y2), 1) - y).abs().max().detach()
        ),
        "chunks": {
            "full": chunk_experiment(),
            "detach": chunk_experiment(detach=True),
            "reset": chunk_experiment(reset=True),
        },
        "retention": [
            {"z": z, "steps": n, **scalar_retention(z, n)}
            for z in (0.5, 0.9, 0.99)
            for n in (1, 5, 10, 50, 100)
        ],
        "half_lives": [
            {"z": z, "steps": math.log(0.5) / math.log(z)}
            for z in (0.5, 0.9, 0.99)
        ],
        "parameter_counts": [
            {
                "cell": name,
                "gates": g,
                "parameters_D4_H8": g * (8 * 4 + 8 * 8 + 2 * 8),
            }
            for name, g in (("RNN", 1), ("GRU", 3), ("LSTM", 4))
        ],
    }


if __name__ == "__main__":
    torch.set_num_threads(1)
    print(json.dumps(results(), indent=2))
