# Batch B handoff — Chapters 39–43

Completed 18 October 2026 in the shared `evolutor-book` checkout, authoring
baseline `698f309`, branch `integration/evolutor-ch22-52`. All five assigned
chapters are authored, tested and locally reviewed as standalone candidates.
Cumulative integration, independent review and publication acceptance remain
open. This handoff returns the assigned material to the integration owner.

No staging, commit, push, reset, clean, shared navigation/build-script/tex edit,
other-repository modification, sibling-chat message or new chat/subagent was
performed. Writes were confined to the assigned chapter/research/test paths,
their generated standalone artifacts and this handoff.

## Deliverables and verification

| Chapter | Authored source | Standalone PDF | Physical pages | Tests passed |
|---|---|---|---:|---:|
| 39 | drafts/ch39/manuscript.tex | output/pdf/evolutor-ch39-review.pdf | 12 | 34 |
| 40 | drafts/ch40/manuscript.tex | output/pdf/evolutor-ch40-review.pdf | 12 | 37 |
| 41 | drafts/ch41/manuscript.tex | output/pdf/evolutor-ch41-review.pdf | 13 | 50 |
| 42 | drafts/ch42/manuscript.tex | output/pdf/evolutor-ch42-review.pdf | 11 | 40 |
| 43 | drafts/ch43/manuscript.tex | output/pdf/evolutor-ch43-review.pdf | 12 | 28 |

Total: **60 standalone physical pages and 189 passing chapter-specific tests**,
zero failures or skips. Page totals include five title pages and individual
front/back matter; they are not an increment to the continuous manuscript.
Each chapter contains sustained explanations, premise-bound proofs, worked
arithmetic, twelve worked exercises/rubrics, selective vocabulary/index,
literal whole-function listings, generated result tables and three original
editable TikZ mechanism plates with semantic TXT companions.

The source directories also contain `reference.py`, `results.json`,
`review.tex`, `build.py`, `sources.tex`, `README.md` and `STORYBOARD.md`.
Every chapter has package-integrity/adoption/source-verification/technical-audit
records and a source-bound `local-review.json` under
`research/integration/chNN/`. `visual-review.json` records all physical pages,
render hashes, review mode and corrections. Local author review is explicitly
not independent review; all five records retain `accepted=false` and
`independent_review=false`.

## Substantive result

- **39 — runtime:** replaces detached mock adapters with the actual Chapter31
  native recurrence and Chapter35 layered Hermon cache over the Chapter23
  learned-absolute-position Transformer. Typed whole-graph preflight precedes
  execution; exact artifact/capability routing, opaque instance/owner-bound
  handles, policy-before-tool effects and finally cleanup are tested. A
  hash-linked trace distinguishes intent, completion and uncertain completion
  after an effect. Scalar recurrence expansion and the full causal Transformer
  are separate continuation oracles. DOGMA remains non-Transformer;
  Chapter31 remains its restricted diagonal teaching model, not full DOGMA.
- **40 — memory:** separates transient native state, immutable event evidence,
  derived summaries, retrieval and issued context. Occurrence identities
  prevent text reinsertion from reviving a tombstoned source. A transitive
  provenance DAG controls expiry/deletion/tenant visibility even through a
  stale candidate index. Rehydration has independent record and UTF-8 payload
  byte bounds; context promotion adds no tool authority. Summary collisions
  and an issued-context revocation counterexample make loss/limits explicit.
- **41 — compiler:** implements a versioned typed straight-line IR, exact
  integer folding and effect-preserving DCE, sequential interpretation,
  actual Chapter39/40 handlers, conservative lowered effect dependencies and
  allocation-before-release liveness. It corrects the supplied classification
  of engine/retrieval as pure. Independent recursive evaluation, randomized
  integer DAGs, handler state/effect comparisons and malformed-program controls
  establish the stated narrow contract. This is not an MLIR/TVM implementation
  or a device compiler.
- **42 — database comparison:** retains Volcano/Cascades/operator/buffer/index/
  transaction/recovery lessons with explicit transfer limits. Hard semantic
  and resource gates precede illustrative weighted cost. A committed-redo-only
  WAL binds page writes to exact durable records and monotone page LSNs.
  Independent last-assignment replay checks seven crash cuts and randomized
  multikey schedules. Wrong values, wrong scalar types, nonexistent flushes
  and stale writes are rejected. This is not full ARIES or real storage I/O.
- **43 — governance:** separates immutable content lineage from mutable stage
  and immutable evaluation evidence. Conjunctive finite gates, distinct caller
  roles, bounded canary observations, revision guards, state-compatibility
  checks and rollback eligibility protect a serialized serving pointer.
  Rejected or never-served candidates cannot become rollback targets.
  The EWC comparison uses a separately derived quadratic example; a 20-trial
  zero-error canary is shown to provide weak statistical assurance. No learned
  adaptation result or authenticated deployment is inferred.

## Package adoption and source evidence

All five archive SHA-256 digests agree with the existing package audit.
All **180 manifest member hashes** (36 per archive) were checked against the
exact ZIP bytes. Complete incoming manuscripts, reference sources, tests,
storyboards, figure TEX/TXT and source ledgers were read and preserved as
text-only provenance. Packaged caches/PYC, stale computed results and QA or
acceptance labels were not used as validation.

The adoption maps account for every incoming manuscript section: Chapter39=22,
40=18, 41=22, 42=16, 43=18; **96 sections total**. Each has its original block
hash, disposition, destination and concrete reason. Introductions, original
figure questions and executable contract corrections are also documented.
No reuse percentage is asserted.

- research/integration/ch39/package-adoption.md
- research/integration/ch40/package-adoption.md
- research/integration/ch41/package-adoption.md
- research/integration/ch42/package-adoption.md
- research/integration/ch43/package-adoption.md

Primary access depth is recorded claim by claim in `source-verification.json`
and `sources.tex`: actual prior code for39; primary abstracts only for
MemGPT/Self-RAG; official MLIR language/effect documentation and the primary
TVM abstract; primary Volcano/Cascades text; and primary EWC HTML method
equations/context. ARIES access was narrower: publisher metadata/abstract
and an indexed primary excerpt on log forcing/LSNs; full-PDF attempts timed
out. No full-paper ARIES inspection or experimental reproduction is claimed.
All local continuity hashes were refreshed on18 October after authoring.

## Reproduction and review scope

The final chapter-specific runs used Python3.13.6, PyTorch2.10.0 and
pytest9.0.2, with reports stored per chapter:

```sh
for ch in 39 40 41 42 43; do
  /Users/wenyan/.pyenv/versions/3.13.6/bin/python3 -m pytest \
    tests/test_ch${ch}_reference.py \
    --junitxml=build/ch${ch}/reference-tests.xml || exit
done
```

The earlier combined run also passed189 tests in6.37s, recorded at
`build/ch39/batch-B-reference.xml`. The final per-chapter counts above come
from the separate JUnit reports. This is not a whole-repository regression.

All five builders completed strict compilation and generated-artifact checks:

```sh
python drafts/chNN/build.py --render
python drafts/chNN/build.py --check
```

The actual interpreter is the explicit Python path above; the system/bundled
Python lacks the required torch installation. Tools also require Pillow,
XeLaTeX/latexmk/makeindex and Poppler. One incremental rebuild initially failed
on a stale generated auxiliary-file line-number command; removing the owned
`.aux`/latexmk database and regenerating succeeded. This failure is not counted
as a passing build. No source was discarded to bypass the compiler.

Strict final logs have no overfull boxes, missing glyphs, unresolved references/
citations or multiply-defined labels. All60 physical pages were inspected in
color and grayscale. Corrections included short proof/function pagination,
consolidated source/reference pages, a liveness-bar endpoint, separated
lineage/serving labels and duplicate index capitalization. After final
index-only cleanup, raster comparison showed only physical pages39:12,
40:12, 41:13 and43:12 changed; those pages were reinspected in both modes.
Short standalone closing vocabulary pages retain intentional whitespace.
Cumulative layout must be checked again. The PDF skill marker was run
successfully once for five PDF outputs.

## Final PDF SHA-256 closure

| Chapter | SHA-256 |
|---|---|
| 39 | 25b56c535a076f19ef6c5c19039494ac4db0ac8cf0038475529bacac42c49779 |
| 40 | 4e9b076a9eff57c8d82f38fadddb9f0331ccbed631359f46946aa87c4c78c3f7 |
| 41 | 1ffeb6f2ffc9b7b7e7cb602b8b701657c85cf53418cc274cab878bda9397fb3f |
| 42 | 8dc7f160fd88add593c2d2f4f24c6ecb1c06c144dbc5319640933021785d8f15 |
| 43 | d9ecfcbc156bd939cdc888660853b1488bc88755f2caacb635714d9832c15876 |

Each `local-review.json` binds the PDF/page count, complete chapter sources,
test source/report, research evidence and actual transitive executable
dependencies. Chapter39 depends on Chapters31/35/23; Chapter41 also depends
on completed owned Chapters39/40. Other assigned references have no external
chapter-code imports. These dependencies are narrower than editorial continuity.

The final read-only admission audit passed for39–43 with no mechanical blockers:
`python3 scripts/audit-production.py --start 39 --end 43 --json --require-ready`.
Its output is `build/ch39/admission-B.json`. A separate closure check matched
every recorded source/dependency/research/PDF/render/test-report/log hash and
verified all color/grayscale page inventories. Mechanical readiness leaves
the audit's manual review and cumulative integration obligations open.

## Integration obligations and stable-interface boundaries

The following are coordinator work after ownership returns. No passing result
is claimed for these cross-batch checks.

1. **35 →36 →39:** Chapter39 currently wraps contiguous Chapter35 KV. It does
   not import Chapter36 or claim physical paging support. BatchA's handoff is
   now available; inspect its real `PagedKV` contract before adding an adapter.
   Preserve all model layers and learned positions; account for its in-place
   consume convention. Compare suffix logits to the full Chapter23 model and
   test shared partial tails/COW, page generations, owner mismatch, eviction,
   capacity failure, cancellation and final release. Do not silently replace
   physical paging with a tuple demonstration.
2. **30–34 →39 →41:** the runtime is serialized and closes per-operation
   engine state in `finally`. It does not implement Chapter30 tickets,
   request clocks, cancellation/publication/acknowledgement fences or the full
   Chapter34 serving shell. Bind those actual stable interfaces and test
   cancellation before publication, held resources through acknowledgement,
   stale owner/version rejection and effect-trace prefixes under failure.
   A Boolean cancel flag or final numerical equality is insufficient.
3. **Compiler observation contract:** folding/DCE is justified for exact total
   integer arithmetic with declared ordered effects and stated resource
   premises. Re-run original/optimized programs against real stable handlers
   after integration, comparing requested outputs, observable effect order,
   native state/cleanup and failure boundaries. No arbitrary floating-kernel
   reassociation, concurrency or production memory-byte claim is supplied.
4. **40 →45/49:** tombstones prevent future authorized reads in the local
   trusted store; issued contexts remain readable by their holder. Integrate
   any actual leases/in-flight revocation, distributed tombstone propagation,
   durability and tenant policy separately. Retrieval provenance must not
   confer tool grants. The summary fixture proves neither physical erasure
   nor learned neural unlearning.
5. **43 →44–46:** roles, data labels and drain/reset flags are trusted assertions
   here. Integrate actual authentication/signatures, durable atomic revision
   updates, ownership/migration epochs and artifact packaging. Pin old requests
   to their artifact during promotion/rollback and test real drain/reset;
   never reuse an old model's native state or KV merely because shapes match.
   Fingerprints must cover actual model/tokenizer/dtype/mode/state schemas.
   A matching hash or checkpoint does not confer permission or freshness.
6. **Recovery/deployment limits:** Chapter42's dictionary crash model has no
   fsync, torn-page protection, uncommitted transaction undo or multipage
   atomicity. Chapter43's pointer change is not a durable concurrent CAS.
   An external tool effect is not rolled back by either mechanism. Do not
   inherit production durability/security claims from the exercises.
7. **Cumulative assembly:** inspect all five adoption maps and local reviews;
   revalidate dependencies, generated fixtures and test reports. Merge the
   authored LaTeX with scoped `evod39:` through `evod43:` labels/bibliography
   keys and consistent proof/listing/figure macros. Consolidate glossary/index,
   notation and sources, and inspect every new continuous-book page plus
   front/back matter. The standalone wrapper's pagination does not transfer.
8. **Final gates:** the integration owner runs the whole-repository regression,
   preservation checks and cumulative builder after sibling authoring settles,
   then updates shared navigation/convergence records and makes the scoped
   integration commit. Obtain independent specialist/reader review and explicit
   publication authorization through the existing gates. Standalone passes
   must not promote either acceptance flag.

This batch did not execute the full regression or cumulative build and did
not update the shared book inventory/navigation. The reference experiments
establish stated teaching contracts; they do not demonstrate full DOGMA,
genomic capability, AGI, hardware speedups or a production service.
