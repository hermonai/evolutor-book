# Findings

Severity: **defect** (demonstrably wrong or misleading for a reader), **risk**
(likely to mislead or to break reproducibility), **preference** (editorial
choice), **gate** (needs evidence or a decision this pass cannot supply).
Page numbers are standalone review-PDF pages unless marked "book p." (printed
folio of the 643-page cumulative candidate).

## Evidence and science

### F-ch23-a — defect — Hermon pilot read as a working system
- **Source:** `drafts/ch23/manuscript.tex`, pilot section; standalone pp. 10–16.
- **Evidence:** `drafts/ch23/results.json`. Hermon held-out accuracy
  0.523/0.523/0.539 over three seeds; random-label control 0.516/0.555/0.555;
  training loss moves 0.714 → 0.692 and stays at ln 2 = 0.6931 for every seed;
  CNN 0.711/0.578/0.883. Classes are balanced (label = length parity).
- **Problem:** the prose said the pilot tests that attention "can participate in a
  coherent trainable system". Held-out accuracy equal to the shuffled-label
  control together with training loss at ln 2 means the model did not fit its
  training set under this budget. It is a negative pilot.
- **Adjustment:** state the negative reading, cite the control, add an exercise on
  the ln 2 plateau, and reword the evidence-ladder sentence.
- **Disposition:** fixed. **Required:** rebuild, `--check`, re-inspect pp. 2, 10–16.

### F-ch22-a — risk — DOGMA pilot not read against chance
- **Source:** `drafts/ch22/manuscript.tex`; standalone pp. 2, 8–15.
- **Evidence:** `drafts/ch22/results.json`. DOGMA dual 0.5625/0.6016/0.5625 (mean
  0.576); GRU 0.479; MLP 0.510; CNN 0.84/0.64/0.52; DOGMA random-label 0.495. With
  128 balanced test records the chance standard error is √(0.25/128) = 0.044, so
  DOGMA sits about 1.7 SE above chance and the held-out losses are 0.66–0.68.
- **Adjustment:** add an explicit reading against chance and a new exercise 17.
- **Disposition:** fixed.

### F-ch24-a, F-ch25-a — risk — superseded single-run percentage in reader prose
- **Source:** `drafts/ch24/manuscript.tex` ("Design the experiment");
  `drafts/ch25/manuscript.tex` ("Diagnose negative results").
- **Problem:** both cited an old single-run 47.7 percent Hermon figure as "incoming
  package" provenance. Chapter 25 missed the teaching link: Chapter 23's pilot is
  exactly the negative result its flowchart diagnoses (loss at ln 2 → overfit a
  tiny subset next).
- **Disposition:** fixed in both chapters.

### F-global-agi — risk — capability framing
- The book's capability chapters (29, 51, 52) already separate hypotheses from
  evidence. The new epilogue keeps that discipline: it gives five questions any
  claim of general or superhuman capability must answer and says plainly that
  none of the book's results answers them. **Disposition:** addressed; no claim
  of AGI, superintelligence, novelty or influence was added anywhere.

## Reader-facing production text

### F-global-provenance — defect — package and coordinator wording in the book
- **Source:** manuscripts of Chapters 22, 24, 25, 32, 37, 38, 40, 42–52 and the
  *Sources* notes of Chapters 23, 25, 33–47.
- **Problem:** "incoming/supplied package", "the package's", "adoption map",
  "coordinator tests", "this batch" describe how the manuscript was produced, not
  the subject. Readers cannot act on them.
- **Adjustment:** rewrite each sentence to keep its scientific point (for example
  "a simpler check would accept …") and every statement about how deeply an
  external source was read. Production provenance stays in
  `research/integration/chNN/`. The prior note texts are archived verbatim in
  `docs/provenance/source-notes-2026-10-19.md`.
- **Disposition:** fixed; listed per chapter in `chapter-amendments.json`.

### F-global-stale — defect — finished chapters described as unfinished
- **Source:** ch10 ("upcoming Chapters 1–10 integration pass"); ch42 ("Chapter 36's
  unfinished physical allocation interface", "when Chapter 36 settles"); ch43
  ("stable Chapter 36 allocator" coordinator note); ch44 ("an unfinished Chapter
  39 runtime"); ch45 ("an unfinished Chapter 40 memory API"); ch49 ("absent
  Chapter 39/40/45 production adapters"); ch52 (separate-software-repository note).
- **Adjustment:** point to the finished chapters, or state plainly what is not
  implemented (for example production adapters).
- **Disposition:** fixed.

### F-global-review-pdf — preference — "compile this review PDF"
- ch13 and ch14 reproduction paragraphs. **Disposition:** fixed ("typeset the
  chapter on its own").

### F-ch03-a — risk — administrative material inside Chapter 3
- **Source:** `tex/textbook/ch03.tex`. A "Revision boundary" callout, 12
  `EVOD-03-Fn.` caption prefixes duplicating figure numbers, the untypeset
  expression "f(r)=2 when r is nonnegative …", a "Publication work still
  required" section and an Appendix B source-adoption ledger.
- **Disposition:** fixed. The removed section and ledger are preserved verbatim in
  `docs/provenance/ch03-source-ledger.md`; all primary links remain in the new
  "Sources and further reading" section. Chapter 3's candidate record is
  superseded, not rewritten (`SUPERSESSION.md`).

### F-ch01-a — risk — gate (author decision) — stale sibling-book plan in frozen Chapter 1
- **Source:** `tex/deep/ch01.tex` line 220: "Book I supplies the
  molecular-computation foundation. Its new Chapter 1 teaches a particular
  graph-search construction … a roadmap reference is not proof that a
  prerequisite chapter already exists."
- **Problem:** the companion *DNA Computing* volume is now a complete 32-chapter
  prepublication edition, so the paragraph is out of date. Chapter 1 is bound by
  a frozen acceptance record, so this pass did not edit it.
- **Proposed replacement (author to approve):** "The companion volume *DNA
  Computing: Molecular mechanisms, algorithms and evidence* develops computation
  with DNA from first principles, beginning with Adleman's graph-search
  construction and its limits. This book does not depend on it. Readers who want
  the molecular background for the epilogue can read it alongside Part~I."
- The new preface already states the correct relationship, so the stale
  paragraph is now the only conflicting text. **Disposition:** open.

### F-ch47-order — preference — exercises after the closing bridge
- `drafts/ch47/manuscript.tex`: "Terms and the application boundary" (l. 271)
  precedes "Twelve worked exercises" (l. 280); other chapters put exercises
  before the bridge. **Disposition:** open; low priority.

## Book architecture and typography

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| F-global-front | risk | Title page read "Continuous integration review candidate"; the book opened with two administrative pages and no preface | Fixed: title page with edition and rights notice, preface, "How to use this book" |
| F-global-toc | preference | 14-page section-level contents with no overview | Fixed: one-page "Contents at a glance" before the full contents |
| F-global-matter | risk | No epilogue, biology primer, notation table or evidence-class reference | Fixed: epilogue, Appendices A–C (biology for computing readers, notation, evidence classes) |
| F-global-guides | preference | Chapters had no stated goals or summaries | Fixed: "In this chapter you will" and "Key ideas" boxes injected by the builder from `tex/convergence/chapter-guides.json`; chapter sources unchanged |
| F-global-parts | preference | Part pages carried only a title | Fixed: guiding question, orientation and chapter list per part |
| F-global-plates | risk | `\Plate` scaled every figure to the line width, so small plates printed with oversized type | Fixed: wide plates shrink to the measure; small plates grow by at most 1.15× |
| F-global-bib-dup | risk | The same arXiv paper appeared up to three times (abs, html and pdf views; v1/v2) | Fixed: arXiv identity normalisation in the builder, with a test; DOIs still take precedence |
| F-global-keyideas | defect (introduced and fixed in this pass) | Key-ideas boxes split across pages (book pp. 236–237, 267–268 in an intermediate build) | Fixed: the box is unbreakable |
| F-global-plate-stack | defect (introduced and fixed in this pass) | Measuring plates in a horizontal box put Figure 13.5's legend line beside its plot instead of below it; `\linewidth`-relative plots (Figures 9.6, 20.2) then grew | Fixed: plates are measured in a `varwidth` box at the real line width; Figure 13.5 matches its standalone layout and every chapter keeps its page count |
| F-global-notes | preference | 21 chapters' source notes were unnumbered *chapters* in the book: each forced a new page and a chapter-level contents entry | Fixed in derived copies only: they are now sections; the book shrank from 658 to 643 pages |

## Reproducibility

### F-build-stale-aux — risk — standalone builds fail on stale auxiliary files
- **Evidence:** `drafts/chNN/build.py` failed with `! Undefined control sequence
  \@LN@col` for Chapters 22, 23, 25, 32–38, 42, 45, 46 and 47. The cause was a
  `build/chNN/review.aux` left by an earlier build (dated 6, 10 or 17 October)
  that references a macro the current preamble no longer defines.
  A failed rebuild leaves the previous PDF in `output/pdf/`, so `--check` can
  still pass against stale bytes.
- **Workaround used:** each stale aux was moved (not deleted) to
  `tmp/recovered-aux-2026-10-19/` and the chapter rebuilt cleanly.
- **Proposed fix:** make the chapter builders delete or regenerate `review.aux`
  when the preamble hash changes, and make a failed latexmk run fail the
  build loudly. **Disposition:** open (builder change, not made here).

### F-toolchain — gate (information) — TeX Live 2025 and 2026 outputs differ
- Superseded standalone PDFs of Chapters 10, 13, 14, 22–38, 42, 45, 46 and 47 were
  TeX Live 2025 builds (xdvipdfmx 20250205); all rebuilt PDFs use TeX Live 2026.
  Chapter 36 page 6 differs only because Figure 36.3's note label is placed
  differently; its source hash is unchanged. Recorded in
  `chapter-amendments.json`. **Disposition:** recorded; recheck figures if the
  toolchain changes again.

## Gates this pass could not close

| ID | Gate | Why |
|---|---|---|
| G-grayscale | Grayscale inspection of every page; full-size views of every dense figure | Colour contact sheets (45–50 dpi) covered all pages; these are navigation, not proof of label legibility |
| G-specialist | Independent biology, DNA-computing and ML specialist review | Agent review is not peer review |
| G-reader | Reader study for the new front matter and part openers | Not available to an agent |
| G-rights | Citation, quotation and artwork rights audit; licence decision | The title page states this is an open gate; no licence was invented |
| G-a11y | Tagged PDF / PDF/UA, alt text, EPUB | Not validated; not claimed |
| G-ch01 | Author decision on F-ch01-a | Frozen record |
