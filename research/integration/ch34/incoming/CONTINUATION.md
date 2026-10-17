# Continuity
EVOD-31 defines one-request DOGMA causal execution; EVOD-32 gives each live state safe pool ownership; EVOD-33 adds immutable checkpoints/branches. EVOD-34 batches independent *state transitions* without changing those semantics.

The scalar per-request step is the correctness oracle. Scheduler → gather → batched transition → scatter must equal applying the scalar oracle independently in request order. Inactive lanes must not advance clocks/state. Request completion/cancellation may change batch membership only between declared scheduling boundaries. Kernel fusion/layout are performance transformations, never permission to weaken ownership.

Next: EVOD-35 — Hermon DNA prefill, decode and KV state.
