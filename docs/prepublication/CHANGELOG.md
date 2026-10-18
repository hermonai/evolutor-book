# Prepublication change log

Changes made on 18–19 October 2026, starting from `2fd93ec`. Each entry gives the
finding it answers (FINDINGS.md), what changed, and its preservation consequence.

## Book-level apparatus (no chapter source changed)

| Change | Files | Finding | Consequence |
|---|---|---|---|
| New title page, preface, "How to use this book" with a reading-map plate | `tex/convergence/matter/{titlepage,preface,how-to-use}.tex`, `figures/reading-map.{tex,txt}` | F-global-front | The two administrative opening pages are gone from the book; their content is now in the preface and how-to-use |
| "Contents at a glance" | `scripts/build-convergence.py` (`contents_at_a_glance`), `book.tex` | F-global-toc | Generated each build from `chapter-structure.json` |
| Part openers with guiding question, orientation and chapter list | `tex/convergence/parts/part01–12.tex`, preamble `\EvolutorPart` | F-global-parts | Part order and titles still come from `chapter-structure.json` (`test_printed_part_navigation_matches_complete_chapter_map` passes) |
| Goals and key-ideas boxes for all 52 chapters | `tex/convergence/chapter-guides.json`; builder `inject_guide` | F-global-guides | Injected into derived copies under `build/convergence/` only; chapter sources and their hashes are unchanged |
| Epilogue, Appendices A–C | `matter/epilogue.tex`, `appendix-{biology,notation,evidence}.tex`, `figures/{three-meanings,duplex-dogma}.{tex,txt}` | F-global-matter, F-global-agi | Appendices use letter numbering and figures A.n, E.n |
| 31 matter bibliography entries | `matter/sources.tex` | — | Merged with chapter entries by identity (DOI, then arXiv ID, then URL) |
| Plate scaling | `tex/convergence/preamble.tex` (`\PlaceScaledPlate`) | F-global-plates | Wide plates shrink to the measure; small plates grow by at most 1.15×. Plates are measured in a `varwidth` box with the real `\linewidth`, so multi-line plates (Figure 13.5) and width-relative plots (Figures 9.6, 20.2) keep their standalone layout |
| Key-ideas box unbreakable | preamble `EvolutorIdeasBox` | F-global-keyideas | A box that does not fit moves whole to the next page |
| Source notes typeset as sections in the book | builder `evidence_heading` | F-global-notes | Derived copies only; standalone review PDFs keep their unnumbered chapter heading. Book 658 → 643 pages |
| arXiv identity normalisation | builder `identity` | F-global-bib-dup | abs/html/pdf views and versions of one arXiv paper merge; a DOI still wins |
| Matter, guides and figure text hashed in the build record | builder | — | `build/convergence/build-record.json` binds 952 source hashes |
| Builder tests | `tests/test_convergence_builder.py` | — | Two new tests (arXiv identity; source-note heading) |

## Grayscale and legibility pass (19 October 2026)

No chapter source changed in this pass; both edits are book-level matter.

| Change | Files | Finding | Consequence |
|---|---|---|---|
| Identify the chapter boxes by their printed headings rather than by colour | `tex/convergence/matter/how-to-use.tex` | F-gray-howto | The sentence now works in monochrome and for red-green colour vision deficiency |
| Raise every label in the three-senses plate from `\tiny` to `\scriptsize` and re-space the panels so nothing collides or overruns | `tex/convergence/figures/three-meanings.tex` | F-gray-labels | No figure label in the book is below 8pt; the plate's `.txt` companion still describes the same drawing |

Only PDF pages 6 and 609 differ from the previous review edition; both were
re-rendered at 120–150 dpi and inspected in colour and grayscale.

## Chapter source edits

| Chapter | Change | Finding |
|---|---|---|
| 3 | Removed the "Revision boundary" callout and 12 `EVOD-03-Fn.` caption prefixes; typeset the f(r) definition; removed "Publication work still required"; renamed Appendix A "Executable boundary diagnostics"; replaced the Appendix B ledger with "Sources and further reading" keeping every primary link | F-ch03-a |
| 10 | Stale "upcoming Chapters 1–10 integration pass" → pointer to Part III and Chapter 11 | F-global-stale |
| 13, 14 | "compile this review PDF" → "typeset the chapter on its own" | F-global-review-pdf |
| 22 | Pilot read against chance (SE 0.044); new exercise 17; "package" → "reference" | F-ch22-a |
| 23 | Negative pilot reading (Hermon = random-label control; loss at ln 2); new ln 2 exercise; evidence-ladder sentence; source note | F-ch23-a |
| 24, 25 | Single-run percentage provenance replaced by the Chapter 23 negative-result link; Chapter 25 source note | F-ch24-a, F-ch25-a |
| 32, 37, 38, 40, 42–52 | Production provenance and stale-chapter statements rewritten to reader-facing text | F-global-provenance, F-global-stale |
| 33–47 | *Sources* notes: package, adoption and coordinator sentences removed; every access-depth statement kept | F-global-provenance |

Per-chapter descriptions, changed pages and raster-unchanged pages are in
`docs/prepublication/chapter-amendments.json`.

## Records and preservation

- **Ch4–21 records** (`artifacts/deep/ch{10,13,14}-review.json`) and **Ch22–52
  records** (`research/integration/chNN/local-review.json` for 25 chapters) were
  amended by `scripts/amend-prepublication-records.py`. Before amending, each
  record was copied unchanged beside itself as
  `chNN-review-superseded-2026-10-19.json` or
  `pre-prepublication-local-review-2026-10-19.json`. Every superseded copy was
  checked byte-for-byte against `git show HEAD:<record>`.
- The new hashes cover the superseded record's exact path set plus current
  chapter files, so transitive dependencies and test files stay bound.
- Each amended record gains a `prepublicationRevision` / `prepublication_revision`
  block: date, reviewer ("author/agent (Claude prepublication pass); not
  independent review"), change, re-inspected pages and the unchanged-page policy.
  `accepted` and `independent_review` remain false; the script refuses to amend
  an accepted record.
- **Frozen, untouched:** Chapter 1 and 2 sources and acceptance records,
  `BOOK_PLAN.md`, `book/book.json`, `research/integration/continuous-through52-review.json`,
  `artifacts/review/evolutor-complete-review.pdf` and its manifest.
- **Chapter 3:** `artifacts/textbook/review.json` describes the earlier Ch3
  source and is now superseded; it is not edited (`SUPERSESSION.md`).
- **Archives:** the removed Ch3 material is in `docs/provenance/ch03-source-ledger.md`;
  the 17 prior source notes are in `docs/provenance/source-notes-2026-10-19.md`
  with SHA-256 of each original file.
- **Stale aux files** for 14 chapters were moved, not deleted, to
  `tmp/recovered-aux-2026-10-19/` (ignored directory).

## New versioned artifact

`artifacts/review/evolutor-prepublication-review-2026-10-19.pdf` with
`artifacts/review/prepublication-2026-10-19-manifest.json`. The 18 October
review copy stays in place and identifiable.
