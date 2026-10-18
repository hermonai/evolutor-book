# Current manuscript and repository guide

Updated 19 October 2026. **All 52 chapters are authored and assembled.**
This is the complete-range review candidate, not an accepted publication edition.

## Start here

- [Prepublication review edition, 19 October 2026](artifacts/review/evolutor-prepublication-review-2026-10-19.pdf) and its [review records](docs/prepublication/)
- [Complete review candidate, 18 October 2026](artifacts/review/evolutor-complete-review.pdf) (kept unchanged)
- [All chapters, twelve parts and prerequisites](CHAPTER_STRUCTURE.md)
- [Final integration report](FINAL_INTEGRATION_REPORT.md)
- [Current source/PDF review closure](research/integration/continuous-through52-review.json)
- [Claude review and adjustment prompt](docs/CLAUDE_PREPUBLICATION_REVIEW_PROMPT.md)
- [Documentation map](docs/README.md)
- [Editorial architecture](EDITORIAL_ARCHITECTURE.md) and [publication gates](PUBLICATION_PLAN.md)

## One manuscript, explicit stages

| Material | Active source/artifact | Status |
|---|---|---|
| Chapters 1–2 | tex/deep/ch01.tex and ch02.tex | Preserved opening sources; historical internal acceptance unchanged |
| Chapter 3 | tex/textbook/ch03.tex | Preserved authored opening |
| Chapters 4–52 | drafts/chNN/manuscript.tex | Authored chapter candidates with executable companions |
| Continuous Chapters 1–52 | output/pdf/evolutor-convergence.pdf | Complete source assembly, unified navigation and reference material |
| Prepublication review edition | artifacts/review/evolutor-prepublication-review-2026-10-19.pdf | Agent-reviewed edition with front/back matter; not an accepted edition |
| Earlier complete PDF | artifacts/review/evolutor-complete-review.pdf | 18 October review copy, unchanged; not an accepted edition |
| Chapter-local reviews | research/integration/chNN/ | Local author evidence, not independent specialist/reader review |
| Historical editions | book/book.json, earlier plans/reports and preserved artifacts | Historical snapshots, not active authoring counters |

All supplied evolutor-ch22-r01.zip through evolutor-ch52-r01.zip are inventoried.
The requested Chapters 30–52 are used and accounted for rather than silently
omitted. New batch adoption maps explain each incoming section, reference/test
correction and figure disposition. ZIP hashes and packaged QA labels never
substitute for local semantic verification.

chapter-structure.json is the current machine-readable map. Its source titles
and direct reading prerequisites drive the human map and printed twelve-part
navigation. Frozen BOOK_PLAN.md and opening acceptance records are not rewritten.

## Build and verify

Use a Python with the dependencies in requirements-review.txt. Recorded local
Python: /Users/wenyan/.pyenv/versions/3.13.6/bin/python3. Set OMP_NUM_THREADS=1.

- Structure: `python3 scripts/check-chapter-structure.py`.
- Complete fresh build: `python3 scripts/build-convergence.py --through 52 --refresh-assets`.
- Full tests, after required assets exist: `python3 -m pytest -q -o addopts=''`.
- Repeat build: the same command without `--refresh-assets`.
- All cumulative renders: `python3 scripts/review-convergence.py --pages all`.
- One chapter: `python3 drafts/chNN/build.py --render` and `--check` (NN=04–52).
- Handoff evidence: `python3 scripts/audit-production.py --require-ready`.
- Paged runtime/compiler example: `python3 examples/integrated_spine/paged_runtime.py`.

On a fresh checkout, generate assets with the fresh build before full tests.
Standalone-PDF review tests can skip until individual chapter PDFs exist; report
those separately from the fully populated coordinator run.
Do not run PDF builds concurrently with preservation tests. Missing ignored
PDFs/build logs on a fresh checkout are missing local evidence, not a license
to fabricate review hashes. Generate chapter artifacts before running their
derived-file checks or reconstructing local admission evidence.

The cumulative builder assembles authored LaTeX, not old PDFs. It consolidates
exact bibliography identifiers, scopes labels, uses the common glossary and
index, and keeps the general pedagogical acknowledgment in front matter once.
A strict compile is not scientific or whole-volume editorial acceptance.

## What integration does and does not establish

The four batches covering 36–38, 39–43, 44–47 and 48–52 have handed off.
Their original records remain provenance. Coordinator revisions to Chapters
41/49/51/52 remove stale production-time wording and link the actual paged
runtime/compiler companion; the superseded author-review records are retained.

The companion connects actual Chapter 36 pages to Chapter 39's protocol and
Chapter 41's handlers. Its tests preserve Chapter 23/35 learned-position
Transformer outputs and effect traces, including shared tails and failure
cleanup. The chapter-local adapter remains contiguous. No hidden substitution
of a one-head toy or a different architecture is claimed.

Chapter 37 scheduler output and Chapter 38 speculative output have distinct
consumed/emitted-token conventions. Joining their serving schedules, asynchronous
completion fences, durable agent/memory adapters, distributed authority,
authenticated deployment, real backend measurements and trained genomic studies
remain explicitly unimplemented or unevaluated where the chapters say so.
A complete book can explain these contracts without claiming those systems exist.

## Review handoff and preservation

Next: run the Claude pre-publication prompt across all 52 chapters and front/back
matter, then obtain appropriate independent specialist/reader review and resolve
rights, licensing, accessibility and final editorial decisions. Record actual
page coverage and exact revised source/artifact hashes.

Source drafts/, tex/, figures/, examples/ and tests/ are not cache.
research/integration/ holds durable provenance. build/ and tmp/ are derived.
Do not blanket-delete old PDFs or rewrite old acceptance records. The historical
cleanup receipts and earlier review snapshots retain their original scope.
