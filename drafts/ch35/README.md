# Chapter 35 — Hermon DNA prefill, decode and KV state

Implement cache continuation through the actual Chapter 23 Hermon stack,
including learned absolute positions, multi-head normalized projections,
residuals, feed-forward sublayers and the final head. Derive the offset causal
mask, token/layer parity theorem, linear payload and cumulative copying cost.

Tests compare the independent original full model, every fixture split and
chunk composition, per-layer QKV hooks, SDPA mask semantics, malformed state
and a resealed forgery. The reference is unpadded canonical ACGT CPU float64
inference: no rotary replacement, paging, GQA conversion, quantized KV,
FlashAttention backend, hostile-process security or genomic capability claim.

## Reproduce

From the repository root (Python 3.13.6, PyTorch 2.10 CPU float64):
```sh
export OMP_NUM_THREADS=1
python3 drafts/ch35/build.py --render
python3 drafts/ch35/build.py --check
python3 -m pytest -q tests/test_ch35_reference.py -o addopts=''
python3 scripts/build-convergence.py --through 35
```
Use XeLaTeX/latexmk, makeindex, Poppler and the project's declared fonts.
Do not run PDF builds concurrently with preservation tests.

`manuscript.tex` is authored prose; `reference.py` is executable evidence.
`build.py` extracts whole tested functions and generates tables/results; it
does not generate the chapter prose. Six original TikZ plates have semantic
TXT companions under `figures/`. Rendered review pages are disposable under
`tmp/pdfs/`; readable PDFs are generated under `output/pdf/`.

Twenty worked exercises connect derivations, implementation, counterexamples
and systems-design consequences. Local review and source hashes are recorded
under `research/integration/ch35/`. No independent acceptance is implied.
