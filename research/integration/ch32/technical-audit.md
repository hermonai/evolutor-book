# Chapter 32 technical audit — 10 October 2026

Starting commit: 2048930. Source ZIP and incoming metadata retained.

Handles bind pool-instance UUID, caller owner pair, artifact and generation.
Release retires pinned slots; final acknowledgement alone allows reuse.
Candidate completion matches captured version and advances one live-token position.
Immutable snapshots prevent writable aliases. Same-tenant clone allocates fresh
storage; cross-tenant export is absent. Capacity failure leaves source unchanged.
Logical zero replacement is not secure erase. The actual Chapter 31 bridge
copies CPU float64 inference values and severs autograd.

Forty chapter tests include an independent randomized canary/accounting ledger,
stale handles, duplicate acknowledgement, two-pin retirement, optimistic
lost-update rejection, owner/artifact mismatches, clone isolation and capacity.
Serialized calls do not prove concurrent GPU safety. Device fencing, allocator
semantics, crash persistence and authentication remain outside scope.

Six vector/TXT plates and twenty worked exercises distinguish cancellation
from reclamation. Chapter 33 must restore fresh ownership and refine independent
copies when implementing optimized prefix sharing.
