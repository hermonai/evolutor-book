# Evolutor: deep technical edition

Status: canonical deep Chapter 1 is an internally reviewed prototype; all later chapters remain plans. The undergraduate edition is frozen. No trained model, engine or wet-lab result is delivered. See [production report](DEEP_CHAPTER_1_REPORT.md) and [edition strategy](CANONICAL_EDITION_STRATEGY.md).

DOGMA = non-Transformer DNA-native model + DOGMA Engine; Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; Evolutor = broader genomic computation theory, research and eventual runtime above both.

## Detailed Chapter 1 outline: Why Genomic Computation?

This is the preserved eight-section preproduction outline. Production deliberately expanded it to 12 sections and ten figures; see the production report and tex/deep/ch01.tex for the actual chapter.

Next execution writes this chapter; this milestone creates no manuscript, finished artwork or animation frames.

Let the argument determine length; a substantial 30–50-page treatment is acceptable, not a quota. The opening establishes the field and exact worked mechanisms without duplicating later full treatments.

### 1.1 Programs, neural models and genomes

Begin with the real comparison: what is stored, selected, executed, persistent and changed? Ordinary software and neural systems can already be conditional; cells need molecular machinery, not DNA alone.

**Formal depth:** Use separate typed lanes before a shared abstraction. A neural parameter tensor, a program and a physical genome are not interchangeable objects.

**Worked sequence:** Compare a compiled program with dispatch, a conditional neural model and a regulated biological system; annotate where the analogy breaks.

**Visual:** EVOD-01-F1 — Program, model and genome. Three aligned lanes with distinct visual grammars and explicit execution machinery.

**Evidence gate:** Read relevant primary sources in full for the claims used; distinguish historical details, original teaching examples and research proposals.

### 1.2 Stored structure versus expressed computation

Use a concrete library of computational modules and a context-dependent selection. Define the execution plan as a selected computation, not just a list of names.

**Formal depth:** Provisional P_x=Reg(G,x), (y,Ω)=Exec(P_x,x); define G, x, plan type, y and trace Ω. Stateful cases require an explicit state argument.

**Worked sequence:** Work a small deterministic two-module routing example with exact inputs, selected plan, output and trace; show a conventional implementation produces the same behavior.

**Visual:** EVOD-01-F2 — Stored versus expressed computation. Separate persistent module catalog, selected plan and execution trace; no claim of novelty from selection alone.

**Evidence gate:** Read relevant primary sources in full for the claims used; distinguish historical details, original teaching examples and research proposals.

### 1.3 Regulation and expression as mechanisms

Explain what controls selection and what operation becomes active. Compare if/else, dispatch, gates, mixture of experts, attention and query planning at mechanism level; defer model internals to Part II.

**Formal depth:** Give domain/codomain and cost for the selector and executor. An ordinary dispatch equivalence is a useful negative result.

**Worked sequence:** Trace two contexts through the same stored catalog; show changed selection without changing the catalog or claiming learning.

**Visual:** EVOD-01-F3 — Regulation with visible alternatives. Two contexts over one unchanged catalog; control arrows differ from data flow.

**Evidence gate:** Read relevant primary sources in full for the claims used; distinguish historical details, original teaching examples and research proposals.

### 1.4 Development, learning, adaptation and evolution

Separate runtime state, learned parameters, generated structure and population change. Illustrate development as building a computational phenotype without claiming it is biological development.

**Formal depth:** Candidate P=Dev(G,E); specify environment E and generated program P. Distinguish s_t, θ, structure and population as different changing objects.

**Worked sequence:** Classify four updates by object, timescale, objective and inheritance; explain that relative timescales are design choices rather than universal laws.

**Visual:** EVOD-01-F4 — Development and adaptation timescales. Aligned state/parameter/structure/population timelines with explicit update triggers.

**Evidence gate:** Read relevant primary sources in full for the claims used; distinguish historical details, original teaching examples and research proposals.

### 1.5 Existing computer science already explains much

Make the nearest baselines central: conditional execution, MoE, recurrent state, compilation, neural architecture search, evolutionary computation, query optimization and orchestration.

**Formal depth:** Separate representational novelty from algorithmic novelty, expressivity, efficiency and measurable utility.

**Worked sequence:** Construct a comparison table where a proposal is equivalent to dispatch, then state what additional semantics or evidence would be needed for a stronger claim.

**Visual:** EVOD-01-F5 — Established alternatives. Mechanism comparison matrix with supported correspondences and explicit non-equivalences.

**Evidence gate:** Read relevant primary sources in full for the claims used; distinguish historical details, original teaching examples and research proposals.

### 1.6 A research thesis with a falsifiable gap

Frame Evolutor as investigation of selection, composition, development and adaptation across heterogeneous computation. Start with mechanisms; keep full provenance and repeated caveats in ledgers.

**Formal depth:** Introduce a candidate cost vector for storage, regulation, execution, state, trace and adaptation; defer its formal complexity treatment.

**Worked sequence:** Ask whether a proposed selective transformation improves a declared task at matched total resources; specify the result that would reject the proposal.

**Visual:** EVOD-01-F6 — Research gap and test. Mechanism → prediction → controlled test → support/rejection, with baseline in the same frame.

**Evidence gate:** Read relevant primary sources in full for the claims used; distinguish historical details, original teaching examples and research proposals.

### 1.7 DOGMA and Hermon DNA: two architecture families

DOGMA is the non-Transformer DNA-native research line, not merely an RNN with biological names. Hermon DNA is the Transformer-based DNA line. Explain carried state versus attention-accessible cached representations as a first systems distinction.

**Formal depth:** Candidate DOGMA (x_t,s_t)↦(s_{t+1},y_t), with prediction timing declared. Hermon consumes token x_t with prior cache and appends K/V for that token. No off-by-one cache convention.

**Worked sequence:** Compare what persists in each family; bounded carried state does not imply infinite recall or constant total memory. Attention access does not guarantee exact retrieval.

**Visual:** EVOD-01-F7 — Two families and their memory. Separate candidate state layout and Transformer KV layout; weights, workspace and external memory shown separately.

**Evidence gate:** Read relevant primary sources in full for the claims used; distinguish historical details, original teaching examples and research proposals.

### 1.8 From theory to reference models, engines and runtime

Show theory, model architecture, training, engine execution, orchestration and industrial serving as separate levels. Evolutor sits above DOGMA Engine and Hermon DNA Engine and may compose other modules.

**Formal depth:** Define reference → parity → profile → optimization as engineering gates, not performance claims. Formal semantics and full model mathematics come later.

**Worked sequence:** Give a concrete next-step research contract with baseline, implementation, tests and limits; provide technical conceptual and design exercises rather than syntax drills.

**Visual:** EVOD-01-F8 — Research and engineering roadmap. UML component/dependency view, with planned interfaces and no implied deployed service.

**Evidence gate:** Read relevant primary sources in full for the claims used; distinguish historical details, original teaching examples and research proposals.

## Executable example scope

Implement a small deterministic selection/execution/trace example and conventional baseline, with exact tests. It is an analogy experiment, not a DOGMA model, Transformer, training library or engine.

## Exercises

Include a fully solved technical example, derivation, algorithm or proof task, implementation check, experimental/systems design task and research critique. Open problems get a rubric, not fabricated solutions.

## Acceptance

- Chapter starts with the actual subject, not counters or a thermostat.
- Definitions and abstraction boundaries are explicit; useful abstraction is not prohibited.
- Every displayed formula has defined symbols, assumptions and interpretation.
- Every figure has editable source and a Unicode TXT companion; scientific and final-page reviews remain required.
- No novelty, performance, biomedical or AGI conclusion without corresponding evidence.
