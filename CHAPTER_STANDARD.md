# Deep-edition chapter production standard

Active from 7 September 2026. This adapts lessons from the two rendered undergraduate prototypes; the old standard remains in Git. The new target is depth with straightforward explanation, not prerequisite-free prose.

## Reasoning and content

1. Inspect the active branch, manuscript status, source history and dependency closure.
2. Read primary sources to the depth required for each claim. Record access depth, edition/date and exact evidence; an abstract is not a full mechanistic reconstruction.
3. Approve a figure-specific storyboard before prose. Identify the question, objects, semantics, changing/unchanged elements, caption and scientific risk.
4. Open with the subject and a meaningful technical problem. Assume declared mathematics/programming; teach domain-specific mechanisms without elementary filler.
5. Use abstraction wherever it clarifies the argument. Explain the map from example to formal object, what is preserved, and what is omitted. Define symbols, units, shapes and timing conventions before relying on them.
6. Derive important equations and proofs through explicit intermediate reasoning. Include a worked example and an interpretation; do not substitute a figure for the derivation.
7. Introduce algorithms and reference implementations only when they serve the subject. Include code from actual tested files, generate numerical tables from declared computations, and test independent expected cases. PyTorch is justified by the model, not branding.
8. Produce original editable vectors and semantic Unicode TXT companions. Use scientific notation for molecules, UML for software, memory layouts for state and timelines for execution. No ASCII box art.
9. Supply conceptual, derivation/proof, algorithmic, coding and experimental/systems-design exercises where appropriate, with worked solutions or explicit open-problem rubrics.
10. Keep a selective glossary, substantive index, cross-references and primary bibliography. Audit notation and domain acronyms; do not require a glossary entry for every ordinary word.
11. Review subject accuracy, mathematics, implementation, sources and explanation separately. Author-agent role reviews must not be represented as independent specialists or reader studies.
12. Compile the distinct deep-edition LaTeX entry point and render every page. Inspect actual print-size labels, grayscale, captions, equation/code layout, references and index. Fix warnings and re-render changed pages.
13. Record claims, negative results, limitations and next scope. Run full regressions and preservation checks. Commit only the scoped work and publish only when authorized.

These are gates, not a rigid table of contents. A long proof, a mechanistic atlas chapter and an engine implementation can have different structures.

## Production lessons retained

### Mechanism-first textbook illustrations

Whenever a relationship is difficult to follow in prose, show the mechanism itself. For biology, use scientifically grounded structures, strand orientation, spatial organization and successive reaction states. For algorithms, use graph structure, evolving state, explicit transformations and directed data or gradient flow. A panel containing only a restated paragraph is not a substitute for an explanatory illustration.

Use an original, professional textbook visual language: editable SVG, consistent typography and spacing, restrained semantic colors, labeled arrows, meaningful visual hierarchy, self-contained captions and semantic TXT companions. Render and inspect the artwork at its intended reading size. Biology diagrams must distinguish physical bonds from recognition and association; algorithm diagrams must distinguish control, data, state and evidence. Introduce molecular illustrations only when a biological mechanism is actually being explained, not as decoration for software.

The earlier page review found an arrow hidden by later-painted panels, a floating figure splitting a sentence, title hyphenation, awkward bibliography spacing and glossary drift. Check the final rendered page rather than assuming valid SVG or successful LaTeX implies clarity. Stable molecular identities and orientation matter more than a generic panel layout. Keep figures and captions together; carefully reviewed floats are acceptable.

Source-linked code must match literal outputs and numerical conventions. A biology drawing must not imply DNA acts without cellular machinery. Color reinforces labels and line styles, never replaces them. Animation-like static panels are not exported animations.

## Deep-edition acceptance

A technically capable reader should be able to reconstruct the mechanism, derive the important relationship, execute or trace the reference model, and distinguish evidence from hypothesis. Internal checks cannot establish that a real reader succeeds. Independent review, reader observation, source/rights auditing and accessible publication structure remain open release gates.

Chapters 1–2 supply deep production examples. See their production reports and source-bound review records under artifacts/deep/. Only the deep edition advances; the undergraduate prototype and previous PDFs are frozen.

## Repeatable production safeguards

Extract whole tested functions into printed listings; fragile line ranges can silently show the wrong code after an edit. Generate numerical tables from the same result artifact used by tests. Check each caption against the actual mechanism and asset, not just an existing filename. Keep physical molecule multiplicity distinct from digital set membership, and test representation boundaries independently.

Include a known failure or negative control when a diagnostic could otherwise pass vacuously. State masks, denominators, units and independence assumptions beside numerical claims. Extend cumulative releases with distinct entry points and filenames; retain prior review records unchanged and bind each new acceptance to all reused and newly reviewed inputs.

## Lessons from the canonical Chapter 1 production

Keep a comparison table header with its rows. Inspect literal separator characters inside SVG text helpers: a vertical-bar line splitter can accidentally turn a KV label into two lines. Mark molecular backbone continuity separately from base pairing. Show explicit UML guards, merge points, and dependency direction. Do not draw causal arrows between unrelated field categories. Static keyframes should expose a changing state, not merely highlight labels. Round generated geometry to a documented precision so different Python math libraries do not create meaningless artifact drift. Keep printed code at readable size, and verify bibliography navigation as well as citation closure. Bind acceptance to hashes of reviewed source and artwork; a passing old review must not certify new edits.
