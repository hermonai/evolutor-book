# Storyboard

1. Contiguous KV sequence → logical fixed-size blocks → physical page table.
2. Logical token index `(block,offset)` → `(page generation,offset)` translation.
3. Prefix fork: shared full pages, shared partial tail initially immutable.
4. Append to shared partial tail triggers copy-on-write.
5. Reference-count lifecycle and eviction with live branch safety.
6. Fragmentation/waste accounting and page-size tradeoff.
