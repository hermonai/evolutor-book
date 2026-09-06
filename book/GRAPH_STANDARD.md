# Shared graph and illustration standard

Canonical top-level diagrams are UTF-8 .txt records with stable IDs, named nodes, typed Unicode arrows, evidence boundary, reading notes and failure path. They are not decorative ASCII box art. DATA → means transformation/dependency, not empirical proof. CONTROL ⇢ means a gate or review. HYPOTHESIS uses a dashed edge and must be explicitly labeled; it never inherits certainty from line style.

The renderer in scripts/render_graphs.py produces SVG from these records. Generated SVGs are committed for browser viewing, with title/description and text labels; canonical text remains the accessible semantic alternative. Validate node IDs and edge endpoints before rendering. Top-level maps use two lanes, prerequisite arrows, cross-lane checks and feedback where appropriate. A diagram need not force feedback onto an acyclic process.

Biological illustrations will use editable SVG sources and source-reviewed scientific notation: strand polarity, molecular composition, covalent versus pairing interactions, distinct intermediates, and readable labels. UML is appropriate for software classes, sequences and state machines, not for chemical structures. Every figure needs a stable ID, caption, legend, source/provenance and evidence scope.

The supplied reference images guide navy headings, whitespace and consistent typography. Do not copy their chemical drawings or assertions as authority. No generative raster image is needed for these conceptual maps. Future chapter illustrations require a biological/math review and visual inspection at final publication size, including grayscale legibility.

Use color as reinforcement only. Re-render after edits; do not manually alter a generated SVG. Keep graph captions outside the image in LaTeX and stable alt text in the source register.

Chapter 2 scientific figures use `LAYOUT: chapter02` with three or more explicitly named semantic nodes and typed edges. They are rendered by `scripts/render_chapter02.py` through the standard renderer. Unlike research maps, they do not require six boxes or seven edges: chemical orientation and relation types determine the drawing. The canonical TXT must enumerate the actual relations shown; the specialized renderer validates the supported node/edge contract rather than silently inventing relations.
