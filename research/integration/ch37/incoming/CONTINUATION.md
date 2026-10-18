# Continuity

EVOD-35 defines prefill/decode and KV parity. EVOD-36 supplies finite paged KV allocation. EVOD-37 schedules work under token/page budgets and introduces precision only through explicit conversion + quality gates.

Continuous batching operates at iteration boundaries: completed requests leave; eligible work may enter; per-request causal token order never changes. Prefill and decode have different cost/latency characteristics, so the scheduler uses chunked prefills rather than treating an arbitrarily long prompt as one indivisible iteration.

Precision is a typed policy, not a global "8-bit" label: weights, activations, KV and accumulators may use different formats. Quantization acceptance requires representative calibration/evaluation, numerical error metrics and task/output-quality gates.

Next: EVOD-38 — Speculative decoding and attention kernels.
