# Chapter 3 progress: illustrated reasoning and executable checks

9 September 2026. **Working draft, not publication acceptance.**

**Differentiation, optimization and tensor programs** now has an expanded [manuscript](drafts/ch03/manuscript.md) of approximately 3352 whitespace-delimited words, eight original editable SVG figures with semantic TXT companions, and twelve exercises with worked reasoning. The 12-figure storyboard has four mechanisms still awaiting artwork. All eight newly produced figures across the two books were rendered and visually inspected; a chart annotation was moved off its data line and reverse-gradient arrows were made explicit. This is figure review, not PDF page review.

The new material derives shared-bias accumulation component by component, explains finite-difference scale and stable cross entropy (including tied maxima), and proves the count-weighted microbatch identity. Tests cover each new numerical artifact, tied-logit gradients, both accumulation-loop implementations, and a batch-centering counterexample where partitioning changes the function.

Numerical charts and the decision trace come from the executable results. Their TXT companions include the underlying values, with units and boundaries kept explicit. No ASCII box art or generated bitmap substitutes for the editable scientific figures.

## Verification

The full suite passes **206 tests**, including **35 working-draft tests**, the publication build in an isolated temporary copy, and source/PDF preservation checks. The accepted Chapters 1–2 source hashes and original published PDF bytes remain unchanged. No acceptance gate was weakened.

The code, prose, figures and tests are a local Chapter 3 development checkpoint. Publication metadata still activates exactly two chapters. No new PDF, moving animation, laboratory experiment, trained-model result or independent review is claimed.

## Remaining production work

Complete the last four storyboard mechanisms, unresolved source/proof work described at the end of the manuscript, and the LaTeX references, glossary and index. Scientific and mathematical review plus every-page inspection must precede a new cumulative release and acceptance record. Older editions, branches and PDFs remain preserved.
