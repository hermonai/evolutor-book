# EVOD-37

Reference continuous scheduler + precision oracle. Scheduler uses a per-iteration token budget, prioritizes existing decode work, and chunk-fills remaining capacity with prompt prefill. The numerical reference provides FP16-like, BF16-like and symmetric INT8 quantization transforms plus error/argmax quality summaries. This is a semantics/measurement scaffold, not a production scheduler or quantized kernel.
