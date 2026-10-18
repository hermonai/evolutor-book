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


def test_arxiv_views_and_versions_share_one_identity():
    base = r.identity(r"\url{https://arxiv.org/abs/2403.03234}")
    assert base == r.identity(r"\url{https://arxiv.org/html/2403.03234v1}")
    assert base == r.identity(r"\url{https://arxiv.org/pdf/2403.03234v2}")
    assert base != r.identity(r"\url{https://arxiv.org/abs/2403.03235}")
    # A DOI still takes precedence over an arXiv link in the same entry.
    assert r.identity(
        r"\url{https://doi.org/10.1/X} \url{https://arxiv.org/abs/2403.03234}"
    ) == "doi:10.1/x"


def test_source_note_becomes_a_section_of_its_chapter_in_the_book():
    note = (
        r"\chapter*{Sources and further reading}" + "\n"
        + r"\addcontentsline{toc}{chapter}{Sources and further reading}" + "\nText."
    )
    assert r.evidence_heading(note) == (
        r"\section*{Sources and further reading}" + "\n"
        + r"\addcontentsline{toc}{section}{Sources and further reading}" + "\nText."
    )
    # Notes that already use a section, or a mismatched contents title, are untouched.
    section = r"\section*{Sources and evidence}" + "\n" + r"\addcontentsline{toc}{section}{Sources and evidence}"
    assert r.evidence_heading(section) == section
    # A note without a contents line stays out of the contents.
    assert r.evidence_heading(r"\chapter*{Evidence}" + "\nText.") == r"\section*{Evidence}" + "\nText."
    # A mismatched contents title is not silently rewritten.
    odd = r"\chapter*{A}" + "\n" + r"\addcontentsline{toc}{chapter}{B}"
    assert r.evidence_heading(odd) == r"\section*{A}" + "\n" + r"\addcontentsline{toc}{chapter}{B}"


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


def test_reserved_figure_loop_variable_is_alpha_renamed_only_in_derived_text():
    source = r"\foreach \x/\label in {0/a,1/b}{\node at (\x,0) {\label};}"
    changed = r.safe_figure_loop_variable(source)
    assert changed == source.replace(r"\label", r"\EvolutorLoopText")
    assert r.safe_figure_loop_variable(changed) == changed
    ordinary_label = r"\node {text}; \label{actual-figure}"
    assert r.safe_figure_loop_variable(ordinary_label) == ordinary_label


def test_ambiguous_loop_and_real_reference_label_fail_instead_of_corrupting():
    source = r"\foreach \x/\label in {0/a}{\node {\label};}\label{real}"
    with pytest.raises(ValueError, match="Ambiguous"):
        r.safe_figure_loop_variable(source)


def test_cumulative_preamble_accepts_incremental_line_number_marker():
    text = (Path(__file__).parents[1] / "tex/convergence/preamble.tex").read_text()
    assert r"\providecommand\@LN@col[1]{}" in text


def test_figure_labels_bypass_caption_local_label_reset_with_explicit_namespace():
    text = (Path(__file__).parents[1] / "tex/convergence/preamble.tex").read_text()
    assert r"\noexpand\OriginalBookLabel{\ChapterNamespace#3}" in text


def test_printed_part_navigation_matches_complete_chapter_map():
    starts = r.part_starts()
    assert list(starts) == [1, 2, 11, 18, 23, 25, 30, 35, 39, 44, 48, 52]
    assert starts[35] == "Hermon DNA Engine: attention-native inference"


def test_cumulative_definition_reserves_its_heading_prose_and_display():
    text = r"\section{Construct the next mixed iteration}" + "\nDefinition."
    assert r"\Needspace{8\baselineskip}" in r.cumulative_layout(37, text)
    assert r.cumulative_layout(36, text) == text
