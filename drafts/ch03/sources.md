# Chapter 3 source ledger

## Review-candidate extension, 12 September 2026

The historical entries below describe the first two passes. The current
extension now implements momentum and two boundary controls, superseding the
earlier statements that these were unproduced.

- [PyTorch 2.10 SGD](https://docs.pytorch.org/docs/2.10/generated/torch.optim.SGD.html): rechecked the first-buffer-equals-gradient convention, retained momentum and dampening behavior. The implemented example has zero dampening and weight decay. Two updates are compared with a hand-computed golden trace and a reset-state counterexample; no Adam result is claimed.
- [PyTorch 2.10 autograd mechanics](https://docs.pytorch.org/docs/2.10/notes/autograd.html): rechecked the nondifferentiability conventions. The hard selector example is an original piecewise function. Tests distinguish the gradient of selected branch parameters from a derivative through the Boolean predicate.
- Alberts et al., [How Genetic Switches Work](https://www.ncbi.nlm.nih.gov/books/NBK26872/), Molecular Biology of the Cell, 4th edition (2002): relevant bacterial transcription-control discussion read for the simplified repressor/promoter illustration. This mechanism motivates conditional computation; it is not evidence that a protein occupancy event is an exact binary gate or provides a software gradient rule.

The fixed-state versus changed-state finite-difference example is original and
analytically checkable. RNG replay is explained as a requirement, not reported
as an implemented stochastic-model experiment. All twelve figures are now
produced. Full optimizer coverage, trained-model results and independent
scientific review remain outside this checkpoint.

Consulted 9 September 2026. Official documentation is pinned to version 2.10 to match the observed CPU runtime, PyTorch 2.10.0. Search results for moving stable/main documentation were not treated as the specification for that installed version.

## Directly read support

- Baydin, Pearlmutter, Radul and Siskind, [*Automatic Differentiation in Machine Learning: a Survey*](https://jmlr.org/papers/volume18/17-468/17-468.pdf), JMLR 18(153), 1–43 (2018). Read the distinction from numerical/symbolic differentiation and the forward/reverse accumulation discussion in Sections 2–3, especially the reverse-mode and storage account around pages 11–13. No claim of having fully audited all historical priority attributions or the whole survey bibliography.
- [PyTorch 2.10 autograd mechanics](https://docs.pytorch.org/docs/2.10/notes/autograd.html): graph reconstruction, saved tensors, derivative conventions and gradient-mode distinctions. The draft uses a stateless smooth CPU function; it does not infer universal correctness for arbitrary stateful or discrete programs.
- [PyTorch 2.10 gradcheck mechanics](https://docs.pytorch.org/docs/2.10/notes/gradcheck.html): real-input central differences and analytical reverse-mode comparisons. Complex Wirtinger derivatives are outside this chapter core. A generated API URL did not load; it was not treated as read support.
- [PyTorch 2.10 numerical accuracy](https://docs.pytorch.org/docs/2.10/notes/numerical_accuracy.html): floating-point order, batched/sliced differences, extreme values and nonfinite-input cautions. GPU backend claims are not made by the CPU fixture.
- [PyTorch 2.10 CrossEntropyLoss](https://docs.pytorch.org/docs/2.10/generated/torch.nn.CrossEntropyLoss.html): logits, class-index targets and reduction semantics. The reference uses unweighted mean loss with every target scored; it does not silently inherit weighted or ignored-target formulas.
- [PyTorch 2.10 SGD](https://docs.pytorch.org/docs/2.10/generated/torch.optim.SGD.html): update-rule options and implementation conventions. Only plain gradient descent is implemented here. Momentum, Adam and decay variants need a fuller directly sourced treatment before their planned figures are produced.

## Original numerical and mathematical examples

### Second-pass evidence check

Rechecked the pinned autograd mechanics section on leaf-gradient accumulation. The new figures use generated per-row logit adjoints and count-weighted microbatch gradients. The component-wise bias proof, maximum-shift cancellation (including tied maxima), cube-root perturbation balance and two accumulation-loop identities are explicit pedagogical derivations, not quotations or new algorithm claims. Tests compare both accumulation implementations at fixed parameters, validate tied-logit value/gradient behavior, and expose a batch-centering counterexample where partitioning changes the forward function. These tests establish only the stated finite cases.

The 3-by-2 input fixture, complete matrix-gradient derivation, explicit broadcast reductions, detached-operand negative control, step-size sweep, stable-logit example and scalar-quadratic traces are original small teaching examples. The forward primitives are shared across manual and automatic differentiation; the hand reverse equations, finite differences and zero-parameter golden case supply different checks.

Parameters and targets are fixed in code. One rate (0.1) is declared for a single toy update; no optimizer tuning or held-out selection is performed. Quadratic rates 0.1, 0.5 and 0.6 are selected analytically to lie below, at and above the known stability boundary. There is no trained-model experiment or architecture comparison to register as completed in the parent experiment ledger.

## Boundaries still requiring work

Non-square dimensions and noncontiguous parameter views are now tested. Full optimizer-state treatment, nonsmooth examples, richer directional checks, stateful controls and the final literature apparatus remain to be developed. Neither the derivative results nor the inherited Chapter 2 causality controls establish a DOGMA/Hermon model result. Independent scholarly and reader review remain open.
