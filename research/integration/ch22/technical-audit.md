# EVOD-22 convergence audit

## Model contract and corrections

The learned-locus proposal is explicitly distinct from the exact pair-count and
block-clock references in Chapters 18 and 20. It retains causal/offline separation
from Chapter 21. Carry now contains both fast state and memory, with explicit
shape/dtype/device/finiteness checks, no caller mutation, and empty-chunk identity.
The causal base head must have four classes; the offline pilot has two.

Read-before-write order is specified, traced against an independent closed form,
and tested. Parameter count is derived and independently checked for multiple
dimensions. Bounded activations are not presented as a gradient/retention proof.
State-dependent regulators cannot generally use an input-only affine scan.

## Experiment evidence

The three-seed pilot adds a task-relevant local CNN and independent exact motif
oracle. It freezes independent training/test generators and checks exact/RC split
disjointness. Random controls have independent targets on BOTH splits; the incoming
run permuted training labels but scored the original motif labels.

The pilot does not match parameter, arithmetic, context/state or tuning budgets.
Results remain implementation observations, not DOGMA superiority, genomic
capability or industrial runtime evidence. The exact oracle solves the stipulated
task without learning. Weak learned performance is retained, not tuned away to
force a favorable table. Multi-seed variation and every individual run are recorded.

The independent-uniform-target cross-entropy floor is a population expectation,
not a bound on finite-sample or training loss. Any future claim must audit
independence and uncertainty before asserting leakage from one low value.

## Claim/theorem/experiment/failure records

EVOD22-T1: bounded state under zero initialization and sigmoid/tanh updates,
elementary convexity argument; no gradient guarantee.
EVOD22-T2: chunk output/carry/gradient parity under undetached complete carry,
induction plus float64 differential tests.
EVOD22-T3: offline pooled RC invariance with shared parameters, inherited
branch-swap proof; not causal semantics.
EVOD22-E1: assigned-parameter trace checked independently of the transition code.
EVOD22-E2: three-seed synthetic pilot with incomparable budgets explicitly reported.
EVOD22-F1: dropping memory carry changes the function.
EVOD22-F2: offline output depends on suffix, demonstrating its illegal causal use.
EVOD22-F3: read-path erasure changes features while preserving transition carry.
EVOD22-O1: fair architecture benchmark, genomic data and industrial engine absent.

Six figures and sixteen worked exercises support these contracts. Local visual
review is not independent scientific/reader review. Whole-book convergence is open.
