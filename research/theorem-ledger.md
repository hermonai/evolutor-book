# Theorem reset ledger

The historical ledger's IDs T01–T15 remain historical IDs. The classifications below screen its stated claims and proof obligations; they are **not** a completed line-by-line audit of every original paper version. Full v1.4.1-to-v1.7 proof review remains blocked from publication until original statements and proof deltas are checked.

| Old ID | Restated target / assumptions | Attack or missing step | Decision |
| --- | --- | --- | --- |
| T01 | Typed execution preserves store typing under typed total primitives | Arbitrary Python callable or untyped external result breaks assumption | REPAIR with full syntax and transitions |
| T02 | Every allowed step preserves a semantic safety policy | Interface validation alone does not constrain external effects | WEAKEN; current code is structural validation only |
| T03 | GCS simulates an unbounded machine with explicit memory/iteration | Finite acyclic executable subset cannot establish it | RESEARCH AGAIN; require encoding and simulation |
| T04 | Runtime bounded by expression work under costed routing/primitives | All gates disabled gives zero firings and nonzero routing work | REPLACE with total cost semantics |
| T05 | A particular SPR algorithm has a linear expression bound | Gate scan, query availability and costs omitted | REPAIR with executable construction |
| T06 | Local synchronous information travels at most one edge per round | Asynchronous “round” can hide sequential propagation | KEEP CONCEPT as a standard locality lemma |
| T07 | Specified LIM model incurs a quadratic interaction cost | Different output location, indexed access or scheduler defeats transfer | WEAKEN to exact restricted model |
| T08 | Pointer chasing admits a claimed regulation-depth upper bound | Pointer accessibility must be paid for per stage | RESEARCH AGAIN |
| T09 | Strict depth hierarchy from communication simulation | \(k+O(1)\) bound does not establish a strict \(k\)-stage separation | BLOCKED until exact round/message argument |
| T10 | A size-bounded genome class is finite | Unbounded constants or names yield infinitely many programs of one node | REPAIR with finite bit encoding |
| T11 | Finite-class uniform convergence under bounded iid loss | Training objective is not automatically population risk | KEEP CONCEPT as standard learning theory |
| T12 | Average trace support bounds editable union | Disjoint supports of size one over \(N\) samples have union \(N\) | REJECT this inference; derive union-aware bound |
| T13 | Exact local minimization with identity candidate is monotone | Monotonicity alone gives no finite termination or generalization | WEAKEN to non-increase |
| T14 | Sound verified invariant preservation composes over edits | Unsound verifier or unmodeled non-edit steps breaks induction | KEEP CONCEPT as standard induction |
| T15 | Revised v1.7 results repair older claims | No full proof delta checked in this reset | UNVERIFIED |

No original theorem is declared novel or established here. A finite-class bound can use
\[
\Pr\{\sup_{h\in H}|\widehat R(h)-R(h)|>\epsilon\}
\leq 2|H|\exp(-2N\epsilon^2)
\]
only with finite \(H\), bounded \([0,1]\) losses and independent identically distributed samples. This is a standard Hoeffding/union-bound consequence, not an Evolutor discovery; a verified learning-theory citation is required before chapter publication.

Trace counterexample: let the support on example \(i\) be \(\{i\}\). Mean support is 1; union support is \(N\). This refutes a dataset-union bound by the mean alone, not every trace-guided search bound.
