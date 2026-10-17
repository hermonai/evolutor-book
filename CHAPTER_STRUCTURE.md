# Evolutor — chapter structure and reading routes

Updated 17 October 2026. This is the current project-level navigation map.
Chapters **1–35 are authored and included** in the continuous review candidate;
Chapters **36–52 are inventoried packages, not integrated content**. Local
author review does not establish independent specialist review or publication acceptance.

The machine-readable companion is [chapter-structure.json](chapter-structure.json).
Run `python3 scripts/check-chapter-structure.py` to check all titles against
active sources, the 52-number spine, part coverage and acyclic prerequisites.
[BOOK_PLAN.md](BOOK_PLAN.md) and `book/book.json` retain their frozen acceptance
snapshot; they are not current progress counters. The map below reconciles
actual authored titles where they differ from that older plan.

## Architecture and boundaries

DOGMA is the non-Transformer DNA-native direction; Hermon DNA is the
Transformer-based direction. Evolutor owns the higher-level theory, compiler,
runtime and governance. A toy recurrence, a synthetic task and a profiled
production engine are different evidence levels.

General foundations precede biological abstractions; those precede model
proposals, fair experiments and engine lowering. The engines then feed
heterogeneous execution, industrial engineering and applications. Biological
mechanisms receive scientific illustrations; software mechanisms receive
state, tensor, memory and execution diagrams. No biological causation is
implied by a software arrow.

## Complete 52-chapter map

“Authored” means source present in the current assembly, not accepted publication.
Ch1–2 retain internal acceptance records; Ch3–21 retain existing review candidates;
Ch22–35 have source-bound local integration review. “Staged” means local gates
must still be rerun. Prerequisites below are reading dependencies, not a claim
that every prerequisite is independently accepted.

### Part 1 — The research question

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 1 | [Why Genomic Computation?](tex/deep/ch01.tex) | Authored | — |

### Part 2 — Learning and sequence-model foundations

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 2 | [Learning objectives, data, tasks, and evaluation](tex/deep/ch02.tex) | Authored | 1 |
| 3 | [Differentiation, optimization and tensor programs](tex/textbook/ch03.tex) | Authored | 2 |
| 4 | [Reproducible PyTorch training](drafts/ch04/manuscript.tex) | Authored | 3 |
| 5 | [Tokenization and sequence representation](drafts/ch05/manuscript.tex) | Authored | 2, 4 |
| 6 | [Recurrent models and gated state](drafts/ch06/manuscript.tex) | Authored | 3, 5 |
| 7 | [State-space models, selective updates and scans](drafts/ch07/manuscript.tex) | Authored | 6 |
| 8 | [Attention and content addressing](drafts/ch08/manuscript.tex) | Authored | 3, 5 |
| 9 | [Assembling a Transformer block](drafts/ch09/manuscript.tex) | Authored | 8 |
| 10 | [Conditional computation and routing](drafts/ch10/manuscript.tex) | Authored | 9 |

### Part 3 — From biology to formal computational hypotheses

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 11 | [Regulation and expression across levels](drafts/ch11/manuscript.tex) | Authored | 1, 2 |
| 12 | [Development and generated computational structure](drafts/ch12/manuscript.tex) | Authored | 11 |
| 13 | [Learning, structural adaptation and evolution](drafts/ch13/manuscript.tex) | Authored | 4, 12 |
| 14 | [Typed genomic computation systems](drafts/ch14/manuscript.tex) | Authored | 3, 11, 12 |
| 15 | [Operational semantics and expression traces](drafts/ch15/manuscript.tex) | Authored | 14 |
| 16 | [Expression complexity and resource semantics](drafts/ch16/manuscript.tex) | Authored | 15 |
| 17 | [Traces, credit and mechanistic evidence](drafts/ch17/manuscript.tex) | Authored | 2, 15, 16 |

### Part 4 — DOGMA: non-Transformer DNA-native computation

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 18 | [DOGMA primitives and state semantics](drafts/ch18/manuscript.tex) | Authored | 5, 7, 14 |
| 19 | [DOGMA regulation and selective transformations](drafts/ch19/manuscript.tex) | Authored | 18 |
| 20 | [Structured memory, locality and timescales](drafts/ch20/manuscript.tex) | Authored | 19 |
| 21 | [Strands, complements and dual-state hypotheses](drafts/ch21/manuscript.tex) | Authored | 5, 18, 20 |
| 22 | [DOGMA reference model and falsifiable research program](drafts/ch22/manuscript.tex) | Authored | 19, 20, 21 |

### Part 5 — Hermon DNA: Transformer-based DNA computation

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 23 | [Hermon DNA reference architecture](drafts/ch23/manuscript.tex) | Authored | 5, 9 |
| 24 | [DNA-aware Transformer mechanisms](drafts/ch24/manuscript.tex) | Authored | 5, 23 |

### Part 6 — Training systems and fair experiments

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 25 | [Shared experiments without false equivalence](drafts/ch25/manuscript.tex) | Authored | 2, 22, 23, 24 |
| 26 | [Training/inference parity and parallel recurrence](drafts/ch26/manuscript.tex) | Authored | 7, 22, 23 |
| 27 | [Optimization and memory-efficient training](drafts/ch27/manuscript.tex) | Authored | 4, 26 |
| 28 | [Distributed training and reproducible model artifacts](drafts/ch28/manuscript.tex) | Authored | 25, 27 |
| 29 | [Benchmark design and comparative evidence](drafts/ch29/manuscript.tex) | Authored | 25, 28 |

### Part 7 — DOGMA Engine: state-native inference

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 30 | [Runtime contracts and request lifecycles](drafts/ch30/manuscript.tex) | Authored | 16, 25 |
| 31 | [DOGMA state construction and execution](drafts/ch31/manuscript.tex) | Authored | 22, 30 |
| 32 | [DOGMA state pools and memory ownership](drafts/ch32/manuscript.tex) | Authored | 30, 31 |
| 33 | [DOGMA checkpoints, branching and prefix state](drafts/ch33/manuscript.tex) | Authored | 31, 32 |
| 34 | [DOGMA batching and state-native kernels](drafts/ch34/manuscript.tex) | Authored | 31, 32, 33 |

### Part 8 — Hermon DNA Engine: attention-native inference

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 35 | [Hermon DNA prefill, decode and KV state](drafts/ch35/manuscript.tex) | Authored | 8, 9, 23, 24, 30 |
| 36 | Paged KV, prefix sharing and allocation | Staged | 32, 35 |
| 37 | Continuous batching and precision | Staged | 34, 35, 36 |
| 38 | Speculative decoding and attention kernels | Staged | 29, 35, 36, 37 |

### Part 9 — Evolutor: heterogeneous execution

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 39 | Evolutor runtime above both engines | Staged | 14, 15, 30, 34, 35 |
| 40 | Hybrid compressed and addressable memory | Staged | 20, 35, 39 |
| 41 | Compiler, IR and execution planning | Staged | 14, 15, 16, 39 |
| 42 | Database engines as a systems comparison | Staged | 32, 36, 41 |
| 43 | Structural adaptation and lifecycle governance | Staged | 13, 17, 41 |

### Part 10 — Industrial engineering

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 44 | Packaging, deployment and observable services | Staged | 28, 30, 39 |
| 45 | Multi-tenancy, isolation and security | Staged | 30, 32, 33, 36, 44 |
| 46 | Distributed serving and state placement | Staged | 28, 36, 39, 45 |
| 47 | Profiling, performance and hardware backends | Staged | 16, 29, 34, 38, 46 |

### Part 11 — Applications and capability research

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 48 | Genomic sequence applications | Staged | 5, 21, 24, 25, 29 |
| 49 | Streaming, language, code and persistent agents | Staged | 29, 39, 40, 45 |
| 50 | Continual learning and population adaptation | Staged | 13, 27, 43 |
| 51 | AGI capability hypotheses and limits | Staged | 17, 29, 43, 48, 49, 50 |

### Part 12 — Research synthesis

| Ch. | Title and active source | Stage | Direct prerequisites |
|---|---|---|---|
| 52 | Failures, open problems and reproducible synthesis | Staged | 29, 43, 47, 48, 49, 50, 51 |

## The current engineering handoff

Chapter 34 lifts the actual Chapter 31 gated state across requests, using
Chapter 32 pins and Chapter 33 restored branches. It distinguishes inactive
identity, local token clocks, completion fences and logical traffic from
device performance. Chapter 35 caches the actual Chapter 23 Hermon stack
with learned absolute positions, per-layer KV and offset causal masks.

**Next: Chapter 36 — Paged KV, prefix sharing and allocation.** Preserve
Chapter 35's exact ordered logical K/V while changing physical placement.
Test full/partial blocks, fresh ownership, generation identity, prefix forks,
copy-on-write tails, eviction versus live references, and reclaim only at
reference-count zero. Chapter 37 then combines admission/batching and precision;
Chapter 38 evaluates speculative verification and optimized attention kernels.

## Reading routes

- **Model builder:** Ch2–10, then Ch18–29. Learn objectives and state semantics before comparing architectures.
- **Formal systems reader:** Ch11–17, then Ch39–43 (the latter are staged). Separate biological analogy from typed semantics and legal lowering.
- **Inference engineer:** Ch23, Ch25–30, Ch31–35; then planned Ch36–38. Keep scalar/full-model oracles when changing storage and scheduling.
- **Deployment engineer:** Ch28–30, Ch32–38, then staged Ch44–47. Do not infer production readiness from reference tests.
- **Application researcher:** Ch2, Ch5, Ch17, Ch21, Ch24–29, then staged Ch48–52. Require dataset, intervention and negative evidence.

## Production and publication gates

Every new chapter needs original authored LaTeX, derivations, literal tested
code, generated numerical evidence, mechanism-specific editable vectors/TXT,
worked exercises and primary-source access notes. Run standalone and cumulative
builds, inspect new pages in color and grayscale, then record source/PDF hashes.
Keep cumulative review scope explicit; new-chapter inspection is not whole-book QA.
Independent specialist/reader review, rights/source audit, cumulative editorial
and accessibility review remain open. A chapter count is not a completion claim.
