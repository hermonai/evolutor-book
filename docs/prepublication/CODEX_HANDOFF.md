# Handoff notes for the next session

Written 19 October 2026 at the end of the Claude prepublication pass. Read
PUBLICATION_READINESS.md first, then FINDINGS.md. Nothing here authorizes a push,
tag, release, licence or authorship change; those need the author.

## Scope boundaries the new material keeps

The author asked for the book to be sensitive to current DNA computing. That
material was added as *cited summaries of what has been demonstrated*, inside
the book's own declared scope. Two statements in the book define that scope, and
a later session should treat them as binding rather than as placeholders:

- the boxed note in the Epilogue ("A boundary this book keeps"), which states
  what the book does not cover and why that needs specialist oversight;
- the closing section of Appendix A ("What this appendix does not cover").

Both were written for readers, not as internal policy, so they belong in the
text. Widening the scope past them is an author decision, and it would need
specialist review before any draft, because the material concerned sits outside
what an implementation textbook can responsibly carry.

Chapter 48's genomic-application material stays descriptive for the same reason:
it explains how assay labels and variant representations work, and does not
interpret variants for any individual.

Claims about capability keep the discipline the book already uses. The
Epilogue's five questions and Appendix C's evidence classes exist so that a new
result can be stated at the strength its evidence supports; the pass added no
claim of novelty, influence, general intelligence or publication readiness, and
the pilots are reported as the negative results they are (F-ch22-a, F-ch23-a).

## What is unfinished

| Item | State | Where |
|---|---|---|
| ~~Grayscale inspection~~ | Done 19 October 2026: all 643 pages read in grayscale, all 75 Red/Green figures read at 150 dpi in grayscale, every text run measured with `pdftohtml -xml -zoom 1`. Two defects fixed. A monochrome **test print** is the one part an agent cannot do | FINDINGS.md, grayscale section |
| Frozen Chapter 1 paragraph about the companion volume | Open; needs the author. Proposed replacement text is written out | F-ch01-a |
| Chapter 47 exercise order | Open preference; exercises follow the closing bridge, unlike other chapters | F-ch47-order |
| Standalone builders and stale `review.aux` | Open. Builders should regenerate or drop `build/chNN/review.aux` when the preamble changes, and a failed latexmk run should fail the build instead of leaving the previous PDF in place | F-build-stale-aux |
| Glossary entries for the new matter | Optional. The epilogue and appendices introduce terms that are not in the generated glossary | — |
| Rights audit, specialist review, reader study, accessibility | Open gates; none was performed | PUBLICATION_READINESS.md |

## How to resume

```sh
export OMP_NUM_THREADS=1
export PATH=/Library/TeX/texbin:/opt/homebrew/bin:$PATH
python3 scripts/check-chapter-structure.py
python3 scripts/build-convergence.py --through 52      # run twice; must be identical
python3 scripts/audit-production.py --require-ready
python3 -m pytest -q -o addopts='' --junitxml=build/prepublication/regression.xml
python3 scripts/review-convergence.py --pages all
```

`python3` is `/Users/wenyan/.pyenv/versions/3.13.6/bin/python3`. Never run a PDF
build at the same time as the tests.

If a `drafts/chNN/build.py` run fails with `! Undefined control sequence
\@LN@col`, the cause is a stale `build/chNN/review.aux`. Move it aside (this pass
kept the ones it moved in `tmp/recovered-aux-2026-10-19/`) and rebuild. Check
`output/pdf/` afterwards: a failed build leaves the previous PDF in place, so
`--check` can pass against stale bytes.

After changing any chapter source, add an entry to
`docs/prepublication/chapter-amendments.json` and run
`scripts/amend-prepublication-records.py`. It copies each record aside before
amending and refuses to touch an accepted one; the existing superseded copies
must not be overwritten, because they carry the prior path set.
