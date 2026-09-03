# Chapter 1 - What Would It Mean for a Program to Behave Like a Genome?

After this chapter, you will be able to state the central Evolutor question as computer science rather than metaphor. You will be able to distinguish persistent structure, regulation, expression, trace, and structural change, and you will be able to run the smallest executable example of that separation.

## 1.1 A genome is not merely a long program

Ordinary software already has persistent code, conditional branches, dynamically loaded modules, configuration, logs, and updates. Renaming these familiar pieces *genes*, *promoters*, *expression*, and *evolution* would not create a new computational model. A genomic approach becomes interesting only when it commits to a precise organization that changes which questions can be asked and measured.

The motivating contrast is captured in [E02 — Stored genome to contextual expression](../diagrams/e02-genome-compile-regulate-express.txt). The graph separates persistent and transient artifacts, records suppressed as well as expressed structure, and keeps regulation cost inside the account.

The right side asserts more structure. It separates what is stored from what is expressed, makes the selection mechanism explicit, treats the execution trace as a semantic output, and restricts how persistent structure may change.

Whether this organization is useful is an open research question. It must earn its value through clearer semantics, stronger guarantees, or measured behavior.

## 1.2 The five-part GCS proposal

Evolutor v1.4.1 defines a Genomic Computation System as a tuple

\[
\mathcal{G}=
(\Sigma,\mathrm{Genome},\mathrm{Reg},\mathrm{Expr},\mathrm{Evo}).
\]

The components play different roles.

### Alphabet \(\Sigma\)

The alphabet supplies the finite symbols or codons from which persistent programs are represented. “Codon” here is formal terminology. Unless a molecular compiler is specified, it is not a biological codon and need not use the DNA alphabet.

### Genome \(\mathrm{Genome}\)

The genome is persistent typed computational structure. A gene may carry a name, signature, regulatory condition, and body. Persistence means that the structure survives across executions until an allowed update changes it. Typing is intended to rule out malformed composition before or during execution.

### Regulation \(\mathrm{Reg}\)

Regulation maps a context and possibly current state to gate decisions or an expression plan. It answers: which stored components are eligible to act now? If evaluating regulation is expensive, that cost must be counted; selection is not free merely because unselected code does not run.

### Expression \(\mathrm{Expr}\)

Expression executes the selected structure and returns an output, a new store, or both. In the theory, expression is represented by a machine state resembling

\[
\langle S,x,\rho,\kappa,\gamma,\Omega\rangle,
\]

where \(S\) is a compiled substrate, \(x\) the context, \(\rho\) a store, \(\kappa\) a frontier or worklist, \(\gamma\) the gate map, and \(\Omega\) a trace.

### Evolution \(\mathrm{Evo}\)

Evolution is a family of permitted structural changes. The word does not imply autonomous intelligence, natural selection, or improvement. An update deserves stronger language only when its proposal mechanism, verification conditions, selection rule, and evidence are explicit.

## 1.3 The stored program and the expressed program

The central architectural bet is that a large persistent structure can support a smaller context-specific execution.

For context \(x\), write the fired subset as

\[
\mathrm{Expr}_x(\mathrm{Genome}).
\]

Evolutor defines expression complexity through the size of this subset:

\[
\mathrm{EC}_G(n)=
\max_{|x|=n}
\left|\mathrm{Expr}_x(G)\right|.
\]

This is a useful proposed measure, but it is not a complete runtime equation. A system may spend substantial work deciding what to express, routing data, evaluating primitives, maintaining the worklist, or reading external memory. Later chapters will therefore keep separate terms for regulation, expression, scheduling, primitive operations, compilation, and I/O.

The narrower claim is valuable: counting expressed structure makes selective execution visible. Whether it predicts wall-clock cost is empirical and implementation-specific.

## 1.4 Compilation makes the proposal executable

The source theory compiles a genome into a substrate

\[
S=\mathrm{compile}(\mathrm{Genome})
=(N,A,\mathrm{sig},\mathrm{gate},\mathrm{succ}),
\]

where nodes represent operations, arcs represent dependencies, signatures carry type information, gates associate regulatory conditions, and successors support scheduling.

This resembles a compiler or query engine because stored declarative structure becomes an executable plan. The analogy is helpful but incomplete. A database optimizer is normally free to choose equivalent plans; a GCS trace may make the chosen mechanism part of the observable semantics. Structural evolution also changes the persistent program rather than merely selecting a plan for one request.

MiniEvolutor implements the smallest form of this pipeline:

```python
genome = Genome(
    genes=(
        Gene(
            name="add",
            inputs=("left", "right"),
            output="total",
            operation=lambda values: values["left"] + values["right"],
            output_type=int,
            gate=lambda context: context["mode"] == "sum",
        ),
    ),
    external_inputs=("left", "right", "mode"),
    outputs=("total",),
)

substrate = compile_genome(genome)
context = {"left": 2, "right": 3, "mode": "sum"}
plan = regulate(substrate, context)
result = ExpressionMachine().execute(plan, context)

assert result.outputs == {"total": 5}
```

The example is intentionally ordinary. Its purpose is to expose interfaces, not to impress with behavior.

## 1.5 What the reference implementation actually guarantees

The current MiniEvolutor compiler checks unique names and outputs, known dependencies, external/output interfaces, and acyclic scheduling. Regulation evaluates context-only Boolean gates. Expression checks that enabled genes have their inputs, validates Python output types, counts fired genes, and records gate/fire/skip events.

These are implemented mechanisms backed by tests. They do not yet establish the full GCS theory.

The reference omits:

- a parser and complete typed codon language;
- a formal store-typing judgment;
- dynamic or staged regulation;
- concurrency and nondeterministic scheduling;
- resource-bounded primitives;
- trace provenance hashes and serialization;
- a sound policy language;
- behavioral equivalence for edits;
- autonomous structural search.

By listing omissions beside guarantees, the implementation remains a semantic foothold rather than a demo that silently claims completeness.

## 1.6 Traces as outputs, not decorations

Many systems produce logs, but Evolutor gives the trace a stronger proposed role. A trace may record gate decisions, fired nodes, emitted values, provenance, state changes, and edit certificates. If the trace is faithful, it can support debugging, accounting, replay, targeted search, or explanations of which structure participated in an output.

These possible uses require separate evidence. A trace can be perfectly faithful yet too large to store. It can identify executed nodes without explaining why a learned component produced a value. Restricting edits to traced regions may reduce search, or it may prevent discovery of useful dormant structure.

“Mechanistic” should therefore mean that trace events correspond to declared machine transitions. It should not be used as a synonym for human-understandable or causally sufficient.

## 1.7 Verified structural change

A proposed update can be written abstractly as

\[
G_{t+1}=\mathcal{E}(G_t,\Omega_t,\mathcal{L}_t),
\]

where the update may depend on the current genome, its trace, and a loss or evaluation signal. Before acceptance, a verifier may check typing, interfaces, effects, resource bounds, and policy invariants.

MiniEvolutor currently supports only a one-gene replacement and verifies that external and output interfaces remain stable and that the candidate still compiles. It explicitly does not prove behavioral equivalence or policy safety.

This small contract illustrates an important division of authority. [E04 — Verified local evolution loop](../diagrams/e04-verified-evolution-loop.txt) separates the observation bundle, proposal mechanism, static verifier, controlled evaluation, rejection record, and versioned acceptance.

Proposal, verification, and selection should remain separable even if one implementation later automates all three.

## 1.8 What would make the model genuinely distinctive?

The GCS vocabulary alone is not enough. A compelling theory or system should answer at least one of these questions better than ordinary abstractions:

- Does a typed persistent genome make structural adaptation safer or more reproducible?
- Does explicit regulation reduce executed work after its own overhead is counted?
- Do faithful traces improve debugging or learning?
- Do verified edits preserve useful invariants across structural search?
- Is expression complexity predictive of measured resource use?
- Can multiple execution backends share a genome representation without erasing their semantics?

These are falsifiable research questions. A negative answer would narrow the theory; it would not make the investigation worthless.

## What this chapter established

- Evolutor proposes a five-part separation among alphabet, persistent genome, regulation, expression, and structural evolution.
- The stored genome and expressed structure are different objects.
- Expression complexity is a proposed structural measure, not automatically wall-clock runtime.
- MiniEvolutor implements a small deterministic compile/regulate/execute/trace contract.
- Structural proposals, verification, and selection should be separate responsibilities.

## What remains unverified

- The full typed language and small-step semantics are not implemented.
- The v1.4.1 universality and regulation-depth claims still have proof obligations.
- No experiment here shows that traces improve learning or explanation.
- No benchmark shows that regulated expression beats a generic router after overhead.
- A portable genomic IR and optimized runtime are future hypotheses, not present results.
