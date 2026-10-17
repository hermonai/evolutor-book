# Chapter 33 technical audit — 17 October 2026

Starting commit: 2f19543. Source package evolutor-ch33-r01.zip SHA-256:
d60373cd75238c9353062d4aaef020023eb1e2515087bff1f3a55b8475c3db54.
All 35 declared package-file hashes verified before import; packaged cache/PYC
files were not executed or adopted. Incoming metadata is retained as UTF-8 text
with a normalized final newline, not as fresh local validation.

## Changes from the incoming candidate

Replace the separate demo recurrence with actual Chapter 31/32 native/pool
interfaces. Context binds tenant, model content, supported native semantics,
ordered-vocabulary tokenization contract, hidden width, vocabulary and dtype.
Reject oversized wire before parsing, duplicate names, nonfinite and overflow
values, nonrepresentable integer hidden values, boolean tokens/positions,
missing/extra schema fields, invalid IDs and inconsistent boundaries.
Native execution rejects unimplemented semantic versions.

Separate checksum consistency, structural validity, native replay and permission.
A rehashed forged state passes structure but fails optional trusted-model replay.
Capture rejects pinned/retiring storage. Restore allocates new ownership and
does not reactivate stale handles. Serialized branch-group preflight rejects
duplicate, already-owned or cross-tenant identities and insufficient capacity,
including pinned retiring slots, before expected mutation.

The LRU stores immutable wire objects, accounts for their exact wire lengths,
validates full context/prefix on lookup, rejects conflicting deterministic state,
and has a forced-key-collision negative control. Oversized insertion does not
evict existing entries. Restored native values remain independent after eviction.

## Mathematics and independent checks

Continuation is an induction over complete state under one deterministic
operator and numerical policy, not proof that arbitrary arrays are sufficient.
An omitted-clock counterexample and explicit inference/autograd boundary
falsify common stronger claims.

The diagonal recurrence has exact-arithmetic error contraction alpha^k and a
geometric accumulation bound for per-step error. Argmax parity still needs a
margin condition. The fixture uses exact rational state updates independent
of native torch code. Every prefix of length 0–3 over three tokens and all
two-token suffixes are checked against that oracle.

Storage sums independently enumerate retained boundaries. Full-prefix token
metadata can grow quadratically even when each hidden state is fixed width.
Uniform residual replay is a workload assumption, not measured latency.
Wire bytes, logical binary payload bytes, Python heap and hardware memory are
distinct quantities.

## Open boundaries

Caller identity, prefix bookkeeping and checkpoint producers are trusted.
No authentication, attack-resistant multi-tenant service, complete parser
sandbox, training restart, crash durability, concurrent allocator, device fence,
physical COW backend or optimized GPU kernel is implemented.
Preflight under serialized calls is not crash/concurrent atomicity.
The code uses no object-deserialization loader and no network requests.
Scientific/genomic capability and hardware performance remain unmeasured.

Six original TikZ/TXT mechanism plates and twenty worked exercises are locally
render-reviewed separately from numerical checks. No independent specialist
review, reader study or publication acceptance is claimed.
