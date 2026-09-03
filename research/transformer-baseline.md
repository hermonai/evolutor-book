# Transformer DNA baseline

## Purpose

Establish an ordinary, understandable causal Transformer before adding DNA-specific mechanisms. This baseline is not yet “target DOGMA” evidence.

## Reference path

[E07 — Transformer reference: training, prefill, and decode](../book/diagrams/e07-transformer-reference-flow.txt) specifies the full-sequence and incremental paths, KV-state growth, causal boundary, and parity obligation.

Training uses shifted next-token cross-entropy. Reference inference recomputes the full prefix and exposes `step(prefix)`. This is intentionally slow and makes the semantic contract obvious. A KV-cache path is a later optimization and must match the no-cache logits.

## First controlled hypotheses

1. reverse-complement augmentation;
2. exact reverse-complement equivariance;
3. strand-aware attention;
4. regulatory conditioning compared with a generic conditional-control baseline.

Each enters separately after the plain baseline passes causality and artifact gates.
