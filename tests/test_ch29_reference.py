import importlib.util
import itertools
import math
from pathlib import Path
import random
import sys
from fractions import Fraction
import pytest

P = Path(__file__).parents[1] / "drafts/ch29/reference.py"
S = importlib.util.spec_from_file_location("evod29", P)
R = importlib.util.module_from_spec(S)
sys.modules[S.name] = R
S.loader.exec_module(R)


def test_paired_correctness_exact_fixture():
    d = R.paired_deltas(
        [1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 1, 1, 0], [1, 1, 0, 0, 1, 0, 0, 0]
    )
    assert d == [0, 1, 1, 0, 0, -1, 1, 0]
    assert sum(d) / len(d) == 0.25
    assert R.exact_bootstrap(d)["interval"] == [-0.25, 0.75]
    assert R.exact_paired_sign_test(d) == 0.625


@pytest.mark.parametrize("d", [[1, 0, -1], [1, 1, -1, -1], [0, 0], [1]])
def test_convolution_independent_cartesian_oracle(d):
    law = {}
    for draw in itertools.product(d, repeat=len(d)):
        total = sum(draw)
        law[total] = law.get(total, 0) + 1
    denominator = len(d) ** len(d)
    exact = R.exact_bootstrap(d)
    assert {v["sum"]: v["mass"] for v in exact["law"]} == pytest.approx(
        {s: n / denominator for s, n in law.items()}
    )
    assert math.fsum(v["mass"] for v in exact["law"]) == pytest.approx(1)


def test_convolution_multinomial_oracle_eight():
    d = [0, 1, 1, 0, 0, -1, 1, 0]
    law = {}
    for plus in range(9):
        for minus in range(9 - plus):
            zero = 8 - plus - minus
            ways = math.factorial(8) // (
                math.factorial(plus) * math.factorial(minus) * math.factorial(zero)
            )
            mass = (
                ways
                * Fraction(3, 8) ** plus
                * Fraction(1, 8) ** minus
                * Fraction(4, 8) ** zero
            )
            law[plus - minus] = law.get(plus - minus, Fraction(0)) + mass
    assert {x["sum"]: x["mass"] for x in R.exact_bootstrap(d)["law"]} == pytest.approx(
        {k: float(v) for k, v in law.items()}
    )


def test_sign_test_independent_swaps():
    # Four discordant pairs; independent within-pair label swaps yield >=observed.
    sums = [sum(v) for v in itertools.product((-1, 1), repeat=4)]
    assert (
        R.exact_paired_sign_test([1, 1, 1, -1, 0])
        == sum(abs(v) >= 2 for v in sums) / 16
    )


def test_identical_models_uncertainty_zero():
    d = R.paired_deltas([1, 0], [1, 1], [1, 1])
    assert R.exact_bootstrap(d)["interval"] == [0, 0]
    assert R.paired_bootstrap_ci(d) == (0, 0)
    assert R.exact_paired_sign_test(d) == 1


def test_interval_not_equivalence_proof():
    # Singleton returns degenerate plug-in interval despite population uncertainty.
    assert R.exact_bootstrap([1])["interval"] == [1, 1]


def test_discrete_quantile_convention():
    assert R.percentile([3, 1, 2, 4], 0.5) == 2
    assert R.percentile([3, 1, 2, 4], 0) == 1
    assert R.percentile([3, 1, 2, 4], 1) == 4


def test_crossed_bootstrap_independent_rng_trace():
    m = [[1, 1, 0, 0], [0, 0, -1, -1], [1, 1, 0, 0]]
    rng = random.Random(29)
    values = []
    for _ in range(4000):
        ss = [rng.choice(range(3)) for _ in range(3)]
        gs = [rng.choice(range(4)) for _ in range(4)]
        # Independent implementation with row/column multiplicity dot product.
        values.append(
            sum(ss.count(s) * gs.count(g) * m[s][g] for s in range(3) for g in range(4))
            / 12
        )
    values.sort()
    result = R.crossed_bootstrap(m)
    assert result["mean"] == 1 / 6
    assert result["interval"] == [values[99], values[3899]]


def test_seed_only_misses_shared_group_uncertainty():
    m = [[1, 1, -1, -1]] * 3
    assert R.crossed_bootstrap([[0.0]] * 3)["interval"] == [0, 0]
    assert R.crossed_bootstrap(m)["interval"] == [-1, 1]


def test_group_only_misses_training_variation():
    m = [[1] * 4, [-1] * 4, [1] * 4]
    assert R.crossed_bootstrap([[1 / 3] * 4])["interval"] == [1 / 3, 1 / 3]
    assert R.crossed_bootstrap(m)["interval"] == [-1, 1]


def test_repeated_rows_do_not_add_groups():
    # Two independent group effects +/-1. Duplication shrinks a false IID SE.
    groups = [1, -1]
    repeated = groups * 100
    group_se = math.sqrt(2) / math.sqrt(2)
    naive_se = math.sqrt(
        sum(x * x for x in repeated) / (len(repeated) - 1)
    ) / math.sqrt(len(repeated))
    assert group_se / naive_se > 10
    assert R.crossed_bootstrap([groups])["interval"] == [-1, 1]


def test_rng_isolation_and_reproduction():
    state = random.getstate()
    assert R.crossed_bootstrap([[1, 0], [-1, 1]]) == R.crossed_bootstrap(
        [[1, 0], [-1, 1]]
    )
    assert R.paired_bootstrap_ci([1, 0, -1]) == R.paired_bootstrap_ci([1, 0, -1])
    assert random.getstate() == state


@pytest.mark.parametrize("bad", [[], [True, 0], [2, 0], [float("nan")]])
def test_bad_deltas(bad):
    with pytest.raises(ValueError):
        R.exact_bootstrap(bad)


@pytest.mark.parametrize("alpha", [0, 1, -0.1, float("nan"), True])
def test_bad_alpha(alpha):
    with pytest.raises(ValueError):
        R.crossed_bootstrap([[0]], alpha=alpha)


@pytest.mark.parametrize("draws", [0, -1, 2.5, True])
def test_bad_draws(draws):
    with pytest.raises(ValueError):
        R.paired_bootstrap_ci([0], draws=draws)


def test_bad_matrix_and_accuracy():
    for m in ([], [[]], [[1], [1, 0]], [[float("nan")]], [[2]]):
        with pytest.raises(ValueError):
            R.crossed_bootstrap(m)
    with pytest.raises(ValueError):
        R.accuracy([1], [True])
    with pytest.raises(ValueError):
        R.paired_deltas([1], [1], [1, 0])


def test_seed_distribution_not_best():
    r = R.seed_summary([0.71, 0.74, 0.69, 0.73, 0.72])
    assert r["mean"] == pytest.approx(0.718)
    assert r["stdev"] == pytest.approx(0.01923538406167136)
    assert r["max"] > r["mean"]
    with pytest.raises(ValueError):
        R.seed_summary([0.5])


@pytest.mark.parametrize("v", [-1, True, 2.5, float("inf")])
def test_invalid_budget(v):
    with pytest.raises(ValueError):
        R.Budget(v, 1, 1, 1, 1, 1)


def test_budget_each_coordinate_blocks():
    ceiling = R.Budget(10, 10, 10, 10, 10, 10)
    for i in range(6):
        values = [1] * 6
        values[i] = 11
        assert not R.within_budget(R.Budget(*values), ceiling)
    assert R.within_budget(ceiling, ceiling)


def test_pareto_not_parameter_only():
    low = R.Budget(10, 10, 10, 10, 10, 10)
    high = R.Budget(11, 10, 10, 10, 10, 10)
    assert R.pareto_dominates(0.8, low, 0.8, high)
    assert not R.pareto_dominates(0.8, low, 0.8, low)
    assert not R.pareto_dominates(0.9, high, 0.8, low)


def test_capacity_tie_break_and_range():
    assert (
        R.capacity_match(
            [{"name": "b", "params": 110}, {"name": "a", "params": 90}], 100
        )["name"]
        == "a"
    )
    with pytest.raises(ValueError):
        R.capacity_match([{"name": "a", "params": True}], 100)


def test_detector_independent_exhaustive_all_length5():
    for word in itertools.product("ACGT", repeat=5):
        seq = "".join(word)
        assert R.detector(seq, "ACG") == int("ACG" in seq)
        assert R.detector(seq, "ACT") == int("ACT" in seq)


def test_matched_gc_target_and_sham():
    pos, neg = "ACGTT", "ACTGT"
    assert sum(c in "GC" for c in pos) == sum(c in "GC" for c in neg) == 2
    assert [R.intervention(s, "off") for s in (pos, neg)] == [0, 0]
    assert [R.intervention(s, "target") for s in (pos, neg)] == [1, 0]
    assert [R.intervention(s, "sham") for s in (pos, neg)] == [0, 1]


def test_false_positive_not_repaired_by_or():
    assert R.motif_oracle("GCGCG") == 0
    assert R.intervention("GCGCG", "target") == 1


def test_task_selection_reverses_ranking():
    assert 0.9 > 0.8
    assert (0.9 + 0.5) / 2 < (0.8 + 0.8) / 2


@pytest.mark.parametrize("seq", ["", "ACGN", None])
def test_bad_sequence(seq):
    with pytest.raises(ValueError):
        R.motif_oracle(seq)


def test_inverted_labels_detect_bounded_claim():
    records = ["ACGTT", "ACTGT"]
    y = [R.motif_oracle(s) for s in records]
    predictions = [R.intervention(s, "target") for s in records]
    assert R.accuracy(y, predictions) == 1
    assert R.accuracy([1 - v for v in y], predictions) == 0
