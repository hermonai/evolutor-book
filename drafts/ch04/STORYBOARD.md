# Chapter 4 storyboard and claim plan

Author-approved production plan, 13 September 2026. Standalone LaTeX candidate;
does not alter accepted chapters or concurrent Chapters 1-3 textbook migration.

1. Shift and mask. Align ACGTN sequence positions with next-base targets, explicit
N and PAD masks, and prediction arrows from each current base only. Digital tokens,
not DNA replication. State loss denominator before code.
2. Split before windows. Group strips assigned to train/validation before any
subwindows. Show a forbidden cross-split copy/RC arrow. Synthetic grouping is not
a homology-detection algorithm.
3. Objective weighting. Two token sets, sums and counts entering one mean;
contrast wrong equal averaging. Empty target set has no mean.
4. Atomic training transition. Sequence of data selection, gradient, momentum,
parameter update and clear-gradient boundary, with checkpoint cut after update.
Draw changed state and retained state; no distributed-system claim.
5. Restart evidence. Generated uninterrupted/restored/broken-control discrepancies
and batch traces; compare parameters, optimizer, RNG and sampler state, not only loss.
6. Evaluation semantics. Two axes: train/eval module behavior and enabled/disabled
autograd. Show dropout retained only in training mode. Evaluation preserves RNG and
parameters in the declared CPU fixture.

Core implementation: CPU float64 embedding/tanh/dropout/linear one-base-context
predictor, fixed synthetic DNA groups, unweighted masked CE, SGD with momentum,
explicit epoch permutation/cursor, separate sampling RNG, serialized state_dict
checkpoint with corpus/config identity and safe weights_only load. Test restart at
multiple cuts and omission controls. No DOGMA/Hermon architecture or genomic benchmark
claim. Whole tested functions are extracted into the printed appendix.
