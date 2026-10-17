# Chapter 34 technical audit — 17 October 2026

Starting revision: 7728387. The supplied ZIP's 35 declared hashes were
verified before local integration; its caches/PYC/build claims were not adopted.

## Semantic correction

The incoming a*h+XW NumPy demo was not the actual prior model. Replace it
with the Chapter 31 input-gated diagonal recurrence through the same Chapter
32 module imported by Chapter 33. Checkpoint-restored branches now continue
in one batch, with exact independent rational states.

Pure numerical batching uses active-row lookup before arithmetic. Every
inactive row preserves state and clock; it publishes no logits. Zero input
is explicitly tested as a failing substitute. Duplicate slots including
inactive aliases, busy slots, invalid live tokens, nonfinite candidates,
foreign caller/pool/artifact/generation are rejected before pin acquisition.

The serialized adapter gathers complete snapshots and computes candidates
before acquiring pins. Issued job object identity, immutable scalar candidates,
per-lane pin completion and model-content revalidation prevent accidental
mismatched completion. A model change discards all pins. Cancellation retires
a slot until acknowledgement; a sibling may commit. An external version
winner makes the old batch completion reject rather than overwrite it.

## Mathematics and numerical evidence

Row independence gives scalar parity and request-permutation equivariance.
An explicit masked identity differs from decay on a zero embedding.
The recurrence-specific geometric error bound includes independent output
reduction error and a sufficient greedy-margin condition; it does not certify
arbitrary DOGMA, fp16 kernels or future divergent token sequences.

Rational enumeration covers all 81 four-token sequences of the tiny model.
Random assigned native models compare scalar/batched values across seeds and
batch sizes. Tests also cover restored branches, canaries, ownership, churn,
fixed-ready-cohort round-robin sweeps and logical byte/FLOP arithmetic.

The corrected logical payload model matches embedding/gating, not the
incoming dense input projection. Base kernel, additional staging and one
intermediate are separated. The bars do not measure latency or actual Python
allocation; weights, transactions, clones and metadata are excluded.

## Boundaries

No concurrent prepare/scatter protocol, GPU kernel or device fence, durable
job recovery, hostile-code isolation or integrated network-output publication.
Per-lane completion is not a cross-request atomic transaction. Every issued
job must be finished/discarded; abandoned jobs can retain pins.
Six editable mechanism figures and twenty worked exercises are author-reviewed,
not independent specialist/reader acceptance.
