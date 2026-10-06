# EVOD-30 technical audit

46 chapter tests. Entire incoming package and neighboring boundaries inspected
before explicit import. The strengthened oracle integrates registry, request,
launch reservation, output queue, terminal arbitration and cleanup.

Independent checks:

- All 6^5=7,776 event words over launch/commit/consume/cancel/complete/cleanup
  compared prefix by prefix with a separate manual specification that never
  calls runtime operations. Phase, reason, pending work, revision, queue and
  conservation are checked after accepted or rejected acts.
- All completion/cancellation/failure permutations preserve the first winner;
  arrival exactly at deadline chooses deadline first.
- Increasing lease generations across state-ID reuse; stale/foreign release,
  duplicate claim, mismatched ticket and same-name ABA rejection.
- Generated total, queued items and UTF-8 byte budget are independent.
  Worst-case reservation blocks without state advancement.
- Cancellation fences output/state commit but cannot release pending work.
  Settled discarded work differs from discarded output.
- Committed bytes remain drainable after terminal selection; explicit cleanup
  discard counts lost output. Release failure retains local handles.
- Malformed/empty/oversized results terminate without output or revision advance.
  L=S+P for work; G=Q+D+X for output; revision=G.
- Thread arbitration uses an external lock, not an internal thread-safety claim.

Normal fixture ends L=S=G=D=revision=3, P=Q=X=0. Cancelled pending fixture ends
L=S=1, discarded work=1, G=0. Dequeue is not client receipt. The ordered in-memory
trace is not authenticated, replay-complete, crash-resilient or a billing meter.

Trusted serialized calls and one pending step are assumed. Identity is not
authentication; leases are fences, not unforgeable capabilities. No native-state
arithmetic, HTTP transport, device synchronization, crash recovery, scheduler or
full DOGMA/HermonDNA parity is implemented. Bounded enumeration excludes process
crashes, weak-memory races and distributed schedules. RFC distinctions inform
retry context, not the definition of this original state machine.

Six original editable plates/TXT, five complete tested listings and twenty worked
exercises. Hash-bound standalone review, cumulative layout, specialist/reader
review and publication acceptance remain distinct. No acceptance promotion or push.
