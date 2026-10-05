# Current manuscript and repository guide

Updated 27 September 2026. This guide identifies the active work; it does not
promote a review candidate into an accepted edition.

## Start here

- Latest chapter: [21 — Strands, complements and dual-state hypotheses](drafts/ch21/README.md).
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
book. Chapters 1–10 still need their combined notation, bibliography, index and
cross-reference integration. Later candidates must retain compatible interfaces;
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

Use the Chapter 21 README commands to build only the active chapter. Its builder
creates build/ch21/ as needed; --check expects the computed assets to exist.
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

Chapter 22 integrates a DOGMA reference and a falsifiable research program, keeping strand symmetry, selective state, memory and evaluation contracts explicit.
Continue the evidence ladder: define assumptions, derive, implement, compare an
independent oracle, break an assumption, and state the experimental test still
needed. Contemporary papers inform research questions, not unearned claims of
biological capability, industrial readiness or performance leadership.
# Package convergence in progress — 6 October 2026

Chapter 22 has been semantically integrated, corrected, tested and visually
reviewed as a standalone candidate. The integration branch preserves the earlier
accepted edition. Remaining packages and cumulative/full-book gates are tracked
separately in `research/integration/chapter-convergence-matrix.md`; this update is
not an acceptance promotion. Use the declared Python environment (Python 3.11+;
PyTorch required for Evolutor), not the macOS system Python.
