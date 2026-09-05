# Evolutor

## Genomic Computation as a Testable Research Program

Publication reboot • edition 2 development • branch `astra-rewrite`.

Biological regulation, development and adaptation motivate questions about adaptive computation. Evolutor will earn its abstractions by distinguishing them from routing, program synthesis, memory systems and structural learning, then testing whether the differences matter.

**Chapter 1 is now drafted and executable**, not a completed book. Read [What would genomic computation add?](tex/chapters/ch01.tex), [the chapter report](CHAPTER_REPORT.md), and [the generated example records](book/results/ch01.json). Build the PDF with `make pdf check-pdf`.

The new edition lives on `astra-rewrite`; the earlier public edition remains on `main`. For the longer plan, see [the redesign](ASTRA_REDESIGN.md), [the candidate contents](BOOK_PLAN.md), and [the preserved reset milestone](RESET_REPORT.md).

- [Research source register](research/primary-sources.md)
- [Publication plan and build commands](PUBLICATION_PLAN.md)
- [Reference implementation design](REFERENCE_IMPLEMENTATION.md)
- [Diagram standard](book/GRAPH_STANDARD.md)
- [Historical edition and audit](historical/README.md)

The old manuscript and research notes are quarantined under `historical/pre-reboot/` and excluded from the publication build. Existing code remains runnable for regression and audit, not as the definition of the new theory. The earlier public edition remains on `main`; no force-push or automatic default-branch change is used.

No authorship or licensing change has been made. Public visibility does not grant a new reuse license. Third-party papers and supplied reference images are not redistributed.
