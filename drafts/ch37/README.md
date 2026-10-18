# Chapter 37 — standalone batch A candidate

LaTeX-first source: manuscript.tex. Whole tested functions and computed tables
are extracted by build.py, cloned from the Chapter 35 builder. Five native TikZ
plates have semantic TXT companions; twenty exercises have worked answers/rubrics.
Package adoption, integrity, sources and local review live in
research/integration/ch37/. No global integration or publication acceptance is claimed.

Reproduce from the book root with Python >=3.11, PyTorch 2.10 CPU, NumPy,
pytest and Pillow; XeLaTeX/latexmk/makeindex and Poppler must be on PATH:

```sh
python -m pytest -q tests/test_ch37_reference.py -o addopts=''
python drafts/ch37/build.py --render
python drafts/ch37/build.py --check
```

This run uses /private/tmp/evolutor-batch-a-venv/bin/python, created with
/opt/homebrew/bin/python3 -m venv and installed torch==2.10.0, pytest, numpy,
pillow. The system/Xcode and bundled artifact Python lacked torch; do not
mistake their failed collection attempts for executed chapter tests.
The PDF skill marker was run once for the batch's three outputs.

All execution is serialized and trusted. Chapter 36 refines the actual
Chapter 35 layered cache with contiguous staging; Chapter 37 uses that pool
for page-credit scheduling and separately emulates rounded KV; Chapter 38
tests history-conditioned speculation, complete-stack online attention
and a separate page-streaming attention visitor. There is no measured
device kernel, production concurrency/security, fairness guarantee or
learned biological/AGI capability result. Final integration must reconcile
the Chapter 37 versus 38 consumed/emitted token API conventions explicitly.
