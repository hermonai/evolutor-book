# Chapter 20: Structured memory, locality and timescales

Standalone authored-LaTeX review candidate. Earlier sources, review records and
accepted publications remain unchanged.

Exact local storage versus compressed state; exponential kernels and timescale
sensitivities; multi-rate block clocks; complete chunk-state ownership; aliasing
and finite-bit capacity; research comparisons and a genomic evaluation contract.

Five original editable vector figures have semantic TXT companions. Twelve
worked exercises connect proofs, numerical implementation and failure cases.
Results and plot coordinates are computed from reference.py; source-access
depth is recorded in sources.tex.

## Reproduce

Run at the repository root using the project Python environment:

```sh
python3 drafts/ch20/build.py --assets-only
python3 -m pytest tests/test_ch20_reference.py
python3 drafts/ch20/build.py --render
python3 drafts/ch20/build.py --check
```

Dependencies: PyTorch, pytest, Pillow, XeLaTeX/latexmk and Poppler.
Only build/ch20/ receives this chapter's compiler output.
Readable PDF: output/pdf/evolutor-ch20-review.pdf.
Author review manifest: artifacts/deep/ch20-review.json.
The PDF and page renders are generated and ignored by Git.

Independent specialist review, reader feedback and cumulative integration
remain open. The examples do not establish new laboratory results, trained
genomic capability or industrial deployment readiness.
