# Chapter 7 review candidate

Original authored-LaTeX chapter, 20 September 2026. Five editable vector
figures with semantic TXT companions, executable derivations, and twelve
worked exercises. Earlier reviewed chapters remain unchanged.

## Reproduce

From the repository root:

    python3 drafts/ch07/build.py --render
    python3 drafts/ch07/build.py --check
    python3 -m pytest -o addopts='' -q tests/test_ch07_reference.py

Python 3.10+, pytest, Pillow, XeLaTeX/latexmk, Poppler, and the fonts in
review.tex are required. The reference also requires PyTorch; local verification uses 2.10.0 CPU float64.
The local gitignored PDF is output/pdf/evolutor-ch07-review.pdf.
The builder generates tables and plots from reference.py and extracts whole
functions for code listings. It does not convert Markdown into manuscript prose.

See sources.tex for source access depth and evidence limitations, and
STORYBOARD.md for the illustration logic. Chapter 7 is not cumulative acceptance.
Author review is recorded separately; independent specialist review and
reader feedback remain open.
