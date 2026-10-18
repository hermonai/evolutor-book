# Chapter 48 package adoption

Archive: `/Users/wenyan/Downloads/evolutor-ch48-r01.zip`  
SHA-256: `502d57b2a698224be00bdf1ceb0ec50bc1f182b5d4c010ff64c175df10ba2972`  
All 48 manifest hashes reverified against archive bytes on 17 October 2026; no mismatches.
Incoming manuscript: `incoming/drafts/ch48/manuscript.tex`, SHA-256 `b995b0556ec7be19483825bf40d5791c158981c84fd54b53702ea05f4f167a92`.
Every incoming section below refers to that exact source. Destinations are headings in `drafts/ch48/manuscript.tex`, including named subsections. Conceptual retention, verbatim wording and executable reuse are different quantities; no reuse percentage is asserted.

| Incoming section | Disposition | Destination | Concrete change/reason |
|---|---|---|---|
| Start from the biological question | expanded | From a biological question to an observation contract | Preserves (X,Y,U,M), all four task families and provenance; adds a transcription mechanism and assay boundary. |
| Coordinates and provenance | expanded | From a biological question to an observation contract | Keeps assembly/contig/interval/strand/source/version; adds half-open coordinates, sequence-length validation and liftover limits. |
| Leakage is the first adversary | expanded | Leakage is a relation, then a transitive closure | Retains overlap/homology/donor warnings; derives whole-component splitting and its limited no-crossing theorem. |
| Reverse complement | expanded | Reverse complement acts on data and labels | Keeps complement map and involution; derives label action and shared averaging, using non-self-RC ACG as a stronger control. |
| Tokenization and resolution | expanded | Resolution, context and the baseline ladder | Preserves base/k-mer tradeoff and named source leads; connects span-level causal leakage to actual Chapter24. |
| Baseline ladder | merged | Resolution, context and the baseline ladder | Retains Markov/MLP/CNN/GRU/Transformer/SSM comparisons with explicit task-appropriate budget controls. |
| DOGMA hypothesis | merged | Resolution, context and the baseline ladder | Retains bounded-state hypothesis; distinguishes actual Chapter31 restriction from full DOGMA. |
| Hermon DNA hypothesis | merged | Resolution, context and the baseline ladder | Retains Transformer hypothesis and adds actual Chapter23 offline RC interface test. |
| Long context | expanded | Resolution, context and the baseline ladder | Retains distal-context rationale and HyenaDNA scope; adds matched central/distal perturbation protocol. |
| Foundation models and specialized models | expanded | Resolution, context and the baseline ladder | Preserves task dependence; verifies frozen-embedding versus task-trained comparison instead of claiming universal superiority. |
| Metrics under imbalance | expanded | Derive discrimination and probability checks | Keeps confusion/MCC/Brier; defines undefined denominators, tie-group AP and hand arithmetic. |
| Uncertainty | expanded | Uncertainty follows the independent unit | Replaces independent-window bootstrap with whole-cluster resampling; states fixed-predictor and weighting assumptions. |
| Variant effects | expanded | Variant scores and mechanistic claims | Retains alternate-minus-reference contrast; adds normalized checked SNV edits and complemented-coordinate test. |
| Interpretability | merged | Variant scores and mechanistic claims | Keeps saliency/motif/GC/shuffle controls and separates sensitivity from mechanism. |
| Biological validation boundary | expanded | Variant scores and mechanistic claims | Retains independent biological evidence requirement; adds a bounded assay/replication handoff, no wet-lab claim. |
| Executable oracle | expanded | Reverse complement acts on data and labels; Derive discrimination and probability checks; Uncertainty follows the independent unit | Reuses all original utility intents, strengthens validation and prints whole tested functions instead of one compressed listing. |
| Twelve worked exercises | expanded | Exercises and worked solutions | Retains all twelve original question themes and expands to twenty worked derivation, coding and protocol problems. |
| Bridge | retained | Bridge | Preserves transition from genomic observation/state provenance to streaming and agents. |

## Other incoming material

The complete reference, tests, storyboard, all six figure TeX/TXT pairs and source ledger were read as source material. Their text is preserved under `incoming/`, with original file hashes in `incoming/manifest.json`. Original QA status strings are provenance only. Caches, PYC, packaged PDFs and rendered PNGs were not adopted or executed.

The six one-step figure concepts are consolidated into three original native TikZ mechanism plates with semantic TXT. The supplied paragraph concepts are retained at their mapped discussion; the generic two-box artwork is replaced because it does not explain the changing objects. Source listings are whole functions extracted from the expanded tested reference. Incoming tests supply retained scenario themes; current tests add independent oracles and negative controls and update incompatible conventions described above. Original exercise themes are retained and deepened into twenty worked problems. Source leads were checked at the access depths recorded in source-verification.json; incoming access claims are not inherited.

Build/review wrappers clone Chapter35's Pagella/Heros authored-LaTeX pattern with chapter identity/counter corrected and short-listing space reservations added. The packaged builder, stale results and acceptance labels do not govern this chapter. All numerical fixtures are regenerated locally. External evidence is paraphrased selectively; no source prose or artwork is copied.

## Figure and executable adoption detail

Each incoming figure entry below covers both its `.tex` and `.txt` companion; their exact original digests are in the preserved manifest.

| Incoming figure pair | New location | Decision |
|---|---|---|
| 01-task | 01-mechanism + observation-contract section | Expanded from task boxes to a biological observation mechanism. |
| 02-split | 02-components + group_split | Explicit intervals and transitive links replace generic split boxes. |
| 03-rc | 03-strands + RC/SNV derivation | Shows antiparallel orientation and allele/coordinate action. |
| 04-baselines | Resolution, context and the baseline ladder | Retained as sustained protocol prose; a second generic ladder drawing adds no mechanism. |
| 05-eval | Generated metrics table + metric/uncertainty functions | Exact denominators, tie policy and independent units replace generic score boxes. |
| 06-interpret | Variant scores and mechanistic claims + 01-mechanism | Keeps sensitivity-versus-assay distinction with an explicit biological boundary. |

All current listings are extracted from whole tested definitions by the chapter builder. No packaged `__pycache__`, PYC, test cache or result/QA flag is an execution dependency. Changed undefined/degenerate conventions, interface substitutions and strengthened tests are explained in technical-audit.md rather than silently preserving a faulty old assertion.
