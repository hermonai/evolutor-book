# Chapter 35 technical audit — 17 October 2026

Starting revision: 7728387. All 36 declared incoming ZIP hashes verified.
No packaged cache, PYC, build success or visual-review claim was executed/adopted.

## Architectural continuity

The package's single-head rotary-attention toy did not implement the actual
Chapter 23 Hermon DNA model. Import the real module and cache its normalized
QKV separately at every layer. Preserve learned absolute position embeddings,
multi-head geometry, residuals, GELU FFN, biases, final normalization and LM head.
Do not transfer a uniform RoPE-shift identity to learned positions.

The reference is a single unpadded canonical ACGT causal record, CPU float64,
bounded model geometry and eval mode. Offline classification/strand averaging,
padding/packing/ambiguous tokens and training restart are not supported.

## Proof and independent checks

Token/chunk and layer induction proves exact-real causal parity under fixed
parameters, positions, information access and deterministic semantics. The
full oracle calls the original causal_logits, not the cache append function.
Per-layer original-model projection hooks check K/V identity. All six splits
across three model seeds, all 32 chunk compositions, three geometry variants,
future-token perturbations and a hand-computed retrieval are checked.

For a past length t, continuation query i allows j <= t+i. The independent
PyTorch SDPA explicit-mask oracle verifies polarity and offset. Upper-left
rectangular is_causal is a deliberately failing shortcut. Functional attention
dropout requires explicit zero for inference.

Tolerances 2e-12 absolute/relative are fixture checks, not a universal
finite-precision theorem. Greedy generation and genomic quality remain untested.

## Cache and cost accounting

Owner/model/mode/token metadata and every layer's shape/dtype/finiteness are
checked before append. Identity includes parameters and relevant nonparameter
normalization/GELU settings. Tensor dataclasses are not deeply immutable;
fresh storage plus content seals detects accidental mutation. A resealed
forgery deliberately passes structure and changes continuation, separating
integrity from trusted replay and authentication.

Actual resident fixture payload is 1536 bytes at six tokens. The large 384 MiB
example is a separate geometry calculation. Old-prefix read/write traffic
2*gamma*G*P + gamma*G*(G-1) is derived separately from final payload, new writes,
extra clones, hashing, allocator overhead and observed device memory.

## Boundaries and handoff

No GQA implementation, paging/sharing/COW, quantized KV, optimized attention
backend, concurrent cache transaction, untrusted-object loader or production
security proof. Chapter 36 must preserve this exact ordered logical KV while
changing physical allocation and ownership/reference lifetime.
Six original vector/TXT figures and twenty worked solutions remain locally
reviewed candidates, not independent acceptance.
