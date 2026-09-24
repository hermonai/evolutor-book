# Chapter 15: Operational semantics and expression traces

Author-approved storyboard for the original standalone candidate. Independent review remains open.

## 01-machine

Question: What is one execution step?
Objects and arrow semantics: Instruction tape, program counter, integer environment and event stream.
Change/invariant and caption claim: One step changes exactly the registers and control position stated by its rule.
Scientific risk: Software state is not a biological cell.

## 02-loop

Question: Why does the summation loop terminate?
Objects and arrow semantics: Control-flow graph with guarded branch, accumulating body and decreasing counter.
Change/invariant and caption claim: Ranking function decreases once per body, not on every edge.
Scientific risk: Fuel exhaustion is not divergence proof.

## 03-effects

Question: Why does reordering two well-typed operations fail?
Objects and arrow semantics: Two read/write dependency schedules; explicit counterexample values.
Change/invariant and caption claim: Effects constrain scheduling beyond value types.
Scientific risk: Do not claim general compiler legality from one example.

## 04-replay

Question: What makes a trace checkable?
Objects and arrow semantics: Before-state and instruction feed a transition checker; recorded after-state is compared, not trusted.
Change/invariant and caption claim: Semantic replay catches tampering or mismatched input.
Scientific risk: No cryptographic authenticity or durable transaction guarantee.

## 05-outcomes

Question: What is the difference between halt, error and fuel exhaustion?
Objects and arrow semantics: Labeled terminal outcomes branching from a step boundary; resumable snapshot for exhaustion.
Change/invariant and caption claim: A bounded run returns a partial trace without claiming a total result.
Scientific risk: A step budget is not a memory or wall-clock sandbox.
