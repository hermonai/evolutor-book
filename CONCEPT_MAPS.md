# Evolutor: undergraduate-first architecture

Status: Chapter 1 internally reviewed development draft; all later units remain planned. No learner study, independent expert certification or new research-model experiment is claimed. Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json). See [Chapter 1 storyboard](research/undergraduate-ch01-storyboard.md) for the six produced figures.

Target taxonomy: **DOGMA = non-Transformer DNA-native architecture + DOGMA Engine; Hermon DNA = Transformer-based DNA architecture + Hermon DNA Engine; Evolutor = research/theory/runtime above both.** These are research targets, not implementation evidence. See [taxonomy and lineage](research/architecture-taxonomy.md). Stable EVOU IDs differ from printed numbers after EVOU-11.

## Just-in-time disciplinary maps

These maps index where each discipline enters the course; arrows follow the reading order. Exact required edges are in PREREQUISITE_GRAPH.md. They are not detached prerequisite courses.

## AI

EVOU-03 → EVOU-07 → EVOU-09 → EVOU-13 → EVOU-14 → EVOU-16 → EVOU-21 → EVOU-36 → EVOU-38 → EVOU-39 → EVOU-40

- **EVOU-03**: machine learning; model; parameter; prediction; training; inference; loss.
- **EVOU-07**: neural network; layer; activation; multilayer perceptron; MLP; backpropagation; convolution; CNN.
- **EVOU-09**: token; vocabulary; embedding; next-token prediction; categorical distribution; softmax; cross-entropy.
- **EVOU-13**: multi-head attention; residual connection; normalization; feed-forward network; Transformer; positional encoding.
- **EVOU-14**: cache; key-value cache; KV cache; retrieval; external memory; index.
- **EVOU-16**: mixture of experts; MoE; expert; load balancing; sparse activation.
- **EVOU-21**: abstraction; mechanism; novelty claim; biological fidelity.
- **EVOU-36**: negative result; confound; replication; stopping rule.
- **EVOU-38**: transfer; continual learning; catastrophic forgetting; population composition; distribution shift.
- **EVOU-39**: artificial general intelligence; AGI; capability scope; generalization claim; evidence scorecard.
- **EVOU-40**: research artifact; replication package; claim retirement.

## ML

EVOU-03 → EVOU-04 → EVOU-05 → EVOU-06 → EVOU-07 → EVOU-08 → EVOU-09 → EVOU-10 → EVOU-11 → EVOU-41 → EVOU-12 → EVOU-13 → EVOU-16 → EVOU-19 → EVOU-22 → EVOU-27 → EVOU-42 → EVOU-43 → EVOU-44 → EVOU-45 → EVOU-46 → EVOU-47 → EVOU-48 → EVOU-29 → EVOU-49 → EVOU-50 → EVOU-51 → EVOU-52 → EVOU-53 → EVOU-54 → EVOU-55 → EVOU-56 → EVOU-57 → EVOU-58 → EVOU-59 → EVOU-34 → EVOU-60 → EVOU-36 → EVOU-37 → EVOU-61 → EVOU-38

- **EVOU-03**: machine learning; model; parameter; prediction; training; inference; loss.
- **EVOU-04**: dataset; training split; validation split; test split; overfitting; mean; variance; confidence interval; data leakage.
- **EVOU-05**: tensor; shape; batch dimension; broadcasting.
- **EVOU-06**: derivative; partial derivative; gradient; chain rule; gradient descent; learning rate.
- **EVOU-07**: neural network; layer; activation; multilayer perceptron; MLP; backpropagation; convolution; CNN.
- **EVOU-08**: PyTorch; automatic differentiation; optimizer; epoch; checkpoint; device; random seed.
- **EVOU-09**: token; vocabulary; embedding; next-token prediction; categorical distribution; softmax; cross-entropy.
- **EVOU-10**: recurrent neural network; RNN; hidden state; unrolling; backpropagation through time; leaky integrator.
- **EVOU-11**: gate; gated recurrent unit; GRU; state-space model; SSM; stability.
- **EVOU-41**: finite-state machine; long short-term memory; LSTM; selective state update; associative scan; RWKV comparison.
- **EVOU-12**: query; key; value; attention score; attention; causal mask; attention head.
- **EVOU-13**: multi-head attention; residual connection; normalization; feed-forward network; Transformer; positional encoding.
- **EVOU-16**: mixture of experts; MoE; expert; load balancing; sparse activation.
- **EVOU-19**: baseline; oracle; ablation; capacity matching; profiling plan; experimental hypothesis; Markov assumption.
- **EVOU-22**: pruning; architecture search; genetic programming; program synthesis; structural update.
- **EVOU-27**: credit assignment; trace provenance; causal intervention.
- **EVOU-42**: DOGMA target architecture; DOGMA transition contract.
- **EVOU-43**: DOGMA regulator candidate; DOGMA expression candidate.
- **EVOU-44**: DOGMA memory locus candidate; DOGMA multi-timescale state.
- **EVOU-45**: DOGMA dual-state candidate; causal reverse-complement boundary.
- **EVOU-46**: DOGMA trace contract; trace utility test.
- **EVOU-47**: Hermon DNA target architecture; Transformer DNA reference contract.
- **EVOU-48**: strand-aware embedding candidate; motif-aware attention candidate.
- **EVOU-29**: candidate training contract; multi-timescale update; frozen structure control.
- **EVOU-49**: dual-family training contract.
- **EVOU-50**: DOGMA training-inference parity.
- **EVOU-51**: DOGMA Engine; prompt ingestion.
- **EVOU-52**: DOGMA state-slot lifecycle.
- **EVOU-53**: prefix state cache; state checkpoint parity.
- **EVOU-54**: state-transition batching.
- **EVOU-55**: Hermon DNA Engine; prefill; attention decode.
- **EVOU-56**: Hermon KV page table; Transformer prefix cache.
- **EVOU-57**: Transformer batch lifecycle; quantization.
- **EVOU-58**: heterogeneous model routing.
- **EVOU-59**: compression-addressability hypothesis.
- **EVOU-34**: parity; profiler; benchmark; warm-up; optimization.
- **EVOU-60**: family-specific kernel gate; state-schema metadata.
- **EVOU-36**: negative result; confound; replication; stopping rule.
- **EVOU-37**: DNA model taxonomy; reverse-complement symmetry study; research-program name.
- **EVOU-61**: cross-family workload matrix.
- **EVOU-38**: transfer; continual learning; catastrophic forgetting; population composition; distribution shift.

## genomic

EVOU-01 → EVOU-41 → EVOU-20 → EVOU-21 → EVOU-22 → EVOU-23 → EVOU-24 → EVOU-28 → EVOU-42 → EVOU-43 → EVOU-44 → EVOU-45 → EVOU-46 → EVOU-47 → EVOU-48 → EVOU-29 → EVOU-49 → EVOU-50 → EVOU-51 → EVOU-52 → EVOU-53 → EVOU-54 → EVOU-55 → EVOU-56 → EVOU-57 → EVOU-58 → EVOU-59 → EVOU-60 → EVOU-37 → EVOU-61 → EVOU-38 → EVOU-40

- **EVOU-01**: biological gene versus computational gene; analogy; research program.
- **EVOU-41**: finite-state machine; long short-term memory; LSTM; selective state update; associative scan; RWKV comparison.
- **EVOU-20**: biological regulation versus routing; sequence transfer versus control; timescale.
- **EVOU-21**: abstraction; mechanism; novelty claim; biological fidelity.
- **EVOU-22**: pruning; architecture search; genetic programming; program synthesis; structural update.
- **EVOU-23**: intermediate representation; IR; developmental program; compilation phase.
- **EVOU-24**: computational genome; computational regulator; expression plan; operational semantics.
- **EVOU-28**: UML state machine; proposal lifecycle; invariant; rollback.
- **EVOU-42**: DOGMA target architecture; DOGMA transition contract.
- **EVOU-43**: DOGMA regulator candidate; DOGMA expression candidate.
- **EVOU-44**: DOGMA memory locus candidate; DOGMA multi-timescale state.
- **EVOU-45**: DOGMA dual-state candidate; causal reverse-complement boundary.
- **EVOU-46**: DOGMA trace contract; trace utility test.
- **EVOU-47**: Hermon DNA target architecture; Transformer DNA reference contract.
- **EVOU-48**: strand-aware embedding candidate; motif-aware attention candidate.
- **EVOU-29**: candidate training contract; multi-timescale update; frozen structure control.
- **EVOU-49**: dual-family training contract.
- **EVOU-50**: DOGMA training-inference parity.
- **EVOU-51**: DOGMA Engine; prompt ingestion.
- **EVOU-52**: DOGMA state-slot lifecycle.
- **EVOU-53**: prefix state cache; state checkpoint parity.
- **EVOU-54**: state-transition batching.
- **EVOU-55**: Hermon DNA Engine; prefill; attention decode.
- **EVOU-56**: Hermon KV page table; Transformer prefix cache.
- **EVOU-57**: Transformer batch lifecycle; quantization.
- **EVOU-58**: heterogeneous model routing.
- **EVOU-59**: compression-addressability hypothesis.
- **EVOU-60**: family-specific kernel gate; state-schema metadata.
- **EVOU-37**: DNA model taxonomy; reverse-complement symmetry study; research-program name.
- **EVOU-61**: cross-family workload matrix.
- **EVOU-38**: transfer; continual learning; catastrophic forgetting; population composition; distribution shift.
- **EVOU-40**: research artifact; replication package; claim retirement.

## mathematics

EVOU-04 → EVOU-05 → EVOU-06 → EVOU-10 → EVOU-11 → EVOU-12 → EVOU-24 → EVOU-39

- **EVOU-04**: dataset; training split; validation split; test split; overfitting; mean; variance; confidence interval; data leakage.
- **EVOU-05**: tensor; shape; batch dimension; broadcasting.
- **EVOU-06**: derivative; partial derivative; gradient; chain rule; gradient descent; learning rate.
- **EVOU-10**: recurrent neural network; RNN; hidden state; unrolling; backpropagation through time; leaky integrator.
- **EVOU-11**: gate; gated recurrent unit; GRU; state-space model; SSM; stability.
- **EVOU-12**: query; key; value; attention score; attention; causal mask; attention head.
- **EVOU-24**: computational genome; computational regulator; expression plan; operational semantics.
- **EVOU-39**: artificial general intelligence; AGI; capability scope; generalization claim; evidence scorecard.

## systems

EVOU-01 → EVOU-02 → EVOU-08 → EVOU-41 → EVOU-14 → EVOU-15 → EVOU-17 → EVOU-18 → EVOU-19 → EVOU-23 → EVOU-25 → EVOU-26 → EVOU-27 → EVOU-28 → EVOU-42 → EVOU-43 → EVOU-44 → EVOU-45 → EVOU-46 → EVOU-47 → EVOU-48 → EVOU-49 → EVOU-50 → EVOU-30 → EVOU-31 → EVOU-32 → EVOU-51 → EVOU-52 → EVOU-53 → EVOU-54 → EVOU-55 → EVOU-56 → EVOU-57 → EVOU-58 → EVOU-59 → EVOU-33 → EVOU-34 → EVOU-60 → EVOU-35 → EVOU-61 → EVOU-40

- **EVOU-01**: biological gene versus computational gene; analogy; research program.
- **EVOU-02**: persistent state; module; interface contract; conditional execution.
- **EVOU-08**: PyTorch; automatic differentiation; optimizer; epoch; checkpoint; device; random seed.
- **EVOU-41**: finite-state machine; long short-term memory; LSTM; selective state update; associative scan; RWKV comparison.
- **EVOU-14**: cache; key-value cache; KV cache; retrieval; external memory; index.
- **EVOU-15**: dispatch; plugin; router; dynamic routing; pure function; lookup cost.
- **EVOU-17**: compiler; runtime; library; application programming interface; API; process; thread; memory.
- **EVOU-18**: service; database; protocol; scheduler; query plan; latency; throughput; batch.
- **EVOU-19**: baseline; oracle; ablation; capacity matching; profiling plan; experimental hypothesis; Markov assumption.
- **EVOU-23**: intermediate representation; IR; developmental program; compilation phase.
- **EVOU-25**: class; instance; method; composition; Unified Modeling Language; UML.
- **EVOU-26**: UML sequence diagram; lifeline; message; executor.
- **EVOU-27**: credit assignment; trace provenance; causal intervention.
- **EVOU-28**: UML state machine; proposal lifecycle; invariant; rollback.
- **EVOU-42**: DOGMA target architecture; DOGMA transition contract.
- **EVOU-43**: DOGMA regulator candidate; DOGMA expression candidate.
- **EVOU-44**: DOGMA memory locus candidate; DOGMA multi-timescale state.
- **EVOU-45**: DOGMA dual-state candidate; causal reverse-complement boundary.
- **EVOU-46**: DOGMA trace contract; trace utility test.
- **EVOU-47**: Hermon DNA target architecture; Transformer DNA reference contract.
- **EVOU-48**: strand-aware embedding candidate; motif-aware attention candidate.
- **EVOU-49**: dual-family training contract.
- **EVOU-50**: DOGMA training-inference parity.
- **EVOU-30**: runtime component; backend; inference contract; UML component diagram.
- **EVOU-31**: serialization; schema version; content hash; model identity; provenance.
- **EVOU-32**: state pool; memory ownership; paged KV; eviction; isolation.
- **EVOU-51**: DOGMA Engine; prompt ingestion.
- **EVOU-52**: DOGMA state-slot lifecycle.
- **EVOU-53**: prefix state cache; state checkpoint parity.
- **EVOU-54**: state-transition batching.
- **EVOU-55**: Hermon DNA Engine; prefill; attention decode.
- **EVOU-56**: Hermon KV page table; Transformer prefix cache.
- **EVOU-57**: Transformer batch lifecycle; quantization.
- **EVOU-58**: heterogeneous model routing.
- **EVOU-59**: compression-addressability hypothesis.
- **EVOU-33**: continuous batching; admission control; backpressure; tail latency.
- **EVOU-34**: parity; profiler; benchmark; warm-up; optimization.
- **EVOU-60**: family-specific kernel gate; state-schema metadata.
- **EVOU-35**: UML deployment diagram; observability; authentication; authorization; threat model; deployment rollback.
- **EVOU-61**: cross-family workload matrix.
- **EVOU-40**: research artifact; replication package; claim retirement.

## AGI concept map

EVOU-04 evaluation on new examples → EVOU-19 fair comparisons → EVOU-36 failure and uncertainty → EVOU-38 transfer → EVOU-39 operational AGI claims → EVOU-40 reproducible argument. AGI means artificial general intelligence; the full reader-facing introduction is reserved for EVOU-39, not smuggled into the opening as an assumed capability.
