# Claims ledger

| ID | Claim | Class | Status / evidence |
| --- | --- | --- | --- |
| G001 | A GCS is defined as \((\Sigma,\mathrm{Genome},\mathrm{Reg},\mathrm{Expr},\mathrm{Evo})\). | SOURCE-DERIVED CLAIM | Evolutor v1.4.1 definition |
| G002 | Compilation yields a dependency substrate with nodes, arcs, signatures, gates, and successors. | SOURCE-DERIVED CLAIM | Evolutor v1.4.1; skeleton implemented |
| G003 | Expression can return both outputs and a mechanistic trace. | SOURCE-DERIVED CLAIM | implemented narrowly in MiniEvolutor |
| G004 | The deterministic GCS core is Turing complete. | SOURCE-DERIVED CLAIM | plausible construction sketch; formal proof incomplete |
| G005 | Runtime is controlled by expression complexity alone. | SOURCE-DERIVED CLAIM | overstated unless gate, primitive, scheduling, I/O, and compilation costs are bounded |
| G006 | SPR separates GCS linear expression from quadratic LIM interactions. | SOURCE-DERIVED CLAIM | model-specific statement; not a Transformer lower bound |
| G007 | \(\mathsf{GCS}_k\subsetneq\mathsf{GCS}_{k+1}\) under locality. | CONJECTURE | v1.4.1 proof has unresolved stage/communication and locality gaps; v1.7 changes require audit |
| G008 | Trace-restricted search reduces candidate growth from genome size to average expressed support. | CONJECTURE | union-over-sample and neighborhood encoding are underspecified |
| G009 | Argmin over candidates including the identity gives monotone empirical-objective descent. | ESTABLISHED COMPUTER SCIENCE | immediate from definition; says little about finding useful edits |
| G010 | Verified edits preserve declared invariants if the verifier is sound and complete for those invariants. | ESTABLISHED COMPUTER SCIENCE | induction; verifier assumptions must be explicit |
| G011 | PyTorch can serve as semantic reference for both neural families. | ENGINEERING PROPOSAL | baselines and parity tests implemented |
| G012 | Current DOGMA is recurrent and current Hermon is transformer-oriented. | SOURCE-DERIVED CLAIM | inspected local architectures |
| G013 | Target DOGMA should be Transformer and target Hermon DNA non-Transformer. | NAMING PROPOSAL | user-supplied intent; migration not executed |
| G014 | A new genomic tensor foundation is necessary. | OPEN QUESTION | no measured PyTorch deficiency yet |
| G015 | Mechanistic traces improve learning or interpretability. | HYPOTHESIS | requires task, metric, baseline, and intervention |
| G016 | Regulation is more than generic conditional routing. | OPEN QUESTION | must isolate an operational property and compare controls |

All quantitative additions must satisfy `experimental-controls.md`.

