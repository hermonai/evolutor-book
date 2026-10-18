# Continuity

EVOD-35 defines the semantic oracle: a request's causal attention sees the exact ordered K/V sequence for its prefix. EVOD-36 may move those K/V rows among physical blocks but may not change order, values, position identity, model identity or ownership.

The page allocator uses `(page_id, generation)` references, explicit reference counts, immutable sharing, copy-on-write for a shared partial tail, and reclamation only at refcount zero. A fork initially shares page references; any mutation that would alter a shared page first creates a private copy. Eviction removes cache ownership but cannot invalidate pages still referenced by live sequences.

Next: EVOD-37 — Continuous batching and precision.
