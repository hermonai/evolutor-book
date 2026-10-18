# Local technical audit — Chapter 38

Date: 17 October 2026. Reviewer: author/agent; not independent.

One-position modified rejection proof covers arbitrary finite normalized p,q, including draft support gaps and p=q. Accepted mass=min(p,q); rejection mass=sum((p-q)+); correction reconstructs exactly target p in real arithmetic. The draft need not use the target's temperature: recorded q must equal its actual proposal law, while p must equal intended target policy. This corrects an unnecessarily restrictive incoming premise.

General blocks now propose sequentially from history-dependent callbacks, retain q_i and verify target p_i at the corresponding candidate prefixes. Rejection discards descendants; the induction establishes target autoregressive joint law. Exact two-token enumeration, 20,000 seeded joint-frequency trials with fixed .015 tolerance, support/equal/TV checks and a wrong-correction negative control supplement the proof. Statistical agreement alone is not called proof.

Native speculative verification forks real Chapter36 layered state, computes a candidate block, shifts initial/returned logits correctly, releases tentative state in finally and recomputes only committed rows. Tests compare every layer against original full-model cache and require OOM to leave live contents/counts unchanged. No bonus token is emitted; all returned tokens are consumed. This differs deliberately from Chapter37's final unconsumed output. The adapter's replay/recompute cost prevents a speed claim.

Online attention maintains per-head/query (m,l,a). The invariant proves exact union summaries and real-arithmetic associativity. Safe shifts handle initially/all-masked rows; empty rows return zero. Extreme score, merge-permutation, wrong-rescaling, explicit offset mask, dense and installed CPU SDPA controls accompany whole-Hermon-stack logits and per-layer KV comparisons across splits/tiles. Learned positions, norms/residuals/FFN/head remain native. Float64 tolerance is2e-12, not universal backend accuracy.

The page visitor streams logical pages without flattening for attention. Complete-stack online_consume uses contiguous KV; combining it with direct in-place paged append is an explicitly open device lowering, not silently claimed complete. It imports no unfinished sibling API.

The exact-law and exact-algebra proofs assume exact arithmetic/RNG laws; floating implementations use finite normalization and pseudo-random draws. The 2Tb one-query score-buffer traffic model excludes probabilities, caches, metadata and repeated loads, and is not FlashAttention's multi-query IO theorem or measured HBM traffic. No CUDA kernel, learned draft, speedup, service SLO or genomic capability is asserted.
