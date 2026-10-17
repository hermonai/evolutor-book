# Current manuscript and repository guide

Updated 17 October 2026. Active content reaches Chapter 33 of the 52-chapter
plan. Locally reviewed candidates are not an accepted publication edition.

## Start here

- [Chapter 33 — DOGMA checkpoints, branching and prefix state](drafts/ch33/README.md)

- [Chapter 31 — DOGMA state construction and execution](drafts/ch31/README.md)
- [Chapter 32 — DOGMA state pools and memory ownership](drafts/ch32/README.md)
- [Editorial architecture and release gates](EDITORIAL_ARCHITECTURE.md)
- [Package convergence matrix](research/integration/chapter-convergence-matrix.md)
- [Continuous PDF hash, review scope and open release gates](research/integration/continuous-through33-review.json)
- [Textbook standard](TEXTBOOK_STANDARD.md) and [chapter standard](CHAPTER_STANDARD.md)

## One manuscript, explicit stages

| Material | Active location | Status |
|---|---|---|
| Opening Chapters 1–3 | tex/ and TEXTBOOK_REVISION.md | Textbook review candidate |
| Chapters 4–21 | drafts/ch04/ through drafts/ch21/ | Authored standalone candidates |
| Chapters 22–33 | drafts/ch22/ through drafts/ch33/ | Source-bound locally reviewed candidates |
| Continuous Chapters 1–33 | output/pdf/evolutor-convergence.pdf | Authored-source cumulative review candidate |
| Chapters 34–52 | Inventoried source ZIPs | Staged, not silently included |
| Accepted Chapters 1–2 | book/book.json and acceptance records | Frozen, not superseded acceptance |
| Historical editions | Existing sources and preservation tests | Archives, not parallel authoring |

Every explicitly requested evolutor-ch30-r01.zip through evolutor-ch52-r01.zip
is inventoried with digest, mapping and separate gates. Chapters 30–33 have
been used and semantically integrated. Following Chapter 34's continuity note
was inspected to check the batching handoff, not silently integrated.
Preserved incoming metadata is provenance, not local validation.

## Build and verify

Use Python 3.13.6 at /Users/wenyan/.pyenv/versions/3.13.6/bin/python3 and
OMP_NUM_THREADS=1 for the declared CPU PyTorch references.

- Chapter builders: drafts/chNN/build.py --render; --check verifies computed assets.
- Continuous build: scripts/build-convergence.py --through 33 --refresh-assets.
- Scoped cumulative render review: scripts/review-convergence.py --pages 1-5,385-417.
- Regression: python -m pytest -q -o addopts=''.
- Do not build PDFs concurrently with preservation tests in the same repository.

The continuous builder assembles authored LaTeX with reconciled bibliography,
global glossary, index and chapter references. The pedagogical acknowledgment
appears once in front matter. A successful build is not cumulative visual review.

## Folder and cleanup policy

Authored drafts/, tex/, figures/, examples/ and tests/ are source, not cache.
research/integration/ holds durable provenance and local evidence.
output/pdf/ contains readable candidates and preserved editions; inspect
provenance before removal. build/ contains generated tables, listings, compiler
outputs and logs. tmp/pdfs/ contains regenerable visual-review pages.

On 27 September 2026, the books' legacy build trees (1,148 files, about 102 MB
combined) were moved to dated macOS Trash with a recovery receipt. Authored
sources, accepted PDFs and historical editions remained unchanged. Resolve
exact targets and archive before future cleanup; never blanket-delete the repo.

## Next: Chapter 34 batching and state-native kernels

Chapter 31 binds native inference to model content and legal token position.
Chapter 32 adds bounded storage, caller ownership, allocation generations,
in-flight pinning and deferred reclamation. That milestone's regression passed
1,212 tests.
Those standalone PDFs are 15 and 14 pages, each with six vector/TXT plates
and twenty worked exercises. Chapter 33 now adds a 17-page checkpoint chapter,
six original vector/TXT mechanisms, twenty worked exercises and 71 new tests.
Full regression: 1,283 passed. Native prefix/suffix parity, exact context/schema
validation, fresh allocation, bounded LRU, rehashed forgery and forced lookup
collision controls are checked against actual preceding interfaces.

Chapter 34 must preserve fresh ownership, exact per-request token positions
and independent-copy semantics under gather, batched transition and scatter.
Inactive lanes must not advance; membership changes need declared boundaries.
Scalar inference snapshots do not preserve autograd; integrity does not confer
authorization. Keep DOGMA non-Transformer and HermonDNA Transformer identities
distinct. No hardware speed, genomic capability or production safety is implied.

Cumulative editorial/visual QA, independent scientific and reader review remain
open. Chapter acceptance and full-book convergence remain false.
BOOK_PLAN.md is the generated frozen acceptance snapshot, not a progress counter.
