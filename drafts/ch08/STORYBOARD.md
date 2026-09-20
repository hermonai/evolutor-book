# Chapter 8 storyboard

The chapter owns single-head attention semantics and cache parity. All assets are original TikZ/vector diagrams plus semantic TXT descriptions; no biological mechanism is implied by tensor operations.

1. Tiny weighted retrieval: query, keys, compatibility scores, normalized weights, and separate values. Hand case scores log(2),0 gives weights 2/3,1/3 and output (2,2); shapes annotate every edge.
2. Packed causal mask: explicit 5-by-5 allowed/blocked matrix for two records plus padding. Color plus symbols distinguish allowed edges. Empty rows use an explicitly zero-output policy, not softmax over all minus infinity.
3. Score-to-output gradient: softmax Jacobian contracts with value deviations; masked coordinates have zero probability and gradient. Show why a large weight is not a biological causal explanation.
4. Cache timeline: old keys/values, append a two-token chunk, and offset-causal query rows. Show absolute positions; a rectangular upper-left causal mask is the wrong cache mask.
5. Multi-head reshape: feature axis to head and channel axes, independent attention, concatenation, output projection. State precise ownership of cached K/V and distinguish operation counts from measured speed.

Numerical tables and mask cells are generated from tested code. Captions identify shape contracts, semantic limits, and the correct inference. Every page is checked in color and grayscale.
