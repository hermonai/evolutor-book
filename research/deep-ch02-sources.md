# Chapter 2 source and evidence ledger

Author-agent review, 8 September 2026. No independent reviewer or Claude Academic dossier was available. The storyboard and EVO-EXP01-CH02-SMOKE specification preceded implementation. No training was run.

## Sources actually consulted

- Walsh et al., DOME, Nature Methods 18 (2021), 1122–1127, [primary article](https://doi.org/10.1038/s41592-021-01205-4). Primary indexed article text read. Data, optimization, model, evaluation reporting anchors; not a new scoring algorithm.
- Cawley and Talbot (2010), JMLR 11, 2079–2107, [primary abstract](https://jmlr.org/papers/v11/cawley10a.html). Finite validation/model-selection overfitting; no imported quantitative estimate.
- Ferrer Florensa et al., SpanSeq (2024), [primary preprint](https://arxiv.org/html/2402.14482v1); published NAR Genomics and Bioinformatics 6, lqae106. Introduction/methods read. Biological similarity-aware splitting, with task-specific similarity assumptions. Our exact/RC/declared-group union is not SpanSeq and is not a homology detector.
- Zhou et al., DNABERT-2, ICLR 2024, [paper](https://arxiv.org/abs/2306.15006) and [author repository](https://github.com/MAGICS-LAB/DNABERT_2): abstract and implementation description consulted for genomic BPE. Early abstract and repository benchmark counts differ; no benchmark totals or superiority numbers copied. Its masked-language objective is not identical to autoregressive next-base evaluation.
- Nguyen et al., HyenaDNA (2023), [primary abstract](https://arxiv.org/abs/2306.15794): single-nucleotide tokenization example only, not a throughput comparison.
- Vaswani et al. (2017), [primary paper](https://arxiv.org/abs/1706.03762), Chapter 1 source: autoregressive attention context; our indexing derivation is original.
- Zhang et al., ICLR 2017, [primary abstract](https://arxiv.org/abs/1611.03530v2): fitting random training labels does not imply predicting independent fresh random targets.
- Bouthillier et al. (2021), [MLSys paper](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf): abstract/intro-level variance anchor. Seed summaries here are explicitly illustrative, not fitted distributions or confidence intervals.
- Guo et al. (2017), [PMLR primary abstract](https://proceedings.mlr.press/v70/guo17a.html): confidence calibration distinct from accuracy; no calibration experiment claimed.
- Gu and Dao, Mamba, [primary abstract](https://arxiv.org/abs/2312.00752v2): selective state-space baseline family, not a reproduced training result.
- [PyTorch 2.10 CrossEntropyLoss](https://docs.pytorch.org/docs/2.10/generated/torch.nn.CrossEntropyLoss.html) and [reproducibility notes](https://docs.pytorch.org/docs/2.10/notes/randomness.html): logits, target indexing, reduction, and reproducibility boundaries. Installed reference environment is torch 2.10.0; do not substitute newer unversioned documentation.

## Repository evidence and scope

Existing research/experimental-program.md and experiment-ledger.md define EVO-EXP01–05. The child CPU smoke record extends EVO-EXP01 without marking its parent training experiment complete. Existing evo_torch.causality is reused and hardened against nonfinite outputs and mode-restoration failures. Fixed prefix counts and the deliberately future-reading predictor have no trained weights. Seeds 11/29/47 vary generated evaluation data only, not optimization runs.

The array [0.51,0.97,0.99] is supplied illustrative data, not a measurement and not enough to establish bimodality. Exact synthetic oracle outputs and analytical entropy identities are original mathematics. Split guarantees cover only declared conflict edges; unknown homology, phylogeny and overlapping coordinates require additional metadata/detection. No DOGMA or Hermon DNA architecture improvement, engine performance, trained-model capability, GPU result, or general-intelligence claim is made.

## Consistency boundary

DOGMA means non-Transformer DNA-native architecture plus its non-Transformer engine. Hermon DNA means Transformer-based DNA architecture plus its Transformer engine. Evolutor is the wider research/theory/compiler/runtime/orchestration framework. Shared biological terminology refers to Book I; tokenizing genomic strings is not itself molecular computation.
