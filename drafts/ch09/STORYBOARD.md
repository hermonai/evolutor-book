# Chapter 9 storyboard: assembling a Transformer block

Author storyboard approved for implementation, 20 September 2026.
The first five plates expose mathematical mechanisms, not biological interactions.

1. Residual computation: pre-normalized attention and FFN branches reconnect to unchanged-width skip paths. Mark two addition nodes, each sublayer input, and identity-gradient bypass. Risk: accidentally drawing post-normalization or sharing the two LayerNorm parameter sets.
2. Layer normalization geometry: one four-feature token becomes centered and scaled; mark feature axis, mean, variance and epsilon. Backward sensitivity removes a constant component and a centered-input component. Risk: calling the scale direction an exact nullspace when epsilon is positive.
3. Position coordinates: sine/cosine pair at absolute positions, showing a displacement as a 2D rotation; cached chunk starts at P, not zero. Risk: claiming arbitrary extrapolation is validated by a mathematical encoding.
4. Complete block cache: two stacked blocks own separate K,V histories derived from their own normalized inputs. Current chunk flows through both; immutable past state is read, new entries appended. Risk: reusing layer-1 keys for layer 2 or detaching during gradient-parity checks.
5. Objective alignment: input token positions predict next token; validity and record identity gate each target edge. One boundary edge and padding edges are visibly excluded. Risk: dividing by padded length or treating a causal mask as sufficient to prevent label leakage.

6. Synthetic training trace: a data-generated loss curve with update count and the valid-target denominator explicit. Distinguish training-set fit from generalization; no biological claim follows. Added as a numbered figure to keep all visual evidence captioned.

Use vector tensor/graph geometry with labels and shapes, not decorative prose
panels. Native TikZ/TXT, all-page color/grayscale render review.
