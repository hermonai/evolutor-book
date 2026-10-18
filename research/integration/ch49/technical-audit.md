# Chapter 49 technical audit

Local author review, 18 October 2026. Serialized reference only; not independent or production-security review.

## Retained scenario and repaired recovery boundary

All incoming event/context/memory, checkpoint/replay/idempotency, ACI/language/code/sandbox, plan/lease/human/concurrency/observability and failure themes remain. The package's volatile tool-result dictionary did not reconstruct idempotency after resume. The expanded oracle logs canonical immutable intent/result events, fingerprints commands, reserves one budget unit before first dispatch and reconstructs maps by replay. Cached result observations are returned as copies so caller mutation cannot alter derived history.

The oracle executes no external effect, authenticates no log, writes no durable store and offers no concurrent transaction. Authorization and lease ticks are trusted host inputs. Queue capacity counts items rather than bytes; retained event history is not bounded total memory. An existing unresolved intent requests reconciliation rather than blind redispatch.

## Proof and tests

The at-most-one local dispatch theorem assumes valid serialized histories and replay before reissue. It is not an exactly-once external-effect theorem. Digest verification binds identity/configuration/prefix bytes against a trusted checkpoint, not origin or truth of the observations. Replay induction validates deterministic reducer reconstruction, not crash durability or concurrent linearizability.

Tests cover empty and surviving-prefix checkpoints, identity/configuration/content/order mismatch, canonical input aliasing and cached-result aliasing, pending/completed reconstruction, changed-command key reuse, duplicate/conflicting completion, budget pre-admission, current authority/expiry, closure with unresolved work, FIFO conservation and forged proposal text. Actual Chapters31 and35 are imported for native and Hermon chunk continuation; the latter uses the actual Chapter23 learned-absolute-position stack. Their ACGT/native vocabularies are not relabeled as trained language/code models.

## Figures and integration

Three editable plates/TXT depict queue occupancy, recovery states and version-bound patch evaluation. Whole short listings and the dispatch proof were inspected with captions and line numbers. A numbered digest equation, selective glossary, meaningful index and twenty worked exercises are included.

Deferred: stable Chapter39 runtime/session adapter, Chapter40 provenance/deletion memory integration, and Chapter45 policy/isolation integration; then failure injection with durable storage and real tool-side idempotency. Coding sandbox and learned language/agent competence require distinct implementation and task evaluations. No passing service integration is claimed.
