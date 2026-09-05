# Shared PyTorch research platform design

Status: design, not a completed trainer. Existing GRU and Transformer are teaching baselines.

## Model and task contracts

A task supplies generated inputs, target positions, padding mask, train/validation/test split hashes and an independent oracle. A sequence model returns logits \([B,T,V]\). A causal decoder predicts position \(t+1\) using only positions through \(t\). A bidirectional encoder is permitted for explicitly noncausal classification, never silently used as an autoregressive baseline.

Start with uniform and empirical Markov predictors, fixed-window MLP, causal CNN, GRU, causal Transformer and a documented SSM implementation. Use the same tokenization, data stream and evaluation code. Equal parameters, width, compute and memory define different comparisons; report each matched axis and each remaining mismatch.

## Gates before learning claims

G0 implementation and oracle integrity; G1 suffix intervention at multiple boundaries; G2 capacity/config reporting; G3 shortcut tests; G4 independently seeded training; G5 strong baselines; G6 mechanism ablation/transplant; G7 claimed scaling; G8 independent reproduction where feasible.

Uniform iid data over \(V\) symbols has expected next-symbol entropy \(\log V\). Finite held-out losses fluctuate; a small empirical deviation is not by itself proof of leakage. Calibrate the sanity test with oracle simulation and held-out uncertainty.

## Artifact contract

Experiment ID; hypothesis/falsifier; source commit plus dirty-tree digest; model and optimizer configs; tokenizer identity; dataset split hashes; actual architecture dimensions; training/evaluation commands; software versions; hardware/precision; seeds; per-seed metrics; checkpoint hashes; failures; generated report. No secret paths or credentials.

Record state parity as well as logits. Tests at float32 tolerances do not authorize the same tolerance for all dtypes. Distinguish teacher-forced full-prefix reference, incremental recurrent inference, future cached attention and the serving system.
