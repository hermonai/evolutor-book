# Notation contract

Every chapter defines its symbols locally. IDs distinguish definitions (DEF), propositions (PROP), claims (CL), experiments (EXP) and graphs (G).

- \(\Sigma_{\mathrm{DNA}}=\{A,C,G,T\}\): canonical base alphabet, not all chemical DNA states.
- \(s=s_1\cdots s_n\): a sequence written \(5'\) to \(3'\); \(n=|s|\).
- \(c\): basewise complement; \(RC\): reversal followed by basewise complement.
- \(x\): input; \(y\): output; \(\theta\): learned parameters.
- \(h_t\): carried computational state; no implied biological interpretation.
- Chapter 2: \(x_t\) is state before input \(u_t\); \(x_{t+1}=(1-d)x_t+p u_t\) is state afterward. \(d\) is a dimensionless loss fraction per update, not a continuous-time rate. The instantaneous comparison is \(y_t=p u_t\). All numerical units are synthetic.
- \(G\): a candidate stored program representation, only when explicitly defined.
- \(P_x\): a program selected for input \(x\); \(\Omega\): recorded execution events.
- \(C_{\mathrm{store}},C_{\mathrm{route}},C_{\mathrm{exec}},C_{\mathrm{state}}\): distinct resource quantities with units and a cost model, not an established new complexity theory.

State whether equations are definitions, identities, assumptions, approximations or fitted relations. The active edition imports no historical theorem by symbol or number. Use LaTeX labels for referenced equations; do not hard-code display numbers.
