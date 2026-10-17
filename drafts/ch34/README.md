# Chapter 34 — DOGMA batching and state-native kernels

Lift the actual Chapter 31 recurrence across independent requests, retaining
Chapter 32 ownership/generation/version pins and Chapter 33 restored branches.
Derive permutation equivalence, inactive identity, local clocks, error/margin
bounds and payload/staging/fusion accounting. Cancellation rejects one lane
without preventing a sibling commit; pin acknowledgement gates reclamation.

This is a serialized inference reference, not a production GPU kernel, atomic
batch transaction, integrated network-output shell or genomic benchmark.

## Reproduce

From the repository root (Python 3.13.6, PyTorch 2.10 CPU float64):
```sh
export OMP_NUM_THREADS=1
python3 drafts/ch34/build.py --render
python3 drafts/ch34/build.py --check
python3 -m pytest -q tests/test_ch34_reference.py -o addopts=''
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
under `research/integration/ch34/`. No independent acceptance is implied.
