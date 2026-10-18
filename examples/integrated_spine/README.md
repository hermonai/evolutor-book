# Cross-chapter integration example

Run from the repository root:

```sh
OMP_NUM_THREADS=1 python3 examples/integrated_spine/paged_runtime.py
python3 -m pytest tests/test_integrated_spine.py -q -o addopts=''
```

`paged_runtime.py` connects the actual Chapter 36 `PagedKV` allocator to
Chapter 39's opaque engine protocol and Chapter 41's real interpreter/lowering
handlers. It preserves all layers and learned absolute positions of the actual
Chapter 23/35 Hermon model. Expected example: four consumed tokens, four logits
per token, no live runtime handles, zero occupied pages and eight free pages.

The tests compare full-model logits, private/shared-tail continuations, prefix
eviction, owner/handle fences, allocation failure, runtime cleanup and compiler
effect traces. DCE must retain an engine operation even when its result is unused.
This is an integration oracle, not a substitute architecture or a performance
result. The Chapter 39 manuscript's original adapter remains contiguous; this
separate companion demonstrates the additional paged adapter explicitly.

Calls are serialized; the model remains immutable while requests exist. The
underlying pool stages a contiguous cache for computation. Model replacement,
asynchronous cancellation/acknowledgement, durable memory, authenticated tenant
authority, real tools, distributed migration and GPU kernels are not implemented
by this example. Chapters 37 and 38 have distinct emitted/consumed-token clocks;
this example consumes exactly the explicit input tuple, without joining their
schedulers or advertising speculative serving.
