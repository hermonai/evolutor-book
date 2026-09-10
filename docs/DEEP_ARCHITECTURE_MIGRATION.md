# Architecture migration decisions

| Chapter | Action | Reason |
| --- | --- | --- |
| EVOD-01 · Why Genomic Computation? | KEEP | Preserve IDs/dependencies; no change to reviewed source. |
| EVOD-02 · Learning objectives, data, tasks, and evaluation | KEEP | Preserve IDs/dependencies; no change to reviewed source. |
| EVOD-03 · Differentiation, optimization and tensor programs | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-04 · Reproducible PyTorch training | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-05 · Tokenization and sequence representation | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-06 · Recurrent models and gated state | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-07 · State-space models, selective updates and scans | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-08 · Attention and content-addressed computation | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-09 · Transformers and cached execution | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-10 · Conditional computation and memory alternatives | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-11 · Regulation and expression across levels | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-12 · Development and generated computational structure | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-13 · Learning, structural adaptation and evolution | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-14 · Typed genomic computation systems | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-15 · Operational semantics and expression traces | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-16 · Expression complexity and resource semantics | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-17 · Traces, credit and mechanistic evidence | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-18 · DOGMA primitives and state semantics | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-19 · DOGMA regulation and selective transformations | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-20 · Structured memory, locality and timescales | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-21 · Strands, complements and dual-state hypotheses | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-22 · DOGMA reference model and falsifiable research program | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-23 · Hermon DNA reference architecture | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-24 · DNA-aware Transformer mechanisms | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-25 · Shared experiments without false equivalence | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-26 · Training/inference parity and parallel recurrence | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-27 · Optimization and memory-efficient training | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-28 · Distributed training and model artifacts | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-29 · Benchmark design and comparative evidence | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-30 · Runtime contracts and request lifecycles | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-31 · DOGMA state construction and execution | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-32 · DOGMA state pools and memory ownership | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-33 · DOGMA checkpoints, branching and prefix state | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-34 · DOGMA batching and state-native kernels | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-35 · Hermon DNA prefill, decode and KV state | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-36 · Paged KV, prefix sharing and allocation | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-37 · Continuous batching and precision | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-38 · Speculative decoding and attention kernels | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-39 · Evolutor runtime above both engines | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-40 · Hybrid compressed and addressable memory | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-41 · Compiler, IR and execution planning | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-42 · Database engines as a systems comparison | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-43 · Structural adaptation and lifecycle governance | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-44 · Packaging, deployment and observable services | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-45 · Multi-tenancy, isolation and security | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-46 · Distributed serving and state placement | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-47 · Profiling, performance and hardware backends | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-48 · Genomic sequence applications | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-49 · Streaming, language, code and persistent agents | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-50 · Continual learning and population adaptation | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-51 · AGI capability hypotheses and limits | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
| EVOD-52 · Failures, open problems and reproducible synthesis | DEEPEN IN PLACE | Preserve IDs/dependencies; apply the mechanism/evidence gate during bounded production. |
