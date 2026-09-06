# Evolutor: undergraduate-first architecture

Status: Chapter 1 internally reviewed development draft; all later units remain planned. No learner study, independent expert certification or new research-model experiment is claimed. Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json). See [Chapter 1 storyboard](research/undergraduate-ch01-storyboard.md) for the six produced figures.

Target taxonomy: **DOGMA = non-Transformer DNA-native architecture + DOGMA Engine; Hermon DNA = Transformer-based DNA architecture + Hermon DNA Engine; Evolutor = research/theory/runtime above both.** These are research targets, not implementation evidence. See [taxonomy and lineage](research/architecture-taxonomy.md). Stable EVOU IDs differ from printed numbers after EVOU-11.

## Teaching route and chapter opening maps

Each opening recalls named prior ideas, introduces only the current step, and identifies what it enables next. A dependency is a teaching requirement, not a claimed biological causal relation. Unlisted previous chapters remain available for optional practice; no later chapter may be required.

## EVOU-01 — Programs, genomes and the question of Evolutor

**Required earlier units (planned unless marked active):** High-school arithmetic and logical reading.

**Book I bridge:** DNAU-03, DNAU-09, DNAU-32. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** biological gene versus computational gene → analogy → research program.

**Tangible opening:** Why compare a genome with a program?

**Why and how the mathematics enters:** No tuple or cost formula. Explain program as written instructions; model and neural network are destinations taught in Chapter 3 and Chapter 7.

**Observable exit task:** Recognize an analogy; identify a missing mechanism; explain that ordinary software can also respond and change.

**Enables next:** EVOU-02, EVOU-20.

## EVOU-02 — Programs that choose and remember

**Required earlier units (planned unless marked active):** EVOU-01: Programs, genomes and the question of Evolutor.

**Book I bridge:** DNAU-03, DNAU-04. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** persistent state → module → interface contract → conditional execution.

**Tangible opening:** How can the same input produce a different answer after a different history?

**Why and how the mathematics enters:** Replay addition and assignment before a state-update table; no recurrence symbols yet.

**Observable exit task:** Trace both histories; test a reset; distinguish the current input, remembered state and stored instructions.

**Enables next:** EVOU-03, EVOU-10, EVOU-15, EVOU-17.

## EVOU-03 — Machine learning with one tiny model

**Required earlier units (planned unless marked active):** EVOU-02: Programs that choose and remember.

**Book I bridge:** DNAU-03, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** machine learning → model → parameter → prediction → training → inference → loss.

**Tangible opening:** How can examples help set a rule's adjustable numbers?

**Why and how the mathematics enters:** Explain input, weight and offset using prices before y=wx+b; errors before mean squared loss. Training uses manual trials, not gradients.

**Observable exit task:** Compute one prediction; compare two trial settings; distinguish fitting examples from success on new ones.

**Enables next:** EVOU-04, EVOU-05, EVOU-06.

## EVOU-04 — Data, uncertainty and fair evaluation

**Required earlier units (planned unless marked active):** EVOU-03: Machine learning with one tiny model.

**Book I bridge:** DNAU-12. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** dataset → training split → validation split → test split → overfitting → mean → variance → confidence interval → data leakage.

**Tangible opening:** Why can a model look good and still fail on new examples?

**Why and how the mathematics enters:** Recall Book I probabilities; concrete spreads precede variance, sampling uncertainty and interval notation; teach what an interval does not guarantee.

**Observable exit task:** Identify leakage; compute a mean error; explain why one run is insufficient evidence.

**Enables next:** EVOU-06, EVOU-08, EVOU-15, EVOU-16, EVOU-19.

## EVOU-05 — Vectors, matrices and tensors as data containers

**Required earlier units (planned unless marked active):** EVOU-03: Machine learning with one tiny model.

**Book I bridge:** DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** tensor → shape → batch dimension → broadcasting.

**Tangible opening:** How can one rule process several measurements together?

**Why and how the mathematics enters:** Recall Book I dot products and matrix multiplication explicitly; every axis gets a name before tensor notation.

**Observable exit task:** Compute a tiny product; label axes; diagnose an accidental broadcast.

**Enables next:** EVOU-06, EVOU-07, EVOU-09, EVOU-11, EVOU-12.

## EVOU-06 — Slopes, gradients and improving a prediction

**Required earlier units (planned unless marked active):** EVOU-03: Machine learning with one tiny model; EVOU-04: Data, uncertainty and fair evaluation; EVOU-05: Vectors, matrices and tensors as data containers.

**Book I bridge:** DNAU-08, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** derivative → partial derivative → gradient → chain rule → gradient descent → learning rate.

**Tangible opening:** Which small change would reduce the error?

**Why and how the mathematics enters:** Finite differences and rise-over-run precede derivatives; one variable before partial derivatives; chain rule before gradient update notation.

**Observable exit task:** Compute a slope; show an overly large step; explain local improvement versus a global guarantee.

**Enables next:** EVOU-07, EVOU-08, EVOU-10, EVOU-12, EVOU-22, EVOU-27.

## EVOU-07 — Neural networks built one layer at a time

**Required earlier units (planned unless marked active):** EVOU-05: Vectors, matrices and tensors as data containers; EVOU-06: Slopes, gradients and improving a prediction.

**Book I bridge:** DNAU-03, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** neural network → layer → activation → multilayer perceptron → MLP → backpropagation → convolution → CNN.

**Tangible opening:** Why put simple transformations in layers?

**Why and how the mathematics enters:** Teach linear versus nonlinear with pictures before matrix-layer notation; convolution is a local shared-weight operation before the acronym convolutional neural network.

**Observable exit task:** Compute two neurons; compare linear compositions and nonlinear layers; trace one gradient path.

**Enables next:** EVOU-08, EVOU-09, EVOU-13.

## EVOU-08 — A complete small training loop in PyTorch

**Required earlier units (planned unless marked active):** EVOU-04: Data, uncertainty and fair evaluation; EVOU-06: Slopes, gradients and improving a prediction; EVOU-07: Neural networks built one layer at a time.

**Book I bridge:** DNAU-04. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** PyTorch → automatic differentiation → optimizer → epoch → checkpoint → device → random seed.

**Tangible opening:** What changes during training, and what stays fixed during inference?

**Why and how the mathematics enters:** Map each code operation to Chapter 6 arithmetic; explain gradient accumulation and reset before optimizer calls.

**Observable exit task:** Repair a missing gradient reset; reproduce a tiny run; verify parameters are unchanged by inference.

**Enables next:** EVOU-09, EVOU-10, EVOU-13, EVOU-16, EVOU-19, EVOU-29, EVOU-49.

## EVOU-09 — Tokens, embeddings and predicting the next symbol

**Required earlier units (planned unless marked active):** EVOU-05: Vectors, matrices and tensors as data containers; EVOU-07: Neural networks built one layer at a time; EVOU-08: A complete small training loop in PyTorch.

**Book I bridge:** DNAU-02, DNAU-12, DNAU-33. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** token → vocabulary → embedding → next-token prediction → categorical distribution → softmax → cross-entropy.

**Tangible opening:** How do written symbols become numbers a model can use?

**Why and how the mathematics enters:** Explain categorical probabilities and normalized positive scores before softmax; logarithm recall precedes cross-entropy; IDs are not numeric distances.

**Observable exit task:** Distinguish a character from a token; compute a tiny normalized distribution; prevent future-token leakage.

**Enables next:** EVOU-10, EVOU-12, EVOU-47.

## EVOU-10 — Recurrence: remembering one step at a time

**Required earlier units (planned unless marked active):** EVOU-02: Programs that choose and remember; EVOU-06: Slopes, gradients and improving a prediction; EVOU-08: A complete small training loop in PyTorch; EVOU-09: Tokens, embeddings and predicting the next symbol.

**Book I bridge:** DNAU-28. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** recurrent neural network → RNN → hidden state → unrolling → backpropagation through time → leaky integrator.

**Tangible opening:** How can a model carry something from the previous symbol?

**Why and how the mathematics enters:** Old amount minus lost amount plus new amount precedes (1-d)x+pu; label before/after state, then generalize to RNN notation.

**Observable exit task:** Compute two steps; compare histories; test reset boundaries and explain why memory is not yet learning.

**Enables next:** EVOU-11, EVOU-41, EVOU-14, EVOU-20.

## EVOU-11 — Gates and state-space models

**Required earlier units (planned unless marked active):** EVOU-05: Vectors, matrices and tensors as data containers; EVOU-10: Recurrence: remembering one step at a time.

**Book I bridge:** DNAU-28, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** gate → gated recurrent unit → GRU → state-space model → SSM → stability.

**Tangible opening:** What should a compact state keep or forget?

**Why and how the mathematics enters:** Matrix recurrence follows scalar recurrence; introduce eigenvalue intuition only if used, with a two-dimensional example; no unprepared stability theorem.

**Observable exit task:** Trace a gate at zero and one; compare state sizes; state what information a compact state may lose.

**Enables next:** EVOU-41, EVOU-19, EVOU-37.

## EVOU-41 — Strong recurrent baselines and valid scans

**Required earlier units (planned unless marked active):** EVOU-10: Recurrence: remembering one step at a time; EVOU-11: Gates and state-space models.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** finite-state machine → long short-term memory → LSTM → selective state update → associative scan → RWKV comparison.

**Tangible opening:** Which familiar mechanisms could already explain a candidate's behavior?

**Why and how the mathematics enters:** Hand trace before equations; recurrence does not imply all training is serial. Teach each named baseline before comparison.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-42, EVOU-45, EVOU-50.

## EVOU-12 — Attention as a weighted lookup

**Required earlier units (planned unless marked active):** EVOU-05: Vectors, matrices and tensors as data containers; EVOU-06: Slopes, gradients and improving a prediction; EVOU-09: Tokens, embeddings and predicting the next symbol.

**Book I bridge:** DNAU-12, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** query → key → value → attention score → attention → causal mask → attention head.

**Tangible opening:** Which earlier symbol should matter now?

**Why and how the mathematics enters:** Use explicit two-number vectors, dot products, softmax and weighted sum before QK-transpose notation.

**Observable exit task:** Compute weights; explain query/key/value roles; demonstrate a causal-mask failure.

**Enables next:** EVOU-13, EVOU-47.

## EVOU-13 — From one attention head to a Transformer

**Required earlier units (planned unless marked active):** EVOU-07: Neural networks built one layer at a time; EVOU-08: A complete small training loop in PyTorch; EVOU-12: Attention as a weighted lookup.

**Book I bridge:** DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** multi-head attention → residual connection → normalization → feed-forward network → Transformer → positional encoding.

**Tangible opening:** How do small attention operations form a useful model?

**Why and how the mathematics enters:** Teach mean/variance normalization and skip addition before block equations; every tensor shape remains labeled.

**Observable exit task:** Trace one token through a block; explain why position matters; reject a full architecture diagram with unlabeled axes.

**Enables next:** EVOU-14, EVOU-16, EVOU-19, EVOU-47, EVOU-37.

## EVOU-14 — Caches, retrieval and external memory

**Required earlier units (planned unless marked active):** EVOU-10: Recurrence: remembering one step at a time; EVOU-13: From one attention head to a Transformer.

**Book I bridge:** DNAU-33. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** cache → key-value cache → KV cache → retrieval → external memory → index.

**Tangible opening:** Why keep earlier work, and when should a system look something up?

**Why and how the mathematics enters:** Count stored rows and reused operations before memory formulas; cache stores computations, not a magical source of factual truth.

**Observable exit task:** Distinguish recurrent state, KV cache and retrieved documents; test stale-cache and mismatched-history cases.

**Enables next:** EVOU-18, EVOU-47, EVOU-32, EVOU-55.

## EVOU-15 — If/else, dispatch, plugins and dynamic routing

**Required earlier units (planned unless marked active):** EVOU-02: Programs that choose and remember; EVOU-04: Data, uncertainty and fair evaluation.

**Book I bridge:** DNAU-03, DNAU-04, DNAU-06. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** dispatch → plugin → router → dynamic routing → pure function → lookup cost.

**Tangible opening:** What already selects only part of a program?

**Why and how the mathematics enters:** Count concrete comparisons before cost tuples; prove equivalence only after tracing matching inputs and assumptions.

**Observable exit task:** Find a duplicate-name bug; compare costs honestly; explain why selective execution alone is not novel.

**Enables next:** EVOU-16, EVOU-17, EVOU-21, EVOU-43.

## EVOU-16 — Mixture of experts and learned routing

**Required earlier units (planned unless marked active):** EVOU-04: Data, uncertainty and fair evaluation; EVOU-08: A complete small training loop in PyTorch; EVOU-13: From one attention head to a Transformer; EVOU-15: If/else, dispatch, plugins and dynamic routing.

**Book I bridge:** DNAU-06, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** mixture of experts → MoE → expert → load balancing → sparse activation.

**Tangible opening:** Can the choice of a module itself be learned?

**Why and how the mathematics enters:** Top-k selection and weighted sums precede routing loss; distinguish stored and activated parameters.

**Observable exit task:** Trace a route; identify collapse; distinguish sparsity from an established end-to-end speedup.

**Enables next:** EVOU-19, EVOU-21, EVOU-43, EVOU-59.

## EVOU-17 — Source code, compilers, runtimes and interfaces

**Required earlier units (planned unless marked active):** EVOU-02: Programs that choose and remember; EVOU-15: If/else, dispatch, plugins and dynamic routing.

**Book I bridge:** DNAU-04, DNAU-25. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** compiler → runtime → library → application programming interface → API → process → thread → memory.

**Tangible opening:** What happens between writing a program and running it?

**Why and how the mathematics enters:** No compiler-theory prerequisites; distinguish representation from running instance before any formal semantics.

**Observable exit task:** Match objects to stages; distinguish process from thread; explain interpreter and runtime without treating them as synonyms.

**Enables next:** EVOU-18, EVOU-23, EVOU-25, EVOU-30.

## EVOU-18 — Services, databases, protocols and scheduling

**Required earlier units (planned unless marked active):** EVOU-14: Caches, retrieval and external memory; EVOU-17: Source code, compilers, runtimes and interfaces.

**Book I bridge:** DNAU-03, DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** service → database → protocol → scheduler → query plan → latency → throughput → batch.

**Tangible opening:** Why does serving several requests need more than a model?

**Why and how the mathematics enters:** Time a single request before latency; count completed requests per interval before throughput; teach query operator order before planning costs.

**Observable exit task:** Trace request identity; compare batching tradeoffs; distinguish a cache from an authoritative database.

**Enables next:** EVOU-19, EVOU-21, EVOU-26, EVOU-32, EVOU-54, EVOU-57, EVOU-33.

## EVOU-19 — Baselines, oracles and resource-matched experiments

**Required earlier units (planned unless marked active):** EVOU-04: Data, uncertainty and fair evaluation; EVOU-08: A complete small training loop in PyTorch; EVOU-11: Gates and state-space models; EVOU-13: From one attention head to a Transformer; EVOU-16: Mixture of experts and learned routing; EVOU-18: Services, databases, protocols and scheduling.

**Book I bridge:** DNAU-06, DNAU-12, DNAU-24, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** baseline → oracle → ablation → capacity matching → profiling plan → experimental hypothesis → Markov assumption.

**Tangible opening:** What would count as a fair improvement?

**Why and how the mathematics enters:** Report sample counts, distributions and uncertainty before summary rankings; separate parameters, executed work and wall time.

**Observable exit task:** Design a falsifier; expose answer leakage; explain why an oracle checks a task but does not certify intelligence.

**Enables next:** EVOU-20, EVOU-21, EVOU-22, EVOU-24, EVOU-27, EVOU-42, EVOU-45, EVOU-47, EVOU-48, EVOU-29, EVOU-49, EVOU-59, EVOU-34, EVOU-61, EVOU-39.

## EVOU-20 — Regulation, expression and different timescales

**Required earlier units (planned unless marked active):** EVOU-01: Programs, genomes and the question of Evolutor; EVOU-10: Recurrence: remembering one step at a time; EVOU-19: Baselines, oracles and resource-matched experiments.

**Book I bridge:** DNAU-13, DNAU-32. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** biological regulation versus routing → sequence transfer versus control → timescale.

**Tangible opening:** What changes within a cell, and what changes across generations?

**Why and how the mathematics enters:** Recall Book I units and recurrence; a biological cartoon is not a fitted differential equation.

**Observable exit task:** Distinguish control from sequence reversal; classify state change, gene expression and inherited change.

**Enables next:** EVOU-21, EVOU-24.

## EVOU-21 — Analogies that can fail

**Required earlier units (planned unless marked active):** EVOU-15: If/else, dispatch, plugins and dynamic routing; EVOU-16: Mixture of experts and learned routing; EVOU-18: Services, databases, protocols and scheduling; EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-20: Regulation, expression and different timescales.

**Book I bridge:** DNAU-32, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** abstraction → mechanism → novelty claim → biological fidelity.

**Tangible opening:** What remains after comparing a biological idea with existing software?

**Why and how the mathematics enters:** No formalism yet; specify observable differences and excluded biological features in ordinary language.

**Observable exit task:** Reject a renamed existing mechanism; propose a discriminating experiment; leave an unsupported claim open.

**Enables next:** EVOU-22, EVOU-23, EVOU-24, EVOU-43.

## EVOU-22 — Learning parameters and changing structure

**Required earlier units (planned unless marked active):** EVOU-06: Slopes, gradients and improving a prediction; EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-21: Analogies that can fail.

**Book I bridge:** DNAU-05, DNAU-06, DNAU-32. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** pruning → architecture search → genetic programming → program synthesis → structural update.

**Tangible opening:** How does changing a number differ from changing a program?

**Why and how the mathematics enters:** Teach tree and syntax node with an arithmetic expression before genetic-programming notation; introduce search spaces concretely.

**Observable exit task:** Classify changes; track who evaluates candidates; identify evaluation-set reuse and selection bias.

**Enables next:** EVOU-23, EVOU-24, EVOU-28, EVOU-44, EVOU-38.

## EVOU-23 — Development as building a representation

**Required earlier units (planned unless marked active):** EVOU-17: Source code, compilers, runtimes and interfaces; EVOU-21: Analogies that can fail; EVOU-22: Learning parameters and changing structure.

**Book I bridge:** DNAU-25, DNAU-31, DNAU-32. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** intermediate representation → IR → developmental program → compilation phase.

**Tangible opening:** Can a compact description construct a larger program?

**Why and how the mathematics enters:** Explain grammar, node type and validation locally before formal grammar notation; no equivalence with embryology.

**Observable exit task:** Find an invalid type; distinguish expansion from learning; identify the biological details intentionally absent.

**Enables next:** EVOU-24.

## EVOU-24 — A minimal genomic-computation hypothesis

**Required earlier units (planned unless marked active):** EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-20: Regulation, expression and different timescales; EVOU-21: Analogies that can fail; EVOU-22: Learning parameters and changing structure; EVOU-23: Development as building a representation.

**Book I bridge:** DNAU-25, DNAU-32, DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** computational genome → computational regulator → expression plan → operational semantics.

**Tangible opening:** What precise system are we proposing to test?

**Why and how the mathematics enters:** Only now collect already taught components into a tuple; explain transition rules and costs one at a time.

**Observable exit task:** Derive one transition; exhibit nearest-baseline equivalence; write a condition that would falsify the additional mechanism.

**Enables next:** EVOU-25, EVOU-42, EVOU-29, EVOU-40.

## EVOU-25 — Classes, interfaces and a UML model

**Required earlier units (planned unless marked active):** EVOU-17: Source code, compilers, runtimes and interfaces; EVOU-24: A minimal genomic-computation hypothesis.

**Book I bridge:** DNAU-03. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** class → instance → method → composition → Unified Modeling Language → UML.

**Tangible opening:** How can the software structure express the proposed rules?

**Why and how the mathematics enters:** No unexplained engineering notation; cardinalities are illustrated with concrete object counts first.

**Observable exit task:** Distinguish class from instance; repair an ownership edge; test interface preconditions.

**Enables next:** EVOU-26, EVOU-28, EVOU-58.

## EVOU-26 — From a request to an expression trace

**Required earlier units (planned unless marked active):** EVOU-18: Services, databases, protocols and scheduling; EVOU-25: Classes, interfaces and a UML model.

**Book I bridge:** DNAU-03. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** UML sequence diagram → lifeline → message → executor.

**Tangible opening:** Who talks to whom during one request?

**Why and how the mathematics enters:** Time flows down, messages sideways; distinguish return from a fresh request before asynchronous detail.

**Observable exit task:** Trace one request; detect a backwards message; compare diagram events to recorded code events.

**Enables next:** EVOU-27, EVOU-42, EVOU-30.

## EVOU-27 — Traces, credit and explanations

**Required earlier units (planned unless marked active):** EVOU-06: Slopes, gradients and improving a prediction; EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-26: From a request to an expression trace.

**Book I bridge:** DNAU-12, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** credit assignment → trace provenance → causal intervention.

**Tangible opening:** Which component deserves credit, and what can a trace actually explain?

**Why and how the mathematics enters:** Event correlation before causal claims; gradients and interventions answer different questions.

**Observable exit task:** Explain why a logged route is not a causal proof; identify missing provenance; propose a controlled intervention.

**Enables next:** EVOU-28, EVOU-46, EVOU-29.

## EVOU-28 — Structural proposals and their lifecycle

**Required earlier units (planned unless marked active):** EVOU-22: Learning parameters and changing structure; EVOU-25: Classes, interfaces and a UML model; EVOU-27: Traces, credit and explanations.

**Book I bridge:** DNAU-06, DNAU-32. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** UML state machine → proposal lifecycle → invariant → rollback.

**Tangible opening:** When may a proposed edit become active?

**Why and how the mathematics enters:** State diagrams precede transition tables; explain safety invariants with invalid examples.

**Observable exit task:** Reject an untested transition; preserve the old version; distinguish bounded validation from universal correctness.

**Enables next:** EVOU-42, EVOU-44, EVOU-46, EVOU-29, EVOU-35, EVOU-38.

## EVOU-42 — DOGMA: candidate primitives and state semantics

**Required earlier units (planned unless marked active):** EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-24: A minimal genomic-computation hypothesis; EVOU-26: From a request to an expression trace; EVOU-28: Structural proposals and their lifecycle; EVOU-41: Strong recurrent baselines and valid scans.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** DOGMA target architecture → DOGMA transition contract.

**Tangible opening:** Can structured state support DNA-native computation without Transformer attention as its organizing mechanism?

**Why and how the mathematics enters:** Define state ownership and token timing before F_theta. A next-token head reads the post-input state; other conventions must be explicit.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-43, EVOU-44, EVOU-50, EVOU-51.

## EVOU-43 — DOGMA regulation and expressed transformations

**Required earlier units (planned unless marked active):** EVOU-15: If/else, dispatch, plugins and dynamic routing; EVOU-16: Mixture of experts and learned routing; EVOU-21: Analogies that can fail; EVOU-42: DOGMA: candidate primitives and state semantics.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** DOGMA regulator candidate → DOGMA expression candidate.

**Tangible opening:** What exactly does regulation select and expression execute?

**Why and how the mathematics enters:** R/E/U is a candidate decomposition, not a validated final definition; introduce each domain and codomain after a hand trace.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-44, EVOU-45, EVOU-46, EVOU-50.

## EVOU-44 — DOGMA modular state, locality and structural memory

**Required earlier units (planned unless marked active):** EVOU-22: Learning parameters and changing structure; EVOU-28: Structural proposals and their lifecycle; EVOU-42: DOGMA: candidate primitives and state semantics; EVOU-43: DOGMA regulation and expressed transformations.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** DOGMA memory locus candidate → DOGMA multi-timescale state.

**Tangible opening:** Does modular state help beyond a single carried vector?

**Why and how the mathematics enters:** Define purpose, update schedule, differentiability and reset rules for each component; genomic names supply no semantics.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-45, EVOU-46, EVOU-59.

## EVOU-45 — DOGMA strands, complements and dual-state proposals

**Required earlier units (planned unless marked active):** EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-41: Strong recurrent baselines and valid scans; EVOU-43: DOGMA regulation and expressed transformations; EVOU-44: DOGMA modular state, locality and structural memory.

**Book I bridge:** DNAU-11, DNAU-32, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** DOGMA dual-state candidate → causal reverse-complement boundary.

**Tangible opening:** Does a paired representation improve a declared task?

**Why and how the mathematics enters:** Book I strand polarity and reverse complement are explicit imports. Full-sequence symmetry and streaming causality are different contracts.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-46.

## EVOU-46 — DOGMA traces and structural adaptation

**Required earlier units (planned unless marked active):** EVOU-27: Traces, credit and explanations; EVOU-28: Structural proposals and their lifecycle; EVOU-43: DOGMA regulation and expressed transformations; EVOU-44: DOGMA modular state, locality and structural memory; EVOU-45: DOGMA strands, complements and dual-state proposals.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** DOGMA trace contract → trace utility test.

**Tangible opening:** Does a trace reveal useful mechanism beyond ordinary activation logs?

**Why and how the mathematics enters:** Trace metadata is not inherently an explanation; state exactly what a claimed intervention changes.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-29, EVOU-49, EVOU-37.

## EVOU-47 — Hermon DNA: a Transformer sequence model

**Required earlier units (planned unless marked active):** EVOU-09: Tokens, embeddings and predicting the next symbol; EVOU-12: Attention as a weighted lookup; EVOU-13: From one attention head to a Transformer; EVOU-14: Caches, retrieval and external memory; EVOU-19: Baselines, oracles and resource-matched experiments.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** Hermon DNA target architecture → Transformer DNA reference contract.

**Tangible opening:** What remains recognizably Transformer-based before DNA-specific changes?

**Why and how the mathematics enters:** Teach all matrix shapes; identify head, layers, positions and output projection. Genomic name does not change attention semantics.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-48, EVOU-55.

## EVOU-48 — Hermon DNA: DNA-aware Transformer hypotheses

**Required earlier units (planned unless marked active):** EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-47: Hermon DNA: a Transformer sequence model.

**Book I bridge:** DNAU-11, DNAU-32, DNAU-34. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** strand-aware embedding candidate → motif-aware attention candidate.

**Tangible opening:** Which DNA-specific change adds value beyond the plain Transformer?

**Why and how the mathematics enters:** Different tokenizations change sequence length and workload; compare full resource accounts, not raw tokens alone.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-29, EVOU-49, EVOU-59, EVOU-37.

## EVOU-29 — Training a candidate Evolutor model

**Required earlier units (planned unless marked active):** EVOU-08: A complete small training loop in PyTorch; EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-24: A minimal genomic-computation hypothesis; EVOU-27: Traces, credit and explanations; EVOU-28: Structural proposals and their lifecycle; EVOU-46: DOGMA traces and structural adaptation; EVOU-48: Hermon DNA: DNA-aware Transformer hypotheses.

**Book I bridge:** DNAU-34, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** candidate training contract → multi-timescale update → frozen structure control.

**Tangible opening:** Does the proposed mechanism help beyond the taught baselines?

**Why and how the mathematics enters:** Map each loss term to a measured objective before combining it; disclose update schedules and budgets.

**Observable exit task:** Audit a training loop; test frozen-structure behavior; report an inconclusive or negative outcome correctly.

**Enables next:** EVOU-49, EVOU-30, EVOU-31, EVOU-36, EVOU-37.

## EVOU-49 — Shared PyTorch experiments without false equivalence

**Required earlier units (planned unless marked active):** EVOU-08: A complete small training loop in PyTorch; EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-29: Training a candidate Evolutor model; EVOU-46: DOGMA traces and structural adaptation; EVOU-48: Hermon DNA: DNA-aware Transformer hypotheses.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** dual-family training contract.

**Tangible opening:** What can both model families share without hiding their differences?

**Why and how the mathematics enters:** No new algebra: consolidate training and inference contracts already taught. Shared prepare/step returns logits, not an unexplained token.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-50, EVOU-51, EVOU-55.

## EVOU-50 — DOGMA training: sequential, chunked and scan forms

**Required earlier units (planned unless marked active):** EVOU-41: Strong recurrent baselines and valid scans; EVOU-42: DOGMA: candidate primitives and state semantics; EVOU-43: DOGMA regulation and expressed transformations; EVOU-49: Shared PyTorch experiments without false equivalence.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** DOGMA training-inference parity.

**Tangible opening:** When can a candidate transition be parallelized without changing its meaning?

**Why and how the mathematics enters:** Prove associativity where required. A nonlinear state-dependent regulator may prevent the proposed scan; do not assume a speedup.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-51, EVOU-60.

## EVOU-30 — An inference runtime with clear boundaries

**Required earlier units (planned unless marked active):** EVOU-17: Source code, compilers, runtimes and interfaces; EVOU-26: From a request to an expression trace; EVOU-29: Training a candidate Evolutor model.

**Book I bridge:** DNAU-03, DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** runtime component → backend → inference contract → UML component diagram.

**Tangible opening:** Which parts must run for one prediction?

**Why and how the mathematics enters:** No new optimization formulas; teach contracts and observable behavior before implementation shortcuts.

**Observable exit task:** Trace a component failure; test parameter immutability; compare class and component diagrams.

**Enables next:** EVOU-31, EVOU-32, EVOU-51, EVOU-55, EVOU-58, EVOU-34.

## EVOU-31 — Model identity, formats and checkpoints

**Required earlier units (planned unless marked active):** EVOU-29: Training a candidate Evolutor model; EVOU-30: An inference runtime with clear boundaries.

**Book I bridge:** DNAU-33, DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** serialization → schema version → content hash → model identity → provenance.

**Tangible opening:** How do we know which model produced this result?

**Why and how the mathematics enters:** Explain byte representation and hash purpose before digest notation; integrity is not authenticity.

**Observable exit task:** Find a missing configuration field; distinguish matching filename from matching model; reject silent fallback.

**Enables next:** EVOU-32, EVOU-51, EVOU-53, EVOU-55, EVOU-58, EVOU-60, EVOU-35, EVOU-37.

## EVOU-32 — Managing recurrent state, KV and external memory

**Required earlier units (planned unless marked active):** EVOU-14: Caches, retrieval and external memory; EVOU-18: Services, databases, protocols and scheduling; EVOU-30: An inference runtime with clear boundaries; EVOU-31: Model identity, formats and checkpoints.

**Book I bridge:** DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** state pool → memory ownership → paged KV → eviction → isolation.

**Tangible opening:** How can several requests share hardware without sharing private state?

**Why and how the mathematics enters:** Labeled byte counts and page sizes precede capacity equations; distinguish logical history from physical location.

**Observable exit task:** Detect cross-request leakage; calculate capacity; explain why recurrent state and KV have different contracts.

**Enables next:** EVOU-51, EVOU-52, EVOU-54, EVOU-55, EVOU-56, EVOU-57, EVOU-33, EVOU-34.

## EVOU-51 — DOGMA Engine: state construction and native steps

**Required earlier units (planned unless marked active):** EVOU-30: An inference runtime with clear boundaries; EVOU-31: Model identity, formats and checkpoints; EVOU-32: Managing recurrent state, KV and external memory; EVOU-42: DOGMA: candidate primitives and state semantics; EVOU-49: Shared PyTorch experiments without false equivalence; EVOU-50: DOGMA training: sequential, chunked and scan forms.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** DOGMA Engine → prompt ingestion.

**Tangible opening:** How does the engine execute the model's exact state machine?

**Why and how the mathematics enters:** State exactly whether predictions precede or follow input consumption; model weights stay fixed during ordinary inference.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-52, EVOU-53, EVOU-54, EVOU-58.

## EVOU-52 — DOGMA Engine: isolated state pools

**Required earlier units (planned unless marked active):** EVOU-32: Managing recurrent state, KV and external memory; EVOU-51: DOGMA Engine: state construction and native steps.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** DOGMA state-slot lifecycle.

**Tangible opening:** How can requests share hardware without sharing state?

**Why and how the mathematics enters:** Account separately for weights, per-request state, temporary buffers, token history, external memory and trace storage.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-53, EVOU-54.

## EVOU-53 — DOGMA Engine: checkpoint, restore and prefix state

**Required earlier units (planned unless marked active):** EVOU-31: Model identity, formats and checkpoints; EVOU-51: DOGMA Engine: state construction and native steps; EVOU-52: DOGMA Engine: isolated state pools.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** prefix state cache → state checkpoint parity.

**Tangible opening:** Can a saved state resume the same computation?

**Why and how the mathematics enters:** A fixed-size recurrent state need not preserve every past detail; state cache is not Transformer KV cache.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-54, EVOU-59, EVOU-61.

## EVOU-54 — DOGMA Engine: scheduling state transitions

**Required earlier units (planned unless marked active):** EVOU-18: Services, databases, protocols and scheduling; EVOU-32: Managing recurrent state, KV and external memory; EVOU-51: DOGMA Engine: state construction and native steps; EVOU-52: DOGMA Engine: isolated state pools; EVOU-53: DOGMA Engine: checkpoint, restore and prefix state.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** state-transition batching.

**Tangible opening:** Which independent requests can take a step together?

**Why and how the mathematics enters:** Do not copy a Transformer scheduler; state shapes, masks, request length and optional scans determine grouping.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-58, EVOU-60, EVOU-37.

## EVOU-55 — Hermon DNA Engine: prefill and attention decode

**Required earlier units (planned unless marked active):** EVOU-14: Caches, retrieval and external memory; EVOU-30: An inference runtime with clear boundaries; EVOU-31: Model identity, formats and checkpoints; EVOU-32: Managing recurrent state, KV and external memory; EVOU-47: Hermon DNA: a Transformer sequence model; EVOU-49: Shared PyTorch experiments without false equivalence.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** Hermon DNA Engine → prefill → attention decode.

**Tangible opening:** Why does one Transformer request have two execution phases?

**Why and how the mathematics enters:** Derive KV bytes from sequence length, layers, KV heads, head dimension and precision; include other memory separately.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-56, EVOU-57, EVOU-58.

## EVOU-56 — Hermon DNA Engine: paged KV and prefix sharing

**Required earlier units (planned unless marked active):** EVOU-32: Managing recurrent state, KV and external memory; EVOU-55: Hermon DNA Engine: prefill and attention decode.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** Hermon KV page table → Transformer prefix cache.

**Tangible opening:** How do logical positions map to reusable physical pages?

**Why and how the mathematics enters:** Memory maps precede byte equations; prefix matching includes model and tokenizer identity.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-57, EVOU-59.

## EVOU-57 — Hermon DNA Engine: continuous batching and precision

**Required earlier units (planned unless marked active):** EVOU-18: Services, databases, protocols and scheduling; EVOU-32: Managing recurrent state, KV and external memory; EVOU-55: Hermon DNA Engine: prefill and attention decode; EVOU-56: Hermon DNA Engine: paged KV and prefix sharing.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** Transformer batch lifecycle → quantization.

**Tangible opening:** How do request phases and numerical precision change serving?

**Why and how the mathematics enters:** Quantization changes represented numbers; teach rounding and scaling before implementation. Performance remains unmeasured.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-58, EVOU-60, EVOU-37, EVOU-61.

## EVOU-58 — Evolutor runtime above two distinct engines

**Required earlier units (planned unless marked active):** EVOU-25: Classes, interfaces and a UML model; EVOU-30: An inference runtime with clear boundaries; EVOU-31: Model identity, formats and checkpoints; EVOU-51: DOGMA Engine: state construction and native steps; EVOU-54: DOGMA Engine: scheduling state transitions; EVOU-55: Hermon DNA Engine: prefill and attention decode; EVOU-57: Hermon DNA Engine: continuous batching and precision.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** heterogeneous model routing.

**Tangible opening:** What belongs in a shared runtime rather than either engine?

**Why and how the mathematics enters:** Separate theory/planning, model architecture and industrial engine. Runtime composition is a target, not an implemented fact.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-59, EVOU-60, EVOU-37.

## EVOU-59 — Hybrid memory as a testable Evolutor proposal

**Required earlier units (planned unless marked active):** EVOU-16: Mixture of experts and learned routing; EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-44: DOGMA modular state, locality and structural memory; EVOU-48: Hermon DNA: DNA-aware Transformer hypotheses; EVOU-53: DOGMA Engine: checkpoint, restore and prefix state; EVOU-56: Hermon DNA Engine: paged KV and prefix sharing; EVOU-58: Evolutor runtime above two distinct engines.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** compression-addressability hypothesis.

**Tangible opening:** When should information be compressed into state or kept addressable?

**Why and how the mathematics enters:** Attention access to past representations is not a guarantee of exact retrieval. Hybrid composition remains a hypothesis.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-61, EVOU-40.

## EVOU-33 — Batching, queues and latency

**Required earlier units (planned unless marked active):** EVOU-18: Services, databases, protocols and scheduling; EVOU-32: Managing recurrent state, KV and external memory.

**Book I bridge:** DNAU-12, DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** continuous batching → admission control → backpressure → tail latency.

**Tangible opening:** Why can throughput improve while some users wait longer?

**Why and how the mathematics enters:** Teach percentile from sorted waiting times before p95; simple arrival examples before queueing formulas.

**Observable exit task:** Calculate waiting times; identify starvation; compare a throughput gain with tail-latency cost.

**Enables next:** EVOU-34, EVOU-35.

## EVOU-34 — Parity, profiling and optimization

**Required earlier units (planned unless marked active):** EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-30: An inference runtime with clear boundaries; EVOU-32: Managing recurrent state, KV and external memory; EVOU-33: Batching, queues and latency.

**Book I bridge:** DNAU-35, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** parity → profiler → benchmark → warm-up → optimization.

**Tangible opening:** How do we make it faster without changing what it computes?

**Why and how the mathematics enters:** Absolute and relative numerical tolerance precede parity thresholds; timing distribution precedes speedup ratios.

**Observable exit task:** Reject unequal workloads; diagnose a tolerance failure; separate logical-event counts from elapsed time.

**Enables next:** EVOU-60, EVOU-35, EVOU-36.

## EVOU-60 — Measured bottlenecks, native kernels and model formats

**Required earlier units (planned unless marked active):** EVOU-31: Model identity, formats and checkpoints; EVOU-34: Parity, profiling and optimization; EVOU-50: DOGMA training: sequential, chunked and scan forms; EVOU-54: DOGMA Engine: scheduling state transitions; EVOU-57: Hermon DNA Engine: continuous batching and precision; EVOU-58: Evolutor runtime above two distinct engines.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** family-specific kernel gate → state-schema metadata.

**Tangible opening:** Which optimization is justified by profiling and semantic parity?

**Why and how the mathematics enters:** Add architecture/state/regulation schemas only if semantics require them; preserve tokenizer and provenance. Do not turn candidate formats into standards prematurely.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-37, EVOU-61.

## EVOU-35 — Serving, observability and safe rollback

**Required earlier units (planned unless marked active):** EVOU-28: Structural proposals and their lifecycle; EVOU-31: Model identity, formats and checkpoints; EVOU-33: Batching, queues and latency; EVOU-34: Parity, profiling and optimization.

**Book I bridge:** DNAU-35. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** UML deployment diagram → observability → authentication → authorization → threat model → deployment rollback.

**Tangible opening:** How do we observe and recover a running service?

**Why and how the mathematics enters:** Service goals and measured thresholds precede any availability formula; security is a separate review discipline.

**Observable exit task:** Distinguish authentication from authorization; trace rollback state; redact a sensitive log.

**Enables next:** EVOU-36, EVOU-40.

## EVOU-36 — Failed ideas as a source of knowledge

**Required earlier units (planned unless marked active):** EVOU-29: Training a candidate Evolutor model; EVOU-34: Parity, profiling and optimization; EVOU-35: Serving, observability and safe rollback.

**Book I bridge:** DNAU-12, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** negative result → confound → replication → stopping rule.

**Tangible opening:** What should we learn when the idea does not win?

**Why and how the mathematics enters:** Teach multiple comparisons and selection effects with repeated toy trials before significance language.

**Observable exit task:** Separate bug, underpowered test and refuted claim; write a transparent negative-result report.

**Enables next:** EVOU-37, EVOU-61, EVOU-38, EVOU-39, EVOU-40.

## EVOU-37 — DOGMA and Hermon DNA: taxonomy, lineage and comparative evidence

**Required earlier units (planned unless marked active):** EVOU-11: Gates and state-space models; EVOU-13: From one attention head to a Transformer; EVOU-29: Training a candidate Evolutor model; EVOU-31: Model identity, formats and checkpoints; EVOU-36: Failed ideas as a source of knowledge; EVOU-46: DOGMA traces and structural adaptation; EVOU-48: Hermon DNA: DNA-aware Transformer hypotheses; EVOU-54: DOGMA Engine: scheduling state transitions; EVOU-57: Hermon DNA Engine: continuous batching and precision; EVOU-58: Evolutor runtime above two distinct engines; EVOU-60: Measured bottlenecks, native kernels and model formats.

**Book I bridge:** DNAU-11, DNAU-34, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** DNA model taxonomy → reverse-complement symmetry study → research-program name.

**Tangible opening:** Which architectural distinction survives beyond a project name?

**Why and how the mathematics enters:** Reuse taught equations. The target mapping is fixed editorial intent; actual old artifacts keep their measured architecture and historical names.

**Observable exit task:** Separate name, architecture and evidence; design a symmetry control; leave an unverifiable claim unresolved.

**Enables next:** EVOU-61, EVOU-38, EVOU-40.

## EVOU-61 — Applications that stress different kinds of memory

**Required earlier units (planned unless marked active):** EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-36: Failed ideas as a source of knowledge; EVOU-37: DOGMA and Hermon DNA: taxonomy, lineage and comparative evidence; EVOU-53: DOGMA Engine: checkpoint, restore and prefix state; EVOU-57: Hermon DNA Engine: continuous batching and precision; EVOU-59: Hybrid memory as a testable Evolutor proposal; EVOU-60: Measured bottlenecks, native kernels and model formats.

**Book I bridge:** None. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** cross-family workload matrix.

**Tangible opening:** Which tasks reveal compression and addressability tradeoffs?

**Why and how the mathematics enters:** Potential streaming, edge and persistent-agent uses are hypotheses. Indefinite ingestion does not imply perfect retention or constant total memory.

**Observable exit task:** Trace the smallest case by hand; identify one failure condition; compare against the nearest conventional alternative before making an advantage claim.

**Enables next:** EVOU-40.

## EVOU-38 — Transfer, continual learning and populations

**Required earlier units (planned unless marked active):** EVOU-22: Learning parameters and changing structure; EVOU-28: Structural proposals and their lifecycle; EVOU-36: Failed ideas as a source of knowledge; EVOU-37: DOGMA and Hermon DNA: taxonomy, lineage and comparative evidence.

**Book I bridge:** DNAU-12, DNAU-32, DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** transfer → continual learning → catastrophic forgetting → population composition → distribution shift.

**Tangible opening:** Does an improvement survive a changed task?

**Why and how the mathematics enters:** Teach task distributions through concrete examples; distinguish adaptation budget from zero-shot evaluation.

**Observable exit task:** Identify hidden retraining; compare retention and transfer; report costs of population search.

**Enables next:** EVOU-39, EVOU-40.

## EVOU-39 — AGI claims and an operational scorecard

**Required earlier units (planned unless marked active):** EVOU-19: Baselines, oracles and resource-matched experiments; EVOU-36: Failed ideas as a source of knowledge; EVOU-38: Transfer, continual learning and populations.

**Book I bridge:** DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** artificial general intelligence → AGI → capability scope → generalization claim → evidence scorecard.

**Tangible opening:** What does a narrow result allow us to say about general intelligence?

**Why and how the mathematics enters:** No single magic scalar; explain operational definition and uncertainty before any aggregate score.

**Observable exit task:** Reject a unit-test-to-AGI inference; propose disconfirming tests; state the limits of the chosen definition.

**Enables next:** EVOU-40.

## EVOU-40 — Capstone: failures, limits and a reproducible research argument

**Required earlier units (planned unless marked active):** EVOU-24: A minimal genomic-computation hypothesis; EVOU-35: Serving, observability and safe rollback; EVOU-36: Failed ideas as a source of knowledge; EVOU-37: DOGMA and Hermon DNA: taxonomy, lineage and comparative evidence; EVOU-38: Transfer, continual learning and populations; EVOU-39: AGI claims and an operational scorecard; EVOU-59: Hybrid memory as a testable Evolutor proposal; EVOU-61: Applications that stress different kinds of memory.

**Book I bridge:** DNAU-36. See the planned exit checks in the shared contract.

**First encounters, in planned teaching order:** research artifact → replication package → claim retirement.

**Tangible opening:** Can another reader reproduce both the result and the boundary of the claim?

**Why and how the mathematics enters:** Use only established tools; require every equation and plotted quantity to trace to a definition and artifact.

**Observable exit task:** Present the strongest bounded claim, a failed alternative and the next falsifying experiment.

**Enables next:** Capstone completion and further research.
