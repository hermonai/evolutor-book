# Chapter 40 figure decisions (before prose)

1. Provenance DAG: source e1 and e2 feed summary s1; s1 and e2 feed s2. Tombstone e1 makes s1 and s2 unavailable, including through a stale index. No claim of physical erasure.
2. A genuine compression collision: distinct source strings share first two words; summary payloads coincide but identities/source edges differ. Rehydration follows edges rather than inverts payload.
3. Working-context budget: whole UTF-8 payload records accumulate to a prefix budget; a separate policy-grant line never originates in retrieved content. Issued context revocation is a distinct distributed problem.
