# LaTeX-first textbook revision

This is a new Chapters 1–3 review candidate, not a promotion of Chapter 3 into
the accepted cumulative edition. Chapters 1–2, their accepted build inputs,
and the standalone Chapter 3 review remain unchanged. Independent specialist
review and cumulative acceptance remain open; Chapter 4 onward is planned.

## What changed

The new entry point is [evolutor-textbook.tex](tex/evolutor-textbook.tex).
It directly includes the accepted chapter sources and a separately editable
[Chapter 3 manuscript](tex/textbook/ch03.tex). Future revisions are authored
in LaTeX; the build never converts Markdown into prose.

An original worked opening follows x = 2 and w = 3 through a = wx and
L = a²/2, then derives separate input and parameter sensitivities. Native
TikZ distinguishes forward values from reverse sensitivities. Updating only
w with learning rate 0.01 gives w = 2.88 and L = 16.5888; the text explains
why this local example is not a general optimization guarantee. The chapter
retains twelve reviewed vector figures, numerical diagnostics, twelve worked
exercises, and its source/evidence ledger.

The shared [textbook standard](TEXTBOOK_STANDARD.md) requires concrete
examples, derivations, executable checks, limitations, and original geometric
illustrations. The general build-from-scratch pedagogy is informed by
Sebastian Raschka's book; prose and illustrations are original.

## Reproduce and review

```sh
make -f textbook.mk textbook-check
make -f textbook.mk textbook
python3 scripts/build_textbook_plan.py --check
python3 -m pytest
python3 scripts/review-textbook-pdf.py output/pdf/evolutor-textbook.pdf build/textbook/review
```

Use Python 3.10+, pytest, the existing numerical dependencies including PyTorch,
XeLaTeX/latexmk, TeX Gyre Pagella and Heros, TikZ, DejaVu fonts, librsvg and
Poppler. The page review helper additionally needs Pillow. Build output stays
under build/ and output/pdf/; generated PDFs are not new acceptance records.

The source checker verifies 180 prior recorded source hashes and the old
standalone PDF hash, checks the native/vector inputs, and independently checks
the scalar loss, gradients, update and finite difference. The build rejects
overfull boxes, missing glyphs and unresolved references. Every page is
rendered; contact-sheet and full-size figure inspection supplement the
automated word-bound audit. Legacy math-font control bytes in extracted XML
are sanitized for parsing only; no PDF glyphs or geometry are discarded.

This is author-agent technical/editorial review, not independent scientific
certification. It is a partial editorial revision: accepted Chapters 1–2
are retained, and Chapter 3 combines retained reviewed material with a new
worked opening and native authoring surface.

## Planning without rewriting history

The historical build_deep_plan.py is a frozen accepted input. Its old roadmap
still calls Chapter 3 planned, while the accepted repository had moved to a
standalone review. The new build_textbook_plan.py layers the current review
status on that generator and changes only ROADMAP.md. Tests retain its old
validation behavior and ensure the overlay cannot mark Chapter 3 accepted.
book/book.json still contains only the two accepted chapters.

Next: obtain specialist review of Chapter 3, close cumulative acceptance,
then author Chapter 4 in LaTeX. No trained DOGMA/Hermon DNA model or empirical
architecture superiority is established by these teaching examples.
