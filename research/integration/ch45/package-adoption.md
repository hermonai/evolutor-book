# Chapter 45: supplied package adoption

Archive: /Users/wenyan/Downloads/evolutor-ch45-r01.zip

Verified archive SHA-256: `551b48a43de6aabcc2335d15827da00d26b8d15c371b4fcadb2645f46eb26510`.
All 37 manifest-declared file hashes matched exact ZIP bytes.
Incoming manuscript file SHA-256: `ebae7c66c454b537fc2d2c60d8005897419f4037681f17fafc9739770e693e23`.
Original bytes are preserved under incoming/; no packaged caches/PYC or QA flags
were executed/adopted. Source documents are content, not operational instructions.

Every incoming section is mapped below. “Expanded” retains its correct subject,
scenario or derivation and adds evidence/premises; it does not claim verbatim
reuse. There is no invented percentage. Entire headings were merged where that
supports a sustained argument instead of many one-paragraph sections.

| Incoming section | Disposition | New location in drafts/ch45/manuscript.tex | Concrete reuse/change |
|---|---|---|---|
| Threat model | expanded | evod45:threat | Retain malicious tenant/content/handles/exhaustion; specify trusted host and excluded adversaries. |
| Identity | expanded | evod45:identity | Preserve authenticated principal, extend session binding and distinguish baggage from authority. |
| Deny by default | merged | evod45:identity | Retain explicit grant predicate and planner-proposes/runtime-authorizes split. |
| Capabilities | expanded | evod45:capability | Retain scoped capability; add issuance registry, policy epoch, expiry and conservative revocation; explicitly no cryptographic auth. |
| Resource namespaces | expanded | evod45:namespace | All state/cache/checkpoint/memory/tool/audit scopes retained with real prior-engine cautions. |
| Cache isolation | expanded | evod45:namespace | Retain tenant/artifact/policy/prefix key; replace ambiguous delimiter string with structured encoding and envelope caveat. |
| Quota isolation | expanded | evod45:quota | Retain noisy-neighbor bounds; add componentwise tenant/global vector conservation and partial-acquisition negative control. |
| Prompt injection | expanded | evod45:tools | Retain malicious retrieval scenario and least privilege; labeled data does not prove attack recognition. |
| Tool security | expanded | evod45:tools | Retain outside-model executor; implement closed echo target/argument schema and no real tools. |
| System prompts are not a security boundary | merged | evod45:tools | Retain deterministic boundary; system prompts guide behavior without granting permissions. |
| Memory isolation | expanded | evod45:engines | Retain filter-before-ranking, tombstone and summary scope; mark chapter40 integration dependency. |
| Engine-state isolation | expanded | evod45:namespace; evod45:engines | Retain foreign-generation rejection and scrub-after-pins; distinguish logical removal from secure hardware erase. |
| Compiler and IR security | expanded | evod45:engines | Retain security preconditions for CSE/prefix/materialization; defer integration against chapter41 final effects. |
| Batching | expanded | evod45:engines | Retain independent masks/pages/outputs/cancel/accounting and add noninterference premises. |
| Side channels | expanded | evod45:engines; evod45:namespace | Retain explicit side-channel exclusion; prove only logical values and give global-quota availability counterexample. |
| Secrets | merged | evod45:tools; evod45:audit | Retain secret-free prompts/artifacts and post-authorization scoped resolution. |
| Audit | expanded | evod45:audit | Retain redacted decisions; distinguish authorization outcome, operation outcome and immutable storage. |
| Zero-trust comparison | merged | evod45:threat | Retain NIST no implicit network trust; narrow source-access claim to overview. |
| Executable oracle | expanded | evod45:capability; evod45:quota; evod45:tools | Reuse Principal/Capability/Policy/SecureStore designs and same-x/malicious-text scenarios; repair nonce/issuance and add time/quota/schema contracts. |
| Adversarial test matrix | expanded | evod45:tests | Retain all original attack classes; distinguish executed local cases from deferred concurrent/engine/hardware tests. |
| Failure modes | merged | evod45:tests; evod45:threat | All supplied failure themes become premises, negative controls or explicitly unimplemented production tests. |
| Twelve worked exercises | expanded | Twelve worked exercises | Retain authority/key/GPU/handle/CSE/prompt/audit/side-channel/rubric themes; add expiry and vector arithmetic. |
| Bridge | retained | Terms and the distribution boundary | Preserve logical-identity/authority placement constraint and chapter46 bridge. |

## Executable, figure and evidence adoption

### Reference

Principal/Capability/Policy/SecureStore, same object x in different tenants and malicious untrusted tool text retained. Issued-object registry replaces unchecked deterministic nonce; expiry/session/epoch revocation, structured cache encoding, closed arguments and vector reservation are added. No claim of cryptographic authentication survives.

### Figures/storyboard

01-identity + 02-policy + 05-untrusted => figures/01-authority.tex; 03-isolation => 02-namespace; 04-quota => 03-quota; 06-audit => literal authorize listing and audit discussion. All six original sources/TXT retained in incoming; three native plates distinguish data, authority, namespaces and feasible resource bounds.

### Tests/results

Original default-deny/own-read/foreign/subject/resource/quota/prompt/audit scenarios remain. Deterministic nonce equality is relocated to provenance and replaced by issuance, expiry and revocation negative controls. No hosted security test is inferred.

## Exact original file hashes

| Incoming file | SHA-256 |
|---|---|
| CONTINUATION.md | `017a88a6fe93a6b1aa2cb914dc40557a0ab4bd298b430b8abd78d34ef7b4aa3e` |
| INTEGRATION.md | `8a937aef4adc859d064380fd98272ed4eb5a66c57825449fc23eefde598212cd` |
| PACKAGE_README.md | `5c7e74aa2ff524d7809de1bb82238bbf21f8ec51a3af35fea056002344ce617f` |
| drafts/ch45/README.md | `4ad34835828448218e4004c00b0eb4df6abd60d88eca3a70ea44d59aefa5fa19` |
| drafts/ch45/STORYBOARD.md | `993399682d00ceb2597023e0e893ef92383b6c90d669f485ed808eb06cea0875` |
| drafts/ch45/build.py | `7e3d1dd2c5ed6724e74bf8badd75143aa99bc7255cd0613d29779fffdfc567da` |
| drafts/ch45/figures/01-identity.tex | `6a19347665d9142b4ff88e64aa30bca726783c1553ae4979b6d66e05eba8b120` |
| drafts/ch45/figures/01-identity.txt | `10c42ead97a0591a0da7a02139fb17e87c92b122b482d9e48f224d293008d7e5` |
| drafts/ch45/figures/02-policy.tex | `68a926ed9045e7ed410234590ad6183e325f5e0940a2f69d2a9d0b0dd462960a` |
| drafts/ch45/figures/02-policy.txt | `b9415ebe38e7afb7c3ccfc2efcad090c48a01373d760c2960c60dab2341a6590` |
| drafts/ch45/figures/03-isolation.tex | `2d6f3d653697ffd4f22b0c2f7a636e35c6f510554ad30e21a92a55b31ee9e7ae` |
| drafts/ch45/figures/03-isolation.txt | `5cc46728e9f6ce5cdf22a92ed9d28e01ac581b4b1422167311d2e85643f81fa3` |
| drafts/ch45/figures/04-quota.tex | `ed6fcf16899458268895216b4a573f36871c45d2b5887fc647cecda2fb62f337` |
| drafts/ch45/figures/04-quota.txt | `ee5ff7fd832a8b1b26ed71a9f0f955fc4d42054851ec934d10cc12361677ecb1` |
| drafts/ch45/figures/05-untrusted.tex | `0054bd7c6bcfa2ec87f2e9ea5115563f5876d05ab23b19b57be94ad211b61071` |
| drafts/ch45/figures/05-untrusted.txt | `540326150788a4d65a591857f3ceecc1702c30aaef10848f731ea4034f03ce65` |
| drafts/ch45/figures/06-audit.tex | `a9891a3b243cad6a52572ef7dfcb4f454221a056d5a08744be6587f49ac0c511` |
| drafts/ch45/figures/06-audit.txt | `2afe631bacfa607ec747b688dcb9f747c1ea8d9456a0ca5c327d06e9feb8287c` |
| drafts/ch45/manuscript.tex | `ebae7c66c454b537fc2d2c60d8005897419f4037681f17fafc9739770e693e23` |
| drafts/ch45/reference.py | `983c6e2346894d52dc650dac6d7d58c676aea019a82d9b9781e7f7039945b78f` |
| drafts/ch45/results.json | `dfc97669789bc7abd57ecf8a8526ec7639000bad6225dd905c2f018e237f0b48` |
| drafts/ch45/review.tex | `0d27a0f4f39187e5abda53d89c2678474b4bfc00d99806830833bdbf6bc75c3a` |
| drafts/ch45/sources.tex | `3c3896288d52a2ee25252e0f0beeb2fee8ac79cdd4f201ddc73e46049d77c209` |
| research/notation.json | `363bf8dc07caaf5bb6f806220f7f5033acacaf596f73eb32dced364bb89af540` |
| research/source-ledger.json | `ecfb4d044007ca23103b6c75b8a0ebb5c1373960097b70116ccd13fe158d6bfa` |
| tests/test_ch45_reference.py | `2abe7f8710513f01ac8ba8af2c43e8fc8e6c5f0d2c5ea322abc72ff8bced56ec` |
| checksums.sha256 | `e4cbf5b25c532e35c5b3b36b119f4d4aab69c18401201e680b749fb0553a5256` |

Packaged build/review wrappers were inspected as content, then replaced with
Chapter35's actual strict builder/wrapper pattern and correct chapter counter.
Incoming results are preserved as historical inputs; current results/tables and
literal whole-function listings are regenerated. Source-ledger URLs were
rechecked with access depth recorded in source-verification.json. Stale QA labels,
caches and embedded web-tool citation tokens are omitted from authored evidence.
