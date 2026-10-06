"""EVOD-27: weighted reduction, recomputation and update oracles; CPU reference only."""

import copy
import json
import math
import torch


class Tiny(torch.nn.Module):
    def __init__(self, d=8, hidden=16, outputs=3):
        super().__init__()
        self.l1 = torch.nn.Linear(d, hidden, dtype=torch.float64)
        self.l2 = torch.nn.Linear(hidden, outputs, dtype=torch.float64)

    def forward(self, x):
        return self.l2(torch.tanh(self.l1(x)))


def make_model(seed=27, outputs=3):
    """Seed only the local CPU initialization context; restore caller RNG."""
    with torch.random.fork_rng(devices=[]):
        torch.random.default_generator.manual_seed(seed)
        return Tiny(outputs=outputs)


def data(n=12, d=8, outputs=3):
    generator = torch.Generator().manual_seed(27)
    x = torch.randn(n, d, generator=generator, dtype=torch.float64)
    y = torch.randn(n, outputs, generator=generator, dtype=torch.float64)
    weights = torch.ones_like(y)
    # Different valid-element mass across records and microbatches.
    if n > 2 and outputs > 1:
        weights[::3, 1:] = 0
        weights[1::4, 0] = 2
    return x, y, weights


def validate_batch(x, y, weights):
    if not all(isinstance(t, torch.Tensor) for t in (x, y, weights)):
        raise ValueError("Tensor batch required")
    if x.ndim != 2 or y.ndim != 2 or len(x) == 0 or len(x) != len(y):
        raise ValueError(
            "Nonempty matching record axis and explicit feature/output axes required"
        )
    if weights.shape != y.shape or weights.requires_grad:
        raise ValueError("Fixed weights must match target shape exactly")
    if not all(
        t.is_floating_point() and torch.isfinite(t).all() for t in (x, y, weights)
    ):
        raise ValueError("Finite floating data and weights required")
    if (
        len({t.dtype for t in (x, y, weights)}) != 1
        or len({t.device for t in (x, y, weights)}) != 1
    ):
        raise ValueError("Matching dtype and device required")
    denominator = weights.sum()
    if (weights < 0).any() or not torch.isfinite(denominator) or denominator <= 0:
        raise ValueError("Nonnegative weights with finite positive total mass required")
    return denominator


def weighted_sum(prediction, target, weights):
    """No broadcasting: numerator is sum of weighted squared output errors."""
    if prediction.shape != target.shape or weights.shape != target.shape:
        raise ValueError("Prediction/target/weight shapes must match exactly")
    return ((prediction - target).square() * weights).sum()


def grads(model):
    if any(
        p.grad is None or not torch.isfinite(p.grad).all() for p in model.parameters()
    ):
        raise ValueError("Missing or non-finite reference gradients")
    return tuple(p.grad.detach().clone() for p in model.parameters())


def full_grad(model, x, y, weights):
    denominator = validate_batch(x, y, weights)
    model.zero_grad(set_to_none=True)
    loss = weighted_sum(model(x), y, weights) / denominator
    loss.backward()
    return loss.item(), grads(model)


def accumulated_grad(model, x, y, weights, micro):
    """Each numerator uses the same global valid-weight denominator."""
    denominator = validate_batch(x, y, weights)
    if type(micro) is not int or micro < 1:
        raise ValueError("Positive integer microbatch size required")
    model.zero_grad(set_to_none=True)
    total = 0.0
    for start in range(0, len(x), micro):
        end = start + micro
        loss = (
            weighted_sum(model(x[start:end]), y[start:end], weights[start:end])
            / denominator
        )
        total += loss.item()
        loss.backward()
    return total, grads(model)


def checkpoint_grad(model, x, y, weights, dropout=0.0, preserve_rng=True):
    """Non-reentrant recomputation with explicit CPU stochastic-state policy."""
    from torch.utils.checkpoint import checkpoint

    denominator = validate_batch(x, y, weights)
    if (
        type(preserve_rng) is not bool
        or type(dropout) not in (int, float)
        or not 0 <= dropout < 1
    ):
        raise ValueError("Boolean RNG policy and dropout in [0,1) required")
    model.zero_grad(set_to_none=True)

    def block(z):
        hidden = torch.tanh(model.l1(z))
        return torch.nn.functional.dropout(hidden, p=dropout, training=True)

    hidden = checkpoint(block, x, use_reentrant=False, preserve_rng_state=preserve_rng)
    loss = weighted_sum(model.l2(hidden), y, weights) / denominator
    loss.backward()
    return loss.item(), grads(model)


def ordinary_dropout_grad(model, x, y, weights, dropout):
    denominator = validate_batch(x, y, weights)
    model.zero_grad(set_to_none=True)
    hidden = torch.nn.functional.dropout(
        torch.tanh(model.l1(x)), p=dropout, training=True
    )
    loss = weighted_sum(model.l2(hidden), y, weights) / denominator
    loss.backward()
    return loss.item(), grads(model)


def adam_step(
    theta, gradient, m, v, step, lr=0.01, beta1=0.9, beta2=0.999, epsilon=1e-8
):
    """Out-of-place scalar/vector Adam oracle, no weight decay or AMSGrad."""
    values = (theta, gradient, m, v)
    if not all(
        isinstance(t, torch.Tensor)
        and t.is_floating_point()
        and torch.isfinite(t).all()
        for t in values
    ):
        raise ValueError("Finite floating optimizer tensors required")
    if (
        len({t.shape for t in values}) != 1
        or len({t.dtype for t in values}) != 1
        or len({t.device for t in values}) != 1
    ):
        raise ValueError("Matching optimizer tensor shape/dtype/device required")
    if (v < 0).any() or type(step) is not int or step < 1:
        raise ValueError(
            "Nonnegative second moment and positive integer update clock required"
        )
    for value in (lr, beta1, beta2, epsilon):
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError("Finite optimizer hyperparameters required")
    if lr < 0 or epsilon <= 0 or not 0 <= beta1 < 1 or not 0 <= beta2 < 1:
        raise ValueError("Invalid Adam hyperparameter domain")
    next_m = beta1 * m + (1 - beta1) * gradient
    next_v = beta2 * v + (1 - beta2) * gradient.square()
    corrected_m = next_m / (1 - beta1**step)
    corrected_v = next_v / (1 - beta2**step)
    next_theta = theta - lr * corrected_m / (corrected_v.sqrt() + epsilon)
    if not all(torch.isfinite(t).all() for t in (next_theta, next_m, next_v)):
        raise ValueError("Non-finite optimizer result")
    return next_theta, next_m, next_v


def adam_bytes(num_params, param_bytes=4, grad_bytes=4, moment_bytes=4, master_bytes=0):
    """Static persistent-array accounting, not peak-memory measurement."""
    if type(num_params) is not int or num_params < 0:
        raise ValueError("Nonnegative integer parameter count required")
    for value in (param_bytes, grad_bytes, moment_bytes, master_bytes):
        if type(value) is not int or value < 0:
            raise ValueError("Nonnegative integer storage widths required")
    return num_params * (param_bytes + grad_bytes + 2 * moment_bytes + master_bytes)


def chain_checkpoint_inventory(layers, block):
    """Equal-size chain toy: boundary plus one recomputed block activation slots."""
    if type(layers) is not int or type(block) is not int or layers < 1 or block < 1:
        raise ValueError("Positive integer chain and block lengths required")
    boundaries = math.ceil(layers / block)
    return {
        "layers": layers,
        "block": block,
        "boundary_slots": boundaries,
        "recompute_slots": min(block, layers),
        "toy_live_slots": boundaries + min(block, layers),
    }


def parity():
    model = make_model()
    x, y, weights = data()
    loss, gf = full_grad(model, x, y, weights)
    rows = []
    for micro in (1, 2, 5, 12, 20):
        la, ga = accumulated_grad(model, x, y, weights, micro)
        rows.append(
            {
                "micro": micro,
                "loss": la,
                "gradient_error": max(
                    (a - b).abs().max().item() for a, b in zip(gf, ga)
                ),
            }
        )
    lc, gc = checkpoint_grad(model, x, y, weights)
    mass = weights.sum().item()
    model.zero_grad(set_to_none=True)
    local = [(0, 5), (5, 10), (10, 12)]
    for start, end in local:
        ww = weights[start:end]
        (
            weighted_sum(model(x[start:end]), y[start:end], ww) / ww.sum() / len(local)
        ).backward()
    bad = grads(model)
    with torch.random.fork_rng(devices=[]):
        torch.random.default_generator.manual_seed(271)
        plain, gp = ordinary_dropout_grad(model, x, y, weights, 0.4)
        torch.random.default_generator.manual_seed(271)
        replay, gr = checkpoint_grad(model, x, y, weights, 0.4, True)
        torch.random.default_generator.manual_seed(271)
        no_replay, gn = checkpoint_grad(model, x, y, weights, 0.4, False)
    parameters = sum(p.numel() for p in model.parameters())
    return {
        "loss": loss,
        "valid_weight_mass": mass,
        "microbatches": rows,
        "checkpoint_loss": lc,
        "checkpoint_gradient_error": max(
            (a - b).abs().max().item() for a, b in zip(gf, gc)
        ),
        "wrong_local_mean_gradient_error": max(
            (a - b).abs().max().item() for a, b in zip(gf, bad)
        ),
        "dropout_forward_equal": plain == replay == no_replay,
        "dropout_replay_gradient_error": max(
            (a - b).abs().max().item() for a, b in zip(gp, gr)
        ),
        "dropout_no_replay_gradient_error": max(
            (a - b).abs().max().item() for a, b in zip(gp, gn)
        ),
        "parameters": parameters,
        "adam_fp32_static_bytes": adam_bytes(parameters),
        "torch_version": torch.__version__,
        "chain": [chain_checkpoint_inventory(64, k) for k in (1, 4, 8, 16, 64)],
        "scope": "CPU float64 semantic probes and static toy inventories; no accelerator memory/speed or mixed-precision certification",
    }


def update_probe(micro):
    model = make_model()
    x, y, w = data()
    _, gradient = (
        full_grad(model, x, y, w)
        if micro is None
        else accumulated_grad(model, x, y, w, micro)
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, eps=1e-8)
    optimizer.step()
    return (
        copy.deepcopy(model.state_dict()),
        tuple(
            (s["exp_avg"].clone(), s["exp_avg_sq"].clone())
            for s in optimizer.state.values()
        ),
        gradient,
    )


def results():
    return parity()


TABLES = [
    (
        "microbatches",
        ["Micro", "Weighted loss", "Gradient error"],
        ["micro", "loss", "gradient_error"],
        "rrr",
    ),
    (
        "chain",
        ["Block", "Boundaries", "Recompute", "Toy live slots"],
        ["block", "boundary_slots", "recompute_slots", "toy_live_slots"],
        "rrrr",
    ),
]
PLOTS = []
LISTINGS = [
    "weighted_sum",
    "accumulated_grad",
    "checkpoint_grad",
    "adam_step",
    "chain_checkpoint_inventory",
]

if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
