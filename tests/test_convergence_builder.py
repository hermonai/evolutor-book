"""Small independent checks of bibliography reconciliation and strict citations."""

import importlib.util
from pathlib import Path

import pytest

p = Path(__file__).parents[1] / "scripts/build-convergence.py"
spec = importlib.util.spec_from_file_location("convergence_builder", p)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def test_bibliography_body_with_nested_url_braces():
    source = (
        r"\begin{thebibliography}{99}\bibitem{a} Author. \url{https://doi.org/10.1/A}."
        + "\n"
        + r"\bibitem{b} Second.\end{thebibliography}"
    )
    items = r.bib_items(source)
    assert items == [("a", r"Author. \url{https://doi.org/10.1/A}."), ("b", "Second.")]
    assert r.strip_bib("before" + source + "after") == "beforeafter"


def test_duplicate_local_key_fails():
    with pytest.raises(ValueError, match="Duplicate"):
        r.bib_items(
            r"\begin{thebibliography}{9}\bibitem{x} A\bibitem{x} B\end{thebibliography}"
        )


def test_exact_doi_dedup_not_fuzzy_title():
    assert r.identity(r"A. \url{https://doi.org/10.1/AbC}.") == r.identity(
        r"B. \url{https://doi.org/10.1/abc}."
    )
    assert r.identity("Same title 2025") != r.identity("Same title 2026")


def test_case_sensitive_url_paths_remain_distinct():
    assert r.identity(r"\url{https://example.org/A}") != r.identity(
        r"\url{https://example.org/a}"
    )


def test_multikey_citation_remap_and_missing_key_fail():
    assert (
        r.remap_cites(r"\cite{x, y}", {"x": "ch22:x", "y": "shared"})
        == r"\cite{ch22:x,shared}"
    )
    with pytest.raises(ValueError, match="Unresolved"):
        r.remap_cites(r"\cite{unknown}", {})
