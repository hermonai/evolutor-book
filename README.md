# Evolutor

**Genomic computation: models, state and systems**

An implementation-first research textbook connecting sequence models, biological
inspiration, typed computation, experimental evidence and engine design.
Derivations, original editable vectors, executable reference models,
counterexamples and worked exercises develop each mechanism.

## Current manuscript

As of **17 October 2026**, authored-source assembly reaches **Chapter 33 of 52**
(417 pages). The latest chapter,
[DOGMA checkpoints, branching and prefix state](drafts/ch33/README.md), connects
the actual native recurrence and pool to immutable snapshots, independent
branches and bounded prefix reuse.

It includes six original vector/TXT plates, twenty worked exercises, a
continuation proof, an approximation bound and a metadata-inclusive storage/replay
derivation. Seventy-one new tests include independent rational continuation oracles,
malformed-data rejection, stale ownership, rehashed forgeries and forced
lookup collisions. Full regression: **1,283 passed**.

These are locally reviewed manuscript candidates, not an independently reviewed
publication, a trained genomic capability demonstration or production engines.
See the [current guide](CURRENT_MANUSCRIPT.md),
[editorial architecture](EDITORIAL_ARCHITECTURE.md), and
[source-bound cumulative review](research/integration/continuous-through33-review.json).

## Read and reproduce

- [Continuous Chapters 1–33](output/pdf/evolutor-convergence.pdf).
- [Standalone Chapter 33](output/pdf/evolutor-ch33-review.pdf).
- [Chapter 33 source and build guide](drafts/ch33/README.md).
- [Chapter/package convergence matrix](research/integration/chapter-convergence-matrix.md).

PDFs are generated locally and ignored by Git unless explicitly preserved as
historical releases. The source files and review records are versioned.

Requirements: Python 3.11+, PyTorch, pytest, Pillow, XeLaTeX/latexmk, makeindex,
Poppler, librsvg and the project's TeX Gyre/DejaVu fonts.
Declared local numerical checks use Python 3.13.6 and CPU float64 PyTorch.

```sh
export OMP_NUM_THREADS=1
python3 drafts/ch33/build.py --render
python3 drafts/ch33/build.py --check
python3 -m pytest -q -o addopts=''
python3 scripts/build-convergence.py --through 33 --refresh-assets
```

Do not rebuild PDFs concurrently with preservation tests. The historical
`make pdf` gate still belongs to the frozen accepted Chapters 1–2; it is not
the current 33-chapter assembly command.

## Source organization and evidence

- `tex/deep/` and `tex/textbook/` supply the active opening Chapters 1–3.
- `drafts/ch04/` through `drafts/ch33/` contain current authored LaTeX,
  reference code, figure sources, semantic TXT companions and standalone builders.
- `code/` contains reusable teaching libraries; `tests/` contains regression checks.
- `research/integration/` preserves package provenance and local review evidence.
- `build/` is generated compiler/asset cache; `tmp/pdfs/` holds visual-review images.
- Earlier editions, acceptance records and historical preservation tests remain
  unchanged. Do not overwrite them to update current progress labels.

The 52-chapter architecture is retained. Chapters 34–52 are inventoried source
packages, not integrated chapters. Next: **DOGMA batching and state-native
kernels**, preserving scalar per-request state, position and ownership.

DOGMA denotes the non-Transformer DNA-native research direction plus its engine;
Hermon DNA denotes the Transformer-based direction and engine; Evolutor is the
broader theory/compiler/runtime program above both. These identities do not
establish novelty, biological equivalence or capability.

Follow the [chapter standard](CHAPTER_STANDARD.md) and
[LaTeX-first textbook standard](TEXTBOOK_STANDARD.md).
The [shared front-matter note](tex/frontmatter/about-this-book.tex) contains the
one-time pedagogical acknowledgment and general evidence policy. Chapter sources
record specific assumptions and primary-source access depth.

Independent specialist/reader review, cumulative scientific/editorial and
accessibility QA, bibliography/index reconciliation and rights auditing remain
publication gates. A successful build or test suite does not close them.
