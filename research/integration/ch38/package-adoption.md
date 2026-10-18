# Chapter 38 package adoption

Archive integrity: see package-integrity.json. Every declared archive member hash was reverified against exact ZIP bytes, including unexecuted binary/cache entries. Text-only incoming content is preserved under incoming/; packaged QA/acceptance flags and cached/PYC execution were not adopted.

Incoming manuscript SHA-256: `3b3b0ba0d90465cc0734faa8806b7d2e2cf06291d3bf4c5f96031945a39061ba`.
Incoming reference SHA-256: `7afc26a8bf81e79ff13bb0b3f73563b5792b08703f474f34a3d13ed53fe3cdfa`.
Incoming tests SHA-256: `b5cbecf5d90fd4c8064c77b5a19c81bd82d71669dae37a7a4487202f8a6bfddb`.
Incoming storyboard SHA-256: `20accd9b74a38bad74ca574f7b34cdd968847821e263f82d66c0c0aa76e15dc2`.

Every incoming section is mapped below. Destinations are labels in drafts/ch38/manuscript.tex, unless noted. No fabricated conceptual/verbatim/executable reuse percentage is assigned.

| Incoming section | Decision | Destination | Reason/change |
|---|---|---|---|
| Modified rejection sampling | expanded | evod38:sampling | Retain algebra; add support-zero, equal-law and wrong-fallback examples. |
| Acceptance and total variation | retained | evod38:sampling | Derive overlap =1-TV and distinguish latency. |
| Speculative blocks | expanded | evod38:blocks | Use history-dependent callbacks and prove joint autoregressive law. |
| Identity and sampling contracts | expanded | evod38:blocks | Correct overly strong identical-temperature premise; actual proposal law suffices. |
| State commit and rollback | expanded | evod38:commit | Verify on actual paged fork; release tentative refs and recompute committed native state. |
| Speed model | expanded | evod38:cost | Derive no-bonus/bonus expected count with independence assumption stated. |
| Exact attention | expanded | evod38:attention | Specify allowed sets, dimensions and vector values. |
| Online softmax | expanded | evod38:attention | Prove summary invariant/associativity and empty-row stable policy. |
| FlashAttention and IO awareness | retained | evod38:io | Read primary algorithm and distinguish CPU loop from device kernel. |
| Simplified traffic model | expanded | evod38:io | Retain2Tb model; derive exact bytes and less-than1% limited inference. |
| Fusion | merged | evod38:io | Keep occupancy/register/shape tradeoffs without invented benchmark. |
| Paged and low-precision attention | expanded | evod38:native | Separate page visitor from full-stack tiled continuation and precision semantics. |
| Executable oracle | expanded | evod38:native | Extend package algebra and one-query test to real multi-layer Hermon. |
| Evidence ladder | retained | evod38:io | Separate proof, traffic model, device profile and service SLO evidence. |
| Failure modes | expanded | evod38:blocks, commit, native, io | Turn sampling, support, rollback, mask, overflow and order failures into controls. |
| Twelve worked exercises | expanded | evod38:exercises | All twelve subjects retained; expand to twenty derivation/coding/design answers. |
| Closing the engine layer | expanded | evod38:chapter | Correct finished-engine wording to tested references and remaining backend gates. |
| Bridge | merged | evod38:chapter | Bridge to heterogeneous typed runtime remains, with no sibling API import. |

## Executable and test adoption

normalize, acceptance/correction, output-law and traffic concepts are retained and hardened. Static list-based speculative blocks become history-conditioned proposals; actual target block verification uses Chapter 36 forks. One-query online softmax becomes H×N queries with explicit masks and a complete Hermon adapter. All incoming marginal/equal/TV/residual/support/seed/attention/stability/traffic/bad-shape/probability subjects remain, plus exact conditional enumeration, seeded joint sampling, native commit/OOM, full-layer KV parity, SDPA offsets, all-masked rows and merge-permutation controls.

## Storyboard, figures and source leads

Incoming draft-verify and block become02-dependencies; rejection becomes01-mass; attention becomes04-online and05-mask. New03-rollback binds lifetime to real pages. Incoming fusion and evidence figures are merged into the IO/evidence derivation rather than repeated generic arrow chains. All six TEX/TXT pairs were read. Leviathan, Chen, FlashAttention and FlashAttention-2 leads are retained, distinguishing inspected methods from abstract-only claims.

The package's brief one-line exercises are expanded into worked derivations, counterexamples and experimental rubrics. No supplied correct major subject is silently dropped. Supplied continuity claims referring to external packages are replaced by the actual stable local prior model interfaces. No Raschka prose/artwork, stale package performance labels, cached results or independent-review flags are adopted.
