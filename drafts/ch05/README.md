# Chapter 5 — Tokenization and sequence representation

Standalone authored-LaTeX review candidate, 15 September 2026. Five original
TikZ mechanism plates with semantic TXT companions, generated resource
accounting, tested Python/PyTorch examples, and twelve worked exercises.
Earlier accepted editions and Chapters 3–4 review sources remain unchanged.

Build a lossless canonical-DNA tokenizer, base-four IDs, explicit vocabulary
IDs, checked offsets, row-lookup embeddings, and causal target boundaries.
Negative controls expose overlapping-target leakage, nonzero padding
vectors, and reverse-complement partition errors with short tails.
No trained genomic model or measured throughput improvement is claimed.

## Reproduce

Run from the repository root:

    python3 drafts/ch05/build.py --render
    python3 drafts/ch05/build.py --check
    python3 -m pytest -o addopts='' -q tests/test_ch05_reference.py

Dependencies: Python 3.10+, PyTorch (tested with 2.10.0), pytest, Pillow for
contact sheets, XeLaTeX/latexmk, Poppler, and fonts declared in review.tex.
The build creates output/pdf/evolutor-ch05-review-v2.pdf and previews under

Revision 2 centralizes the recurring pedagogy and review disclosure in
tex/frontmatter/about-this-book.tex. Earlier PDF and review records are retained.
tmp/pdfs/ch05-review/; these outputs are local, not tracked in Git.

The manuscript is authored directly in LaTeX. Whole tested functions become
code listings; resource counts and golden results come from reference.py.
The builder rejects overflow, missing glyphs, and unresolved references.
The source notes state actual access depth and limits of the numerical
demonstrations. Raschka's author companion informed the general teaching
progression; all prose, examples, code, and figures are original.

The author review in artifacts/deep/ch05-review.json binds source hashes.
Independent review and cumulative acceptance remain open; the accepted
Chapters 1–2 stay frozen. Next planned chapter: recurrent models and gated state.
