# Chapter 9: Assembling a Transformer block

Authored LaTeX review candidate with six original vector figures, semantic TXT
companions, runnable reference code, and twelve worked exercises.

## Reproduce

    python3 drafts/ch09/build.py --render
    python3 drafts/ch09/build.py --check
    python3 -m pytest -o addopts='' -q tests/test_ch09_reference.py tests/test_ch09_review.py

Requires Python 3.10+, pytest, Pillow, XeLaTeX/latexmk, Poppler, and the
fonts specified in review.tex. Numerical checks use PyTorch 2.10.0 CPU float64.
PDF: output/pdf/evolutor-ch09-review.pdf (generated, gitignored).

General acknowledgment and evidence policy remain in book-level frontmatter.
Source-specific access notes and model limitations remain in the chapter.
Standalone author review does not advance cumulative acceptance.
