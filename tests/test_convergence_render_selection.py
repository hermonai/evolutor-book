"""Page selection tests only; never rebuild preservation-test PDFs here."""

import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "convergence_render", Path(__file__).parents[1] / "scripts/review-convergence.py"
)
r = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)


@pytest.mark.parametrize(
    "expression,expected",
    [
        ("all", list(range(1, 11))),
        ("4-6,1,5,9-10", [1, 4, 5, 6, 9, 10]),
        ("1", [1]),
    ],
)
def test_exact_deduplicated_selection(expression, expected):
    assert r.selected_pages(expression, 10) == expected


@pytest.mark.parametrize("expression", ["0", "11", "3-2", "1-2-3", ""])
def test_invalid_or_outside_page_ranges_fail(expression):
    with pytest.raises(ValueError):
        r.selected_pages(expression, 10)


def test_consecutive_runs_preserve_every_selected_page_once():
    selected = [1, 4, 5, 6, 9, 10]
    runs = r.page_runs(selected)
    assert runs == [(1, 1), (4, 6), (9, 10)]
    assert [p for first, last in runs for p in range(first, last + 1)] == selected
    assert r.page_runs([]) == []
