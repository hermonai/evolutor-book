# Chapter 2 development report

> Preserved edition-2 document. This does not describe the active undergraduate-first edition. See [PEDAGOGICAL_REDESIGN.md](PEDAGOGICAL_REDESIGN.md); the new manuscript has no drafted chapters yet.

Date: 2026-09-06. Publication branch: `astra-rewrite`. This is an internally reviewed two-chapter draft, not a complete or independently peer-reviewed textbook.

## Delivered

[Chapter 2](tex/chapters/ch02.tex): **Biological inspiration and its limits**. Includes a bounded biological account, exact worked example, elementary proof, resource/model limitations, six exercises and solution notes.

[Research review](research/chapter-02-review.md), [canonical scientific graph](book/diagrams/evo-g07.txt), [generated SVG](book/figures/evo-g07.svg), [executed records](book/results/ch02.json), and [claim ledger](research/claims-ledger.md) make the evidence boundaries inspectable. Chapter 1 remains in the manuscript.

## What the example establishes

A scalar recurrence retains state after its input switches off; an instantaneous gate does not. Exact rational results are checked against the convolution expression for 765 binary-input/loss-setting cases, with decay and boundary-case tests. This is a conventional leaky integrator in arbitrary units, not a biological simulation, learning mechanism or AGI result. Sequence-transfer arrows and regulatory inhibition are explicitly distinguished in the scientific diagram.

## Verification

The full test suite passes (32 tests), including artifact freshness, canonical graph contracts and executable-example checks. The A4 PDF contains 18 pages and passes the PDF log check with no missing glyphs, undefined references or overfull boxes. All final pages were inspected as rendered contact sheets, with detailed inspection of the new figures, equations, tables and code examples.

Visual review caught crowded stacked fractions in the results table and a nearly empty ending page; inline rational notation and a tighter ending resolved both.

Verification used Python 3.13.6, pytest 9.0.2, TeX Live 2025 (XeLaTeX), latexmk 4.86a, rsvg-convert 2.61.1 and Poppler. The output uses PDF 1.7. These internal tests establish the stated computational contracts, not experimental biological validity.

The PDF skill requires rendering and visual inspection, not just compilation. Canonical TXT and accessible SVG descriptions accompany the figures; the PDF is not tagged or PDF/UA-certified. Independent scientific review remains a final-release gate.

## Reproduce

```sh
python3 -m pytest
python3 scripts/chapter02_artifacts.py --check
make pdf check-pdf
```

See PUBLICATION_PLAN.md for the build environment. Public source is on [hermonai/evolutor-book](https://github.com/hermonai/evolutor-book/tree/astra-rewrite). PDFs remain local build artifacts; their source, tables and SVGs are versioned. The earlier main branch and archival history are preserved.

## Next

Chapter 3: capabilities, evidence and AGI claims. Develop an operational scorecard with explicit task scope and evaluation boundaries, without transferring unit-test success into broad capability claims.
