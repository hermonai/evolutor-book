# EVOD-24 convergence audit

Decision: replace duplicated r01 data exposition with canonical DNA-aware
Transformer mechanisms. Preserve incoming data contracts for Chapter 25's shared
experiment envelope. Chapter 23 owns basic attention/masks; 24 owns span geometry,
strand actions, base-coordinate rotations and access graph semantics.

EVOD24-T1: half-open span [a,b) maps to [L-b,L-a) under RC; stride-grid origin
and omitted tail can break re-tokenization commutation.
EVOD24-T2: causal target base p requires all contributing span ends <=p. Token
triangle alone does not enforce base-level availability; overlapping masked tokens
must all be hidden/corrupted to obscure the base.
EVOD24-T3: tied even/odd embedding is equivariant under joint record RC and
orientation sign change, not under unchanged orientation or arbitrary downstream
mixing. This local representation is not a full Caduceus reproduction.
EVOD24-T4: pair rotations preserve norm and common-coordinate-shift scores;
reflection, full-model RC equivariance and trained extrapolation do not follow.
EVOD24-T5: local/global edges need two layers for a distant offline relay and
never bypass the causal j<=i constraint. Edge count is not measured speedup.
EVOD24-E1: 24 tests cover span/RC/mutation, strand action and batch isolation,
independent block-matrix rotations, norm/shift and float64 finite differences.
EVOD24-E2: sparse/dense values and Q/K/V gradients, legal-index oracle, padding
zero rows, finite future perturbations, reachability and edge-budget checks.
EVOD24-F1: target inside token defeats causal score masking.
EVOD24-F2: suffix-selected global positions can leak despite triangular edges.
EVOD24-F3: equivariant embedding followed by unrestricted parity mixing can fail.
EVOD24-O1: no full genomic training, retrieval, optimized sparse kernel or matched
budget performance claim. Mechanism usefulness and scientific acceptance are open.

Twenty worked questions, six original editable plates and generated traces
separate assigned values from capability evidence. DOGMA/Hermon/Evolutor taxonomy
and Chapter 21 offline causal boundary remain intact. Incoming 23 pilot percentage
is provenance, not the current three-seed result or a genomic benchmark.
