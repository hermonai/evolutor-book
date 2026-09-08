# Deep Chapter 2 production report

Review date: 9 September 2026. Scope: author-agent-reviewed development manuscript, not an independently certified edition.

## Release surface

- Starting commit: `b319a6abcc834e3630855556761e9ea5714cc3dd`; branch: `astra-deep-rewrite`.
- Chapter: **Learning objectives, data, tasks, and evaluation**, [source](tex/deep/ch02.tex).
- 20 sections; 18 body pages (printed 15–32, physical 19–36).
- [Cumulative Chapters 1–2 PDF](output/pdf/deep-evolutor-ch01-02.pdf): 41 pages including front matter, glossaries, bibliography and index.
- 13 original editable SVG figures, 13 semantic TXT companions, nine static keyframes (split construction, future intervention and experiment lifecycle). These are not exported moving media.
- Twelve exercises and twelve worked solutions; 12 distinct sources cited in Chapter 2, 21 entries in the cumulative bibliography.
- [Storyboard](pedagogy/deep-ch02-storyboard.json), [source-access ledger](research/deep-ch02-sources.md), [executable companion](examples/deep/ch02.py), [computed results](artifacts/deep/ch02-results.json).

## Scientific and skeptical review

The chapter separates data, task, training objective, model and evaluation protocol through explicit information contracts. Autoregressive input/target shifts are defined before discussing masks. Genomic sequence tokenization is software representation, not evidence of molecular computation or general intelligence.

The random-data bound is derived using conditional KL divergence: expected fresh iid uniform next-base loss cannot beat ln(4) with only permitted information. It is not a lower bound on every finite sample or memorized training set. Overlapping three-mers share two bases and therefore have only ln(4), not ln(64), next-token conditional entropy under that process. Bits per base and perplexity retain their proper scoring denominators.

Dataset splitting takes connected components of exact/reverse-complement and declared metadata conflicts, including transitive relations. Row-order invariance and cross-fold constraints are tested. Unknown homology, coordinate overlap and phylogenetic proximity are not detected by this small reference; they require additional relationship construction and a claim-appropriate split.

The existing causality helper now rejects nonfinite/malformed outputs, validates input assumptions, clones reference prefixes and restores per-module train/eval modes even after errors. Finite interventions at seven boundaries distinguish PrefixCounts (difference zero) from the deliberate FutureCopy leak (difference eight). This does not prove universal causality; tests discuss suffix transformations that can leave a noncausal function unchanged.

The fixed child specification EVO-EXP01-CH02-SMOKE precedes execution and is bound to results by SHA-256. Three seeds (11,29,47) use CPU PyTorch 2.10.0, no training. The uniform reference gives ln(4); the leaky diagnostic gives about 0.001006 nats/base. It scores 248 targets, whereas full-length references score 256: the chapter explicitly rejects treating those displays as a fair model ranking.

Capacity is a vector, not just parameter count. The toy same-width formulas yield 384 versus 2,176 parameters, not counts for implemented DOGMA or Hermon models. Removal and transplant tests distinguish local contribution from transfer. The values 0.51,0.97,0.99 are marked illustrative; three points cannot establish bimodality or explain a failure. Exact delay-oracle tests, balanced memory tasks, shortcut audits, training budgets and engine-parity controls establish prerequisites for later experiments.

## Publication review

All 41 cumulative pages were rendered and visually inspected. Revisions corrected swapped entropy/intervention asset references, entropy-panel spacing and whole-function code pagination. Numerical tables are generated from actual result artifacts. Captions, equations, code, glossary, bibliography and index were checked; all nine Chapter 2 frames and representative grayscale pages were inspected. No clipping, overlapping labels, unresolved references or layout warnings remain in the reviewed build.

The source-bound [acceptance record](artifacts/deep/ch02-review.json) covers the cumulative source surface, including the reused causality helper and fixed experiment specification. Chapter 1 source, apparatus, review and all existing PDF bytes remain unchanged against the starting commit.

## Verification

Full repository run: **171 passed**, zero failures or skips, using Python 3.13.6. This includes 48 dedicated Chapter 2 tests and a healthy-copy control for the cumulative review gate. Existing tests remain enabled; milestone assertions now accept exactly Chapters 1–2 and still reject Chapter 3.

`make pdf` passes the source-bound acceptance gate, both chapter artifact freshness checks and LaTeX log validation. The full suite includes generated-plan freshness, citation/asset closure, independent expected results and preservation checks. No errors, missing glyphs, undefined references or overfull boxes were reported.

## Limits, consistency and next dependency

No model was trained; no DOGMA/Hermon implementation, genomic benchmark, systems benchmark or AGI result was established. Parent studies EVO-EXP01 through EVO-EXP05 remain NOT RUN. The CPU child diagnostic is recorded in the existing [experiment ledger](research/experiment-ledger.md).

DOGMA = non-Transformer DNA-native model + DOGMA Engine; Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; Evolutor = broader theory/research/compiler/runtime above both. This taxonomy agrees with Chapter 1 and Book I. Biology and chemistry are imported from Book I without equating analogy to mechanism.

Review was performed by the authoring agent; no independent Academic/Science dossier or reviewer was available. Independent subject review, reader testing and accessible tagged publication remain open; the PDF is not certified PDF/UA.

The next planned chapter is **Differentiation, optimization and tensor programs**. It should derive parameter updates and executable tensor semantics before architecture baselines. No Chapter 3 source was implemented.
