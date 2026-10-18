# EVOD-36

Executable page allocator and paged KV semantic oracle. Each token stores a small K/V row. Logical sequences own ordered page tables; physical pages carry generations and reference counts. Fork/PrefixCache share immutable page references, append performs copy-on-write where necessary, release/eviction decrements references, and flattening reconstructs the exact contiguous KV oracle.
