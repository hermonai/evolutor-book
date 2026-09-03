# TXT graph standard

The canonical diagrams in this book are UTF-8 `.txt` graphs. They are designed to remain readable in a terminal, a Git diff, an ebook source tree, and an accessibility-oriented text workflow.

## Required structure

Every graph must contain:

1. a stable diagram ID and title;
2. a one-sentence scope statement;
3. a legend that defines node, boundary, and edge meanings;
4. named nodes rather than unlabeled shapes;
5. typed edges whose labels say what crosses the edge;
6. explicit feedback, failure, or evidence paths when they matter;
7. reading notes that explain the logic and its limits.

## Visual grammar

- `┌─┐`, `├─┤`, and `└─┘` define conceptual or operational nodes.
- `╔═╗` defines a hard evidence, system, or trust boundary.
- `→` carries data, state, or a declared transformation.
- `⇒` carries justification or evidence strong enough to support a scoped claim.
- `⇢` marks a proposal, hypothesis, or bridge that still requires validation.
- `↺` marks feedback, retry, correction, or recurrence.
- `⊣` marks rejection, blocking, or a failed gate.

Each graph states its own edge vocabulary; arrows never mean “therefore” by default. Layout communicates structure, but the reading notes carry the complete interpretation.

## Quality gate

A graph is manuscript-ready only when a reader can answer all of these questions from the graph and its notes:

- What enters and leaves the system?
- Which state persists, and which state is transient?
- Which transformations are defined, measured, or merely proposed?
- Where can a claim fail?
- Which evidence boundary prevents a stronger interpretation?
- What does the graph deliberately not assert?

Graph sources should normally stay within 118 columns. If the logic does not fit, split it into coordinated panels inside the same `.txt` file rather than shrinking labels into ambiguity.
