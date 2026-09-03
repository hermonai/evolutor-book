# Proof dependency graph

```text
finite alphabet + formal grammar + store typing
                  |
                  v
             typed genome
              /       \
             v         v
      compilation    policy judgment
             |             |
             v             |
      substrate typing <---+
             |
             v
    small-step expression semantics
        /       |           \
       v        v            v
type safety  trace soundness  cost semantics
                              |
                              v
                    expression complexity theorem

TM encoding + simulation invariant ---> universality

LIM definition ---> light-cone lemma ---> SPR LIM lower bound
        |                                      |
SPR GCS construction ---> linear upper bound --+
                                               v
                                      scoped SPR separation

local GCS interface ---> stage/round simulation ---+
pointer communication problem ---> round lower bound+--> depth hierarchy

finite genome encoding ---> finite hypothesis class ---> uniform convergence
trace semantics + edit encoding ---> candidate count claim
verified edit soundness + identity candidate ---> monotone descent + invariants
```

The depth hierarchy and trace-count branches are blocked by explicit proof obligations rather than treated as foundations for later claims.

