# Mechanism-first visual production map

Biology uses structures and reaction states; mathematics uses graphs and equations;
software uses UML and explicit state. Every figure needs a semantic TXT companion.
A molecular drawing labels 5′/3′ orientation, covalent backbone versus pairing,
binding/cleavage sites and what changes. Color is redundant with labels and shapes.
These per-chapter entries are plans, not a claim of completed artwork.

## EVOD-01 · Why Genomic Computation?

Program/model/genome comparison and two-family roadmap.
State sequence: persistent structure → context → regulation → expression → execution → trace → possible adaptation.
Question/test anchor: Compare conventional conditional execution with a proposed genomic organization and identify a falsifier.

## EVOD-02 · Learning objectives, data, tasks, and evaluation

Data lineage and objective.
State sequence: examples → prediction → loss → held-out check.
Question/test anchor: Construct a leakage-resistant split and hand-check loss and calibration on a tiny dataset.

## EVOD-03 · Differentiation, optimization and tensor programs

Tensor and gradient flow.
State sequence: forward values → loss → backward gradients → parameter update.
Question/test anchor: Check autograd with finite differences and demonstrate numerical failure cases.

## EVOD-04 · Reproducible PyTorch training

Training lifecycle.
State sequence: batch → forward → backward → update → evaluate → checkpoint.
Question/test anchor: Implement a reference training loop with exact small cases and restart tests.

## EVOD-05 · Tokenization and sequence representation

Sequence to indexed tensor.
State sequence: sequence → tokens → embeddings → aligned targets.
Question/test anchor: Test tokenization round trips and orientation handling without future leakage.

## EVOD-06 · Recurrent models and gated state

Unrolled and stepwise state.
State sequence: token and state → gate/update → next state → prediction.
Question/test anchor: Compare recurrent baselines on copying and running statistics with matched controls.

## EVOD-07 · State-space models, selective updates and scans

Scan tree and recurrent trace.
State sequence: transition factors → composition → prefix states.
Question/test anchor: Test sequential/chunked/scan parity and review strong primary-source baselines.

## EVOD-08 · Attention and content-addressed computation

Keys, query scores and weighted values.
State sequence: query → key comparison → normalization → value mixture.
Question/test anchor: Implement a small attention oracle and causal masking tests.

## EVOD-09 · Transformers and cached execution

Block diagram and cached token sequence.
State sequence: prompt → block computation → cached state → next step.
Question/test anchor: Verify logits and K/V across full and cached execution.

## EVOD-10 · Conditional computation and memory alternatives

Dispatch and memory comparison.
State sequence: context → route → selected operator → output.
Question/test anchor: Build an ordinary routed baseline and account for inactive parameter storage.

## EVOD-11 · Regulation and expression across levels

Biology/software comparison with typed arrows.
State sequence: context → regulator → selected structure → execution.
Question/test anchor: Compare a regulatory proposal to gates, dispatch and MoE with an explicit equivalence test.

## EVOD-12 · Development and generated computational structure

Development stages and compiler analogy.
State sequence: persistent description → developmental process → executable structure.
Question/test anchor: Generate a small executable structure and test whether development adds value over direct encoding.

## EVOD-13 · Learning, structural adaptation and evolution

Multiple timescales.
State sequence: inference state → parameter update → structural revision → population selection.
Question/test anchor: Contrast one state update, optimizer step, structural proposal and population generation.

## EVOD-14 · Typed genomic computation systems

Typed module and state relations.
State sequence: input types → selected plan → legal execution → typed result.
Question/test anchor: Build a minimal interpreter with types, invariants and a conventional baseline.

## EVOD-15 · Operational semantics and expression traces

State-transition rules and execution trace.
State sequence: configuration → permitted transition → trace event → next configuration.
Question/test anchor: Compare exact transition traces; test invalid configurations and causal ordering.

## EVOD-16 · Expression complexity and resource semantics

Cost decomposition and counterexample.
State sequence: stored system → selected execution → full resource ledger.
Question/test anchor: Construct a counterexample where fewer active modules cost more overall.

## EVOD-17 · Traces, credit and mechanistic evidence

Trace interventions.
State sequence: recorded execution → intervention → changed outcome → evidence.
Question/test anchor: Ablate trace-guided proposals against logging and random-selection controls.

## EVOD-18 · DOGMA primitives and state semantics

One-step candidate state machine.
State sequence: input and state → regulation → expressed transformation → new state → output.
Question/test anchor: Implement only a minimal candidate after its semantics; reject redundant biological terminology.

## EVOD-19 · DOGMA regulation and selective transformations

Regulation and transformation panels.
State sequence: context → control → selected transformation → state update.
Question/test anchor: Measure one-mechanism ablations with state/logit/gradient checks.

## EVOD-20 · Structured memory, locality and timescales

State layout and update timescales.
State sequence: state partitions → selective updates → retained and lost information.
Question/test anchor: Test retention, interference and reset behavior at matched memory and parameter budgets.

## EVOD-21 · Strands, complements and dual-state hypotheses

Paired state with causal boundaries.
State sequence: forward context → paired proposal → allowed interaction → output.
Question/test anchor: Detect reverse-complement future leakage; compare dual-state with augmentation and equivariant baselines.

## EVOD-22 · DOGMA reference model and falsifiable research program

Semantic reference and evidence loop.
State sequence: specified transition → reference → test → experiment → retain or reject.
Question/test anchor: Train a small candidate only after exact tests; retain losing hypotheses and failure reports.

## EVOD-23 · Hermon DNA reference architecture

DNA Transformer tensor pipeline.
State sequence: tokens → embeddings → attention blocks → output head.
Question/test anchor: Train a small controlled reference and test full/incremental parity.

## EVOD-24 · DNA-aware Transformer mechanisms

Baseline versus DNA-aware mechanism.
State sequence: baseline computation → proposed modification → controlled comparison.
Question/test anchor: Run one-factor ablations and matched-budget DNA-task controls; no biomedical success implied.

## EVOD-25 · Shared experiments without false equivalence

UML interface and two opaque state types.
State sequence: shared request → family adapter → typed state/result.
Question/test anchor: Build compatible prepare/step contracts with explicit logits versus sampled tokens.

## EVOD-26 · Training/inference parity and parallel recurrence

Parity comparison across execution modes.
State sequence: reference trace → alternate execution → aligned comparison.
Question/test anchor: Compare state/logit/gradient trajectories and deliberately broken masks or scans.

## EVOD-27 · Optimization and memory-efficient training

Training memory and recomputation timeline.
State sequence: forward activations → checkpoint choice → backward recomputation.
Question/test anchor: Measure loss/gradient drift, memory and restart fidelity under one optimization at a time.

## EVOD-28 · Distributed training and model artifacts

UML deployment and communication schedule.
State sequence: sharded training → synchronized update → versioned checkpoint.
Question/test anchor: Specify small distributed parity and fault-recovery tests; benchmark only measured configurations.

## EVOD-29 · Benchmark design and comparative evidence

Capability/resource matrix.
State sequence: hypothesis → matched tasks → repeated trials → bounded conclusion.
Question/test anchor: Build a benchmark matrix including copying, retrieval, statistics, motifs and state-machine tasks.

## EVOD-30 · Runtime contracts and request lifecycles

UML state and sequence diagrams.
State sequence: admit → prepare → step → finish or cancel → release.
Question/test anchor: Build a runtime skeleton only after model semantics; test request isolation and cancellation.

## EVOD-31 · DOGMA state construction and execution

DOGMA step sequence.
State sequence: prompt tokens → state construction → native transition → logits.
Question/test anchor: Compare token-by-token and valid chunked state construction against PyTorch.

## EVOD-32 · DOGMA state pools and memory ownership

State-pool memory map.
State sequence: allocate → own → update → reset → reuse.
Question/test anchor: Stress reuse and cancellation with cross-request leakage tests.

## EVOD-33 · DOGMA checkpoints, branching and prefix state

Branching states and ownership.
State sequence: shared prefix → immutable snapshot → independent branches.
Question/test anchor: Measure clone/restore cost and reject tokenizer/model/schema mismatches.

## EVOD-34 · DOGMA batching and state-native kernels

Scheduler timeline and kernel dataflow.
State sequence: queued states → compatible batch → kernel → independent next states.
Question/test anchor: Profile the reference, optimize one bottleneck and test state/logit parity and latency tails.

## EVOD-35 · Hermon DNA prefill, decode and KV state

Tensor layout and request sequence.
State sequence: prompt → K/V construction → new query → updated cache.
Question/test anchor: Validate full/cached logits and K/V before throughput measurements.

## EVOD-36 · Paged KV, prefix sharing and allocation

Paged KV memory map.
State sequence: logical positions → physical pages → shared prefix → release.
Question/test anchor: Test page reuse, invalidation, cancellation and cross-request isolation.

## EVOD-37 · Continuous batching and precision

Request timeline and quantized layout.
State sequence: admit → schedule → decode batch → finish → reclaim.
Question/test anchor: Compare declared workloads with quality and latency distributions, not only peak tokens/sec.

## EVOD-38 · Speculative decoding and attention kernels

Draft/verify timeline and kernel memory flow.
State sequence: draft tokens → target verification → accept/correct → continue.
Question/test anchor: Check distributional correctness where applicable and report quality, latency and memory.

## EVOD-39 · Evolutor runtime above both engines

UML components and sequence.
State sequence: request → planner → family/tool adapter → execution → trace.
Question/test anchor: Execute a small heterogeneous plan with typed results, failure propagation and audit traces.

## EVOD-40 · Hybrid compressed and addressable memory

Dual memory layout and routing.
State sequence: context → state or addressable memory → regulator → output.
Question/test anchor: Test copying and streaming tradeoffs at matched total memory; report losses as well as wins.

## EVOD-41 · Compiler, IR and execution planning

UML pipeline and typed IR.
State sequence: source → typed IR → optimized plan → backend execution.
Question/test anchor: Lower a small expression plan to two backends with trace-equivalence tests.

## EVOD-42 · Database engines as a systems comparison

Query-plan and runtime-plan comparison.
State sequence: logical request → candidate plans → cost choice → operator execution.
Question/test anchor: Cost two valid plans and expose a bad optimizer assumption using measured or synthetic labeled data.

## EVOD-43 · Structural adaptation and lifecycle governance

UML proposal lifecycle.
State sequence: propose → validate → compare → promote or reject → rollback.
Question/test anchor: Test invalid proposals, lineage checks and rollback without uncontrolled self-modification.

## EVOD-44 · Packaging, deployment and observable services

UML deployment and fault sequence.
State sequence: package → deploy → observe → recover or roll back.
Question/test anchor: Build reproducible deployment examples with version mismatch and restart tests.

## EVOD-45 · Multi-tenancy, isolation and security

Trust boundaries and ownership map.
State sequence: untrusted request → authorization → isolated execution → controlled result.
Question/test anchor: Test adversarial cancellation/reuse and unauthorized cross-tenant state access.

## EVOD-46 · Distributed serving and state placement

UML deployment and communication timeline.
State sequence: route → place state → execute shards → aggregate → recover.
Question/test anchor: Compare declared multi-device layouts and failure scenarios without fabricated speedups.

## EVOD-47 · Profiling, performance and hardware backends

Memory traffic, roofline and measured curves.
State sequence: workload → profile → bottleneck → optimized backend → parity check.
Question/test anchor: Produce reproducible profiles and latency distributions; report power only when measured.

## EVOD-48 · Genomic sequence applications

Genomic task, split and evidence map.
State sequence: sequence dataset → controlled prediction → biological interpretation limits.
Question/test anchor: Evaluate a controlled genomic task with causal/symmetry checks and strong baselines.

## EVOD-49 · Streaming, language, code and persistent agents

Memory-demand and request timeline.
State sequence: stream → state or cache → task query → evaluated outcome.
Question/test anchor: Compare family capabilities across algorithmic, language and agent tasks at declared budgets.

## EVOD-50 · Continual learning and population adaptation

Task sequence and population lineage.
State sequence: old tasks → new task → adaptation → retention check.
Question/test anchor: Run controlled sequential-task and population comparisons with rollback and lineage.

## EVOD-51 · AGI capability hypotheses and limits

Capability/evidence matrix.
State sequence: mechanism → task evidence → transfer test → bounded claim.
Question/test anchor: Design held-out capability tests and document what would falsify a broad claim.

## EVOD-52 · Failures, open problems and reproducible synthesis

Claim-to-evidence and failure map.
State sequence: proposal → experiment → failure or support → revised theory.
Question/test anchor: Deliver a reproducible argument with baseline, ablation, uncertainty, artifact lineage and unsolved questions.
