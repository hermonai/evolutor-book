# Runtime roadmap

## Semantic layer

- MiniEvolutor defines symbolic compile/regulate/execute/trace behavior.
- PyTorch defines differentiable Transformer and recurrent behavior.
- Full-sequence and incremental paths require parity tests.

## Optimization sequence

1. profile a stable reference;
2. identify the bottleneck;
3. specify the optimized operation;
4. cross-check outputs/state/trace;
5. add failure and precision tests;
6. then integrate batching and serving.

## Likely distinct engines

Transformer models naturally require attention kernels and KV-like state. Recurrent/GCS models naturally require carried state, expression plans, and traces. A common request protocol may sit above them, but internal engines should not be forced into one abstraction.

## Genomic IR gate

Design a portable IR only after at least two working backends need the same typed program representation. The IR must version types, effects, resource bounds, gates, state, trace semantics, and compatibility.

