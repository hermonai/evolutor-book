# Local technical audit — Chapter 36

Date: 17 October 2026. Reviewer: author/agent; not independent.

The reference imports the actual Chapter 35 adapter and, transitively, the Chapter 23 learned-absolute-position multi-layer Hermon Transformer. Paged rows contain every layer's projected K/V. Flatten creates fresh contiguous tensors, seals them and validates through the native adapter. Physical layout is changed; logical computation is not replaced by a tuple-only toy.

The chapter proves reference conservation from registry incidence and branch-isolation/native parity by continuation induction. Its preflight formula includes partial-tail COW and all following blocks. Model arithmetic, tensor preparation and table/payload hashes precede serialized publication. Claims are limited to expected validation/arithmetic/capacity failure paths, not crash or concurrent atomicity. No asynchronous page pin is implemented; device work would require the prior completion-fence protocol.

Tests use an independent original full model, compare every layer and output across page sizes/splits, force noncontiguous placement, retain a cache hit through eviction, examine stale generation/foreign handles, all three-branch release orders, private tails at capacity and multi-page OOM. Table, payload and reference-count corruption are deliberate negative controls. Seals detect accidental mutation; a trusted producer can reseal a false cache, so no authentication or native-reachability proof is asserted.

The package's U=sum(request lengths)/(physical slots) is corrected: this is logical multiplicity and can exceed1. Physical utilization counts distinct occupied page rows. Example prefix3/child4/P2 has5 physical rows in6 slots,7 logical rows,512-byte pages; capacities/metadata/staging costs remain distinct.

Limitations: serial trusted Python registry, immutable full-page sharing with partial-tail replacement, exact float64 arena only, expensive repeated artifact/content hashing, contiguous native compute staging, no production security/concurrency, device kernel or measured speedup. Prefix cache is bounded by entry count, not a byte budget, and put/replacement is not advertised as an atomic cache transaction.
