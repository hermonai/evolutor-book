# Proof obligations

## P0 - Definitions before theorems

- Give a complete grammar, value domain, store typing, and evaluation relation.
- Separate compile time, regulation time, expression time, and evolution time.
- Define a trace's relationship to actual transitions.

## P1 - Preservation

- Prove progress or state why stuck states are permitted.
- Prove preservation for each transition and primitive.
- Define policy safety semantically, not only as a template type.

## P2 - Universality

- Specify the unbounded resource that permits Turing completeness.
- Provide configuration encoding/decoding and one-step simulation lemmas.
- Clarify repeated expression versus one expression run.

## P3 - Expression cost

- Give cost to gate evaluation, primitive evaluation, worklist operations, and I/O.
- State whether `EC` counts revisits or distinct nodes.
- Prove scheduler overhead is linear or include it in the bound.

## P4 - LIM separation

- Define synchronous and asynchronous variants separately.
- Fix where output is produced and what a round costs.
- State plainly that the lower bound does not cover global attention, indexed memory, or arbitrary algorithms.

## P5 - Regulation depth

- Define the boundary information available per stage.
- Prove a stage-to-communication simulation with exact round and message bounds.
- Use a cited pointer-chasing lower bound whose parameters actually contradict the simulated protocol.
- Repair off-by-one conventions between `PC_k`, stages, and hierarchy classes.

## P6 - Learning

- Define a finite encoding for genomes and edits.
- Replace average support with a valid bound on the editable union or distribution-dependent quantity.
- Distinguish monotone search on training objective from generalization or efficient learnability.

