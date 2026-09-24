"""Deterministic structural search with equal per-candidate training budgets."""

import math
from itertools import product
import numpy as np

LISTINGS = ["fit", "select", "evolve", "inherit"]
TRAIN_X = np.array([[-1.0, -1.0], [1.0, 1.0]])
TRAIN_Y = 2 * TRAIN_X[:, 0]
VALID_X = np.array(list(product((-1.0, 1.0), repeat=2)))
VALID_Y = 2 * VALID_X[:, 0]


def checked(mask, x, y):
    mask = tuple(mask)
    if not mask or any(type(v) is not int or v not in (0, 1) for v in mask):
        raise ValueError("binary feature mask required")
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim != 2 or x.shape[1] != len(mask) or x.shape[0] == 0:
        raise ValueError("nonempty sample-by-feature matrix required")
    if (
        y.shape != (x.shape[0],)
        or not np.isfinite(x).all()
        or not np.isfinite(y).all()
    ):
        raise ValueError("finite aligned target required")
    return np.array(mask, dtype=float), x, y


def fit(mask, x, y, steps=40, rate=0.1):
    """Every candidate starts with zero weights and identical step count."""
    m, x, y = checked(mask, x, y)
    if (
        type(steps) is not int
        or steps < 0
        or not math.isfinite(rate)
        or rate <= 0
    ):
        raise ValueError("valid step budget and positive rate required")
    w = np.zeros(len(m))
    for _ in range(steps):
        residual = x @ (m * w) - y
        gradient = 2 * m * (x.T @ residual) / len(y)
        w -= rate * gradient
    return w


def mse(mask, w, x, y):
    m, x, y = checked(mask, x, y)
    w = np.asarray(w, dtype=float)
    if w.shape != m.shape or not np.isfinite(w).all():
        raise ValueError("finite aligned weights required")
    return float(np.mean((x @ (m * w) - y) ** 2))


def select(candidates, xtrain, ytrain, xvalid, yvalid, penalty=0.05):
    if not math.isfinite(penalty) or penalty < 0 or not candidates:
        raise ValueError("candidates and nonnegative penalty required")
    rows = []
    for mask in sorted(set(candidates)):
        w = fit(mask, xtrain, ytrain)
        loss = mse(mask, w, xvalid, yvalid)
        rows.append(
            dict(
                mask=list(mask),
                weights=w.tolist(),
                train=mse(mask, w, xtrain, ytrain),
                valid=loss,
                score=loss + penalty * sum(mask),
            )
        )
    # Stable lexical tie break, not arrival order.
    return min(rows, key=lambda r: (r["score"], r["mask"])), rows


def evolve(rounds=2):
    """(1+lambda) elitist mask search; weights are never inherited."""
    if type(rounds) is not int or rounds < 0:
        raise ValueError("nonnegative rounds required")
    parent = (0, 1)
    history = []
    for generation in range(rounds + 1):
        candidates = [parent]
        if generation:
            candidates += [
                tuple(1 - v if j == i else v for j, v in enumerate(parent))
                for i in range(len(parent))
            ]
        best, rows = select(candidates, TRAIN_X, TRAIN_Y, VALID_X, VALID_Y)
        history.append(
            dict(
                generation=generation,
                parent=list(parent),
                candidates=rows,
                winner=best["mask"],
                score=best["score"],
            )
        )
        parent = tuple(best["mask"])
    return history


def inherit(old_mask, new_mask, weights):
    """Explicit alternative policy: retain only shared active coordinates."""
    if len(old_mask) != len(new_mask) or len(weights) != len(old_mask):
        raise ValueError("stable coordinate map required")
    if any(
        type(v) is not int or v not in (0, 1)
        for v in (*old_mask, *new_mask)
    ):
        raise ValueError("binary masks required")
    if not np.isfinite(weights).all():
        raise ValueError("finite weights required")
    return np.array(
        [
            w if old and new else 0.0
            for old, new, w in zip(old_mask, new_mask, weights)
        ]
    )


def false_positive(searches, alpha=0.05):
    if type(searches) is not int or searches < 0 or not 0 <= alpha <= 1:
        raise ValueError(
            "nonnegative searches and valid probability required"
        )
    return 1 - (1 - alpha) ** searches


def results():
    _, rows = select(
        list(product((0, 1), repeat=2)), TRAIN_X, TRAIN_Y, VALID_X, VALID_Y
    )
    return dict(
        candidates=rows,
        history=evolve(),
        multiplicity_curve=[
            dict(searches=k, probability=false_positive(k))
            for k in range(101)
        ],
        multiplicity=[
            dict(searches=k, probability=false_positive(k))
            for k in (1, 2, 5, 10, 20, 50, 100)
        ],
        inherited=inherit((1, 0), (1, 1), [2.0, 9.0]).tolist(),
    )
