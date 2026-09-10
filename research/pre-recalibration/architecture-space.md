# Architecture-space map

These are comparison families, not an equal-performance claim.

| Family | Representation / memory | Baseline role | Candidate addition | Key confound |
| --- | --- | --- | --- | --- |
| Markov / MLP | Local statistics / fixed window | Trivial and local controls | None initially | A local shortcut may solve the task |
| CNN | Finite receptive field | Local pattern baseline | Context gates | Padding or future context leakage |
| RNN / GRU / LSTM | Compressed recurrent state | Streaming state baseline | Structured state writes | State width and precision |
| SSM / selective state model | State transition dynamics | Efficient sequence baseline | Regulated dynamics | Hidden state caps; numerical equivalence |
| Transformer | Contextual attention, optional KV cache | Retrieval and content interaction | Sparse or context-specific modules | Width, context and caching budget |
| Linear attention | Kernelized carried statistics | Alternative compression | Hybrid memory | Not exact softmax attention generally |
| MoE / dynamic graphs | Routed modules | Direct regulation comparison | Structural growth | Router/expert capacity and dispatch overhead |
| Retrieval / memory systems | Index and persistent records | External access baseline | Controlled memory regimes | Information leakage through the index |
| Program synthesis / neural programs | Executable symbolic structure | Compositional reuse | Developmental construction | Search-budget mismatch |
| GNN / cellular automata / CRN | Graph, lattice or reaction state | Local dynamics | Adaptive local rules | Number of rounds and communication cost |
| Evolution strategies / genetic programming | Parameters or program populations | Structural-search controls | Trace-guided edits | Unequal evaluation budget |
| World models / agents / neuro-symbolic systems | Predictive state plus programs/tools | Planning/composition controls | Modular adaptive controller | Tool/environment information advantage |

Active inference, meta-learning and continual learning are further reading tracks, not interchangeable backbone families. E-S01–E-S11 anchor selected rows; linear-attention, LSTM, GNN, CRN and active-inference primary audits remain open. No family is assigned to DOGMA or Hermon DNA by branding.
