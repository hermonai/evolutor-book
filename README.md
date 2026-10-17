# Evolutor

**Genomic computation: models, state and systems**

An implementation-first research textbook connecting sequence models, biological
inspiration, typed computation, experimental evidence and engine design.
Derivations, original editable vectors, executable reference models,
counterexamples and worked exercises develop each mechanism.

## Current manuscript

As of **17 October 2026**, authored-source assembly reaches **Chapter 35 of 52**
(443 pages). Both new standalone chapters are 17 pages. Full regression:
**1,416 passed**, including 47 Chapter 34 tests, 85 Chapter 35 tests and the
new project-structure check.
The [complete chapter structure](CHAPTER_STRUCTURE.md) organizes all 52 chapters
into twelve parts with direct prerequisites and honest authoring/review stages.

The two newest chapters extend the actual preceding implementations:

- [Chapter 34 — DOGMA batching and state-native kernels](drafts/ch34/README.md):
  rowwise native parity, inactive identity, request clocks, pinned/fenced
  completion, cancellation, layouts and honest traffic accounting.
- [Chapter 35 — Hermon DNA prefill, decode and KV state](drafts/ch35/README.md):
  full Transformer-stack cache parity, learned absolute positions, per-layer KV,
  offset masks, context/integrity limits and cumulative copying cost.

Each contains six original editable vector/TXT mechanism plates and twenty
worked exercises. Tests use rational arithmetic, actual scalar/full-model
oracles, checkpoint-restored branches, every fixture chunk partition,
layer-wise KV hooks, cancellation/version fences and negative controls.

These are locally reviewed manuscript candidates, not an independently reviewed
publication, a trained genomic capability demonstration or production engines.
See the [current guide](CURRENT_MANUSCRIPT.md),
[editorial architecture](EDITORIAL_ARCHITECTURE.md), and
[source-bound cumulative review](research/integration/continuous-through35-review.json).

## Read and reproduce

- [Continuous Chapters 1–35](output/pdf/evolutor-convergence.pdf).
- [Standalone Chapter 34](output/pdf/evolutor-ch34-review.pdf).
- [Standalone Chapter 35](output/pdf/evolutor-ch35-review.pdf).
- [Complete structure and reading routes](CHAPTER_STRUCTURE.md).
- [Chapter/package convergence matrix](research/integration/chapter-convergence-matrix.md).

PDFs are generated locally and ignored by Git unless explicitly preserved as
historical releases. The source files and review records are versioned.

Requirements: Python 3.11+, PyTorch, pytest, Pillow, XeLaTeX/latexmk, makeindex,
Poppler, librsvg and the project's TeX Gyre/DejaVu fonts.
Declared local numerical checks use Python 3.13.6 and CPU float64 PyTorch.

```sh
export OMP_NUM_THREADS=1
python3 drafts/ch34/build.py --render
python3 drafts/ch35/build.py --render
python3 drafts/ch34/build.py --check
python3 drafts/ch35/build.py --check
python3 scripts/check-chapter-structure.py
python3 -m pytest -q -o addopts=''
python3 scripts/build-convergence.py --through 35 --refresh-assets
```

Do not rebuild PDFs concurrently with preservation tests. The historical
`make pdf` gate still belongs to the frozen accepted Chapters 1–2; it is not
the current 35-chapter assembly command.

## Source organization and evidence

- `tex/deep/` and `tex/textbook/` supply the active opening Chapters 1–3.
- `drafts/ch04/` through `drafts/ch35/` contain current authored LaTeX,
  reference code, figure sources, semantic TXT companions and standalone builders.
- `code/` contains reusable teaching libraries; `tests/` contains regression checks.
- `research/integration/` preserves package provenance and local review evidence.
- `build/` is generated compiler/asset cache; `tmp/pdfs/` holds visual-review images.
- Earlier editions, acceptance records and historical preservation tests remain
  unchanged. Do not overwrite them to update current progress labels.

The 52-chapter architecture is retained. Chapters 36–52 are inventoried source
packages, not integrated chapters. Next: **Paged KV, prefix sharing and
allocation**, preserving exact ordered K/V while changing physical storage.

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
