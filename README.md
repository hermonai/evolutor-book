# Evolutor

Genomic Computation, DNA-Native AI, and Adaptive Machine Intelligence

Active development branch: **astra-deep-rewrite**. The target is full technical and scientific depth with straightforward explanations, including useful abstraction. This is currently a **planning-only deep edition**: 52 substantial chapters are planned; none is drafted yet. No new deep PDF, model or engine is claimed.

Start with [DEEP_REDESIGN.md](DEEP_REDESIGN.md), [contents](BOOK_PLAN.md), [Chapter 1 outline](CHAPTER_1_OUTLINE.md), [technical reset](TECHNICAL_LEVEL_RESET.md) and [redesign report](DEEP_REDESIGN_REPORT.md).

DOGMA = non-Transformer DNA-native model + DOGMA Engine; Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; Evolutor = broader theory/research/runtime above both. These are target research roles, not evidence of implementation.\n\n## Validate the plan

```sh
python3 scripts/build_deep_plan.py --check
python3 scripts/build_pedagogy.py --check
python3 -m pytest
make pedagogy
```

The default `make pdf` intentionally refuses to build until a new deep manuscript is accepted. `make historical-pdf` explicitly reproduces the preserved undergraduate prototype into build/, without replacing its committed PDF or treating it as the new edition. See [publication policy](PUBLICATION_PLAN.md).

## Previous editions

The undergraduate experiment is preserved at astra-undergraduate-rewrite commit af8de42e16c71024d3e228a57e1d4d87c8d87276. Its [source](tex/undergraduate/ch01.tex), [historical report](CHAPTER_1_REPORT.md) and [historical PDF](output/pdf/undergraduate-evolutor.pdf) remain available, but are not the active intellectual target. Earlier astra-rewrite and pre-reboot snapshots are unchanged. No main merge, deletion, license or authorship change is included.

Active planning data use the deep- prefix under pedagogy/. The older unprefixed data are retained only for historical regression checks. Tests verify structure and preservation, not scientific novelty or successful reader learning.
