# Deep scientific architecture: refinement proposal

Preserve the current 52 chapters and 12 parts.
No chapter files are moved. Chapters 1–2 retain acceptance; Chapter 3 is the next unfinished chapter.
This source-derived map adds scientific gates; it does not turn planned chapters into manuscripts.

## EVOD-01 · Why Genomic Computation?

- **Central question:** How do programs, neural models, genomes, stored and expressed computation, development, adaptation support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** Declared entry assumptions.
- **Book I imports:** DNAD-30, DNAD-32.
- **Mathematics:** Use provisional typed selection/execution maps after a concrete module example; novelty remains a question.
- **Implementation / experiment:** Compare conventional conditional execution with a proposed genomic organization and identify a falsifier.
- **Principal figure:** Program/model/genome comparison and two-family roadmap.
- **Keyframes:** persistent structure → context → regulation → expression → execution → trace → possible adaptation.
- **Research status:** internally-reviewed-draft in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-02 · Learning objectives, data, tasks, and evaluation

- **Central question:** How do prediction, likelihood, splits, uncertainty, controls, capacity support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-01.
- **Book I imports:** None additional.
- **Mathematics:** Derive a sequence likelihood and loss; separate training fit from held-out generalization.
- **Implementation / experiment:** Construct a leakage-resistant split and hand-check loss and calibration on a tiny dataset.
- **Principal figure:** Data lineage and objective.
- **Keyframes:** examples → prediction → loss → held-out check.
- **Research status:** internally-reviewed-draft in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-03 · Differentiation, optimization and tensor programs

- **Central question:** How do tensor shapes, gradients, autograd, optimization, numerical precision support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-02.
- **Book I imports:** None additional.
- **Mathematics:** Derive chain-rule gradients for a small network and annotate every dimension.
- **Implementation / experiment:** Check autograd with finite differences and demonstrate numerical failure cases.
- **Principal figure:** Tensor and gradient flow.
- **Keyframes:** forward values → loss → backward gradients → parameter update.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-04 · Reproducible PyTorch training

- **Central question:** How do datasets, batching, masking, optimizer, checkpoints, seeds support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-02, EVOD-03.
- **Book I imports:** None additional.
- **Mathematics:** Relate code to the objective and masking assumptions; distinguish resumption from reproducibility.
- **Implementation / experiment:** Implement a reference training loop with exact small cases and restart tests.
- **Principal figure:** Training lifecycle.
- **Keyframes:** batch → forward → backward → update → evaluate → checkpoint.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-05 · Tokenization and sequence representation

- **Central question:** How do DNA tokens, k-mers, embeddings, positions, strand orientation support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-02, EVOD-04.
- **Book I imports:** DNAD-05, DNAD-25.
- **Mathematics:** Derive vocabulary and sequence-length tradeoffs; state reverse-complement alignment conventions.
- **Implementation / experiment:** Test tokenization round trips and orientation handling without future leakage.
- **Principal figure:** Sequence to indexed tensor.
- **Keyframes:** sequence → tokens → embeddings → aligned targets.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-06 · Recurrent models and gated state

- **Central question:** How do RNN, LSTM, GRU, state transition, retention, gradients support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-03, EVOD-05.
- **Book I imports:** None additional.
- **Mathematics:** Derive one-step and unrolled computations and identify vanishing/exploding gradient mechanisms.
- **Implementation / experiment:** Compare recurrent baselines on copying and running statistics with matched controls.
- **Principal figure:** Unrolled and stepwise state.
- **Keyframes:** token and state → gate/update → next state → prediction.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-07 · State-space models, selective updates and scans

- **Central question:** How do linear recurrence, S4/S5, selective SSM, Mamba, RWKV, chunking support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-06.
- **Book I imports:** None additional.
- **Mathematics:** Derive an associative scan for a valid linear case and show where state-dependent nonlinearities break it.
- **Implementation / experiment:** Test sequential/chunked/scan parity and review strong primary-source baselines.
- **Principal figure:** Scan tree and recurrent trace.
- **Keyframes:** transition factors → composition → prefix states.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-08 · Attention and content-addressed computation

- **Central question:** How do Q/K/V, scores, masks, heads, softmax, retrieval support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-03, EVOD-05.
- **Book I imports:** None additional.
- **Mathematics:** Derive shaped attention from weighted lookup; distinguish addressability from exact recall.
- **Implementation / experiment:** Implement a small attention oracle and causal masking tests.
- **Principal figure:** Keys, query scores and weighted values.
- **Keyframes:** query → key comparison → normalization → value mixture.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-09 · Transformers and cached execution

- **Central question:** How do residuals, normalization, MLP, positions, blocks, KV, prefill, decode support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-04, EVOD-08.
- **Book I imports:** None additional.
- **Mathematics:** Derive a complete decoder block and full versus incremental equivalence under declared positions.
- **Implementation / experiment:** Verify logits and K/V across full and cached execution.
- **Principal figure:** Block diagram and cached token sequence.
- **Keyframes:** prompt → block computation → cached state → next step.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-10 · Conditional computation and memory alternatives

- **Central question:** How do dispatch, MoE, retrieval, external memory, dynamic graphs, hybrid models support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-06, EVOD-07, EVOD-09.
- **Book I imports:** None additional.
- **Mathematics:** Separate routing cost, active computation and memory access; compare mechanisms without renaming them.
- **Implementation / experiment:** Build an ordinary routed baseline and account for inactive parameter storage.
- **Principal figure:** Dispatch and memory comparison.
- **Keyframes:** context → route → selected operator → output.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-11 · Regulation and expression across levels

- **Central question:** How do biological regulation, stored modules, selection, execution, context support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-01, EVOD-10.
- **Book I imports:** DNAD-30.
- **Mathematics:** Give distinct biological and software interpretations and a typed selection map.
- **Implementation / experiment:** Compare a regulatory proposal to gates, dispatch and MoE with an explicit equivalence test.
- **Principal figure:** Biology/software comparison with typed arrows.
- **Keyframes:** context → regulator → selected structure → execution.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-12 · Development and generated computational structure

- **Central question:** How do genotype/phenotype, developmental encoding, compilation, program synthesis, NAS support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-10, EVOD-11.
- **Book I imports:** DNAD-30.
- **Mathematics:** Formulate a candidate development map and compare it to established program/network generation.
- **Implementation / experiment:** Generate a small executable structure and test whether development adds value over direct encoding.
- **Principal figure:** Development stages and compiler analogy.
- **Keyframes:** persistent description → developmental process → executable structure.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-13 · Learning, structural adaptation and evolution

- **Central question:** How do state change, parameter learning, structural learning, populations, selection support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-04, EVOD-11, EVOD-12.
- **Book I imports:** DNAD-30.
- **Mathematics:** Specify which object changes, at what timescale, with what objective and inheritance rule.
- **Implementation / experiment:** Contrast one state update, optimizer step, structural proposal and population generation.
- **Principal figure:** Multiple timescales.
- **Keyframes:** inference state → parameter update → structural revision → population selection.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-14 · Typed genomic computation systems

- **Central question:** How do alphabet, computational gene, genome, regulator, expression, state, trace support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-10, EVOD-11, EVOD-12, EVOD-13.
- **Book I imports:** DNAD-16, DNAD-18, DNAD-32.
- **Mathematics:** Derive typed interfaces from examples; re-evaluate the old tuple rather than canonizing it.
- **Implementation / experiment:** Build a minimal interpreter with types, invariants and a conventional baseline.
- **Principal figure:** Typed module and state relations.
- **Keyframes:** input types → selected plan → legal execution → typed result.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-15 · Operational semantics and expression traces

- **Central question:** How do configuration, transition, evaluation rule, effects, termination, trace support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-14.
- **Book I imports:** None additional.
- **Mathematics:** Define a small-step semantics and prove a bounded correspondence with the reference interpreter.
- **Implementation / experiment:** Compare exact transition traces; test invalid configurations and causal ordering.
- **Principal figure:** State-transition rules and execution trace.
- **Keyframes:** configuration → permitted transition → trace event → next configuration.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-16 · Expression complexity and resource semantics

- **Central question:** How do stored size, routing, active work, state, communication, trace, adaptation support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-07, EVOD-09, EVOD-15.
- **Book I imports:** DNAD-04, DNAD-24.
- **Mathematics:** Reassess expression-size complexity against a cost vector with units and worst-case quantifiers.
- **Implementation / experiment:** Construct a counterexample where fewer active modules cost more overall.
- **Principal figure:** Cost decomposition and counterexample.
- **Keyframes:** stored system → selected execution → full resource ledger.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-17 · Traces, credit and mechanistic evidence

- **Central question:** How do logging, causal interventions, credit assignment, structural proposals support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-13, EVOD-15, EVOD-16.
- **Book I imports:** None additional.
- **Mathematics:** Distinguish observed activation traces from causal explanations and useful adaptation signals.
- **Implementation / experiment:** Ablate trace-guided proposals against logging and random-selection controls.
- **Principal figure:** Trace interventions.
- **Keyframes:** recorded execution → intervention → changed outcome → evidence.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-18 · DOGMA primitives and state semantics

- **Central question:** How do State, Regulator, Expression, Strand, Complement, Gate, Memory locus, Module, Trace support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-07, EVOD-14, EVOD-15, EVOD-16.
- **Book I imports:** None additional.
- **Mathematics:** Define candidate primitives by type and transition; compare each with nearest recurrent or conditional baseline.
- **Implementation / experiment:** Implement only a minimal candidate after its semantics; reject redundant biological terminology.
- **Principal figure:** One-step candidate state machine.
- **Keyframes:** input and state → regulation → expressed transformation → new state → output.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-19 · DOGMA regulation and selective transformations

- **Central question:** How do regulation, expression, conditional state update, routing, ablation support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-10, EVOD-17, EVOD-18.
- **Book I imports:** None additional.
- **Mathematics:** Derive candidate R/E/U maps and compare gates, selection and dispatch algebraically.
- **Implementation / experiment:** Measure one-mechanism ablations with state/logit/gradient checks.
- **Principal figure:** Regulation and transformation panels.
- **Keyframes:** context → control → selected transformation → state update.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-20 · Structured memory, locality and timescales

- **Central question:** How do local/global state, modular memory, regulatory state, fast/slow state, capacity support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-07, EVOD-16, EVOD-18, EVOD-19.
- **Book I imports:** None additional.
- **Mathematics:** Specify ownership, updates, resets and capacity; no infinite-context or constant-total-memory claim.
- **Implementation / experiment:** Test retention, interference and reset behavior at matched memory and parameter budgets.
- **Principal figure:** State layout and update timescales.
- **Keyframes:** state partitions → selective updates → retained and lost information.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-21 · Strands, complements and dual-state hypotheses

- **Central question:** How do paired states, reverse complement, equivariance, causal streaming support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-05, EVOD-18, EVOD-20.
- **Book I imports:** DNAD-05, DNAD-30.
- **Mathematics:** Separate offline symmetry from causal inference; formalize a candidate interaction and augmentation control.
- **Implementation / experiment:** Detect reverse-complement future leakage; compare dual-state with augmentation and equivariant baselines.
- **Principal figure:** Paired state with causal boundaries.
- **Keyframes:** forward context → paired proposal → allowed interaction → output.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-22 · DOGMA reference model and falsifiable research program

- **Central question:** How do reference implementation, state trace, objective, baseline, ablation, negative evidence support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-04, EVOD-17, EVOD-19, EVOD-20, EVOD-21.
- **Book I imports:** None additional.
- **Mathematics:** Fix prediction timing after consumed tokens and precise state/logit contracts.
- **Implementation / experiment:** Train a small candidate only after exact tests; retain losing hypotheses and failure reports.
- **Principal figure:** Semantic reference and evidence loop.
- **Keyframes:** specified transition → reference → test → experiment → retain or reject.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-23 · Hermon DNA reference architecture

- **Central question:** How do DNA tokenizer, Transformer blocks, output head, causal positions support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-05, EVOD-09, EVOD-16.
- **Book I imports:** None additional.
- **Mathematics:** Specify a recognizably Transformer reference with all tensor shapes and attention semantics.
- **Implementation / experiment:** Train a small controlled reference and test full/incremental parity.
- **Principal figure:** DNA Transformer tensor pipeline.
- **Keyframes:** tokens → embeddings → attention blocks → output head.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-24 · DNA-aware Transformer mechanisms

- **Central question:** How do strand embeddings, motifs, k-mers, multi-scale positions, sparse/long context, retrieval support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-10, EVOD-21, EVOD-23.
- **Book I imports:** DNAD-25, DNAD-30.
- **Mathematics:** Define each modification as a testable change to the baseline, including symmetry and causality.
- **Implementation / experiment:** Run one-factor ablations and matched-budget DNA-task controls; no biomedical success implied.
- **Principal figure:** Baseline versus DNA-aware mechanism.
- **Keyframes:** baseline computation → proposed modification → controlled comparison.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-25 · Shared experiments without false equivalence

- **Central question:** How do data contracts, model interfaces, state types, losses, benchmarks support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-04, EVOD-22, EVOD-23, EVOD-24.
- **Book I imports:** None additional.
- **Mathematics:** Separate common evaluation interfaces from family-specific recurrent and KV states.
- **Implementation / experiment:** Build compatible prepare/step contracts with explicit logits versus sampled tokens.
- **Principal figure:** UML interface and two opaque state types.
- **Keyframes:** shared request → family adapter → typed state/result.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-26 · Training/inference parity and parallel recurrence

- **Central question:** How do sequential, chunked, scan, full sequence, incremental, gradients support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-07, EVOD-09, EVOD-22, EVOD-23, EVOD-25.
- **Book I imports:** None additional.
- **Mathematics:** State tolerances and valid equivalences; test outputs and internal state, not just loss.
- **Implementation / experiment:** Compare state/logit/gradient trajectories and deliberately broken masks or scans.
- **Principal figure:** Parity comparison across execution modes.
- **Keyframes:** reference trace → alternate execution → aligned comparison.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-27 · Optimization and memory-efficient training

- **Central question:** How do mixed precision, accumulation, checkpointing, optimizer state, stability support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-03, EVOD-04, EVOD-25, EVOD-26.
- **Book I imports:** None additional.
- **Mathematics:** Derive effective batch and memory accounting; distinguish recomputation from saved state.
- **Implementation / experiment:** Measure loss/gradient drift, memory and restart fidelity under one optimization at a time.
- **Principal figure:** Training memory and recomputation timeline.
- **Keyframes:** forward activations → checkpoint choice → backward recomputation.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-28 · Distributed training and model artifacts

- **Central question:** How do data/tensor/pipeline parallelism, communication, sharding, formats, provenance support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-25, EVOD-26, EVOD-27.
- **Book I imports:** None additional.
- **Mathematics:** Derive communication and memory consequences; identify model/state schema version boundaries.
- **Implementation / experiment:** Specify small distributed parity and fault-recovery tests; benchmark only measured configurations.
- **Principal figure:** UML deployment and communication schedule.
- **Keyframes:** sharded training → synchronized update → versioned checkpoint.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-29 · Benchmark design and comparative evidence

- **Central question:** How do oracles, budgets, multi-seed evaluation, capacity controls, causality, transplant tests support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-16, EVOD-17, EVOD-22, EVOD-24, EVOD-26, EVOD-27.
- **Book I imports:** None additional.
- **Mathematics:** Define estimands, uncertainty and a full resource vector before comparing families.
- **Implementation / experiment:** Build a benchmark matrix including copying, retrieval, statistics, motifs and state-machine tasks.
- **Principal figure:** Capability/resource matrix.
- **Keyframes:** hypothesis → matched tasks → repeated trials → bounded conclusion.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-30 · Runtime contracts and request lifecycles

- **Central question:** How do request, model identity, state ownership, cancellation, streaming, errors support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-15, EVOD-25, EVOD-26, EVOD-28.
- **Book I imports:** None additional.
- **Mathematics:** Specify prepare/step semantics and lifecycle invariants without assuming a cache type.
- **Implementation / experiment:** Build a runtime skeleton only after model semantics; test request isolation and cancellation.
- **Principal figure:** UML state and sequence diagrams.
- **Keyframes:** admit → prepare → step → finish or cancel → release.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-31 · DOGMA state construction and execution

- **Central question:** How do prompt ingestion, native step, chunking, output head, state tracing support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-18, EVOD-22, EVOD-26, EVOD-30.
- **Book I imports:** None additional.
- **Mathematics:** Derive engine transitions from the exact model; distinguish prompt ingestion from Transformer prefill.
- **Implementation / experiment:** Compare token-by-token and valid chunked state construction against PyTorch.
- **Principal figure:** DOGMA step sequence.
- **Keyframes:** prompt tokens → state construction → native transition → logits.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-32 · DOGMA state pools and memory ownership

- **Central question:** How do allocation, reset, reuse, clone, isolation, temporary buffers support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-20, EVOD-28, EVOD-30, EVOD-31.
- **Book I imports:** None additional.
- **Mathematics:** Define slot ownership and generation counters; separate persistent state from workspace and weights.
- **Implementation / experiment:** Stress reuse and cancellation with cross-request leakage tests.
- **Principal figure:** State-pool memory map.
- **Keyframes:** allocate → own → update → reset → reuse.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-33 · DOGMA checkpoints, branching and prefix state

- **Central question:** How do checkpoint, restore, state clone, versioning, shared prefixes support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-28, EVOD-31, EVOD-32.
- **Book I imports:** None additional.
- **Mathematics:** Specify semantic equivalence and invalidation for cached state snapshots.
- **Implementation / experiment:** Measure clone/restore cost and reject tokenizer/model/schema mismatches.
- **Principal figure:** Branching states and ownership.
- **Keyframes:** shared prefix → immutable snapshot → independent branches.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-34 · DOGMA batching and state-native kernels

- **Central question:** How do state-transition batching, scheduling, scans, locality, kernel profiling support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-07, EVOD-26, EVOD-31, EVOD-32, EVOD-33.
- **Book I imports:** None additional.
- **Mathematics:** Group only compatible transitions; gate native kernels on profiling and parity.
- **Implementation / experiment:** Profile the reference, optimize one bottleneck and test state/logit parity and latency tails.
- **Principal figure:** Scheduler timeline and kernel dataflow.
- **Keyframes:** queued states → compatible batch → kernel → independent next states.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-35 · Hermon DNA prefill, decode and KV state

- **Central question:** How do prefill, decode, cache layout, positions, memory growth support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-09, EVOD-23, EVOD-26, EVOD-30.
- **Book I imports:** None additional.
- **Mathematics:** Derive KV bytes as 2*B*L*T*H_KV*D_h*b under declared layout; include other memory separately.
- **Implementation / experiment:** Validate full/cached logits and K/V before throughput measurements.
- **Principal figure:** Tensor layout and request sequence.
- **Keyframes:** prompt → K/V construction → new query → updated cache.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-36 · Paged KV, prefix sharing and allocation

- **Central question:** How do pages, blocks, fragmentation, prefix cache, reference counting, eviction support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-28, EVOD-30, EVOD-35.
- **Book I imports:** None additional.
- **Mathematics:** Derive allocation overhead and shared-prefix ownership without assuming exact retrieval.
- **Implementation / experiment:** Test page reuse, invalidation, cancellation and cross-request isolation.
- **Principal figure:** Paged KV memory map.
- **Keyframes:** logical positions → physical pages → shared prefix → release.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-37 · Continuous batching and precision

- **Central question:** How do admission, prefill/decode scheduling, quantization, quality, tails support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-27, EVOD-29, EVOD-35, EVOD-36.
- **Book I imports:** None additional.
- **Mathematics:** Separate TTFT, ITL and throughput; derive scheduling and quantization tradeoffs.
- **Implementation / experiment:** Compare declared workloads with quality and latency distributions, not only peak tokens/sec.
- **Principal figure:** Request timeline and quantized layout.
- **Keyframes:** admit → schedule → decode batch → finish → reclaim.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-38 · Speculative decoding and attention kernels

- **Central question:** How do draft/verify, acceptance, numerical parity, memory traffic, fused kernels support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-26, EVOD-29, EVOD-35, EVOD-37.
- **Book I imports:** None additional.
- **Mathematics:** Explain exactness conditions for a chosen speculative scheme and profile kernel bottlenecks.
- **Implementation / experiment:** Check distributional correctness where applicable and report quality, latency and memory.
- **Principal figure:** Draft/verify timeline and kernel memory flow.
- **Keyframes:** draft tokens → target verification → accept/correct → continue.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-39 · Evolutor runtime above both engines

- **Central question:** How do planner, router, adapters, tools, retrieval, symbolic modules, trace support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-14, EVOD-15, EVOD-30, EVOD-34, EVOD-38.
- **Book I imports:** None additional.
- **Mathematics:** Define composition contracts without collapsing state and KV representations.
- **Implementation / experiment:** Execute a small heterogeneous plan with typed results, failure propagation and audit traces.
- **Principal figure:** UML components and sequence.
- **Keyframes:** request → planner → family/tool adapter → execution → trace.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-40 · Hybrid compressed and addressable memory

- **Central question:** How do compression, addressability, forgetting, retrieval, memory routing support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-10, EVOD-16, EVOD-20, EVOD-29, EVOD-33, EVOD-36, EVOD-39.
- **Book I imports:** None additional.
- **Mathematics:** Formulate a regulator hypothesis and compare established hybrid-memory and routing alternatives.
- **Implementation / experiment:** Test copying and streaming tradeoffs at matched total memory; report losses as well as wins.
- **Principal figure:** Dual memory layout and routing.
- **Keyframes:** context → state or addressable memory → regulator → output.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-41 · Compiler, IR and execution planning

- **Central question:** How do IR, typing, optimization, lowering, backend legality, cost model support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-12, EVOD-14, EVOD-15, EVOD-16, EVOD-39.
- **Book I imports:** None additional.
- **Mathematics:** Derive an IR only from implemented mechanisms; prove one transformation preserves semantics.
- **Implementation / experiment:** Lower a small expression plan to two backends with trace-equivalence tests.
- **Principal figure:** UML pipeline and typed IR.
- **Keyframes:** source → typed IR → optimized plan → backend execution.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-42 · Database engines as a systems comparison

- **Central question:** How do parser, logical plan, optimizer, physical operators, buffer pool, transactions support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-10, EVOD-16, EVOD-30, EVOD-39, EVOD-41.
- **Book I imports:** None additional.
- **Mathematics:** Compare database planning to expression planning and state exactly where transaction semantics differ.
- **Implementation / experiment:** Cost two valid plans and expose a bad optimizer assumption using measured or synthetic labeled data.
- **Principal figure:** Query-plan and runtime-plan comparison.
- **Keyframes:** logical request → candidate plans → cost choice → operator execution.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-43 · Structural adaptation and lifecycle governance

- **Central question:** How do proposals, validation, evaluation, promotion, rollback, lineage support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-13, EVOD-17, EVOD-29, EVOD-39, EVOD-41.
- **Book I imports:** None additional.
- **Mathematics:** Specify a proposal state machine and separate learning-time changes from serving-time state.
- **Implementation / experiment:** Test invalid proposals, lineage checks and rollback without uncontrolled self-modification.
- **Principal figure:** UML proposal lifecycle.
- **Keyframes:** propose → validate → compare → promote or reject → rollback.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-44 · Packaging, deployment and observable services

- **Central question:** How do versioning, APIs, tracing, metrics, streaming, fault handling, rollback support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-28, EVOD-30, EVOD-39, EVOD-43.
- **Book I imports:** None additional.
- **Mathematics:** Define compatible artifacts and end-to-end failure semantics.
- **Implementation / experiment:** Build reproducible deployment examples with version mismatch and restart tests.
- **Principal figure:** UML deployment and fault sequence.
- **Keyframes:** package → deploy → observe → recover or roll back.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-45 · Multi-tenancy, isolation and security

- **Central question:** How do ownership, quotas, untrusted inputs, tool authority, state leakage, threat model support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-32, EVOD-36, EVOD-39, EVOD-44.
- **Book I imports:** None additional.
- **Mathematics:** Specify trust boundaries, tenant isolation and resource exhaustion limits.
- **Implementation / experiment:** Test adversarial cancellation/reuse and unauthorized cross-tenant state access.
- **Principal figure:** Trust boundaries and ownership map.
- **Keyframes:** untrusted request → authorization → isolated execution → controlled result.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-46 · Distributed serving and state placement

- **Central question:** How do replication, partitioning, tensor/pipeline parallelism, sharding, migration support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-28, EVOD-34, EVOD-38, EVOD-39, EVOD-44, EVOD-45.
- **Book I imports:** None additional.
- **Mathematics:** Derive communication and placement costs for recurrent state versus growing KV.
- **Implementation / experiment:** Compare declared multi-device layouts and failure scenarios without fabricated speedups.
- **Principal figure:** UML deployment and communication timeline.
- **Keyframes:** route → place state → execute shards → aggregate → recover.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-47 · Profiling, performance and hardware backends

- **Central question:** How do TTFT, ITL, throughput, memory, power, utilization, roofline intuition support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-29, EVOD-34, EVOD-38, EVOD-44, EVOD-46.
- **Book I imports:** None additional.
- **Mathematics:** Separate measured data from analytical bounds; state synchronization and hardware assumptions.
- **Implementation / experiment:** Produce reproducible profiles and latency distributions; report power only when measured.
- **Principal figure:** Memory traffic, roofline and measured curves.
- **Keyframes:** workload → profile → bottleneck → optimized backend → parity check.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-48 · Genomic sequence applications

- **Central question:** How do regulatory sequence analysis, motifs, long context, strand symmetry, uncertainty support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-24, EVOD-29, EVOD-40, EVOD-44, EVOD-47.
- **Book I imports:** DNAD-25, DNAD-26, DNAD-30, DNAD-31.
- **Mathematics:** Define task-specific labels and leakage-resistant biological splits; no clinical inference from toy success.
- **Implementation / experiment:** Evaluate a controlled genomic task with causal/symmetry checks and strong baselines.
- **Principal figure:** Genomic task, split and evidence map.
- **Keyframes:** sequence dataset → controlled prediction → biological interpretation limits.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-49 · Streaming, language, code and persistent agents

- **Central question:** How do statistics, retrieval, copying, code, tools, persistent state, planning support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-29, EVOD-33, EVOD-40, EVOD-45, EVOD-47.
- **Book I imports:** None additional.
- **Mathematics:** Define retention and exact-retrieval demands separately and account for external tools/memory.
- **Implementation / experiment:** Compare family capabilities across algorithmic, language and agent tasks at declared budgets.
- **Principal figure:** Memory-demand and request timeline.
- **Keyframes:** stream → state or cache → task query → evaluated outcome.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-50 · Continual learning and population adaptation

- **Central question:** How do transfer, forgetting, structural search, populations, open-ended learning support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-13, EVOD-29, EVOD-40, EVOD-43, EVOD-49.
- **Book I imports:** None additional.
- **Mathematics:** Specify retention/adaptation objectives and distinguish in-context state from learned changes.
- **Implementation / experiment:** Run controlled sequential-task and population comparisons with rollback and lineage.
- **Principal figure:** Task sequence and population lineage.
- **Keyframes:** old tasks → new task → adaptation → retention check.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-51 · AGI capability hypotheses and limits

- **Central question:** How do reasoning, planning, world models, transfer, tools, self-modification, generalization support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-29, EVOD-43, EVOD-48, EVOD-49, EVOD-50.
- **Book I imports:** None additional.
- **Mathematics:** Operationalize capability axes without treating architectural resemblance as AGI evidence.
- **Implementation / experiment:** Design held-out capability tests and document what would falsify a broad claim.
- **Principal figure:** Capability/evidence matrix.
- **Keyframes:** mechanism → task evidence → transfer test → bounded claim.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.

## EVOD-52 · Failures, open problems and reproducible synthesis

- **Central question:** How do failed mechanisms, causality leaks, capacity confounds, negative results, historical lineage support this chapter's stated mechanism?
- **Scientific context:** Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.
- **Prerequisites:** EVOD-29, EVOD-43, EVOD-47, EVOD-48, EVOD-49, EVOD-50, EVOD-51.
- **Book I imports:** None additional.
- **Mathematics:** Separate established mechanisms, implemented results, conjectures and rejected proposals.
- **Implementation / experiment:** Deliver a reproducible argument with baseline, ablation, uncertainty, artifact lineage and unsolved questions.
- **Principal figure:** Claim-to-evidence and failure map.
- **Keyframes:** proposal → experiment → failure or support → revised theory.
- **Research status:** planned-not-drafted in canonical metadata; Chapter 3 has a separate working draft.
- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.
