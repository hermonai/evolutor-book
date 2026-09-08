# Evolutor: deep technical edition

Status: canonical deep Chapters 1–2 are internally reviewed development manuscripts; Chapter 3 onward remains planned. Prior editions and the Chapter 1-only PDF are preserved. No new wet-lab result, trained model or engine benchmark is delivered. See [Chapter 2 production report](DEEP_CHAPTER_2_REPORT.md).

DOGMA = non-Transformer DNA-native model + DOGMA Engine; Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; Evolutor = broader genomic computation theory, research and eventual runtime above both.

## Knowledge organization and reading routes

### I · The research question

EVOD-01

- EVOD-01: programs; neural models; genomes; stored and expressed computation; development; adaptation.

### II · Learning and sequence-model foundations

EVOD-02 → EVOD-03 → EVOD-04 → EVOD-05 → EVOD-06 → EVOD-07 → EVOD-08 → EVOD-09 → EVOD-10

- EVOD-02: prediction; likelihood; splits; uncertainty; controls; capacity.
- EVOD-03: tensor shapes; gradients; autograd; optimization; numerical precision.
- EVOD-04: datasets; batching; masking; optimizer; checkpoints; seeds.
- EVOD-05: DNA tokens; k-mers; embeddings; positions; strand orientation.
- EVOD-06: RNN; LSTM; GRU; state transition; retention; gradients.
- EVOD-07: linear recurrence; S4/S5; selective SSM; Mamba; RWKV; chunking.
- EVOD-08: Q/K/V; scores; masks; heads; softmax; retrieval.
- EVOD-09: residuals; normalization; MLP; positions; blocks; KV; prefill; decode.
- EVOD-10: dispatch; MoE; retrieval; external memory; dynamic graphs; hybrid models.

### III · From biology to formal computational hypotheses

EVOD-11 → EVOD-12 → EVOD-13 → EVOD-14 → EVOD-15 → EVOD-16 → EVOD-17

- EVOD-11: biological regulation; stored modules; selection; execution; context.
- EVOD-12: genotype/phenotype; developmental encoding; compilation; program synthesis; NAS.
- EVOD-13: state change; parameter learning; structural learning; populations; selection.
- EVOD-14: alphabet; computational gene; genome; regulator; expression; state; trace.
- EVOD-15: configuration; transition; evaluation rule; effects; termination; trace.
- EVOD-16: stored size; routing; active work; state; communication; trace; adaptation.
- EVOD-17: logging; causal interventions; credit assignment; structural proposals.

### IV · DOGMA: non-Transformer DNA-native computation

EVOD-18 → EVOD-19 → EVOD-20 → EVOD-21 → EVOD-22

- EVOD-18: State; Regulator; Expression; Strand; Complement; Gate; Memory locus; Module; Trace.
- EVOD-19: regulation; expression; conditional state update; routing; ablation.
- EVOD-20: local/global state; modular memory; regulatory state; fast/slow state; capacity.
- EVOD-21: paired states; reverse complement; equivariance; causal streaming.
- EVOD-22: reference implementation; state trace; objective; baseline; ablation; negative evidence.

### V · Hermon DNA: Transformer-based DNA computation

EVOD-23 → EVOD-24

- EVOD-23: DNA tokenizer; Transformer blocks; output head; causal positions.
- EVOD-24: strand embeddings; motifs; k-mers; multi-scale positions; sparse/long context; retrieval.

### VI · Training systems and fair experiments

EVOD-25 → EVOD-26 → EVOD-27 → EVOD-28 → EVOD-29

- EVOD-25: data contracts; model interfaces; state types; losses; benchmarks.
- EVOD-26: sequential; chunked; scan; full sequence; incremental; gradients.
- EVOD-27: mixed precision; accumulation; checkpointing; optimizer state; stability.
- EVOD-28: data/tensor/pipeline parallelism; communication; sharding; formats; provenance.
- EVOD-29: oracles; budgets; multi-seed evaluation; capacity controls; causality; transplant tests.

### VII · DOGMA Engine: state-native inference

EVOD-30 → EVOD-31 → EVOD-32 → EVOD-33 → EVOD-34

- EVOD-30: request; model identity; state ownership; cancellation; streaming; errors.
- EVOD-31: prompt ingestion; native step; chunking; output head; state tracing.
- EVOD-32: allocation; reset; reuse; clone; isolation; temporary buffers.
- EVOD-33: checkpoint; restore; state clone; versioning; shared prefixes.
- EVOD-34: state-transition batching; scheduling; scans; locality; kernel profiling.

### VIII · Hermon DNA Engine: attention-native inference

EVOD-35 → EVOD-36 → EVOD-37 → EVOD-38

- EVOD-35: prefill; decode; cache layout; positions; memory growth.
- EVOD-36: pages; blocks; fragmentation; prefix cache; reference counting; eviction.
- EVOD-37: admission; prefill/decode scheduling; quantization; quality; tails.
- EVOD-38: draft/verify; acceptance; numerical parity; memory traffic; fused kernels.

### IX · Evolutor: heterogeneous execution

EVOD-39 → EVOD-40 → EVOD-41 → EVOD-42 → EVOD-43

- EVOD-39: planner; router; adapters; tools; retrieval; symbolic modules; trace.
- EVOD-40: compression; addressability; forgetting; retrieval; memory routing.
- EVOD-41: IR; typing; optimization; lowering; backend legality; cost model.
- EVOD-42: parser; logical plan; optimizer; physical operators; buffer pool; transactions.
- EVOD-43: proposals; validation; evaluation; promotion; rollback; lineage.

### X · Industrial engineering

EVOD-44 → EVOD-45 → EVOD-46 → EVOD-47

- EVOD-44: versioning; APIs; tracing; metrics; streaming; fault handling; rollback.
- EVOD-45: ownership; quotas; untrusted inputs; tool authority; state leakage; threat model.
- EVOD-46: replication; partitioning; tensor/pipeline parallelism; sharding; migration.
- EVOD-47: TTFT; ITL; throughput; memory; power; utilization; roofline intuition.

### XI · Applications and capability research

EVOD-48 → EVOD-49 → EVOD-50 → EVOD-51

- EVOD-48: regulatory sequence analysis; motifs; long context; strand symmetry; uncertainty.
- EVOD-49: statistics; retrieval; copying; code; tools; persistent state; planning.
- EVOD-50: transfer; forgetting; structural search; populations; open-ended learning.
- EVOD-51: reasoning; planning; world models; transfer; tools; self-modification; generalization.

### XII · Research synthesis

EVOD-52

- EVOD-52: failed mechanisms; causality leaks; capacity confounds; negative results; historical lineage.

Arrows here indicate reading order, not extra hard prerequisites. Use PREREQUISITE_GRAPH.md for minimal dependency closure. Domain abstractions are deliberate: explain the mapping, preserved properties and omitted phenomena.
