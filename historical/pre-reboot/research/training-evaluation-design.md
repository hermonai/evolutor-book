# Shared training and evaluation design

## Shared surface

Both neural branches accept token IDs `[B,T]`, return logits `[B,T,V]`, use the same next-token objective, and consume the same dataset/split manifests. They share metric definitions, seed policy, checkpoint metadata, causality interventions, and reporting tables.

They do not share internal state structures, inference engines, or hidden capacity assumptions.

## Training

[E16 — Training, evaluation, and artifact provenance](../book/diagrams/e16-training-evaluation-flow.txt) connects immutable manifests to tokenization, optimization, frozen evaluation, and the final artifact bundle. It also marks integrity failures and keeps per-seed records primary.

The first loop will use ordinary PyTorch optimizers and checkpoint `state_dict` plus a versioned architecture config. Dataset and source hashes live with every result.

## Inference

- Transformer reference: prefix recomputation, then a parity-checked KV-cache prototype.
- Recurrent reference: explicit carried state and repeated step parity.
- GCS symbolic reference: expression plan, store, output, and trace.

## Evaluation gates

1. intervention causality;
2. training/inference parity;
3. data leakage and oracle audit;
4. parameter/width/state/compute tables;
5. per-seed inspection;
6. negative-result preservation.

Initial tasks separate exact retrieval from running aggregates, then add genomic motif and regulation tasks with group-aware splits.
