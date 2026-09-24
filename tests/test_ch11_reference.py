from pathlib import Path
import importlib.util
import sys
import json
import pytest
import math

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ch11_reference_tests", ROOT / "drafts/ch11/reference.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_occupancy_normalizes_and_competition_reduces_activity():
    assert m.occupancy(0.2, 0) == pytest.approx((5 / 6, 1 / 6, 0))
    assert m.occupancy(0.2, 1)[1] == pytest.approx(1 / 11)
    assert sum(m.occupancy(1e308, 1e308)) == pytest.approx(1)
    assert m.occupancy(0, 0) == (1, 0, 0)


@pytest.mark.parametrize(
    "rna_rate,protein_rate", [(1, 0.5), (1, 1), (1, 1 + 1e-12), (0.5, 2)]
)
def test_exact_step_matches_independent_rk4(rna_rate, protein_rate):
    state = m.State(0.3, 0.7)
    dt = 0.001
    source = 2
    k = 1.7
    y = [state.rna, state.protein]

    def f(v):
        return [source - rna_rate * v[0], k * v[0] - protein_rate * v[1]]

    for _ in range(1000):
        a = f(y)
        b = f([v + dt * z / 2 for v, z in zip(y, a)])
        c = f([v + dt * z / 2 for v, z in zip(y, b)])
        d = f([v + dt * z for v, z in zip(y, c)])
        y = [
            v + dt * (aa + 2 * bb + 2 * cc + dd) / 6
            for v, aa, bb, cc, dd in zip(y, a, b, c, d)
        ]
    exact = m.expression_step(state, source, k, rna_rate, protein_rate, 1)
    assert [exact.rna, exact.protein] == pytest.approx(y, rel=1e-10)


def test_equal_rates_closed_form_and_semigroup():
    s = m.expression_step(m.State(), 2, 3, 1, 1, 2)
    assert s.rna == pytest.approx(2 * (1 - math.exp(-2)))
    assert s.protein == pytest.approx(6 * (1 - 3 * math.exp(-2)))
    start = m.State(0.2, 1)
    whole = m.expression_step(start, 2, 3, 1, 0.5, 2)
    half = m.expression_step(start, 2, 3, 1, 0.5, 1)
    twice = m.expression_step(half, 2, 3, 1, 0.5, 1)
    assert twice.rna == pytest.approx(whole.rna)
    assert twice.protein == pytest.approx(whole.protein)


def test_steady_state_and_zero_duration():
    state = m.steady_state(2, 2, 1, 0.5)
    assert state == m.State(2, 8)
    assert m.expression_step(state, 2, 2, 1, 0.5, 10) == state
    assert m.expression_step(state, 0, 0, 1, 0.5, 0) == state


def test_closed_promoter_does_not_erase_existing_expression():
    d = m.Definition(12, 2, 1, 0.5)
    cold = m.regulated_step(d, m.State(), 0.2, 0, 0, 1)
    warm = m.regulated_step(d, m.State(2, 8), 0.2, 0, 0, 1)
    assert cold == m.State()
    assert warm.protein == pytest.approx(6.761455026030596)


def test_protein_only_cannot_separate_source_and_translation():
    for t in [0.1, 1, 5, 20]:
        a = m.expression_step(m.State(), 2, 2, 1, 0.5, t)
        b = m.expression_step(m.State(), 1, 4, 1, 0.5, t)
        assert a.protein == pytest.approx(b.protein)
        assert a.rna == pytest.approx(2 * b.rna)


def test_protein_can_rise_just_after_transcription_stops():
    rows = m.results()["response"]
    assert rows[17]["rna"] < rows[16]["rna"]
    assert rows[17]["protein"] > rows[16]["protein"]


@pytest.mark.parametrize(
    "gm,gp,dt", [(0, 1, 1), (1, 0, 1), (1, 1, -1), (1, 1, float("nan"))]
)
def test_invalid_dynamics(gm, gp, dt):
    with pytest.raises(ValueError):
        m.expression_step(m.State(), 2, 2, gm, gp, dt)


def test_generated_results():
    assert m.results() == json.loads(
        (ROOT / "drafts/ch11/results.json").read_text()
    )


def test_closed_access_does_not_hide_invalid_definition():
    with pytest.raises(ValueError):
        m.regulated_step(
            m.Definition(-1, 2, 1, 0.5), m.State(), 0.2, 0, 0, 1
        )
