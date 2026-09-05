# Historical material — not active edition

Original public commit: `3895e94ff206a537a846a88966a27435b14f6ae2`.

Snapshot including unfinished earlier-request work: `9df0d006e10e56cd836a4b84400009dab3cbf4f2` on `archive/pre-reboot-20260905`.

`pre-reboot/book/` and `pre-reboot/research/` preserve the old files byte-for-byte. Their statuses are historical statements, not endorsements by the new edition. Their relative links may point to the original layout; use the snapshot branch for the fully reconstructable old working tree. No source text was destroyed.

Existing `code/` remains in its original location so tests and package imports continue to work. Its classification and limitations are in [the code audit](../REFERENCE_IMPLEMENTATION.md). Historical JSON records and their tests validate structure only, not scientific truth. In particular, the old DOGMA provenance record overgeneralizes a configuration: optional attention/scan in evo-trainer cannot be summarized as a universal recurrent-only lineage.

Restore for inspection in a separate worktree with `git worktree add ../evolutor-book-historical archive/pre-reboot-20260905`. Do not reset the current development tree.
