# Evolutor: Genomic Computation

**From Regulation and Expression to Machine Intelligence**

This repository develops Evolutor as an umbrella theory and executable research program. [E01 — Genomic Computation System: components and interfaces](book/diagrams/e01-gcs-interfaces.txt) shows the persistent genome, compiled substrate, contextual regulation, expression outputs, trace/cost channel, independent verifier, and versioned evolution loop.

Evolutor is not automatically DOGMA, Hermon DNA, a neural network, or a molecular computer. A Genomic Computation System (GCS) may have symbolic, differentiable, or other implementations, and every implementation inherits a claim boundary.

## Bootstrap contents

- an architecture taxonomy and name-lineage audit;
- a claim and theorem ledger with explicit proof obligations;
- a revised book plan and notation standard;
- MiniEvolutor, a deterministic reference for genome/compile/regulate/execute/trace;
- `evo_torch`, minimal Transformer and recurrent DNA baselines with shared training and intervention-based causality tests.

Start with [the book plan](BOOK_PLAN.md), [Chapter 1](book/chapters/01-program-as-genome.md), [Chapter 2](book/chapters/02-five-layers.md), [Chapter 3](book/chapters/03-correction-record-as-method.md), [architecture taxonomy](research/architecture-taxonomy.md), [theorem ledger](research/theorem-ledger.md), and the [TXT graph standard](book/diagrams/TXT_GRAPH_STANDARD.md).

## Development

```bash
python3 -m pytest
```

PyTorch is the semantic reference layer for early neural experiments. A new tensor library, compiler, or inference engine must be justified by a measured deficiency and must preserve parity with this layer.

## Manuscript status

Chapters 1 through 3 have complete first drafts. Chapter 4 will turn the architecture lineage into a durable provenance scheme.

## Publication status

Public research repository; not yet publication-ready. No source PDFs are copied here, and this repository currently has no open-source license.
