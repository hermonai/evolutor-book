# Publication policy and remaining gates

Updated 18 October 2026. The active manuscript contains all 52 planned chapters.
It is a complete-range review candidate, not an accepted publication edition.
GitHub source publication is distinct from scientific/publication acceptance.

## Active and historical editions

The complete candidate uses tex/convergence/book.tex and
`python3 scripts/build-convergence.py --through 52`. Its current guide is
CURRENT_MANUSCRIPT.md, with chapter-level sources in CHAPTER_STRUCTURE.md.
BOOK_PLAN.md, book/book.json, accepted opening records and earlier production
reports retain their historical meaning. `make pdf` still checks the frozen
opening edition; do not repurpose that acceptance gate for new sources.

Keep one active manuscript. Do not restart another parallel beginner edition
or regenerate authored LaTeX from Markdown. Existing historical sources/PDFs
remain preserved; no blanket cleanup, history rewrite or tag movement.

## Before an accepted release

- Reproduce chapter fixtures and literal listings; run all tests without
  concurrent PDF builds. Verify source, dependency and PDF identities.
- Read every chapter, proof, example and exercise; resolve notation, transition,
  bibliography, glossary and index issues across the complete book.
- Inspect final rendered pages at readable size, in color and grayscale.
  Compilation alone cannot establish diagram clarity or editorial quality.
- Obtain appropriate external specialist and intended-reader review. A second
  AI-agent pass is useful but is not independent scientific peer review.
- Audit quotations, citations, illustrations, source redistribution and data
  rights. The repository has no general reuse license; do not invent one or
  change authorship without the owner's decision.
- Review accessible structure, text alternatives, navigation and publication
  formats. The current PDF is not claimed tagged, PDF/UA-compliant or an EPUB.
- Rebuild and review changed material, then record acceptance against exact
  final source/artifact hashes and obtain explicit human release authorization.

Use [the Claude prompt](docs/CLAUDE_PREPUBLICATION_REVIEW_PROMPT.md) for a
structured local review and bounded corrections. Track unresolved production
integrations and empirical claims separately; a durable engine, hardware result,
trained genomic finding or AGI result is not a prerequisite to explaining its
research contract, but must not be described as already demonstrated.

The author's 18 October request authorizes pushing the completed review work
to GitHub. It does not authorize a final accepted release, main-branch merge,
license choice or automatic future pushes by a reviewing agent.
