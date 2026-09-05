# Experimental program

No experiment below has been run in this reset. IDs and rejection criteria are fixed planning records, not results.

| ID | Question / candidate | Baseline and data | Falsifier before running | Budget / next gate |
| --- | --- | --- | --- | --- |
| EVO-EXP01 | Can the shared pipeline avoid shortcuts and leakage? | Uniform iid DNA, Markov oracle, deliberately leaky negative control | Future edits alter prefix logits or held-out sanity distribution is implausibly low | CPU smoke first; train runner and data hashes required |
| EVO-EXP02 | Does RC symmetry help a strand-invariant task? | Augmentation, tied symmetry model, CNN/GRU/Transformer; synthetic invariant label oracle | No held-out benefit after matching compute/data, or task actually strand-sensitive | Five prespecified seeds; formal oracle first |
| EVO-EXP03 | Which memory regime suits which task? | Exact key-value retrieval and streaming modular count; lookup/state oracles | Apparent advantage disappears under state/context or shortcut controls | Length and state sweeps; report memory/latency |
| EVO-EXP04 | Does trace-guided structural search improve edits? | Exhaustive-small, random, gradient/profiling-informed search on typed DAG tasks | No search-cost advantage at equal validation calls, or degraded retention | Finite edit grammar, semantic verifier and train/test split first |
| EVO-EXP05 | Does developmental construction generalize? | Direct graph, parameter-shared graph, program synthesis / cellular dynamics | Compact encoding saves description but loses task performance or recovery | Define phenotype/environment shift before implementation |

Cross-domain transfer and language/agent studies follow only if a mechanism survives these tasks. No automatic GPU allocation, long training job or external paid service is started. Seed count is not a guarantee of statistical sufficiency; publish individual outcomes and uncertainty and increase runs when variance demands it.
