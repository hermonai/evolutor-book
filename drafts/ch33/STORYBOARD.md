# Chapter 33 storyboard — approved before local prose, 17 October 2026

Scope: serial, bounded CPU float64 inference snapshots of the actual Chapter 31
recurrence in the Chapter 32 pool. Independent copies are the correctness oracle.

1. Boundary cut: consumed token cells on the left, untouched suffix on the right,
   hidden coordinates and position at the cut; show missing-clock counterexample.
2. Envelope: exact schema/context/prefix/payload fields bracketed by the digest.
   Separately draw the trusted-producer boundary: a digest is not authorization.
3. Restore and branch: one immutable byte envelope produces two separate pool
   slots and new owners. Divergent single-token transitions carry exact numbers.
4. Prefix matching: token rows with longest exact prefix, rejected same-text
   different-token and cross-namespace candidates; execute only the suffix.
5. Copy-on-write refinement: independent-copy oracle beside a conceptual shared
   page with reference count two, first-write private copy, unchanged other page.
   Explicitly mark physical COW as unimplemented.
6. Cost tradeoff: state-only checkpoint bytes versus full-prefix metadata and
   expected replay as spacing changes. Axes use declared modeled units, not speed.

All plates: original TikZ vectors, readable at print size, restrained labeled
colors, semantic TXT companions. No decorative biology in an engine chapter.
Risks: identity is not replay proof; bounded JSON is not a sandbox; serialized
preflight is not concurrent atomicity; stored values do not retain autograd.
