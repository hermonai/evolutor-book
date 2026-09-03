# Chapter 3 - The Correction Record as Method

After this chapter, you will be able to treat a correction as a change to a research dependency graph rather than an embarrassing footnote. You will be able to contain an invalid result, classify its failure, design a corrected contract, and decide which claims may be reinstated.

## 3.1 Why this chapter comes before the new theory

An ambitious research program is especially vulnerable to accumulating plausible but unsupported stories. Evolutor combines formal semantics, neural models, runtime systems, biological inspiration, and structural learning. A defect in one layer can travel through shared vocabulary into all the others.

The inherited DOGMA work supplies a valuable correction record: future-token leakage, a hidden state cap, capacity-matching confounds, a mean that hid heterogeneous seeds, a gameable retrieval oracle, a mechanism that failed causal tests, and biological language stronger than the implementation justified.

The important fact is not that earlier work was imperfect. All research is. The important fact is that these failures reveal where the method must place gates. They are design inputs for the new program.

[E15 — Correction record as an active research subsystem](../diagrams/e15-correction-record-loop.txt) is the canonical process. An active claim produces testable expectations. Adversarial probes generate anomalies or counterevidence. The defect is classified, affected descendants are contained, a corrected contract is versioned, and only a rerun plus dependency review can reinstate a conclusion.

## 3.2 A correction is not deletion

Deleting a failed result destroys information. It hides how the claim was formed, prevents readers from learning the failure signature, and makes the same mistake easier to repeat. Leaving the result unmarked is equally harmful because later work may continue to cite it.

A proper correction preserves two histories:

1. the **artifact history** — code, configuration, data identity, checkpoint, metrics, and logs that produced the result;
2. the **epistemic history** — what was claimed, why it seemed supported, what failed, and which wording now survives.

The old artifact remains immutable. Its status changes. A new record may supersede it, but it does not overwrite it.

## 3.3 The claim-state machine

An Evolutor claim can occupy several states:

- `PROPOSED`: precisely stated but not yet tested or proved;
- `ACTIVE`: currently used, with identified support and scope;
- `QUARANTINED`: a material anomaly exists and interpretation is suspended;
- `NARROWED`: a smaller claim survives after a dependency failed;
- `WITHDRAWN`: available evidence no longer supports the claim;
- `SUPERSEDED`: a later definition or experiment replaces it;
- `REINSTATED`: a corrected independent evaluation again supports a scoped form.

Transitions require reasons and artifact links. A claim cannot move from `QUARANTINED` to `ACTIVE` because the corrected number looks better. It moves only when the failure mechanism has been addressed and the corrected contract passes.

Containment comes first. When a causal mask is wrong, every checkpoint trained under it is marked affected before a replacement training run begins. When a theorem dependency is missing, later propositions that use it are blocked before the proof is repaired. This order prevents an attractive downstream result from weakening the correction.

## 3.4 Failure class one: semantic leakage

In the inherited recurrent work, multiple layers allowed future tokens to affect earlier logits. Tiny-gradient probes did not reliably expose the problem. The apparent causal model therefore did not implement the claimed information boundary.

The standing correction is a finite intervention. Hold a prefix fixed, replace the future suffix with a materially different suffix, and compare all prefix outputs:

\[
f(x_{\le t},x_{>t})_{\le t}
\stackrel{?}{=}
f(x_{\le t},x'_{>t})_{\le t}.
\]

This test targets behavior, not an indirect symptom. It runs for every architecture path and relevant checkpoint. Gradients may supplement it, but they do not replace it.

The broader method is: translate a semantic claim into an adversarial intervention at the exact boundary the claim asserts.

## 3.5 Failure class two: hidden capacity

A default scan-state dimension was capped below the intended value. Comparisons labeled by nominal model size were therefore comparisons of different actual capacities, and conclusions changed when the real state dimension was exposed.

The correction is not merely to raise the cap. Every artifact must record the resolved runtime dimension after defaults, clamps, and derived configuration are applied. Experiments sweep the actual state budget. Tests fail when a requested dimension is silently changed.

This lesson generalizes. Configuration is executable semantics. The effective model is the one instantiated after defaults and constraints, not the one described in a command line or paper table.

## 3.6 Failure class three: one matching rule called fairness

Equal parameter count produced unequal width and state capacity. An observed effect could therefore be attributed to the named mechanism even though a hidden dimension supplied the advantage.

No single matching rule eliminates every confound. Evolutor records at least parameter count, representation width, explicit state capacity, training compute, inference compute, and memory growth. Each comparison states which quantity was controlled and which remained different.

This changes the language of conclusions. Instead of “architecture A is better than B,” the record says that A improved a named metric under parameter matching, while the advantage did or did not persist under width, state, and compute controls.

## 3.7 Failure class four: aggregates that erase modes

A mean combined failed and successful seeds into a moderate-looking result. The aggregate was arithmetically correct but scientifically misleading because it described no stable behavior.

The correction makes the seed table primary. Learning curves, final metrics, failure modes, and stopping events remain visible for every run. Aggregates are computed only after inspection, and multimodality or catastrophic runs are described rather than averaged away.

Adding seeds estimates variability. It does not turn a bimodal mechanism into a reliable one. The research question may need to change from “what is the mean effect?” to “what determines which regime a run enters?”

## 3.8 Failure class five: a gameable oracle

Some retrieval variants measured starvation, output-space effects, or shortcuts rather than the intended memory capability. A model could score well for reasons unrelated to the proposed mechanism, while an expected baseline ranking failed.

The standing response is an oracle audit before expensive training:

1. solve the task with trivial constant, frequency, recency, and shortcut baselines;
2. verify that input generation makes the target identifiable;
3. check whether the output vocabulary or loss leaks target frequency;
4. establish the expected ranking of perfect, partial, and non-solving strategies;
5. perturb the intended evidence and confirm that performance changes.

A benchmark is a measuring instrument. If it can be gamed, it must be corrected and all dependent results quarantined.

## 3.9 Failure class six: metric gain without the claimed mechanism

A proposed Boolean or XOR explanation failed ablation and transplant tests. The larger system may still have produced a useful metric, but the stated causal story did not survive intervention.

This distinction is foundational. A performance claim and a mechanism claim are separate nodes. If removing the mechanism does not remove the effect, or transplanting it does not transfer the effect, the mechanism claim is withdrawn even when the performance result remains.

Evolutor will use the same discipline for genomic proposals. A trace-aware model that improves accuracy does not show that the trace caused the gain until trace interventions distinguish it from capacity, optimization, or generic auxiliary supervision. A regulated model does not establish a special genomic principle until it beats an operationally equivalent generic router.

## 3.10 Failure class seven: biological overclaim

Neural features initialized from biological constants were described as if they had physical meaning. Initialization can encode a prior, but learned parameters, normalization, data, and objective can move the model far from the motivating quantity.

The correction is an evidence boundary. A parameter may be *inspired by* complementarity, binding, regulation, or temperature. It becomes a physical estimator only after calibration and validation against appropriate measurements. Biological names do not supply that bridge.

This rule protects both sides of the project. Biology remains accurately represented, and software hypotheses can be explored without pretending they already realize biology.

## 3.11 Corrections propagate through dependencies

A defect has a blast radius. Let claim (C_i) depend on artifacts or claims (D_i). If (d\in D_i) is invalidated, (C_i) must be reviewed even if its own final metric or proof text did not change.

The review asks:

- Was the failed dependency necessary or merely contextual?
- Can the conclusion be narrowed to exclude it?
- Are checkpoints, plots, tables, or downstream theorems affected?
- What new test would distinguish repair from cosmetic change?
- Does an independent implementation or dataset need to be added?

[E05 — Theorem dependency graph and blocked obligations](../diagrams/e05-theorem-dependencies.txt) applies the same method to formal work. The depth hierarchy and trace-count branches remain visibly blocked; they cannot become premises through repeated citation.

## 3.12 The corrected experimental contract

For neural experiments, [E16 — Training, evaluation, and artifact provenance](../diagrams/e16-training-evaluation-flow.txt) makes the manifest an input to training. It binds source identity, data hashes, resolved architecture, budgets, seeds, metrics, interventions, checkpoints, and raw results.

A corrected contract adds a field for the correction it addresses and the adversarial test that would have caught the original failure. This converts experience into a regression guard. Examples include:

- finite suffix interventions for causality;
- assertions on resolved state dimensions;
- multi-axis capacity tables;
- mandatory per-seed output;
- trivial and shortcut benchmark baselines;
- component ablation and transplant;
- biological-claim labels and calibration requirements.

The next failure will not necessarily fit these seven classes. The point is to make the system extensible: a new correction adds a new gate without erasing the old path.

## 3.13 When may a claim return?

Reinstatement requires more than repairing code. The corrected run must start from fresh initialization when the original checkpoint learned under invalid semantics. It must use immutable artifacts. It must pass the new regression test, the ordinary integrity gates, and any independent replication appropriate to the claim.

The reinstated wording may still be narrower. If a corrected result holds only at one state dimension or on one benchmark family, that scope becomes part of the claim. If the metric returns but the mechanism test still fails, only the performance node can return.

Some claims should remain withdrawn. Preserving that outcome is a sign that the correction system worked.

## 3.14 Correction as a source of architecture

The seven inherited failures now shape the research architecture itself:

- causality is tested by intervention;
- state dimensions are explicit interface data;
- comparison reports carry multiple capacity views;
- seed-level artifacts are first-class;
- tasks ship with oracle audits;
- mechanism claims require causal ablation;
- biological bridges require separate validation.

The correction record is therefore not behind the work. It is inside the work. It determines APIs, schemas, tests, chapter order, and the permitted strength of conclusions.

## What this chapter established

- A correction changes artifacts, claim status, and downstream dependencies.
- Containment precedes repair and preserves invalidated artifacts with visible status.
- Seven inherited failure classes produce concrete standing gates for Evolutor.
- Performance and mechanism claims can have different fates.
- Reinstatement requires a corrected contract, fresh evidence, and dependency review.
- Negative and withdrawn results are durable outputs of the research program.

## What remains unverified

- The correction workflow is documented but not yet enforced by an automated artifact registry.
- Fresh controlled DOGMA/Hermon DNA experiments have not yet exercised every standing gate.
- The dependency graph between all manuscript claims and executable artifacts is incomplete.
- Independent reviewers have not yet tested whether the correction categories and reinstatement criteria are sufficient.
