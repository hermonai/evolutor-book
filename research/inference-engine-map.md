# Reference inference before specialized engines

2026-09-10 · bounded author audit, not independent review.

| Domain | Chapter home | Mechanism / current finding | Limit / action |
| --- | --- | --- | --- |
| DOGMA Engine | 30–34 | Load a validated candidate; derive sequence state, reset, clone, chunking and batching contracts. | Persistent state shape, cacheability and static/dynamic execution remain architecture-dependent. |
| Hermon DNA Engine | 35–38 | Transformer prefill/decode and KV plus only justified genomic state. | A genomic intervention can invalidate ordinary reuse or batching assumptions. |
| Runtime / compiler | 39–47 | Profile a correct reference, then select lowering and memory policies. | Do not build a branded engine before a bottleneck or semantic requirement exists. |

Evidence and access depth: [source ledger](scientific-recalibration-sources.md).
