# Complete manuscript integration report

18 October 2026. Book: **Evolutor: Genomic computation: models, state and systems**.
Starting coordinator revision: 32f71e6 on integration/evolutor-ch22-52.
The four authoring chats had finished and returned ownership before integration.

## Delivered scope

All 52 chapters now have authored sources in one 619-page continuous candidate,
organized into twelve printed parts. All supplied Chapters 22–52 are accounted for in
the inventory; the remaining seventeen chapters were not silently omitted.
The complete readable artifact is
[the review PDF](artifacts/review/evolutor-complete-review.pdf), with its
byte identity in [the artifact manifest](artifacts/review/manifest.json).

The main README, current guide, chapter map, inventory/convergence matrix,
editorial architecture, roadmap, contribution instructions and publication
policy distinguish manuscript completion from scientific/publication acceptance.
[The documentation map](docs/README.md) identifies active and historical material.
[The Claude prompt](docs/CLAUDE_PREPUBLICATION_REVIEW_PROMPT.md) authorizes a fresh
local review and justified adjustments, not automatic publication or remote pushes.

## Chapter/package checks

- All four handoffs were inspected. New chapter suites declare 567 tests across
  Chapters 36–52; these are included in the coordinator's complete regression,
  not added to its total a second time.
- The 17 new adoption maps were inspected for incoming subject coverage,
  corrections, figure consolidation and retained limitations. All supplied
  archives remain identified by their original audit digests.
- The initial integrity pass checked 843 declared local evidence, transitive
  dependency and raster/contact-sheet hashes with no mismatch. Chapters 36–38
  lacked two shared admission keys; existing package-integrity digests and
  explicit exclusions of inherited QA claims were added without manuscript/PDF
  changes. Their changed research-record hashes were refreshed explicitly.
- All 49 standalone builders for Chapters 4–52 reproduced their result files,
  generated tables and literal source-function listings using --check.
  This is fixture reproduction, not replication of cited external experiments.

## Substantive integration and corrections

[The paged-runtime companion](examples/integrated_spine/README.md) connects the
actual Chapter 36 all-layer pool to Chapter 39 opaque handles and Chapter 41
lowering/effect handlers. Sixteen new tests check actual full-model continuation,
every assigned split, shared-tail isolation, prefix eviction, owner/instance/
stale-handle rejection, invalid input, allocation failure, trace failure and
final cleanup. Original versus optimized compiler observations include the
unused engine effect, not just the requested integer answer.

The adapter retains the actual Chapter 23/35 learned-position Transformer.
Its model is immutable during live requests and its calls are serialized;
the allocator still stages contiguous tensors. It is not a GPU kernel,
asynchronous serving shell, authenticated tenant service or task benchmark.
Chapter 37 and 38 token clocks are explicitly not silently joined.

Chapters 41/49/51/52 were edited to remove stale references to changing or
unfinished authoring batches and to describe the actual bounded companion.
Chapter 52's review-gate illustration is now a timeless evidence contract,
not an outdated batch-status display. Their standalone PDFs were rebuilt;
changed pages were inspected in color and grayscale, with unchanged raster
hashes retaining the prior author's local scope. Superseded author review
records are preserved beside the coordinator amendments. No model/reference
arithmetic or theorem was changed by those editorial corrections.

## Whole-book production

The cumulative builder now prints the same twelve parts as chapter-structure.json
and binds that input in its source closure. The global glossary covers the new
memory, paging, scheduling, governance and evidence terminology. Bibliography
consolidation remains exact-identifier based, not fuzzy matching of papers.

Strict compilation exposed a legacy incremental lineno marker and caption-local
label resets. The preamble consumes the one-column bookkeeping marker and names
figure labels explicitly before writing them. Legacy TikZ loops named \label
are alpha-renamed only in derived copies; ambiguous mixed uses fail rather than
corrupt a real cross-reference. Historical chapter artwork remains byte-identical.
A cumulative-only Chapter 37 spacing adjustment keeps a definition's final word
from being stranded above its display. These transformations have regression tests.

The complete candidate is compiled from LaTeX, not concatenated older PDFs.
The strict gate checks overfull boxes, missing glyphs, unresolved citations/
references and duplicate labels. The new renderer batches consecutive page
ranges in one Poppler call; selection tests verify exact coverage.

## Verification and preservation

Exact final counts, commands, versions, source hashes, PDF hashes, physical-page
ranges and review scope are recorded in
[continuous-through52-review.json](research/integration/continuous-through52-review.json).
The initial complete regression passed 2,047 tests before new integration checks.
An intermediate run found preservation failures after convenience targets were
added to the hash-frozen Makefile, a stale roadmap overlay and a missing report
link. Those failures are not counted as passes: the original Makefile was
restored, targets moved to complete-book.mk, and only the unfrozen current
roadmap overlay was advanced. No acceptance digest or preservation assertion was
weakened. The final regression passed 2,078 tests with no failures or skips,
without concurrent PDF builds. Chapter-structure validation, local production
admission declarations and the changed-tooling lint pass also succeed.

Original accepted opening sources, reviewed build machinery, book/book.json,
BOOK_PLAN.md and historical accepted PDFs remain preserved. Earlier throughNN
review records keep their historical source scope; they are not rewritten to
certify the new book. Invalid generated auxiliary files were moved to an exact
local recovery directory under tmp/, not broadly deleted.

## What remains before an accepted publication

This coordinator pass is not a new full scientific peer review or an intended
reader study. Cumulative visual scope is explicit in the source-bound record;
rendering every page is not the same as inspecting every page or proving
accessibility. The Claude prompt requires a fresh all-chapter and whole-volume
editorial review, followed by appropriate external specialist/reader review.

Rights/source access, a reuse-license decision, final copyediting, accessible
document structure and explicit human release acceptance remain open. The PDF
is not claimed tagged or PDF/UA compliant. No new license, author identity,
accepted-edition flag, Git tag or public release is created by this integration.
All reported font resources are embedded, but earlier imported figure PDFs
retain Type 3 resources; inspect/rework those vectors as needed for publisher
requirements rather than assuming the complete candidate has native text in
every inherited illustration.

Production joins remain research/engineering work where declared: asynchronous
cancellation and acknowledgements, tentative speculative workspace, durable
agent/memory adapters, authenticated authority, distributed fencing and device
kernels. Real backend measurements, task-trained held-out genomic evaluations,
biological findings and AGI are not established here. These limits are preserved
rather than filled with detached demos or invented successful experiments.

The user's request authorizes the GitHub push of this review work. The integration
branch is the delivery branch; the default main branch and release history are
not silently merged, retagged or promoted to publication acceptance.
