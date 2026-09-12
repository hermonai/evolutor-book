# Chapter 3 review candidate

**Differentiation, optimization and tensor programs**

This is a standalone review candidate, not a newly accepted cumulative edition.
The accepted Chapters 1-2 and their recorded source/PDF hashes remain unchanged.

The [manuscript](manuscript.md) now has twelve original editable SVG figures,
each with a semantic TXT companion, plus twelve exercises with worked solutions,
a selected glossary, primary-source notes and executable examples.

Read the [source ledger](sources.md), [storyboard](storyboard.json),
[reference implementation](reference.py), [reference results](results.json),
[boundary diagnostics](completion_diagnostics.py) and
[diagnostic results](completion-results.json). Biology and software are explicitly
distinguished; schematic molecules do not constitute a calibrated laboratory model.

## Reproduce

Use Python 3.13 with the repository dependencies installed; the verified PyTorch
version is 2.10.0. Building requires Pandoc, XeLaTeX, rsvg-convert and Poppler;
the Mac PDF style uses Times New Roman, Arial and Menlo. Page rendering also uses Pillow.

```sh
python3 drafts/ch03/build_assets.py --check
python3 -m pytest -o addopts='' -q
python3 drafts/ch03/build_review.py --render
```

The isolated builder writes the Chapter 3 review PDF under output/pdf/, renders
every page under tmp/pdfs/ch03-review/ and records source hashes under
build/ch03-review/. It never invokes the accepted cumulative PDF recipe.
Figures remain editable vectors in the PDF. Appendix A reproduces tested boundary
diagnostics directly from source; Appendix B includes the access-depth source ledger.

See [the review report](../../DEEP_CHAPTER_3_REVIEW_REPORT.md) for checks, author
visual-review evidence, limitations and the next bounded step. Independent
scientific review and cumulative integration/index/bibliography remain release
gates. Future chapter manuscripts are not generated in this checkpoint.
