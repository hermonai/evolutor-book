# Chapter 10 storyboard: conditional computation and routing

Author-approved scope: a deterministic top-1 residual expert branch, not a
reproduction of Switch training or a biological capability demonstration.
Original TikZ plus semantic TXT; computed values use tested reference code.

1. Routing trace: token/expert probability cells, selected edges, capacity slots,
   and one overflow. Label selection versus admission versus weighted output.
2. Gather/scatter: token indices compacted into expert batches and scattered back;
   keep original token identity and show an overflow's unchanged residual.
3. Gradient map: the selected probability remains differentiable; the discrete
   selection and admission decisions do not. Show the top-1 renormalization trap.
4. Capacity history: a full cohort versus two chunks with reset counters versus
   carried counters. Token identity stays fixed; admission changes only on reset.
5. Load and cost: pre-admission demand, admitted count, dropped count and unused
   slots, alongside a computed capacity sweep. Do not turn MAC counts into speed.

Use a full-compute masked oracle for output and gradient parity, deterministic
ties, padding exclusion, expert permutation away from ties, all-overflow
behavior, and integration into the Chapter 9 pre-LN block. Derive the auxiliary
load gradient, including why a uniform numeric loss is not proof of balanced
hard assignments. State grouping/order as model semantics.
