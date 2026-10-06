# Chapter 27 visual teaching plan

## 01-memory

Persistent parameter, gradient, two moment and optional master arrays are separate from workload live activations/workspaces and runtime/distributed buffers. P=195; hypothetical all-FP32 arrays3120bytes, actual all-Float64 arrays6240bytes. Neither is measured peak.

## 02-accum

Record microbatches5/5/2 have weight masses12/13/6. Backpropagate N1/31,N2/31,N3/31 at fixed parameters; sum gradients then unscale/check/clip and one update. Local means divided by3 change weighting.

## 03-checkpoint

Save input boundary and parameter version; forward nonlinear/dropout block; discard inner saves. Backward reconstructs using same input, parameters and RNG. No replay preserves first-forward loss but changes gradients by about.220225; replay also preserves caller CPU RNG trajectory.

## 04-precision

Explicit policy chooses operator dtype, sensitive-reduction precision, moments/master dtype. Scaled backward -> unscale -> finite check and clip -> one update or skip. Diagram specifies algorithmic order, not executed AMP certification.

## 05-adam

Complete gradient fans out to first and second moments. Correct clock t supplies both bias corrections before writing theta_t. Semantic tests compare loss, all gradients, both moments and parameters.

## 06-gate

Semantic loss/gradient/update gate precedes numerical dtype/restart, measured resource peak/time and multi-seed scientific quality. This chapter passes only its CPU semantic fixture and toy static accounting; remaining gates open.

Editable TikZ sources and semantic TXT companions; labels and contrasting line/shape conventions preserve meaning in grayscale. No externally copied artwork.
