# Chapter 3 review and scientific-architecture checkpoint

12 September 2026. Author review, not independent acceptance.

## Delivered chapter

Differentiation, optimization and tensor programs: 4222 whitespace-delimited manuscript words,
12 original editable SVG figures with semantic TXT companions, 12 worked exercises,
a glossary, tested boundary diagnostics and a source ledger. The standalone
review PDF has 21 pages, including its contents and appendices.

The PDF skill's render-and-inspect workflow informed the final layout: a separate
contents page, captions kept with figures, legible vector labels and checked page
boundaries. Every page was inspected in contact sheets; the eight new figures
across both books were also inspected at their native rasterized size.
A grayscale sample covers the new mechanism figures. No independent
biologist, mathematician or reader approval is implied.

PDF SHA-256: e5ca2ed5935253163917e4898b0a900864be49c12c3b177b3b70b4e010001732

Machine-readable provenance: [Chapter 3 review record](artifacts/deep/ch03-review.json).
Reproduction: [Chapter 3 README](drafts/ch03/README.md).

## Requested architecture report

| No. | Field | Finding |
| --- | --- | --- |
| 1 | Starting commit | 8ee4777976af0a68a01d2662cdd746ba0dfe49da |
| 2 | Branch | astra-deep-rewrite |
| 3 | Repository status | Clean at architecture-pass entry. This checkpoint changes only bounded research/Chapter 3 assets and their checks; generated PDF/render output is gitignored. |
| 4 | Completed chapters preserved | Accepted Chapters 1-2, canonical chapter count, review manifest and published PDF bytes are unchanged. No new acceptance hashes substitute for earlier review. |
| 5 | Scientific sources inspected | Baydin et al. AD survey (relevant sections); versioned PyTorch 2.10 docs; Alberts genetic-switch discussion. Caduceus and CrossDNA primary abstracts inform the architecture audit; full-paper coverage and benchmark replication are not claimed. |
| 6 | Current strengths | Manual matrix adjoints, automatic/numerical checks, negative controls, normalization accounting and explicit separation of biological regulation from software differentiation. |
| 7 | Missing scientific domains | Mechanism-specific transfer evidence for regulation, state organization, development and structural variation. A naming analogy does not establish useful genomic computation. |
| 8 | Missing mathematical foundations | General nonsmooth optimization, surrogate/search estimators, stochastic-state treatment and broader convergence theory remain beyond the declared fixtures. |
| 9 | Missing computational foundations | Complete DOGMA operator semantics, Hermon intervention definitions, trained reference models and engine parity; none is inferred from the toy tensor program. |
| 10 | Missing experimental foundations | Leakage-resistant datasets, preregistered budgets, repeated-seed training, restart equivalence and intervention/ablation studies. |
| 11 | Visual weaknesses addressed | Replaced the four remaining storyboard-only entries with original SVG/TXT pairs. Protein occupancy, antiparallel DNA and population cartoons are distinct from algorithmic boxes. These are pedagogical schematics, not atomistic models. Chapter-wide specialist review is still required. |
| 12 | Recommended Parts | Retain twelve: research question; learning foundations; biological hypotheses; DOGMA; Hermon DNA; training; DOGMA Engine; Hermon DNA Engine; Evolutor; industrial engineering; applications; synthesis. |
| 13 | Recommended chapters | Retain the 52-chapter curriculum, including separate architecture, training, reference inference and specialized-engine tracks. |
| 14 | Chapters retained | All canonical chapter IDs and prerequisite ordering are retained. Chapters 1-2 remain accepted; Chapter 3 is a review candidate. |
| 15 | Chapters deepened | Chapter 3 now adds hard selection, momentum state, controlled numerical differentiation and a training-lifecycle handoff. Later deepen-in-place entries remain plans. |
| 16 | Chapters moved | None. |
| 17 | Chapters split or merged | None. |
| 18 | New chapters | None beyond continuing the already-started Chapter 3. No Chapter 4 manuscript was generated. |
| 19 | Dependency DAG | docs/scientific-dependencies.json and .txt retain the canonical ordered acyclic graph. Cross-book imports remain explicit in the chapter map. |
| 20 | Master architecture | docs/DEEP_SCIENTIFIC_BOOK_ARCHITECTURE.md and research/figures/scientific-master.svg/.txt; not a replacement acceptance manifest. |
| 21 | Animation plan | docs/SCIENTIFIC_VISUAL_MAP.md preserves chapter keyframe plans. New mechanism assets are static editable vectors; no completed video or new animation sequence is claimed. |
| 22 | Executable progression | Checked tensor program → reproducible PyTorch training → minimal defined DOGMA and Transformer-baseline Hermon interventions → reference inference parity → profiling and specialized engines. |
| 23 | Source/research map | research/scientific-recalibration-sources.md, domain-specific research maps and drafts/ch03/sources.md. Access-depth limits are explicit; preserved maps remain under research/pre-recalibration/. |
| 24 | Checks passed | Final validation counts are recorded below. All 12 chapter SVGs plus the master map passed browser text-bound checks; the PDF has no extracted words outside page boundaries or missing-character build warnings. |
| 25 | Commits | Architecture: a2a6aa2. Chapter work: the bounded feat(book) commit containing this report; includes a navigation shim for an archived relative link. |
| 26 | Push status | Not pushed. No remote publication or repository settings changed. |
| 27 | Exact next bounded chapter | First close Chapter 3 independent/cumulative acceptance gates. Then EVOD-04: Reproducible PyTorch training, including restart equivalence and held-out evaluation. |
| 28 | DOGMA taxonomy verification | Non-Transformer DNA-native research track, consistently represented in the curriculum, shared terminology and master map. |
| 29 | Hermon DNA taxonomy verification | Transformer-based genomic research track; not interchangeable with DOGMA. |
| 30 | Genomic mechanisms investigated | Pairing/orientation, transcriptional control, regulated expression and state organization are mapped; the new chapter specifically illustrates repressor/promoter occupancy and its abstraction boundary. |
| 31 | Prior-art conflicts | Caduceus already supplies reverse-complement-equivariant bidirectional sequence modeling; CrossDNA already investigates cross-strand communication. Dual strands, gating or biological labels alone cannot support novelty. Access was abstract-level here. |
| 32 | DOGMA architecture gaps | State types, legal local operators, routing/search rules, update semantics, complexity and nearest ordinary recurrence/SSM baseline must be specified and tested. |
| 33 | Hermon DNA architecture gaps | Fix the reference Transformer, select one mechanistic intervention, define causality and symmetry conventions, then ablate under equal budgets. |
| 34 | Training-system gaps | Data lineage, masks/denominators, split integrity, optimizer/RNG/data-cursor checkpointing and repeatable end-to-end runs. |
| 35 | Inference-engine gaps | Reference-state semantics and parity before fused kernels, cache/state compression, scheduling or speed claims. |
| 36 | Evolutor-system gaps | Evidence registry, heterogeneous state ownership, selection policy and a demonstrated benefit over an ordinary experiment runner. |
| 37 | Strongest falsifiable hypotheses | A precisely specified regulation or memory operator may improve a preregistered task under matched information and compute budgets; removing it should erase the effect. Reverse-complement interventions can be tested directly for their stated invariance/equivariance. |
| 38 | Weakest current hypotheses | Biological naming implies novelty; genomic organization alone implies intelligence; dual strands imply general superiority; structural growth implies generality. None is accepted. |
| 39 | Historical claims requiring revalidation | Priority, architecture-family labels, dual-strand novelty, claimed biological equivalences, speed comparisons and any capabilities asserted without reproducible evidence. |
| 40 | Recommended experimental sequence | Define semantics → establish trivial/local and nearest-family baselines → unit/gradient/causality checks → frozen splits/budgets → one intervention with ablation → repeated-seed held-out results → restart/reference-inference parity → profile → specialize only measured bottlenecks. |

## Validation and limitations

Final regression result: 232 passed in 92.36 seconds.
Scientific architecture/figure regeneration checks and git whitespace checks passed.

The initial shell selected Python 3.9 without PyTorch; validation was rerun using
Python 3.13.6 with PyTorch 2.10.0. A later preservation test caught the review PDF
changing while its renderer and the regression suite ran concurrently. No
preservation assertion was weakened; final validation runs after all PDF writes.
The accepted Chapter 1-2 manifest and published release remain unchanged.

Scientific acceptance is still open: independent review, cumulative source
integration, consistent final figure numbering, bibliography and index must be
completed before promoting the chapter. The source ledger preserves earlier
pass notes and marks what the current extension supersedes. No new wet-lab
result, trained genomic model, specialized engine, speedup or novelty claim is made.
