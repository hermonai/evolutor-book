# Chapter 8: Attention and content addressing

Authored LaTeX review candidate. Five original vector mechanism figures with TXT
companions, runnable reference code, independent checks, and twelve worked exercises.

## Reproduce

    python3 drafts/ch08/build.py --render
    python3 drafts/ch08/build.py --check
    python3 -m pytest -o addopts='' -q tests/test_ch08_reference.py tests/test_ch08_review.py

Requires Python 3.10+, pytest, Pillow, XeLaTeX/latexmk, Poppler, and the fonts
specified in review.tex. Numerical checks use PyTorch 2.10.0 CPU float64.
PDF: output/pdf/evolutor-ch08-review.pdf (generated, gitignored).

General pedagogical acknowledgment and evidence policy live once in
tex/frontmatter/about-this-book.tex. Chapter sources document only relevant
technical evidence. The review record binds the full chapter source set;
standalone author review is not cumulative acceptance.
