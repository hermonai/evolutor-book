# Storyboard

1. Arrival/admission → paged-memory capacity → ready queue.
2. Iteration scheduler mixing decode tokens and bounded prefill chunks.
3. Timeline showing TTFT, decode token timestamps and ITL.
4. Precision stack: weights / activations / KV / accumulators as separate choices.
5. Quantize → execute → dequantize/reference comparison → quality gate.
6. Throughput-vs-tail-latency frontier; no single scalar optimization target.
