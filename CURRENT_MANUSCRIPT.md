# Current manuscript and repository guide

Updated 6 October 2026. This guide identifies the active work; it does not
promote a review candidate into an accepted edition.

## Start here

- Latest integrated chapter candidate: [28 — Distributed training and reproducible model artifacts](drafts/ch28/README.md).
- Current scope and chapter responsibilities: [editorial architecture](EDITORIAL_ARCHITECTURE.md).
- Opening LaTeX revision: [revision guide](TEXTBOOK_REVISION.md).
- Production criteria: [textbook standard](TEXTBOOK_STANDARD.md) and [chapter standard](CHAPTER_STANDARD.md).

## One manuscript, explicit stages

| Material | Where to work or read | Status |
|---|---|---|
| Opening Chapters 1–3 revision | tex/ and TEXTBOOK_REVISION.md | Textbook review candidate; accepted opening preserved separately |
| Standalone Chapter 3 | drafts/ch03/README.md | Earlier review candidate and figure sources |
| Chapters 4–20 | drafts/ch04/ through drafts/ch20/ | Authored standalone review candidates |
| Chapter 21 | drafts/ch21/README.md | New standalone review candidate |
| Accepted Chapters 1–2 | book/book.json and existing acceptance records | Frozen; not a claim that Chapters 3–21 are cumulatively accepted |
| Historical editions | Existing historical sources and preservation tests | Archives, not parallel active authoring |

Read chapters in numerical order. The latest standalone PDF is not the entire
book. The new continuous authored-LaTeX builder consolidates notation, bibliography,
index and cross-references through the explicitly requested chapter. Later candidates must retain compatible interfaces;
integration and independent specialist/reader review are explicit open gates.
BOOK_PLAN.md is a generated acceptance snapshot and long-range chapter spine,
not a live list of completed drafts. Do not edit frozen status files to make
progress appear larger.

## What belongs in each folder

| Folder | Purpose | Cleanup rule |
|---|---|---|
| drafts/, tex/, figures/, examples/ | Authored text, diagrams and reference implementations | Preserve; never treat as build cache |
| tests/ | Numerical, semantic and preservation checks | Preserve and run |
| artifacts/deep/ | Review records binding source and PDF hashes | Preserve; update only after actual review |
| output/pdf/ | Readable generated PDFs and preserved publications | Do not blanket-delete; inspect edition and provenance first |
| build/ | Generated tables/listings, LaTeX auxiliaries, compiler PDFs and logs | Disposable only after checking tracked files and active builds |
| tmp/pdfs/ | Rendered page images used for visual QA | Regenerable; not manuscript sources |

A .tex file under build/ may be a generated table, not an authored chapter.
Edit drafts/ch21/manuscript.tex or its figures instead. An identical-looking
PDF under build/ is a compiler product; read the named file under output/pdf/.

## Clean current workflow

Use the chapter README commands for standalone reviews. For continuous assembly,
run Python 3.13: scripts/build-convergence.py --through 28 --refresh-assets.
This produces output/pdf/evolutor-convergence.pdf and a source-bound build
report in build/convergence/. It is a cumulative review candidate, not an accepted
full planned book. --check on chapter builders verifies existing computed assets.
Do not use historical-pdf or older cumulative builders merely to preview a new
chapter: those are explicit reproduction workflows and recreate their own caches.

On 27 September 2026, the two books' old build trees (1,148 files, approximately
102 MB combined) were moved to a dated macOS Trash archive, not deleted.
Authored files, prior review PDFs, acceptance records and historical editions
were retained. Current chapter builds and the regression suite recreate only
the caches they need (including textbook validation assets). The local
archive includes a recovery receipt. Future cleanup should likewise resolve
exact paths, confirm no tracked source or active process, then archive rather
than recursively delete a repository directory.

## Next editorial milestone

Chapter 29 develops benchmark design and comparative evidence; retain objective, dependency-aware split and restart contracts, and reconcile historical claims with the rewritten earlier chapters.
Primary sources inform questions; local implementation checks do not establish biological capability or industrial leadership.

# Package convergence in progress — 6 October 2026

Chapters 22–28 have been semantically integrated, rewritten, tested and locally
visually reviewed as standalone candidates. Source-bound evidence is tracked
in the matrix, not inferred from file presence. The integration branch preserves the earlier
accepted edition. Remaining packages and cumulative/full-book gates are tracked
separately in `research/integration/chapter-convergence-matrix.md`; this update is
not an acceptance promotion. Use the declared Python environment (Python 3.11+;
PyTorch required for Evolutor), not the macOS system Python.
