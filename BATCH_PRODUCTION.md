# Evolutor: complete the supplied chapter packages in substantial batches

User request: use the ChatGPT-generated evolutor-ch33-r01.zip through
evolutor-ch52-r01.zip as much as possible, preserve quality, and split the
remaining production across multiple conversations rather than stopping at
one or two chapters. Recorded 17 October 2026.

## Starting point and package coverage

Baseline commit: 698f309 on integration/evolutor-ch22-52.
Chapters 1–35 are in the 443-page continuous review candidate. The latest
baseline full regression passed 1,416 tests. Chapters 33–35 already used their
r01 packages; their source-verification and technical-audit records explain
the extensions and compatibility corrections. Do not replace them blindly.

All twenty supplied archives are present in /Users/wenyan/Downloads.
All 771 declared file hashes have been reverified against exact archive bytes,
and archive digests agree with the existing inventory. No path traversal,
absolute entry names or symlink entries were found. This is integrity and
inventory verification, not semantic or independent scientific acceptance.
See [package-reuse-audit.json](research/integration/package-reuse-audit.json).

## Four authoring conversations, one final integration owner

| Batch | Chapters | Main subject | Authoring boundary |
|---|---|---|---|
| A | 36–38 | Paged KV, scheduling/precision, speculative decoding/attention | Finish the attention-native engine layer |
| B | 39–43 | Heterogeneous runtime, memory, compiler, database comparison, governance | Build the Evolutor systems layer |
| C | 44–47 | Packaging, security, distributed serving, profiling/backends | Build industrial engineering contracts |
| D | 48–52 | Genomics, persistent agents, adaptation, capability limits, synthesis | Complete applications and research synthesis |

Each author owns only its chapter directories, matching chapter tests and
chapter-local research records. The original conversation owns global
navigation, the convergence matrix/inventory, cumulative build, whole-repository
regression and the final integration commit. New conversations are ordinary
user-visible chats; they are not independent scientific reviewers.

Parallel authoring must not mean concurrent edits to shared status files.
A batch can author material against a documented earlier contract. If an
executable example needs another unfinished batch, identify that dependency
and defer the integration test until the real interface is stable. Do not
invent a passing integration, import partially changing files, or replace
a missing implementation with a silently detached demo.

## Allowed write scope for a chapter author

For each assigned chapter NN:

- drafts/chNN/: authored LaTeX, reference implementation, generated numerical
  fixture, storyboard, native vector figures plus semantic TXT, standalone
  review wrapper/builder and README.
- tests/test_chNN_reference.py and, if needed, a uniquely named batch test
  whose inputs are confined to completed owned sources.
- research/integration/chNN/: incoming text-only provenance, source access,
  package-adoption map, technical review, source-bound local review and handoff.
- Generated build/chNN/, tmp/pdfs/chNN-review/ and
  output/pdf/evolutor-chNN-review.pdf.

Do not edit README.md, CURRENT_MANUSCRIPT.md, CHAPTER_STRUCTURE.md,
chapter-structure.json, EDITORIAL_ARCHITECTURE.md, BOOK_PLAN.md, book/book.json,
shared tex/, global scripts or research/integration/{package-inventory.json,
chapter-convergence-matrix.md,integration-decisions.md}. Do not run the
cumulative builder or whole-repository preservation tests while other authors
are compiling. Run chapter-specific tests and standalone builds only.
Do not commit, push, reset, clean or stage another conversation's work.
Do not modify DNA Computing, Inside LLM Engine, the actual Evolutor runtime
repository, or any finance projects.

Each author records completion in
research/integration/batches/<batch-id>-handoff.md, which is owned by that batch.
Machine-readable dispatch metadata lives in
research/integration/production-batches.json and is coordinator-owned.

## Reuse policy: preserve the supplied content, upgrade the evidence

Read the complete incoming manuscript, reference, tests, storyboard, figure
sources/TXT and source ledger for every assigned chapter. Verify the archive
and manifest against package-reuse-audit.json before adopting anything.
Packaged caches, compiled PYC, stale results and QA labels are not trusted
executables or local validation.

Reuse correct explanations, derivations, worked scenarios, examples, exercise
questions, terminology and source leads. Reorganize excessive one-paragraph
sections into sustained arguments. Extend rather than discard good material.
Do not copy stale chapter-history claims, unsupported novelty/performance/
capability assertions or incompatible toy interfaces as if they were integrated.

A chapter-local package-adoption.md must map every incoming section to a
retained, expanded, merged, relocated or omitted destination with a concrete
reason. Record original file hash and the location in the new chapter.
Do not use a fabricated reuse percentage: conceptual coverage, verbatim reuse
and executable reuse are different quantities.

## Quality contract

Read CHAPTER_STANDARD.md, TEXTBOOK_STANDARD.md, CHAPTER_STRUCTURE.md,
EDITORIAL_ARCHITECTURE.md and the immediately relevant actual preceding
sources. Original derive–implement–test pedagogy is the reference, not copied
Raschka wording/artwork. Keep the shared general acknowledgment in front matter
once; chapter notes should concern their specific evidence and limitations.

Use deep but straightforward explanations, defined units/tensor shapes,
worked arithmetic, explicit premises, proofs where material, executable source
listings, independent oracles and negative controls. No word-count quota or
fixed figure count replaces explanatory substance. Incoming drafts are often
short skeletons; merely copying them does not finish the chapter.

Make professional textbook mechanism illustrations: biology/biochemistry
notation for actual biological mechanisms; state/tensor/memory/algorithm
graphics for systems. Editable native TikZ with semantic TXT companions;
no ASCII box art, decorative DNA or screenshots of equations. Read and use
the PDF skill for authoring, render every standalone page in color and grayscale,
and correct typography, caption, figure-label, code and proof pagination.

Keep DOGMA non-Transformer; Hermon DNA Transformer; Evolutor the broader
theory/compiler/runtime direction. Chapter 31 is a restricted diagonal
teaching model, not full DOGMA. Chapter 35 uses the real Chapter 23
learned-absolute-position Transformer. Never silently substitute rotary
positions or a detached one-head oracle for that implemented architecture.

Verify niche/current technical claims with primary sources and record exact
access depth. An abstract is not full-paper inspection. Model arithmetic,
synthetic fixtures, CPU timings and actual hardware measurements must be
distinguished. Biological or AGI claims need falsifiable protocols and limits.
Security chapter threat models and reference checks are not production security
certification. Local author review is not independent specialist/reader review.

For each chapter: reproduce generated values, run its tests, strict compile,
inspect every PDF page color/grayscale, and bind local review to actual
source/PDF hashes. Preserve frozen opening chapters and accepted artifacts.

## Final convergence, after all four batches settle

The integration owner checks each adoption map and dependency handoff, reruns
cross-chapter examples against real stable interfaces, validates bibliography/
notation/labels and builds one continuous candidate through Chapter 52.
It then runs the full regression suite with no simultaneous PDF builds,
reviews the new cumulative pages/front and back matter, records precise
review scope and hashes, updates navigation and README, and makes a scoped
local integration commit. Publishing requires explicit user authorization.

Authoring, tested standalone, cumulative integration, local review and
publication acceptance remain separate stages. The presence of all ZIPs or
all chapter source folders does not close the final gates.
