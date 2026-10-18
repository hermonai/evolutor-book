# Validation report

Everything below was run on this machine on 18–19 October 2026 and reports what
the commands actually printed. It records local verification by one agent. It is
not independent certification, and no field in any review record was promoted to
accepted or independently reviewed.

## Environment

| Tool | Version |
|---|---|
| Python | 3.13.6 (`/Users/wenyan/.pyenv/versions/3.13.6/bin/python3`) |
| PyTorch / NumPy / pytest / Pillow | 2.10.0 / 2.4.3 / 9.0.2 / 12.1.1 |
| XeTeX | 3.141592653-2.6-0.999998 (TeX Live 2026) |
| latexmk | 4.88 (9 March 2026) |
| Poppler (`pdftoppm`) | 26.07.0 |
| librsvg (`rsvg-convert`) | 2.61.1 |
| Environment | `OMP_NUM_THREADS=1`, `PATH=/Library/TeX/texbin:/opt/homebrew/bin:$PATH` |

Starting revision `2fd93ec` on `main`, clean working tree. PDF builds were never
run concurrently with the tests.

## Commands and results

```sh
python3 scripts/check-chapter-structure.py
python3 scripts/build-convergence.py --through 52        # run twice
python3 drafts/chNN/build.py --check                     # NN = 04..52
python3 scripts/audit-production.py --require-ready
python3 -m pytest -q -o addopts='' --junitxml=build/prepublication/regression.xml
python3 scripts/review-convergence.py --pages all
```

| Command | Result |
|---|---|
| `check-chapter-structure.py` | exit 0 — "52 chapters, 12 parts; authored through 52; dependencies acyclic" |
| `build-convergence.py --through 52`, first run | exit 0 — 643 pages |
| same command, second run | exit 0 — byte-identical PDF, so the build is deterministic and free of incremental auxiliary-file failures |
| `drafts/chNN/build.py --check`, all 49 chapters 04–52 | all exit 0 |
| `audit-production.py --require-ready` | exit 0 — Chapters 36–52, 17 chapters "ready for manual review", local evidence declarations only |
| `pytest -q -o addopts=''` | 2080 passed, 0 failed, 0 skipped, 0 errors; JUnit XML at `build/prepublication/regression.xml` |
| `review-convergence.py --pages all` | exit 0 — 643 of 643 pages rendered, 161 contact sheets in colour and 161 in grayscale under `tmp/pdfs/convergence-review/` |

No skipped tests: every standalone chapter PDF existed when the suite ran,
because all 49 were rebuilt during this pass.

## Artifact identity

| Item | Value |
|---|---|
| PDF | `artifacts/review/evolutor-prepublication-review-2026-10-19.pdf` |
| SHA-256 | `6a33815aee31f0741cfd06078f223654de4f43b9ae01b84bdcd856463901a1fd` |
| Bytes / pages | 3,626,590 / 643 |
| Build record | `build/convergence/build-record.json`, same SHA-256, 952 bound source hashes |
| Manifest | `artifacts/review/prepublication-2026-10-19-manifest.json`, `accepted: false`, `independent_review: false` |
| Supersedes | `artifacts/review/evolutor-complete-review.pdf` (`89d1be51…6a6e`, 619 pages), left unchanged |

Bibliography: 147 entries from 190 chapter and matter contributions, merged by
identity (DOI, then arXiv ID, then URL). The previous build had 132 entries;
the matter added about 24 and arXiv normalisation merged about 9 duplicates that
had appeared two or three times as `abs`, `html` and `pdf` views or as different
versions.

LaTeX diagnostics on the final build: 0 overfull hboxes, 0 overfull vboxes. The
only remaining warnings are two missing italic font shapes
(`DejaVuSansMono.ttf/m/it`, `texgyreheros-regular.otf/m/it`), where XeTeX
substitutes the upright shape; no reference, citation or label is undefined.

## Physical-page coverage

| Pass | Coverage | How |
|---|---|---|
| Complete volume, colour | all 643 pages | 27 contact sheets at 45 dpi, six pages per sheet, read in sequence |
| New front and back matter | title page, preface, how to use, contents at a glance, epilogue, Appendix A | 80 dpi full-page renders |
| Changed standalone chapter pages | all 53 changed pages across 28 chapters | 75 dpi colour, one page at a time |
| Specific repairs | Figures 9.6, 13.5, 20.2; Chapter 36 page 6; Chapter 20 pagination; Appendix A coordinate table | 70–110 dpi renders, before and after |
| Complete volume, grayscale | all 643 pages | 27 sheets at 45 dpi, six pages per sheet, converted to grayscale and read in sequence (19 October) |
| Figures using the Red/Green pair | all 75 | cropped from 150 dpi page renders, converted to grayscale, read four to a sheet |
| Type size | every text run on every page | measured with `pdftohtml -xml -zoom 1`, which reports effective size after plate scaling |

Contact sheets at 45 dpi show layout, collisions, breaks and widows; they do not
by themselves prove that a small label is legible. That question was answered
instead by measuring every text run in the PDF: the smallest word label in the
book is now 8pt, and the only smaller text is mathematical sub- and
superscripts and code line numbers. Dense figures, listings and tables were read
at 110–150 dpi wherever the measurement or the grayscale sheets raised a
question, and the two defects that surfaced were fixed (F-gray-howto,
F-gray-labels).

## Changed-page identification

Changed pages were found by comparing each rebuilt standalone PDF with the
superseded one, page by page, in two ways: extracted text, and a 60 dpi raster
hash. Every page whose raster hash changed was re-rendered at 75 dpi and
inspected. Pages whose raster hash was identical retain their prior local
inspection; this is recorded in each amended record as
`unchanged_page_policy`, and the per-chapter lists are in
`chapter-amendments.json`.

The superseded standalone PDFs of Chapters 10, 13, 14, 22–38, 42, 45, 46 and 47
were built under TeX Live 2025 (`xdvipdfmx 20250205`) and the new ones under TeX
Live 2026 (`20260317`), so raster comparison also catches toolchain-only
differences. Exactly one such difference was found and inspected: Chapter 36
page 6, where the note label of Figure 36.3 is placed differently. That figure's
source hash is unchanged.

## Independent checks of specific claims

- **Pilot statistics** (Chapters 22 and 23) were recomputed from each chapter's
  `results.json` rather than taken from the prose: per-seed accuracies, the
  random-label controls, the training losses, and the chance standard error for
  128 balanced test records, √(0.25/128) = 0.044.
- **Worked numbers in Chapters 1–11** were recomputed by hand or by script and
  all matched.
- **Coordinate conventions** in Appendix A were checked against the primary
  documents: the UCSC format FAQ for BED, the VCF 4.3 specification for `POS`,
  and the Sequence Ontology GFF3 specification. Access date 18 October 2026.
- **New bibliography entries** for AlphaGenome, Evo and Enformer were checked
  against the publisher pages for author list, title, venue, volume, pages, date
  and DOI. Entries copied from the companion DNA Computing book keep that book's
  verified metadata.
- **Colour separability** was computed rather than judged: the palette's relative
  luminances put Red at 0.116 and Green at 0.128, and the three pale tints within
  0.03 of each other, so those pairs cannot be told apart in monochrome. Every
  figure using Red with Green was then checked for a redundant non-colour cue;
  all 75 carry one.
- **Builder behaviour** gained two tests: arXiv identity normalisation across
  `abs`/`html`/`pdf` views and versions, with DOI still taking precedence; and
  the source-note heading rewrite, including the cases it must leave alone.

## Failed attempts and how they were resolved

1. **Standalone builds failed silently on 14 chapters.** `drafts/chNN/build.py`
   aborted with `! Undefined control sequence \@LN@col`, caused by a stale
   `build/chNN/review.aux` written when the preamble still loaded line numbering.
   A failed build leaves the previous PDF in `output/pdf/`, so `--check` could
   still pass against stale bytes. Each aux file was **moved**, not deleted, to
   `tmp/recovered-aux-2026-10-19/`, and the chapter rebuilt cleanly. The builder
   itself was not changed; this is open finding F-build-stale-aux.
2. **Key-ideas boxes split across pages.** `\Needspace{6\baselineskip}` was not
   enough for a four-bullet box. Raising the reservation would have been
   guesswork, so the box was made unbreakable instead; it now moves whole.
3. **Measuring plates in a horizontal box broke Figure 13.5.** Switching the
   plate macro to a `varwidth` box fixed a figure whose legend line had been set
   beside its plot, but a `varwidth` of `8\linewidth` also made `\linewidth`
   enormous *inside* the box, so plots sized as `.87\linewidth` (Figures 9.6 and
   20.2) grew and Chapter 20 lost a page. Resolved by saving the real measure and
   restoring `\linewidth` inside the wide box; every chapter then kept its
   previous page count and Figure 13.5 matches its standalone layout.
4. **An earlier run of the amendment script dropped paths.** Rehashing only the
   current chapter files lost `drafts/ch09/reference.py` and the test files from
   Chapter 10's record, which `test_ch10_review` caught and the audit reported as
   uncovered source tests. The script now rehashes the superseded record's exact
   path set plus the current chapter files.
5. **Raising the Epilogue plate's labels needed two corrections.** Setting every
   label to `\scriptsize` first pushed three annotations past their panel
   borders, and a second attempt stacked "toehold" directly against "strand
   displacement" and ran "input strand" through the strand it names. The plate
   was re-spaced — wider catalogue boxes at a wider pitch, the displacement label
   set as two right-aligned lines lower beside its arrow, the input label moved
   below its strand, the reporter note shortened — and re-rendered until the
   measurement showed 8pt throughout and the page read cleanly in grayscale.
6. **Ragged-right columns.** New matter tables first used a locally defined `L`
   column type; the repository already defines `P` for this in
   `tex/textbook/preamble.tex`, which the book loads, so the local definition was
   removed and the tables use `P`.

## Limitations

- One agent performed this review. It is not peer review, specialist review, a
  reader study or an accessibility audit.
- Chapter companion code was executed through its tests, not audited line by
  line. Passing tests are evidence about those tests.
- No new training run, hardware measurement or biological experiment was
  performed, and none is claimed.
- The remaining open gates are listed in PUBLICATION_READINESS.md.
