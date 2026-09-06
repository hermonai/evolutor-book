# Evolutor: undergraduate-first architecture

Status: planning only. No new chapters, finished figures, animations, experiments or reviewed learning outcomes are claimed. Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json); edit that source and regenerate.

## Exercises, code and experiments

Progress through recognition → hand calculation/tracing → application → implementation → reasoning → research design. Early chapters stop before levels whose tools are untaught. Every introductory task gets a worked solution or a staged hint and answer check. Later research tasks get a rubric and explicit acceptable uncertainty, not a fabricated unique answer. Return to earlier concepts after a delay and interleave worked examples with new attempts.

Before code: picture, plain-language procedure, trace, pseudocode, then syntax explanation. No code lab assumes an untaught library. Existing code is audit material, not automatic chapter content.

## EVOU-01

**Worked example / exercise ladder:** Recognize an analogy; identify a missing mechanism; explain that ordinary software can also respond and change.

**Code or hands-on progression:** Paper comparison of what is stored, what changes and what is observed; no new code.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-02

**Worked example / exercise ladder:** Trace both histories; test a reset; distinguish the current input, remembered state and stored instructions.

**Code or hands-on progression:** Refresh Book I Python functions, dictionaries and tests, then build a two-command stateful program.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-03

**Worked example / exercise ladder:** Compute one prediction; compare two trial settings; distinguish fitting examples from success on new ones.

**Code or hands-on progression:** Plain Python predictions and a short table of trial parameter choices; keep training and inference functions separate.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-04

**Worked example / exercise ladder:** Identify leakage; compute a mean error; explain why one run is insufficient evidence.

**Code or hands-on progression:** Create a tiny split with duplicate detection; keep an untouched test file.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-05

**Worked example / exercise ladder:** Compute a tiny product; label axes; diagnose an accidental broadcast.

**Code or hands-on progression:** Plain Python arrays with shape labels and a paper tensor-layout exercise; PyTorch tensor construction and setup wait for Chapter 8.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-06

**Worked example / exercise ladder:** Compute a slope; show an overly large step; explain local improvement versus a global guarantee.

**Code or hands-on progression:** Calculate a finite-difference gradient in plain Python and compare a hand-derived scalar gradient.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-07

**Worked example / exercise ladder:** Compute two neurons; compare linear compositions and nonlinear layers; trace one gradient path.

**Code or hands-on progression:** Tiny scalar network first, then batched matrix forward pass; no large architecture.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-08

**Worked example / exercise ladder:** Repair a missing gradient reset; reproduce a tiny run; verify parameters are unchanged by inference.

**Code or hands-on progression:** Teach installation, tensors, autograd, zero_grad, backward and step; separate no-update inference and evaluation behavior.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-09

**Worked example / exercise ladder:** Distinguish a character from a token; compute a tiny normalized distribution; prevent future-token leakage.

**Code or hands-on progression:** Build a tiny tokenizer and embedding lookup, then a next-token table baseline.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-10

**Worked example / exercise ladder:** Compute two steps; compare histories; test reset boundaries and explain why memory is not yet learning.

**Code or hands-on progression:** Exact rational leaky example before a small trained RNN; distinguish hand-set recurrence from learning.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-11

**Worked example / exercise ladder:** Trace a gate at zero and one; compare state sizes; state what information a compact state may lose.

**Code or hands-on progression:** Implement a small GRU and a declared linear SSM baseline before contemporary variants.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-12

**Worked example / exercise ladder:** Compute weights; explain query/key/value roles; demonstrate a causal-mask failure.

**Code or hands-on progression:** Hand-compute a three-token example, then plain tensors and autograd parity checks.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-13

**Worked example / exercise ladder:** Trace one token through a block; explain why position matters; reject a full architecture diagram with unlabeled axes.

**Code or hands-on progression:** Build one small causal block and test shape, masking and checkpoint reload before stacking.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-14

**Worked example / exercise ladder:** Distinguish recurrent state, KV cache and retrieved documents; test stale-cache and mismatched-history cases.

**Code or hands-on progression:** Compare cached and uncached tiny-model outputs; build a tiny exact retrieval index.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-15

**Worked example / exercise ladder:** Find a duplicate-name bug; compare costs honestly; explain why selective execution alone is not novel.

**Code or hands-on progression:** Rebuild the old dispatch example with explicit errors, purity assumptions and counted events.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-16

**Worked example / exercise ladder:** Trace a route; identify collapse; distinguish sparsity from an established end-to-end speedup.

**Code or hands-on progression:** Implement a tiny routed baseline with a matched dense control; report routing cost as well as expert work.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-17

**Worked example / exercise ladder:** Match objects to stages; distinguish process from thread; explain interpreter and runtime without treating them as synonyms.

**Code or hands-on progression:** Build a tiny expression interpreter before optional compilation; document an API with inputs and failure outputs.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-18

**Worked example / exercise ladder:** Trace request identity; compare batching tradeoffs; distinguish a cache from an authoritative database.

**Code or hands-on progression:** Single-process simulated service and queue; no production deployment required.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-19

**Worked example / exercise ladder:** Design a falsifier; expose answer leakage; explain why an oracle checks a task but does not certify intelligence.

**Code or hands-on progression:** Shared experiment contract for Markov, MLP, CNN, GRU, Transformer and SSM baselines; teach Markov assumption with a small transition table here.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-20

**Worked example / exercise ladder:** Distinguish control from sequence reversal; classify state change, gene expression and inherited change.

**Code or hands-on progression:** Revisit a toy control example next to an ordinary stateful software baseline.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-21

**Worked example / exercise ladder:** Reject a renamed existing mechanism; propose a discriminating experiment; leave an unsupported claim open.

**Code or hands-on progression:** Write a mechanism contract and a nearest-baseline checklist before any genomic class.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-22

**Worked example / exercise ladder:** Classify changes; track who evaluates candidates; identify evaluation-set reuse and selection bias.

**Code or hands-on progression:** Compare parameter fitting, pruning and small program search under a declared budget.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-23

**Worked example / exercise ladder:** Find an invalid type; distinguish expansion from learning; identify the biological details intentionally absent.

**Code or hands-on progression:** Build a tiny checked expression plan from a declarative source.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-24

**Worked example / exercise ladder:** Derive one transition; exhibit nearest-baseline equivalence; write a condition that would falsify the additional mechanism.

**Code or hands-on progression:** Specify a small deterministic reference before neural implementations; all novelty claims remain hypotheses.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-25

**Worked example / exercise ladder:** Distinguish class from instance; repair an ownership edge; test interface preconditions.

**Code or hands-on progression:** Reference classes follow the Chapter 24 contract; class diagram names must match code.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-26

**Worked example / exercise ladder:** Trace one request; detect a backwards message; compare diagram events to recorded code events.

**Code or hands-on progression:** Single-request reference execution with deterministic trace IDs and explicit failures.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-27

**Worked example / exercise ladder:** Explain why a logged route is not a causal proof; identify missing provenance; propose a controlled intervention.

**Code or hands-on progression:** Trace-based ablation harness with a counterfactual baseline where well-defined.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-28

**Worked example / exercise ladder:** Reject an untested transition; preserve the old version; distinguish bounded validation from universal correctness.

**Code or hands-on progression:** Pending, validated, tested, accepted and rejected states with illegal-transition tests.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-29

**Worked example / exercise ladder:** Audit a training loop; test frozen-structure behavior; report an inconclusive or negative outcome correctly.

**Code or hands-on progression:** Small PyTorch candidate with identical evaluation interface to Chapter 19; no large-run result invented.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-30

**Worked example / exercise ladder:** Trace a component failure; test parameter immutability; compare class and component diagrams.

**Code or hands-on progression:** Reference runtime with backend adapter; inference must not silently train or accept structural edits.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-31

**Worked example / exercise ladder:** Find a missing configuration field; distinguish matching filename from matching model; reject silent fallback.

**Code or hands-on progression:** Round-trip serialization tests, schema validation and explicit incompatible-version errors.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-32

**Worked example / exercise ladder:** Detect cross-request leakage; calculate capacity; explain why recurrent state and KV have different contracts.

**Code or hands-on progression:** Small memory-manager simulation with isolation, eviction and reset tests.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-33

**Worked example / exercise ladder:** Calculate waiting times; identify starvation; compare a throughput gain with tail-latency cost.

**Code or hands-on progression:** Discrete-event serving simulator with declared arrival traces; no production performance claim.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-34

**Worked example / exercise ladder:** Reject unequal workloads; diagnose a tolerance failure; separate logical-event counts from elapsed time.

**Code or hands-on progression:** Reference-versus-optimized harness with warm-up, synchronization and hardware/version records.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-35

**Worked example / exercise ladder:** Distinguish authentication from authorization; trace rollback state; redact a sensitive log.

**Code or hands-on progression:** Local deployment diagram and failure-injection exercise; no live service or credentials required.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-36

**Worked example / exercise ladder:** Separate bug, underpowered test and refuted claim; write a transparent negative-result report.

**Code or hands-on progression:** Archive all declared runs, including crashes and null results; use synthetic records only when explicitly labeled.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-37

**Worked example / exercise ladder:** Separate name, architecture and evidence; design a symmetry control; leave an unverifiable claim unresolved.

**Code or hands-on progression:** Re-audit source, dataset splits, checkpoints and licenses before experiments; runnable substitutes are clearly labeled.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-38

**Worked example / exercise ladder:** Identify hidden retraining; compare retention and transfer; report costs of population search.

**Code or hands-on progression:** Two-task forgetting study with frozen controls and explicit adaptation budgets.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-39

**Worked example / exercise ladder:** Reject a unit-test-to-AGI inference; propose disconfirming tests; state the limits of the chosen definition.

**Code or hands-on progression:** Generate a scorecard from actual experiment records; unknown cells stay unknown.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## EVOU-40

**Worked example / exercise ladder:** Present the strongest bounded claim, a failed alternative and the next falsifying experiment.

**Code or hands-on progression:** Release a small reproducible package with source, UML, tests, records and limitations; publication and rights gates remain explicit.

**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, then an independent task with answer notes. Ask the learner to explain one wrong answer.

## Training-code route

EVOU-03 manual parameter trials → EVOU-06 finite-difference gradient → EVOU-07 tiny network → EVOU-08 complete PyTorch loop → EVOU-09 sequence objective → EVOU-10–13 architecture-specific models → EVOU-19 common controls → EVOU-29 candidate training → EVOU-36 failures.

## Inference-code route

EVOU-03 fixed-parameter prediction → EVOU-08 no-update evaluation → EVOU-14 cache parity → EVOU-17–18 interpreter and service → EVOU-26 traced request → EVOU-30 runtime → EVOU-31 identity → EVOU-32–35 memory, scheduling, profiling and rollback.

## Experiment progression

Exact hand cases → independent checkers → untouched splits → repeated seeds → nearest conventional baselines → declared matched budgets → one-mechanism ablations → failed hypotheses → transfer. No training or benchmark is run in this planning milestone.
