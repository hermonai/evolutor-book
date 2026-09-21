# Chapter 10: Conditional computation and routing

Authored LaTeX review candidate with five original editable vector figures,
semantic TXT companions, tested reference code, and twelve worked exercises.

## Reproduce

    python3 drafts/ch10/build.py --render
    python3 drafts/ch10/build.py --check
    python3 -m pytest -o addopts='' -q tests/test_ch10_reference.py tests/test_ch10_review.py

Requires Python 3.10+, PyTorch (tested with 2.10, CPU float64), pytest, Pillow, XeLaTeX/latexmk,
Poppler and the fonts specified in review.tex.
PDF: output/pdf/evolutor-ch10-review.pdf (generated, gitignored).

Chapter 9 reference.py supplies normalization and attention; its hash is bound
in the Chapter 10 review record. Keep both chapter directories together.

General pedagogy acknowledgment remains in book-level frontmatter. Source-specific
notes and scientific/model limitations remain beside the chapter's claims.
Independent review and cumulative Chapters 1-10 integration remain open.
