# Evolutor Chapter 23 package
**Chapter:** 23 — Hermon DNA reference architecture
**Stable ID:** EVOD-23 | **Revision:** r01 | **Status:** review candidate

Hermon DNA is defined here as the Transformer-based research direction, distinct
from DOGMA. The chapter builds a transparent nucleotide-level encoder with explicit
token/position conventions, pre-norm multi-head self-attention, feed-forward blocks,
padding/attention masks, reverse-complement actions, causal and offline objectives,
gradient/parity tests, and a small synthetic experiment.

Commands:
```sh
python3 drafts/ch23/reference.py
python3 -m pytest -q tests/test_ch23_reference.py
python3 drafts/ch23/build.py
```
