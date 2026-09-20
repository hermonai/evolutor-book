# Editorial architecture and release roadmap

Updated 20 September 2026. This is the current execution map, not a claim
that every planned chapter is written or independently reviewed.

## One manuscript, distinct review stages

Retain the 52-chapter spine in BOOK_PLAN.md. Its generated status describes
the frozen canonical acceptance snapshot; use this map and the root README
for current authoring progress. Do not regenerate archived editions merely
to change their progress labels.

Chapters 1-2 retain their internal acceptance records. Chapter 3 has standalone
and combined LaTeX review candidates. Chapters 4-8 have isolated authored-LaTeX
review candidates with code, vector figures, and worked solutions.
Chapter 9 is the next unwritten chapter in this authoring sequence.
Independent specialist review and cumulative integration are still open.

## Give each architectural layer a distinct responsibility

| Chapter group | Owned question and evidence | Boundary against duplication or overclaim |
|---|---|---|
| 1-5: foundations and experimental contract | What is the objective, what is differentiated, what is reproduced, and what does a token mean? Small executable contracts. | No architecture wins established by an attractive diagram |
| 6-10: sequence mechanisms | How do recurrence, state-space updates, attention, Transformers, and conditional computation work? Derivations, transparent reference code, forward and gradient oracles. | Not complete genomic models or optimized production kernels |
| 11-17: biology to formal semantics | Which regulatory mechanisms motivate which typed abstractions? Explicit mappings and counterexamples. | Biological resemblance is not biological equivalence |
| 18-24: model directions | DOGMA is non-Transformer DNA-native research; Hermon DNA is Transformer-based. Specify each model's semantics and testable hypotheses. | Do not infer those identities from the Chapter 7 diagonal toy |
| 25-29: comparison and execution | Shared evaluation, full-model sequential/chunk/scan parity, training memory, distribution, and benchmarks. | Chapter 26 extends Chapter 7 with model-scale boundaries and precision; it does not repeat the affine-scan proof |
| 30-38: engines | How do model semantics become measurable execution in DOGMA Engine and Hermon DNA Engine? Memory layout, correctness, and profiled kernels. | Operation counts alone do not establish speedups |
| 39-43: Evolutor layer | How do research abstractions become an auditable compiler and runtime above both directions? Typed contracts and legal transformations. | Compiler legality is separate from learned capability |
| 44-47: industrial operation | What is required for reproducibility, deployment, and operational reliability? Explicit failure handling and evidence. | Do not label a reference implementation production-ready |
| 48-52: applications and synthesis | What task-specific evidence supports usefulness, and what remains a hypothesis? Baselines, interventions, and failures. | No AGI or biological discovery claims from synthetic examples |

Keep the learning order: token identity and record boundaries (5), carried
state versus gradient history (6), input-selected affine state and legal
scan composition (7), then content-addressed history (8). The reader should
understand why an attention cache is a different representation before
implementing a complete Transformer in Chapter 9.

## Chapter 8 scope (standalone candidate): attention and content addressing

Start with a small hand-computed retrieval problem. Introduce query, key,
value, score scaling, masking, normalization, and weighted aggregation in
that order; annotate tensor dimensions at every change of representation.
Derive a causal attention reference and compare values and gradients with
an independent library oracle.

Show why masked future tokens cannot affect earlier outputs, how record
boundaries differ from simple padding, and why all-masked rows need an
explicit policy. Derive a minimal cached decode path, then test it against
full causal execution. Cache semantics and an operation-count model belong
here; hardware speed claims and optimized kernels belong in the later
systems chapters.

Keep the sequence-model explanation general and use DNA examples only where
their semantics are explicit. Biology figures should depict real mechanisms;
algorithm figures should expose computation, not imply molecular causation.

## Next chapter brief: assembling a Transformer block

Integrate Chapter 8 attention with position handling, normalization,
residual paths, and a feed-forward sublayer. Trace one token through a
complete, explicitly chosen pre-normalized block. State tensor shapes and
parameter ownership; distinguish architecture choices from universal rules.

Test residual and normalization derivatives, causal full/chunk parity
through the entire block, and a small training objective with shifted
targets and padding excluded from loss. Include failures caused by
inconsistent positions and accidentally active dropout. Hardware benchmarks
and biological capability claims remain outside the reference's scope.

## Quality gates before widening the manuscript

1. Complete a reproducible chapter: explanations, derivations, documented
   source access, tested examples, worked exercises, and figure TXT companions.
   Validate displayed numerical labels, not only underlying code.
2. Inspect every rendered page in color and grayscale. Audit tensor shapes,
   causal dependencies, state ownership, and gradient paths separately from
   layout. Hash the reviewed source set and PDF.
3. Obtain independent specialist and reader review; record corrections.
   Author-agent review does not satisfy this gate.
4. After Chapter 10, prepare a combined Chapters 1-10 integration candidate:
   reconcile notation, shared examples, prerequisites, citations, index,
   and the model/runtime vocabulary. Reviews may start before this milestone.
5. Advance cumulative acceptance only through the existing gates. Do not
   treat chapter PDF generation as acceptance of the whole architecture.

Use predict, derive, implement, compare, break, and explain as the recurring
teaching progression. Reuse contracts while increasing scope; do not repeat
entire mechanisms. Favor depth and clear causal explanations over either
artificial simplicity or an arbitrary manuscript length.
