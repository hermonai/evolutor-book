# Evolutor

Canonical active edition: **astra-deep-rewrite**. Deep science and engineering, straightforward explanations, useful abstraction.

Chapter 1 — **Why Genomic Computation?** — is the new internally reviewed prototype: ten original editable figures, semantic Unicode TXT, an exact Python companion, exercises with solutions, glossary, bibliography and index. The 52-chapter architecture remains; only Chapter 1 is drafted.

Read the [deep PDF](output/pdf/deep-evolutor.pdf), [chapter source](tex/deep/ch01.tex), [production report](DEEP_CHAPTER_1_REPORT.md), [edition strategy](CANONICAL_EDITION_STRATEGY.md), [book plan](BOOK_PLAN.md) and [chapter standard](CHAPTER_STANDARD.md).

DOGMA = non-Transformer DNA-native model + DOGMA Engine; Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; Evolutor = broader theory/research/compiler/runtime above both. These are research identities, not claims of trained models or production engines.

## Build and verify

```sh
python3 examples/deep/ch01.py
python3 scripts/build_deep_chapter.py --check
python3 scripts/build_deep_plan.py --check
make pdf
python3 -m pytest
python3 scripts/review_deep.py
```

Dependencies: Python 3.10+ (pytest; Pillow for page review), XeLaTeX/latexmk, librsvg, Poppler, and DejaVu fonts. The full historical numerical regression suite also uses the existing repository dependencies. The PDF gate rejects old, empty, later-chapter, unreviewed, or changed-after-review source. To author new material, build a preview under build/ and complete review before updating the acceptance record; do not weaken the gate.

## Frozen editions

astra-undergraduate-rewrite is a pedagogical archive, not a parallel manuscript. Its source, figures, examples and committed PDF remain byte-identical. The default tests verify its preserved publication without rebuilding it; make historical-pdf remains an explicit reproduction tool under build/. Main, astra-rewrite and historical snapshots are preserved; no main merge is part of this milestone.

The original eight-section [preproduction outline](CHAPTER_1_OUTLINE.md) is retained as design history. The actual chapter deliberately expands it to 12 sections and ten figures. Full source-access details live in [the chapter source review](research/deep-ch01-sources.md). Review is author-agent work, not independent scientific certification or a real-reader study.
