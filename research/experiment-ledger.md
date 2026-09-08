# Experiment ledger

EVO-EXP01 through EVO-EXP05 are preregistered design outlines in experimental-program.md. Status of each parent training study: NOT RUN. No trained-model loss, accuracy, latency, throughput, scaling, energy or AGI result has been generated. Historical regression test outcomes are reported separately in RESET_REPORT.md.

## EVO-EXP01-CH02-SMOKE: CPU reference diagnostic

Completed for the Chapter 2 development manuscript; no optimizer, training steps, GPU run or architecture comparison. The [fixed child specification](EVO-EXP01-ch02-spec.json) was written before execution and its SHA-256 is recorded in [the result artifact](../artifacts/deep/ch02-results.json). This extends EVO-EXP01 rather than creating a competing registry.

Seeds 11, 29 and 47 generate independent synthetic DNA evaluation inputs. Uniform logits give ln(4) nats/base. PrefixCounts respects the tested prefix interventions (maximum difference zero); deliberately future-reading FutureCopy is detected (difference eight). The leaky diagnostic scores 248 targets versus 256 for the full-length references, so these are not fair comparative model averages. The split example preserves exact/reverse-complement and declared metadata conflict components, not unknown homology.

Reproduce with `python3 examples/deep/ch02.py` from the repository root with PyTorch installed. The reference run used PyTorch 2.10.0 on CPU. These finite controls establish executable checks, not universal causality, genomic prediction quality or DOGMA/Hermon superiority. See [the Chapter 2 report](../DEEP_CHAPTER_2_REPORT.md).
