# Chapter 15: Operational semantics and expression traces

Standalone authored-LaTeX review candidate. Prior accepted editions remain unchanged.

The original manuscript, tested reference implementation, editable TikZ figures and semantic TXT companions are stored together here. Source-access notes are in sources.tex. Each chapter includes worked exercises and explicit model limitations.

Run from the repository root with Python 3.13 and the project's dependencies:

```sh
python3 drafts/ch15/build.py --assets-only
python3 -m pytest tests/test_ch15_reference.py
python3 drafts/ch15/build.py --render
python3 drafts/ch15/build.py --check
```

Output: output/pdf/evolutor-ch15-review.pdf.

Independent specialist review, reader feedback and cumulative integration remain open.
