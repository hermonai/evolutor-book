# Integration contract

Reconcile page/block terminology with the integrated Hermon runtime. Verify paged-vs-contiguous attention parity, allocator generation/refcount invariants, prefix-sharing isolation, COW on partial pages, eviction with live references, OOM/failure atomicity, and multi-tenant namespace policy.

Benchmark page size, lookup overhead, fragmentation, prefix-hit rate, memory utilization and throughput on declared hardware only after semantic parity passes. Production rendering and independent review remain separate gates.
