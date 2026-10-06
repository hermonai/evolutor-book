# EVOD-26 convergence audit

Decision: rewrite schedule comparison around independent mathematical, derivative and boundary oracles. Chapter27 owns activation/gradient scheduling; no duplicate trained capability comparison.

EVOD26-T1: chronological affine composition is associative over exact reals with identity(1,0), generally noncommutative. Full parallel evaluation requires coefficients available without the recurrent state. This does not certify the complete DOGMA22 locus/gating model.
EVOD26-T2: inclusive doubling scan reads the preceding stage out-of-place and produces every prefix. Work sum(T-2^k) is O(TlogT), depthceilLog2T; not work-efficient Blelloch scan or measured runtime.
EVOD26-T3: reset-before-valid-step maps to(0,a*h_reset+b), padding to(1,0). Global time masks shared across state lanes; per-lane ragged reset support not claimed.
EVOD26-T4: derivative lambda_t=w_t+a_(t+1)*lambda_(t+1),da=lambda*hprev,db=lambda,dh0=a1*lambda1. Coefficient-generator parameters would require additional end-to-end gradients.

EVOD26-E1: 30 tests cover independent 2x2 homogeneous matrices, hand traces, closed-form product/sum, full coefficient/initial/reset gradients, manual reverse oracle, finite differences at zero coefficient, all chunk sizes, reset/padding and future-causality interventions, batch lanes, empty sequence, lengths up to1024, domain guards, in-place scan and detach mutants.
EVOD26-E2: hand tracea(.5,2,0,-1),b(1,.5,3,2),h0=2 gives(2,4.5,3,-1). WorkT1024:10stages9217paircompositions, not FLOPs.
EVOD26-F1: detach preserves forward state but changes earlier gradients. EVOD26-F2: float64 a=1,b(1e16,-1e16,1),h0=0 gives sequentialfinal1,scanfinal0; not an unrestricted numerical-parity proof. EVOD26-F3: identity padding must not zero state. EVOD26-F4: chunk incoming state is not global reset state. EVOD26-F5: causal coefficient generation can still be sequential if it depends on native recurrent state.

Open: complete trained DOGMA scan eligibility and implementation, Hermon KV-cache parity, native serving state ownership implementation, production kernel/backward, BF16/FP16 stress, measured accelerator memory and latency, genomic validation and independent review. Finite input validation does not guarantee finite outputs on expansive inputs.
