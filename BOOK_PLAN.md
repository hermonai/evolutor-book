# Book plan

## Working title

**Evolutor: Genomic Computation - From Regulation and Expression to Machine Intelligence**

## Scope decision

Book I supplies DNA biology, classical DNA computing, and common ML foundations. This volume uses that material but does not repeat a second foundations textbook. Its center is GCS: persistent typed structure, context-dependent regulation, selective expression, traces, and verified structural change.

## Proposed macro structure

### Part I - The question and the evidence boundary

1. What would it mean for a program to behave like a genome?
2. Biology, inspiration, formal model, ML architecture, and runtime
3. The correction record as method
4. Architecture names, lineages, and claims

### Part II - Genomic Computation Systems

5. The tuple \((\Sigma, \mathrm{Genome}, \mathrm{Reg}, \mathrm{Expr}, \mathrm{Evo})\)
6. Typed genomes and the core codon language
7. Compilation to a dependency substrate
8. Regulation, expression plans, and machine state
9. Mechanistic traces and provenance

### Part III - Semantics, safety, and universality

10. Small-step expression semantics
11. Type and policy preservation
12. Universality: construction, assumptions, and proof obligations
13. MiniEvolutor as an executable specification

### Part IV - Complexity and selective execution

14. Expression complexity and the cost model
15. Local interaction models and light cones
16. Sparse pointer retrieval: what the separation does and does not show
17. Regulation depth and pointer chasing
18. Adversarial review of the hierarchy claim

### Part V - Learning and structural evolution

19. Safe hypothesis classes and compute-regularized objectives
20. Trace-restricted search
21. Verified local edits and invariant preservation
22. Descent guarantees versus learning capability

### Part VI - PyTorch semantic foundations

23. Shared DNA tokenization, data, losses, and artifacts
24. Training/inference parity
25. Intervention-based causality
26. Capacity controls and experimental records

### Part VII - Transformer DNA research line

27. A standard causal Transformer reference
28. Reverse-complement and strand-aware hypotheses
29. Attention, retrieval, KV state, and long-context inference
30. Proposed target name: DOGMA, with lineage qualification

### Part VIII - Non-Transformer DNA research line

31. GRU and state-space references
32. Selective recurrence, regulation, and structured state
33. Expression and trace-aware models
34. Proposed target name: Hermon DNA, with lineage qualification

### Part IX - Controlled comparison and long context

35. Parameter, width, state, and compute matching
36. Retrieval versus accumulated-state tasks
37. Genomic prediction and leakage-aware splits
38. Negative results, replication, and stop conditions

### Part X - Toward a genomic computer

39. Double-strand and complementary computation
40. Genomic graphs, geometry, and intermediate representations
41. Training foundations and trace-aware autograd hypotheses
42. Inference engines and a possible common serving protocol
43. Database/query-engine analogy and its failure points
44. Open problems and falsification agenda

## Chapter dependency map

[E14 — Evolutor book dependency map](book/diagrams/e14-book-dependency-map.txt) is the canonical dependency graph. It exposes the formal and neural branches, shared validation boundary, blocked inferences, and the point at which a compiler/runtime proposal becomes justified.

## Text-diagram inventory

Canonical UTF-8 `.txt` graphs cover the GCS tuple, compiler pipeline, expression machine state, trace/evolution loop, theorem dependency graph, training/inference split for both neural families, long-context capability map, historical versus target names, and a possible genomic IR/runtime stack. They use stable IDs, legends, named nodes, typed edges, failure paths, and reading notes under the [TXT graph standard](book/diagrams/TXT_GRAPH_STANDARD.md). See [the inventory](book/diagrams/INVENTORY.md).

## Completion gates

Each chapter must distinguish source theory from new proposal, link nontrivial claims to the ledger, state theorem assumptions and proof status, map formal equations to executable semantics where possible, and close with “What this chapter established” and “What remains unverified.”
