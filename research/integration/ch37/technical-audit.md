# Local technical audit — Chapter 37

Date: 17 October 2026. Reviewer: author/agent; not independent.

The scheduler owns a dedicated actual Chapter 36 arena and executes every scheduled prefill/decode through it. Admission reserves ceil((prompt+output-1)/page_size) credits. The proof uses private requests, no external forks, fixed validated output bounds and serial execution; it does not extend to shared-prefix or speculative workspace policies.

Consumed and emitted clocks are explicit: final prefill logits emit output0; each later step consumes previous output. Cache length=prefilled+max(0,emitted-1). Completion releases the cache without consuming the last emitted token. Every iteration audits used<=reserved<=capacity, exactly one pool state per active request and correct causal length. Tests compare greedy outputs with repeated original full-model recomputation under multiple budgets/chunks/page sizes, plus arrival, waiting/readmission, cancellation, invalid identities/lengths and first-token timing controls.

The no-overspend argument follows decreasing remaining token budget; it is not an iteration-runtime bound. Decode-first with rotating ready order is a teaching policy and not a tenant-fairness theorem. Per-lane publication is not an atomic whole-batch transaction. Abstract ticks are not milliseconds; single-output ITL has no sample rather than zero measured delay.

Precision tests use actual PyTorch FP16/BF16 casts and symmetric INT8 reconstruction, including zeros, half-step unsaturated bound, saturation/outlier failures, overflow rejection, nonfinite gate failure and near-tie argmax flip. Layered native KV is rounded after each teacher-forced token; arithmetic is float64 and reconstructed storage remains float64. This is no compressed paged arena or quantized GEMM. Per-row argmax agreement replaces the incoming flattened metric.

The mathematical error analysis assumes a fixed query/mask and exact arithmetic: score perturbation<=norm(q)*epsilon_K/sqrt(d), softmax L1<=2delta by path integration, output norm<=epsilon_V+2Vmax*delta. It does not claim a full-model error theorem. Margin>2epsilon is sufficient for deterministic argmax stability only. Untrained eight-token fixtures do not establish task quality, calibrated uncertainty or future sampled equality.

Open service evidence: representative calibration/task validation, typed native kernels and compressed allocation, asynchronous cancellation fences, fairness policy and offered-load SLO curves. The page-credit conservative policy has no speculative workspace reservation; Chapter38's different consumed/emitted API needs an explicit adapter before combined scheduling.
