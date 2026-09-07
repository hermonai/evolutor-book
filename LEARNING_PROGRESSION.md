# Evolutor: deep technical edition

Status: architecture and detailed outlines only; no new manuscript, final figures, animation frames, models, engines or experiments are delivered. Canonical source: [deep curriculum](pedagogy/deep-curriculum.json). Prior editions remain historical references, not the active teaching level.

DOGMA = non-Transformer DNA-native model + DOGMA Engine; Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; Evolutor = broader genomic computation theory, research and eventual runtime above both.

## Mathematics, implementation and evidence

Motivate the problem → explain the mechanism → define the abstraction → derive → interpret → work an example → implement → test → examine limits. This is a reasoning discipline, not a rigid chapter template. Basic programming is assumed; library-specific and domain-specific semantics are taught. Proofs, differential equations and formal systems are welcome.

### EVOD-01

Use provisional typed selection/execution maps after a concrete module example; novelty remains a question.

Compare conventional conditional execution with a proposed genomic organization and identify a falsifier.

### EVOD-02

Derive a sequence likelihood and loss; separate training fit from held-out generalization.

Construct a leakage-resistant split and hand-check loss and calibration on a tiny dataset.

### EVOD-03

Derive chain-rule gradients for a small network and annotate every dimension.

Check autograd with finite differences and demonstrate numerical failure cases.

### EVOD-04

Relate code to the objective and masking assumptions; distinguish resumption from reproducibility.

Implement a reference training loop with exact small cases and restart tests.

### EVOD-05

Derive vocabulary and sequence-length tradeoffs; state reverse-complement alignment conventions.

Test tokenization round trips and orientation handling without future leakage.

### EVOD-06

Derive one-step and unrolled computations and identify vanishing/exploding gradient mechanisms.

Compare recurrent baselines on copying and running statistics with matched controls.

### EVOD-07

Derive an associative scan for a valid linear case and show where state-dependent nonlinearities break it.

Test sequential/chunked/scan parity and review strong primary-source baselines.

### EVOD-08

Derive shaped attention from weighted lookup; distinguish addressability from exact recall.

Implement a small attention oracle and causal masking tests.

### EVOD-09

Derive a complete decoder block and full versus incremental equivalence under declared positions.

Verify logits and K/V across full and cached execution.

### EVOD-10

Separate routing cost, active computation and memory access; compare mechanisms without renaming them.

Build an ordinary routed baseline and account for inactive parameter storage.

### EVOD-11

Give distinct biological and software interpretations and a typed selection map.

Compare a regulatory proposal to gates, dispatch and MoE with an explicit equivalence test.

### EVOD-12

Formulate a candidate development map and compare it to established program/network generation.

Generate a small executable structure and test whether development adds value over direct encoding.

### EVOD-13

Specify which object changes, at what timescale, with what objective and inheritance rule.

Contrast one state update, optimizer step, structural proposal and population generation.

### EVOD-14

Derive typed interfaces from examples; re-evaluate the old tuple rather than canonizing it.

Build a minimal interpreter with types, invariants and a conventional baseline.

### EVOD-15

Define a small-step semantics and prove a bounded correspondence with the reference interpreter.

Compare exact transition traces; test invalid configurations and causal ordering.

### EVOD-16

Reassess expression-size complexity against a cost vector with units and worst-case quantifiers.

Construct a counterexample where fewer active modules cost more overall.

### EVOD-17

Distinguish observed activation traces from causal explanations and useful adaptation signals.

Ablate trace-guided proposals against logging and random-selection controls.

### EVOD-18

Define candidate primitives by type and transition; compare each with nearest recurrent or conditional baseline.

Implement only a minimal candidate after its semantics; reject redundant biological terminology.

### EVOD-19

Derive candidate R/E/U maps and compare gates, selection and dispatch algebraically.

Measure one-mechanism ablations with state/logit/gradient checks.

### EVOD-20

Specify ownership, updates, resets and capacity; no infinite-context or constant-total-memory claim.

Test retention, interference and reset behavior at matched memory and parameter budgets.

### EVOD-21

Separate offline symmetry from causal inference; formalize a candidate interaction and augmentation control.

Detect reverse-complement future leakage; compare dual-state with augmentation and equivariant baselines.

### EVOD-22

Fix prediction timing after consumed tokens and precise state/logit contracts.

Train a small candidate only after exact tests; retain losing hypotheses and failure reports.

### EVOD-23

Specify a recognizably Transformer reference with all tensor shapes and attention semantics.

Train a small controlled reference and test full/incremental parity.

### EVOD-24

Define each modification as a testable change to the baseline, including symmetry and causality.

Run one-factor ablations and matched-budget DNA-task controls; no biomedical success implied.

### EVOD-25

Separate common evaluation interfaces from family-specific recurrent and KV states.

Build compatible prepare/step contracts with explicit logits versus sampled tokens.

### EVOD-26

State tolerances and valid equivalences; test outputs and internal state, not just loss.

Compare state/logit/gradient trajectories and deliberately broken masks or scans.

### EVOD-27

Derive effective batch and memory accounting; distinguish recomputation from saved state.

Measure loss/gradient drift, memory and restart fidelity under one optimization at a time.

### EVOD-28

Derive communication and memory consequences; identify model/state schema version boundaries.

Specify small distributed parity and fault-recovery tests; benchmark only measured configurations.

### EVOD-29

Define estimands, uncertainty and a full resource vector before comparing families.

Build a benchmark matrix including copying, retrieval, statistics, motifs and state-machine tasks.

### EVOD-30

Specify prepare/step semantics and lifecycle invariants without assuming a cache type.

Build a runtime skeleton only after model semantics; test request isolation and cancellation.

### EVOD-31

Derive engine transitions from the exact model; distinguish prompt ingestion from Transformer prefill.

Compare token-by-token and valid chunked state construction against PyTorch.

### EVOD-32

Define slot ownership and generation counters; separate persistent state from workspace and weights.

Stress reuse and cancellation with cross-request leakage tests.

### EVOD-33

Specify semantic equivalence and invalidation for cached state snapshots.

Measure clone/restore cost and reject tokenizer/model/schema mismatches.

### EVOD-34

Group only compatible transitions; gate native kernels on profiling and parity.

Profile the reference, optimize one bottleneck and test state/logit parity and latency tails.

### EVOD-35

Derive KV bytes as 2*B*L*T*H_KV*D_h*b under declared layout; include other memory separately.

Validate full/cached logits and K/V before throughput measurements.

### EVOD-36

Derive allocation overhead and shared-prefix ownership without assuming exact retrieval.

Test page reuse, invalidation, cancellation and cross-request isolation.

### EVOD-37

Separate TTFT, ITL and throughput; derive scheduling and quantization tradeoffs.

Compare declared workloads with quality and latency distributions, not only peak tokens/sec.

### EVOD-38

Explain exactness conditions for a chosen speculative scheme and profile kernel bottlenecks.

Check distributional correctness where applicable and report quality, latency and memory.

### EVOD-39

Define composition contracts without collapsing state and KV representations.

Execute a small heterogeneous plan with typed results, failure propagation and audit traces.

### EVOD-40

Formulate a regulator hypothesis and compare established hybrid-memory and routing alternatives.

Test copying and streaming tradeoffs at matched total memory; report losses as well as wins.

### EVOD-41

Derive an IR only from implemented mechanisms; prove one transformation preserves semantics.

Lower a small expression plan to two backends with trace-equivalence tests.

### EVOD-42

Compare database planning to expression planning and state exactly where transaction semantics differ.

Cost two valid plans and expose a bad optimizer assumption using measured or synthetic labeled data.

### EVOD-43

Specify a proposal state machine and separate learning-time changes from serving-time state.

Test invalid proposals, lineage checks and rollback without uncontrolled self-modification.

### EVOD-44

Define compatible artifacts and end-to-end failure semantics.

Build reproducible deployment examples with version mismatch and restart tests.

### EVOD-45

Specify trust boundaries, tenant isolation and resource exhaustion limits.

Test adversarial cancellation/reuse and unauthorized cross-tenant state access.

### EVOD-46

Derive communication and placement costs for recurrent state versus growing KV.

Compare declared multi-device layouts and failure scenarios without fabricated speedups.

### EVOD-47

Separate measured data from analytical bounds; state synchronization and hardware assumptions.

Produce reproducible profiles and latency distributions; report power only when measured.

### EVOD-48

Define task-specific labels and leakage-resistant biological splits; no clinical inference from toy success.

Evaluate a controlled genomic task with causal/symmetry checks and strong baselines.

### EVOD-49

Define retention and exact-retrieval demands separately and account for external tools/memory.

Compare family capabilities across algorithmic, language and agent tasks at declared budgets.

### EVOD-50

Specify retention/adaptation objectives and distinguish in-context state from learned changes.

Run controlled sequential-task and population comparisons with rollback and lineage.

### EVOD-51

Operationalize capability axes without treating architectural resemblance as AGI evidence.

Design held-out capability tests and document what would falsify a broad claim.

### EVOD-52

Separate established mechanisms, implemented results, conjectures and rejected proposals.

Deliver a reproducible argument with baseline, ablation, uncertainty, artifact lineage and unsolved questions.
