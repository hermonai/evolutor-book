# Correction record

The correction record is a core methodological chapter, not an appendix.

| Failure category | What happened in the inherited DOGMA research | Standing rule |
| --- | --- | --- |
| causality leak | multiple layers allowed future tokens to affect earlier logits; tiny-gradient probes missed it | use finite intervention tests per architecture and checkpoint |
| state-dimension cap | a hidden default capped scan state and reversed conclusions | report and sweep actual state dimensions |
| parameter-matching confound | equal parameters created unequal width/state and inflated an effect | report parameter, width, and state budgets together |
| bimodal seed mean | a mean hid one failed seed and two successful ones | inspect every seed before interpreting aggregates |
| gameable oracle | retrieval variants measured starvation, output-space effects, and shortcuts | test trivial/gameable baselines and expected ranking |
| falsified mechanism | a proposed Boolean/XOR mechanism failed ablation and transplant | withdraw mechanism claims when causal tests fail |
| biological overclaim | neural features initialized from biological constants were described physically | biological names are hypotheses until physically validated |

The 2026-08-02 audit withdraws old checkpoints and broad universality/performance claims. New evidence starts from fresh initialization and immutable artifacts.

