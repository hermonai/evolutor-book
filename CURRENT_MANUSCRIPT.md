# Current manuscript and repository guide

Updated 17 October 2026. Active authored content reaches Chapter 35 of 52.
Locally reviewed candidates are not an accepted publication edition.

## Start here

- [Complete 52-chapter structure, parts and prerequisites](CHAPTER_STRUCTURE.md)
- [Chapter 34 — DOGMA batching and state-native kernels](drafts/ch34/README.md)
- [Chapter 35 — Hermon DNA prefill, decode and KV state](drafts/ch35/README.md)
- [Editorial architecture and release gates](EDITORIAL_ARCHITECTURE.md)
- [Package convergence matrix](research/integration/chapter-convergence-matrix.md)
- [Continuous PDF hash and actual review scope](research/integration/continuous-through35-review.json)
- [Textbook standard](TEXTBOOK_STANDARD.md) and [chapter standard](CHAPTER_STANDARD.md)
- [Four-batch production and ownership rules](BATCH_PRODUCTION.md)

## One manuscript, explicit stages

| Material | Active location | Status |
|---|---|---|
| Opening Chapters 1–3 | tex/ and TEXTBOOK_REVISION.md | Preserved opening review sources |
| Chapters 4–21 | drafts/ch04/ through drafts/ch21/ | Existing authored candidates |
| Chapters 22–35 | drafts/ch22/ through drafts/ch35/ | Source-bound local integration candidates |
| Continuous Chapters 1–35 | output/pdf/evolutor-convergence.pdf | Authored-source cumulative candidate |
| Chapters 36–52 | Supplied ZIPs and chapter-local working directories | Four authoring chats active; not yet in the continuous candidate |
| Accepted Chapters 1–2 | book/book.json and acceptance records | Frozen internal records, unchanged |
| Historical editions | Existing sources and preservation tests | Archives, not parallel authoring |

Every requested evolutor-ch30-r01.zip through evolutor-ch52-r01.zip is
inventoried with digest, mapping and separate gates. Chapters 30–35 have now
been used and semantically integrated. Chapter 36's continuity note was
inspected for the allocation handoff, not silently integrated. Incoming
validation labels remain provenance, not local verification.

`chapter-structure.json` is the current machine-readable navigation map;
`CHAPTER_STRUCTURE.md` supplies human reading routes. Actual authored titles
supersede old planned title variants without rewriting the frozen BOOK_PLAN.md
acceptance snapshot. Run the structure checker after future integrations.

## Build and verify

Use Python 3.13.6 at /Users/wenyan/.pyenv/versions/3.13.6/bin/python3 and
OMP_NUM_THREADS=1 for declared CPU references. Requirements and fonts are in README.

- Standalone: `python3 drafts/ch34/build.py --render` and the corresponding ch35 command.
- Derived-data checks: chapter builder `--check`.
- Structure: `python3 scripts/check-chapter-structure.py`.
- Production handoffs: `python3 scripts/audit-production.py` (read-only; no stage promotion).
- Continuous: `python3 scripts/build-convergence.py --through 35 --refresh-assets`.
- Scoped rendering: `python3 scripts/review-convergence.py --pages <physical-ranges>`.
- Regression: `python3 -m pytest -q -o addopts=''`.
- Do not build PDFs concurrently with preservation tests in this repository.

The cumulative builder assembles authored LaTeX, consolidated bibliography,
global glossary and index. Its front matter carries the general pedagogical
acknowledgment once. A successful compile is not cumulative scientific,
editorial or visual acceptance. Scoped renders go to `tmp/pdfs/convergence-review/`.

## Folder and cleanup policy

Authored drafts/, tex/, figures/, examples/ and tests/ are source, not cache.
research/integration/ holds durable package provenance and local review records.
output/pdf/ contains readable candidates and preserved editions; inspect
provenance before removal. build/ contains generated tables/listings/compiler
outputs; tmp/pdfs/ contains regenerable visual-review images.

The legacy cleanup recorded on 27 September remains historical: dated macOS
Trash and its recovery receipt preserved authored/accepted sources. Do not
blanket-delete directories to make the tree appear tidy. Current chapter folders
have one authored manuscript, one tested reference and one standalone builder.

## Current handoff: Chapters 36–52 in production

Four disjoint authoring chats cover Chapters 36–38, 39–43, 44–47 and 48–52.
Their working files do not change the integrated-through-35 baseline. Each
batch returns a source-bound handoff before the coordinator runs cross-batch
tests and cumulative assembly. See BATCH_PRODUCTION.md for ownership and the
read-only admission check; unfinished references are not executed by that check.

Chapter 34 batches the actual gated state from Chapter 31, through pool pins
and independently restored Chapter 33 branches. It preserves masked identity,
owner/generation/version fences and per-request clocks. Per-lane scatter is
not an atomic cross-request transaction or integrated network-output publication.

Chapter 35 caches the actual Chapter 23 Hermon model, including learned
absolute positions and all residual/normalization/FFN layers. Its independent
full-model oracle, every fixture chunk composition, per-layer KV hooks and
offset-mask counterexample are retained for allocator refinement.

Next, Chapter 36 must change physical allocation without changing ordered
logical K/V. Derive blocks, partial tails, generations, reference counts,
immutable prefix sharing, copy-on-write and eviction versus live ownership.
Chapters 37–38 then address scheduling/precision and speculative/attention
kernel experiments. Do not equate state geometry or operation counts with
learned capability or observed speed.

Independent specialist/reader review, cumulative editorial/accessibility QA,
rights/source audit and publication acceptance remain open. No acceptance
promotion is implied by authoring progress.
