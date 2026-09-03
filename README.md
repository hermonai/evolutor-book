# Evolutor: Genomic Computation

**From Regulation and Expression to Machine Intelligence**

This repository develops Evolutor as an umbrella theory and executable research program:

```text
Genome -> Regulation -> Expression -> output + trace -> verified local evolution
```

Evolutor is not automatically DOGMA, Hermon DNA, a neural network, or a molecular computer. A Genomic Computation System (GCS) may have symbolic, differentiable, or other implementations, and every implementation inherits a claim boundary.

## Bootstrap contents

- an architecture taxonomy and name-lineage audit;
- a claim and theorem ledger with explicit proof obligations;
- a revised book plan and notation standard;
- MiniEvolutor, a deterministic reference for genome/compile/regulate/execute/trace;
- `evo_torch`, minimal Transformer and recurrent DNA baselines with shared training and intervention-based causality tests.

Start with [the book plan](BOOK_PLAN.md), [Chapter 1](book/chapters/01-program-as-genome.md), [Chapter 2](book/chapters/02-five-layers.md), [architecture taxonomy](research/architecture-taxonomy.md), and [theorem ledger](research/theorem-ledger.md).

## Development

```bash
python3 -m pytest
```

PyTorch is the semantic reference layer for early neural experiments. A new tensor library, compiler, or inference engine must be justified by a measured deficiency and must preserve parity with this layer.

## Manuscript status

Chapters 1 and 2 have complete first drafts. Chapter 3 will make the inherited correction record a methodological foundation; Chapter 4 will turn the architecture lineage into a durable provenance scheme.

## Publication status

Bootstrap research repository; private and not publication-ready. No source PDFs are copied here, and this repository currently has no open-source license.
