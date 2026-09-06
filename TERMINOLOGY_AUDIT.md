# Evolutor: undergraduate-first architecture

Status: Chapter 1 internally reviewed development draft; all later units remain planned. No learner study, independent expert certification or new research-model experiment is claimed. Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json). See [Chapter 1 storyboard](research/undergraduate-ch01-storyboard.md) for the six produced figures.

Target taxonomy: **DOGMA = non-Transformer DNA-native architecture + DOGMA Engine; Hermon DNA = Transformer-based DNA architecture + Hermon DNA Engine; Evolutor = research/theory/runtime above both.** These are research targets, not implementation evidence. See [taxonomy and lineage](research/architecture-taxonomy.md). Stable EVOU IDs differ from printed numbers after EVOU-11.

## First-encounter ledger

This is a planned terminology inventory, not a finished glossary. Definitions, illustrations and glossary entries must be authored and checked with the chapter. A parser cannot discover every unknown word. Human noun/acronym audit remains mandatory, including terms inside captions, code and exercises.

For each term: intuition → everyday example → labeled picture → precise definition → notation. The eventual digital glossary records short definition, first-use section, related terms and reciprocal chapter links; the print index records every substantive occurrence. No acronym appears before its expanded name and explanation.

| First-use chapter | Terms to teach | Definition / illustration / glossary state |
|---|---|---|
| EVOU-01 | biological gene versus computational gene; analogy; research program | Produced; see Chapter 1 first-sentence audit |
| EVOU-02 | persistent state; module; interface contract; conditional execution | Pending chapter production |
| EVOU-03 | machine learning; model; parameter; prediction; training; inference; loss | Pending chapter production |
| EVOU-04 | dataset; training split; validation split; test split; overfitting; mean; variance; confidence interval; data leakage | Pending chapter production |
| EVOU-05 | tensor; shape; batch dimension; broadcasting | Pending chapter production |
| EVOU-06 | derivative; partial derivative; gradient; chain rule; gradient descent; learning rate | Pending chapter production |
| EVOU-07 | neural network; layer; activation; multilayer perceptron; MLP; backpropagation; convolution; CNN | Pending chapter production |
| EVOU-08 | PyTorch; automatic differentiation; optimizer; epoch; checkpoint; device; random seed | Pending chapter production |
| EVOU-09 | token; vocabulary; embedding; next-token prediction; categorical distribution; softmax; cross-entropy | Pending chapter production |
| EVOU-10 | recurrent neural network; RNN; hidden state; unrolling; backpropagation through time; leaky integrator | Pending chapter production |
| EVOU-11 | gate; gated recurrent unit; GRU; state-space model; SSM; stability | Pending chapter production |
| EVOU-41 | finite-state machine; long short-term memory; LSTM; selective state update; associative scan; RWKV comparison | Pending chapter production |
| EVOU-12 | query; key; value; attention score; attention; causal mask; attention head | Pending chapter production |
| EVOU-13 | multi-head attention; residual connection; normalization; feed-forward network; Transformer; positional encoding | Pending chapter production |
| EVOU-14 | cache; key-value cache; KV cache; retrieval; external memory; index | Pending chapter production |
| EVOU-15 | dispatch; plugin; router; dynamic routing; pure function; lookup cost | Pending chapter production |
| EVOU-16 | mixture of experts; MoE; expert; load balancing; sparse activation | Pending chapter production |
| EVOU-17 | compiler; runtime; library; application programming interface; API; process; thread; memory | Pending chapter production |
| EVOU-18 | service; database; protocol; scheduler; query plan; latency; throughput; batch | Pending chapter production |
| EVOU-19 | baseline; oracle; ablation; capacity matching; profiling plan; experimental hypothesis; Markov assumption | Pending chapter production |
| EVOU-20 | biological regulation versus routing; sequence transfer versus control; timescale | Pending chapter production |
| EVOU-21 | abstraction; mechanism; novelty claim; biological fidelity | Pending chapter production |
| EVOU-22 | pruning; architecture search; genetic programming; program synthesis; structural update | Pending chapter production |
| EVOU-23 | intermediate representation; IR; developmental program; compilation phase | Pending chapter production |
| EVOU-24 | computational genome; computational regulator; expression plan; operational semantics | Pending chapter production |
| EVOU-25 | class; instance; method; composition; Unified Modeling Language; UML | Pending chapter production |
| EVOU-26 | UML sequence diagram; lifeline; message; executor | Pending chapter production |
| EVOU-27 | credit assignment; trace provenance; causal intervention | Pending chapter production |
| EVOU-28 | UML state machine; proposal lifecycle; invariant; rollback | Pending chapter production |
| EVOU-42 | DOGMA target architecture; DOGMA transition contract | Pending chapter production |
| EVOU-43 | DOGMA regulator candidate; DOGMA expression candidate | Pending chapter production |
| EVOU-44 | DOGMA memory locus candidate; DOGMA multi-timescale state | Pending chapter production |
| EVOU-45 | DOGMA dual-state candidate; causal reverse-complement boundary | Pending chapter production |
| EVOU-46 | DOGMA trace contract; trace utility test | Pending chapter production |
| EVOU-47 | Hermon DNA target architecture; Transformer DNA reference contract | Pending chapter production |
| EVOU-48 | strand-aware embedding candidate; motif-aware attention candidate | Pending chapter production |
| EVOU-29 | candidate training contract; multi-timescale update; frozen structure control | Pending chapter production |
| EVOU-49 | dual-family training contract | Pending chapter production |
| EVOU-50 | DOGMA training-inference parity | Pending chapter production |
| EVOU-30 | runtime component; backend; inference contract; UML component diagram | Pending chapter production |
| EVOU-31 | serialization; schema version; content hash; model identity; provenance | Pending chapter production |
| EVOU-32 | state pool; memory ownership; paged KV; eviction; isolation | Pending chapter production |
| EVOU-51 | DOGMA Engine; prompt ingestion | Pending chapter production |
| EVOU-52 | DOGMA state-slot lifecycle | Pending chapter production |
| EVOU-53 | prefix state cache; state checkpoint parity | Pending chapter production |
| EVOU-54 | state-transition batching | Pending chapter production |
| EVOU-55 | Hermon DNA Engine; prefill; attention decode | Pending chapter production |
| EVOU-56 | Hermon KV page table; Transformer prefix cache | Pending chapter production |
| EVOU-57 | Transformer batch lifecycle; quantization | Pending chapter production |
| EVOU-58 | heterogeneous model routing | Pending chapter production |
| EVOU-59 | compression-addressability hypothesis | Pending chapter production |
| EVOU-33 | continuous batching; admission control; backpressure; tail latency | Pending chapter production |
| EVOU-34 | parity; profiler; benchmark; warm-up; optimization | Pending chapter production |
| EVOU-60 | family-specific kernel gate; state-schema metadata | Pending chapter production |
| EVOU-35 | UML deployment diagram; observability; authentication; authorization; threat model; deployment rollback | Pending chapter production |
| EVOU-36 | negative result; confound; replication; stopping rule | Pending chapter production |
| EVOU-37 | DNA model taxonomy; reverse-complement symmetry study; research-program name | Pending chapter production |
| EVOU-61 | cross-family workload matrix | Pending chapter production |
| EVOU-38 | transfer; continual learning; catastrophic forgetting; population composition; distribution shift | Pending chapter production |
| EVOU-39 | artificial general intelligence; AGI; capability scope; generalization claim; evidence scorecard | Pending chapter production |
| EVOU-40 | research artifact; replication package; claim retirement | Pending chapter production |

Chapter 1 production overrides the planned inventory: see [its first-sentence audit](research/undergraduate-ch01-terminology.md), including locally defined preview terms and optional-code vocabulary. Later units deepen these ideas rather than assuming the full planned treatment has already occurred.
