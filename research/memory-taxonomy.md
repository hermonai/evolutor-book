# Memory taxonomy

| Memory | What persists | Write / access regime | Measure separately |
| --- | --- | --- | --- |
| Weights | Learned parameters | Optimizer updates / forward computation | Bytes, update cost, forgetting |
| Activations | Intermediate values | Per forward pass | Peak live memory and recomputation |
| Recurrent state | Compressed prefix summary | Per token / state transition | Dimension, precision, retention error |
| KV cache | Layer attention keys/values | Per decoded token / attention | Context, heads, width, eviction |
| External memory | Explicit records | API or learned write / indexed read | Capacity, access latency, permissions |
| Episodic records | Time/context-linked events | Event writes / retrieval | Provenance and retrieval fidelity |
| Semantic store | Consolidated facts/representations | Consolidation / lookup | Staleness and conflicting updates |
| Working memory | Task-local state | During a task | Lifetime and interference |
| Retrieval index | Searchable keys/embeddings | Index updates / search | Build cost, recall and leakage |
| World state | Estimated environment state | Observation/model update | Partial observability and calibration |
| Program state | Interpreter variables | Execution transitions | Type and lifetime rules |
| Structural memory | Architecture/library choices | Accepted structural changes | Version compatibility and rollback |

Functional categories such as episodic and semantic do not prescribe one implementation. Compact recurrent memory cannot guarantee exact unbounded recall at fixed finite precision. Exact retrieval and streaming accumulation therefore need different task families and cost measurements. E-S02, E-S05 and E-S11 motivate comparisons; no universal winner is inferred.
