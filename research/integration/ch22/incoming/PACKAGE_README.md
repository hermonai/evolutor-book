# Evolutor Chapter 22 package

**Chapter:** 22 — DOGMA reference model and falsifiable research program  
**Stable ID:** EVOD-22  
**Revision:** r01  
**Status:** standalone authored-LaTeX review candidate.

The chapter integrates the established token, regulator, selective-update, memory,
strand and trace contracts into one proposed non-Transformer reference model. It
defines two legal modes: causal streaming and offline strand-symmetric encoding.
The offline reverse-complement branch is never leaked into a left-to-right predictor.

The reference implementation uses PyTorch, performs deterministic forward/gradient
checks, runs a small synthetic training experiment against capacity-reported GRU and
MLP baselines, and records ablations/negative controls. Synthetic success is evidence
about the implementation contract only, not genomic capability.

Reproduce:
```sh
python3 drafts/ch22/reference.py
python3 -m pytest -q tests/test_ch22_reference.py
python3 drafts/ch22/build.py
```
