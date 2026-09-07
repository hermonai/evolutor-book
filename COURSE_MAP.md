# Evolutor: deep technical edition

Status: canonical deep Chapter 1 is an internally reviewed prototype; all later chapters remain plans. The undergraduate edition is frozen. No trained model, engine or wet-lab result is delivered. See [production report](DEEP_CHAPTER_1_REPORT.md) and [edition strategy](CANONICAL_EDITION_STRATEGY.md).

DOGMA = non-Transformer DNA-native model + DOGMA Engine; Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; Evolutor = broader genomic computation theory, research and eventual runtime above both.

## Chapter dependencies, mechanisms and exit tasks

Entry assumptions: Basic programming and algorithmic reasoning; Algebra, functions, sets and discrete mathematical maturity; Basic probability, vectors, matrices and first-year calculus; DNA Computing or demonstrated equivalent molecular/formal knowledge; named imports remain planned until taught.

### EVOD-01 — Why Genomic Computation?

**Required earlier chapters:** Declared entry assumptions.

**Book I imports:** DNAD-30, DNAD-32. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** programs; neural models; genomes; stored and expressed computation; development; adaptation.

**Formal/mathematical development:** Use provisional typed selection/execution maps after a concrete module example; novelty remains a question.

**Implementation / assessment:** Compare conventional conditional execution with a proposed genomic organization and identify a falsifier.

**Enables:** EVOD-02, EVOD-11.

### EVOD-02 — Learning objectives, data and evaluation

**Required earlier chapters:** EVOD-01.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** prediction; likelihood; splits; uncertainty; controls; capacity.

**Formal/mathematical development:** Derive a sequence likelihood and loss; separate training fit from held-out generalization.

**Implementation / assessment:** Construct a leakage-resistant split and hand-check loss and calibration on a tiny dataset.

**Enables:** EVOD-03, EVOD-04, EVOD-05.

### EVOD-03 — Differentiation, optimization and tensor programs

**Required earlier chapters:** EVOD-02.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** tensor shapes; gradients; autograd; optimization; numerical precision.

**Formal/mathematical development:** Derive chain-rule gradients for a small network and annotate every dimension.

**Implementation / assessment:** Check autograd with finite differences and demonstrate numerical failure cases.

**Enables:** EVOD-04, EVOD-06, EVOD-08, EVOD-27.

### EVOD-04 — Reproducible PyTorch training

**Required earlier chapters:** EVOD-02, EVOD-03.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** datasets; batching; masking; optimizer; checkpoints; seeds.

**Formal/mathematical development:** Relate code to the objective and masking assumptions; distinguish resumption from reproducibility.

**Implementation / assessment:** Implement a reference training loop with exact small cases and restart tests.

**Enables:** EVOD-05, EVOD-09, EVOD-13, EVOD-22, EVOD-25, EVOD-27.

### EVOD-05 — Tokenization and sequence representation

**Required earlier chapters:** EVOD-02, EVOD-04.

**Book I imports:** DNAD-05, DNAD-25. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** DNA tokens; k-mers; embeddings; positions; strand orientation.

**Formal/mathematical development:** Derive vocabulary and sequence-length tradeoffs; state reverse-complement alignment conventions.

**Implementation / assessment:** Test tokenization round trips and orientation handling without future leakage.

**Enables:** EVOD-06, EVOD-08, EVOD-21, EVOD-23.

### EVOD-06 — Recurrent models and gated state

**Required earlier chapters:** EVOD-03, EVOD-05.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** RNN; LSTM; GRU; state transition; retention; gradients.

**Formal/mathematical development:** Derive one-step and unrolled computations and identify vanishing/exploding gradient mechanisms.

**Implementation / assessment:** Compare recurrent baselines on copying and running statistics with matched controls.

**Enables:** EVOD-07, EVOD-10.

### EVOD-07 — State-space models, selective updates and scans

**Required earlier chapters:** EVOD-06.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** linear recurrence; S4/S5; selective SSM; Mamba; RWKV; chunking.

**Formal/mathematical development:** Derive an associative scan for a valid linear case and show where state-dependent nonlinearities break it.

**Implementation / assessment:** Test sequential/chunked/scan parity and review strong primary-source baselines.

**Enables:** EVOD-10, EVOD-16, EVOD-18, EVOD-20, EVOD-26, EVOD-34.

### EVOD-08 — Attention and content-addressed computation

**Required earlier chapters:** EVOD-03, EVOD-05.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** Q/K/V; scores; masks; heads; softmax; retrieval.

**Formal/mathematical development:** Derive shaped attention from weighted lookup; distinguish addressability from exact recall.

**Implementation / assessment:** Implement a small attention oracle and causal masking tests.

**Enables:** EVOD-09.

### EVOD-09 — Transformers and cached execution

**Required earlier chapters:** EVOD-04, EVOD-08.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** residuals; normalization; MLP; positions; blocks; KV; prefill; decode.

**Formal/mathematical development:** Derive a complete decoder block and full versus incremental equivalence under declared positions.

**Implementation / assessment:** Verify logits and K/V across full and cached execution.

**Enables:** EVOD-10, EVOD-16, EVOD-23, EVOD-26, EVOD-35.

### EVOD-10 — Conditional computation and memory alternatives

**Required earlier chapters:** EVOD-06, EVOD-07, EVOD-09.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** dispatch; MoE; retrieval; external memory; dynamic graphs; hybrid models.

**Formal/mathematical development:** Separate routing cost, active computation and memory access; compare mechanisms without renaming them.

**Implementation / assessment:** Build an ordinary routed baseline and account for inactive parameter storage.

**Enables:** EVOD-11, EVOD-12, EVOD-14, EVOD-19, EVOD-24, EVOD-40, EVOD-42.

### EVOD-11 — Regulation and expression across levels

**Required earlier chapters:** EVOD-01, EVOD-10.

**Book I imports:** DNAD-30. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** biological regulation; stored modules; selection; execution; context.

**Formal/mathematical development:** Give distinct biological and software interpretations and a typed selection map.

**Implementation / assessment:** Compare a regulatory proposal to gates, dispatch and MoE with an explicit equivalence test.

**Enables:** EVOD-12, EVOD-13, EVOD-14.

### EVOD-12 — Development and generated computational structure

**Required earlier chapters:** EVOD-10, EVOD-11.

**Book I imports:** DNAD-30. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** genotype/phenotype; developmental encoding; compilation; program synthesis; NAS.

**Formal/mathematical development:** Formulate a candidate development map and compare it to established program/network generation.

**Implementation / assessment:** Generate a small executable structure and test whether development adds value over direct encoding.

**Enables:** EVOD-13, EVOD-14, EVOD-41.

### EVOD-13 — Learning, structural adaptation and evolution

**Required earlier chapters:** EVOD-04, EVOD-11, EVOD-12.

**Book I imports:** DNAD-30. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** state change; parameter learning; structural learning; populations; selection.

**Formal/mathematical development:** Specify which object changes, at what timescale, with what objective and inheritance rule.

**Implementation / assessment:** Contrast one state update, optimizer step, structural proposal and population generation.

**Enables:** EVOD-14, EVOD-17, EVOD-43, EVOD-50.

### EVOD-14 — Typed genomic computation systems

**Required earlier chapters:** EVOD-10, EVOD-11, EVOD-12, EVOD-13.

**Book I imports:** DNAD-16, DNAD-18, DNAD-32. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** alphabet; computational gene; genome; regulator; expression; state; trace.

**Formal/mathematical development:** Derive typed interfaces from examples; re-evaluate the old tuple rather than canonizing it.

**Implementation / assessment:** Build a minimal interpreter with types, invariants and a conventional baseline.

**Enables:** EVOD-15, EVOD-18, EVOD-39, EVOD-41.

### EVOD-15 — Operational semantics and expression traces

**Required earlier chapters:** EVOD-14.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** configuration; transition; evaluation rule; effects; termination; trace.

**Formal/mathematical development:** Define a small-step semantics and prove a bounded correspondence with the reference interpreter.

**Implementation / assessment:** Compare exact transition traces; test invalid configurations and causal ordering.

**Enables:** EVOD-16, EVOD-17, EVOD-18, EVOD-30, EVOD-39, EVOD-41.

### EVOD-16 — Expression complexity and resource semantics

**Required earlier chapters:** EVOD-07, EVOD-09, EVOD-15.

**Book I imports:** DNAD-04, DNAD-24. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** stored size; routing; active work; state; communication; trace; adaptation.

**Formal/mathematical development:** Reassess expression-size complexity against a cost vector with units and worst-case quantifiers.

**Implementation / assessment:** Construct a counterexample where fewer active modules cost more overall.

**Enables:** EVOD-17, EVOD-18, EVOD-20, EVOD-23, EVOD-29, EVOD-40, EVOD-41, EVOD-42.

### EVOD-17 — Traces, credit and mechanistic evidence

**Required earlier chapters:** EVOD-13, EVOD-15, EVOD-16.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** logging; causal interventions; credit assignment; structural proposals.

**Formal/mathematical development:** Distinguish observed activation traces from causal explanations and useful adaptation signals.

**Implementation / assessment:** Ablate trace-guided proposals against logging and random-selection controls.

**Enables:** EVOD-19, EVOD-22, EVOD-29, EVOD-43.

### EVOD-18 — DOGMA primitives and state semantics

**Required earlier chapters:** EVOD-07, EVOD-14, EVOD-15, EVOD-16.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** State; Regulator; Expression; Strand; Complement; Gate; Memory locus; Module; Trace.

**Formal/mathematical development:** Define candidate primitives by type and transition; compare each with nearest recurrent or conditional baseline.

**Implementation / assessment:** Implement only a minimal candidate after its semantics; reject redundant biological terminology.

**Enables:** EVOD-19, EVOD-20, EVOD-21, EVOD-31.

### EVOD-19 — DOGMA regulation and selective transformations

**Required earlier chapters:** EVOD-10, EVOD-17, EVOD-18.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** regulation; expression; conditional state update; routing; ablation.

**Formal/mathematical development:** Derive candidate R/E/U maps and compare gates, selection and dispatch algebraically.

**Implementation / assessment:** Measure one-mechanism ablations with state/logit/gradient checks.

**Enables:** EVOD-20, EVOD-22.

### EVOD-20 — Structured memory, locality and timescales

**Required earlier chapters:** EVOD-07, EVOD-16, EVOD-18, EVOD-19.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** local/global state; modular memory; regulatory state; fast/slow state; capacity.

**Formal/mathematical development:** Specify ownership, updates, resets and capacity; no infinite-context or constant-total-memory claim.

**Implementation / assessment:** Test retention, interference and reset behavior at matched memory and parameter budgets.

**Enables:** EVOD-21, EVOD-22, EVOD-32, EVOD-40.

### EVOD-21 — Strands, complements and dual-state hypotheses

**Required earlier chapters:** EVOD-05, EVOD-18, EVOD-20.

**Book I imports:** DNAD-05, DNAD-30. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** paired states; reverse complement; equivariance; causal streaming.

**Formal/mathematical development:** Separate offline symmetry from causal inference; formalize a candidate interaction and augmentation control.

**Implementation / assessment:** Detect reverse-complement future leakage; compare dual-state with augmentation and equivariant baselines.

**Enables:** EVOD-22, EVOD-24.

### EVOD-22 — DOGMA reference model and falsifiable research program

**Required earlier chapters:** EVOD-04, EVOD-17, EVOD-19, EVOD-20, EVOD-21.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** reference implementation; state trace; objective; baseline; ablation; negative evidence.

**Formal/mathematical development:** Fix prediction timing after consumed tokens and precise state/logit contracts.

**Implementation / assessment:** Train a small candidate only after exact tests; retain losing hypotheses and failure reports.

**Enables:** EVOD-25, EVOD-26, EVOD-29, EVOD-31.

### EVOD-23 — Hermon DNA reference architecture

**Required earlier chapters:** EVOD-05, EVOD-09, EVOD-16.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** DNA tokenizer; Transformer blocks; output head; causal positions.

**Formal/mathematical development:** Specify a recognizably Transformer reference with all tensor shapes and attention semantics.

**Implementation / assessment:** Train a small controlled reference and test full/incremental parity.

**Enables:** EVOD-24, EVOD-25, EVOD-26, EVOD-35.

### EVOD-24 — DNA-aware Transformer mechanisms

**Required earlier chapters:** EVOD-10, EVOD-21, EVOD-23.

**Book I imports:** DNAD-25, DNAD-30. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** strand embeddings; motifs; k-mers; multi-scale positions; sparse/long context; retrieval.

**Formal/mathematical development:** Define each modification as a testable change to the baseline, including symmetry and causality.

**Implementation / assessment:** Run one-factor ablations and matched-budget DNA-task controls; no biomedical success implied.

**Enables:** EVOD-25, EVOD-29, EVOD-48.

### EVOD-25 — Shared experiments without false equivalence

**Required earlier chapters:** EVOD-04, EVOD-22, EVOD-23, EVOD-24.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** data contracts; model interfaces; state types; losses; benchmarks.

**Formal/mathematical development:** Separate common evaluation interfaces from family-specific recurrent and KV states.

**Implementation / assessment:** Build compatible prepare/step contracts with explicit logits versus sampled tokens.

**Enables:** EVOD-26, EVOD-27, EVOD-28, EVOD-30.

### EVOD-26 — Training/inference parity and parallel recurrence

**Required earlier chapters:** EVOD-07, EVOD-09, EVOD-22, EVOD-23, EVOD-25.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** sequential; chunked; scan; full sequence; incremental; gradients.

**Formal/mathematical development:** State tolerances and valid equivalences; test outputs and internal state, not just loss.

**Implementation / assessment:** Compare state/logit/gradient trajectories and deliberately broken masks or scans.

**Enables:** EVOD-27, EVOD-28, EVOD-29, EVOD-30, EVOD-31, EVOD-34, EVOD-35, EVOD-38.

### EVOD-27 — Optimization and memory-efficient training

**Required earlier chapters:** EVOD-03, EVOD-04, EVOD-25, EVOD-26.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** mixed precision; accumulation; checkpointing; optimizer state; stability.

**Formal/mathematical development:** Derive effective batch and memory accounting; distinguish recomputation from saved state.

**Implementation / assessment:** Measure loss/gradient drift, memory and restart fidelity under one optimization at a time.

**Enables:** EVOD-28, EVOD-29, EVOD-37.

### EVOD-28 — Distributed training and model artifacts

**Required earlier chapters:** EVOD-25, EVOD-26, EVOD-27.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** data/tensor/pipeline parallelism; communication; sharding; formats; provenance.

**Formal/mathematical development:** Derive communication and memory consequences; identify model/state schema version boundaries.

**Implementation / assessment:** Specify small distributed parity and fault-recovery tests; benchmark only measured configurations.

**Enables:** EVOD-30, EVOD-32, EVOD-33, EVOD-36, EVOD-44, EVOD-46.

### EVOD-29 — Benchmark design and comparative evidence

**Required earlier chapters:** EVOD-16, EVOD-17, EVOD-22, EVOD-24, EVOD-26, EVOD-27.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** oracles; budgets; multi-seed evaluation; capacity controls; causality; transplant tests.

**Formal/mathematical development:** Define estimands, uncertainty and a full resource vector before comparing families.

**Implementation / assessment:** Build a benchmark matrix including copying, retrieval, statistics, motifs and state-machine tasks.

**Enables:** EVOD-37, EVOD-38, EVOD-40, EVOD-43, EVOD-47, EVOD-48, EVOD-49, EVOD-50, EVOD-51, EVOD-52.

### EVOD-30 — Runtime contracts and request lifecycles

**Required earlier chapters:** EVOD-15, EVOD-25, EVOD-26, EVOD-28.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** request; model identity; state ownership; cancellation; streaming; errors.

**Formal/mathematical development:** Specify prepare/step semantics and lifecycle invariants without assuming a cache type.

**Implementation / assessment:** Build a runtime skeleton only after model semantics; test request isolation and cancellation.

**Enables:** EVOD-31, EVOD-32, EVOD-35, EVOD-36, EVOD-39, EVOD-42, EVOD-44.

### EVOD-31 — DOGMA state construction and execution

**Required earlier chapters:** EVOD-18, EVOD-22, EVOD-26, EVOD-30.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** prompt ingestion; native step; chunking; output head; state tracing.

**Formal/mathematical development:** Derive engine transitions from the exact model; distinguish prompt ingestion from Transformer prefill.

**Implementation / assessment:** Compare token-by-token and valid chunked state construction against PyTorch.

**Enables:** EVOD-32, EVOD-33, EVOD-34.

### EVOD-32 — DOGMA state pools and memory ownership

**Required earlier chapters:** EVOD-20, EVOD-28, EVOD-30, EVOD-31.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** allocation; reset; reuse; clone; isolation; temporary buffers.

**Formal/mathematical development:** Define slot ownership and generation counters; separate persistent state from workspace and weights.

**Implementation / assessment:** Stress reuse and cancellation with cross-request leakage tests.

**Enables:** EVOD-33, EVOD-34, EVOD-45.

### EVOD-33 — DOGMA checkpoints, branching and prefix state

**Required earlier chapters:** EVOD-28, EVOD-31, EVOD-32.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** checkpoint; restore; state clone; versioning; shared prefixes.

**Formal/mathematical development:** Specify semantic equivalence and invalidation for cached state snapshots.

**Implementation / assessment:** Measure clone/restore cost and reject tokenizer/model/schema mismatches.

**Enables:** EVOD-34, EVOD-40, EVOD-49.

### EVOD-34 — DOGMA batching and state-native kernels

**Required earlier chapters:** EVOD-07, EVOD-26, EVOD-31, EVOD-32, EVOD-33.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** state-transition batching; scheduling; scans; locality; kernel profiling.

**Formal/mathematical development:** Group only compatible transitions; gate native kernels on profiling and parity.

**Implementation / assessment:** Profile the reference, optimize one bottleneck and test state/logit parity and latency tails.

**Enables:** EVOD-39, EVOD-46, EVOD-47.

### EVOD-35 — Hermon DNA prefill, decode and KV state

**Required earlier chapters:** EVOD-09, EVOD-23, EVOD-26, EVOD-30.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** prefill; decode; cache layout; positions; memory growth.

**Formal/mathematical development:** Derive KV bytes as 2*B*L*T*H_KV*D_h*b under declared layout; include other memory separately.

**Implementation / assessment:** Validate full/cached logits and K/V before throughput measurements.

**Enables:** EVOD-36, EVOD-37, EVOD-38.

### EVOD-36 — Paged KV, prefix sharing and allocation

**Required earlier chapters:** EVOD-28, EVOD-30, EVOD-35.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** pages; blocks; fragmentation; prefix cache; reference counting; eviction.

**Formal/mathematical development:** Derive allocation overhead and shared-prefix ownership without assuming exact retrieval.

**Implementation / assessment:** Test page reuse, invalidation, cancellation and cross-request isolation.

**Enables:** EVOD-37, EVOD-40, EVOD-45.

### EVOD-37 — Continuous batching and precision

**Required earlier chapters:** EVOD-27, EVOD-29, EVOD-35, EVOD-36.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** admission; prefill/decode scheduling; quantization; quality; tails.

**Formal/mathematical development:** Separate TTFT, ITL and throughput; derive scheduling and quantization tradeoffs.

**Implementation / assessment:** Compare declared workloads with quality and latency distributions, not only peak tokens/sec.

**Enables:** EVOD-38.

### EVOD-38 — Speculative decoding and attention kernels

**Required earlier chapters:** EVOD-26, EVOD-29, EVOD-35, EVOD-37.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** draft/verify; acceptance; numerical parity; memory traffic; fused kernels.

**Formal/mathematical development:** Explain exactness conditions for a chosen speculative scheme and profile kernel bottlenecks.

**Implementation / assessment:** Check distributional correctness where applicable and report quality, latency and memory.

**Enables:** EVOD-39, EVOD-46, EVOD-47.

### EVOD-39 — Evolutor runtime above both engines

**Required earlier chapters:** EVOD-14, EVOD-15, EVOD-30, EVOD-34, EVOD-38.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** planner; router; adapters; tools; retrieval; symbolic modules; trace.

**Formal/mathematical development:** Define composition contracts without collapsing state and KV representations.

**Implementation / assessment:** Execute a small heterogeneous plan with typed results, failure propagation and audit traces.

**Enables:** EVOD-40, EVOD-41, EVOD-42, EVOD-43, EVOD-44, EVOD-45, EVOD-46.

### EVOD-40 — Hybrid compressed and addressable memory

**Required earlier chapters:** EVOD-10, EVOD-16, EVOD-20, EVOD-29, EVOD-33, EVOD-36, EVOD-39.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** compression; addressability; forgetting; retrieval; memory routing.

**Formal/mathematical development:** Formulate a regulator hypothesis and compare established hybrid-memory and routing alternatives.

**Implementation / assessment:** Test copying and streaming tradeoffs at matched total memory; report losses as well as wins.

**Enables:** EVOD-48, EVOD-49, EVOD-50.

### EVOD-41 — Compiler, IR and execution planning

**Required earlier chapters:** EVOD-12, EVOD-14, EVOD-15, EVOD-16, EVOD-39.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** IR; typing; optimization; lowering; backend legality; cost model.

**Formal/mathematical development:** Derive an IR only from implemented mechanisms; prove one transformation preserves semantics.

**Implementation / assessment:** Lower a small expression plan to two backends with trace-equivalence tests.

**Enables:** EVOD-42, EVOD-43.

### EVOD-42 — Database engines as a systems comparison

**Required earlier chapters:** EVOD-10, EVOD-16, EVOD-30, EVOD-39, EVOD-41.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** parser; logical plan; optimizer; physical operators; buffer pool; transactions.

**Formal/mathematical development:** Compare database planning to expression planning and state exactly where transaction semantics differ.

**Implementation / assessment:** Cost two valid plans and expose a bad optimizer assumption using measured or synthetic labeled data.

**Enables:** Research synthesis.

### EVOD-43 — Structural adaptation and lifecycle governance

**Required earlier chapters:** EVOD-13, EVOD-17, EVOD-29, EVOD-39, EVOD-41.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** proposals; validation; evaluation; promotion; rollback; lineage.

**Formal/mathematical development:** Specify a proposal state machine and separate learning-time changes from serving-time state.

**Implementation / assessment:** Test invalid proposals, lineage checks and rollback without uncontrolled self-modification.

**Enables:** EVOD-44, EVOD-50, EVOD-51, EVOD-52.

### EVOD-44 — Packaging, deployment and observable services

**Required earlier chapters:** EVOD-28, EVOD-30, EVOD-39, EVOD-43.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** versioning; APIs; tracing; metrics; streaming; fault handling; rollback.

**Formal/mathematical development:** Define compatible artifacts and end-to-end failure semantics.

**Implementation / assessment:** Build reproducible deployment examples with version mismatch and restart tests.

**Enables:** EVOD-45, EVOD-46, EVOD-47, EVOD-48.

### EVOD-45 — Multi-tenancy, isolation and security

**Required earlier chapters:** EVOD-32, EVOD-36, EVOD-39, EVOD-44.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** ownership; quotas; untrusted inputs; tool authority; state leakage; threat model.

**Formal/mathematical development:** Specify trust boundaries, tenant isolation and resource exhaustion limits.

**Implementation / assessment:** Test adversarial cancellation/reuse and unauthorized cross-tenant state access.

**Enables:** EVOD-46, EVOD-49.

### EVOD-46 — Distributed serving and state placement

**Required earlier chapters:** EVOD-28, EVOD-34, EVOD-38, EVOD-39, EVOD-44, EVOD-45.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** replication; partitioning; tensor/pipeline parallelism; sharding; migration.

**Formal/mathematical development:** Derive communication and placement costs for recurrent state versus growing KV.

**Implementation / assessment:** Compare declared multi-device layouts and failure scenarios without fabricated speedups.

**Enables:** EVOD-47.

### EVOD-47 — Profiling, performance and hardware backends

**Required earlier chapters:** EVOD-29, EVOD-34, EVOD-38, EVOD-44, EVOD-46.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** TTFT; ITL; throughput; memory; power; utilization; roofline intuition.

**Formal/mathematical development:** Separate measured data from analytical bounds; state synchronization and hardware assumptions.

**Implementation / assessment:** Produce reproducible profiles and latency distributions; report power only when measured.

**Enables:** EVOD-48, EVOD-49, EVOD-52.

### EVOD-48 — Genomic sequence applications

**Required earlier chapters:** EVOD-24, EVOD-29, EVOD-40, EVOD-44, EVOD-47.

**Book I imports:** DNAD-25, DNAD-26, DNAD-30, DNAD-31. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** regulatory sequence analysis; motifs; long context; strand symmetry; uncertainty.

**Formal/mathematical development:** Define task-specific labels and leakage-resistant biological splits; no clinical inference from toy success.

**Implementation / assessment:** Evaluate a controlled genomic task with causal/symmetry checks and strong baselines.

**Enables:** EVOD-51, EVOD-52.

### EVOD-49 — Streaming, language, code and persistent agents

**Required earlier chapters:** EVOD-29, EVOD-33, EVOD-40, EVOD-45, EVOD-47.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** statistics; retrieval; copying; code; tools; persistent state; planning.

**Formal/mathematical development:** Define retention and exact-retrieval demands separately and account for external tools/memory.

**Implementation / assessment:** Compare family capabilities across algorithmic, language and agent tasks at declared budgets.

**Enables:** EVOD-50, EVOD-51, EVOD-52.

### EVOD-50 — Continual learning and population adaptation

**Required earlier chapters:** EVOD-13, EVOD-29, EVOD-40, EVOD-43, EVOD-49.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** transfer; forgetting; structural search; populations; open-ended learning.

**Formal/mathematical development:** Specify retention/adaptation objectives and distinguish in-context state from learned changes.

**Implementation / assessment:** Run controlled sequential-task and population comparisons with rollback and lineage.

**Enables:** EVOD-51, EVOD-52.

### EVOD-51 — AGI capability hypotheses and limits

**Required earlier chapters:** EVOD-29, EVOD-43, EVOD-48, EVOD-49, EVOD-50.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** reasoning; planning; world models; transfer; tools; self-modification; generalization.

**Formal/mathematical development:** Operationalize capability axes without treating architectural resemblance as AGI evidence.

**Implementation / assessment:** Design held-out capability tests and document what would falsify a broad claim.

**Enables:** EVOD-52.

### EVOD-52 — Failures, open problems and reproducible synthesis

**Required earlier chapters:** EVOD-29, EVOD-43, EVOD-47, EVOD-48, EVOD-49, EVOD-50, EVOD-51.

**Book I imports:** None. DNAD-01 is prototype-available; later imports remain future teaching dependencies, not completed outcomes.

**Mechanisms and concepts:** failed mechanisms; causality leaks; capacity confounds; negative results; historical lineage.

**Formal/mathematical development:** Separate established mechanisms, implemented results, conjectures and rejected proposals.

**Implementation / assessment:** Deliver a reproducible argument with baseline, ablation, uncertainty, artifact lineage and unsolved questions.

**Enables:** Research synthesis.
