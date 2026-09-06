# Evolutor: undergraduate-first architecture

Status: planning only. No new chapters, finished figures, animations, experiments or reviewed learning outcomes are claimed. Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json); edit that source and regenerate.

## Teaching route and chapter opening maps

Each opening recalls named prior ideas, introduces only the current step, and identifies what it enables next. A dependency is a teaching requirement, not a claimed biological causal relation. Unlisted previous chapters remain available for optional practice; no later chapter may be required.

## EVOU-01 — Programs, genomes and the question of Evolutor

**Already taught locally:** High-school arithmetic and logical reading.

**Book I bridge:** DNAU-03, DNAU-09, DNAU-32. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** biological gene versus computational gene → analogy → research program.

**Tangible opening:** Why compare a genome with a program?

**Why and how the mathematics enters:** No tuple or cost formula. Explain program as written instructions; model and neural network are destinations taught in Chapter 3 and Chapter 7.

**Observable exit task:** Recognize an analogy; identify a missing mechanism; explain that ordinary software can also respond and change.

**Enables next:** EVOU-02, EVOU-20.

## EVOU-02 — Programs that choose and remember

**Already taught locally:** EVOU-01: Programs, genomes and the question of Evolutor.

**Book I bridge:** DNAU-03, DNAU-04. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** persistent state → module → interface contract → conditional execution.

**Tangible opening:** How can the same input produce a different answer after a different history?

**Why and how the mathematics enters:** Replay addition and assignment before a state-update table; no recurrence symbols yet.

**Observable exit task:** Trace both histories; test a reset; distinguish the current input, remembered state and stored instructions.

**Enables next:** EVOU-03, EVOU-10, EVOU-15, EVOU-17.

## EVOU-03 — Machine learning with one tiny model

**Already taught locally:** EVOU-02: Programs that choose and remember.

**Book I bridge:** DNAU-03, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** machine learning → model → parameter → prediction → training → inference → loss.

**Tangible opening:** How can examples help set a rule's adjustable numbers?

**Why and how the mathematics enters:** Explain input, weight and offset using prices before y=wx+b; errors before mean squared loss. Training uses manual trials, not gradients.

**Observable exit task:** Compute one prediction; compare two trial settings; distinguish fitting examples from success on new ones.

**Enables next:** EVOU-04, EVOU-05, EVOU-06.

## EVOU-04 — Data, uncertainty and fair evaluation

**Already taught locally:** EVOU-03: Machine learning with one tiny model.

**Book I bridge:** DNAU-12. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** dataset → training split → validation split → test split → overfitting → mean → variance → confidence interval → data leakage.

**Tangible opening:** Why can a model look good and still fail on new examples?

**Why and how the mathematics enters:** Recall Book I probabilities; concrete spreads precede variance, sampling uncertainty and interval notation; teach what an interval does not guarantee.

**Observable exit task:** Identify leakage; compute a mean error; explain why one run is insufficient evidence.

**Enables next:** EVOU-06, EVOU-08, EVOU-15, EVOU-16, EVOU-19.

## EVOU-05 — Vectors, matrices and tensors as data containers

**Already taught locally:** EVOU-03: Machine learning with one tiny model.

**Book I bridge:** DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** tensor → shape → batch dimension → broadcasting.

**Tangible opening:** How can one rule process several measurements together?

**Why and how the mathematics enters:** Recall Book I dot products and matrix multiplication explicitly; every axis gets a name before tensor notation.

**Observable exit task:** Compute a tiny product; label axes; diagnose an accidental broadcast.

**Enables next:** EVOU-06, EVOU-07, EVOU-09, EVOU-11, EVOU-12.

## EVOU-06 — Slopes, gradients and improving a prediction

**Already taught locally:** EVOU-03: Machine learning with one tiny model; EVOU-04: Data, uncertainty and fair evaluation; EVOU-05: Vectors, matrices and tensors as data containers.

**Book I bridge:** DNAU-08, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** derivative → partial derivative → gradient → chain rule → gradient descent → learning rate.

**Tangible opening:** Which small change would reduce the error?

**Why and how the mathematics enters:** Finite differences and rise-over-run precede derivatives; one variable before partial derivatives; chain rule before gradient update notation.

**Observable exit task:** Compute a slope; show an overly large step; explain local improvement versus a global guarantee.

**Enables next:** EVOU-07, EVOU-08, EVOU-10, EVOU-12, EVOU-22, EVOU-27.

## EVOU-07 — Neural networks built one layer at a time

**Already taught locally:** EVOU-05: Vectors, matrices and tensors as data containers; EVOU-06: Slopes, gradients and improving a prediction.

**Book I bridge:** DNAU-03, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** neural network → layer → activation → multilayer perceptron → MLP → backpropagation → convolution → CNN.

**Tangible opening:** Why put simple transformations in layers?

**Why and how the mathematics enters:** Teach linear versus nonlinear with pictures before matrix-layer notation; convolution is a local shared-weight operation before the acronym convolutional neural network.

**Observable exit task:** Compute two neurons; compare linear compositions and nonlinear layers; trace one gradient path.

**Enables next:** EVOU-08, EVOU-09, EVOU-13.

## EVOU-08 — A complete small training loop in PyTorch

**Already taught locally:** EVOU-04: Data, uncertainty and fair evaluation; EVOU-06: Slopes, gradients and improving a prediction; EVOU-07: Neural networks built one layer at a time.

**Book I bridge:** DNAU-04. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** PyTorch → automatic differentiation → optimizer → epoch → checkpoint → device → random seed.

**Tangible opening:** What changes during training, and what stays fixed during inference?

**Why and how the mathematics enters:** Map each code operation to Chapter 6 arithmetic; explain gradient accumulation and reset before optimizer calls.

**Observable exit task:** Repair a missing gradient reset; reproduce a tiny run; verify parameters are unchanged by inference.

**Enables next:** EVOU-09, EVOU-10, EVOU-13, EVOU-16, EVOU-19, EVOU-29.

## EVOU-09 — Tokens, embeddings and predicting the next symbol

**Already taught locally:** EVOU-05: Vectors, matrices and tensors as data containers; EVOU-07: Neural networks built one layer at a time; EVOU-08: A complete small training loop in PyTorch.

**Book I bridge:** DNAU-02, DNAU-12, DNAU-33. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** token → vocabulary → embedding → next-token prediction → categorical distribution → softmax → cross-entropy.

**Tangible opening:** How do written symbols become numbers a model can use?

**Why and how the mathematics enters:** Explain categorical probabilities and normalized positive scores before softmax; logarithm recall precedes cross-entropy; IDs are not numeric distances.

**Observable exit task:** Distinguish a character from a token; compute a tiny normalized distribution; prevent future-token leakage.

**Enables next:** EVOU-10, EVOU-12.

## EVOU-10 — Recurrence: remembering one step at a time

**Already taught locally:** EVOU-02: Programs that choose and remember; EVOU-06: Slopes, gradients and improving a prediction; EVOU-08: A complete small training loop in PyTorch; EVOU-09: Tokens, embeddings and predicting the next symbol.

**Book I bridge:** DNAU-28. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** recurrent neural network → RNN → hidden state → unrolling → backpropagation through time → leaky integrator.

**Tangible opening:** How can a model carry something from the previous symbol?

**Why and how the mathematics enters:** Old amount minus lost amount plus new amount precedes (1-d)x+pu; label before/after state, then generalize to RNN notation.

**Observable exit task:** Compute two steps; compare histories; test reset boundaries and explain why memory is not yet learning.

**Enables next:** EVOU-11, EVOU-14, EVOU-20.

## EVOU-11 — Gates and state-space models

**Already taught locally:** EVOU-05: Vectors, matrices and tensors as data containers; EVOU-10: Recurrence: remembering one step at a time.

**Book I bridge:** DNAU-28, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** gate → gated recurrent unit → GRU → state-space model → SSM → stability.

**Tangible opening:** What should a compact state keep or forget?

**Why and how the mathematics enters:** Matrix recurrence follows scalar recurrence; introduce eigenvalue intuition only if used, with a two-dimensional example; no unprepared stability theorem.

**Observable exit task:** Trace a gate at zero and one; compare state sizes; state what information a compact state may lose.

**Enables next:** EVOU-19, EVOU-37.

## EVOU-12 — Attention as a weighted lookup

**Already taught locally:** EVOU-05: Vectors, matrices and tensors as data containers; EVOU-06: Slopes, gradients and improving a prediction; EVOU-09: Tokens, embeddings and predicting the next symbol.

**Book I bridge:** DNAU-12, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** query → key → value → attention score → attention → causal mask → attention head.

**Tangible opening:** Which earlier symbol should matter now?

**Why and how the mathematics enters:** Use explicit two-number vectors, dot products, softmax and weighted sum before QK-transpose notation.

**Observable exit task:** Compute weights; explain query/key/value roles; demonstrate a causal-mask failure.

**Enables next:** EVOU-13.

## EVOU-13 — From one attention head to a Transformer

**Already taught locally:** EVOU-07: Neural networks built one layer at a time; EVOU-08: A complete small training loop in PyTorch; EVOU-12: Attention as a weighted lookup.

**Book I bridge:** DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** multi-head attention → residual connection → normalization → feed-forward network → Transformer → positional encoding.

**Tangible opening:** How do small attention operations form a useful model?

**Why and how the mathematics enters:** Teach mean/variance normalization and skip addition before block equations; every tensor shape remains labeled.

**Observable exit task:** Trace one token through a block; explain why position matters; reject a full architecture diagram with unlabeled axes.

**Enables next:** EVOU-14, EVOU-16, EVOU-19, EVOU-37.

## EVOU-14 — Caches, retrieval and external memory

**Already taught locally:** EVOU-10: Recurrence: remembering one step at a time; EVOU-13: From one attention head to a Transformer.

**Book I bridge:** DNAU-33. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** cache → key-value cache → KV cache → retrieval → external memory → index.

**Tangible opening:** Why keep earlier work, and when should a system look something up?

**Why and how the mathematics enters:** Count stored rows and reused operations before memory formulas; cache stores computations, not a magical source of factual truth.

**Observable exit task:** Distinguish recurrent state, KV cache and retrieved documents; test stale-cache and mismatched-history cases.

**Enables next:** EVOU-18, EVOU-32.

## EVOU-15 — If/else, dispatch, plugins and dynamic routing

**Already taught locally:** EVOU-02: Programs that choose and remember; EVOU-04: Data, uncertainty and fair evaluation.

**Book I bridge:** DNAU-03, DNAU-04, DNAU-06. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** dispatch → plugin → router → dynamic routing → pure function → lookup cost.

**Tangible opening:** What already selects only part of a program?

**Why and how the mathematics enters:** Count concrete comparisons before cost tuples; prove equivalence only after tracing matching inputs and assumptions.

**Observable exit task:** Find a duplicate-name bug; compare costs honestly; explain why selective execution alone is not novel.

**Enables next:** EVOU-16, EVOU-17, EVOU-21.

## EVOU-16 — Mixture of experts and learned routing

**Already taught locally:** EVOU-04: Data, uncertainty and fair evaluation; EVOU-08: A complete small training loop in PyTorch; EVOU-13: From one attention head to a Transformer; EVOU-15: If/else, dispatch, plugins and dynamic routing.

**Book I bridge:** DNAU-06, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** mixture of experts → MoE → expert → load balancing → sparse activation.

**Tangible opening:** Can the choice of a module itself be learned?

**Why and how the mathematics enters:** Top-k selection and weighted sums precede routing loss; distinguish stored and activated parameters.

**Observable exit task:** Trace a route; identify collapse; distinguish sparsity from an established end-to-end speedup.

**Enables next:** EVOU-19, EVOU-21.

## EVOU-17 — Source code, compilers, runtimes and interfaces

**Already taught locally:** EVOU-02: Programs that choose and remember; EVOU-15: If/else, dispatch, plugins and dynamic routing.

**Book I bridge:** DNAU-04, DNAU-25. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** compiler → runtime → library → application programming interface → API → process → thread → memory.

**Tangible opening:** What happens between writing a program and running it?

**Why and how the mathematics enters:** No compiler-theory prerequisites; distinguish representation from running instance before any formal semantics.

**Observable exit task:** Match objects to stages; distinguish process from thread; explain interpreter and runtime without treating them as synonyms.

**Enables next:** EVOU-18, EVOU-23, EVOU-25, EVOU-30.

## EVOU-18 — Services, databases, protocols and scheduling

**Already taught locally:** EVOU-14: Caches, retrieval and external memory; EVOU-17: Source code, compilers, runtimes and interfaces.

**Book I bridge:** DNAU-03, DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** service → database → protocol → scheduler → query plan → latency → throughput → batch.

**Tangible opening:** Why does serving several requests need more than a model?

**Why and how the mathematics enters:** Time a single request before latency; count completed requests per interval before throughput; teach query operator order before planning costs.

**Observable exit task:** Trace request identity; compare batching tradeoffs; distinguish a cache from an authoritative database.

**Enables next:** EVOU-19, EVOU-21, EVOU-26, EVOU-32, EVOU-33.

## EVOU-19 — Baselines, oracles and resource-matched experiments

**Already taught locally:** EVOU-04: Data, uncertainty and fair evaluation; EVOU-08: A complete small training loop in PyTorch; EVOU-11: Gates and state-space models; EVOU-13: From one attention head to a Transformer; EVOU-16: Mixture of experts and learned routing; EVOU-18: Services, databases, protocols and scheduling.

**Book I bridge:** DNAU-06, DNAU-12, DNAU-24, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** baseline → oracle → ablation → capacity matching → profiling plan → experimental hypothesis → Markov assumption.

**Tangible opening:** What would count as a fair improvement?

**Why and how the mathematics enters:** Report sample counts, distributions and uncertainty before summary rankings; separate parameters, executed work and wall time.

**Observable exit task:** Design a falsifier; expose answer leakage; explain why an oracle checks a task but does not certify intelligence.

**Enables next:** EVOU-20, EVOU-21, EVOU-22, EVOU-24, EVOU-27, EVOU-29, EVOU-34, EVOU-39.

## EVOU-20 — Regulation, expression and different timescales

**Already taught locally:** EVOU-01: Programs, genomes and the question of Evolutor; EVOU-10: Recurrence: remembering one step at a time; EVOU-19: Baselines, oracles and resource-matched experiments.

**Book I bridge:** DNAU-13, DNAU-32. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** biological regulation versus routing → sequence transfer versus control → timescale.

**Tangible opening:** What changes within a cell, and what changes across generations?

**Why and how the mathematics enters:** Recall Book I units and recurrence; a biological cartoon is not a fitted differential equation.

**Observable exit task:** Distinguish control from sequence reversal; classify state change, gene expression and inherited change.

**Enables next:** EVOU-21, EVOU-24.

## EVOU-21 — Analogies that can fail

**Already taught locally:** EVOU-15: If/else, dispatch, plugins and dynamic routing; EVOU-16: Mixture of experts and learned routing; EVOU-18: Services, databases, protocols and scheduling; EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-20: Regulation, expression and different timescales.

**Book I bridge:** DNAU-32, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** abstraction → mechanism → novelty claim → biological fidelity.

**Tangible opening:** What remains after comparing a biological idea with existing software?

**Why and how the mathematics enters:** No formalism yet; specify observable differences and excluded biological features in ordinary language.

**Observable exit task:** Reject a renamed existing mechanism; propose a discriminating experiment; leave an unsupported claim open.

**Enables next:** EVOU-22, EVOU-23, EVOU-24.

## EVOU-22 — Learning parameters and changing structure

**Already taught locally:** EVOU-06: Slopes, gradients and improving a prediction; EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-21: Analogies that can fail.

**Book I bridge:** DNAU-05, DNAU-06, DNAU-32. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** pruning → architecture search → genetic programming → program synthesis → structural update.

**Tangible opening:** How does changing a number differ from changing a program?

**Why and how the mathematics enters:** Teach tree and syntax node with an arithmetic expression before genetic-programming notation; introduce search spaces concretely.

**Observable exit task:** Classify changes; track who evaluates candidates; identify evaluation-set reuse and selection bias.

**Enables next:** EVOU-23, EVOU-24, EVOU-28, EVOU-38.

## EVOU-23 — Development as building a representation

**Already taught locally:** EVOU-17: Source code, compilers, runtimes and interfaces; EVOU-21: Analogies that can fail; EVOU-22: Learning parameters and changing structure.

**Book I bridge:** DNAU-25, DNAU-31, DNAU-32. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** intermediate representation → IR → developmental program → compilation phase.

**Tangible opening:** Can a compact description construct a larger program?

**Why and how the mathematics enters:** Explain grammar, node type and validation locally before formal grammar notation; no equivalence with embryology.

**Observable exit task:** Find an invalid type; distinguish expansion from learning; identify the biological details intentionally absent.

**Enables next:** EVOU-24.

## EVOU-24 — A minimal genomic-computation hypothesis

**Already taught locally:** EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-20: Regulation, expression and different timescales; EVOU-21: Analogies that can fail; EVOU-22: Learning parameters and changing structure; EVOU-23: Development as building a representation.

**Book I bridge:** DNAU-25, DNAU-32, DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** computational genome → computational regulator → expression plan → operational semantics.

**Tangible opening:** What precise system are we proposing to test?

**Why and how the mathematics enters:** Only now collect already taught components into a tuple; explain transition rules and costs one at a time.

**Observable exit task:** Derive one transition; exhibit nearest-baseline equivalence; write a condition that would falsify the additional mechanism.

**Enables next:** EVOU-25, EVOU-29, EVOU-40.

## EVOU-25 — Classes, interfaces and a UML model

**Already taught locally:** EVOU-17: Source code, compilers, runtimes and interfaces; EVOU-24: A minimal genomic-computation hypothesis.

**Book I bridge:** DNAU-03. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** class → instance → method → composition → Unified Modeling Language → UML.

**Tangible opening:** How can the software structure express the proposed rules?

**Why and how the mathematics enters:** No unexplained engineering notation; cardinalities are illustrated with concrete object counts first.

**Observable exit task:** Distinguish class from instance; repair an ownership edge; test interface preconditions.

**Enables next:** EVOU-26, EVOU-28.

## EVOU-26 — From a request to an expression trace

**Already taught locally:** EVOU-18: Services, databases, protocols and scheduling; EVOU-25: Classes, interfaces and a UML model.

**Book I bridge:** DNAU-03. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** UML sequence diagram → lifeline → message → executor.

**Tangible opening:** Who talks to whom during one request?

**Why and how the mathematics enters:** Time flows down, messages sideways; distinguish return from a fresh request before asynchronous detail.

**Observable exit task:** Trace one request; detect a backwards message; compare diagram events to recorded code events.

**Enables next:** EVOU-27, EVOU-30.

## EVOU-27 — Traces, credit and explanations

**Already taught locally:** EVOU-06: Slopes, gradients and improving a prediction; EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-26: From a request to an expression trace.

**Book I bridge:** DNAU-12, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** credit assignment → trace provenance → causal intervention.

**Tangible opening:** Which component deserves credit, and what can a trace actually explain?

**Why and how the mathematics enters:** Event correlation before causal claims; gradients and interventions answer different questions.

**Observable exit task:** Explain why a logged route is not a causal proof; identify missing provenance; propose a controlled intervention.

**Enables next:** EVOU-28, EVOU-29.

## EVOU-28 — Structural proposals and their lifecycle

**Already taught locally:** EVOU-22: Learning parameters and changing structure; EVOU-25: Classes, interfaces and a UML model; EVOU-27: Traces, credit and explanations.

**Book I bridge:** DNAU-06, DNAU-32. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** UML state machine → proposal lifecycle → invariant → rollback.

**Tangible opening:** When may a proposed edit become active?

**Why and how the mathematics enters:** State diagrams precede transition tables; explain safety invariants with invalid examples.

**Observable exit task:** Reject an untested transition; preserve the old version; distinguish bounded validation from universal correctness.

**Enables next:** EVOU-29, EVOU-35, EVOU-38.

## EVOU-29 — Training a candidate Evolutor model

**Already taught locally:** EVOU-08: A complete small training loop in PyTorch; EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-24: A minimal genomic-computation hypothesis; EVOU-27: Traces, credit and explanations; EVOU-28: Structural proposals and their lifecycle.

**Book I bridge:** DNAU-34, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** candidate training contract → multi-timescale update → frozen structure control.

**Tangible opening:** Does the proposed mechanism help beyond the taught baselines?

**Why and how the mathematics enters:** Map each loss term to a measured objective before combining it; disclose update schedules and budgets.

**Observable exit task:** Audit a training loop; test frozen-structure behavior; report an inconclusive or negative outcome correctly.

**Enables next:** EVOU-30, EVOU-31, EVOU-36, EVOU-37.

## EVOU-30 — An inference runtime with clear boundaries

**Already taught locally:** EVOU-17: Source code, compilers, runtimes and interfaces; EVOU-26: From a request to an expression trace; EVOU-29: Training a candidate Evolutor model.

**Book I bridge:** DNAU-03, DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** runtime component → backend → inference contract → UML component diagram.

**Tangible opening:** Which parts must run for one prediction?

**Why and how the mathematics enters:** No new optimization formulas; teach contracts and observable behavior before implementation shortcuts.

**Observable exit task:** Trace a component failure; test parameter immutability; compare class and component diagrams.

**Enables next:** EVOU-31, EVOU-32, EVOU-34.

## EVOU-31 — Model identity, formats and checkpoints

**Already taught locally:** EVOU-29: Training a candidate Evolutor model; EVOU-30: An inference runtime with clear boundaries.

**Book I bridge:** DNAU-33, DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** serialization → schema version → content hash → model identity → provenance.

**Tangible opening:** How do we know which model produced this result?

**Why and how the mathematics enters:** Explain byte representation and hash purpose before digest notation; integrity is not authenticity.

**Observable exit task:** Find a missing configuration field; distinguish matching filename from matching model; reject silent fallback.

**Enables next:** EVOU-32, EVOU-35, EVOU-37.

## EVOU-32 — Managing recurrent state, KV and external memory

**Already taught locally:** EVOU-14: Caches, retrieval and external memory; EVOU-18: Services, databases, protocols and scheduling; EVOU-30: An inference runtime with clear boundaries; EVOU-31: Model identity, formats and checkpoints.

**Book I bridge:** DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** state pool → memory ownership → paged KV → eviction → isolation.

**Tangible opening:** How can several requests share hardware without sharing private state?

**Why and how the mathematics enters:** Labeled byte counts and page sizes precede capacity equations; distinguish logical history from physical location.

**Observable exit task:** Detect cross-request leakage; calculate capacity; explain why recurrent state and KV have different contracts.

**Enables next:** EVOU-33, EVOU-34.

## EVOU-33 — Batching, queues and latency

**Already taught locally:** EVOU-18: Services, databases, protocols and scheduling; EVOU-32: Managing recurrent state, KV and external memory.

**Book I bridge:** DNAU-12, DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** continuous batching → admission control → backpressure → tail latency.

**Tangible opening:** Why can throughput improve while some users wait longer?

**Why and how the mathematics enters:** Teach percentile from sorted waiting times before p95; simple arrival examples before queueing formulas.

**Observable exit task:** Calculate waiting times; identify starvation; compare a throughput gain with tail-latency cost.

**Enables next:** EVOU-34, EVOU-35.

## EVOU-34 — Parity, profiling and optimization

**Already taught locally:** EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-30: An inference runtime with clear boundaries; EVOU-32: Managing recurrent state, KV and external memory; EVOU-33: Batching, queues and latency.

**Book I bridge:** DNAU-35, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** parity → profiler → benchmark → warm-up → optimization.

**Tangible opening:** How do we make it faster without changing what it computes?

**Why and how the mathematics enters:** Absolute and relative numerical tolerance precede parity thresholds; timing distribution precedes speedup ratios.

**Observable exit task:** Reject unequal workloads; diagnose a tolerance failure; separate logical-event counts from elapsed time.

**Enables next:** EVOU-35, EVOU-36.

## EVOU-35 — Serving, observability and safe rollback

**Already taught locally:** EVOU-28: Structural proposals and their lifecycle; EVOU-31: Model identity, formats and checkpoints; EVOU-33: Batching, queues and latency; EVOU-34: Parity, profiling and optimization.

**Book I bridge:** DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** UML deployment diagram → observability → authentication → authorization → threat model → deployment rollback.

**Tangible opening:** How do we observe and recover a running service?

**Why and how the mathematics enters:** Service goals and measured thresholds precede any availability formula; security is a separate review discipline.

**Observable exit task:** Distinguish authentication from authorization; trace rollback state; redact a sensitive log.

**Enables next:** EVOU-36, EVOU-40.

## EVOU-36 — Failed ideas as a source of knowledge

**Already taught locally:** EVOU-29: Training a candidate Evolutor model; EVOU-34: Parity, profiling and optimization; EVOU-35: Serving, observability and safe rollback.

**Book I bridge:** DNAU-12, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** negative result → confound → replication → stopping rule.

**Tangible opening:** What should we learn when the idea does not win?

**Why and how the mathematics enters:** Teach multiple comparisons and selection effects with repeated toy trials before significance language.

**Observable exit task:** Separate bug, underpowered test and refuted claim; write a transparent negative-result report.

**Enables next:** EVOU-37, EVOU-38, EVOU-39, EVOU-40.

## EVOU-37 — DNA sequence models: DOGMA and Hermon DNA as questions

**Already taught locally:** EVOU-11: Gates and state-space models; EVOU-13: From one attention head to a Transformer; EVOU-29: Training a candidate Evolutor model; EVOU-31: Model identity, formats and checkpoints; EVOU-36: Failed ideas as a source of knowledge.

**Book I bridge:** DNAU-11, DNAU-34, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** DNA model taxonomy → reverse-complement symmetry study → research-program name.

**Tangible opening:** Which architectural distinction survives beyond a project name?

**Why and how the mathematics enters:** Reuse established equations; no new family definition from branding and no claim of validated taxonomy.

**Observable exit task:** Separate name, architecture and evidence; design a symmetry control; leave an unverifiable claim unresolved.

**Enables next:** EVOU-38, EVOU-40.

## EVOU-38 — Transfer, continual learning and populations

**Already taught locally:** EVOU-22: Learning parameters and changing structure; EVOU-28: Structural proposals and their lifecycle; EVOU-36: Failed ideas as a source of knowledge; EVOU-37: DNA sequence models: DOGMA and Hermon DNA as questions.

**Book I bridge:** DNAU-12, DNAU-32, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** transfer → continual learning → catastrophic forgetting → population composition → distribution shift.

**Tangible opening:** Does an improvement survive a changed task?

**Why and how the mathematics enters:** Teach task distributions through concrete examples; distinguish adaptation budget from zero-shot evaluation.

**Observable exit task:** Identify hidden retraining; compare retention and transfer; report costs of population search.

**Enables next:** EVOU-39, EVOU-40.

## EVOU-39 — AGI claims and an operational scorecard

**Already taught locally:** EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-36: Failed ideas as a source of knowledge; EVOU-38: Transfer, continual learning and populations.

**Book I bridge:** DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** artificial general intelligence → AGI → capability scope → generalization claim → evidence scorecard.

**Tangible opening:** What does a narrow result allow us to say about general intelligence?

**Why and how the mathematics enters:** No single magic scalar; explain operational definition and uncertainty before any aggregate score.

**Observable exit task:** Reject a unit-test-to-AGI inference; propose disconfirming tests; state the limits of the chosen definition.

**Enables next:** EVOU-40.

## EVOU-40 — Capstone: a reproducible research-engineering argument

**Already taught locally:** EVOU-24: A minimal genomic-computation hypothesis; EVOU-35: Serving, observability and safe rollback; EVOU-36: Failed ideas as a source of knowledge; EVOU-37: DNA sequence models: DOGMA and Hermon DNA as questions; EVOU-38: Transfer, continual learning and populations; EVOU-39: AGI claims and an operational scorecard.

**Book I bridge:** DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** research artifact → replication package → claim retirement.

**Tangible opening:** Can another reader reproduce both the result and the boundary of the claim?

**Why and how the mathematics enters:** Use only established tools; require every equation and plotted quantity to trace to a definition and artifact.

**Observable exit task:** Present the strongest bounded claim, a failed alternative and the next falsifying experiment.

**Enables next:** Capstone completion and further research.
