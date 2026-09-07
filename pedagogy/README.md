# Planning data ownership

Active deep edition:

- deep-curriculum.json: canonical 52-chapter architecture, dependencies, depth tasks and prior-topic dispositions.
- deep-book-i-contract.json: shared, versioned Book I exports; all remain planned-not-yet-taught.
- deep-ch01-outline.json: eight detailed sections and eight figure briefs for the next Chapter 1.
- deep-figure-inventory.json / deep-animation-inventory.json: generated plans, no finished assets.

Root BOOK_PLAN.md, COURSE_MAP.md, PREREQUISITE_GRAPH.md and related generated documents derive from these sources using scripts/build_deep_plan.py. The active book metadata points here. No script generates manuscript prose.

Historical undergraduate data are retained unchanged: curriculum.json, book-i-contract.json, figure-inventory.json, animation-inventory.json, ch01-storyboard.json and ch01-terms.json. Do not use these to extend the deep edition. Their regression expectations are compared with the preserved Git commit, not the new root documents.
