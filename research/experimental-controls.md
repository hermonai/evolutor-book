# Experimental controls

## Required run record

Every comparison reports model family/version, source commit, config hash, dataset and split manifest, tokenizer, checkpoint hashes, parameter count, model width, state dimension, layers, heads and FFN width where applicable, training tokens, context length, optimizer, learning-rate schedule, batch size, seed list, hardware, precision, wall-clock/compute accounting, metric code, and causality output.

## Matching conventions

- **Parameter matched** controls stored trainable scalar count.
- **Width matched** controls representation width.
- **State-capacity matched** controls carried recurrent state or declared memory budget.
- **Compute matched** controls a specified training/inference compute budget.

These conventions bracket different questions; none is universal fairness.

## Causal models

For any prefix length \(t\), intervening on \(x_{>t}\) must not change \(y_{\le t}\) beyond a justified tolerance. Use finite interventions, not only gradients at initialization.

## Claim attribution

“X causes Y” requires a one-factor ablation, generic control, transplant when feasible, per-seed outcomes, capacity table, and negative-result record. A surprising architecture ranking triggers an oracle audit.

## Artifact policy

Uncommitted trees are not source identities. Store immutable configuration, data, code, checkpoint, and result hashes. Preserve failures and superseded claims.

