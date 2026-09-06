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
