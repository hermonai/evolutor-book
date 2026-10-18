# Contributing

Contributions should improve the active 52-chapter manuscript while preserving
source and architecture provenance. Start with CURRENT_MANUSCRIPT.md,
CHAPTER_STRUCTURE.md, CHAPTER_STANDARD.md and TEXTBOOK_STANDARD.md.

Before opening a pull request:

1. classify new claims in `research/claims-ledger.md`;
2. update theorem status and proof obligations when formal statements change;
3. keep biology, formal semantics, executable references, ML evidence, and runtime evidence distinct;
4. add tests for executable semantics and finite-intervention causality where relevant;
5. report width, state, parameters, compute, data, seeds, and artifact hashes for comparisons;
6. never transfer measurements across architecture renames;
7. reproduce the affected chapter's `drafts/chNN/build.py --check` fixtures,
   run `python3 -m pytest -q -o addopts=''`, then compile the complete candidate
   with `python3 scripts/build-convergence.py --through 52`;
8. inspect changed standalone/cumulative pages in color and grayscale, record
   actual scope and refresh legitimate source-bound evidence;
9. do not run PDF builds concurrently with preservation tests, and do not turn
   an author's test/render pass into independent acceptance.

For new environments, regenerate missing chapter assets with the corresponding
builder's `--assets-only` option before testing, or use the complete builder's
`--through 52 --refresh-assets` option first. Tests of standalone PDFs can skip
when those local PDFs have not been regenerated; do not report them as passes.
Complete-book code references require PyTorch,
NumPy, pytest and Pillow; PDF production also needs XeLaTeX/latexmk, makeindex,
Poppler and librsvg. Historical opening acceptance records are not current
progress counters. Do not modify them to satisfy a new chapter gate.

Do not commit source PDFs without confirmed redistribution rights. This public repository currently carries no general reuse license; contributions do not change that status.

