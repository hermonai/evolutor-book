# Chapter 14: Typed genomic computation systems

Author storyboard approved before prose, 24 September 2026. This is an internal authoring decision, not independent scientific approval.

## 01-types

Question: Why are equal dimensions not enough?

Two 2x2 arrays with row and column semantic labels swapped; explicit transpose edge and incompatible direct edge. Caption: axis meaning belongs in the contract. Risk: metadata does not prove true data provenance.

Editable TikZ source plus semantic TXT companion. Labels, geometry and line patterns remain meaningful in grayscale.

## 02-genome

Question: What is a computational gene?

UML-style class decomposition of immutable typed instruction, ordered genome, regulator and external parameter/state owners. Multiplicity and ownership labels; biology analogy confined to caption. Risk: not a production Evolutor implementation.

Editable TikZ source plus semantic TXT companion. Labels, geometry and line patterns remain meaningful in grayscale.

## 03-step

Question: How does expression update state?

Concrete affine-plus-add execution with previous state, proposed output and next-state version; distinct read/data/commit arrows. Caption: successful typed execution precedes commit. Risk: transactional memory is reference semantics, not durability.

Editable TikZ source plus semantic TXT companion. Labels, geometry and line patterns remain meaningful in grayscale.

## 04-rejection

Question: Where are malformed genomes rejected?

Instruction-level trace of valid register environment, followed by axis mismatch, duplicate output, undeclared owner and missing input counterexamples. Caption: reject before numeric execution. Risk: rejecting these errors is not a safety proof for arbitrary plugins.

Editable TikZ source plus semantic TXT companion. Labels, geometry and line patterns remain meaningful in grayscale.

## 05-trace

Question: What must replay bind?

Genome version, parameters, input, regulator decision and state snapshot join at an expression event; output and state digest follow. Caption: event fields are evidence, not the computation itself. Risk: no claim that a minimal reference trace is a secure audit log.

Editable TikZ source plus semantic TXT companion. Labels, geometry and line patterns remain meaningful in grayscale.
