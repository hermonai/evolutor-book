# Publication readiness

Assessment after the agent prepublication pass of 18–19 October 2026. It covers
`artifacts/review/evolutor-prepublication-review-2026-10-19.pdf`
(SHA-256 `6a33815a…a1fd`, 643 pages).

## Assessment

The manuscript is a **complete, internally consistent, locally verified review
edition**. It is not ready to publish, and nothing in this pass makes it so.

What this pass can support, because it was checked:

- All 52 chapters are authored, assemble into one volume, and build
  deterministically: two consecutive builds produced byte-identical PDFs.
- The book now reads as a book rather than an integration artifact: it has a
  title page, preface, reading guide, contents at a glance, twelve part openers,
  per-chapter goals and key ideas, an epilogue, three appendices, a glossary, a
  reconciled 147-entry bibliography and an index.
- Production provenance has been removed from the text readers see. Where a
  statement recorded how deeply an external source was read, it was kept; where
  it described packages, adoption maps or coordinator tests, it was rewritten,
  and the originals are archived verbatim under `docs/provenance/`.
- The two pilot results are now reported as the negative results the data show,
  with their controls and their chance baseline stated (F-ch22-a, F-ch23-a).
- 2,080 tests pass, the production audit passes, and all 49 standalone chapters
  pass their `--check`.
- Every page of the volume has been read in colour and in grayscale, every
  changed page of every rebuilt chapter inspected at full size, and every text
  run measured: no figure label is below 8pt, and no figure depends on colour
  alone to carry its meaning.

What this pass cannot support: anything about the book's scientific standing,
its usefulness to real readers, its legal position, or its accessibility. Those
are the gates below.

## Blockers

These must close before publication. Five remain open and none of those can be
closed by an agent; B3 closed on 19 October 2026 and is kept here, struck
through, so the record shows what was done rather than what quietly vanished.

| # | Blocker | Why it is open | Who |
|---|---|---|---|
| B1 | Independent scientific review | This is an additional agent review. The book's genomics, DNA-computing, systems and ML claims need specialists who did not write them. The Epilogue and Appendix A are new and have had no specialist read at all | Author, external reviewers |
| B2 | Rights audit and licence decision | Citations, quotations and artwork have not been audited for reuse rights, and the repository has no reuse licence. The title page states this as an open gate; no licence was invented | Author, counsel |
| ~~B3~~ | Complete grayscale and full-size figure review | **Closed 19 October 2026.** All 643 pages read in grayscale; all 75 figures using the Red/Green pair read at 150 dpi in grayscale; every text run measured. Two defects fixed. What remains is a proof on paper: a monochrome test print, which needs a press, not an agent | — |
| B4 | Accessibility | The PDF is not tagged, has no alt text, and no PDF/UA or EPUB validation was run. No compliance is claimed anywhere | Author, accessibility specialist |
| B5 | Reader study | The new front matter, part openers and chapter guides were written to help readers; no reader has tried them | Author |
| B6 | Frozen Chapter 1 paragraph | Chapter 1 still says the companion volume supplies molecular-computation foundations with a "new Chapter 1", which is out of date now that that volume is a complete 32-chapter edition. Chapter 1 is bound by a frozen acceptance record, so this pass did not touch it. Replacement text is drafted in FINDINGS.md (F-ch01-a) | Author |

## Justified optional improvements

Worth doing, but none blocks publication.

| Item | Rationale |
|---|---|
| Builder fix for stale `review.aux` (F-build-stale-aux) | A failed chapter build currently leaves the previous PDF in place, so a stale artifact can pass `--check`. This is a reproducibility trap for the next session, not a defect in the book |
| Glossary entries for the new matter | The epilogue and appendices introduce terms the generated glossary does not carry |
| Chapter 47 exercise order (F-ch47-order) | Exercises follow the closing bridge there, unlike every other chapter |
| A figure-level review of the three new plates | They were drawn for this pass and inspected, but they have had no second reader |

## Human decisions still required

1. Accept, revise or reject each chapter edit in CHANGELOG.md. The edits are
   bounded and recorded, but they are an agent's editorial judgement.
2. Decide F-ch01-a, which requires editing a frozen chapter.
3. Decide whether the 19 October edition replaces the 18 October one as the
   review copy readers are pointed to. README and CURRENT_MANUSCRIPT now list
   both, with the older one kept and labelled.
4. Decide licensing and authorship. This pass changed neither.
5. Decide whether to commission B1 and B5 now or after further editing.

## What was deliberately not done

- No record was promoted. `accepted` and `independent_review` are still `false`
  everywhere, and the amendment script refuses to touch an accepted record.
- No historical evidence was rewritten. Superseded records were copied aside
  byte-for-byte and verified against `git show HEAD:<record>`; the Chapter 1 and
  2 acceptance records, `BOOK_PLAN.md`, `book/book.json` and the 18 October
  review artifact are untouched. See SUPERSESSION.md.
- Nothing was pushed, merged, tagged or released, and no sibling repository was
  modified.
- No claim of novelty, influence, market position, scientific validation or
  publication readiness was added to the book. The pass added the opposite: an
  explicit list of what would count as evidence for strong capability claims,
  and an explicit statement that none of the book's results answers it.
