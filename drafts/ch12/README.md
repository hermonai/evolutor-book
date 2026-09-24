# Chapter 12: Development and generated computational structure

Authored LaTeX review candidate, 24 September 2026. Five original editable
TikZ figures with semantic TXT companions, executable reference code,
independent checks and twelve worked exercises.

## Reproduce

    python3 drafts/ch12/build.py --render
    python3 drafts/ch12/build.py --check
    python3 -m pytest -o addopts='' -q tests/test_ch12_reference.py tests/test_ch12_review.py

Requires Python 3.10+, pytest, Pillow, XeLaTeX/latexmk, Poppler and the fonts
specified in review.tex. PyTorch 2.10 CPU float64 was used for numerical checks.
The PDF is generated under output/pdf/ and is gitignored.

General pedagogy acknowledgments remain in book-level frontmatter. This chapter
adds source-specific access notes and keeps claim limitations next to the claims.
Independent specialist/reader review and cumulative integration remain open.
Prior chapters and accepted editions are preserved.
