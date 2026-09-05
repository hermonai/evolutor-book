# Publication plan

## Format and scope

Title: Evolutor. Subtitle: Genomic Computation as a Testable Research Program. Edition label: **2-development**, a new major intellectual edition, not a final release. No author attribution or license is changed. The active shell is a prospectus and typesetting check, not a manuscript with placeholder chapters. Historic material is never included automatically.

Markdown holds research and rapid drafts; reviewed chapter LaTeX is the publication source. Conversion is explicit and reviewed: no two silently divergent canonical chapter versions. An HTML edition is deferred until the first reviewed chapters exist; GitHub renders the present Markdown/SVG materials.

## Reproducible build

Prerequisites: Python 3.11+, pytest, PyTorch (existing teaching code); TeX Live with XeLaTeX, latexmk, natbib, amsthm, fancyvrb, glossaries and makeidx; librsvg's rsvg-convert. TeX fonts are loaded by filename from the TeX distribution. No shell escape is required. The committed tex/.latexmkrc selects PDF 1.7 for vector-figure compatibility.

```sh
python3 -m pytest
make pdf
make check-pdf
```

Main entry: tex/evolutor.tex → preamble.tex + metadata.tex + frontmatter/prospectus.tex + chapters/manifest.tex + bibliography.bib. The manifest is empty by design, not populated with placeholder chapters. latexmk manages XeLaTeX/BibTeX passes. Index and no-index glossary hooks are exercised in the shell. TXT graph inclusion uses DejaVu Sans Mono with Unicode; vector figures are generated from the same canonical text.

Output: output/pdf/evolutor.pdf. Build products are ignored; source and reviewed SVGs are versioned. Build checks reject missing characters, undefined references/citations and overfull boxes. Visual review still matters; passing log checks is not layout certification. Record tool versions in RESET_REPORT.md. Reproducibility means same content/layout with documented dependencies, not byte-identical PDF timestamps.

## Release and review

First reboot commit contains research, audits, architecture, roadmaps and publication infrastructure only. Commit each repository separately on astra-rewrite and publish the branch after tests. Preserve main and the archival branch. Later reviewed chapter milestones may use edition-2-* tags; no final-edition tag is created now.

Before a chapter enters the manifest: complete source reading, claim classification, mathematical audit, executable example tests, biological/UML figure review, citation check, skeptical review and PDF inspection. Before public final release: independent subject review, full bibliography, index/glossary coverage, accessible alternatives, rights review and explicit author/license approval.

No third-party PDFs or supplied screenshots are redistributed. Measured tables must be generated from immutable experimental artifacts; currently there are no new measured research results.
