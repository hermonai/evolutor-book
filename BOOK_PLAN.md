# Evolutor: undergraduate-first architecture

Status: Chapter 1 internally reviewed development draft; all later units remain planned. No learner study, independent expert certification or new research-model experiment is claimed. Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json). See [Chapter 1 storyboard](research/undergraduate-ch01-storyboard.md) for the six produced figures.

Target taxonomy: **DOGMA = non-Transformer DNA-native architecture + DOGMA Engine; Hermon DNA = Transformer-based DNA architecture + Hermon DNA Engine; Evolutor = research/theory/runtime above both.** These are research targets, not implementation evidence. See [taxonomy and lineage](research/architecture-taxonomy.md). Stable EVOU IDs differ from printed numbers after EVOU-11.

## Table of contents

### I · Why genomic computation?

1. **EVOU-01 — Programs, genomes and the question of Evolutor**. Why compare a genome with a program?

### II · Computation and machine-learning foundations

2. **EVOU-02 — Programs that choose and remember**. How can the same input produce a different answer after a different history?
3. **EVOU-03 — Machine learning with one tiny model**. How can examples help set a rule's adjustable numbers?
4. **EVOU-04 — Data, uncertainty and fair evaluation**. Why can a model look good and still fail on new examples?
5. **EVOU-05 — Vectors, matrices and tensors as data containers**. How can one rule process several measurements together?
6. **EVOU-06 — Slopes, gradients and improving a prediction**. Which small change would reduce the error?
7. **EVOU-07 — Neural networks built one layer at a time**. Why put simple transformations in layers?
8. **EVOU-08 — A complete small training loop in PyTorch**. What changes during training, and what stays fixed during inference?

### III · How sequence models work

9. **EVOU-09 — Tokens, embeddings and predicting the next symbol**. How do written symbols become numbers a model can use?
10. **EVOU-10 — Recurrence: remembering one step at a time**. How can a model carry something from the previous symbol?
11. **EVOU-11 — Gates and state-space models**. What should a compact state keep or forget?
12. **EVOU-41 — Strong recurrent baselines and valid scans**. Which familiar mechanisms could already explain a candidate's behavior?
13. **EVOU-12 — Attention as a weighted lookup**. Which earlier symbol should matter now?
14. **EVOU-13 — From one attention head to a Transformer**. How do small attention operations form a useful model?
15. **EVOU-14 — Caches, retrieval and external memory**. Why keep earlier work, and when should a system look something up?

### IV · From biology to genomic computation

16. **EVOU-15 — If/else, dispatch, plugins and dynamic routing**. What already selects only part of a program?
17. **EVOU-16 — Mixture of experts and learned routing**. Can the choice of a module itself be learned?
18. **EVOU-17 — Source code, compilers, runtimes and interfaces**. What happens between writing a program and running it?
19. **EVOU-18 — Services, databases, protocols and scheduling**. Why does serving several requests need more than a model?
20. **EVOU-19 — Baselines, oracles and resource-matched experiments**. What would count as a fair improvement?
21. **EVOU-20 — Regulation, expression and different timescales**. What changes within a cell, and what changes across generations?
22. **EVOU-21 — Analogies that can fail**. What remains after comparing a biological idea with existing software?
23. **EVOU-22 — Learning parameters and changing structure**. How does changing a number differ from changing a program?
24. **EVOU-23 — Development as building a representation**. Can a compact description construct a larger program?
25. **EVOU-24 — A minimal genomic-computation hypothesis**. What precise system are we proposing to test?
26. **EVOU-25 — Classes, interfaces and a UML model**. How can the software structure express the proposed rules?
27. **EVOU-26 — From a request to an expression trace**. Who talks to whom during one request?
28. **EVOU-27 — Traces, credit and explanations**. Which component deserves credit, and what can a trace actually explain?
29. **EVOU-28 — Structural proposals and their lifecycle**. When may a proposed edit become active?

### V · DOGMA: non-Transformer DNA-native architecture

30. **EVOU-42 — DOGMA: candidate primitives and state semantics**. Can structured state support DNA-native computation without Transformer attention as its organizing mechanism?
31. **EVOU-43 — DOGMA regulation and expressed transformations**. What exactly does regulation select and expression execute?
32. **EVOU-44 — DOGMA modular state, locality and structural memory**. Does modular state help beyond a single carried vector?
33. **EVOU-45 — DOGMA strands, complements and dual-state proposals**. Does a paired representation improve a declared task?
34. **EVOU-46 — DOGMA traces and structural adaptation**. Does a trace reveal useful mechanism beyond ordinary activation logs?

### VI · Hermon DNA: Transformer DNA architecture

35. **EVOU-47 — Hermon DNA: a Transformer sequence model**. What remains recognizably Transformer-based before DNA-specific changes?
36. **EVOU-48 — Hermon DNA: DNA-aware Transformer hypotheses**. Which DNA-specific change adds value beyond the plain Transformer?

### VII · Training systems and shared contracts

37. **EVOU-29 — Training a candidate Evolutor model**. Does the proposed mechanism help beyond the taught baselines?
38. **EVOU-49 — Shared PyTorch experiments without false equivalence**. What can both model families share without hiding their differences?
39. **EVOU-50 — DOGMA training: sequential, chunked and scan forms**. When can a candidate transition be parallelized without changing its meaning?
40. **EVOU-30 — An inference runtime with clear boundaries**. Which parts must run for one prediction?
41. **EVOU-31 — Model identity, formats and checkpoints**. How do we know which model produced this result?
42. **EVOU-32 — Managing recurrent state, KV and external memory**. How can several requests share hardware without sharing private state?

### VIII · DOGMA inference engine

43. **EVOU-51 — DOGMA Engine: state construction and native steps**. How does the engine execute the model's exact state machine?
44. **EVOU-52 — DOGMA Engine: isolated state pools**. How can requests share hardware without sharing state?
45. **EVOU-53 — DOGMA Engine: checkpoint, restore and prefix state**. Can a saved state resume the same computation?
46. **EVOU-54 — DOGMA Engine: scheduling state transitions**. Which independent requests can take a step together?

### IX · Hermon DNA inference engine

47. **EVOU-55 — Hermon DNA Engine: prefill and attention decode**. Why does one Transformer request have two execution phases?
48. **EVOU-56 — Hermon DNA Engine: paged KV and prefix sharing**. How do logical positions map to reusable physical pages?
49. **EVOU-57 — Hermon DNA Engine: continuous batching and precision**. How do request phases and numerical precision change serving?

### X · Unified Evolutor runtime

50. **EVOU-58 — Evolutor runtime above two distinct engines**. What belongs in a shared runtime rather than either engine?
51. **EVOU-59 — Hybrid memory as a testable Evolutor proposal**. When should information be compressed into state or kept addressable?
52. **EVOU-33 — Batching, queues and latency**. Why can throughput improve while some users wait longer?

### XI · Industrial engineering

53. **EVOU-34 — Parity, profiling and optimization**. How do we make it faster without changing what it computes?
54. **EVOU-60 — Measured bottlenecks, native kernels and model formats**. Which optimization is justified by profiling and semantic parity?
55. **EVOU-35 — Serving, observability and safe rollback**. How do we observe and recover a running service?

### XII · Applications and their evidence

56. **EVOU-36 — Failed ideas as a source of knowledge**. What should we learn when the idea does not win?
57. **EVOU-37 — DOGMA and Hermon DNA: taxonomy, lineage and comparative evidence**. Which architectural distinction survives beyond a project name?
58. **EVOU-61 — Applications that stress different kinds of memory**. Which tasks reveal compression and addressability tradeoffs?
59. **EVOU-38 — Transfer, continual learning and populations**. Does an improvement survive a changed task?

### XIII · Toward AGI: operational claims

60. **EVOU-39 — AGI claims and an operational scorecard**. What does a narrow result allow us to say about general intelligence?

### XIV · Failures, limits and open problems

61. **EVOU-40 — Capstone: failures, limits and a reproducible research argument**. Can another reader reproduce both the result and the boundary of the claim?

Chapter count is provisional, not a promise of one semester. These are small teaching units, not equal-length lectures. The full two-book path can span multiple courses. No chapter requires an external prerequisite textbook.
