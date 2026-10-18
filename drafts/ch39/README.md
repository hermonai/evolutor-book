# Chapter 39 standalone integration candidate

Authored LaTeX is `manuscript.tex`; `reference.py` is the inspectable source.
The builder extracts whole tested functions and regenerates result tables.
Native TikZ and semantic TXT are in `figures/`; storyboard decisions precede prose.

From the book repository, with Python 3.13, PyTorch 2.10, pytest, Pillow,
XeLaTeX/latexmk/makeindex and Poppler available:

```sh
python3 -m pytest tests/test_ch39_reference.py
python3 drafts/ch39/build.py --render
python3 drafts/ch39/build.py --check
```

Output: `output/pdf/evolutor-ch39-review.pdf`. Generated artifacts stay in
`build/ch39/` and `tmp/pdfs/ch39-review/`.
Package integrity, full section adoption, primary-source access and local review
are under `research/integration/ch39/`.

The output is an authored, tested standalone review candidate. Independent
review, cross-batch integration, cumulative layout and publication acceptance
remain open. No Chapter 36 import or simulated passing allocation integration
is used. See the batch B handoff for coordinator checks. Do not infer hardware
performance, learned task capability, production security or durable deployment
from these trusted serialized examples.
