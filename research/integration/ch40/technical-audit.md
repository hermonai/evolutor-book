# Chapter 40 technical audit — 17 October 2026

## Contract correction and reuse

Content-only summary ID equality from the incoming tests is intentionally replaced by fresh occurrence identity; identical summaries retain identical text but distinct source/occurrence identity. Original direct-only tombstones did not invalidate derived summaries.

Full per-section and figure adoption is in package-adoption.md/json. All incoming
manifest hashes were checked; cached executables, results and QA claims were not adopted.

## Mathematical and executable review

Strict ancestor availability is monotone under fixed DAG bytes, nondecreasing time and growing tombstones. A concrete collision proves summary non-invertibility. Count/UTF-8 payload bounds are proved separately from actual object/tokenizer memory. Memoized availability, depth32/capacity10000 bounds, stale-index checks, transitive forgetting and issued-context persistence are tested. No physical erasure or disk persistence is implemented.

## Failure and integration boundary

Local tests cover negative controls as well as positive fixtures. These are
contract tests, not learned capability, independent scientific review, actual
hardware benchmarks, concurrency/security certification or production durability.
Cross-batch integration is not claimed. The batch B handoff identifies actual
prior-engine state, Chapter30 lifecycle and stable Chapter36 allocator checks
for the coordinator. Source/PDF hashes and test/render results belong to the
final local-review.json, with accepted=false and independent_review=false.
