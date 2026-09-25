"""Exact interventions and credit in declared synthetic mechanisms."""

from itertools import permutations
import json
import math

LISTINGS = ["evaluate", "shapley", "memory"]
TABLES = [
    ("interventions", ["Intervention", "Output"], ["name", "y"], "lr"),
    (
        "credit",
        ["Game", "A credit", "B credit", "Joint value"],
        ["game", "a", "b", "total"],
        "lrrr",
    ),
    (
        "memory",
        ["Time", "Baseline", "Patched", "Difference"],
        ["time", "base", "patched", "difference"],
        "rrrr",
    ),
]
PLOTS = [("memory-plot", "memory", "time", ["base", "patched"])]


def evaluate(u, interventions=None):
    """Surgically replace selected equations, then recompute all descendants."""
    intervention = dict(interventions or {})
    if set(intervention) - {"a", "b", "z", "y"}:
        raise ValueError("unknown intervention target")
    if any(not math.isfinite(v) for v in [u, *intervention.values()]):
        raise ValueError("finite values required")
    values = {}
    for name, compute in (
        ("a", lambda: 2 * u),
        ("b", lambda: u),
        ("z", lambda: u),  # logged bystander; not a parent of y
        ("y", lambda: values["a"] + 3 * values["b"]),
    ):
        values[name] = (
            intervention[name] if name in intervention else compute()
        )
    return values


def shapley(players, value):
    """Exact permutation average; exponential/factorial teaching scope."""
    if not players or len(set(players)) != len(players):
        raise ValueError("nonempty unique players required")
    credit = dict.fromkeys(players, 0.0)
    count = 0
    for order in permutations(players):
        coalition = frozenset()
        before = value(coalition)
        for player in order:
            coalition = coalition | {player}
            after = value(coalition)
            credit[player] += after - before
            before = after
        count += 1
    return {p: c / count for p, c in credit.items()}


def memory(inputs, retention=0.5, patch=None):
    """Patch one input by (zero-based time, replacement), then rerun."""
    xs = tuple(inputs)
    if not math.isfinite(retention) or not 0 <= retention <= 1:
        raise ValueError("retention in [0,1] required")
    if any(not math.isfinite(x) for x in xs):
        raise ValueError("finite inputs required")
    if patch is not None:
        k, replacement = patch
        if (
            type(k) is not int
            or not 0 <= k < len(xs)
            or not math.isfinite(replacement)
        ):
            raise ValueError("valid patch time and finite value required")
    h, states = 0.0, []
    for t, x in enumerate(xs):
        x = patch[1] if patch is not None and t == patch[0] else x
        h = retention * h + x
        states.append(h)
    return states


def results():
    games = {
        "redundant": lambda s: float(bool(s)),
        "synergistic": lambda s: float(len(s) == 2),
        "additive": lambda s: 2 * ("a" in s) + 3 * ("b" in s),
    }
    base, patched = memory([1, 1, 1, 1]), memory([1, 1, 1, 1], patch=(1, 0))
    return {
        "interventions": [
            dict(name=name, y=evaluate(1, patch)["y"])
            for name, patch in [
                ("none", {}),
                ("do(a=0)", {"a": 0}),
                ("do(b=0)", {"b": 0}),
                ("do(z=0)", {"z": 0}),
            ]
        ],
        "credit": [
            dict(
                game=name,
                a=shapley(("a", "b"), v)["a"],
                b=shapley(("a", "b"), v)["b"],
                total=v({"a", "b"}) - v(set()),
            )
            for name, v in games.items()
        ],
        "memory": [
            dict(time=t + 1, base=a, patched=b, difference=a - b)
            for t, (a, b) in enumerate(zip(base, patched))
        ],
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
