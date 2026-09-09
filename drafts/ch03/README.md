# Chapter 3 working draft

**Differentiation, optimization and tensor programs**

This directory is prepublication work. It is deliberately outside the accepted source paths so the Chapter 2 review cannot certify Chapter 3 implicitly. The published book still contains Chapters 1–2, unchanged.

Read the [manuscript](manuscript.md), [source ledger](sources.md), [12-figure storyboard](storyboard.json), [executable reference](reference.py) and [computed results](results.json). Four storyboard figures currently have original editable SVG and semantic TXT companions in figures/. The other eight remain plans, not produced artwork.

The first core contains approximately 2400 words across 12 numbered sections and six exercises with worked reasoning. It has not undergone cumulative LaTeX/page review and should not be labeled a complete Chapter 3.

## Reproduce from the repository root

```sh
python3 drafts/ch03/reference.py
python3 drafts/ch03/build_assets.py --check
python3 -m pytest tests/test_ch03_working_draft.py
python3 -m pytest
```

Python 3.13.6 was used for the recorded run. The numerical reference requires PyTorch; recorded version 2.10.0, CPU float64.

The first full regression run passed 202 tests, including 31 working-draft tests. A subsequent preservation fix makes the existing PDF build test run the real recipe in a temporary repository copy, rather than overwrite a published PDF. The final preservation run is recorded in [the progress report](../../DEEP_CHAPTER_3_PROGRESS.md).

## Next production pass

Complete the outstanding source/proof work stated at the end of the manuscript; produce and inspect the remaining figure mechanisms; expand the exercise set; then add a distinct cumulative LaTeX entry point and new PDF filename. Scientific review and every-page inspection must precede any new acceptance manifest. Do not edit old acceptance hashes merely to admit an unfinished chapter.
