# Chapter 6 storyboard — approved author scope, 19 September 2026

Question: what state is retained, updated, differentiated, and reset?
Build RNN/LSTM/GRU cell equations and manually implement the PyTorch GRU
variant. Test forward/backward parity, streaming, padding, and truncation.
Synthetic memory examples are not trained genomic capability benchmarks.

1. Unrolled recurrence: three DNA-base inputs, shared parameters, causal state
   edges and next-base readout; input/state/output axes are explicit.
2. LSTM internal paths: forget-retain and input-write merge into cell state,
   output gate reads tanh(cell); dashed gates distinguish control from state.
3. GRU arithmetic: reset-after hidden projection, candidate, convex retention
   merge; show why reset-before is a different operation.
4. Gradient transport: computed scalar retention powers, and a local-versus-total
   Jacobian diagram to prevent the claim that gates guarantee stable gradients.
5. Chunk boundary: carry numeric state, detach gradient, or reset both; padding
   holds state, record boundaries reset it. Arrows denote data versus gradients.

Five editable TikZ/TXT plates, computed tables, twelve worked exercises.
New prose is authored LaTeX. No modifications to earlier frozen chapters.
