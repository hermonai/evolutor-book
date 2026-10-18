# Chapter 36 package adoption

Archive integrity: see package-integrity.json. Every declared archive member hash was reverified against exact ZIP bytes, including unexecuted binary/cache entries. Text-only incoming content is preserved under incoming/; packaged QA/acceptance flags and cached/PYC execution were not adopted.

Incoming manuscript SHA-256: `4f577ad4771cfd15446c8dbf3120b9e5f9c8f86524f345eaeabd6443769910d9`.
Incoming reference SHA-256: `e428ca4b8adb4d5664e97eb43b10857b07f0d424c617158f940c041f7acaf518`.
Incoming tests SHA-256: `680bb5f3dde3737e49f47ea4f807f09e1ae70e53b1147563f4c05f321ee8d02d`.
Incoming storyboard SHA-256: `5e236c143918f2435ae26dd88dce6ce0b175b8d72106cd64ed128e2290da6403`.

Every incoming section is mapped below. Destinations are labels in drafts/ch36/manuscript.tex, unless noted. No fabricated conceptual/verbatim/executable reuse percentage is assigned.

| Incoming section | Decision | Destination | Reason/change |
|---|---|---|---|
| The invariant | expanded | evod36:invariant | Specify all-layer tensor geometry and native flatten equality. |
| Logical blocks and physical pages | expanded | evod36:invariant | Retain block/offset arithmetic with scattered physical placement. |
| Generational page references | expanded | evod36:lifetime | Arena identity and issued handles supplement page generations. |
| Reference counts | expanded | evod36:lifetime | Add registry-incidence conservation proof and negative audit control. |
| Appending | merged | evod36:cow | Separate full-page append from private/shared partial tails. |
| Copy-on-write | expanded | evod36:cow | Prove branch isolation through actual native layer candidates. |
| Why full pages are simpler | retained | evod36:cow | Full pages remain immutable under append and share unchanged. |
| Prefix sharing | expanded | evod36:prefix | Bind exact tenant/artifact/mode/token keys and fresh-owner handles. |
| Eviction | expanded | evod36:prefix | Cache entries own registered forks; eviction/live branch test retained. |
| Internal fragmentation | retained | evod36:memory | Derive ceil and bounded tail waste with generated P sweep. |
| External fragmentation | merged | evod36:memory | Restrict fragmentation claim to fixed-page allocation level. |
| Page size | expanded | evod36:memory | Retain page-size tradeoff without transferring measured throughput. |
| Allocation failure | expanded | evod36:atomic | Preflight entire multi-page chunk and COW before publication. |
| Block-table integrity | expanded | evod36:prefix | Seal ordered tables separately from layer payloads; expose forgery limit. |
| Attention over pages | relocated | evod36:evidence | Chapter 38 visitor is separate from contiguous staging; no kernel claim. |
| Branches and beam/search workloads | expanded | evod36:memory | Fanout analysis distinguishes full sharing from divergent tail cost. |
| Reference implementation | expanded | evod36:atomic | Replace detached tuple rows with actual all-layer Chapter 35 cache. |
| Worked result | expanded | evod36:memory | Retain prefix3/page2 scenario and derive 5/6 versus7/6. |
| Memory accounting | expanded | evod36:memory | Correct duplicate logical-row ratio; distinguish occupied/capacity bytes. |
| Security and isolation | expanded | evod36:prefix | Tenant policy and timing leakage remain separate from lifetime. |
| What Chapter 36 does not establish | retained | evod36:evidence | State serial/reference/device boundaries explicitly. |
| Twelve worked exercises | expanded | evod36:exercises | All twelve prompts covered with derivations; extend to twenty worked items. |
| Bridge | retained | evod36:chapter | Closing storage-to-service transition introduces Chapter37. |

## Executable and test adoption

The allocator's block translation, generations, refcounts, COW, fork/release, exact-prefix and eviction algorithms are retained as semantics, then rewritten around actual Chapter 35 tensors and a registered owner ledger. The tuple-only Sequence API is not passed off as native integration. Incoming tests' contiguous/order, fork, partial/full tail, final release/stale generation, cache eviction, waste/capacity and shared mutation cases are represented by layered parity, branch-isolation, generation, cache, OOM and corruption tests. Added multi-page atomicity, duplicate ownership, arena identity and incidence-count adversaries.

## Storyboard, figures and source leads

Incoming 01-translation and 02-index merge into 01-translation's actual cell/block mapping. Incoming 03-fork/04-cow become 02-cow with literal before/after references. Incoming 05-refcount becomes 03-lifetime. Incoming 06-fragmentation becomes 05-geometry with exact T=13 cells. New 04-preflight illustrates multi-page failure. Every incoming TEX/TXT pair was read; new art is native editable TikZ with semantic TXT, rather than copying generic boxes. Kwon/PagedAttention and actual prior-generation/COW leads remain with honest access depth.

The package's brief one-line exercises are expanded into worked derivations, counterexamples and experimental rubrics. No supplied correct major subject is silently dropped. Supplied continuity claims referring to external packages are replaced by the actual stable local prior model interfaces. No Raschka prose/artwork, stale package performance labels, cached results or independent-review flags are adopted.
