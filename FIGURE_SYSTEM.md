# Shared textbook figure system

Status: production specification; no new publication artwork is delivered in this architecture milestone.

## Purpose before drawing

Every figure has a stable ID, reader question, storyboard, semantic source or companion, editable vector source, teaching caption, alt description and review record. The current inventories are [figures](pedagogy/figure-inventory.json) and [animation candidates](pedagogy/animation-inventory.json). Entries explicitly say when art is not drawn. A planned path is not a delivered asset.

TXT graphs remain Unicode semantic companions for machine readability, differences and fallback. Publication teaching figures should use richer SVG where that makes the mechanism easier to see. Do not force a molecule into six generic boxes to satisfy a graph template. Do not use ASCII box art. A dependency arrow means “teach before,” not physical causation.

## Visual grammars

Biology uses recognizable molecular objects, oriented strands, enzyme identities, physical labels, reaction steps and explicit non-scale warnings. Distinguish covalent connections, pairing interactions, sequence transfer and regulatory control. Do not render a polymerase as an unlabeled software component. Zoom in and back out so readers can reconnect parts with the whole.

Software uses actors, objects, messages, components, interfaces, state transitions and deployment nodes. Teach Unified Modeling Language (UML) symbols before using them. Use reproducible PlantUML or an equivalent editable source for UML. Classes are not instances; ownership is not a message; a return is not automatically an asynchronous call. A software database is not a protein.

Object figures answer “what is it?”; sequences answer “what changes?”; comparisons expose a distinction; architecture and UML expose responsibilities and interactions. Use the smallest grammar that answers the question.

## Shared palette and accessible distinctions

| Role | Color target | Non-color cue |
|---|---|---|
| DNA | Blue #1768A6 | DNA label and orientation marks |
| RNA | Red #B73549 | RNA label and distinct strand annotation |
| Protein / enzyme | Amber #A56A00 | Named shape and enzyme label |
| Regulation / control | Green #28764A | Explicit control verb and control endpoint |
| State / memory | Purple #7147A8 | State label, time label or storage outline |
| Software / system | Blue-gray #40576D | Standard component or object notation |
| Warning / failure | Red #B3261E | Warning word and cross/exception marker |
| Proposed analogy | Neutral gray | Dashed question-mark relation |

These are design targets, not measured accessibility certification. Measure text/background contrast in rendered artifacts; use dark text on light fills, not small white text on amber. Test grayscale. Do not encode meaning through color alone. Arrow styles must have a local legend; a dashed hypothesis arrow and an inhibitory relation must not be confused.

## Sequence and animation contract

For each keyframe record: objects before, changes, unchanged objects, movement, created objects, consumed objects. Preserve object positions and identities unless motion teaches the change. “Not applicable” is valid for a nonphysical software operation. Replication uses intact duplex → local opening → primers → extension → leading/lagging distinction → daughter duplexes. Do not show multiple inconsistent fork directions across frames.

Future animation directories contain storyboard.md, frame-NN.svg and machine-readable frame metadata. Static PDF selects the essential frames; an eventual interactive edition offers reduced-motion and static alternatives. No video export or working animation is claimed now.

## Caption and layout gates

Each final figure needs number, title, labels, direction marks, short explanatory caption, legend where necessary, and boundary note. Captions say what the learner should notice, not merely name the topic. A figure should be largely understandable without searching backward, but must not teach an unexplained vocabulary cluster by accident.

Use stable typography with readable labels at final print size, generous separation, and consistent margins. Split crowded figures into successive panels or figures. Review after embedding in a real page, not only the standalone SVG. Scientific correctness and visual clarity are separate checks, and both must pass.

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
