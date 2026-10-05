# Chapter 19: DOGMA regulation and selective transformations

Standalone authored-LaTeX review candidate; earlier accepted editions remain unchanged.

Input-conditioned state updates, convexity proofs, causal chunking, analytic gradients, state-feedback counterexamples, non-identifiable gates, and a falsifiable genomic evaluation contract.

Five original editable TikZ figures have semantic TXT companions. Twelve exercises
include worked answers. Tables, plots and code listings come from reference.py;
sources.tex records primary-source access and separates published research from
the proposed teaching models.

## Reproduce

Run from the repository root with the project Python environment:

```sh
python3 drafts/ch19/build.py --assets-only
python3 -m pytest tests/test_ch19_reference.py
python3 drafts/ch19/build.py --render
python3 drafts/ch19/build.py --check
```

Dependencies: PyTorch, pytest, Pillow, XeLaTeX/latexmk and Poppler.
The chapter does not require SciPy. Build intermediates stay in build/ch19/.
The readable PDF is output/pdf/evolutor-ch19-review.pdf.
PDFs and page previews are generated and ignored by Git; authored sources,
numerical results, tests and the author-review manifest are versioned.

The review record is artifacts/deep/ch19-review.json. Technical and visual
author review is not independent scientific acceptance. Specialist review,
reader feedback and cumulative integration remain open. Next topic: DOGMA memory and multiscale processing.

