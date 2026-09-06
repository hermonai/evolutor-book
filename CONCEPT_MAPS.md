# Evolutor: undergraduate-first architecture

Status: planning only. No new chapters, finished figures, animations, experiments or reviewed learning outcomes are claimed. Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json); edit that source and regenerate.

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

EVOU-03 → EVOU-04 → EVOU-05 → EVOU-06 → EVOU-07 → EVOU-08 → EVOU-09 → EVOU-10 → EVOU-11 → EVOU-12 → EVOU-13 → EVOU-16 → EVOU-19 → EVOU-22 → EVOU-27 → EVOU-29 → EVOU-34 → EVOU-36 → EVOU-37 → EVOU-38

- **EVOU-03**: machine learning; model; parameter; prediction; training; inference; loss.
- **EVOU-04**: dataset; training split; validation split; test split; overfitting; mean; variance; confidence interval; data leakage.
- **EVOU-05**: tensor; shape; batch dimension; broadcasting.
- **EVOU-06**: derivative; partial derivative; gradient; chain rule; gradient descent; learning rate.
- **EVOU-07**: neural network; layer; activation; multilayer perceptron; MLP; backpropagation; convolution; CNN.
- **EVOU-08**: PyTorch; automatic differentiation; optimizer; epoch; checkpoint; device; random seed.
- **EVOU-09**: token; vocabulary; embedding; next-token prediction; categorical distribution; softmax; cross-entropy.
- **EVOU-10**: recurrent neural network; RNN; hidden state; unrolling; backpropagation through time; leaky integrator.
- **EVOU-11**: gate; gated recurrent unit; GRU; state-space model; SSM; stability.
- **EVOU-12**: query; key; value; attention score; attention; causal mask; attention head.
- **EVOU-13**: multi-head attention; residual connection; normalization; feed-forward network; Transformer; positional encoding.
- **EVOU-16**: mixture of experts; MoE; expert; load balancing; sparse activation.
- **EVOU-19**: baseline; oracle; ablation; capacity matching; profiling plan; experimental hypothesis; Markov assumption.
- **EVOU-22**: pruning; architecture search; genetic programming; program synthesis; structural update.
- **EVOU-27**: credit assignment; trace provenance; causal intervention.
- **EVOU-29**: candidate training contract; multi-timescale update; frozen structure control.
- **EVOU-34**: parity; profiler; benchmark; warm-up; optimization.
- **EVOU-36**: negative result; confound; replication; stopping rule.
- **EVOU-37**: DNA model taxonomy; reverse-complement symmetry study; research-program name.
- **EVOU-38**: transfer; continual learning; catastrophic forgetting; population composition; distribution shift.

## genomic

EVOU-01 → EVOU-20 → EVOU-21 → EVOU-22 → EVOU-23 → EVOU-24 → EVOU-28 → EVOU-29 → EVOU-37 → EVOU-38 → EVOU-40

- **EVOU-01**: biological gene versus computational gene; analogy; research program.
- **EVOU-20**: biological regulation versus routing; sequence transfer versus control; timescale.
- **EVOU-21**: abstraction; mechanism; novelty claim; biological fidelity.
- **EVOU-22**: pruning; architecture search; genetic programming; program synthesis; structural update.
- **EVOU-23**: intermediate representation; IR; developmental program; compilation phase.
- **EVOU-24**: computational genome; computational regulator; expression plan; operational semantics.
- **EVOU-28**: UML state machine; proposal lifecycle; invariant; rollback.
- **EVOU-29**: candidate training contract; multi-timescale update; frozen structure control.
- **EVOU-37**: DNA model taxonomy; reverse-complement symmetry study; research-program name.
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

EVOU-01 → EVOU-02 → EVOU-08 → EVOU-14 → EVOU-15 → EVOU-17 → EVOU-18 → EVOU-19 → EVOU-23 → EVOU-25 → EVOU-26 → EVOU-27 → EVOU-28 → EVOU-30 → EVOU-31 → EVOU-32 → EVOU-33 → EVOU-34 → EVOU-35 → EVOU-40

- **EVOU-01**: biological gene versus computational gene; analogy; research program.
- **EVOU-02**: persistent state; module; interface contract; conditional execution.
- **EVOU-08**: PyTorch; automatic differentiation; optimizer; epoch; checkpoint; device; random seed.
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
- **EVOU-30**: runtime component; backend; inference contract; UML component diagram.
- **EVOU-31**: serialization; schema version; content hash; model identity; provenance.
- **EVOU-32**: state pool; memory ownership; paged KV; eviction; isolation.
- **EVOU-33**: continuous batching; admission control; backpressure; tail latency.
- **EVOU-34**: parity; profiler; benchmark; warm-up; optimization.
- **EVOU-35**: UML deployment diagram; observability; authentication; authorization; threat model; deployment rollback.
- **EVOU-40**: research artifact; replication package; claim retirement.

## AGI concept map

EVOU-04 evaluation on new examples → EVOU-19 fair comparisons → EVOU-36 failure and uncertainty → EVOU-38 transfer → EVOU-39 operational AGI claims → EVOU-40 reproducible argument. AGI means artificial general intelligence; the full reader-facing introduction is reserved for EVOU-39, not smuggled into the opening as an assumed capability.
