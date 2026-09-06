# Chapter 1 production report: Evolutor

Date: 6 September 2026. Status: internally reviewed development chapter; no independent expert certification or learner study.

## Identity and scope

Starting commit: 252def4c94f256a731917aa7e8a210ab7dea483b.
Branch: astra-undergraduate-rewrite.
Publication commit: the commit containing this report (retrieve with git log -1 --format=%H -- CHAPTER_1_REPORT.md); its exact hash is supplied in the final delivery. This avoids a self-referential hash inside its own commit.

Approved title: **Programs, genomes and the question of Evolutor**.
Canonical source: [tex/undergraduate/ch01.tex](tex/undergraduate/ch01.tex).
The title agreed across the approved redesign files. No old chapter prose was copied; earlier tex/chapters/ch01.tex and ch02.tex remain byte-identical. Only this chapter is active.

## Section sequence

1. Begin with a program that chooses
2. A boundary makes the rule precise
3. Optional: read the exact program
4. A biological reminder: stored DNA is not the whole story
5. What an analogy can and cannot carry
6. Evolutor begins as a research question
7. A route toward sharper questions
8. Practice: trace, compare, challenge
9. Answers and the question to keep

## Learning objectives and prerequisite handling

Trace a fixed conditional program including equality; separate input, context and instructions; recall a gene/expression distinction; distinguish biological gene from proposed software unit; turn an analogy into a falsifiable comparison. The opening supplies a short local reminder because Book I imports DNAU-03, DNAU-09 and DNAU-32 are still planned. Learned models remain in EVOU-03 and are not needed here.

The paper exercise remains compulsory; the tiny code section is optional. This explicitly refines the original no-new-code planning note without changing the entry contract.

## Terms, figures and executable material

29 retained glossary definitions: program; input; output; execution; rule; computation; threshold; condition; trace; context; Python; function; cell; molecule; DNA; genome; RNA; protein; gene; gene expression; gene regulation; analogy; computational gene; research program; hypothesis; baseline; evidence; representation; information.

The [terminology ledger](research/undergraduate-ch01-terminology.md) records first sentence/heading preview, definition sentence, section, picture or worked example, glossary key and related term. It includes early title/objective previews instead of pretending every name first appears at its formal definition.

- EVOU-01-F1: A stored rule can choose.
- EVOU-01-F2: The boundary belongs to the rule.
- EVOU-01-F3: Same DNA, different expression.
- EVOU-01-F4: An analogy is a question, not an identity.
- EVOU-01-F5: How a proposal earns evidence.
- EVOU-01-F6: The route from programs to research.

Each figure has original editable SVG, a Unicode TXT semantic companion, title/description metadata, scientific risk and evidence record. The generator is scripts/build_undergraduate.py; sources are under book/figures/undergraduate and book/diagrams/undergraduate. No copied textbook image, decorative raster illustration, ASCII box art or exported animation is included.

New code: examples/undergraduate/ch01_rule.py (heater, four lines). The listing is included directly with VerbatimInput. The generated trace and artifacts/undergraduate/ch01-results.json run that exact function. Independent hand expectations test 18, 20, 22 and 19, plus strict near-boundary cases. There are eight exercises and eight answer notes.

## Verification

Full-suite result: 62 passed in 6.15 seconds (Python 3.13.6; pytest with real PDF integration).
Baseline rerun before production: 42 passing tests.
New Chapter 1 tests: 16 cases covering exact outputs, repeatability/boundary behavior, generated assets, six editable SVG/TXT pairs, invalid storyboard rejection, glossary/reference closure, source-linked code and real LaTeX/PDF integration.
Four additional taxonomy tests reject either family reversal and check stable IDs, prerequisite paths and required active documents.

The original architecture-only blocking test was legitimately replaced by a stricter new-edition gate: only the new Chapter 1 may build; empty, unreviewed or preserved-edition manifests are rejected. Existing computational examples and historical preservation regressions remain.

Publication: 17 A4 PDF pages, of which nine are the chapter (printed pages 1–9). There are three physical front-matter pages and five back-matter pages. All pages were rendered and inspected; final minor text corrections were rebuilt and rechecked. No overfull/underfull boxes, missing glyphs or undefined references remain in the checked build. PDFs are not tagged; no PDF/UA claim is made.

## Actual page and figure review findings

- Added a visible tray boundary to the counter storyboard to separate the counted collection from waiting objects.
- Repainted roadmap connectors after panels so their arrowheads remain visible.
- Kept figures and captions at authored paragraph boundaries after a biology float split a sentence.
- Prevented the Evolutor chapter title from hyphenating its project name.
- Made bibliography URLs ragged-right, eliminating meaningful spacing warnings.
- Generated reciprocal glossary links without duplicate punctuation or recursive location records.
- Corrected sentence-initial term presentation and exact lowercase returned words.

All six figures were checked independently of prose for identity, arrow meaning, labeling, reading size and grayscale interpretation. The biology illustrations explicitly state schematic level and missing machinery; software uses data flow, not molecular shapes. Front/back matter deliberately has more whitespace than teaching pages.

## Internal beginner and general-reader review

These are author-agent role perspectives, not actual participants.

The beginner review flagged RNA/protein appearing inside the gene definition before explanation; the reminder now defines them first. The general-reader review checked whether a fixed program was being portrayed as unable to respond; the equality trace and ordinary-program comparison make its abilities explicit. Code output is a word, not a real actuator command. No attention, tensor or genomic-state notation enters Chapter 1.

## Internal specialist-perspective review

| Perspective | Question and disposition |
|---|---|
| ML researcher | Does the opening depend on unintroduced learned-model internals? No; those remain in Chapter 3 onward. No training or advantage is reported. |
| Systems engineer | Is toy output a device action, or shared state implicit? It is a returned word; no real controller or cross-request system is claimed. |
| Computational biologist | Does gene expression mean DNA changes or acts alone? Both implications are explicitly excluded; low/high is conceptual, not data. |
| AGI skeptic | Is resemblance promoted to capability? The research box states no benchmark or general-intelligence result. A comparison can lose. |
| Software-architecture instructor | Is a computational gene a molecule or an implementation? It is a provisional software label awaiting semantics. The active future taxonomy separates models, engines and orchestration. |

## Claims and limits

Eight new ledger rows EVOU-CL01 through EVOU-CL08 cover the exact toy, input-dependent conventional behavior, biological terms, RNA/protein, expression, analogy limits, research positioning and corrected target taxonomy.
See [claims ledger](research/claims-ledger.md) and [source register](research/undergraduate-ch01-sources.md). No scientific experiment was performed.

Remaining weaknesses: actual learner testing and independent subject review are still needed; chemical pictures are intentionally introductory; short exact tests do not validate arbitrary inputs; PDF accessibility structure is incomplete; index coverage emphasizes substantive definitions rather than a final exhaustive book-wide index. Later chapter links refer to plans, not completed text.

## Corrected future architecture amendment

**DOGMA = non-Transformer DNA-native architecture + DOGMA Engine.**
**Hermon DNA = Transformer-based DNA architecture + Hermon DNA Engine.**
**Evolutor = genomic computation theory/planning/research and eventual runtime above both.**

The curriculum now contains 61 units in 14 parts. The original 40 IDs remain stable and 21 units are added in prerequisite order. Model/primitives, training-parity and inference-engine paths are separate. No new architecture or engine chapter is drafted. Historical naming is retained and actual artifacts are not reclassified by intent.

Active taxonomy-enforcement files changed: pedagogy/curriculum.json; scripts/build_pedagogy.py; BOOK_PLAN.md; PEDAGOGICAL_REDESIGN.md; COURSE_MAP.md; PREREQUISITE_GRAPH.md; VISUAL_STORYBOARD.md; ROADMAP.md; CONCEPT_MAPS.md; LEARNING_PROGRESSION.md; TERMINOLOGY_AUDIT.md; PREVIOUS_EDITION_AUDIT.md; pedagogy/figure-inventory.json; pedagogy/animation-inventory.json; README.md; research/architecture-taxonomy.md; research/claims-ledger.md; tests/test_architecture_taxonomy.py; tests/test_pedagogical_architecture.py. The Chapter 1 roadmap figure now uses the revised parts rather than obsolete chapter ranges.

## Cross-book conclusion and next scope

See [the shared comparison](CROSS_BOOK_CHAPTER_1_REVIEW.md) and [the production standard](CHAPTER_STANDARD.md), written after the real production/review work.

Next: EVOU-02 — Programs that choose and remember, with a local bridge for still-planned DNAU-03/DNAU-04.
No next chapter was drafted in this milestone.
