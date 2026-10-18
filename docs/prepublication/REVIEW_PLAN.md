# Prepublication review plan

Review of *Evolutor: Genomic computation: models, state and systems*, carried out
under `docs/CLAUDE_PREPUBLICATION_REVIEW_PROMPT.md` on 18–19 October 2026 by one
agent session (Claude). This is an additional agent review. It is not
independent scientific peer review, a reader study or an accessibility audit.

## Starting point

| Item | Value |
|---|---|
| Branch / starting revision | `main` at `2fd93ec` ("docs(book): verify clean-checkout build and clarify review prerequisites"), clean working tree |
| Committed review copy | `artifacts/review/evolutor-complete-review.pdf`, 619 pages, SHA-256 `89d1be51…6a6e` |
| Local baseline build | `scripts/build-convergence.py --through 52`: 619 pages; local SHA-256 `81bb52bb…` (TeX Live 2026; differs in bytes from the committed copy, as the README allows) |
| Baseline tests | `pytest -q -o addopts=''`: 2,078 passed |
| Frozen records | `artifacts/deep/ch01-review.json`, `ch02-review.json` (accepted opening chapters); `BOOK_PLAN.md`, `book/book.json`; `research/integration/continuous-through52-review.json` (review of the 619-page candidate) |

## Scope

1. All 52 chapters, read in full (completed 18 October 2026), plus the
   cumulative front matter, part openers, reference material and index.
2. Book-level architecture: front and back matter, navigation, the reader's
   route through twelve parts, and the book's relation to DNA computing.
3. Evidence discipline in reader-facing prose: pilots, provenance wording,
   stale integration statements and claims about capability.
4. Rendered typography of the complete volume and of every changed standalone
   chapter page.
5. Record keeping: amended chapter-local records with preserved superseded
   copies, a change log and a validation report.

Out of scope: production rewrites of the reference engines, new trained
experiments, new wet-lab or generative-design content, licensing and
authorship changes, and anything that would publish or push.

## Order and risk-based priorities

| Priority | Area | Reason |
|---|---|---|
| 1 | Pilot interpretation, Chapters 22–25 | Reader-facing evidence claims; a wrong reading of a negative result is a scientific defect |
| 2 | Production provenance in reader prose, Chapters 10–52 | "Incoming package", "supplied", "coordinator" and stale "unfinished Chapter N" text misdescribes the finished book |
| 3 | Front and back matter | The candidate opened with administrative pages and had no preface, epilogue, glossary of conventions or biology primer |
| 4 | DNA computing and frontier models | The user asked for the book to address current DNA computing; this must be done with cited, bounded claims |
| 5 | Typography | Plate scaling, a 14-page contents, split boxes, chapter-level source notes |
| 6 | Records | Every source change must keep its prior review record identifiable |

Chapters 1–2 are bound by frozen acceptance records and were not edited.
Findings for them are proposals for the author (see FINDINGS.md, F-ch01-a).
Chapter 3 is bound only by a candidate record and was edited; see
`docs/prepublication/SUPERSESSION.md`.

## Checkpoint

The review scope above is complete except for the gates listed in
PUBLICATION_READINESS.md. The next session should start from
`docs/prepublication/CODEX_HANDOFF.md`.
