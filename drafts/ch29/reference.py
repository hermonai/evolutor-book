"""EVOD-29: exact statistical teaching fixtures, not trained-model rankings."""

from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
import json
import math
import random
import statistics

LISTINGS = [
    "paired_deltas",
    "exact_bootstrap",
    "crossed_bootstrap",
    "within_budget",
    "intervention",
]
TABLES = [
    (
        "paired-table",
        ["Case", "A correct", "B correct", "$d_i$"],
        ["case", "a", "b", "d"],
        "lrrr",
    ),
    (
        "group-table",
        ["Seed fixture", "G1", "G2", "G3", "G4", "Mean"],
        ["seed", "g1", "g2", "g3", "g4", "mean"],
        "lrrrrr",
    ),
    (
        "mechanism-table",
        ["Setting", "Accuracy", "Gain vs off"],
        ["setting", "accuracy", "gain"],
        "lrr",
    ),
    (
        "lottery-table",
        ["Task selection", "A mean", "B mean", "Winner"],
        ["selection", "a", "b", "winner"],
        "lrrl",
    ),
]
PLOTS = []


def integer(x, name, minimum=0):
    if type(x) is not int or x < minimum:
        raise ValueError(f"{name}: exact integer >= {minimum} required")
    return x


def finite_values(values, *, lower=None, upper=None):
    if not values:
        raise ValueError("nonempty values required")
    for v in values:
        if (
            isinstance(v, bool)
            or not isinstance(v, (int, float))
            or not math.isfinite(v)
        ):
            raise ValueError("finite numbers required")
        if lower is not None and v < lower or upper is not None and v > upper:
            raise ValueError("values outside declared range")
    return values


def binary(values):
    if not values or any(type(v) is not int or v not in (0, 1) for v in values):
        raise ValueError("nonempty exact binary integers required")


def accuracy(y, pred):
    binary(y)
    binary(pred)
    if len(y) != len(pred):
        raise ValueError("equal lengths required")
    return sum(a == b for a, b in zip(y, pred)) / len(y)


def paired_deltas(y, pred_a, pred_b):
    """Same held-out cases; correctness A minus B, not independent samples."""
    binary(y)
    binary(pred_a)
    binary(pred_b)
    if not len(y) == len(pred_a) == len(pred_b):
        raise ValueError("paired equal-length arrays required")
    return [int(a == pa) - int(a == pb) for a, pa, pb in zip(y, pred_a, pred_b)]


def deltas_ok(deltas):
    if not deltas or any(type(x) is not int or x not in (-1, 0, 1) for x in deltas):
        raise ValueError("nonempty exact correctness differences required")


def alpha_ok(alpha):
    finite_values([alpha])
    if not 0 < alpha < 1:
        raise ValueError("alpha in (0,1) required")


def percentile(values, q):
    """Inverse empirical CDF: first value at cumulative probability >=q."""
    finite_values(values)
    finite_values([q], lower=0, upper=1)
    values = sorted(values)
    return values[max(0, math.ceil(q * len(values)) - 1)]


def exact_bootstrap(deltas, alpha=0.05):
    """Exact n-out-of-n IID paired percentile law via convolution."""
    deltas_ok(deltas)
    alpha_ok(alpha)
    n = len(deltas)
    if n > 100:
        raise ValueError("teaching convolution limited to n<=100")
    category = {v: Fraction(deltas.count(v), n) for v in set(deltas)}
    law = {0: Fraction(1)}
    for _ in range(n):
        nxt = {}
        for total, mass in law.items():
            for value, p in category.items():
                nxt[total + value] = nxt.get(total + value, Fraction(0)) + mass * p
        law = nxt

    def quantile(q):
        cumulative = Fraction(0)
        for total, mass in sorted(law.items()):
            cumulative += mass
            if cumulative >= Fraction(str(q)):
                return total / n
        return max(law) / n

    return {
        "mean": sum(deltas) / n,
        "interval": [quantile(alpha / 2), quantile(1 - alpha / 2)],
        "law": [{"sum": s, "mass": float(p)} for s, p in sorted(law.items())],
    }


def paired_bootstrap_ci(deltas, draws=4000, seed=29, alpha=0.05):
    deltas_ok(deltas)
    integer(draws, "draws", 1)
    integer(seed, "seed")
    alpha_ok(alpha)
    rng = random.Random(seed)
    n = len(deltas)
    means = [sum(deltas[rng.randrange(n)] for _ in range(n)) / n for _ in range(draws)]
    return percentile(means, alpha / 2), percentile(means, 1 - alpha / 2)


def exact_paired_sign_test(deltas):
    deltas_ok(deltas)
    plus, minus = deltas.count(1), deltas.count(-1)
    n = plus + minus
    if n == 0:
        return 1.0
    return min(
        1.0, 2 * sum(math.comb(n, i) for i in range(min(plus, minus) + 1)) / 2**n
    )


def seed_summary(values):
    finite_values(values, lower=0, upper=1)
    if len(values) < 2:
        raise ValueError("two or more prespecified trials required")
    return {
        "n": len(values),
        "values": list(values),
        "mean": statistics.mean(values),
        "stdev": statistics.stdev(values),
        "min": min(values),
        "max": max(values),
    }


def matrix_ok(matrix):
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("nonempty rectangular seed-by-group matrix required")
    for row in matrix:
        finite_values(row, lower=-1, upper=1)


def crossed_bootstrap(matrix, draws=4000, seed=29, alpha=0.05):
    """Equal seed/group estimand; resample both shared axes, not pooled cells."""
    matrix_ok(matrix)
    integer(draws, "draws", 1)
    integer(seed, "seed")
    alpha_ok(alpha)
    ns, ng = len(matrix), len(matrix[0])
    rng = random.Random(seed)
    means = []
    for _ in range(draws):
        rows = [rng.randrange(ns) for _ in range(ns)]
        cols = [rng.randrange(ng) for _ in range(ng)]
        # Shared group draw across seed rows preserves the crossed design.
        means.append(sum(matrix[s][g] for s in rows for g in cols) / (ns * ng))
    return {
        "mean": sum(map(sum, matrix)) / (ns * ng),
        "interval": [percentile(means, alpha / 2), percentile(means, 1 - alpha / 2)],
        "draws": draws,
        "seed": seed,
        "estimand": "equal-seed equal-group mean",
    }


@dataclass(frozen=True)
class Budget:
    params: int
    train_tokens: int
    forward_steps: int
    peak_bytes: int
    persistent_state_bytes: int
    inference_work: int

    def __post_init__(self):
        for name in self.__dataclass_fields__:
            integer(getattr(self, name), name)


def within_budget(candidate, ceiling):
    """All controlled dimensions pass; missing measurements are not zeros."""
    if not isinstance(candidate, Budget) or not isinstance(ceiling, Budget):
        raise ValueError("complete measured budget vectors required")
    return all(
        getattr(candidate, k) <= getattr(ceiling, k)
        for k in Budget.__dataclass_fields__
    )


def pareto_dominates(a_score, a, b_score, b):
    finite_values([a_score, b_score], lower=0, upper=1)
    if not isinstance(a, Budget) or not isinstance(b, Budget):
        raise ValueError("budget vectors required")
    weak = a_score >= b_score and within_budget(a, b)
    strict = a_score > b_score or any(
        getattr(a, k) < getattr(b, k) for k in Budget.__dataclass_fields__
    )
    return weak and strict


def capacity_match(candidates, target_params):
    integer(target_params, "target_params")
    if not candidates:
        raise ValueError("nonempty candidate set required")
    for c in candidates:
        if (
            set(c) != {"name", "params"}
            or not isinstance(c["name"], str)
            or not c["name"]
        ):
            raise ValueError("name/params schema required")
        integer(c["params"], "params")
    return min(
        candidates,
        key=lambda c: (abs(c["params"] - target_params), c["params"], c["name"]),
    )


def dna(seq):
    if not isinstance(seq, str) or not seq or any(c not in "ACGT" for c in seq):
        raise ValueError("nonempty ACGT sequence required")


def motif_oracle(seq):
    dna(seq)
    return int("ACG" in seq)


def detector(seq, motif):
    dna(seq)
    if motif not in ("ACG", "ACT"):
        raise ValueError("declared motif detector required")
    # Both target and sham execute the same full window/character loops.
    found = False
    for start in range(max(0, len(seq) - 2)):
        matched = True
        for j in range(3):
            matched = (seq[start + j] == motif[j]) and matched
        found = found or matched
    return int(found)


def base_model(seq):
    dna(seq)
    return int(2 * (seq.count("C") + seq.count("G")) >= len(seq))


def intervention(seq, mode):
    """No trainable parameters; source/recipient/sham toy Boolean program."""
    if mode not in ("off", "target", "sham"):
        raise ValueError("declared intervention mode required")
    base = base_model(seq)
    if mode == "off":
        return base
    return max(base, detector(seq, "ACG" if mode == "target" else "ACT"))


def results():
    y = [1, 0, 1, 0, 1, 0, 1, 0]
    a = [1, 0, 1, 0, 1, 1, 1, 0]
    b = [1, 1, 0, 0, 1, 0, 0, 0]
    d = paired_deltas(y, a, b)
    matrix = [[1, 1, 0, 0], [0, 0, -1, -1], [1, 1, 0, 0]]
    records = ["ACGTT", "TTTTT", "AACGA", "AAAAA", "GGACG", "GCGCG", "TACGT", "CCCCC"]
    labels = [motif_oracle(s) for s in records]
    rows = []
    off = accuracy(labels, [intervention(s, "off") for s in records])
    for mode in ("off", "target", "sham"):
        score = accuracy(labels, [intervention(s, mode) for s in records])
        rows.append({"setting": mode, "accuracy": score, "gain": score - off})
    return {
        "paired": {
            "A": accuracy(y, a),
            "B": accuracy(y, b),
            "deltas": d,
            "exact": exact_bootstrap(d),
            "monte_carlo": paired_bootstrap_ci(d),
            "sign_test_p": exact_paired_sign_test(d),
        },
        "paired-table": [
            {"case": str(i + 1), "a": int(pa == t), "b": int(pb == t), "d": di}
            for i, (t, pa, pb, di) in enumerate(zip(y, a, b, d))
        ],
        "group-table": [
            dict(
                seed=f"Fixture {i + 1}",
                g1=row[0],
                g2=row[1],
                g3=row[2],
                g4=row[3],
                mean=statistics.mean(row),
            )
            for i, row in enumerate(matrix)
        ],
        "crossed": crossed_bootstrap(matrix),
        "seed_only": crossed_bootstrap([[statistics.mean(row)] for row in matrix]),
        "group_only": crossed_bootstrap([[statistics.mean(c) for c in zip(*matrix)]]),
        "seeds": seed_summary([0.71, 0.74, 0.69, 0.73, 0.72]),
        "mechanism-table": rows,
        "gc_matched_pair": {
            "positive": "ACGTT",
            "negative": "ACTGT",
            "gc_count": 2,
            "target_outputs": [intervention(s, "target") for s in ("ACGTT", "ACTGT")],
            "sham_outputs": [intervention(s, "sham") for s in ("ACGTT", "ACTGT")],
        },
        "lottery-table": [
            {"selection": "Task 1 only", "a": 0.9, "b": 0.8, "winner": "A"},
            {
                "selection": "Both tasks, equal weight",
                "a": 0.7,
                "b": 0.8,
                "winner": "B",
            },
        ],
        "budget_counterexample": {
            "feasible": within_budget(
                Budget(10, 10, 10, 10, 10, 11), Budget(100, 100, 100, 100, 100, 10)
            )
        },
        "capacity": capacity_match(
            [{"name": "x", "params": 90}, {"name": "y", "params": 105}], 100
        ),
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
