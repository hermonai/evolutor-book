# Foundation-library roadmap

## Decision now

Do not build a new foundation library. PyTorch expresses the initial tensor, autograd, attention, recurrence, loss, and inference semantics, while MiniEvolutor expresses the symbolic GCS path.

## Candidate native concepts

Future requirements may include `Tensor`, `State`, `Genome`, `Gene`, `Regulator`, `ExpressionPlan`, `Trace`, `Mutation`, `Scan`, `Graph`, and `Checkpoint`. Names are provisional.

## Evidence required to leave PyTorch

1. a working experiment blocked by a specific semantic or performance limitation;
2. a minimal primitive that resolves it;
3. reference behavior and gradients where applicable;
4. parity tests against PyTorch;
5. a benchmark showing material benefit;
6. an interoperability and checkpoint plan.

## Possible staged API

```python
plan = genome.regulate(context)
output, trace = plan.execute()
proposal = evolver.propose(genome, trace, loss)
candidate = verifier.check(proposal)
```

This is a requirements probe, not a committed API.

