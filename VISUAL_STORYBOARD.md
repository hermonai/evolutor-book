# Evolutor: undergraduate-first architecture

Status: planning only. No new chapters, finished figures, animations, experiments or reviewed learning outcomes are claimed. Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json); edit that source and regenerate.

## Figure production contract

Storyboard → semantic TXT companion → editable vector source → teaching caption → scientific/engineering check → beginner check → rendered-page check. F1 is the primary teaching sequence. F2 is a small worked-example comparison; it is not automatically another large figure. Final figure density depends on actual page layout, with a useful visual or worked example approximately every one or two foundational pages. No quotas override clarity.

## EVOU-01 — Programs, genomes and the question of Evolutor

**Reader question:** Why compare a genome with a program?

**EVOU-01-F1 (sequential teaching figure):**

1. Execute a familiar written recipe.
2. Show a fixed program reacting to two inputs.
3. Recall one genome with different expression states.
4. Place a question mark, not an equals sign, between biology and software.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** No tuple or cost formula. Explain program as written instructions; model and neural network are destinations taught in Chapter 3 and Chapter 7.

**EVOU-01-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Recognize an analogy; identify a missing mechanism; explain that ordinary software can also respond and change.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-02 — Programs that choose and remember

**Reader question:** How can the same input produce a different answer after a different history?

**EVOU-02-F1 (sequential teaching figure):**

1. Run an if/else choice.
2. Add a remembered counter.
3. Run the same input after two histories.
4. Separate stored instructions from changing state.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Replay addition and assignment before a state-update table; no recurrence symbols yet.

**EVOU-02-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Trace both histories; test a reset; distinguish the current input, remembered state and stored instructions.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-03 — Machine learning with one tiny model

**Reader question:** How can examples help set a rule's adjustable numbers?

**EVOU-03-F1 (sequential teaching figure):**

1. Place measured points on a small chart.
2. Try a rule with one adjustable multiplier.
3. Add an offset.
4. Compare predictions with targets.
5. Freeze the numbers for a new input.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Explain input, weight and offset using prices before y=wx+b; errors before mean squared loss. Training uses manual trials, not gradients.

**EVOU-03-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Compute one prediction; compare two trial settings; distinguish fitting examples from success on new ones.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-04 — Data, uncertainty and fair evaluation

**Reader question:** Why can a model look good and still fail on new examples?

**EVOU-04-F1 (sequential teaching figure):**

1. Sort examples into three named boxes.
2. Fit only the training box.
3. Choose settings using validation.
4. Open the test box once.
5. Repeat with a different random seed.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Recall Book I probabilities; concrete spreads precede variance, sampling uncertainty and interval notation; teach what an interval does not guarantee.

**EVOU-04-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Identify leakage; compute a mean error; explain why one run is insufficient evidence.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-05 — Vectors, matrices and tensors as data containers

**Reader question:** How can one rule process several measurements together?

**EVOU-05-F1 (sequential teaching figure):**

1. Recall a feature vector.
2. Stack examples as matrix rows.
3. Add a batch axis with labeled dimensions.
4. Show an invalid shape combination.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Recall Book I dot products and matrix multiplication explicitly; every axis gets a name before tensor notation.

**EVOU-05-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Compute a tiny product; label axes; diagnose an accidental broadcast.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-06 — Slopes, gradients and improving a prediction

**Reader question:** Which small change would reduce the error?

**EVOU-06-F1 (sequential teaching figure):**

1. Move one parameter slightly left and right.
2. Measure the change in loss.
3. Draw a local slope.
4. Follow two linked operations backward.
5. Take a small update step.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Finite differences and rise-over-run precede derivatives; one variable before partial derivatives; chain rule before gradient update notation.

**EVOU-06-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Compute a slope; show an overly large step; explain local improvement versus a global guarantee.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-07 — Neural networks built one layer at a time

**Reader question:** Why put simple transformations in layers?

**EVOU-07-F1 (sequential teaching figure):**

1. Apply one weighted sum.
2. Add a nonlinear activation.
3. Connect two small layers.
4. Compare a shared sliding filter.
5. Trace the error backward.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Teach linear versus nonlinear with pictures before matrix-layer notation; convolution is a local shared-weight operation before the acronym convolutional neural network.

**EVOU-07-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Compute two neurons; compare linear compositions and nonlinear layers; trace one gradient path.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-08 — A complete small training loop in PyTorch

**Reader question:** What changes during training, and what stays fixed during inference?

**EVOU-08-F1 (sequential teaching figure):**

1. Load labeled examples.
2. Predict.
3. Compare and form loss.
4. Compute gradients.
5. Update parameters.
6. Repeat, then freeze parameters and predict.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Map each code operation to Chapter 6 arithmetic; explain gradient accumulation and reset before optimizer calls.

**EVOU-08-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Repair a missing gradient reset; reproduce a tiny run; verify parameters are unchanged by inference.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-09 — Tokens, embeddings and predicting the next symbol

**Reader question:** How do written symbols become numbers a model can use?

**EVOU-09-F1 (sequential teaching figure):**

1. Split a tiny sequence using a declared tokenizer.
2. Assign token IDs.
3. Look up small learned rows.
4. Predict one next-token distribution.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Explain categorical probabilities and normalized positive scores before softmax; logarithm recall precedes cross-entropy; IDs are not numeric distances.

**EVOU-09-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Distinguish a character from a token; compute a tiny normalized distribution; prevent future-token leakage.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-10 — Recurrence: remembering one step at a time

**Reader question:** How can a model carry something from the previous symbol?

**EVOU-10-F1 (sequential teaching figure):**

1. Show state zero.
2. Read the first symbol.
3. Retain part of old state and add new input.
4. Read a second symbol with changed state.
5. Unroll the same update across time.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Old amount minus lost amount plus new amount precedes (1-d)x+pu; label before/after state, then generalize to RNN notation.

**EVOU-10-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Compute two steps; compare histories; test reset boundaries and explain why memory is not yet learning.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-11 — Gates and state-space models

**Reader question:** What should a compact state keep or forget?

**EVOU-11-F1 (sequential teaching figure):**

1. Show retained and discarded contributions.
2. Introduce one adjustable gate.
3. Compare a GRU update with fixed retention.
4. Draw state transition and observation separately.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Matrix recurrence follows scalar recurrence; introduce eigenvalue intuition only if used, with a two-dimensional example; no unprepared stability theorem.

**EVOU-11-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Trace a gate at zero and one; compare state sizes; state what information a compact state may lose.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-12 — Attention as a weighted lookup

**Reader question:** Which earlier symbol should matter now?

**EVOU-12-F1 (sequential teaching figure):**

1. Give three tokens labeled information cards.
2. Ask one query.
3. Compare it with three keys.
4. Normalize scores.
5. Combine values.
6. Hide a forbidden future position.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Use explicit two-number vectors, dot products, softmax and weighted sum before QK-transpose notation.

**EVOU-12-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Compute weights; explain query/key/value roles; demonstrate a causal-mask failure.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-13 — From one attention head to a Transformer

**Reader question:** How do small attention operations form a useful model?

**EVOU-13-F1 (sequential teaching figure):**

1. Recall a single head.
2. Compare two heads.
3. Add residual and normalization steps.
4. Add a feed-forward sublayer.
5. Add position information.
6. Stack labeled blocks.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Teach mean/variance normalization and skip addition before block equations; every tensor shape remains labeled.

**EVOU-13-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Trace one token through a block; explain why position matters; reject a full architecture diagram with unlabeled axes.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-14 — Caches, retrieval and external memory

**Reader question:** Why keep earlier work, and when should a system look something up?

**EVOU-14-F1 (sequential teaching figure):**

1. Generate two tokens without reuse.
2. Retain earlier keys and values.
3. Generate the next token reusing them.
4. Compare lookup in an external document collection.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Count stored rows and reused operations before memory formulas; cache stores computations, not a magical source of factual truth.

**EVOU-14-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Distinguish recurrent state, KV cache and retrieved documents; test stale-cache and mismatched-history cases.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-15 — If/else, dispatch, plugins and dynamic routing

**Reader question:** What already selects only part of a program?

**EVOU-15-F1 (sequential teaching figure):**

1. Choose a function by a name.
2. Compare a scan with an indexed lookup.
3. Load a declared plugin.
4. Record selection work separately from execution work.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Count concrete comparisons before cost tuples; prove equivalence only after tracing matching inputs and assumptions.

**EVOU-15-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Find a duplicate-name bug; compare costs honestly; explain why selective execution alone is not novel.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-16 — Mixture of experts and learned routing

**Reader question:** Can the choice of a module itself be learned?

**EVOU-16-F1 (sequential teaching figure):**

1. Score three expert choices.
2. Select a small subset.
3. Combine their outputs.
4. Show an overloaded expert and balancing response.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Top-k selection and weighted sums precede routing loss; distinguish stored and activated parameters.

**EVOU-16-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Trace a route; identify collapse; distinguish sparsity from an established end-to-end speedup.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-17 — Source code, compilers, runtimes and interfaces

**Reader question:** What happens between writing a program and running it?

**EVOU-17-F1 (sequential teaching figure):**

1. Show source text.
2. Transform to an executable representation.
3. Start a process.
4. Call a library through a named interface.
5. Compare separate processes and threads sharing memory.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** No compiler-theory prerequisites; distinguish representation from running instance before any formal semantics.

**EVOU-17-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Match objects to stages; distinguish process from thread; explain interpreter and runtime without treating them as synonyms.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-18 — Services, databases, protocols and scheduling

**Reader question:** Why does serving several requests need more than a model?

**EVOU-18-F1 (sequential teaching figure):**

1. Send a request to a service.
2. Queue two requests.
3. Fetch a row from a database.
4. Compare two query plans.
5. Return labeled responses.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Time a single request before latency; count completed requests per interval before throughput; teach query operator order before planning costs.

**EVOU-18-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Trace request identity; compare batching tradeoffs; distinguish a cache from an authoritative database.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-19 — Baselines, oracles and resource-matched experiments

**Reader question:** What would count as a fair improvement?

**EVOU-19-F1 (sequential teaching figure):**

1. Specify a task before choosing a model.
2. Put simple and advanced baselines alongside a proposal.
3. Hide test answers.
4. Match declared resources.
5. Repeat with several seeds.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Report sample counts, distributions and uncertainty before summary rankings; separate parameters, executed work and wall time.

**EVOU-19-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Design a falsifier; expose answer leakage; explain why an oracle checks a task but does not certify intelligence.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-20 — Regulation, expression and different timescales

**Reader question:** What changes within a cell, and what changes across generations?

**EVOU-20-F1 (sequential teaching figure):**

1. Recall DNA-to-RNA-to-protein sequence transfer.
2. Add a separately typed control relation.
3. Hold DNA fixed while state changes.
4. Contrast inherited variation across generations.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Recall Book I units and recurrence; a biological cartoon is not a fitted differential equation.

**EVOU-20-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Distinguish control from sequence reversal; classify state change, gene expression and inherited change.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-21 — Analogies that can fail

**Reader question:** What remains after comparing a biological idea with existing software?

**EVOU-21-F1 (sequential teaching figure):**

1. Pair gene with module using a question-mark link.
2. Compare promoter and condition.
3. Compare expression and execution.
4. Cross out an equivalence when mechanisms differ.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** No formalism yet; specify observable differences and excluded biological features in ordinary language.

**EVOU-21-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Reject a renamed existing mechanism; propose a discriminating experiment; leave an unsupported claim open.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-22 — Learning parameters and changing structure

**Reader question:** How does changing a number differ from changing a program?

**EVOU-22-F1 (sequential teaching figure):**

1. Update one weight.
2. Remove a connection.
3. Choose another small architecture.
4. Edit a syntax tree.
5. Select among candidate programs.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Teach tree and syntax node with an arithmetic expression before genetic-programming notation; introduce search spaces concretely.

**EVOU-22-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Classify changes; track who evaluates candidates; identify evaluation-set reuse and selection bias.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-23 — Development as building a representation

**Reader question:** Can a compact description construct a larger program?

**EVOU-23-F1 (sequential teaching figure):**

1. Expand a small repeated pattern.
2. Build a typed expression representation.
3. Validate its structure.
4. Compile or interpret it.
5. Compare construction with biological development.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Explain grammar, node type and validation locally before formal grammar notation; no equivalence with embryology.

**EVOU-23-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Find an invalid type; distinguish expansion from learning; identify the biological details intentionally absent.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-24 — A minimal genomic-computation hypothesis

**Reader question:** What precise system are we proposing to test?

**EVOU-24-F1 (sequential teaching figure):**

1. Recall stored modules, context and state.
2. Select an expression plan.
3. Execute it with an explicit trace.
4. Show an optional separately authorized structural proposal.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Only now collect already taught components into a tuple; explain transition rules and costs one at a time.

**EVOU-24-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Derive one transition; exhibit nearest-baseline equivalence; write a condition that would falsify the additional mechanism.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-25 — Classes, interfaces and a UML model

**Reader question:** How can the software structure express the proposed rules?

**EVOU-25-F1 (UML class):**

1. Compare a blueprint class with two instances.
2. Teach class compartments and relationship symbols.
3. Draw Genome, Gene and Regulator classes.
4. Add ExpressionPlan and Trace ownership.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** No unexplained engineering notation; cardinalities are illustrated with concrete object counts first.

**EVOU-25-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Distinguish class from instance; repair an ownership edge; test interface preconditions.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-26 — From a request to an expression trace

**Reader question:** Who talks to whom during one request?

**EVOU-26-F1 (UML sequence):**

1. Introduce actor and lifeline notation.
2. Send context from Runtime to Regulator.
3. Return an expression plan.
4. Execute modules.
5. Return result and trace.
6. Show the error branch.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Time flows down, messages sideways; distinguish return from a fresh request before asynchronous detail.

**EVOU-26-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Trace one request; detect a backwards message; compare diagram events to recorded code events.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-27 — Traces, credit and explanations

**Reader question:** Which component deserves credit, and what can a trace actually explain?

**EVOU-27-F1 (sequential teaching figure):**

1. Record chosen modules.
2. Associate outputs with events.
3. Remove one component in a controlled run.
4. Compare the result with the original.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Event correlation before causal claims; gradients and interventions answer different questions.

**EVOU-27-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Explain why a logged route is not a causal proof; identify missing provenance; propose a controlled intervention.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-28 — Structural proposals and their lifecycle

**Reader question:** When may a proposed edit become active?

**EVOU-28-F1 (UML state machine):**

1. Teach state/transition notation.
2. Create a proposal.
3. Validate it.
4. Evaluate in isolation.
5. Accept or reject.
6. Retain a rollback path.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** State diagrams precede transition tables; explain safety invariants with invalid examples.

**EVOU-28-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Reject an untested transition; preserve the old version; distinguish bounded validation from universal correctness.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-29 — Training a candidate Evolutor model

**Reader question:** Does the proposed mechanism help beyond the taught baselines?

**EVOU-29-F1 (sequential teaching figure):**

1. Load a declared task split.
2. Train the fixed-structure control.
3. Train the candidate.
4. Separate parameter updates from structural proposals.
5. Compare held-out results.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Map each loss term to a measured objective before combining it; disclose update schedules and budgets.

**EVOU-29-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Audit a training loop; test frozen-structure behavior; report an inconclusive or negative outcome correctly.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-30 — An inference runtime with clear boundaries

**Reader question:** Which parts must run for one prediction?

**EVOU-30-F1 (UML component):**

1. Teach component and interface symbols.
2. Load a checked model.
3. Connect planning and execution.
4. Separate storage and monitoring.
5. Return a bounded result.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** No new optimization formulas; teach contracts and observable behavior before implementation shortcuts.

**EVOU-30-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Trace a component failure; test parameter immutability; compare class and component diagrams.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-31 — Model identity, formats and checkpoints

**Reader question:** How do we know which model produced this result?

**EVOU-31-F1 (sequential teaching figure):**

1. Save weights and configuration.
2. Attach schema and data provenance.
3. Reload into a fresh process.
4. Compare identity and outputs.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Explain byte representation and hash purpose before digest notation; integrity is not authenticity.

**EVOU-31-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Find a missing configuration field; distinguish matching filename from matching model; reject silent fallback.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-32 — Managing recurrent state, KV and external memory

**Reader question:** How can several requests share hardware without sharing private state?

**EVOU-32-F1 (sequential teaching figure):**

1. Assign two requests separate state slots.
2. Allocate cache pages.
3. Grow one history.
4. Evict a permitted entry.
5. Verify the other history is unchanged.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Labeled byte counts and page sizes precede capacity equations; distinguish logical history from physical location.

**EVOU-32-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Detect cross-request leakage; calculate capacity; explain why recurrent state and KV have different contracts.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-33 — Batching, queues and latency

**Reader question:** Why can throughput improve while some users wait longer?

**EVOU-33-F1 (sequential teaching figure):**

1. Time one request.
2. Queue several arrivals.
3. Form a batch.
4. Let completed requests leave while new ones enter.
5. Compare waiting-time distributions.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Teach percentile from sorted waiting times before p95; simple arrival examples before queueing formulas.

**EVOU-33-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Calculate waiting times; identify starvation; compare a throughput gain with tail-latency cost.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-34 — Parity, profiling and optimization

**Reader question:** How do we make it faster without changing what it computes?

**EVOU-34-F1 (sequential teaching figure):**

1. Compare reference and optimized outputs.
2. Locate measured work in a profile.
3. Change one bottleneck.
4. Repeat under the same workload.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Absolute and relative numerical tolerance precede parity thresholds; timing distribution precedes speedup ratios.

**EVOU-34-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Reject unequal workloads; diagnose a tolerance failure; separate logical-event counts from elapsed time.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-35 — Serving, observability and safe rollback

**Reader question:** How do we observe and recover a running service?

**EVOU-35-F1 (UML deployment):**

1. Teach nodes and deployed artifacts.
2. Route an authenticated request.
3. Observe logs and metrics without exposing secrets.
4. Roll out a version.
5. Detect failure and roll back.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Service goals and measured thresholds precede any availability formula; security is a separate review discipline.

**EVOU-35-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Distinguish authentication from authorization; trace rollback state; redact a sensitive log.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-36 — Failed ideas as a source of knowledge

**Reader question:** What should we learn when the idea does not win?

**EVOU-36-F1 (sequential teaching figure):**

1. State a claim and its failure condition.
2. Show matched results including failures.
3. Test a suspected confound.
4. Revise or retire the claim.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Teach multiple comparisons and selection effects with repeated toy trials before significance language.

**EVOU-36-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Separate bug, underpowered test and refuted claim; write a transparent negative-result report.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-37 — DNA sequence models: DOGMA and Hermon DNA as questions

**Reader question:** Which architectural distinction survives beyond a project name?

**EVOU-37-F1 (sequential teaching figure):**

1. Compare a Transformer DNA model with a non-Transformer model.
2. Mark shared data and objectives.
3. Test a reverse-complement intervention.
4. Place DOGMA and Hermon DNA names only after source and artifact audit.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Reuse established equations; no new family definition from branding and no claim of validated taxonomy.

**EVOU-37-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Separate name, architecture and evidence; design a symmetry control; leave an unverifiable claim unresolved.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-38 — Transfer, continual learning and populations

**Reader question:** Does an improvement survive a changed task?

**EVOU-38-F1 (sequential teaching figure):**

1. Train on a first task.
2. Evaluate a genuinely new task.
3. Continue learning and recheck the first.
4. Compare individual and population mechanisms.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Teach task distributions through concrete examples; distinguish adaptation budget from zero-shot evaluation.

**EVOU-38-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Identify hidden retraining; compare retention and transfer; report costs of population search.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-39 — AGI claims and an operational scorecard

**Reader question:** What does a narrow result allow us to say about general intelligence?

**EVOU-39-F1 (sequential teaching figure):**

1. List specific tasks and conditions.
2. Mark measured, failed and untested cells.
3. Separate breadth from repeated variants.
4. Show unresolved safety and transfer boundaries.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** No single magic scalar; explain operational definition and uncertainty before any aggregate score.

**EVOU-39-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Reject a unit-test-to-AGI inference; propose disconfirming tests; state the limits of the chosen definition.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.

## EVOU-40 — Capstone: a reproducible research-engineering argument

**Reader question:** Can another reader reproduce both the result and the boundary of the claim?

**EVOU-40-F1 (sequential teaching figure):**

1. Connect hypothesis to mechanism.
2. Connect mechanism to code and diagrams.
3. Reproduce baseline and candidate results.
4. Inspect failures.
5. State what remains unproven.

Keep objects in stable positions when identity is unchanged. Each frame ledger must mark before-state, change, unchanged objects, movement, creation and consumption; use 'not applicable' rather than inventing a physical process for a software picture.

**Caption teaching target:** Use only established tools; require every equation and plotted quantity to trace to a definition and artifact.

**EVOU-40-F2 (worked comparison):** Show a correct worked case beside the mistake or boundary tested here: Present the strongest bounded claim, a failed alternative and the next falsifying experiment.

**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, sequence transfer and control; software distinguishes messages, data, ownership and state transitions. Use labels and line styles as well as color.

**Animation decision:** candidate-keyframe-sequence; storyboard only, no exported frames yet.
