# Chapter 49 package adoption

Archive: `/Users/wenyan/Downloads/evolutor-ch49-r01.zip`  
SHA-256: `3838d1578a123ccec48e55ca12ec8bb717fa1df1d36c6a844183fae77810ffa1`  
All 48 manifest hashes reverified against archive bytes on 17 October 2026; no mismatches.
Incoming manuscript: `incoming/drafts/ch49/manuscript.tex`, SHA-256 `1dc76abc3a69813932f2de5139bc6589d38b570c12634aa8fb445cb50d522dfc`.
Every incoming section below refers to that exact source. Destinations are headings in `drafts/ch49/manuscript.tex`, including named subsections. Conceptual retention, verbatim wording and executable reuse are different quantities; no reuse percentage is asserted.

| Incoming section | Disposition | Destination | Concrete change/reason |
|---|---|---|---|
| Events, not one giant prompt | expanded | Events, ordering and bounded pressure | Keeps ordered typed event stream; adds canonical immutable payloads and serialized ordering assumptions. |
| Backpressure | expanded | Events, ordering and bounded pressure | Keeps bounded queue; derives item conservation, rejection ownership and byte-budget limitation. |
| Four kinds of state | expanded | Four states that cannot substitute for one another | Keeps native/context/durable/external separation and MemGPT source; explicitly tests actual earlier engines without converting them. |
| Session identity | expanded | Identity binds replay to one contract | Preserves tenant/model/policy/session identity; binds configuration and migration assumptions. |
| Checkpoint and resume | expanded | Identity binds replay to one contract | Preserves prefix digest, replaces negative index with event count and states trusted-digest limitation. |
| Replay | expanded | Replay is reduction, not re-execution | Keeps pure/effect separation; adds reducer induction and model/sampler reproducibility boundary. |
| Idempotency | expanded | An action state machine for ambiguous crashes | Replaces volatile result dict with replayable intent/result maps; detects changed commands and unresolved outcomes. |
| Agent-computer interface | expanded | Language and code workloads need task evidence | Retains typed ACI and SWE-agent lead; distinguishes availability, authority and learned competence. |
| Language streams | merged | Language and code workloads need task evidence | Keeps bounded summaries, original evidence and correction/deletion tests. |
| Streaming generation | merged | Replay is reduction, not re-execution | Retains irreversible emitted-token boundary; separates audit replay from model regeneration. |
| Code agents | expanded | Language and code workloads need task evidence | Keeps versioned repository/environment/test loop and adds base-change conflict plate. |
| Sandboxing | merged | Language and code workloads need task evidence | Keeps host-enforced filesystem/network/process/credential permissions; no sandbox certification. |
| Persistent memory | merged | Four states that cannot substitute for one another; Language and code workloads need task evidence | Retains provenance, retention and retrieval-not-authority rules; declares Chapter40 adapter deferred. |
| Long-horizon planning | expanded | Plans, leases, humans and observability | Keeps versioned hypotheses, preconditions and replanning; requires stale external-state checks. |
| Leases and budgets | expanded | Plans, leases, humans and observability; An action state machine for ambiguous crashes | Preserves lifetime/budget semantics; adds reserve-before-dispatch and trusted caller clock limitations. |
| Human interaction | retained | Plans, leases, humans and observability | Keeps action/resource/version-scoped approval and assistance accounting without changing user authority. |
| Crash recovery | expanded | An action state machine for ambiguous crashes; Replay is reduction, not re-execution | Retains reconciliation; adds absence/intent/completion state machine and dispatch theorem with explicit external limit. |
| Concurrency | merged | Plans, leases, humans and observability | Keeps immutable shared reads and explicit write conflicts; serial oracle is not concurrent implementation. |
| Observability | retained | Plans, leases, humans and observability | Keeps session/plan/engine/tool traces, queue/retry/budget measures and privacy limits. |
| Executable oracle | expanded | An action state machine for ambiguous crashes; Replay is reduction, not re-execution | Reuses session, checkpoint, FIFO and idempotency intents with replay reconstruction and adversarial tests. |
| Failure modes | merged | Events, ordering and bounded pressure; An action state machine for ambiguous crashes; Plans, leases, humans and observability | All incoming failure themes appear at their mechanism boundaries instead of an isolated checklist. |
| Twelve worked exercises | expanded | Exercises and worked solutions | Retains twelve themes, expands to twenty worked problems including crash-window protocol and real-engine boundary. |
| Bridge | retained | Bridge | Preserves distinction between persistent evidence and learning in Chapter50. |

## Other incoming material

The complete reference, tests, storyboard, all six figure TeX/TXT pairs and source ledger were read as source material. Their text is preserved under `incoming/`, with original file hashes in `incoming/manifest.json`. Original QA status strings are provenance only. Caches, PYC, packaged PDFs and rendered PNGs were not adopted or executed.

The six one-step figure concepts are consolidated into three original native TikZ mechanism plates with semantic TXT. The supplied paragraph concepts are retained at their mapped discussion; the generic two-box artwork is replaced because it does not explain the changing objects. Source listings are whole functions extracted from the expanded tested reference. Incoming tests supply retained scenario themes; current tests add independent oracles and negative controls and update incompatible conventions described above. Original exercise themes are retained and deepened into twenty worked problems. Source leads were checked at the access depths recorded in source-verification.json; incoming access claims are not inherited.

Build/review wrappers clone Chapter35's Pagella/Heros authored-LaTeX pattern with chapter identity/counter corrected and short-listing space reservations added. The packaged builder, stale results and acceptance labels do not govern this chapter. All numerical fixtures are regenerated locally. External evidence is paraphrased selectively; no source prose or artwork is copied.

## Figure and executable adoption detail

Each incoming figure entry below covers both its `.tex` and `.txt` companion; their exact original digests are in the preserved manifest.

| Incoming figure pair | New location | Decision |
|---|---|---|
| 01-stream | 01-pressure | Uses actual queue occupancy and rejected arrival rather than restated flow. |
| 02-memory | Four states that cannot substitute for one another | Preserves all four types in prose and real-interface tests; no false unified-memory implementation. |
| 03-resume | 02-recovery + replay proof | Makes unresolved intent and completed result distinct on restart. |
| 04-aci | Language and code workloads need task evidence + typed issue | Retains proposal/authority/tool boundary at its tested contract. |
| 05-code | 03-code | Base-revision conflict explains why old tests cannot certify a changed target. |
| 06-lifecycle | Plans, leases, humans and observability + Session.issue | Lease/admission/budget behavior is in the actual code and worked exercises. |

All current listings are extracted from whole tested definitions by the chapter builder. No packaged `__pycache__`, PYC, test cache or result/QA flag is an execution dependency. Changed undefined/degenerate conventions, interface substitutions and strengthened tests are explained in technical-audit.md rather than silently preserving a faulty old assertion.
