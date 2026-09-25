from pathlib import Path
import importlib.util
import json
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evolutor_book_ch17", ROOT / "drafts/ch17/reference.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_results_are_reproducible():
    assert m.results() == json.loads(
        (ROOT / "drafts/ch17/results.json").read_text()
    )


from itertools import combinations
from math import factorial


def subset_oracle(players, value):
    n = len(players)
    out = {}
    for p in players:
        rest = [q for q in players if q != p]
        out[p] = 0.0
        for k in range(n):
            for s in combinations(rest, k):
                weight = factorial(k) * factorial(n - k - 1) / factorial(n)
                out[p] += weight * (value(set(s) | {p}) - value(set(s)))
    return out


def test_intervention_is_not_log_edit():
    assert m.evaluate(1) == {"a": 2, "b": 1, "z": 1, "y": 5}
    assert m.evaluate(1, {"a": 0})["y"] == 3
    assert m.evaluate(1, {"b": 0})["y"] == 2
    assert m.evaluate(1, {"z": 0})["y"] == 5
    log = m.evaluate(1)
    log["a"] = 0
    assert log["y"] == 5
    assert m.evaluate(1, {"y": 9})["y"] == 9


@pytest.mark.parametrize("kind", ["or", "and", "additive", "interaction"])
def test_credit_efficiency_symmetry_and_independent_oracle(kind):
    players = ("a", "b", "c")
    games = {
        "or": lambda s: float(bool(s)),
        "and": lambda s: float(len(s) == 3),
        "additive": lambda s: sum({"a": 2, "b": 3, "c": 0}[p] for p in s),
        "interaction": lambda s: (
            2 * ("a" in s) + 5 * ({"b", "c"} <= set(s)) + 7
        ),
    }
    v = games[kind]
    actual = m.shapley(players, v)
    assert actual == pytest.approx(subset_oracle(players, v))
    assert sum(actual.values()) == pytest.approx(v(set(players)) - v(set()))
    assert m.shapley(players[::-1], v) == pytest.approx(actual)
    if kind in ("or", "and"):
        assert list(actual.values()) == pytest.approx([1 / 3] * 3)


@pytest.mark.parametrize("retention", [0, 0.5, 0.9, 1])
@pytest.mark.parametrize("k", range(6))
def test_temporal_credit_closed_form(retention, k):
    xs = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    original = list(xs)
    base = m.memory(xs, retention)
    patch = m.memory(xs, retention, (k, 0))
    for t, (a, b) in enumerate(zip(base, patch)):
        expected = 0 if t < k else xs[k] * retention ** (t - k)
        assert a - b == pytest.approx(expected)
    assert xs == original


def test_redundancy_synergy_and_confounding():
    for u in range(-5, 6):
        assert m.evaluate(u)["y"] == 5 * m.evaluate(u)["z"]
    assert m.evaluate(1, {"z": 2})["y"] == 5
    # A surrogate 5*z agrees observationally but predicts 10 under this intervention.
    assert m.shapley(("a", "b"), lambda s: float(bool(s))) == {
        "a": 0.5,
        "b": 0.5,
    }
    assert m.shapley(("a", "b"), lambda s: float(len(s) == 2)) == {
        "a": 0.5,
        "b": 0.5,
    }


def test_invalid_interventions():
    with pytest.raises(ValueError):
        m.evaluate(0, {"unknown": 1})
    with pytest.raises(ValueError):
        m.memory([1], patch=(1, 0))
    with pytest.raises(ValueError):
        m.shapley(("a", "a"), lambda s: 1)
