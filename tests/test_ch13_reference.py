from pathlib import Path
import importlib.util
import sys
import json
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ch13_reference_tests", ROOT / "drafts/ch13/reference.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

from itertools import product
import numpy as np


@pytest.mark.parametrize("steps", [0, 1, 2, 10, 40])
def test_training_recurrence_oracles(steps):
    for mask in [(1, 0), (0, 1)]:
        w = m.fit(mask, m.TRAIN_X, m.TRAIN_Y, steps=steps)
        np.testing.assert_allclose(
            w, np.array(mask) * 2 * (1 - 0.8**steps), atol=1e-14
        )
    np.testing.assert_allclose(
        m.fit((1, 1), m.TRAIN_X, m.TRAIN_Y, steps=steps),
        np.full(2, 1 - 0.6**steps),
        atol=1e-14,
    )


@pytest.mark.parametrize("mask", list(product((0, 1), repeat=2)))
def test_gradient_finite_difference(mask):
    x = np.array([[0.2, -0.7], [0.9, 0.4], [-0.3, 0.8]])
    y = np.array([0.1, 0.7, -0.5])
    w = np.array([0.3, -0.2])
    mm = np.array(mask)
    grad = 2 * mm * (x.T @ (x @ (mm * w) - y)) / len(y)
    numeric = []
    for i in range(2):
        d = np.zeros(2)
        d[i] = 1e-6
        numeric.append(
            (m.mse(mask, w + d, x, y) - m.mse(mask, w - d, x, y)) / 2e-6
        )
    np.testing.assert_allclose(grad, numeric, rtol=1e-8, atol=1e-9)
    # Test actual fit first update, not just the standalone formula.
    residual = -y
    expected = -0.1 * 2 * mm * (x.T @ residual) / len(y)
    np.testing.assert_allclose(m.fit(mask, x, y, steps=1), expected)


def test_validation_closed_form_for_arbitrary_weights():
    for mask in product((0, 1), repeat=2):
        w = np.array([0.7, -1.3])
        expected = (mask[0] * w[0] - 2) ** 2 + (mask[1] * w[1]) ** 2
        assert m.mse(mask, w, m.VALID_X, m.VALID_Y) == pytest.approx(
            expected
        )


def test_lineage_and_no_inheritance():
    history = m.evolve()
    assert [r["winner"] for r in history] == [[0, 1], [1, 1], [1, 0]]
    assert [len(r["candidates"]) for r in history] == [1, 3, 3]
    for r in history:
        for candidate in r["candidates"]:
            np.testing.assert_allclose(
                candidate["weights"],
                m.fit(candidate["mask"], m.TRAIN_X, m.TRAIN_Y),
            )
    assert all(
        a["score"] >= b["score"] for a, b in zip(history, history[1:])
    )


def test_selection_order_invariance_and_tie_break():
    masks = [(1, 0), (0, 1)]
    a = m.select(masks, m.TRAIN_X, m.TRAIN_Y, m.TRAIN_X, m.TRAIN_Y)[0]
    b = m.select(masks[::-1], m.TRAIN_X, m.TRAIN_Y, m.TRAIN_X, m.TRAIN_Y)[0]
    assert a == b and a["mask"] == [0, 1]


def test_inheritance_coordinate_policy():
    old = np.array([2.0, 9.0])
    np.testing.assert_array_equal(
        m.inherit((1, 0), (1, 1), old), [2.0, 0.0]
    )
    np.testing.assert_array_equal(
        m.inherit((1, 1), (0, 1), old), [0.0, 9.0]
    )
    np.testing.assert_array_equal(old, [2.0, 9.0])
    with pytest.raises(ValueError):
        m.inherit((1,), (1, 0), [2.0])


def test_repeated_testing_probability():
    assert m.false_positive(0) == 0
    assert m.false_positive(2) == pytest.approx(0.0975)
    assert m.false_positive(20) == pytest.approx(0.6415140775914581)


@pytest.mark.parametrize(
    "mask,x,y",
    [
        ((1, 2), [[1.0, 2.0]], [1.0]),
        ((1, 0), [], []),
        ((1, 0), [[1.0, 2.0]], [1.0, 2.0]),
        ((1, 0), [[float("nan"), 2.0]], [1.0]),
    ],
)
def test_invalid_fit(mask, x, y):
    with pytest.raises(ValueError):
        m.fit(mask, x, y)


def test_committed_result_artifact_matches_execution():
    assert (
        json.loads((ROOT / "drafts/ch13/results.json").read_text())
        == m.results()
    )
