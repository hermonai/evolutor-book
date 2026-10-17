# Continuity
EVOD-23/24 define Hermon DNA as a Transformer-based DNA-aware direction with strict causal and offline/strand-aware modes kept distinct. EVOD-35 is the causal serving path. It derives one-layer multi-head self-attention prefill, token-by-token decode and append-only KV state with explicit positions.

Full causal execution is the correctness oracle. Cached decode must match the logits/hidden output of full execution for every prefix under deterministic settings. KV cache identity includes model/layer/head geometry, dtype/device and position convention. This chapter uses contiguous per-request cache to expose semantics; Chapter 36 introduces paging, sharing, reference counts, fragmentation and eviction.
