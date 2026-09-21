# Evolutor

The shared [About this book note](tex/frontmatter/about-this-book.tex) owns
the pedagogical acknowledgment and general evidence/review policy. It is
authored front matter for one-time inclusion in the next integrated edition;
chapter-specific assumptions and source notes remain in their chapters.

New authoring uses the [LaTeX-first Chapters 1–3 textbook candidate](tex/evolutor-textbook.tex),
with a worked first-principles opening, native TikZ mechanisms and retained
reviewed vector figures. See [revision scope and build commands](TEXTBOOK_REVISION.md)
and the [shared textbook standard](TEXTBOOK_STANDARD.md). Run
`make -f textbook.mk textbook-check` then `make -f textbook.mk textbook`.
This is a new review candidate; the accepted Chapters 1–2 and their hashes remain frozen.

Canonical active edition: **astra-deep-rewrite**. Deep science and engineering, straightforward explanations, useful abstraction.

Chapters 1–2 are internally reviewed development manuscripts. Chapter 2 — **Learning objectives, data, tasks, and evaluation** — adds 13 original editable SVG figures with semantic TXT companions, nine static keyframes, executable reference code and twelve exercises with worked solutions. The 52-chapter architecture remains; Chapter 3 has standalone and combined LaTeX review candidates. [Chapter 4: Reproducible PyTorch training](drafts/ch04/README.md) is now an isolated authored-LaTeX review candidate with five vector plates, an exact-restart experiment, and twelve worked exercises. [Chapter 5: Tokenization and sequence representation](drafts/ch05/README.md) adds five original mechanism plates, implementation-first derivations, tested code, and twelve worked exercises. [Chapter 6: Recurrent models and gated state](drafts/ch06/README.md) adds five vector figures, tested numerical models, and twelve worked exercises. [Chapter 7: State-space models, selective updates and scans](drafts/ch07/README.md) adds five mechanism figures, independent numerical checks, and twelve worked exercises. [Chapter 8: Attention and content addressing](drafts/ch08/README.md) adds five algorithm plates, masked attention and cache references, gradient checks, and twelve worked exercises. [Chapter 9: Assembling a Transformer block](drafts/ch09/README.md) adds six computation figures, a complete two-block reference and forward/backward equivalence checks, and twelve worked exercises. [Chapter 10: Conditional computation and routing](drafts/ch10/README.md) adds five routing figures, sparse/dense gradient checks, capacity-history counterexamples, and twelve worked exercises. Chapters 1-10 integration is next; cumulative acceptance has not advanced.

The [current editorial architecture](EDITORIAL_ARCHITECTURE.md) defines chapter responsibilities, prerequisites, evidence gates, and the next integration milestone. Use it for current authoring progress; generated historical plans retain their acceptance-snapshot status.

Read the [Chapters 1–2 PDF](output/pdf/deep-evolutor-ch01-02.pdf), [Chapter 2 source](tex/deep/ch02.tex), [Chapter 2 production report](DEEP_CHAPTER_2_REPORT.md), [edition strategy](CANONICAL_EDITION_STRATEGY.md), [book plan](BOOK_PLAN.md) and [chapter standard](CHAPTER_STANDARD.md). The [Chapter 1-only PDF](output/pdf/deep-evolutor.pdf) and [its production report](DEEP_CHAPTER_1_REPORT.md) are preserved unchanged.

DOGMA = non-Transformer DNA-native model + DOGMA Engine; Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; Evolutor = broader theory/research/compiler/runtime above both. These are research identities, not claims of trained models or production engines.

## Build and verify

Chapter 3 now has a standalone [review edition](drafts/ch03/README.md), with twelve editable SVG/TXT figures and a page-inspected PDF. See the [review report and release gates](DEEP_CHAPTER_3_REVIEW_REPORT.md). It is not yet included in the accepted cumulative PDF.

```sh
python3 examples/deep/ch01.py
python3 examples/deep/ch02.py
python3 scripts/build_deep_chapter.py --check
python3 scripts/build_deep_chapter02.py --check
python3 scripts/build_textbook_plan.py --check
make pdf
python3 -m pytest
python3 scripts/review_deep.py
```

Dependencies: Python 3.10+ (pytest; Pillow for page review), XeLaTeX/latexmk, librsvg, Poppler, and DejaVu fonts. The full historical numerical regression suite also uses the existing repository dependencies. The PDF gate rejects old, empty, later-chapter, unreviewed, or changed-after-review source. To author new material, build a preview under build/ and complete review before updating the acceptance record; do not weaken the gate.

## Frozen editions

astra-undergraduate-rewrite is a pedagogical archive, not a parallel manuscript. Its source, figures, examples and committed PDF remain byte-identical. The default tests verify its preserved publication without rebuilding it; make historical-pdf remains an explicit reproduction tool under build/. Main, astra-rewrite and historical snapshots are preserved; no main merge is part of this milestone.

The original eight-section [preproduction outline](CHAPTER_1_OUTLINE.md) is retained as design history. The actual chapter deliberately expands it to 12 sections and ten figures. Full source-access details live in [the chapter source review](research/deep-ch01-sources.md). Review is author-agent work, not independent scientific certification or a real-reader study.
