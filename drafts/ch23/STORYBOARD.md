# EVOD-23 mechanism storyboard

1. Pre-norm residual block with both bypass paths and temporary activation shape.
2. QKV shapes and distinct score/weighted-value paths; all-masked zero convention.
3. Offline, causal and causal-plus-padding legality matrices; query rows run down,
   key columns run right. Invalid queries and keys are both blocked.
4. ACGA versus TCGT, reversing validity along with bases; shared parameters and
   averaged offline logits. Full-record RC must not feed causal next-token features.
5. Evolutor above DOGMA typed carry and Hermon temporary token activations;
   references are not production engines.
6. Numerical contract, synthetic pilot, genomic evidence and biological mechanism:
   only the first two are executed, without promotion to later claims.

All diagrams are editable vector sources with semantic TXT specifications.
Labels, position and crosses preserve meaning in grayscale.
