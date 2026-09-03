# Theorem ledger

Status meanings: `sketch`, `conditional`, `gap`, `standard consequence`, `unreviewed revision`.

| ID | v1.4.1 result | Dependencies | Audit status | Main obligation |
| --- | --- | --- | --- | --- |
| T01 | expression type preservation | complete typing rules; transition semantics | sketch | define every AST form, store typing, primitive, and edit transition |
| T02 | policy safety preservation | policy type semantics; safe transition relation | sketch / partly by definition | show all emits and external primitives respect policy, not only edits |
| T03 | GCS universality | unbounded sequence/tape, random access, iteration, deterministic regulation | sketch | formal encoding and multi-step simulation relation; state-space accounting |
| T04 | expression-bounded runtime | local routing, total constant-cost primitives, gate-cost bound, fair scheduler | conditional | replace “runtime is O(EC)” with a cost semantics including gates and primitive costs |
| T05 | SPR linear expression upper bound | scan genome; explicit query availability | sketch | give executable genome and count gates/firings separately |
| T06 | LIM light-cone lemma | synchronous local rounds or precisely bounded asynchronous steps | standard consequence | resolve asynchronous-round definition |
| T07 | SPR quadratic LIM interaction lower bound | T06; output location; all-pairs-per-round cost | conditional | state output model and scheduler; clarify it is LIM-only |
| T08 | regulation-depth upper bound for pointer chasing | staged scan; pointer availability; locality | gap | reconcile “bounded location carried between stages” with local gate access |
| T09 | strict regulation-depth hierarchy | communication lower bound; faithful stage-to-round simulation | gap | `k+O(1)` does not yield `<k`; message-size and cut interface need bounds |
| T10 | finite-class size bound | finite grammar encoding including constants/names/structure | gap | define a prefix-free finite encoding; `(A B)^s` is currently too coarse |
| T11 | uniform convergence over finite class | finite H, bounded i.i.d. loss | standard consequence | correct constants and distinguish risk from regularized objective |
| T12 | trace-restricted candidate-count bound | support union, edit radius, local encoding choices | gap | average support does not bound union across N examples without more assumptions |
| T13 | monotone verified-local descent | finite candidate set, identity candidate, exact argmin | standard consequence | state lower bound/grid assumptions for termination count |
| T14 | invariants under verified edits | initial invariant, sound verifier, preservation per step | standard induction | formalize verifier and non-edit transitions |
| T15 | v1.7 revised pointer-depth and normalized learning results | version-specific definitions | unreviewed revision | prepare a line-by-line v1.4.1-to-v1.7 proof delta |

No `gap` result is presented as established in the manuscript.

