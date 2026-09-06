# Undergraduate architecture implementation report

Date: 2026-09-06. Branch: astra-undergraduate-rewrite. Scope: the review's first execution only.

## Outcome

The new curriculum is designed from scratch as 40 planned teaching units, with prerequisites taught before formalism. No new Chapter 1, old Chapter 3, publication PDF, finished figure, animation asset or research result is produced.

The prior two-chapter edition remains at `58fa55a8097157d297be4afe21f146623048b875` on astra-rewrite. Main and the older archive are untouched. The original Chapter 1–2 TeX files remain byte-identical; they are excluded from the new empty active manifest. Normal PDF build/check targets refuse to present them as the new edition.

## Deliverable coverage

| Requested deliverable | Implementation |
|---|---|
| New pedagogical thesis and TOC | PEDAGOGICAL_REDESIGN.md; BOOK_PLAN.md |
| Every chapter's prerequisites and exit tasks | COURSE_MAP.md; pedagogy/curriculum.json |
| Chapter dependency and cross-book graph | PREREQUISITE_GRAPH.md; pedagogy/book-i-contract.json |
| Disciplinary concept maps | CONCEPT_MAPS.md |
| Every chapter's visual sequence and publication inventory | VISUAL_STORYBOARD.md; pedagogy/figure-inventory.json |
| Exercise and code progression | LEARNING_PROGRESSION.md |
| Training, inference and experiment routes | Separate final sections in LEARNING_PROGRESSION.md |
| Animation inventory | pedagogy/animation-inventory.json, explicitly planned-no-assets |
| Beginner and professional critiques | BEGINNER_REVIEW.md; PROFESSIONAL_REVIEW.md |
| Current and planned old chapter disposition | PREVIOUS_EDITION_AUDIT.md (29 entries) |
| Unknown-word/first-use plan | TERMINOLOGY_AUDIT.md |
| Vector, TXT companion and UML rules | FIGURE_SYSTEM.md |
| Chapter production and release gates | REVIEW_GATES.md |

## Verification

Full suite: 42 passing tests under Python 3.13.6 and pytest 9.0.2. The additional architecture tests check generated-document freshness, ordered dependencies, invalid-plan rejection, all old-outline dispositions, preserved chapter bytes, empty active manifest, blocked PDF targets, and synchronized Book I contract copies. The paired contract comparison runs when both repositories are available locally.

The plans contain 80 figure entries, not finished figures. Structural validation and internal role critiques do not establish scientific correctness, learner comprehension or external peer review. No source or figure claim is promoted merely because an old regression test passes.

Manual sequencing review also moved formal complexity-class terminology behind machine/reduction foundations, removed premature parameter terminology from Evolutor's state exercise, deferred library tensor operations until setup is taught, and added explicit missing biological terms to the first-use ledger.

## Next boundary

Review the architecture and issue the next execution prompt for the new Chapter 1. Actual prose, glossary definitions, complete figure sources, animation frames, rendered pages and real-reader validation remain future chapter-production work. No continuation of the old manuscript is implied.
