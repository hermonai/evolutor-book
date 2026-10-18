# Batch D handoff: Chapters 48–52

Completed standalone authoring and local author review on **18 October 2026**.
All five assigned chapters are ready for the coordinator's substantive review.
**accepted=false; independent_review=false; cumulative_integration=false.**
This handoff does not promote the whole book, the separate Evolutor software
repository, a scientific hypothesis or a production deployment.

## Delivered sources and evidence

Each chapter has authored LaTeX, an expanded executable reference, regenerated
results, a standalone builder/wrapper, a storyboard, three original editable
TikZ/TXT mechanism plates, a selective glossary/index, and twenty worked
exercises. The five standalone PDFs contain **63 physical pages** in total,
including their covers, contents, references and indexes. There are **15 plates**
and **100 worked exercises**. Page counts are not a measure of scientific
acceptance.

| Chapter | Subject | Source and instructions | Adoption and audit | Bound local review |
|---|---|---|---|---|
| 48 | Genomic sequence applications | [draft](../../../drafts/ch48/manuscript.tex), [README](../../../drafts/ch48/README.md) | [adoption](../ch48/package-adoption.md), [audit](../ch48/technical-audit.md) | [review](../ch48/local-review.json) |
| 49 | Streaming, language, code and persistent agents | [draft](../../../drafts/ch49/manuscript.tex), [README](../../../drafts/ch49/README.md) | [adoption](../ch49/package-adoption.md), [audit](../ch49/technical-audit.md) | [review](../ch49/local-review.json) |
| 50 | Continual learning and population adaptation | [draft](../../../drafts/ch50/manuscript.tex), [README](../../../drafts/ch50/README.md) | [adoption](../ch50/package-adoption.md), [audit](../ch50/technical-audit.md) | [review](../ch50/local-review.json) |
| 51 | AGI capability hypotheses and limits | [draft](../../../drafts/ch51/manuscript.tex), [README](../../../drafts/ch51/README.md) | [adoption](../ch51/package-adoption.md), [audit](../ch51/technical-audit.md) | [review](../ch51/local-review.json) |
| 52 | Failures, open problems and reproducible synthesis | [draft](../../../drafts/ch52/manuscript.tex), [README](../../../drafts/ch52/README.md) | [adoption](../ch52/package-adoption.md), [audit](../ch52/technical-audit.md) | [review](../ch52/local-review.json) |

Each research directory also contains source-verification.json,
hash-verification.json and incoming/ text-only provenance. Source access records
state abstract-only versus inspected sections; they do not inherit the ZIP's
review or acceptance claims. Local-review.json binds every owned source/test,
declared earlier reference dependency, audit record, test report, build log,
final PDF and reviewed raster/contact sheet to exact SHA-256 bytes.

The read-only production admission check for Chapters 48–52 passes with zero
mechanical blockers. Its first run identified two missing schema declarations
in each source-access record; the existing verified package digest and explicit
exclusion of inherited validation claims are now recorded under the expected
keys. This metadata correction changed no manuscript, numerical result or PDF.
Admission validates local evidence consistency, not the manual/scientific gates.

## Final standalone PDFs and tests

| Chapter | Physical pages | Assigned tests passed | Final PDF SHA-256 |
|---|---:|---:|---|
| 48 | 12 | 25 | `f69c1603c60acbe87af6f9437821ff63e684616179477baa4191d95aa3987c28` |
| 49 | 12 | 21 | `257fbefd5476426f3e3bbb76762a3ba980d8e9dcae93c96ea1288a22c9c05882` |
| 50 | 13 | 29 | `7454f0ed3845f819285f09f272a8bffdd1dea0d21789b5c2d6d6d3ed6e733161` |
| 51 | 12 | 23 | `e9edbbaa366e718bd123e7aeee5c780db0aebbb574747eb8ae966953c171d546` |
| 52 | 14 | 26 | `cef39bb77c1d5c8f18f92ba7dec40ed73361939680455c2bed4c42ef6279e4ba` |

The final PDFs are:

- [Chapter 48](../../../output/pdf/evolutor-ch48-review.pdf)
- [Chapter 49](../../../output/pdf/evolutor-ch49-review.pdf)
- [Chapter 50](../../../output/pdf/evolutor-ch50-review.pdf)
- [Chapter 51](../../../output/pdf/evolutor-ch51-review.pdf)
- [Chapter 52](../../../output/pdf/evolutor-ch52-review.pdf)

**124 assigned tests passed; zero failures, errors or skips.** Per-chapter JUnit
reports are build/chNN/tests.xml; the combined assigned-only report is
build/ch52/batch-D-tests.xml. The latest numerical fixture checks passed for
all five chapters. All five strict standalone repeat builds succeeded. Their
build-record.json files bind the complete source inventory and resulting PDF.

The build rejects overfull boxes, missing glyphs, unresolved references/citations
and duplicate labels. Every final physical page was inspected in color and
grayscale at 110 dpi via contact sheets, with individual-page inspection during
corrections. Figures were corrected for arrow/label collisions; short whole
function listings reserve page space. A local wrapper compatibility definition
accepts a legacy lineno auxiliary column marker on repeat compilation, avoiding
a clean-build-only success. No shared TeX or global builder was edited.

The cover authoring date remains 17 October; the final tests, repeat builds,
render review and this handoff were completed on 18 October.

## Supplied-package preservation

All **231 declared file hashes** across the five archives were checked against
exact ZIP bytes (48, 48, 43, 45 and 47 files respectively), with zero mismatches.
Archive digests match the coordinator's package-reuse-audit.json. Preserved
incoming text hashes also match their original manifest entries.

All **123 incoming manuscript sections** are mapped individually (18, 23, 21,
30 and 31), with dispositions, current headings and concrete reasons. Each
adoption map also accounts for all six incoming figure TeX/TXT pairs, exercises,
reference/test themes, source leads and wrappers. Correct ideas and worked
scenarios were retained and expanded; six generic plates per package became
three explanatory original plates per chapter plus sustained prose and tested
tables. No fabricated reuse percentage is asserted. Packaged PYC/caches,
compiled PDFs/PNGs, stale numerical results and acceptance flags were not adopted.

## Substantive corrections and strongest supported conclusions

- **48:** biological observation and assay contracts precede prediction. Split
  assignment closes declared overlap/homology links transitively; proof is
  limited to those declared relations. Reverse complement transforms alleles
  and coordinates. Masked N, undefined MCC, tie-group AP and whole-cluster
  bootstrap conventions are explicit. The actual Chapter 23 shared-RC path is
  exercised on an untrained model. No trained genomic or wet-lab result follows.
- **49:** immutable event payloads and configuration-bound prefixes support
  validated replay of a trusted serialized reducer. Intent reserves budget
  before dispatch; resumed pending effects require reconciliation. The proof is
  at-most-one local dispatch under that history, not external exactly-once
  execution. Count-bounded queues do not bound bytes or history. Real Chapter 31
  recurrent continuation and Chapter 35 multi-layer K/V continuation are
  checked, preserving the actual learned-absolute-position Chapter 23 model.
- **50:** the supplied quadratic is retained and solved in closed form. Assigned
  importance F=I is not an estimated Fisher or full EWC. Acquisition, peak
  forgetting, signed BWT and counterfactual FWT have explicit conventions.
  Anchoring improves retention at a stated new-task cost; clipped geometric
  quality is not classification accuracy. Replay and population search account
  for evaluation costs; an offspring is not automatically promoted.
- **51:** all fourteen capability themes become operational tests. Six editorial
  evidence levels require scoped supporting records; metadata does not prove
  authenticity, independence or scientific validity. A mixed-unit ratio is
  replaced by one-axis acquisition area. Finite-test underdetermination,
  Hoeffding premises and the exact zero-failure bound are derived. Official ARC
  pages inform evaluation design only; no benchmark score or AGI level is claimed.
- **52:** the synthesis distinguishes actual earlier/owned implementations,
  proposed experiments and sibling integration. The failure-aware ledger imports
  the owned Chapter 51 contract, rejects cross-claim failure links and preserves
  counterexamples after resolution. Uniform-target cross entropy is an expected
  bound, not a finite-sample floor. Actual Hermon causality has a changing suffix
  and later-output positive control. The eight-reference-file manifest is a
  stated subset, not a full environment/data closure.

Independent oracles and negative controls include exhaustive ACGTN strings
through length four; an independently sampled cluster-bootstrap oracle;
Fraction and finite-difference checks of adaptation; unstable-rate rejection;
failed/held-out/replication identity controls; an independent capsule serializer;
changed/missing/tampered files and unsafe-path/symlink controls; actual model
parity and causality probes. These establish their tested contracts under stated
premises, not production concurrency, security or universal capability.

## Explicit cross-batch obligations for the coordinator

These are **unrun integration checks**, not hidden passing examples. Batch D did
not import changing Chapters 36–47 or substitute toy backends for their APIs.

| Boundary | Work after sibling interfaces are stable |
|---|---|
| 39/40/45 → 49 | Bind the event/recovery contract to the real runtime and memory APIs. Preserve tenant/session/artifact/policy identity, source provenance, derived-summary authority and deletion invalidation. Exercise stale leases, ambiguous external effects, durable crash/restart and policy revocation. Distinguish adapter correctness from model task success. |
| 43 → 50 | Connect candidate lineage, structural edit compatibility, promotion eligibility, state invalidation and rollback to actual governance. Preserve failed/expensive candidate accounting. No chapter-local population score authorizes deployment. |
| 43/45 → 51 | Map real governance and isolation evidence into bounded capability claims without treating a valid digest, policy field or independence declaration as evidence of truth or intelligence. |
| 47 → 48–51 | Carry actual units, budget accounting and evidence class. Do not replace synthetic arithmetic with GPU measurements, trained held-out results or biological validation. |
| 48–51 → 52 | Reconcile synthesis claims with the final implementations and unresolved experiments. Extend the declared dependency/source capsule to the actual integrated closure. |
| All chapters → continuous book | Reconcile glossary, notation, scoped labels, bibliography, cross-references and navigation; build through Chapter 52, run the full regression without concurrent author builds, inspect cumulative color/grayscale pages and update coordinator-owned status. |

Chapter 48 has no missing local prior-model API; real genomic datasets,
task-trained controls and biological validation are open research work. Chapter
49's real tools, durable backend and concurrent/distributed protocols are absent
by declared design, not passing production integrations. Chapter 50's governance
adapter is deferred. Chapter 51's evidence contract is deliberately bounded.
Chapter 52 cannot accept unfinished sibling work by declaring a completed spine.

## Reproduction and next owner actions

Use /Users/wenyan/.pyenv/versions/3.13.6/bin/python3 (pytest, Pillow and torch
2.10.0); the host /usr/bin/python3 lacks dependencies for actual-model checks.
Host TeX is /Library/TeX/texbin and Poppler is /opt/homebrew/bin. The chapter
READMEs give exact per-chapter commands.

For an assigned-only numerical/test reproduction from the repository root:

```sh
/Users/wenyan/.pyenv/versions/3.13.6/bin/python3 -m pytest tests/test_ch48_reference.py tests/test_ch49_reference.py tests/test_ch50_reference.py tests/test_ch51_reference.py tests/test_ch52_reference.py -q -o addopts=''
```

For each NN in 48 through 52, run its drafts/chNN/build.py --check to validate
derived assets, or --render to reproduce the strict standalone PDF and color/
grayscale raster set. A rebuilt PDF or edited source requires a fresh matching
local review; this handoff's hashes identify the exact reviewed bytes above.

The coordinator should read the five complete adoption/audit records, reproduce
local tests and fixtures, resolve the listed interfaces against actual stable
sources, then perform global convergence under BATCH_PRODUCTION.md. Independent
scientific/specialist and reader review, rights/access checks and explicit
publication authorization remain separate gates.

No shared navigation/status, global scripts/TeX, earlier chapters, other book or
finance repository, running service or remote system was changed by Batch D.
No cumulative builder or whole-repository regression was run. No staging,
commit, push, reset or clean was performed. This file is the owned completion
handoff; production-batches.json and global convergence records remain the
coordinator's responsibility.

