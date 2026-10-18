# Chapter 46: supplied package adoption

Archive: /Users/wenyan/Downloads/evolutor-ch46-r01.zip

Verified archive SHA-256: `bfeff1f21c1f9ccd43e7713a4839b29840c0c4e8b8b295604066a2e2ee84cd10`.
All 37 manifest-declared file hashes matched exact ZIP bytes.
Incoming manuscript file SHA-256: `0ef1f02c35e2a7e20291ad1f59ade0846e04963e046ca1c2967602fdfa5c58c9`.
Original bytes are preserved under incoming/; no packaged caches/PYC or QA flags
were executed/adopted. Source documents are content, not operational instructions.

Every incoming section is mapped below. “Expanded” retains its correct subject,
scenario or derivation and adds evidence/premises; it does not claim verbatim
reuse. There is no invented percentage. Entire headings were merged where that
supports a sustained argument instead of many one-paragraph sections.

| Incoming section | Disposition | New location in drafts/ch46/manuscript.tex | Concrete reuse/change |
|---|---|---|---|
| Control and data planes | expanded | evod46:control | Retain advertisements/control/data distinction; add freshness and revalidation. |
| Placement function | expanded | evod46:control | Retain hard feasible set before weighted estimates; define units and deterministic synthetic tie-breaking. |
| State ownership | expanded | evod46:owner | Retain sid/tenant/artifact/schema/owner/epoch; bind backend and distinguish fencing from model position. |
| Immutable versus mutable replication | merged | evod46:owner | Retain immutable replication versus mutable single owner and separate durable-memory consistency. |
| Migration protocol | expanded | evod46:migrate | Retain prepare/copy/verify/commit; add source freezing, destination reservations, abort, issued transfer identity and proof premises. |
| DOGMA placement | expanded | evod46:representations | Preserve compact-native hypothesis without universal benefit; use actual restricted Chapter31 continuation fixture. |
| Hermon placement | expanded | evod46:representations | Preserve ordered KV movement plus metadata; use actual Chapter35/23 learned-position layered fixture. |
| Prefill/decode disaggregation | expanded | evod46:pd | Retain DistServe lead, phase separation and communication tradeoff; inspect primary paper selected passages, no borrowed speedups. |
| Topology | merged | evod46:observe; evod46:pd | Retain GPU/host/rack/zone topology; distinguish byte model from measured path. |
| Routing versus placement | merged | evod46:control | Retain logical implementation versus physical worker distinction. |
| Admission | expanded | evod46:pd | Retain downstream capacity; implement paired all-or-none logical reservations and issued release tickets. |
| Failure model | expanded | evod46:failure | Retain crash/reset/loss/partition/stale-membership; enumerate protocol windows and trusted evidence. |
| Exactly-once warning | merged | evod46:failure | Retain duplicate external effect warning; no live tools or generic exactly-once guarantee. |
| Cancellation | expanded | evod46:failure | Retain authoritative epoch; terminal cancellation aborts staging and forbids resurrection. |
| Backpressure | merged | evod46:observe | Retain upstream pressure and bounded queues; no unimplemented distributed scheduler claim. |
| Distributed observability | expanded | evod46:observe | Retain placement provenance; add causal spans, local durations and clock-error boundary. |
| Consistency boundary | merged | evod46:owner; evod46:failure | Retain distinct durable-memory versus engine-state protocols; no consensus implementation claim. |
| Executable oracle | expanded | evod46:migrate; evod46:pd; evod46:failure | Reuse Worker/StateHandle/Cluster scenario; add hard destination compatibility, freeze, reservation accounting, abort/cancel, trusted replay digest. |
| Failure injection | expanded | evod46:tests | Retain fault plan; execute only local corruption/phase/capacity/failure controls and actual-model snapshot continuations. |
| Twelve worked exercises | expanded | Twelve worked exercises | Retain all twelve themes; add movement arithmetic and concrete fault-state rubric. |
| Bridge | retained | Terms and the measurement boundary | Keep measured versus estimated Chapter47 bridge without claiming industrial distribution complete. |

## Executable, figure and evidence adoption

### Reference

Worker/StateHandle/Cluster, cross-zone native migration, stale rejection and same-zone prefill/decode scenario retained conceptually. Compatibility, source freezing, destination reservation, abort/cancel, conservation and trusted replay evidence deepen the oracle. The old unverified arbitrary recovery and backend-blind destination checks are replaced.

### Figures/storyboard

01-control => placement predicate/prose; 02-owner => figures/01-owner.tex; 03-migrate => 02-migrate; 04-pd => 03-pd; 05-failure => 02-migrate plus failure-window analysis; 06-trace => distributed-observability discussion/event schema. All originals retained in incoming; arrows and state transitions redrawn natively.

### Tests/results

All original capacity/zone/migration/epoch/foreign/recovery/PD/log-order themes retained or strengthened. New tests inject corruption/failure/cancellation and verify accounting, plus actual Chapter31/35 snapshot suffix continuation. Trusted replay hash is not supplied by arbitrary received bytes.

## Exact original file hashes

| Incoming file | SHA-256 |
|---|---|
| CONTINUATION.md | `127bc1868bce4847639aa02c3a3d4676a65060171c01b80b3206b0896d924c25` |
| INTEGRATION.md | `3d9a19ee637c32c1014ac5475c7c2d327ff9d8a9d774a9d3ca140d1b30c65487` |
| PACKAGE_README.md | `6b003f77c713cbafe6f93e2cea234b5648f7762dbe0a0072be6011e5c1210880` |
| drafts/ch46/README.md | `0ceca2d2e80fdc20a79db7d2dffab2ec78f63d3597bbd4bea5d7b8bbafdda54c` |
| drafts/ch46/STORYBOARD.md | `e19650c41887374446d681ed7f2376aefb148636b612e895f2ab01042b7fda99` |
| drafts/ch46/build.py | `6c2993faae2fc89aa6414e98c1ecc65ce3d9b136dc11ef57b93d3abe6f06d618` |
| drafts/ch46/figures/01-control.tex | `2fd489ead439d7774c07b3ba43031c4ded85f71fc4dfa9bac7915f280910c9f5` |
| drafts/ch46/figures/01-control.txt | `fc78e7d7203f02fae8b84211f24501198d242e503f19da4c9a7c408317b753ce` |
| drafts/ch46/figures/02-owner.tex | `1aefd26a676ec5bbb6bdf3778a8a418f9a56d6c4a49385c2a0796afc2760351e` |
| drafts/ch46/figures/02-owner.txt | `64b2812c3689106aca1d8c73892dff8b5520492990b331118a4fdab81d96321e` |
| drafts/ch46/figures/03-migrate.tex | `8695c600657a895985928c4379f06cb84f84b63f13a66a397b1d9f283eff9f2e` |
| drafts/ch46/figures/03-migrate.txt | `bddd7f5a239861e849b92312238301b011507d6e8d6217ed67b120facfcd440c` |
| drafts/ch46/figures/04-pd.tex | `0a05df6f7eb6c567ebff90e1f372ef096720b23acbd7568a394c00b5475ca775` |
| drafts/ch46/figures/04-pd.txt | `648d0cf4bf4338291275c5035baa5975279f9c48dd1c94bb703768ccb3ead75f` |
| drafts/ch46/figures/05-failure.tex | `bcd67ff50abb150baee6010adf029e3f8d04248f8a179d79c23a2195fd6bbc56` |
| drafts/ch46/figures/05-failure.txt | `fdee2670cfc828d3b0a974841103367806c3619847328a6b839f164340fb5926` |
| drafts/ch46/figures/06-trace.tex | `5c0f6e1ab98f48ecc9924905177197b859bd78ff2fe754f398082f7978476b46` |
| drafts/ch46/figures/06-trace.txt | `97798e2cbf499eb17a63a40c99539ce76614a1ad46efd7cc80057290df73734e` |
| drafts/ch46/manuscript.tex | `0ef1f02c35e2a7e20291ad1f59ade0846e04963e046ca1c2967602fdfa5c58c9` |
| drafts/ch46/reference.py | `e258df1f881fefd72ba1348f92799faf432467cc71583ae43297d23cca810dee` |
| drafts/ch46/results.json | `7b9ae66bd081d2d3501b7c3d45107d1e14b4c73d02e1de8ae37dec671ce07a4b` |
| drafts/ch46/review.tex | `34853183991852b0b3ce83d67cdc38e8fca96864e4d1a988a1a2527143372e89` |
| drafts/ch46/sources.tex | `cf7e567469ddff7b1d3345689c3811d9026beea1d39be1037e4026a6087311fb` |
| research/notation.json | `45c000f9511a8bc6c5e41785712907775a2ca6dcd5e17182ea5557fa84f639ad` |
| research/source-ledger.json | `e8cbabd8a75d7784112465f01683fcfd07cc5c13586d6d86b05d085c6b14bf85` |
| tests/test_ch46_reference.py | `6fa0dfc9b28111ebdfc860bd40f08debbb4542743ac459bcc772f59070afa486` |
| checksums.sha256 | `5353d96740c49644c854037aa4e9016ccea2245f26d66c6552065b641ff87518` |

Packaged build/review wrappers were inspected as content, then replaced with
Chapter35's actual strict builder/wrapper pattern and correct chapter counter.
Incoming results are preserved as historical inputs; current results/tables and
literal whole-function listings are regenerated. Source-ledger URLs were
rechecked with access depth recorded in source-verification.json. Stale QA labels,
caches and embedded web-tool citation tokens are omitted from authored evidence.
