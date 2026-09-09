"""Fixed CPU float64 tensor/derivative diagnostics; no trained-model claim."""
import json
import math
import torch
from torch.nn import functional as F


def fixture():
    tensor = lambda x: torch.tensor(x, dtype=torch.float64)
    x = tensor([[1, 0], [0, 1], [1, -1]])
    y = torch.tensor([0, 2, 1], dtype=torch.long)
    parameters = (tensor([[.2, -.1], [.4, .3]]), tensor([.05, -.02]),
                  tensor([[.3, -.2, .1], [-.4, .2, .5]]), tensor([.01, -.03, .02]))
    return x, y, parameters


def validate(x, y, parameters):
    if len(parameters) != 4:
        raise ValueError("expected W,b,U,c")
    w, b, u, c = parameters
    arrays = (x, w, b, u, c)
    if any(t.dtype != torch.float64 or t.device.type != "cpu" or not torch.isfinite(t).all() for t in arrays):
        raise ValueError("finite CPU float64 reference tensors required")
    if x.ndim != 2 or x.shape[0] < 1 or x.shape[1] < 1 or w.ndim != 2 or w.shape[1] < 1:
        raise ValueError("nonempty X[B,D], W[D,H] required")
    if (w.shape[0] != x.shape[1] or b.shape != (w.shape[1],) or u.ndim != 2
            or u.shape[0] != w.shape[1] or u.shape[1] < 2 or c.shape != (u.shape[1],)):
        raise ValueError("incompatible W,b,U,c shapes")
    if (y.shape != (x.shape[0],) or y.dtype != torch.long or y.device.type != "cpu"
            or y.min() < 0 or y.max() >= u.shape[1]):
        raise ValueError("one valid class index per row required")


def objective(x, y, parameters):
    validate(x, y, parameters)
    w, b, u, c = parameters
    hidden = torch.tanh(x @ w + b)
    logits = hidden @ u + c
    return F.cross_entropy(logits, y)


def manual_gradients(x, y, parameters):
    """Closed-form reverse pass, independent of torch.autograd."""
    validate(x, y, parameters)
    w, b, u, c = parameters
    with torch.no_grad():
        hidden = torch.tanh(x @ w + b)
        logits = hidden @ u + c
        probabilities = torch.softmax(logits, dim=1)
        error = (probabilities - F.one_hot(y, u.shape[1])) / x.shape[0]
        du = hidden.T @ error
        dc = error.sum(0)
        dh = error @ u.T
        da = dh * (1 - hidden.square())
        dw = x.T @ da
        db = da.sum(0)
    return dw, db, du, dc


def autodiff_gradients(x, y, parameters):
    leaves = tuple(t.detach().clone().requires_grad_() for t in parameters)
    return tuple(g.detach() for g in torch.autograd.grad(objective(x, y, leaves), leaves))


def finite_difference_gradients(x, y, parameters, h=1e-5):
    validate(x, y, parameters)
    if not math.isfinite(h) or h <= 0:
        raise ValueError("finite positive perturbation required")
    gradients = []
    with torch.no_grad():
        for which, parameter in enumerate(parameters):
            result = torch.empty(parameter.shape, dtype=torch.float64)
            for index in range(parameter.numel()):
                plus = [t.detach().clone().contiguous() for t in parameters]
                minus = [t.detach().clone().contiguous() for t in parameters]
                plus[which].view(-1)[index] += h
                minus[which].view(-1)[index] -= h
                if torch.equal(plus[which], minus[which]):
                    raise ValueError("perturbation vanished at this scale")
                result.view(-1)[index] = (objective(x, y, plus) - objective(x, y, minus)) / (2 * h)
            gradients.append(result)
    return tuple(gradients)


def maximum_error(a, b):
    if len(a) != len(b) or not a or any(x.shape != y.shape for x, y in zip(a, b)):
        raise ValueError("matching nonempty gradient collections required")
    if any(not torch.isfinite(t).all() for t in (*a, *b)):
        raise ValueError("nonfinite gradient cannot pass comparison")
    return max(float((x - y).abs().max()) for x, y in zip(a, b))


def detached_negative_control():
    x = torch.tensor(2., dtype=torch.float64, requires_grad=True)
    def wrong_graph(value):
        return value * value.detach()
    wrong_gradient = float(torch.autograd.grad(wrong_graph(x), x)[0])
    h = 1e-5
    with torch.no_grad():
        numeric = float((wrong_graph(x + h) - wrong_graph(x - h)) / (2 * h))
    return {"input": 2., "forward_value": float(wrong_graph(x).detach()),
            "autograd_derivative": wrong_gradient, "finite_difference": numeric,
            "mathematical_derivative_of_forward_values": 4.}


def quadratic_trace(curvature, eta, initial=1., steps=6):
    if (not all(math.isfinite(v) for v in (curvature, eta, initial))
            or curvature <= 0 or eta < 0 or type(steps) is not int or steps < 0):
        raise ValueError("positive curvature, nonnegative rate and step count required")
    x = initial
    trace = []
    for k in range(steps + 1):
        trace.append({"step": k, "x": x, "loss": .5 * curvature * x * x})
        x *= 1 - eta * curvature
    return trace


def stable_nll(logits, targets):
    if (logits.ndim != 2 or logits.shape[0] < 1 or logits.shape[1] < 2
            or not logits.is_floating_point() or not torch.isfinite(logits).all()
            or targets.shape != (logits.shape[0],) or targets.dtype != torch.long
            or targets.device != logits.device or targets.min() < 0 or targets.max() >= logits.shape[1]):
        raise ValueError("finite logits [B,V] and valid integer targets required")
    shifted = logits - logits.max(dim=1, keepdim=True).values
    chosen = shifted.gather(1, targets[:, None]).squeeze(1)
    return (shifted.exp().sum(1).log() - chosen).mean()


def cancellation_example():
    # Original scalar example chosen to expose dtype dependence exactly.
    values = {}
    for dtype in (torch.float32, torch.float64):
        x = torch.tensor(100_000_000., dtype=dtype)
        values[str(dtype)] = float((x + 1) - x)
    return values


def results():
    x, y, parameters = fixture()
    manual = manual_gradients(x, y, parameters)
    automatic = autodiff_gradients(x, y, parameters)
    finite = finite_difference_gradients(x, y, parameters)
    leaves = tuple(t.clone().requires_grad_() for t in parameters)
    checked = torch.autograd.gradcheck(lambda *p: objective(x, y, p), leaves,
                                       eps=1e-6, atol=1e-5, rtol=1e-3)
    eta = .1  # Fixed demonstration step, not selected by a sweep.
    updated = tuple(p - eta * g for p, g in zip(parameters, manual))
    extreme = torch.tensor([[1000., 1001., 999.]], dtype=torch.float64)
    target = torch.tensor([1])
    return {"scope": "Fixed CPU derivative diagnostics and one declared toy update; no trained architecture",
            "torch_version": torch.__version__, "shapes": {k: list(v.shape) for k, v in
                zip(("X", "y", "W", "b", "U", "c"), (x, y, *parameters))},
            "loss": float(objective(x, y, parameters)), "manual_gradients": [g.tolist() for g in manual],
            "manual_autograd_max_abs": maximum_error(manual, automatic),
            "manual_finite_difference_max_abs": maximum_error(manual, finite),
            "gradcheck": checked, "negative_control": detached_negative_control(),
            "fixed_step": {"eta": eta, "loss_after": float(objective(x, y, updated))},
            "step_size_scan": [{"h": h, "max_abs_error": maximum_error(manual,
                finite_difference_gradients(x, y, parameters, h))} for h in (1e-1, 1e-3, 1e-5, 1e-7, 1e-9)],
            "quadratic": {str(eta): quadratic_trace(4., eta) for eta in (.1, .5, .6)},
            "extreme_logits": {"naive_exp_finite": bool(torch.isfinite(extreme.exp()).all()),
                "stable_nll": float(stable_nll(extreme, target)),
                "torch_nll": float(F.cross_entropy(extreme, target))},
            "cancellation": cancellation_example()}


if __name__ == "__main__":
    print(json.dumps(results(), indent=2, allow_nan=False))
