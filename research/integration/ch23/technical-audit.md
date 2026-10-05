# EVOD-23 convergence audit

Incoming r01 was inspected with Chapters 22 and 24. Hermon remains Transformer
based; DOGMA remains recurrent/non-Transformer; Evolutor sits above both.

EVOD23-T1: legal-row softmax normalization; entirely masked rows need the declared
zero-output convention, not an undefined softmax or artificial uniform prediction.
EVOD23-T2: two-pass offline RC invariance on the sequence-and-validity-mask pair;
shared weights and an involution are premises. It is forbidden as causal context.
EVOD23-T3: exact parameter accounting for embeddings, blocks, normalization and
both heads, including the inactive LM head during classification.
EVOD23-E1: independent row-wise allowed-index attention values/gradients, finite
differences, strict masks, padding invariance and finite suffix intervention.
EVOD23-E2: frozen synthetic ACGT classification, three seeds, CNN/string baselines
and independent random targets. ACGT is its own RC, not two distinct motifs.
EVOD23-F1: offline context can change prefix outputs; causal context cannot.
EVOD23-F2: parameter counts differ and epochs do not equal matched compute budgets.
EVOD23-O1: masked pretraining, genomic benchmark, optimized engine, matched compute
comparison and independent specialist/reader review are not implemented.

Attention scaling is derived under explicit centered independent coordinate
assumptions, not claimed to universally bound trained logits. Padding cannot
silently shift valid positions, revive invalid queries through biases or discard
the validity mask in the RC branch. Invalid classification records are rejected.

Seven primary-source records were checked at recorded depths. Evo 2 now cites the
2026 Nature version. Transformer/Hyena/Caduceus abstracts and source READMEs are
not misrepresented as reproduced experiments. Nucleotide Transformer full text
was inaccessible in this check, so only its indexed primary abstract is claimed.

All six figures were redrawn to expose residual, score/value, mask and RC logic.
Local review, full-book convergence and independent acceptance remain separate.
