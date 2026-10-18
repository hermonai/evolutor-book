# Chapter 44 — Packaging, deployment and observable services

Authored LaTeX standalone review candidate. Retains the supplied r01 package's
scenarios and expands contracts, derivations, negative controls and worked
exercises. See research/integration/ch44/package-adoption.md for every incoming
section and exact provenance hashes. No production certification or acceptance.

From the repository root, using the existing Python 3.13.6 environment:

```sh
/Users/wenyan/.pyenv/shims/python3 drafts/ch44/build.py --render
/Users/wenyan/.pyenv/shims/python3 drafts/ch44/build.py --check
/Users/wenyan/.pyenv/shims/python3 -m pytest -q tests/test_ch44_reference.py -o addopts=''
```

Requires XeLaTeX/latexmk, makeindex, Poppler, Pillow and the declared fonts.
The builder follows Chapter 35: it extracts whole tested functions, generates
results/tables, strictly checks compilation and renders color/grayscale sheets.
It never generates prose. Figures are original editable TikZ with semantic TXT.
Only assigned standalone tests/builds were run; cumulative integration and
independent review belong to the final integrator.

Evidence: deterministic serial teaching models, assigned timings and analytic
payloads. Chapter 46 also checks test-local data-only snapshot continuation with
actual Chapter 31 and Chapter 35/23 models. No remote systems, services,
credentials, real tools, device kernels or real backend timings are used.
