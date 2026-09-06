# Pedagogical redesign: Evolutor

Date: 2026-09-06. New branch: astra-undergraduate-rewrite. Status: unit EVOU-01 production; later units remain planned.

## Thesis: discovery before architecture

**Evolutor: From Genomic Computation to Adaptive Machine Intelligence** assumes only completion of the eventual Book I curriculum. It does not assume machine learning, calculus, PyTorch, compilers or service-engineering coursework.

The book opens with a familiar program and a recalled biological genome. It asks which organizational similarities are useful and which are misleading. The old dispatch comparison and cost tuple are moved to unit EVOU-15 and later formal accounting. The old scalar recurrence becomes a step-by-step arithmetic example in unit EVOU-10. Neither remains an opening gatekeeper.

The story is observation → computational question → conventional explanation → remaining difference → explicit mechanism → smallest implementation → fair test → failure or bounded extension. Calling a module a gene is not a discovery. Ordinary software can already choose, remember, construct programs and adapt; biology is a source of questions, not an automatic superiority claim.

## The new staircase

A tiny model with adjustable numbers introduces prediction, training, inference and error in unit EVOU-03. Gradients come only after numerical trials, slopes and arrays. A neural network is built one layer at a time. Tokens and embeddings precede sequence models. Scalar retention precedes recurrence; a three-token weighted lookup precedes attention; one head precedes the full Transformer.

Book II explicitly teaches calculus where needed: finite differences, derivative, partial derivative, gradient and chain rule before backpropagation. It teaches software concepts before using architectural notation: interpreter, compiler, runtime, library, API, process, thread, service, protocol, database, scheduler and cache. Query planning is taught in unit EVOU-18 before a genomic-routing novelty comparison.

The proposal begins only after conventional if/else, dispatch, plugins, MoE routing, attention and query planning. Parameter learning, pruning, architecture search, genetic programming and program synthesis precede structural evolution. The genomic tuple arrives in unit EVOU-24 to summarize known components, not introduce mysterious symbols.

## The Book I dependency is a checked promise, not an assumption about the old PDF

Each chapter lists explicit DNAU imports from the versioned Book I contract. Those are planned outcomes, not current achievements. The existing two-chapter DNA draft is not sufficient preparation. Book II's chapter bridges recall the imported concept and test it briefly; if an outcome is not actually delivered in Book I, teach it locally or repair Book I before relying on it.

No Book I → Book II → Book I dependency cycle is allowed. Book I's sequence-model discussion distinguishes DNA data analysis from molecular computation without needing the AI course that follows here.

## Engineering and research stay conditional

UML is taught before class, sequence, state-machine, component and deployment diagrams are used. Training and inference have separate code routes and tests. Memory managers, paged key-value storage and continuous batching appear only after requests, caches, memory use, queues and latency.

Target taxonomy is now fixed by the user's amendment: **DOGMA is non-Transformer DNA-native architecture plus DOGMA Engine; Hermon DNA is Transformer-based DNA architecture plus Hermon DNA Engine. Evolutor is the higher-level genomic theory, planning, research and runtime.** Actual historical artifacts still require source and behavior audits; target naming does not relabel evidence. See [taxonomy and lineage](research/architecture-taxonomy.md).

The plan now has 61 teaching units in 14 parts. Twenty-one new units are inserted by prerequisites while the original 40 EVOU IDs remain stable. DOGMA has its own primitives, structured state, regulation/expression, trace, training-parity and engine agenda; ordinary recurrence, gates and selective state models remain strong comparisons. Hermon DNA has separate Transformer mathematics, DNA variants and attention/KV inference teaching. Runtime composition and hybrid memory are explicit hypotheses. AGI means artificial general intelligence; its late scorecard keeps untested cells unknown. A passing reference implementation is not evidence of AGI.

## Pedagogical contract

The learner arrives with high-school arithmetic and algebra, curiosity, and no assumed university biology, chemistry, probability, algorithms, machine learning or software-engineering course. Teach just enough immediately before it is needed. Do not replace advanced material with vague metaphors; build the staircase to it.

The normal teaching order is prerequisite → intuition → concrete example → illustration → precise definition → mathematics → procedure → implementation → application. A departure needs a recorded reason. A first encounter includes an ordinary example and a labeled picture before notation. Equations must be assembled from quantities the reader can explain, not dropped as definitions. Technical terms in captions, exercises, code comments and chapter-opening maps count as first encounters too.

A chapter opens with a tangible question and an already-known/current/next map. Small sections teach one step at a time. It ends with what the learner now knows, what remains simplified, and what that enables next. A proof begins with reasoning and a proof idea; formal proof is introduced gradually. Code follows a manually traced procedure, with syntax explained before it is required.

## Architecture deliverables and source of truth

- [Course contents](BOOK_PLAN.md): part structure and every planned chapter.
- [Course map](COURSE_MAP.md): per-chapter prerequisites, first encounters, mathematics bridge and exit task.
- [Prerequisite graph](PREREQUISITE_GRAPH.md): typed Unicode TXT teaching dependencies, no ASCII box art.
- [Disciplinary maps](CONCEPT_MAPS.md): just-in-time concept routes.
- [Visual storyboard](VISUAL_STORYBOARD.md): teaching questions, sequential frames and comparison figures for every chapter.
- [Learning progression](LEARNING_PROGRESSION.md): exercises, code and experiments.
- [First-encounter ledger](TERMINOLOGY_AUDIT.md): planned terms, not a falsely completed glossary.
- [Previous-edition audit](PREVIOUS_EDITION_AUDIT.md): disposition of every old drafted and planned chapter.
- [Beginner review](BEGINNER_REVIEW.md) and [professional review](PROFESSIONAL_REVIEW.md): internal role-based critiques, not external endorsements.
- [Figure system](FIGURE_SYSTEM.md): scientific and engineering visual rules.
- [Review gates](REVIEW_GATES.md): criteria for authorizing and then accepting chapter production.

The canonical editable plan is pedagogy/curriculum.json. scripts/build_pedagogy.py derives the maps and inventories. A change to a title, prerequisite, first-use term or storyboard is made there first. Generated documents are checked for freshness. These files are editorial plans, not reader-facing manuscript chapters.

## Course scope and pacing

A full book is not assumed to fit one semester. The proposed small chapters are teaching units with variable length; scheduling and contact-hour estimates remain unvalidated. Readers can study at different speeds, but a short course must not skip prerequisite nodes while claiming the same exit competence. Optional research projects are separate from the baseline exit checks. No external textbook is used as a substitute for missing teaching.

Exercises progress from recognition, calculation and tracing through application, implementation, reasoning and research. Early work uses only taught tools. Provide the first solved case, a partially worked case, and a fresh case with hints and answer checks. A research question receives an evaluation rubric and explicit acceptable uncertainty rather than an invented unique solution. Include delayed retrieval of earlier ideas, not only immediate imitation.

## Evidence and access

A picture that is easy to understand can still be wrong. Biological arrows require mechanism and orientation checks; software diagrams require agreement with the code. No internal role simulation substitutes for independent subject review or observed learner testing. Existing regression tests demonstrate code properties, not textbook readability, biology, experimental advantage or intelligence.

This architecture adopts concrete-to-abstract bridges, paired verbal/visual explanations, worked examples interleaved with practice, and spaced retrieval. These choices are consistent with the recommendations in the official [IES practice guide, Organizing Instruction and Study to Improve Student Learning](https://ies.ed.gov/ncee/wwc/PracticeGuide/1), reviewed on 2026-09-06. The guide does not validate this curriculum or its proposed chapter count. The exact prerequisite-first invariant is our editorial requirement, not a claimed universal empirical theorem.

Research registers from the old edition remain useful leads, not automatic scientific approval. Every new chapter needs renewed section-level source review and explicit observation/model/hypothesis boundaries. Current frontier chapters require fresh primary-paper and artifact review when drafted. No benchmark, experiment or contemporary taxonomy is asserted by this outline.

## Current production boundary

Phase 2 authorizes only the new Chapter 1, not later manuscripts. The original approved title is retained. Its visual storyboard was internally approved before prose. Six original editable figures replace the two coarse planning placeholders. A tiny optional Python example implements the paper exercise without making programming an entry prerequisite.

The local biology reminder supplies the narrow opening dependency while DNAU-03, DNAU-09 and DNAU-32 remain planned. Machine-learning mechanisms stay out of the opening; the taxonomy amendment changes future architecture, not Chapter 1's difficulty.

The active source is tex/undergraduate/ch01.tex. Earlier tex/chapters/ch01.tex and ch02.tex remain byte-preserved. No main merge, force push, licensing change, independent-review claim or activation of the full Book I exit contract is authorized by this production step.
