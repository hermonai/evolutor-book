# Chapter 19 storyboard — 27 September 2026

Author-approved scope before prose: one explicitly proposed non-Transformer
operator with causal input-conditioned gates; not a trained DOGMA model. Extend
Chapter 18 without duplicating Chapter 7's scan derivation or Chapter 10's MoE.

1. **01-address** — What selects a transformation? A DNA-symbol pair selects one
   table row containing candidate, write logit and retention logit. A matrix strip
   exposes the distinct parameters and one active row; software addresses, not
   a molecular binding illustration.
2. **02-update** — What is retained versus overwritten? Two arithmetic paths
   compute a*old_state and (1-a)*candidate; add them into the next state. The
   write gate changes both coefficients. Scalar worked values support inspection.
3. **03-causality** — What is known before state evaluation? Positions 1..4 carry
   token-derived gates and causal recurrent edges. An explicitly prohibited
   future-to-past arrow shows leakage; no biological causation implied.
4. **04-feedback** — Why do locally bounded values not prove contraction? Plot
   the feedback-gated scalar map and identity near zero. A tangent marks derivative
   2.5 even though the output remains in the candidate/state convex hull.
5. **05-ablation** — Which information loss is repaired? Two sequences AACA/ACAA
   have identical pair histograms but distinct proposed terminal states. Compare
   generated trace values and controlled ablations, not invented training metrics.

Risk checks: shape/axis semantics, constant and input-only versus state-conditioned
gates, mask identity, record reset, derivative paths, exact/float distinction,
strand symmetry, and no throughput/capability claim from the synthetic examples.
