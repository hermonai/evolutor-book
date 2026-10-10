# Chapter 32 storyboard — revision before prose

1. Logical owner/artifact/position versus physical slot with version and generation.
2. Lifecycle: free, owned, pinned, retiring, final completion, scrub, reused generation.
3. Stale handle and stale in-flight version: address is insufficient.
4. Independent inference clone, same-tenant policy and copied storage.
5. Persistent pool versus step workspace; source snapshots retain no writable aliases.
6. Deterministic canary reuse/accounting and capacity under deferred release.

Serialized bounded inference pool, native Chapter 31 bridge, optimistic completion
version check, explicit no production security/concurrency/durability claim.
