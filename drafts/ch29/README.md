# Chapter 29 — Benchmark design and comparative evidence

Active authored-LaTeX integration candidate; earlier accepted editions unchanged.

Strict scoring and budget schemas; exact rational paired-bootstrap convolution and sign test; crossed seed/group resampling; pseudoreplication, task-choice and supplied-mechanism controls.

Six original editable TikZ plates with semantic TXT companions, five complete tested function listings, twenty worked exercises and 45 chapter tests. Computed values are model outputs, not physical measurements or neural training benchmarks.

## Reproduce

Use Python 3.13.6 (PyTorch Float64 required for DNA reference). From this repository:

```sh
OMP_NUM_THREADS=1 /Users/wenyan/.pyenv/versions/3.13.6/bin/python3 -m pytest tests/test_ch29_reference.py -q -o addopts=''
OMP_NUM_THREADS=1 /Users/wenyan/.pyenv/versions/3.13.6/bin/python3 drafts/ch29/build.py --render
OMP_NUM_THREADS=1 /Users/wenyan/.pyenv/versions/3.13.6/bin/python3 drafts/ch29/build.py --check
```

Full manuscript: scripts/build-convergence.py --through 29 --refresh-assets.
Source-bound local author review and distinct acceptance gates are recorded in research/integration/ch29. Whole-book visual/editorial and independent specialist/reader review remain open. No publication acceptance is inferred from compilation or passing tests.
