# Continuity contract

Inherited from EVOD-18..21:
- DOGMA is a proposed non-Transformer DNA-native direction, not a renamed RNN.
- State, regulator, expression, strand, memory locus, module and trace have explicit
  ownership.
- Selective updates require declared gates and state-reset semantics.
- Chapter 21 proved that full-record reverse-complement dual state contains suffix
  information and is illegal for ordinary left-to-right next-token prediction.

EVOD-22 resolves the mode split:
1. `causal`: one forward state, prefix-only token access, legal for next-token loss.
2. `offline_dual`: forward plus aligned reverse-complement state, legal for
   whole-record classification/annotation objectives, not causal generation.

New contribution: one executable reference model, trace schema, objective contracts,
baseline/ablation harness and falsification matrix.

Next: EVOD-23 — Hermon DNA reference architecture.
