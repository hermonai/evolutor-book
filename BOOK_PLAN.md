# Evolutor: undergraduate-first architecture

Status: planning only. No new chapters, finished figures, animations, experiments or reviewed learning outcomes are claimed. Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json); edit that source and regenerate.

## Table of contents

### I · From a familiar genome to a new question

1. **EVOU-01 — Programs, genomes and the question of Evolutor**. Why compare a genome with a program?
2. **EVOU-02 — Programs that choose and remember**. How can the same input produce a different answer after a different history?
3. **EVOU-03 — Machine learning with one tiny model**. How can examples help set a rule's adjustable numbers?
4. **EVOU-04 — Data, uncertainty and fair evaluation**. Why can a model look good and still fail on new examples?

### II · Learning the language of neural models

5. **EVOU-05 — Vectors, matrices and tensors as data containers**. How can one rule process several measurements together?
6. **EVOU-06 — Slopes, gradients and improving a prediction**. Which small change would reduce the error?
7. **EVOU-07 — Neural networks built one layer at a time**. Why put simple transformations in layers?
8. **EVOU-08 — A complete small training loop in PyTorch**. What changes during training, and what stays fixed during inference?

### III · Sequences and memory

9. **EVOU-09 — Tokens, embeddings and predicting the next symbol**. How do written symbols become numbers a model can use?
10. **EVOU-10 — Recurrence: remembering one step at a time**. How can a model carry something from the previous symbol?
11. **EVOU-11 — Gates and state-space models**. What should a compact state keep or forget?
12. **EVOU-12 — Attention as a weighted lookup**. Which earlier symbol should matter now?
13. **EVOU-13 — From one attention head to a Transformer**. How do small attention operations form a useful model?
14. **EVOU-14 — Caches, retrieval and external memory**. Why keep earlier work, and when should a system look something up?

### IV · Existing software before genomic abstractions

15. **EVOU-15 — If/else, dispatch, plugins and dynamic routing**. What already selects only part of a program?
16. **EVOU-16 — Mixture of experts and learned routing**. Can the choice of a module itself be learned?
17. **EVOU-17 — Source code, compilers, runtimes and interfaces**. What happens between writing a program and running it?
18. **EVOU-18 — Services, databases, protocols and scheduling**. Why does serving several requests need more than a model?
19. **EVOU-19 — Baselines, oracles and resource-matched experiments**. What would count as a fair improvement?

### V · Borrowing from biology carefully

20. **EVOU-20 — Regulation, expression and different timescales**. What changes within a cell, and what changes across generations?
21. **EVOU-21 — Analogies that can fail**. What remains after comparing a biological idea with existing software?
22. **EVOU-22 — Learning parameters and changing structure**. How does changing a number differ from changing a program?
23. **EVOU-23 — Development as building a representation**. Can a compact description construct a larger program?
24. **EVOU-24 — A minimal genomic-computation hypothesis**. What precise system are we proposing to test?

### VI · Implementing only what is specified

25. **EVOU-25 — Classes, interfaces and a UML model**. How can the software structure express the proposed rules?
26. **EVOU-26 — From a request to an expression trace**. Who talks to whom during one request?
27. **EVOU-27 — Traces, credit and explanations**. Which component deserves credit, and what can a trace actually explain?
28. **EVOU-28 — Structural proposals and their lifecycle**. When may a proposed edit become active?
29. **EVOU-29 — Training a candidate Evolutor model**. Does the proposed mechanism help beyond the taught baselines?
30. **EVOU-30 — An inference runtime with clear boundaries**. Which parts must run for one prediction?

### VII · Engineering and reproducibility

31. **EVOU-31 — Model identity, formats and checkpoints**. How do we know which model produced this result?
32. **EVOU-32 — Managing recurrent state, KV and external memory**. How can several requests share hardware without sharing private state?
33. **EVOU-33 — Batching, queues and latency**. Why can throughput improve while some users wait longer?
34. **EVOU-34 — Parity, profiling and optimization**. How do we make it faster without changing what it computes?
35. **EVOU-35 — Serving, observability and safe rollback**. How do we observe and recover a running service?

### VIII · Evidence, failure and the frontier

36. **EVOU-36 — Failed ideas as a source of knowledge**. What should we learn when the idea does not win?
37. **EVOU-37 — DNA sequence models: DOGMA and Hermon DNA as questions**. Which architectural distinction survives beyond a project name?
38. **EVOU-38 — Transfer, continual learning and populations**. Does an improvement survive a changed task?
39. **EVOU-39 — AGI claims and an operational scorecard**. What does a narrow result allow us to say about general intelligence?
40. **EVOU-40 — Capstone: a reproducible research-engineering argument**. Can another reader reproduce both the result and the boundary of the claim?

Chapter count is provisional, not a promise of one semester. These are small teaching units, not equal-length lectures. The full two-book path can span multiple courses. No chapter requires an external prerequisite textbook.
