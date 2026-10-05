# Continuity contract
EVOD-22 froze DOGMA as a proposed non-Transformer model with fast state, addressable
memory loci, explicit causal/offline modes and falsification criteria.

EVOD-23 begins a separate branch:
- Hermon DNA is Transformer-based.
- Single-nucleotide A/C/G/T tokenization is the reference default; tokenizer choice
  remains an experimental variable.
- `offline_encoder` uses bidirectional self-attention and may use RC-symmetric
  whole-record objectives.
- `causal_lm` uses a strict triangular mask and next-token target shift.
- Full-record reverse-complement features are forbidden in causal next-token mode.
- Reverse-complement sharing/equivariance is a testable design choice, not claimed
  as unprecedented; Caduceus and other genomic models are explicit comparison points.

Next: EVOD-24 — Tokenization, sequence objectives and genomic data contracts.
