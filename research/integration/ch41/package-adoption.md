# Chapter 41 package adoption

Archive and every declared file hash were reverified against `package-reuse-audit.json`; see `package-integrity.json`. The full incoming manuscript/reference/tests/storyboard/figures/TXT/source ledger are preserved under `incoming/`, without PYC, caches or packaged QA flags. No reuse percentage is asserted.

Incoming manuscript SHA-256: `8328be287e7c144e1ef7cc934b055edaaffa866a87d6dc942ed8d128dab54bdd`. Each original section block also has an exact hash in `package-adoption.json`. The opening is expanded into a concrete prediction problem; stale history claims are corrected.

| Incoming section | Treatment | Authored destination | Reason |
|---|---|---|---|
| Why an IR | expanded | `evod41:ir` | Define program, operation, SSA observations and a concrete before/after example. |
| SSA-like values | retained | `evod41:ir` | Retain one definition per value and producer dependencies. |
| Operation schema | expanded | `evod41:ir` | Add immutable attributes and explicit memory effects. |
| Verifier | expanded | `evod41:verify` | Reject effect lies, unknown schemas and malformed attributes before passes. |
| Effects | expanded | `evod41:semantics` | Remove unsafe purity of engine/retrieval; preserve all declared observations. |
| Constant folding | expanded | `evod41:passes` | Add exact-integer observation proof and floating arithmetic counterexample. |
| Dead-code elimination | expanded | `evod41:passes` | Backward liveness proof retains reads, engine state, memory and tools. |
| Common subexpressions and caching | merged | `evod41:lower` | Keep artifact/RNG/state/version prerequisites; no unsupported CSE pass claimed. |
| Capability-aware lowering | expanded | `evod41:lower` | Call actual Ch39 router with exact artifact; preserve source IDs. |
| Multi-level IR | merged | `evod41:semantics` | Verify narrow comparison against official MLIR docs; no framework implementation claim. |
| TVM comparison | retained | `evod41:lower` | Keep narrow graph/schedule/codegen organization comparison. |
| Resource planning | expanded | `evod41:liveness` | Derive peak bytes including workspace/external state, separate from count proxy. |
| Liveness | expanded | `evod41:liveness` | Fix peak timing to allocation before input release and keep output values live. |
| Scheduling | expanded | `evod41:lower` | Build data dependencies plus a conservative ordered-effect chain. |
| Cost model | merged | `evod41:lower` | Retain legal-before-cheap and measured-versus-estimated boundary, developed Ch39/42. |
| Optimization legality | expanded | `evod41:passes` | State pass proof premises and excluded batching/prefix/fusion rewrites. |
| Executable compiler | expanded | `evod41:oracles` | Add independent recursive oracle and real Ch39/40 handlers. |
| Negative tests | expanded | `evod41:oracles` | Add randomized DAGs, denial preservation, effect-erasure and result-type controls. |
| IR serialization | expanded | `evod41:boundaries` | Pin schema and distinguish trusted objects from an untrusted decoder. |
| Debuggability | expanded | `evod41:boundaries` | Preserve source IDs and explain future many-source fusion lineage. |
| Twelve worked exercises | expanded | `evod41:exercises` | Retain concepts with concrete answers and scheduling rubric. |
| Bridge | relocated | `final Vocabulary section` | Final Vocabulary and comparison boundary transitions to databases. |

## Executable and figure adoption

Incoming PURE={const,add,retrieve,engine} is intentionally corrected. Engine/retrieval observations are effects; handler outputs are checked. The incoming post-release peak count missed allocation overlap.

All incoming test topics are retained conceptually in expanded chapter-local tests; packaged tests/logs are not treated as local passing evidence. Incoming twelve exercise topics are retained and extended with derivations, negative cases and open-problem rubrics.

The six incoming figure questions are merged into three new native TikZ mechanism plates with TXT companions. Incoming generic box chains/repeated paragraph panels are not reproduced as final artwork. Pipeline/IR/verifier become typed SSA with effect edges; passes become before/after exact instructions; lowering/schedule become liveness timing plus generated dependency records.

Original source-ledger leads were checked at the recorded access depth in `source-verification.json`; incomplete ARIES full-PDF access is recorded rather than upgraded to a full read. Local authored review is not independent review or publication acceptance.
