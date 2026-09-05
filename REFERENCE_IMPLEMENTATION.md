# Reference implementation reset

## Existing code classification

All source modules were inspected; the snapshot passed 16 repository tests. Passing tests support only tested semantics.

| Module group | Classification | Decision / limitation |
| --- | --- | --- |
| minievolutor gene.py, genome.py | Typed-record prototype | Runtime Python types and unique keys; not formal type-system soundness |
| substrate.py | Acyclic scheduler prototype | Topological scheduling can scan remaining nodes repeatedly; no universal linear compile-time claim |
| regulation.py | Context-only gate prototype | Evaluates every gate up front; cannot use newly computed intermediate values as regulatory input |
| expression.py | Deterministic interpreter prototype | Counts firings, not full runtime; disabled prerequisites can produce missing-input errors |
| trace.py | Mutable event list | “Append-only” intent is not enforced against list mutation |
| evolution.py | Local structural checks | Preserves interfaces and compilation, not behavior or safety of arbitrary callables |
| package __init__ files | Public interfaces | Names remain historical pending redesign |
| evo_torch recurrent_dna.py | GRU teaching baseline | No novel DNA mechanism; step/full-state parity exists |
| transformer_dna.py | Causal Transformer teaching baseline | No KV cache; step recomputes prefix; learned positions limit configured length |
| tokenization.py | DNA tokenizer prototype | Empty encoding dtype and padding/loss contract need review |
| training.py | Next-token loss helper | No complete experiment runner or padding mask contract |
| inference.py | Greedy prototype | Does not ensure eval mode or validate all length cases |
| causality.py | Intervention diagnostic | One deterministic suffix change; no full intervention suite; restore mode in finally before robust use |
| metrics.py | Parameter counter | Insufficient resource/capability evaluation alone |
| scripts/validate_provenance.py | Structural schema prototype | Checks nonempty identities, not strict digest syntax or truth |

## Proposed stack

Pure task generators and exact oracles; model-neutral batch/loss/state interfaces; Python/PyTorch baselines; causality and parity tests; training runner; immutable artifacts; generated comparison tables. Keep interpreter/program-composition research separate from sequence-model training so neither can borrow the other's evidence.

No Rust runtime, framework fork or large code rewrite in this phase. First fix narrow contracts when a chapter needs them. A new foundation library requires a measured PyTorch limitation and reference-equivalent semantics.
