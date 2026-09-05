# Chapter 1 development report

Date: 2026-09-05. Branch: `astra-rewrite`. This is one internally reviewed chapter, not a finished book or an independently peer-reviewed release.

## Delivered

[Canonical manuscript](tex/chapters/ch01.tex), [research and skeptical review](research/chapter-01-review.md), [claim ledger](research/claims-ledger.md), [example records](book/results/ch01.json), [canonical graph](book/diagrams/evo-g06.txt), and [generated SVG](book/figures/evo-g06.svg).

The chapter includes a concrete example, an elementary proposition with explicit premises, resource/evidence boundaries, six exercises and concise solution notes. The active PDF now contains a reader preface and Chapter 1 rather than reset-only typesetting demonstrations. Planned later chapters are not placeholders in the manuscript.

## Result and interpretation

Indexed and full-scan dispatch return the same arithmetic results under the declared contract. For libraries of four and 64 operations, both fire once, while the full scan performs four and 64 name comparisons. Equivalence is checked over 492 request/input cases and against independent arithmetic expressions. These logical counters do not establish wall-clock speed, genomic novelty, learned behavior or AGI capability.

## Verification

- **25 tests passed**, including existing regression checks, byte-for-byte historical preservation, active links/manifest, graph contracts, example oracles and generated-record freshness.
- **13-page A4 PDF, version 1.7**, built with XeLaTeX/TeX Live 2025 and latexmk 4.86a. Final log checks passed: no errors, missing glyphs, undefined citations/references or overfull boxes.
- Rendered every final page with Poppler and inspected the complete contact sheet plus full-size proof/table and figure pages. The generated table and six-node diagram remain legible with no observed clipping or overlapping labels. A first-build unsupported notation macro was replaced with standard evaluation notation, then rebuilt successfully.
- The PDF skill required render-and-review before delivery; log checks alone were not used as visual certification.
- Verified environment: Python 3.13.6, PyTorch 2.10.0, pytest 9.0.2. These tests and exact example counts are not new wet-lab or learned-model results.

The PDF is not tagged or PDF/UA-certified. Canonical TXT and accessible SVG descriptions provide diagram alternatives; final accessibility and independent subject review remain open.

## Reproduce

```sh
python3 -m pytest
python3 scripts/chapter01_artifacts.py --check
make pdf check-pdf
```

Use the documented Python/TeX environment in PUBLICATION_PLAN.md. Generated JSON and LaTeX table sources are committed and freshness-tested; local PDF/build products remain ignored. The reset report is pinned to its original milestone commit.

## Next

Chapter 2: biological inspiration and its limits, with explicit separation between documented biological mechanisms and proposed computational analogies.

Public source: [hermonai/evolutor-book](https://github.com/hermonai/evolutor-book/tree/astra-rewrite). The earlier default `main` and archival branch are preserved; no force-push, new license or authorship change is part of this milestone.
