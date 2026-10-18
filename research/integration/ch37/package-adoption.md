# Chapter 37 package adoption

Archive integrity: see package-integrity.json. Every declared archive member hash was reverified against exact ZIP bytes, including unexecuted binary/cache entries. Text-only incoming content is preserved under incoming/; packaged QA/acceptance flags and cached/PYC execution were not adopted.

Incoming manuscript SHA-256: `f778204e1f59f67069ae468fa003fbfc740a40c752d44ea029172caf328b3d6b`.
Incoming reference SHA-256: `586cefdf6dcba0cc5fd96d363c12669af976cc32829cdbb8814b4ba567330e18`.
Incoming tests SHA-256: `19edac4022833398f2fe8708cf364cef1b99db1fa427f1f5afe5886723e250c1`.
Incoming storyboard SHA-256: `8aa6e64ac99aa027aa6a0c73fea6340579ea86ae4992d970f9195b85e7f8b194`.

Every incoming section is mapped below. Destinations are labels in drafts/ch37/manuscript.tex, unless noted. No fabricated conceptual/verbatim/executable reuse percentage is assigned.

| Incoming section | Decision | Destination | Reason/change |
|---|---|---|---|
| Iteration-level scheduling | expanded | evod37:schedule | Retain iteration membership changes and rotate decoders. |
| Resource-aware admission | expanded | evod37:admission | Bind real pool; prove conservative maximum-page reservations. |
| Prefill and decode are different | expanded | evod37:clock | Correct first output to final-prefill logits and consumed count P+O-1. |
| Chunked prefill | expanded | evod37:schedule | Bound prompt chunks by remaining token units and C_p. |
| Continuous batch churn | expanded | evod37:schedule | Implement native completion/release, readmission and serialized cancellation. |
| TTFT | expanded | evod37:metrics | Use explicit completion boundaries, including queueing and prefill. |
| Inter-token latency | expanded | evod37:metrics | Undefined single-token ITL is a dash, not a zero sample. |
| Throughput is another axis | expanded | evod37:metrics | Compute useful-output and consumed-work numerators separately. |
| Fairness | expanded | evod37:metrics | Explain finite-workload completion versus starvation/tenant fairness. |
| Precision is typed | retained | evod37:precision | Keep separate weight/activation/KV/accumulator/output roles. |
| FP16 and BF16 | expanded | evod37:precision | Use actual PyTorch CPU casts; reject overflow. |
| FP8 | merged | evod37:precision | Keep family/contract distinction; no unverified current hardware claim. |
| INT8 | expanded | evod37:precision | Derive unsaturated half-scale bound and zero-scale convention. |
| SmoothQuant as an example of a method | retained | evod37:precision | Retain rescaling/calibration method comparison without borrowing its quality. |
| KV precision | expanded | evod37:gate | Execute repeated rounded native layered KV, label approximate state. |
| Error metrics | expanded | evod37:error | Add fixed-query attention perturbation bound and per-row argmax. |
| Quality gates | expanded | evod37:gate | Fail closed on nonfinite metrics and apply declared thresholds. |
| Calibration | expanded | evod37:gate | Separate representative calibration and held-out task evaluation. |
| Saturation and underflow | expanded | evod37:precision | Outlier and saturation controls delimit rounding guarantee. |
| Precision and batching interact | retained | evod37:gate | Explain changed page capacity/batch frontier without simulated byte savings. |
| Chunked prefill and tails | merged | evod37:schedule | Retain prompt chunk overhead and latency-policy discussion. |
| Reference scheduler | expanded | evod37:schedule | Execute real paged model instead of detached counters. |
| Reference precision oracle | expanded | evod37:gate | Replace approximate bit trick and flattened argmax with native casts/row metrics. |
| SLO experiment design | expanded | evod37:metrics | Declare arrival/load, quality, percentile and high-water evidence. |
| No context-free winner | retained | evod37:metrics | Use load curves rather than fabricated best operating point. |
| What Chapter 37 does not establish | retained | evod37:gate | No production fairness/kernel/task-quality claim. |
| Twelve worked exercises | expanded | evod37:exercises | All twelve subjects retained; twenty worked quantitative/design items. |
| Bridge | retained | evod37:chapter | Transition explicitly budgets speculation and mask/precision requirements. |

## Executable and test adoption

The decode-first/chunk-fill policy, request trace, FP16/BF16/INT8 representation study and numerical gate are retained. Counter-only requests become actual paged-model requests with reservations, cancellation and native greedy oracle parity. Incoming budget/chunk/priority/arrival/order/TTFT cases remain; rounding/zero/INT8 bound and argmax-negative cases remain. The BF16 bit trick is replaced by native cast; extra first decode is corrected; global flattened argmax becomes row-wise agreement; nonfinite inputs fail closed.

## Storyboard, figures and source leads

Incoming admission becomes01-reservation with actual credit cells; mix becomes02-timeline; metrics becomes03-clock; precision and quantization/gate become04-quantization and05-margin. The incoming generic frontier is relocated to workload/load-curve prose, not reproduced as measured data. All six incoming TEX/TXT pairs were read. Orca, Sarathi-Serve, VTC and SmoothQuant leads are retained with precise access depth; the exact tensor-role policy remains in prose and tested reference.

The package's brief one-line exercises are expanded into worked derivations, counterexamples and experimental rubrics. No supplied correct major subject is silently dropped. Supplied continuity claims referring to external packages are replaced by the actual stable local prior model interfaces. No Raschka prose/artwork, stale package performance labels, cached results or independent-review flags are adopted.
