# Chapter 2 - Five Layers That Must Not Be Collapsed

After this chapter, you will be able to place an Evolutor claim in the correct layer, identify what kind of artifact could support it, and understand why the DOGMA/Hermon naming conflict is a scientific provenance problem rather than a branding detail.

## 2.1 One program, several kinds of truth

Evolutor crosses biology, formal computer science, machine learning, and systems engineering. A sentence that is sensible in one layer may be false in another. To keep the program coherent, this book separates five layers:

```text
1. BIOLOGY
   observed or experimentally supported living/molecular mechanisms

2. FORMAL COMPUTATION
   alphabets, genomes, transition systems, semantics, proofs, cost models

3. EXECUTABLE REFERENCE
   Python programs that implement a declared subset of the semantics

4. MACHINE-LEARNING ARCHITECTURE
   parameterized models, objectives, data, training, and experiments

5. SYSTEMS RUNTIME
   kernels, memory, scheduling, batching, serving, and hardware behavior
```

A possible molecular implementation would connect layers one and two through a separate compiler and experimental program. It is not assumed by the current software.

## 2.2 Biology supplies phenomena, not software guarantees

Genomes persist. Gene expression depends on context. Regulatory networks contain feedback. Mutation and selection change populations over time. These biological facts can motivate computational questions.

The abstraction step must state what is retained and what is discarded. A formal gate may retain context-dependent enablement while omitting binding kinetics, concentrations, chromatin, cellular compartments, noise, and energy. Calling the gate a *promoter* does not restore those omitted mechanisms.

Biological inspiration is most useful when it generates a precise, testable design constraint: persistent typed modules, complement symmetry, local interaction, bounded edits, or explicit expression traces. It becomes weakest when it supplies only names.

## 2.3 Formal computation supplies definitions and obligations

The formal layer decides what a GCS is. It defines the genome, regulation stages, expression transitions, traces, and cost measures. Here, validity is mathematical. A theorem may be correct even if no fast implementation exists, and a fast program may exist without proving the theorem.

Evolutor v1.4.1 contains theorem-shaped claims about type preservation, policy safety, universality, expression-bounded runtime, sparse pointer retrieval, regulation-depth hierarchy, generalization, trace-restricted search, and verified descent.

The theorem ledger does not assign all of them the same status. Some are standard consequences after assumptions are formalized. Some have proof sketches. Some have material gaps. In particular:

- expression runtime must include gate, primitive, scheduling, and I/O costs unless bounded;
- the sparse-pointer lower bound applies to the defined Local Interaction Model, not to every sequence architecture;
- the v1.4.1 regulation-depth proof does not yet establish the stated strict hierarchy;
- average trace support does not automatically bound the union of editable locations across a dataset.

An executable example can find counterexamples and clarify definitions, but it cannot replace these proofs.

## 2.4 The executable reference supplies semantic tests

MiniEvolutor and `evo_torch` sit at the executable-reference layer. Their job is clarity.

MiniEvolutor turns a small genome into a topological substrate, evaluates gates, executes enabled genes, checks output types, and emits a trace. Its tests establish those behaviors for the implemented subset.

`evo_torch` provides an ordinary causal Transformer and an ordinary GRU. Both accept `[batch, time]` tokens and produce `[batch, time, vocabulary]` logits. The GRU exposes carried state; the Transformer reference recomputes the prefix. Tests compare full-sequence and incremental semantics.

The causality test performs a finite intervention:

\[
y_{\le t}(x_{\le t},x_{>t})
=
y_{\le t}(x_{\le t},x'_{>t})
\]

within a declared numerical tolerance. This is stronger for detecting gross future leakage than observing tiny gradients at initialization.

These programs are baselines, not novel genomic models. Their ordinariness is essential: future mechanisms need controls.

## 2.5 Machine learning supplies measured behavior

At the ML layer, truth comes from a frozen experimental contract. A claim about predictive quality needs data, splits, objectives, budgets, seeds, checkpoints, metrics, uncertainty, and code identity. A claim about a component's effect additionally needs ablation and an appropriate generic control.

Four matching conventions answer different questions:

| Convention | Holds approximately fixed | Leaves potentially different |
| --- | --- | --- |
| parameter matched | trainable scalar count | width, state, FLOPs, memory |
| width matched | representation width | parameters and compute |
| state-capacity matched | carried or addressable state budget | width and parameters |
| compute matched | declared training/inference compute | representation and memory |

No convention produces universal fairness. Reporting several can reveal whether a result is robust or merely moves with hidden capacity.

The inherited correction record makes this concrete. Earlier DOGMA work contained future-token leakage, a hidden state cap, parameter/width confounds, a mean that hid a failed seed, a gameable retrieval oracle, and a falsified mechanism hypothesis. The lesson is not that experimentation is hopeless. It is that controls must be part of the architecture.

## 2.6 The runtime supplies operational facts

The systems layer asks different questions: how state is laid out, how requests are batched, whether memory grows with context, which kernels dominate latency, how precision affects parity, and what happens under failure.

A Transformer may use a KV cache for incremental decoding. A recurrent model may carry fixed-shaped state. A symbolic GCS may carry a store, worklist, expression plan, and trace. A common serving API might route all three, but their internal memory and scheduling are not interchangeable.

An optimized runtime must reproduce the semantic reference within a declared tolerance. Faster code that computes a different recurrence or mask is not an optimization of the same model.

Runtime measurements also remain hardware- and workload-specific. Constant state per sequence does not prove good retrieval. Efficient attention kernels do not prove better statistical learning. Each fact stays in its layer.

## 2.7 Architecture names are provenance keys

The current corpus uses DOGMA for a recurrent non-transformer model and engine. The current Hermon repository implements Transformer-oriented serving machinery including attention and paged KV. The intended future taxonomy proposes the opposite association: DOGMA for a Transformer DNA line and Hermon DNA for a non-transformer line.

If names changed without qualification, a reader could mistakenly attach recurrent measurements to a Transformer or Hermon's paged-KV implementation to a future recurrent model. That would contaminate evidence even if every individual number were copied correctly.

During the transition, this book uses:

- **DOGMA-R** for historical/current recurrent DOGMA;
- **Hermon Engine** for historical/current Transformer serving;
- **DOGMA-T** for the proposed Transformer DNA line;
- **Hermon DNA-R** for the proposed non-transformer line.

These are documentation qualifiers, not repository renames. A later migration requires architecture IDs in checkpoints and artifacts that do not depend on branding.

## 2.8 How evidence moves between layers

Evidence can connect layers only through an explicit bridge.

```text
biological phenomenon
      |
      | abstraction with declared omissions
      v
formal operator
      |
      | implementation + semantic tests
      v
executable reference
      |
      | frozen training/evaluation protocol
      v
measured model result
      |
      | parity + profiling + hardware record
      v
runtime result
```

Moving upward is not automatic. A biological observation suggests a formal operator. It does not prove that the operator helps learning. A PyTorch implementation enables an experiment. It does not prove a runtime advantage. A kernel benchmark establishes performance on its hardware and shapes. It does not validate the theory's broader claims.

## 2.9 A rule for ambitious work

Ambition and discipline reinforce one another when every large claim can be decomposed into smaller claims with clear failure conditions.

“Genomic computation is a new foundation for machine intelligence” is not directly testable. The following are:

- a typed genome compiler rejects a specified class of invalid edits;
- expression complexity predicts measured executed nodes under a named scheduler;
- trace-restricted proposals reduce search cost without reducing solution quality on a benchmark;
- a reverse-complement-equivariant model improves sample efficiency under fixed budgets;
- a recurrent state model extrapolates on a running-state task but fails exact retrieval;
- an optimized engine matches PyTorch outputs and state within tolerance.

The research program becomes credible by accumulating or rejecting such bounded statements.

## What this chapter established

- Biology, formal computation, executable references, ML architectures, and systems runtimes use different standards of evidence.
- Code tests semantics; experiments measure behavior; neither automatically proves formal theorems.
- Architecture comparisons need multiple capacity views and intervention-based causality.
- Runtime parity is part of model correctness.
- DOGMA/Hermon names currently conflict with the proposed target taxonomy, so qualified lineage names are necessary.

## What remains unverified

- No GCS-specific neural mechanism has yet surpassed ordinary controls in this repository.
- The full theorem audit is not complete across Evolutor v1.4.1 and v1.7.0.
- No common serving protocol has been justified.
- No molecular compiler or wet-lab realization exists here.
- The final public naming migration remains undecided.

