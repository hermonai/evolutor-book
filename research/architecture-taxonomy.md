# Architecture taxonomy

## Umbrella

**Evolutor / GCS** is a formal computational program with five roles. [E01 — Genomic Computation System: components and interfaces](../book/diagrams/e01-gcs-interfaces.txt) gives the full decomposition, including compilation, transient expression plans, trace/cost output, independent verification, and persistent version change.

It can be instantiated by a symbolic interpreter, graph runtime, differentiable model, Transformer, recurrence, or future molecular compiler. No one instantiation defines the umbrella.

## Independent DNA-LLM branches

| Dimension | Transformer DNA line | Non-Transformer DNA line |
| --- | --- | --- |
| proposed target name | DOGMA | Hermon DNA |
| baseline | causal Transformer | GRU / simple state model / SSM |
| sequence interaction | causal attention | recurrence, scan, graph, or regulated state |
| incremental memory | KV or equivalent attention state | carried fixed/structured state |
| natural strength to test | exact content access and retrieval | streaming sufficient statistics and state transitions |
| central risk | quadratic prefill / growing KV for standard attention | state bottleneck / weak exact retrieval |
| genomic hypotheses | strand-aware attention, regulatory conditioning | expression gates, state organization, GCS traces |

The table is a research map, not a winner declaration.

## Implementation layers

1. **Formal theory:** types, semantics, theorems, cost models.
2. **Executable symbolic reference:** MiniEvolutor.
3. **Differentiable semantic reference:** PyTorch Transformer/recurrent baselines.
4. **Training system:** data, optimization, checkpoints, evaluation.
5. **Inference system:** prefill/step, state ownership, batching, kernels.
6. **Optimized runtime:** only after reference parity.
7. **Molecular realization:** separate compiler, kinetics, and wet-lab validation.

Claims do not cross layers automatically.
