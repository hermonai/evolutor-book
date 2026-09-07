# Beginner review: Evolutor

> Historical undergraduate-design review, retained as evidence of the earlier experiment. It is not the active audience policy. See DEEP_REDESIGN.md and REVIEW_GATES.md for the deep edition.

This is an internal role-based walkthrough performed by the authoring assistant, not a panel of actual readers or separate agents. Status: revised architecture ready for user review; empirical readability remains untested.

| Perspective | Where the old route loses them | Applied structural revision | Remaining check |
|---|---|---|---|
| 18-year-old first-year student after Book I | Dispatch semantics and cost tuples before a useful mental picture | Familiar program/genome question in EVOU-01; tiny adjustable model in 03; dispatch in 15 | Explain stored instructions versus changing state without jargon |
| Software-curious biology student | Neural layers, gradients and runtime vocabulary assumed | Arithmetic fitting → slopes → layers → PyTorch in 03–08; runtime foundations in 17–18 | Predict one update manually before library calls |
| Biology-curious programmer | Genomic language appears to rename ordinary functions | Biological recall in 20, question-mark mappings in 21, nearest baselines before proposals | Identify a mapping that fails and explain why |
| Technical entrepreneur | Architecture names and AGI language may look like shipped capabilities | Research-program status in 01; names re-audited only in 37; evidence scorecard in 39 | Distinguish a proposed architecture, test result and deployable service |
| Scientifically literate general reader | Formula, tensor axes and full Transformer arrive together | Containers in 05; token cards in 09; one weighted lookup in 12; block construction in 13 | Explain a three-token figure before seeing matrix notation |

## Revisions from this walkthrough

- Do not lead with program → neural network → genome as three unexplained boxes. Open with the familiar program/genome question; teach the tiny model and neural network before the comparison becomes technical.
- Define inference separately from training in Chapter 3 and revisit the distinction in code.
- Add a calculus bridge: finite differences, derivative, gradient and chain rule precede backpropagation.
- Put softmax and categorical probabilities before attention scores; show numerical weighted sums before the full Transformer.
- Move scalar recurrence behind old-amount/loss/input arithmetic and state history.
- Teach compiler/runtime/process/service vocabulary before software architecture.
- Move query planning before regulation novelty comparisons.
- Mark all Book I imports as planned competencies; the current DNA draft is not accepted as a substitute.

## Opening design to test next, not drafted prose

EVOU-01 compares a written instruction rule and a recalled biological genome, explicitly distinguishing biological genes from later proposed computational genes. It asks a research question without asserting that software is incapable of adaptation. No formal genomic tuple, dispatch proof or resource ledger is required.

EVOU-10 shows old amount minus lost amount plus new amount, a retained-fraction picture, one numerical update and a second history before any indexed recurrence. Only then does it generalize to a trained recurrent network.

## Unresolved

No new manuscript has been tested with real readers. Book I outcomes may change during its production, and any affected import must be repaired before use. The final research chapters require renewed source/artifact audits. A 40-unit outline is not a validated teaching schedule, and the unknown-word ledger cannot mechanically guarantee comprehensibility.
