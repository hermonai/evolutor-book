# EVO-01 research and review record

Question: what observable advantage would justify calling a computational abstraction genomic?

Outline: stored versus selected computation; a plain dispatch baseline; an equivalent full-gate scan; exact operation accounting; candidate operational semantics; conditions for novelty; biological boundaries; falsifiers and exercises.

Source review on 2026-09-05: Shazeer et al. (2017), arXiv:1701.06538v1, introduction, MoE structure/gating and performance-challenge sections inspected in full relevant text at https://arxiv.org/html/1701.06538v1. No numerical benchmark result is reproduced or transferred to this example. The arithmetic library, two selectors, cost counters and equivalence proof are original elementary teaching examples, not an MoE reimplementation.

Claims: EVO-CL07 both selectors implement the same specified pure function; EVO-CL08 zero or one firing does not account for routing work; EVO-CL09 this example establishes no genomic novelty or AGI capability.

Math review: distinguish functional equivalence from efficiency and learning. Costs count logical gate/lookup/invocation events, not CPU instructions or latency. Dictionary construction/storage costs and integer-size effects remain explicit. No claim of constant worst-case hash lookup is made.

Skeptical review: the strongest interpretation is ordinary dispatch. The chapter accepts that interpretation and gives criteria under which a later candidate could improve it. Names and metadata alone cannot change behavior. There is no model training, benchmark victory, self-modification deployment or AGI result.

Verification and publication outcome are recorded in CHAPTER_REPORT.md. This is internal review, not independent peer review.
