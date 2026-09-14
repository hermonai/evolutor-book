# Chapter 4 review candidate

**Reproducible PyTorch training**

This standalone chapter is authored directly in [LaTeX](manuscript.tex), following
the repository's textbook standard. It does not regenerate prose from Markdown,
change accepted Chapters 1-2, or promote Chapter 3 to cumulative acceptance.
The curriculum's cumulative progression remains gated; this directory records
the separate Chapter 4 production candidate requested by the author.

The chapter builds a synthetic one-base-context predictor and derives alignment,
target masking, count-weighted cross-entropy, momentum updates, data-split lineage,
evaluation mode, and the complete state needed for the supported restart boundary.
Its 84-parameter CPU model is a teaching component, not a genomic benchmark or
an implemented DOGMA/Hermon DNA architecture. Exact replay is environment-scoped;
in-memory serialization is not a crash-safe filesystem checkpoint.

Five editable native TikZ plates explain data lineage, tensor alignment, objective
weighting, the training transition, and computed missing-state controls.
[Semantic TXT companions](figures/semantic-descriptions.txt) preserve their logic.
Twelve exercises have worked answers or a scoring rubric. The
[reference module](reference.py), [recorded results](results.json), and
[source notes](sources.tex) provide executable evidence and primary documentation.

## Reproduce

The recorded environment is Python 3.13.6, PyTorch 2.10.0, CPU float64, and one
execution thread. Building also uses TeX Live 2025 with XeLaTeX/latexmk and
makeindex, Poppler, and Pillow. Fonts: TeX Gyre Pagella (body and mathematics),
TeX Gyre Heros (headings), and DejaVu Sans Mono (code).

From the repository root, with those dependencies available:

```sh
python3 drafts/ch04/reference.py
python3 drafts/ch04/build.py --assets-only
python3 drafts/ch04/build.py --check
python3 -m pytest -o addopts='' -q tests/test_ch04_reference.py
python3 drafts/ch04/build.py --render
```

The builder writes `output/pdf/evolutor-ch04-review.pdf`, data tables and literal
code excerpts under `build/ch04/`, and all page renders plus color and grayscale
contact sheets under `tmp/pdfs/ch04-review/`. Run full-repository tests after PDF
builds finish, because preservation tests must not race output writes. Build
outputs remain generated artifacts, consistent with the repository's ignore rules.

## Review status

The 16-page candidate received author technical, editorial, and all-page visual
review, including grayscale inspection, on 14 September 2026. This is not
independent specialist review. Compilation has no overfull boxes, missing glyphs,
or unresolved references. Exact-restart tests cover cuts after updates 1 through
7 and compare parameters, optimizer state, row traces, and loss traces. Three
intentional state omissions cause divergence. Other tests cover masking gradients,
padding, duplicate boundaries, snapshot aliasing, and evaluation side effects.
The full repository suite also passes its preservation contracts.

See the [source-bound review record](../../artifacts/deep/ch04-review.json).
Open gates: independent specialist review, reader feedback, and cumulative
integration with consistent cross-chapter numbering/index/bibliography. Those
gates remain open for prior review candidates too.
