# Superseded records

These historical records describe earlier bytes. This pass did not edit them;
they stay valid as statements about what they reviewed, and they do not cover
the current sources or PDF.

| Record | What it describes | What changed | Current evidence |
|---|---|---|---|
| `artifacts/textbook/review.json` (13 September 2026, "Chapters 1–3 LaTeX-first review candidate; not cumulative acceptance") | `tex/textbook/ch03.tex` at SHA-256 `6247fdcd64bd…` and `output/pdf/evolutor-textbook.pdf` | Chapter 3 source edited (F-ch03-a); current SHA-256 `f719e03f6c7b…`. No test binds this record | Chapter 3 pages of `artifacts/review/evolutor-prepublication-review-2026-10-19.pdf`; removed text in `docs/provenance/ch03-source-ledger.md` |
| `research/integration/continuous-through52-review.json` (18 October 2026) | The 619-page `artifacts/review/evolutor-complete-review.pdf` (`89d1be51…6a6e`) | New front/back matter, part openers, guides, layout and the chapter edits listed in CHANGELOG.md | `artifacts/review/prepublication-2026-10-19-manifest.json` and this directory |
| `artifacts/deep/ch{10,13,14}-review-superseded-2026-10-19.json` | Chapters 10, 13, 14 before this pass | Amended records beside them carry a `prepublicationRevision` block | `artifacts/deep/chNN-review.json` |
| `research/integration/chNN/pre-prepublication-local-review-2026-10-19.json` (Chapters 22–25, 32–52) | Those chapters before this pass | Amended records beside them carry a `prepublication_revision` block | `research/integration/chNN/local-review.json` |

The Chapter 1 and 2 acceptance records (`artifacts/deep/ch01-review.json`,
`ch02-review.json`) still match their sources, because those sources were not
edited.
