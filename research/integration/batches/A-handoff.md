# Batch A handoff — Chapters 36–38

Completed 17 October 2026 in the shared evolutor-book checkout on
integration/evolutor-ch22-52. Authoring baseline supplied: 698f309.
These are completed, tested, locally reviewed standalone chapter candidates.
They are not cumulative integration, independent review or publication acceptance.
No staging, commit, push, reset, clean, global navigation edit or sibling-chat
message was performed. No further chats or subagents were created.

## Completed deliverables

| Chapter | Authored source | Standalone PDF | Physical pages | Assigned tests passed |
|---|---|---|---|---|
| 36 | drafts/ch36/manuscript.tex | output/pdf/evolutor-ch36-review.pdf | 14 | 52 |
| 37 | drafts/ch37/manuscript.tex | output/pdf/evolutor-ch37-review.pdf | 14 | 47 |
| 38 | drafts/ch38/manuscript.tex | output/pdf/evolutor-ch38-review.pdf | 15 | 47 |

Each drafts/chNN directory contains the expanded tested reference, generated
results, source-linked whole-function listings via build.py, Pagella/Heros
review wrapper, five editable native TikZ/TXT mechanism plates, approved
storyboard, selective glossary/index and twenty worked exercises/rubrics.
The total is 43 standalone physical pages, including three covers and three
sets of front/back matter; this is not an addition to a cumulative page count.

## Substantive result

- Chapter36 replaces the detached tuple-only example with an all-layer
  actual Chapter35/23 Hermon cache allocator. It proves registry/refcount
  conservation and COW/native continuation refinement, preflights complete
  multi-page appends, distinguishes cache eviction from final reclamation,
  and corrects physical utilization versus duplicate logical multiplicity.
- Chapter37 executes chunked prefill/decode through the real page pool.
  It proves conservative page-credit safety and token-budget accounting,
  corrects first-token prediction timing, tests cancellation/readmission,
  and runs actual layered KV representation experiments. Fixed-query
  attention perturbation and logit-margin bounds have explicit premises.
- Chapter38 proves corrected sampling and the history-dependent
  autoregressive law; tests exact enumeration and seeded joint sampling;
  verifies/rolls back actual paged native state; proves online-softmax
  summaries and real-arithmetic associativity; tests complete Hermon
  continuation, per-layer KV, explicit offset masks and CPU SDPA.
  Its separate page visitor traverses actual scattered pages.

No learned genomic capability, full DOGMA implementation, GPU timing,
native quantized backend, service fairness guarantee, concurrency or
production security certification is inferred.

## Package reuse and integrity

All three archive digests agree with research/integration/package-reuse-audit.json.
All 108 declared member hashes (36 per archive) were rechecked against exact
ZIP bytes. Path traversal, absolute paths and symlinks were rejected.
Incoming manuscripts, references, tests, storyboards, figure TEX/TXT and source
ledgers were read. Text-only incoming provenance is retained; no packaged
PYC/cache, stale computed result or QA/acceptance flag was executed/adopted.

Every incoming manuscript section has an explicit decision/destination/reason:

- research/integration/ch36/package-adoption.md
- research/integration/ch37/package-adoption.md
- research/integration/ch38/package-adoption.md

Original manuscript/reference/test/storyboard hashes are in those maps;
per-member hashes are in each package-integrity.json. Primary source access
depth and failed access attempts are recorded in source-verification.json
and sources.tex. Abstract-only inspection is never labeled full-paper review.

## Actual verification

Final command, using the scratch Python environment:
```sh
/private/tmp/evolutor-batch-a-venv/bin/python -m pytest -q \
  tests/test_ch36_reference.py tests/test_ch37_reference.py \
  tests/test_ch38_reference.py -o addopts='' \
  --junitxml=build/ch36/batch-a-tests.xml
```

Result: **146 passed in 7.25 s**, zero failed/skipped: Chapter36=52,
Chapter37=47, Chapter38=47. This includes the actual stable prior model
interfaces imported by these tests. It is not the whole-repository regression.
The initial system/Xcode and bundled Python attempts failed collection
because they lacked torch/pytest; a scratch venv was then created with
Python3.13.6, PyTorch2.10.0, NumPy2.5.4, pytest9.1.1 and Pillow13.0.0.
These environment failures are not reported as passed tests.

Each chapter's standalone builder completed with strict checks for overfull
boxes, missing glyphs and undefined/multiply-defined citations/references.
All three --check derived-artifact checks passed. The final PDFs' every
physical page was inspected in color and grayscale, with targeted full-page
figure/code views. Diagram overlaps, one wide exercise, a short split
listing and an isolated closing paragraph were corrected. Inherited
unicode-math/caption notices and minor visually acceptable underfull
paragraphs remain; no substantive layout defect is claimed accepted.
The PDF skill marker was run successfully exactly once for three PDF outputs.

All source/PDF/research/provenance/dependency/test-report hashes and page
coverage are frozen in each research/integration/chNN/local-review.json,
with accepted=false and independent_review=false. The upstream runtime
sources remain unchanged: Chapter23 SHA a071820f55006631c2b26a4710dab8b16149fc9e2f1b57b546b955d2168d225b;
Chapter35 SHA3861e11797f0d6c8e480d2426e110d29347c5e6a281742208e49a91ea3075e98.

## PDF hash closure

- Chapter36: `e34c91612c52680e91af78b35b2ef0784a7d6f1b93e8ceb98d0dd713f73ba822`
- Chapter37: `883e1a290952360de4e8c38c8b9d5f0db2d5db3f54bf342cd541b7e829a69dbd`
- Chapter38: `513c0b3453da476f32c6b7d3f012cccd6dddb5359f58415933a506e15e0ace82`

## Stable API and integration boundaries

Chapter36 exports PagedKV(model, capacity, page_size), empty(owner), state,
consume(handle, owner, tokens)->logits, flatten->fresh native Cache,
fork(handle, old_owner, new_owner), release, required_pages and audit.
The pool is tied to the actual CPU float64 causal Hermon artifact.
consume updates the registered handle in place after staging; no caller
should expect Chapter35's returned (logits,new_cache) tuple from this method.
PrefixCache is tenant-scoped exact-prefix LRU bounded by entry count.

Chapter37 Scheduler.submit takes a nonempty prompt and positive bounded
output count. Final prefill emits output0; later decode consumes the previous
output. Completion does not consume its final emitted token and releases
state. Reservations cover prompt+output-1, with no outside forks.
Its precision_rollout is a separate float64 reconstruction experiment,
not a lower-precision Chapter36 pool or exact prefix-cache entry.

Chapter38 native_speculative verifies on a temporary fork, discards it and
recomputes only committed rows. No bonus token. All returned tokens are
already consumed into KV. Do not feed those tokens again through the
Chapter37 convention. It replays initial target logits and recomputes on
commit, so it is a correctness oracle, not an amortized fast path.
Generic speculative_block uses history-conditioned callbacks and actual q_i.

Chapter38 online_consume replaces attention reduction through the entire
actual Transformer but still uses contiguous KV. paged_attention separately
streams Chapter36 pages in logical order with explicit query ordinals.
A direct paged in-place complete-model append kernel is not supplied.
Load and reuse the modules' exposed paging/native objects when exchanging
reference Cache instances; importing one Python source under different
module aliases can create distinct dataclass identities. None is a wire API.

## Unresolved cross-batch checks and exact next steps

No assigned test was deferred for an unfinished sibling API: this batch imports
only completed Chapters23/35 and its own completed Chapter36. The following
remain final-integrator checks, and no passing result is claimed for them:

1. After all authors settle, inspect the three adoption maps/local reviews and
   verify their hashes. Use the Chapter35 wrapper/builder conventions already
   cloned here; consolidate bibliography keys (new keys are evod36:, evod37:,
   evod38:) and namespace/notation/index consistency in the cumulative book.
2. Integrate Chapter39's actual runtime against opaque request-owned handles
   and declared token-consumption conventions. Do not pass one engine's
   state as the other's or import a changing sibling implementation.
3. If the integrated runtime schedules speculation, add an explicit adapter
   for Chapter37 versus38 token clocks and reserve tentative COW/new-page
   workspace. Then test OOM, cancellation, rejection and completion fences
   against the actual stable runtime. Current Scheduler deliberately does
   not advertise speculative scheduling.
4. Chapters45–47 should retain the trusted/serialized boundary and separate
   exact CPU reference, numerical emulation, real device kernel, asynchronous
   reclamation and measured service evidence. No hardware speed or security
   claim may be inherited from these PDFs.
5. The integration owner runs the cumulative build and whole-repo regression
   when sibling compilation has stopped, reviews the resulting new cumulative
   pages/front/back matter, and updates global navigation/convergence records.
   This author did not modify shared root maps, scripts/tex or other chapters.
6. Obtain independent specialist/reader review and publication authorization
   through the existing gates. Current accepted=false and independent_review=false
   must not be promoted merely because standalone builds/tests passed.
