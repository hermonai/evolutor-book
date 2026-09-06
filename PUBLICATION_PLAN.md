# Undergraduate publication plan

The new entry point is tex/undergraduate-evolutor.tex. Its manifest includes only tex/undergraduate/ch01.tex. Preserved old chapter files are never silently promoted.

## Rebuild

Run make pdf with the intended Python executable. The target checks the active manifest, derives glossary/terminology from the manuscript, generates six SVG/TXT pairs and the tested example trace, converts SVG to PDF and runs XeLaTeX through latexmk. The output uses a distinct undergraduate filename under output/pdf. The published snapshot of that exact file accompanies this milestone; future rebuilds may differ in PDF metadata.

Run make check-pdf and the full pytest suite. The new integration test also checks all six figure references, glossary, bibliography, index and the absence of missing references or box warnings. Dependencies are listed in README.

## Visual acceptance

Run scripts/review_undergraduate.py with Python and Pillow. It renders every page at 110 dpi with Poppler and produces numbered color/grayscale contact sheets in tmp/pdfs. Inspect every page and enlarge any uncertain figure or line. Do not equate a successful build with a successful page. Rebuild and re-render after meaningful changes.

The present preview contains a nine-page chapter plus front/back matter. It has no tagged-PDF structure; accessibility certification and independent reviewer/learner checks remain open.

## Publication boundary

Publish this coherent Chapter 1 milestone and supporting plans to origin/astra-undergraduate-rewrite only after checks and staged-diff review. Main, astra-rewrite and pre-reboot history stay unchanged. No automatic merge, force push, license change, deployment or research-engine implementation is included.

The final delivery provides the publication commit hash. CHAPTER_1_REPORT.md describes the content and verification; the commit containing that report is the authoritative release identity.
