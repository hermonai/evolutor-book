# EVOD-24 — DNA-aware Transformer mechanisms

This chapter extends Chapter 23's Transformer reference instead of restarting
Chapter 5's dataset explanation. Its artifacts implement token-span geometry,
base-target availability, a joint reverse-complement/orientation feature action,
rotary base-coordinate positions, local/global causal access and ragged attention.

Tests include independent matrix rotations, float64 sparse/dense values and all
Q/K/V gradients, finite differences, finite suffix perturbations, padding and
invalid domains. No genomic training, performance speedup, retrieval pipeline or
production sparse kernel is claimed. Six original TikZ figures have same-stem
semantic TXT descriptions; twenty exercises have solutions/rubrics.

Run drafts/ch24/build.py --render and --check with Python 3.13 and PyTorch.
The incoming r01 data-contract material overlaps canonical Chapter 25 and remains
intact in external integration staging; incoming metadata is archived in
research/integration/ch24/incoming. Reconcile those contracts into Chapter 25.
The Chapter 21 offline dual/RC state is forbidden as causal prefix information.
DOGMA remains non-Transformer, Hermon DNA Transformer-based, and Evolutor the
broader orchestration/research layer. Scientific acceptance remains open.
