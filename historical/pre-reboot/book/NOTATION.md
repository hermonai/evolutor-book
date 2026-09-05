# Mathematical notation

## Genomic Computation System

\[
\mathcal{G}=(\Sigma,\mathrm{Genome},\mathrm{Reg},\mathrm{Expr},\mathrm{Evo}).
\]

| Symbol | Meaning |
| --- | --- |
| \(\Sigma\) | finite codon/symbol alphabet |
| \(G\) or \(\mathrm{Genome}\) | persistent typed computational structure |
| \(\mathrm{Reg}\) | context-dependent regulatory mechanism |
| \(\mathrm{Expr}\) | expression/execution semantics |
| \(\mathrm{Evo}\) | allowed verified structural modifications |
| \(S=\mathrm{compile}(G)\) | compiled substrate |
| \(N,A\) | substrate nodes and dependency arcs |
| \(\gamma\) | gate map |
| \(\rho\) | store/state |
| \(\kappa\) | worklist/frontier |
| \(\Omega\) | append-only mechanistic trace |

The expression machine state is written

\[
\langle S,x,\rho,\kappa,\gamma,\Omega\rangle.
\]

## Complexity

\[
\mathrm{EC}_G(n)=\max_{|x|=n}|\mathrm{Expr}_x(G)|.
\]

`EC` counts fired nodes/codons only after the expression unit is defined. Gate evaluation, routing, primitive costs, scheduling, compilation, storage, and I/O are separate cost terms unless a theorem explicitly absorbs them under assumptions.

| Symbol | Meaning |
| --- | --- |
| \(T_G(x)\) | runtime under a named machine/cost model |
| \(\mathrm{IC}_{M}(x)\) | interactions in a named interaction model \(M\) |
| \(k\) | regulation stages, not neural-network layers unless declared |

## Learning

| Symbol | Meaning |
| --- | --- |
| \(h_G\) | predictor induced by genome \(G\) |
| \(\widehat R_D(G)\) | empirical risk on dataset/sample \(D\) |
| \(R(G)\) | population risk |
| \(J(G)\) | declared accuracy/compute/safety objective |
| \(\mathcal H_{s,d,e}\) | hypothesis class under explicit structural bounds |

## Neural references

Use \(d_{\mathrm{model}}\), \(d_{\mathrm{state}}\), \(L\), \(H\), and \(V\) for model width, recurrent-state width, layers, attention heads, and vocabulary size. Training tensors use `[B,T]` or `[B,T,V]`; brackets are shapes, not mathematical intervals.

No symbol may cross biology, formal theory, and ML layers without a local declaration.

