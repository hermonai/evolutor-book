# Continuity
EVOD-30 owns request lifecycle. EVOD-31 defines causal DOGMA state construction/execution and whole-vs-chunk parity. EVOD-32 introduces reusable physical pools with generational handles, scrub-before-reuse and independent clone as the correctness oracle.

EVOD-33 adds immutable data-only checkpoints, integrity digests, artifact/semantic-version binding, restore into fresh mutable ownership, branches from exact token boundaries, and content-addressed immutable prefix state. Sharing is allowed only for immutable snapshots. Mutable branch state remains private. Copy-on-write is presented as an optimization that must refine deep-copy semantics.

The canonical next chapter is EVOD-34 — DOGMA batching and state-native kernels.
