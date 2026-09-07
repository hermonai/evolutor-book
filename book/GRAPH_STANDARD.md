# Shared graph and illustration standard

Active deep edition: use the deep-prefixed inventories under pedagogy/ and CHAPTER_1_OUTLINE.md. Legacy renderer and Chapter 1/2 details below describe preserved implementations, not constraints forcing new figures into old layouts. Abstraction is allowed; declare its relationship to the molecular, mathematical or software mechanism. No deep artwork is produced by the planning milestone.

Canonical top-level diagrams are UTF-8 .txt records with stable IDs, named nodes, typed Unicode arrows, evidence boundary, reading notes and failure path. They are not decorative ASCII box art. DATA → means transformation/dependency, not empirical proof. CONTROL ⇢ means a gate or review. HYPOTHESIS uses a dashed edge and must be explicitly labeled; it never inherits certainty from line style.

The renderer in scripts/render_graphs.py produces SVG from these records. Generated SVGs are committed for browser viewing, with title/description and text labels; canonical text remains the accessible semantic alternative. Validate node IDs and edge endpoints before rendering. Top-level maps use two lanes, prerequisite arrows, cross-lane checks and feedback where appropriate. A diagram need not force feedback onto an acyclic process.

Biological illustrations will use editable SVG sources and source-reviewed scientific notation: strand polarity, molecular composition, covalent versus pairing interactions, distinct intermediates, and readable labels. UML is appropriate for software classes, sequences and state machines, not for chemical structures. Every figure needs a stable ID, caption, legend, source/provenance and evidence scope.

The supplied reference images guide navy headings, whitespace and consistent typography. Do not copy their chemical drawings or assertions as authority. No generative raster image is needed for these conceptual maps. Future chapter illustrations require a biological/math review and visual inspection at final publication size, including grayscale legibility.

Use color as reinforcement only. Re-render after edits; do not manually alter a generated SVG. Keep graph captions outside the image in LaTeX and stable alt text in the source register.

Chapter 2 scientific figures use `LAYOUT: chapter02` with three or more explicitly named semantic nodes and typed edges. They are rendered by `scripts/render_chapter02.py` through the standard renderer. Unlike research maps, they do not require six boxes or seven edges: chemical orientation and relation types determine the drawing. The canonical TXT must enumerate the actual relations shown; the specialized renderer validates the supported node/edge contract rather than silently inventing relations.

## Chapter 1 production conventions (2026-09-06)

These conventions were refined after actual SVG-to-PDF rendering of both openings.

| Figure class | Meaning to preserve | Visual convention |
|---|---|---|
| Biology textbook illustration | Physical objects versus their written descriptions | Clearly label schematic level; connected chain is not movement; omit unintroduced chemistry explicitly |
| Process storyboard | Object identity and permitted change | Number stages; preserve counter identities; distinguish unchanged objects, movement and absence of creation/consumption |
| Mathematical diagram | Quantity versus carrier | State the reading convention; derive notation from a hand-worked case |
| Software UML | Standard engineering relations | Teach the relevant UML symbols before use; do not draw software as molecules |
| Introductory data-flow / architecture | Information use versus physical action | Solid directed connectors with a stated meaning; output word is not a live device action |
| Research evidence diagram | Proposal, comparison, test and possible rejection | Keep hypotheses visibly unmeasured; dashed analogy links are not causal or execution arrows |

Use a restrained navy/blue palette, pale panels, amber for an alternate/boundary condition, and dark labels. Color never carries the distinction alone. At 900 source units over the publication text width, 20–24-unit labels remain readable; inspect the actual PDF, not just the source dimensions. Avoid tiny labels to rescue a crowded panel.

Every publication figure keeps editable SVG, a Unicode TXT semantic companion, title/description metadata, caption, evidence and limitation. No ASCII box art and no decorative raster illustration. The Chapter 1 generator is intentionally small: labeled panels, tokens, schematic strands, text and typed arrows. Draw connectors after panels where required so arrowheads are not occluded.

Keep a caption with its figure. Check identity, arrow direction and meaning separately from typography. Static multi-frame artwork does not count as an exported animation. Internal illustration review is not independent scientific certification.
