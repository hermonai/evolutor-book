# Chapter 21: Strands, complements and dual-state hypotheses

Standalone authored-LaTeX review candidate; earlier sources and accepted
publications are preserved.

Derive reverse-complement actions, shared dual-state lifts, constrained
readouts, causality limits, offline chunk equivalence and shared-parameter
gradients. Distinguish algebraic symmetry from genomic capability.

Five original editable vector figures have semantic TXT companions. Twelve
worked exercises connect proofs, implementations and counterexamples.
Computed tables and plot coordinates come from reference.py. Primary-source
access boundaries are recorded in sources.tex; these are teaching references,
not laboratory measurements or trained genomic results.

## Reproduce

Run at the repository root in the project Python environment:

~~~sh
python3 drafts/ch21/build.py --assets-only
python3 -m pytest tests/test_ch21_reference.py
python3 drafts/ch21/build.py --render
python3 drafts/ch21/build.py --check
~~~

Dependencies: PyTorch, pytest, Pillow, XeLaTeX/latexmk and Poppler.
Compiler output stays in build/ch21/.
Readable PDF: output/pdf/evolutor-ch21-review.pdf.
Author review manifest: artifacts/deep/ch21-review.json.
PDFs and page renders are generated and ignored by Git.

Independent specialist review, reader feedback and cumulative integration
remain open. Author review does not certify industrial readiness.

