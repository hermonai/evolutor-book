# Canonical chapter production standard

Established after producing and rendering both undergraduate Chapter 1s on 6 September 2026. This records observed production lessons, not a template written before chapter experience.

## Required sequence

1. Inspect the branch, dirty state, approved title, prerequisites and preservation anchors.
2. Read the relevant redesign and source material. Record access depth: an abstract supports a narrower use than a fully inspected paper.
3. Approve a figure-specific storyboard internally **before prose**: question, prerequisite, objects, steps, caption, scientific risk and evidence. Internal approval is not independent validation.
4. Draft fresh around that visual sequence. Start with objects and a hand trace. Define every term before substantive dependence. Identify title/objective previews honestly.
5. Introduce symbols only after their quantities and operations are understood. The first worked example must be executable by hand.
6. Keep code optional when the entry contract does not require programming. Include printed code from actual tested files, generate tables from it, and test independently specified expected cases.
7. Generate editable vectors and semantic Unicode TXT companions. Do not treat a valid SVG as a reviewed illustration.
8. Supply recognition, boundary, application and critical-thinking exercises with answers. State the acceptable scope of open research responses.
9. Generate reciprocal glossary/section links from canonical definitions and add the print index. Audit prose, captions, code, exercises and answers, not just a vocabulary list.
10. Review separately as an introductory learner, a returning general reader and each relevant specialist perspective. Label author-agent role reviews honestly. Keep real learner and independent expert checks open.
11. Compile and render **every page**. Inspect final-size labels, grayscale distinctions, caption placement, page rhythm, references and index. Fix meaningful warnings and re-render changed pages.
12. Update the claims ledger, candid production report and next prerequisite-complete scope. Run all regressions, preserve earlier editions and inspect the staged diff. Push only the authorized branch; no implicit main merge.

## Lessons actually observed in Chapter 1

- Two course-level figure placeholders were too coarse for production. Six concrete figures per opening worked here, but six is not a quota for later chapters.
- A floating figure split a biological sentence. The introductory TeachingFigure macro now keeps artwork and caption together at the authored boundary. Later long figures may use carefully reviewed floats; no policy overrides actual page layout.
- An arrow generated before the next panel was painted over. Connectors must survive the complete drawing order; an XML test cannot detect every occlusion.
- A genotype picture could look like DNA acting alone. Put “cellular machinery required” and “conceptual, not measured” in the visual itself.
- Source-linked code exposed the importance of exact case: the returned word on must not become On in an answer.
- A glossary copied manually drifted after a definition-order correction. It is now generated from explicit Teach definitions with related-term links that do not recursively add glossary pages to occurrence lists.
- Optional code and biological reminders introduce narrow previews before later full treatments. Record that refinement; do not pretend the entire original prerequisite has been delivered.
- Title hyphenation and justified bibliography URLs needed correction despite a successful build.
- “All tests pass” is evidence about these contracts, not scientific novelty, readability, external endorsement or intelligence.

## Stable working assets

tex/undergraduate/preamble.tex defines the page system.
scripts/build_undergraduate.py contains the small original SVG primitives and deterministic data generation.
scripts/audit_undergraduate.py derives the glossary and first-sentence ledger.
scripts/review_undergraduate.py renders pages/contact sheets, including grayscale.
pedagogy/ch01-storyboard.json records the visual decisions.

Avoid expanding this into a general illustration platform before later chapters demonstrate a need.

## Acceptance and remaining external gates

The canonical template is an internally reviewed development standard. Actual novice observation, independent subject review and tagged-PDF/accessibility work remain separate gates. The current PDFs are not tagged and are not claimed PDF/UA compliant. A linked SVG description and readable print layout do not substitute for accessible PDF structure.
