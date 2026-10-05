# EVOD-23 — Hermon DNA reference architecture

Locally integrated r01 candidate. Transparent pre-norm Transformer implementation
with literal QKV mathematics, row-wise independent attention/gradient oracle,
strict mask shapes, padding-safe positions, causal suffix isolation and offline
reverse-complement invariance. Masked-language pretraining is not implemented.

The synthetic motif pilot uses frozen train/test records, exact reverse-complement
split disjointness, three initialization seeds, a local CNN, an exact string
oracle and independently randomized labels. Results do not establish genomic
capability or a budget-matched model ranking.

Run Python 3.13 with PyTorch: `OMP_NUM_THREADS=1 python drafts/ch23/build.py --render`;
check reproducible assets with `--check`. Six editable vector figures have semantic
TXT specifications; seventeen worked questions include attention arithmetic and
parameter accounting. Source access depths are recorded under
research/integration/ch23. Chapter 24 extends DNA-aware mechanisms; Chapter 25 owns
shared data/model contracts. Standalone local review is not independent acceptance.
