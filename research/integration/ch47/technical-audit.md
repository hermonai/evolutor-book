# Chapter 47 author technical audit

Local author review only. The exact supplied synthetic three-request trace,
TTFT/ITL, percentile, goodput, roofline and speedup cases are retained. Fresh
validation rejects malformed/nonfinite/reversed timestamps, invalid quantiles,
nonpositive windows and out-of-window terminal records. A failed zero-token
request has no TTFT sample but stays in the outcome denominator and requires a
terminal timestamp. One-token ITL is absent, not zero. The analyzer requires
closed terminal cohorts and does not implement a live streaming estimator.

Maximum-gap SLO is explicitly distinct from mean TPOT (1/99ms counterexample).
Pooled token ITL differs from per-request distributions. Tests prove the exact
11-token/44tok-s/8goodreq-s arithmetic, percentile permutation invariance,
throughput-goodput reversal and missing/failed outcomes, not real service speed.
The DAG recurrence assumes topological order and sufficient resources; overlap
counterexample gives 70 rather than sum100ms and branch switching after prefill
optimization. Amdahl assumes fixed work/serial fractions and no new overhead.
Matched ratios report dispersion only; no unsupported confidence interval or
independence from correlated tokens is claimed.

FLOP/byte ceilings name a memory boundary. Attention QK+AV excludes softmax,
projections and other layers. Native 2BDV+4BD excludes sigmoid and shared parameter
traffic, matching Chapter34's actual restricted embedding-driven recurrence.
Byte tables are not measured traffic, backend kernels or equal-quality model
comparisons. Chapter35 remains the actual Chapter23 learned-position multi-layer
Transformer. Reference results contain an empty real_backend_measurements list.
CPU/Metal/CUDA/Vulkan table lists required experiment fields, not rankings.
No profiler, GPU benchmark, external system or device kernel was run.

Source-access caveats: packaged Roofline URL failed; primary 2008 Berkeley
Section3 inspected instead. FlashAttention abstract only; DistServe selected
architecture/metric passages; official profiler/tool documents selected API and
overhead/replay/sync passages, not every guide/counter. All claims are narrower
than full-paper replication. Future benchmarks against actual completed
Chapter34/38/46 backends are deferred integration/evidence work. Three original
TikZ/TXT plates and whole-function listings have source/PDF-bound local review.
