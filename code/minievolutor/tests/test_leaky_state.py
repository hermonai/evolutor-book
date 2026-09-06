from fractions import Fraction as F
from itertools import product
import pytest
from minievolutor.leaky_state import response, closed_form, chapter_example


def test_exact_pulse_trajectory():
    assert [s.after for s in chapter_example()] == [2, 3, F(3, 2), F(3, 4), F(3, 8), F(35, 16)]
    assert [s.instantaneous for s in chapter_example()] == [2, 2, 0, 0, 0, 2]


def test_recurrence_matches_convolution_over_all_short_binary_inputs():
    for length in range(8):
        for signals in product((0, 1), repeat=length):
            for loss in (F(0), F(1, 2), F(1)):
                steps = response(signals, production=3, loss=loss, initial=1)
                actual = steps[-1].after if steps else F(1)
                assert actual == closed_form(signals, production=3, loss=loss, initial=1)


def test_decay_and_same_input_different_history():
    first = response((1, 0))[-1]
    second = response((0, 0))[-1]
    assert first.signal == second.signal == 0 and first.after != second.after
    assert response((0, 0, 0), initial=8)[-1].after == 1


def test_loss_extremes_and_nonnegative_bound():
    assert [s.after for s in response((1, 0, 1), loss=1)] == [2, 0, 2]
    assert [s.after for s in response((1, 0, 1), loss=0)] == [2, 2, 4]
    assert all(0 <= s.after <= 4 for s in response((1,) * 20))


def test_invalid_parameters_and_signals():
    for loss in (-1, 2):
        with pytest.raises(ValueError):
            response((1,), loss=loss)
    for kwargs in ({"production": -1}, {"initial": -1}):
        with pytest.raises(ValueError):
            response((1,), **kwargs)
    with pytest.raises(TypeError):
        response((1,), loss=0.5)
    for signals in ((2,), (True,), (0.0,)):
        with pytest.raises(ValueError):
            response(signals)
