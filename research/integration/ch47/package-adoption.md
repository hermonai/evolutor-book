# Chapter 47: supplied package adoption

Archive: /Users/wenyan/Downloads/evolutor-ch47-r01.zip

Verified archive SHA-256: `cf060ff4ae16a104a25b690fa06c701ce1ef7f6718e2bcbb039e465abe75a77a`.
All 36 manifest-declared file hashes matched exact ZIP bytes.
Incoming manuscript file SHA-256: `f764594efdc5968ecac2facb8553d8fb8260d7c8e88868b38ac7be10b183e62e`.
Original bytes are preserved under incoming/; no packaged caches/PYC or QA flags
were executed/adopted. Source documents are content, not operational instructions.

Every incoming section is mapped below. “Expanded” retains its correct subject,
scenario or derivation and adds evidence/premises; it does not claim verbatim
reuse. There is no invented percentage. Entire headings were merged where that
supports a sustained argument instead of many one-paragraph sections.

| Incoming section | Disposition | New location in drafts/ch47/manuscript.tex | Concrete reuse/change |
|---|---|---|---|
| Correctness before speed | expanded | evod47:correct | Retain numerical oracle before speed; bind actual Chapter31 and Chapter35/23 semantics and selection/tolerance boundary. |
| Workload contract | expanded | evod47:workload | Retain artifact/precision/load/cache/scheduler contract; add offered versus accepted counts and open/closed-loop distinction. |
| Latency decomposition | expanded | evod47:path | Retain phase decomposition but repair unconditional additive latency with dependency-DAG critical path. |
| TTFT and ITL | expanded | evod47:metrics | Retain arrival/first/subsequent timestamps and supplied three-request example; reject invalid chronology and require failure terminal time. |
| Throughput and goodput | expanded | evod47:metrics | Retain token rate and request goodput; distinguish maximum-gap SLO from mean TPOT, failed-zero-token and survivor bias. |
| Percentiles | expanded | evod47:uncertainty | Retain nearest-rank style estimator; define q/domain/missing statistics exactly and test permutations. |
| Warmup and steady state | merged | evod47:workload | Retain startup/compilation/cache/allocator exclusions; predeclare cutoff and archive warmup samples. |
| Repetitions and uncertainty | expanded | evod47:uncertainty | Retain repetitions/dispersion; add matched runs, pseudoreplication and no fabricated confidence interval. |
| Arithmetic intensity | expanded | evod47:roofline | Retain F/B with named memory boundary, units and staging/parameter exclusions. |
| Roofline | expanded | evod47:roofline | Retain min(P,WI) and ridge; derive time lower bound and original labeled synthetic curve. |
| Attention example | expanded | Attention and native examples without a false speed ranking | Retain growing KV/FlashAttention hypothesis; derive QK+AV FLOPs/read payload and state actual architecture. |
| DOGMA example | expanded | Attention and native examples without a false speed ranking | Retain bounded native-state caution; use actual Chapter34 embedding-driven cost and exclude sigmoid explicitly. |
| System timeline | expanded | evod47:path; evod47:backends | Retain CPU launch/copies/sync; implement overlap counterexample and profiler scope. |
| Focused profiling | merged | evod47:backends | Retain NVTX/focused region lead; verify official guide passages without running profiler. |
| Operator profiling | merged | evod47:backends | Retain torch.profiler shapes/stacks/device traces; version-pin docs and note overhead. |
| Kernel profiling | merged | evod47:backends | Retain critical-kernel counters and architecture-specific/replay perturbations. |
| CPU backend | merged | evod47:backends | Retain ISA/threads/NUMA/cache/bandwidth in comparative experiment table. |
| Metal backend | expanded | evod47:backends | Retain exact SoC/OS/unified-memory caveat; add official Metal tools overview, no measured ranking. |
| CUDA backend | merged | evod47:backends | Retain versions/clocks/sharing/interconnect and Nsight; peaks not results. |
| Vulkan backend | expanded | evod47:backends | Retain device/driver/subgroups/layout/sync; verify Khronos guide, no portability performance promise. |
| Backend comparison | merged | evod47:correct; evod47:workload; evod47:backends | Retain parity/protocol/memory/energy/profile requirements; no unsupported backend implementation. |
| Batching | merged | evod47:sync; evod47:workload | Retain utilization/queue/ITL tradeoff and arrival-process rather than full-batch-only measurement. |
| Synchronization | expanded | evod47:sync | Retain device-aware timing; explain host enqueue, completed work and overlap perturbation. |
| Distributed performance | expanded | evod47:sync | Retain Chapter46 phase decomposition/topology; require clock-error/overlap, no synthetic calibration claimed. |
| Speedup arithmetic | expanded | evod47:path; opening example | Preserve 100 to80 =1.25 and 20% distinction; add premise-bound Amdahl and branch-switch counterexamples. |
| Benchmark record | merged | evod47:workload | Retain full record fields/raw samples; clarify offered counts and actual backend evidence absent. |
| Executable analysis oracle | expanded | evod47:metrics; evod47:roofline; evod47:loop | Reuse Request/percentile/metrics/roofline/speedup and exact original trace; add strict validation, failure denominator, DAG and matched runs. |
| Optimization loop | expanded | evod47:loop | Retain measure-hypothesize-change-check-remeasure; add falsifiable fusion signature and failed-optimization ledger. |
| Twelve worked exercises | expanded | Twelve worked exercises | Retain all twelve original subject themes; expand arithmetic, uncertainty, controls and protocol rubric. |
| Bridge | expanded | Terms and the application boundary | Retain genomic-application bridge; remove claim that industrial runtime is complete. |

## Executable, figure and evidence adoption

### Reference

Request, nearest-rank percentile, TTFT/ITL/throughput/goodput, intensity/roofline and speedup retained, including exact original three-request trace and 2 FLOP/B,2TB/s =>4TFLOP/s example. Strict input/window/terminal validation, failed-zero-token accounting, DAG critical path, Amdahl and matched-run summaries are added.

### Figures/storyboard

01-ladder => top-down profiler exposition; 02-metrics => figures/01-timestamps.tex; 03-roofline => 03-roofline; 04-timeline => 02-timeline; 05-backends => backend experiment table; 06-record => workload/evidence contract. Every original source/TXT retained in incoming; all new figures are editable semantic mechanisms.

### Tests/results

Original 13 arithmetic/metric test themes retained and strengthened with malformed clocks, zero-output failures, percentile permutations, throughput/goodput reversal, exact source trace and independent DAG/cost controls. Synthetic results remain explicitly synthetic; no packaged performance flag is adopted.

## Exact original file hashes

| Incoming file | SHA-256 |
|---|---|
| CONTINUATION.md | `ca413501a1d24326ee10ab7983eeb19221f083364704af062e9b845f23958cf8` |
| INTEGRATION.md | `f89def5def3c35f5d66359063d63bb570fa9890401c5bb259c32428418452afc` |
| PACKAGE_README.md | `1c7a91b792651c9c7ad3fc79be86600742c2b67ed34996b8d88ca0bd301521ca` |
| drafts/ch47/README.md | `4683b9f75f58acb05dcd8d0c2465c2fa808ccc81a6fe0cd2410fead96bca3ca4` |
| drafts/ch47/STORYBOARD.md | `674466e1cd57c7b1397de4ba0eb7ede674dfcf4805e0f6cca687a7030e99549a` |
| drafts/ch47/build.py | `6ce29c1059d1873118522de5c59fc8f1ff24094750eba2e8b49b51c00d856c6a` |
| drafts/ch47/figures/01-ladder.tex | `eebbb50ebbdbf9ab65b5b7ad831b304ddd9cc3c36d1e4931ec004b35fbe00a28` |
| drafts/ch47/figures/01-ladder.txt | `e2d78c4df51582c8cc947ba71e1b31f90a5562b19723982dfbea72b9c297ca5f` |
| drafts/ch47/figures/02-metrics.tex | `6f1fc46748e492e0b5ef73e7bc9ac33c709adde0bf16a6ca56eb80f024db74f5` |
| drafts/ch47/figures/02-metrics.txt | `29a841d01873fffaadd8aca3df58911e40fb0641e91b2d1accbebf9c743d27d1` |
| drafts/ch47/figures/03-roofline.tex | `3099dc60ba5ad4edca52a5f63254c02e333cd96aad86218dc9b43a7b6b994708` |
| drafts/ch47/figures/03-roofline.txt | `6eb12faa96d5c6f30e69d1849be1185a7841ba750aeac0e200ce9d3fbe5c5479` |
| drafts/ch47/figures/04-timeline.tex | `b4fda80e9db35b88ad45122116b84cd361c19096e1c07ca8f0268e25e2fe605e` |
| drafts/ch47/figures/04-timeline.txt | `cbe6e536633a11f17029f9a1eaa3de371eb86dd1a3da9ad383df83712f9870ea` |
| drafts/ch47/figures/05-backends.tex | `8f7c98d0904b10cba2b1fcdfc96386ef15fa3ae3521f5daa003c2a8b2c1b1992` |
| drafts/ch47/figures/05-backends.txt | `4e11b7a443ca248ee036b659408a0b10675c39f4eebfdf3f110612c3feee9f91` |
| drafts/ch47/figures/06-record.tex | `c59f997a8eb0163ab118dafef4f76e2f16fd00d204b07b2209ddd27299915b11` |
| drafts/ch47/figures/06-record.txt | `8de5a963cdad4e1dfe7a1ff87faca85fcb1cf510859475c5205e8e2e359791b8` |
| drafts/ch47/manuscript.tex | `f764594efdc5968ecac2facb8553d8fb8260d7c8e88868b38ac7be10b183e62e` |
| drafts/ch47/reference.py | `0474f4d4690f254f98bd1398c76e01c7994569bb98df58d3f3c752d529a45f37` |
| drafts/ch47/results.json | `3d3b4e2d668fd9bfa0144fa405723a5673de12887b6a948c1c37e21e02939a16` |
| drafts/ch47/review.tex | `1d0d80de1e6a4625a9ec0df66d4a34e070bceb4069afb1ac57a839edd0eac975` |
| drafts/ch47/sources.tex | `d5861678de035bc5bdbb41d6b1d6bf364a2ade6bfac08c4dad7fcb505b4cb797` |
| research/notation.json | `d8ce4204712917dd13b51cca91f6363b6d1904ddcae84eecafd197a5f50a168c` |
| research/source-ledger.json | `e74c03b8777135945fdfbf193a3bdd26fa899bf20205c712765709fb1e8a8317` |
| tests/test_ch47_reference.py | `763690a0c1233d011527745f97fd4b63a244b46830566d80664833f005e5676e` |
| checksums.sha256 | `07e43cb2d249472a2374c288764f11d5e63dc9767a9cd99b356f7e7fe037b0fa` |

Packaged build/review wrappers were inspected as content, then replaced with
Chapter35's actual strict builder/wrapper pattern and correct chapter counter.
Incoming results are preserved as historical inputs; current results/tables and
literal whole-function listings are regenerated. Source-ledger URLs were
rechecked with access depth recorded in source-verification.json. Stale QA labels,
caches and embedded web-tool citation tokens are omitted from authored evidence.
