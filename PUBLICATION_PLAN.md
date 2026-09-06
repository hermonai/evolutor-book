# Publication plan: undergraduate-first edition

Status: architecture-only, edition 3 planning, branch astra-undergraduate-rewrite. Title: Evolutor. Subtitle: From Genomic Computation to Adaptive Machine Intelligence. No authorship or license change.

## Active versus preserved

The active source of pedagogical architecture is pedagogy/curriculum.json. Its generated Markdown maps and JSON inventories are versioned. The new book/book.json has an empty chapter list, no active TeX main, and an explicit previous-edition commit. tex/chapters/manifest.tex has no chapter includes.

The existing TeX chapters, preamble, metadata, scientific figures, tests and reference code are preserved audit inputs. Their byte identity is checked where covered by the preservation test. They are not reader-facing content in the new edition. Old reports describe their original milestone, not current active status.

## Build isolation

`make pdf` and `make check-pdf` stop while the new edition has no accepted chapters. Do not compile the old TeX main directly and call it the new edition. Existing local output PDFs are earlier-edition artifacts; this milestone neither edits nor exports them.

To reproduce the earlier edition, check out preserved commit `58fa55a8097157d297be4afe21f146623048b875` in a separate worktree and follow its PUBLICATION_PLAN.md. Its existing LaTeX build remains available in that history. The new edition will reuse infrastructure only after its reader preface, metadata, glossary, index and accepted chapter manifest are deliberately revised.

## Architecture checks

```sh
python3 scripts/build_pedagogy.py
python3 scripts/build_pedagogy.py --check
python3 -m pytest
```

The generator uses the standard library. Existing regression tests still require the previously documented project dependencies. Verified interpreter: Python 3.13.6; pytest 9.0.2. No new dependency installation or third-party asset redistribution is required for this milestone.

## Chapter production and release

Use [the full gate checklist](REVIEW_GATES.md). Only a newly taught, reviewed chapter enters the active manuscript. Code-native SVG and reproducible UML sources accompany Unicode TXT semantics. Animation inventories are plans, not generated frame assets. PDF layout review happens after actual chapter production, not during this planning-only pass.

Publish scoped architecture commits on astra-undergraduate-rewrite. Preserve main, astra-rewrite and archival branches. Do not change the default branch or create a final-edition release. Independent review, novice teach-back, source verification, rights and accessibility checks remain release gates.
