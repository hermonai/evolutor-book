# Evolutor

## From Genomic Computation to Adaptive Machine Intelligence

Active work: **undergraduate-first pedagogical architecture**, branch `astra-undergraduate-rewrite`. No new manuscript chapters have been drafted.

Start with [the redesign](PEDAGOGICAL_REDESIGN.md), [new contents](BOOK_PLAN.md), [course map](COURSE_MAP.md), [prerequisite graph](PREREQUISITE_GRAPH.md) and [chapter storyboards](VISUAL_STORYBOARD.md). See [beginner review](BEGINNER_REVIEW.md), [professional-perspective review](PROFESSIONAL_REVIEW.md) and [review gates](REVIEW_GATES.md) before authorizing new Chapter 1.

The plan contains 40 small teaching units. It is a proposed learning route, not a completed book or a validated semester schedule. Book II assumes only the eventually verified Book I outcomes, not a separate ML or software-architecture course.

## Preservation and build boundary

The two-chapter edition is preserved on [astra-rewrite at 58fa55a](https://github.com/hermonai/evolutor-book/tree/58fa55a8097157d297be4afe21f146623048b875). The earlier public edition remains on main. No force-push, deletion, default-branch, license or authorship change is made.

The old LaTeX chapters, code, figures and reports remain audit material, not active new-edition content. The new manuscript manifest is empty. `make pdf` and `make check-pdf` deliberately fail with an explanatory message while the edition is architecture-only. Existing local PDFs still belong to the earlier edition and are not regenerated or relabeled. Reproduce them from the preserved commit, preferably in a separate worktree.

## Verify the architecture

```sh
python3 scripts/build_pedagogy.py --check
python3 -m pytest
```

After editing pedagogy/curriculum.json, run `python3 scripts/build_pedagogy.py`. Checks cover prerequisite ordering, cross-book imports, inventory freshness and preservation. They do not certify readability or scientific validity.

See [publication plan](PUBLICATION_PLAN.md), [learning/code progression](LEARNING_PROGRESSION.md), [concept maps](CONCEPT_MAPS.md), [figure system](FIGURE_SYSTEM.md), [terminology audit](TERMINOLOGY_AUDIT.md) and [previous-outline disposition](PREVIOUS_EDITION_AUDIT.md). Third-party papers and supplied review screenshots are not redistributed.
