# Evolutor

## Genomic computation: models, state and systems

An implementation-first research textbook connecting sequence models, biological
inspiration, formal semantics, experimental evidence and execution systems.
Original derivations, editable mechanism illustrations, executable references,
counterexamples and worked exercises develop the ideas from the ground up.

## Complete manuscript candidate

**All 52 chapters are authored and assembled in twelve parts.** The 18 October
2026 integration completes the supplied chapter packages and the whole-book
source spine. It is a review candidate, not an independently accepted edition.

- [Read the complete review PDF](artifacts/review/evolutor-complete-review.pdf).
- [Chapter map and reading routes](CHAPTER_STRUCTURE.md).
- [Verified integration results and remaining limits](FINAL_INTEGRATION_REPORT.md).
- [Claude pre-publication review and revision prompt](docs/CLAUDE_PREPUBLICATION_REVIEW_PROMPT.md).
- [Current manuscript guide](CURRENT_MANUSCRIPT.md) and [documentation map](docs/README.md).

The book moves from learning and sequence-model foundations to biological
abstractions, DOGMA and Hermon DNA, fair experiments, inference engines,
heterogeneous execution, industrial engineering, genomic applications and
research synthesis. The printed contents and PDF navigation follow the same
twelve-part structure as the machine-readable chapter map.

DOGMA is the non-Transformer DNA-native research direction; Hermon DNA is the
Transformer-based direction; Evolutor is the broader theory/compiler/runtime
program. The Chapter 31 diagonal teaching model is not full DOGMA, and cache
parity is not learned genomic competence. Synthetic arithmetic, measured
performance and biological evidence remain separate.

## Reproduce the book

Python 3.11+ is required; the recorded numerical environment is Python 3.13.6,
PyTorch 2.10.0, NumPy 2.4.3, pytest 9.0.2 and Pillow 12.1.1. Use an isolated
environment and [the pinned review dependencies](requirements-review.txt).
PDF production additionally needs XeLaTeX/latexmk, makeindex, Poppler, librsvg,
TeX Gyre Pagella/Heros/math fonts and DejaVu Sans Mono.

```sh
python3 -m pip install -r requirements-review.txt
export OMP_NUM_THREADS=1
# On this Mac; use your installation paths on other hosts.
export PATH=/Library/TeX/texbin:/opt/homebrew/bin:$PATH

python3 scripts/check-chapter-structure.py
python3 -m pytest -q -o addopts=''
python3 scripts/build-convergence.py --through 52 --refresh-assets
python3 scripts/review-convergence.py --pages all
```

The generated working PDF is output/pdf/evolutor-convergence.pdf. The versioned
review copy above makes this candidate readable from GitHub without a local TeX
installation. Generated build/ and tmp/ material is ignored. A local rebuild need
not have the same PDF bytes: source hashes, numerical fixtures and reviewed
artifact identity are separate checks.

For one chapter, use its `drafts/chNN/build.py --render` and `--check` commands
(NN is 04–52). A fresh checkout needs generated assets before `--check`.
`make -f complete-book.mk complete-book` builds the full candidate; the target `complete-book-fresh`
refreshes all chapter assets. Do not build PDFs concurrently with preservation
tests. Historical `make pdf` still belongs to the frozen opening edition.

## Follow the actual execution path

[The integrated-spine companion](examples/integrated_spine/README.md) connects
Chapter 36's real all-layer paged KV storage to Chapters 39/41's opaque runtime
and effect-aware compiler. Tests cover native full-model parity, shared-tail
copy-on-write, prefix eviction, ownership, allocation failure and cleanup.
It is serialized CPU reference evidence, not a GPU kernel or serving benchmark.

```sh
OMP_NUM_THREADS=1 python3 examples/integrated_spine/paged_runtime.py
python3 -m pytest tests/test_integrated_spine.py -q -o addopts=''
```

## Repository organization

| Location | Role |
|---|---|
| tex/deep/, tex/textbook/ | Active opening Chapters 1–3; frozen records remain separate |
| drafts/ch04/ … drafts/ch52/ | Authored LaTeX, tested reference, generated fixture, native figures/TXT, standalone builder |
| code/, examples/, tests/ | Reusable teaching libraries, examples and regression checks |
| tex/convergence/, scripts/ | Whole-book composition, glossary, bibliography/index and production tooling |
| research/integration/ | Package provenance, adoption decisions, local reviews and current source/PDF closure |
| artifacts/review/ | Versioned complete review candidate and artifact manifest |
| docs/ | Current documentation map and pre-publication review prompt |
| build/, tmp/, output/ | Regenerable local compiler outputs, renders and working PDFs |

[BOOK_PLAN.md](BOOK_PLAN.md), book/book.json and earlier reset/edition reports
retain historical acceptance snapshots. They are not current chapter counters.
No parallel beginner edition is maintained. See [contribution guidance](CONTRIBUTING.md).

## Before publication

Independent scientific and reader review, whole-volume editorial polish, rights
and licensing decisions, and accessibility remediation remain open. The PDF is
not claimed tagged or PDF/UA-compliant. There is no general reuse license; public
repository visibility does not supply one.

Use [the Claude prompt](docs/CLAUDE_PREPUBLICATION_REVIEW_PROMPT.md) for a fresh
chapter-by-chapter review and justified local corrections, then obtain the
external review and human release decisions in [PUBLICATION_PLAN.md](PUBLICATION_PLAN.md).
Do not infer genomic capability, AGI, production security or durable distributed
execution from a passing test suite or a complete manuscript.
