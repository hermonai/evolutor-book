# Batch C handoff — Chapters 44–47

Completed 18 October 2026 in the shared evolutor-book checkout. The assigned
chapters are completed, tested, locally reviewed standalone candidates.
Cumulative integration, independent specialist/reader review and publication
acceptance remain open. No additional chats/subagents, sibling-chat messages,
staging, commits, pushes, resets or repository cleaning were performed.

## Deliverables

| Chapter | Subject | Source | Standalone PDF | Physical pages | Tests passed |
|---|---|---|---|---|---|
| 44 | Packaging, deployment and observable services | drafts/ch44/manuscript.tex | output/pdf/evolutor-ch44-review.pdf | 13 | 31 |
| 45 | Multi-tenancy, isolation and security | drafts/ch45/manuscript.tex | output/pdf/evolutor-ch45-review.pdf | 12 | 21 |
| 46 | Distributed serving and state placement | drafts/ch46/manuscript.tex | output/pdf/evolutor-ch46-review.pdf | 12 | 21 |
| 47 | Profiling, performance and hardware backends | drafts/ch47/manuscript.tex | output/pdf/evolutor-ch47-review.pdf | 12 | 35 |

The total is 49 standalone physical pages, including four covers and four sets
of front/back matter; it is not an addition to a cumulative book page count.
Every chapter includes an expanded reference implementation, generated results,
literal whole-function listings, three editable native TikZ/TXT mechanism
plates, twelve worked exercises, selective terms/index, primary references,
storyboard, README and strict standalone builder. Total: 12 plates and 48
worked exercises. Storyboards were finalized alongside prose; no independent
pre-authoring storyboard approval is claimed.

## Substantive changes and evidence limits

- Chapter 44 binds model, runtime, tokenizer, configuration and interpretation
  contracts into a release identity. Its data-only capsule checks actual bytes
  against that manifest and an independently supplied trusted pin. Corruption
  and coherent manifest replacement are separate negative controls. The release
  controller remains metadata-only: verified loading/readiness integration is
  a caller obligation. Revision-local canary evidence, nearest-rank tails,
  liveness/readiness/capacity, issued-request settlement, drain conservation
  and compatible rollback have executable contracts. Telemetry privacy,
  error-budget arithmetic, sampling uncertainty and irreversible tool effects
  have explicit limits. No signing, real service rollout or reproducible build
  experiment is claimed.
- Chapter 45 requires exact issued authority objects, session/tenant/action/
  resource matching, current policy epoch and expiry. Structured cache keys
  prevent delimiter aliasing; they do not implement payload authorization or
  cache poisoning protection. Vector quota reservation is checked before
  mutation and settled once. The logical-value noninterference proposition
  excludes timing and availability; a shared-quota counterexample demonstrates
  the stronger claim failing. The only tool is a closed-schema in-memory echo.
  This trusted-process serialized model is not cryptographic authentication,
  penetration testing or production security certification.
- Chapter 46 applies hard feasibility before a declared synthetic placement
  score. Migration freezes writes, reserves destination capacity, verifies
  bytes and advances ownership epoch through explicit prepare/copy/commit or
  abort/cancel transitions. Recovery requires an independently trusted digest.
  Owner/staging/paired-prefill-decode accounting has negative controls and
  conservation checks. Actual Chapter 31 recurrent state and Chapter 35/23
  layered Hermon K/V snapshots are reconstructed in test-local data-only JSON;
  one-token suffix logits match exactly. This is not a detached substitute,
  network transport, durable consensus service or physical page migration.
- Chapter 47 reproduces the original assigned three-request trace: 11 tokens
  in 250 ms = 44 tokens/s; two qualifying requests = 8 good requests/s;
  nearest-rank TTFT p95 = 130 ms. Failed tokenless outcomes remain in the
  denominator; missing ITL is absent, not zero. Maximum-gap versus mean TPOT,
  critical-path overlap and branch switching, Amdahl premises, scoped roofline
  and native/attention arithmetic are explicit. Matched ratios do not claim
  confidence intervals. CPU/Metal/CUDA/Vulkan tables specify experiments;
  real_backend_measurements is empty. No hardware ranking is inferred.

DOGMA remains the non-Transformer direction, Chapter 31 its restricted diagonal
teaching recurrence, and Hermon DNA the actual Chapter 23 learned-position
Transformer used by Chapter 35. None of these tests establishes learned genomic
capability, general intelligence, equal model quality or device performance.

## Package adoption and source access

All four archive digests agree with the original inventory. All 146 declared
member hashes were verified against exact ZIP bytes (36/37/37/36). Text-only
incoming provenance is preserved under each chapter's incoming directory.
Packaged PYC/cache files, stale computed results and inherited QA labels were
not executed or adopted as validation. Every original manuscript section has
an explicit destination and reason: 19/23/21/30 sections, 93 total.

Each research/integration/chNN directory contains package-integrity.json,
package-adoption.md, section-adoption.json, source-verification.json,
technical-audit.md and local-review.json. The maps record original source
hashes, reference/test changes and the consolidation of six incoming figures
into three substantive mechanisms. No invented reuse percentage is reported.

Source access was checked on 17 October. Exact access depth is recorded:
SLSA/OpenTelemetry/Kubernetes official definitions; NIST overview and selected
OWASP mitigation passages; selected primary DistServe passages; Berkeley's
2008 Roofline report Section 3 after the packaged URL failed; FlashAttention
abstract only; selected official PyTorch/Nsight/Apple/Khronos documentation.
Failed URLs and restricted access are disclosed. No full-paper replication,
outside security exercise or external benchmark was performed.

## Verification and frozen evidence

Chapter-specific JUnit reports in build/chNN/tests.xml total **108 passed**,
zero failures, errors or skips: 31 + 21 + 21 + 35. Chapter 44's final extension
was tested on 18 October; the other reports are from 17 October. No cumulative
builder or whole-repository regression ran in this batch. Earlier attempts
using Python installations without pytest are not counted as successful tests.
The working environment is /Users/wenyan/.pyenv/shims/python3, Python 3.13.6
with PyTorch 2.10.0. Each --check derived-artifact check passed on final sources.

To reproduce only the assigned chapter checks, run from the repository root:

```sh
for n in 44 45 46 47; do
  /Users/wenyan/.pyenv/shims/python3 -m pytest -q \
    tests/test_ch${n}_reference.py -o addopts='' -p no:cacheprovider \
    --junitxml=build/ch${n}/tests.xml
  /Users/wenyan/.pyenv/shims/python3 drafts/ch${n}/build.py --check
done
```

Build an individual standalone PDF with the corresponding build.py --render.
Regeneration changes evidence bytes; refresh local review hashes after a
changed source, report or PDF rather than retaining stale closure records.

Each strict compile passed the overfull/missing-glyph/undefined-reference/
undefined-citation/multiply-defined checks. Every final standalone physical
page was inspected in color and grayscale. Figure overlaps, orphaned headings
and listing splits were corrected during iteration. Inherited unicode-math
and caption notices remain, with no observed substantive final layout defect.
A stale Chapter 44 auxiliary file was removed before its final successful
compile. The PDF skill operation marker ran successfully exactly once for
four PDF outputs.

PDF SHA-256 closure:

- Chapter 44: fbcc734930c636f492a53045779bbf702b3345a48830bff6f096a5fcfb547914
- Chapter 45: 7249e8485f473c07758c0d2cfbc3a874a8e4ce05d2a627b6aed164e4cabfb3e0
- Chapter 46: 9b7e6098c9fec79a0f06153c06336ab6a9c718c32e909b77d5bce47ebc3b3f9b
- Chapter 47: 9226fd7a79f9a1b4447b8badce71bc904ff7c284190f0038f9a6bf9f6905303f

Each local-review.json binds actual source, PDF, build record, generated
listings/tables, incoming provenance, JUnit and all page-render hashes.
All four explicitly retain accepted=false and independent_review=false.
The read-only production-admission command was run for Chapters 44–47 with
--require-ready; all four are mechanically ready for coordinator review,
with no evidence blockers. This does not close its listed manual checks.
Chapter 46 additionally binds its unchanged transitive runtime dependencies:

- drafts/ch31/reference.py: b0c0f8cc3815ee9c3156f07e8e427878ef11c77b489139dcbb4835c305d88d9a
- drafts/ch35/reference.py: 3861e11797f0d6c8e480d2426e110d29347c5e6a281742208e49a91ea3075e98
- drafts/ch23/reference.py: a071820f55006631c2b26a4710dab8b16149fc9e2f1b57b546b955d2168d225b

## Integration obligations for the final owner

1. Review adoption maps and technical premises, independently reproduce the
   tests/fixtures and verify hash closure. Local author checks do not close
   specialist/reader review. Existing mechanically ready admission checks
   may be used read-only; their result is not semantic acceptance.
2. Join Chapter 44's release identity, state-schema and rollback policy to the
   actual Chapter 30 publication/resource fences, Chapter 39 runtime and
   Chapter 43 artifact registry. Payload integrity grants neither tenant
   permission nor freshness. No passing cross-batch interface is claimed.
3. Join Chapter 45 authority and reservations to actual Chapter 32/33 pool
   lifetimes, Chapter 36 pages, Chapter 37 scheduling, Chapter 40 memory and
   Chapter 41 effects/labels. Preserve authorization before access and explicit
   cancel/device acknowledgement before physical reclamation.
4. Integrate Chapter 46 owner epochs and data snapshots with actual Chapter 36
   page/pin ownership and Chapter 39 physical execution. Durable metadata,
   resource-side fencing, retry journals, distributed reservations, transfer
   acknowledgement and crash recovery remain production obligations. The local
   paired-PD ticket reserves resources but does not execute or convert them.
5. Validate Chapter 47 experiments against finalized Chapter 34/38/46 backends
   and carry workload, units, outcome denominator and evidence class into
   Chapters 48–52. Synthetic arithmetic must not become a real speedup or
   capability claim. Actual device profiling and energy measurements are open.
6. Only after all batches settle, wire shared navigation and cumulative build,
   consolidate bibliography/glossary/index and labels (evod44: through evod47:),
   resolve actual cross-chapter interfaces, run the whole regression without
   concurrent PDF builds, and inspect the continuous candidate's new pages and
   front/back matter. Standalone pagination does not guarantee cumulative layout.
7. Obtain independent review and explicit publication authorization through the
   existing gates. Shared root maps, tex, scripts, sibling chapters, accepted
   artifacts, actual runtime and finance projects were outside this author's
   write scope and were not modified by this batch.
