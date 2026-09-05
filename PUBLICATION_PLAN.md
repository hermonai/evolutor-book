# Publication plan

## Format and scope

Title: Evolutor. Subtitle: Genomic Computation as a Testable Research Program. Edition label: **2-development**, a new major intellectual edition, not a final release. No author attribution or license is changed. The active manuscript contains a reader preface and Chapter 1. Historic material and the reset prospectus are never included automatically.

Markdown holds research and rapid drafts; reviewed chapter LaTeX is the publication source. Conversion is explicit and reviewed: no two silently divergent canonical chapter versions. An HTML edition is deferred until the first reviewed chapters exist; GitHub renders the present Markdown/SVG materials.

## Reproducible build

Prerequisites: Python 3.11+, pytest, PyTorch (existing teaching code); TeX Live with XeLaTeX, latexmk, natbib, amsthm, fancyvrb, glossaries and makeidx; librsvg's rsvg-convert. TeX fonts are loaded by filename from the TeX distribution. No shell escape is required. The committed tex/.latexmkrc selects PDF 1.7 for vector-figure compatibility.

```sh
python3 -m pip install -e '.[dev]'
python3 -m pytest
make pdf
make check-pdf
```

Main entry: tex/evolutor.tex → preamble.tex + metadata.tex + frontmatter/preface.tex + chapters/manifest.tex + bibliography.bib. The manifest includes only the internally reviewed Chapter 1 draft and is checked against book/book.json. latexmk manages XeLaTeX/BibTeX passes. Index and no-index glossary hooks are active. Vector figures are generated from canonical Unicode TXT graphs.

`make pdf` regenerates diagrams and the Chapter 1 JSON/LaTeX table from the reference example before compiling. `python3 scripts/chapter01_artifacts.py --check` verifies committed record freshness. These are exact logical example counts, not newly measured research results. The verified environment uses Python 3.13.6, PyTorch 2.10.0 and pytest 9.0.2; select a suitable interpreter through `make PYTHON=...` if the default Python lacks dependencies.

Output: output/pdf/evolutor.pdf. Build products are ignored; source and reviewed SVGs are versioned. Build checks reject missing characters, undefined references/citations and overfull boxes. Visual review still matters; passing log checks is not layout certification. Record tool versions in RESET_REPORT.md. Reproducibility means same content/layout with documented dependencies, not byte-identical PDF timestamps.

## Release and review

First reboot commit contains research, audits, architecture, roadmaps and publication infrastructure only. Commit each repository separately on astra-rewrite and publish the branch after tests. Preserve main and the archival branch. Later reviewed chapter milestones may use edition-2-* tags; no final-edition tag is created now.

Before a chapter enters the manifest: complete source reading, claim classification, mathematical audit, executable example tests, biological/UML figure review, citation check, skeptical review and PDF inspection. Before public final release: independent subject review, full bibliography, index/glossary coverage, accessible alternatives, rights review and explicit author/license approval.

No third-party PDFs or supplied screenshots are redistributed. Measured tables must be generated from immutable experimental artifacts; currently there are no new measured research results.
