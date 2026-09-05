# Research-reset execution report

Date: 2026-09-05. Milestone: first-principles redesign and compiling publication shell, not completed books.

## Repository identity

- Starting public commit: `3895e94ff206a537a846a88966a27435b14f6ae2`.
- Historical snapshot including unfinished earlier work: `9df0d006e10e56cd836a4b84400009dab3cbf4f2`.
- Working/publication branch: `astra-rewrite`; archival branch: `archive/pre-reboot-20260905`.
- Final reset commit: `e439334ad525bf0291170ec48004aa40b3b661ff`. This report records that fixed historical milestone; later chapter work is reported in CHAPTER_REPORT.md.
- Public repository: [hermonai/evolutor-book](https://github.com/hermonai/evolutor-book/tree/astra-rewrite). The default branch remains main; no force-push is used.

## Delivered

New thesis and audience in ASTRA_REDESIGN.md; 29-chapter candidate TOC; publication plan; reference-stack design; source register and topic maps; chapter/graph/code/claim audits; terminology and notation contracts; five new canonical TXT graphs with generated accessible SVGs; LaTeX shell with bibliography, cross-references, theorem environments, Unicode/code rendering, glossary and index; automated archive/link/graph/build checks.

Every old chapter, diagram and research file was moved from the active edition into historical/pre-reboot without content edits. Existing implementation code remains at its original path for regression checks; old README, plan and roadmap remain in Git. Historical source references are not endorsements. No third-party papers, attached screenshots or local infrastructure instructions were copied into the public edition.

## Research and conclusions

Biological regulation, development and adaptation motivate questions about adaptive computation. Evolutor will earn its abstractions by distinguishing them from routing, program synthesis, memory systems and structural learning, then testing whether the differences matter.

The source register records primary research and authoritative terminology, access date and reading depth. This is a scoping review, **not a complete systematic review or full-text proof/experimental audit**. All three prior chapters and every historical graph received disposition screening. Scientific correctness of old diagrams was not recertified. Source-module inspection found limitations documented in REFERENCE_IMPLEMENTATION.md. The GCS tuple and architecture names no longer define the thesis. The historical theorem suite remains gated, with explicit counterexamples to overbroad cost and trace-union inferences.

## Verification

- Regression and reboot-contract tests: **20 passed** (snapshot baseline: 16). Tests verify active relative links, graph structure and generated SVG presence, malformed-edge rejection, the empty chapter manifest, and byte-for-byte archival fidelity for every old book/research file.
- LaTeX: **9 pages, PDF 1.7**, built with XeLaTeX / TeX Live 2025 and latexmk 4.86a. Final build/log checks show no warnings, missing glyphs, undefined references/citations, overfull boxes or errors. Bibliography, index and glossary generated successfully.
- Visual QA: rendered all nine final pages with Poppler; inspected complete contact sheets and full-size figure/math pages. Rendered and reviewed all five generated SVG maps. No clipping or overlapping labels observed. The PDF skill drove this render-and-review step.
- Environment: macOS 26.6.2 arm64; Python 3.13.6; PyTorch 2.10.0; pytest 9.0.2; rsvg-convert 2.61.1. Run with a Python environment containing these dependencies; the system Python may lack PyTorch.
- Accessibility: readable text and vector diagrams plus canonical text alternatives are provided. The shell is **not a tagged PDF/UA-certified edition**; full accessible-publication review remains a release gate.
- Credential guard and scoped token/private-key-pattern screening passed. No source repository outside these two books was changed.
- Build artifacts are local under output/pdf; source and SVG are published. No final-release tag or full-book completion claim is made.

## Cross-book decisions

Shared: rigorous source/claim records, reversible history, PyTorch reference semantics where useful, Unicode TXT plus generated SVG, LaTeX publication machinery.

Different: DNA Computing explains physical molecular information processing; Evolutor tests candidate abstractions against established CS/ML methods. Neither needs the other to prove its thesis. Molecular analogy does not transfer biological evidence into an AI claim.

DOGMA and Hermon DNA: unassigned research names, no automatic backbone selection or renaming. GCS: candidate model with proof obligations, not inherited authority. PyTorch: initial reference laboratory for training/inference; a new framework is deferred until a measured limitation justifies it. AGI: unverified research question, not a result.

## Open work and recommended next request

Complete chapter-specific source/method reviews, resolve pending formal-model variants and historical proof/benchmark artifacts, then build the books sequentially. No new training or wet-lab experiment occurred in this milestone. The attached visual references do not substitute for biological figure review.

Suggested next request: “Develop the first chapter of both redesigned books. Read the redesign and audit files; research its claims from full primary sources, then write the chapter with a worked example, tests, source-reviewed figures and exercises. Render and review both PDFs before committing. Keep speculative and unmeasured claims explicitly labeled.”
