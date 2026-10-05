# Chapter 20 storyboard
Approved author plan, 27 September 2026. No independent review implied.

Question: what does a memory keep, for how long, at which cost?
Prerequisites: Chapters 6-7 and 18-19. This chapter owns representation and clocks;
Chapter 21 owns strand symmetry; later engines own optimized kernels.

1. Storage geometry: exact recent token slots versus compressed fast/slow
   numerical state and a pending block accumulator; name all state shapes.
2. Kernel: generated impulse responses for retention 1/2 and 7/8. Input weight
   is 1-a, not one. Normalize lag conventions and distinguish signal from accuracy.
3. Multi-rate clock: six valid positions, B=4 commit, split at position 3;
   carry partial sum and phase. Chunk is a transport boundary, not model reset.
4. Aliasing: [1,-1] and [-1,1] map to the same block mean yet different fast
   states. Do not call coarse-graining lossless.
5. Ownership: separate two record lanes and explicit reset, plus tensor/phase
   fields that must cross a chunk boundary. No implied literal biological organs.

Five semantic TXT companions; twelve worked problems. Reference implements
a differentiable exponential bank and block-clock state, checks convolution,
gradients, chunking, padding and caller ownership. Timescales are hypotheses,
not learned genomic utility. Readout capacity and operational failure cases
are separate from the state recurrence.
