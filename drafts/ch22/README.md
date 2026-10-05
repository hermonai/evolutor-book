# Chapter 22: DOGMA reference model and falsifiable research program

Local convergence revision, 6 October 2026. Original r01 provenance is preserved
under research/integration/ch22/incoming; imported QA claims are not local QA.

The learned-locus model is an explicit additional reference variant, not a rename
of Chapters 18 or 20. It separates causal prefix processing from an offline
reverse-complement-invariant classifier. Continuation carries both fast state and
memory; shape/dtype/device/finiteness checks, empty-chunk identity, request isolation,
state/input/parameter gradients and a read-path intervention are tested.

Six editable TikZ figures with semantic TXT companions explain the gate equation,
causal boundary, paired offline access, old-memory reads/new-memory writes,
falsification controls and a numeric convex write. Sixteen worked exercises extend
the derivations. Literal method listings are extracted from the complete runnable
reference.py module, which also contains constructors and supporting helpers.

A three-seed CPU motif pilot includes GRU, MLP, local CNN, exact label oracle and
independent random-label control. Parameter and strand-pass budgets differ;
it is NOT a superiority benchmark. The independent uniform-target cross-entropy
floor applies in population expectation, not to every finite held-out sample.

```sh
OMP_NUM_THREADS=1 python3 -m pytest tests/test_ch22_reference.py
python3 drafts/ch22/build.py --assets-only
python3 drafts/ch22/build.py --render
python3 drafts/ch22/build.py --check
```

Requirements: Python 3.10+, PyTorch, pytest, Pillow, XeLaTeX/latexmk, Poppler and
existing fonts. Building recomputes the pilot with one CPU thread and records the
PyTorch version. No accelerator throughput or trained genomic capability is claimed.

Output: output/pdf/evolutor-ch22-review.pdf. Standalone local review candidate;
full-book integration and independent review are separate gates. Chapter 23 starts
the separate Hermon DNA Transformer branch.
