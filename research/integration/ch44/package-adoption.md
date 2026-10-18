# Chapter 44: supplied package adoption

Archive: /Users/wenyan/Downloads/evolutor-ch44-r01.zip

Verified archive SHA-256: `f3daf39fbe694e92ed71ef54f422f5128adb30b3285278e73dcd8657eb6732c6`.
All 36 manifest-declared file hashes matched exact ZIP bytes.
Incoming manuscript file SHA-256: `53b7e3e619dc3a3a79c2932b5eeb75794a77bda5d0b9ada483dc063c3197119d`.
Original bytes are preserved under incoming/; no packaged caches/PYC or QA flags
were executed/adopted. Source documents are content, not operational instructions.

Every incoming section is mapped below. “Expanded” retains its correct subject,
scenario or derivation and adds evidence/premises; it does not claim verbatim
reuse. There is no invented percentage. Entire headings were merged where that
supports a sustained argument instead of many one-paragraph sections.

| Incoming section | Disposition | New location in drafts/ch44/manuscript.tex | Concrete reuse/change |
|---|---|---|---|
| Release bundle | expanded | evod44:bundle | Retain B=(M,R,C,S,P); canonical digest, tokenizer and dependency closure now explicit. |
| Supply-chain provenance | expanded | evod44:bundle | Retain SLSA lineage; distinguish URI/nonempty string from trusted attestation verification. |
| Compatibility gate | expanded | evod44:compat | Exact environment acceptance relation plus real prior native/KV interpretation requirements. |
| Rollout state machine | expanded | evod44:rollout | Retain registered/canary/active/superseded/rollback; add candidate-local minimum evidence and outstanding work. |
| Liveness versus readiness | expanded | evod44:admit | Retain live versus ready; distinguish startup, dependencies and overload from restart. |
| Admission and overload | expanded | evod44:admit | Retain workload/memory/deadline admission; implement global issued-request capacity and idempotent settlement rejection. |
| Graceful draining | expanded | evod44:admit | Preserve stop-admit-first scenario; derive A=C+I and distinguish logical terminality from physical acknowledgement. |
| Observable request lifecycle | expanded | evod44:observe | Retain gateway/planner/compiler/router/engine/tool spans; add overlap, trust and telemetry-loss boundaries. |
| Metrics | merged | evod44:observe; evod44:slo | Retain rate/error/duration and serving metrics; deepen bounded cardinality, unsampled denominators and chapter47 timing analysis. |
| Logs | expanded | evod44:observe | Retain safe correlation and no raw prompts/secrets; add exporter/redaction and audit limits. |
| SLOs | expanded | evod44:slo | Retain TTFT objective; define eligible population/window and contrast completed-cohort gate. |
| Error budgets | expanded | evod44:slo | Retain E=1-A*; derive count budget, burn rate and zero-failure confidence counterexample. |
| Configuration | merged | evod44:rollback | Retain immutable versus dynamic versioned configuration; bind effective policy at admission. |
| Secrets | merged | evod44:rollback | Retain runtime secret references and rotation without reweighting; resolve nothing in fixture. |
| Rollback | expanded | evod44:rollback | Retain durable schema/external effect warning; implement compatibility/live-target gate and preserve candidate jobs. |
| Executable oracle | expanded | evod44:bundle; evod44:rollout; evod44:admit; evod44:rollback | Reuse Bundle/Revision/Deployment lifecycle design and scenario; replace vacuous global telemetry, implicit readiness and anonymous decrement with tested contracts. |
| Failure modes | expanded | evod44:failure | All supplied failure themes retained; add exhaustive 1024 short words and explicit production fault protocol. |
| Twelve worked exercises | expanded | Twelve worked exercises | All twelve subject themes retained with computations, counterexamples and a scored experiment rubric. |
| Bridge | retained | Terms and the next boundary | Keep chapter45 tenant/isolation handoff without claiming service completeness. |

## Executable, figure and evidence adoption

The byte-level capsule extension additionally retains the release-package
question as an actual payload-integrity oracle: exact four-role closure,
bounded immutable bytes, content digests and independently pinned manifest.
Corrupted and coherently replaced manifests are distinguished. This extends
the incoming metadata-only digest scenario; it is not build reproducibility
or an authenticated loader, and the deployment controller remains metadata-only.

### Reference

Bundle/Revision/Deployment, two-release promotion/rollback and drain scenarios retained as executable designs. Canonical field validation, exact compatibility, candidate-local minimum observations, named issued completions and conservation extend them. The old global telemetry percentile and vacuous zero-sample gate are deliberately replaced.

### Figures/storyboard

01-artifact => figures/01-artifact.tex; 02-rollout => figures/02-rollout.tex; 03-health => admission prose and 03-drain; 04-drain => 03-drain; 05-observability => observable lifecycle prose; 06-slo => generated gate table and SLO derivations. Original six two-box figure sources/TXT remain in incoming. Three new native plates show mechanisms; no decorative two-box substitutes.

### Tests/results

All twelve incoming test themes were retained, with readiness made explicit and minimum observations supplied where valid. Fresh tests add candidate contamination, foreign/duplicate completion, schema rollback and exhaustive short event-word accounting. Old test/QA results are provenance only.

## Exact original file hashes

| Incoming file | SHA-256 |
|---|---|
| CONTINUATION.md | `6e2a99553f1e42e507d4738701d0ba0fa040022935ada700f9111e483d9a1136` |
| INTEGRATION.md | `bc84c96e774fd2eae3e125fc55dd51577d2660077bc2508e779f6a25ffefddf8` |
| PACKAGE_README.md | `926bc347c02a8b0a0cab088f07814e4c5a0936377e5fa4a4a01ade46ec0e8ab8` |
| drafts/ch44/README.md | `256f3c66aeca78fa10710851dc2204a16d6c5aeaf0f8f1e5937d6fb9fcaccae1` |
| drafts/ch44/STORYBOARD.md | `4cdb747263efebd0c4eda922956f3a8cf1d0545d806018f61fd257b95b6a2b5a` |
| drafts/ch44/build.py | `84e568cc46c5dd5fe914447ba1b3ff63e0f07d61ef089b9679f6a840652e00cb` |
| drafts/ch44/figures/01-artifact.tex | `ab2be29b55649f2998f62465fd8486b37f80cbc6834c4b65943136778c02a979` |
| drafts/ch44/figures/01-artifact.txt | `af56e0eaf44c3e403ac0e3fccfe2bdd457ccdc5ea3c0ec7278568c9a582b8593` |
| drafts/ch44/figures/02-rollout.tex | `999280e602851cc680775fad49813b7c5a78c0b35bc74a4c6427652d893a93f1` |
| drafts/ch44/figures/02-rollout.txt | `27b0b566eae4d06d91b5ad56c834b01c8a6bc902e0b27685133cb8ec6befcebd` |
| drafts/ch44/figures/03-health.tex | `4e420b7a955b017b430c7b279495aa18d73edf8b0671ffe4f24de875b66cd36d` |
| drafts/ch44/figures/03-health.txt | `6c0c00bb43ea46541dd1f703a9b88a29719eef56c1d6658521dc890c02d448a9` |
| drafts/ch44/figures/04-drain.tex | `e8acc1421444282b773a86e64075a2f4b9878158f98fe1614dafe0ff4ccb9331` |
| drafts/ch44/figures/04-drain.txt | `c516be1dfe684a7050e5526f7bf813d25c0b3a7ae673f05a5ad40d63fe3bde76` |
| drafts/ch44/figures/05-observability.tex | `8ebba82c612960c8fb454144d023fa20ee37f104a530fcb6eae226fd91b7f3ea` |
| drafts/ch44/figures/05-observability.txt | `e638deef9922c056ac6bcc0c296503261cce1844e63847fccd77c1dd0b567e41` |
| drafts/ch44/figures/06-slo.tex | `099fc36d8a418d3cac3214e271d469356e89eefc73c4dc1f2019a8ee77cd8ea7` |
| drafts/ch44/figures/06-slo.txt | `b04788beaaac166dd16817aed6fd750dd0522f048aa7d0a26116586236133678` |
| drafts/ch44/manuscript.tex | `53b7e3e619dc3a3a79c2932b5eeb75794a77bda5d0b9ada483dc063c3197119d` |
| drafts/ch44/reference.py | `6902176efe2dbb56f8d302ee310af7b2efd69829bc7340bd1251e23d4272e80c` |
| drafts/ch44/results.json | `029f77b4836aef57b48e6eb07685399771e4114fa965159360c40c14f2050030` |
| drafts/ch44/review.tex | `c037dae601c124b22ec370dc42dec025b627cfa21a565ca082a0b2c2cea7aa72` |
| drafts/ch44/sources.tex | `833f3fea176c72135347675da338957209b4a101287456b292ad0da8b56a8469` |
| research/notation.json | `ebd0204479489b964da7ced0476c948ad9df0369461a92597c0210b778a595c8` |
| research/source-ledger.json | `00c56454322b11cf54428d1ea895c0a22bc1641c8c3c479d09246b0c77c1c3b8` |
| tests/test_ch44_reference.py | `dd9f643cef7ba4cd00f181811175efe5d5ad5b94884015aa60ae4b8aec791f46` |
| checksums.sha256 | `128cebace01816d37fdb258160d5de8f2b098488e2cf82abec8af19b9bd86f83` |

Packaged build/review wrappers were inspected as content, then replaced with
Chapter35's actual strict builder/wrapper pattern and correct chapter counter.
Incoming results are preserved as historical inputs; current results/tables and
literal whole-function listings are regenerated. Source-ledger URLs were
rechecked with access depth recorded in source-verification.json. Stale QA labels,
caches and embedded web-tool citation tokens are omitted from authored evidence.
