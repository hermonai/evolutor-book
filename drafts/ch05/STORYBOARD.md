# Chapter 5 production storyboard

Author-approved scope, 15 September 2026: tokenization and sequence representation.
Build an original deterministic tokenizer and explicit embedding example. No
borrowed prose/artwork/code from Raschka; reference his general implementation-first pedagogy.

1. One sequence, three segmentations: ACGTACG, single bases, overlapping 3-mers,
   disjoint 3-mers plus an explicit short tail. Show nucleotide spans and offsets.
2. Base-four integer encoding: ACG digits 0,1,2, weighted sum 6; invert by divmod.
3. Embedding lookup and gradient accumulation: repeated token selects one row
   twice; show numeric rows and accumulated gradient, not a decorative neural network.
4. Future leakage: overlapping tokens ACG and CGT share CG; a shifted token
   label reveals only T as new information. Show a safe next-unseen-base target.
5. Reverse-complement alignment: reverse token order and complement each token;
   disjoint segmentation of a length-seven sequence changes tail alignment.

Resource tradeoffs are computed tables. Canonicalization gets an explicit
counterexample for directional tasks, not an assumed biological invariance.
All code tests must include lossless reconstruction, invalid inputs, offsets,
target reach, special tokens, gradient rows, and representation identity.
