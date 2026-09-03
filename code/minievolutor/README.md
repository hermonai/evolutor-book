# MiniEvolutor

MiniEvolutor is a deliberately small executable specification of the bootstrap flow:

```text
Genome -> compile -> Substrate -> regulate(context) -> ExpressionPlan
                                                    -> execute -> output + trace
```

It currently supports deterministic acyclic dataflow, context-only gates, runtime Python type checks, and verified one-gene replacement. It does not yet implement a parser, staged regulation, autonomous evolution, or the full v1.4.1 small-step semantics.

