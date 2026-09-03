# Non-Transformer DNA baseline

## Purpose

Establish ordinary recurrent/state baselines before claiming a genomic mechanism. The first executable baseline is a GRU with explicit full-sequence and one-token stateful paths.

## Reference path

```text
DNA character IDs [B,T]
        |
embedding [B,T,D]
        |
GRU recurrence, carried state [L,B,S]
        |
vocabulary logits [B,T,V]
```

The baseline tests that repeated `step(token, state)` equals full-sequence forward execution. It supplies a control for later simple recurrence, state-space, selective-scan, regulation, and trace-aware models.

## Research ordering

1. GRU;
2. explicit first-order linear/gated recurrence;
3. simple state-space update;
4. selective update with state-capacity sweeps;
5. regulated expression or GCS mechanisms only after generic controls.

None is defined as “genomic computation” merely because it carries state.

