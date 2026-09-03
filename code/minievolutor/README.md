# MiniEvolutor

MiniEvolutor is a deliberately small executable specification of the bootstrap flow. [E02 — Stored genome to contextual expression](../../book/diagrams/e02-genome-compile-regulate-express.txt) is the canonical system graph; it distinguishes persistent and transient artifacts, suppression records, machine state, trace, and cost.

It currently supports deterministic acyclic dataflow, context-only gates, runtime Python type checks, and verified one-gene replacement. It does not yet implement a parser, staged regulation, autonomous evolution, or the full v1.4.1 small-step semantics.
