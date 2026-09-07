# Canonical deep Chapter 1 production report

Date: 7 September 2026. Status: internally reviewed development prototype, not a completed book or independent scientific endorsement.

## Release identity

- Repository: hermonai/evolutor-book; verified public.
- Branch: `astra-deep-rewrite`; no merge into main.
- Starting commit: `68b730a77286aca2ce1aec668996dcda7c9a0376`.
- Final release commit: the commit introducing this report; resolve with `git log --diff-filter=A --format=%H -- DEEP_CHAPTER_1_REPORT.md`. Its actual hash and remote verification are reported in the delivery message, avoiding a self-referential commit hash.
- Chapter: [Why Genomic Computation?](tex/deep/ch01.tex).
- PDF: [canonical Chapter 1](output/pdf/deep-evolutor.pdf), 20 physical pages: cover, about, contents; 14 chapter pages; glossary, bibliography and selective index.
- 12 sections, 10 exercises with worked solutions/discussion, 11 bibliography entries.
- The original eight-section planning outline remains preproduction history; production deliberately refines it without expanding into Chapter 2.

## Sections

1. Three ways to organize computation
2. Stored, expressed, and adapted are different roles
3. What biological regulation actually contributes
4. An exact typed example of expression
5. Development: constructing the working system
6. Execution, learning, and structural change
7. Before calling it genomic, check computer science
8. Evolutor, DOGMA, and Hermon DNA
9. Two memory strategies, one honest budget
10. A research program with concrete stopping points
11. Exercises
12. Worked solutions and discussion

## Original figures and static sequence

Ten editable SVG figures in [book/figures/deep](book/figures/deep), each with a semantic Unicode TXT companion in [book/diagrams/deep](book/diagrams/deep). No copied source artwork, raster figure, or ASCII box-art diagram is used. Figure IDs are EVOD-01-F1 through F10.

Figures teach program/model/genomic organization, stored versus selected plans, biological regulation, UML activity flow, development by construction, distinct update roles, established CS alternatives, UML-style project dependencies, carried state versus KV memory, and research dependencies.

[Animation directory](animation/evod-01) contains 7 original editable static keyframes plus a state ledger and storyboard. Each frame identifies changed, unchanged and created/consumed information; a concrete state panel changes alongside the focus highlight. These are not exported moving animations or experimental recordings.

## Executable work and mathematics

[Plain Python companion](examples/deep/ch01.py), runnable as `python3 examples/deep/ch01.py`, and [generated results](artifacts/deep/ch01-results.json). Printed excerpts are generated references to actual source lines, not separately maintained code.

The immutable catalog exposes clip, center and prefix over nonempty rational sequences. Two contexts select ordered plans and preserve exact execution traces. An independent direct-branching baseline agrees over 64 rational triples in each context. Tests also cover noncommutativity, unknown contexts/modules, empty input, development domains and memory scaling.

Formal work: typed Reg/Expr/Exec roles; exact rational traces (3,3,5) and (5/3,−2/3,0); invariant proofs and counterexamples; Dev(G,E) and repeated-prefix construction; separate execution/parameter/structure update indices; state migration; causal KV indexing; attention dimensions/masking; array budgets 2BLTH_kv d_h b versus BLd_s b. The hypothetical example gives 192 MiB of KV arrays versus 96 KiB of carried state, not a speed or equal-quality comparison.

## Source and scientific review

[Source-by-source access ledger](research/deep-ch01-sources.md) distinguishes read portions and permitted scope. All 11 citation keys resolve; no long quotations, imported benchmarks or historical figure reproductions.

Gene expression produces functional RNA/protein; regulation is not a single DNA on/off switch. Development and environment are introduced without treating a genome as a finished-organism lookup table. The software abstractions are explicitly analogies. Ordinary routing, MoE, attention, NAS, synthesis, genetic programming, SSMs and agents establish the novelty burden. No learning or structural update is claimed for the exact toy program.

Scientific, mathematical, clarity, citation and visual review were conducted by the authoring agent. They are not independent expert approval or demonstrated reader learning.

## Visual and build review

Every physical page (1–20) was rendered and inspected in color; all 7 static frames were inspected. Representative mechanism/memory pages were also checked in grayscale. The PDF skill's rendered-page review led to concrete fixes: readable code sizing, unbroken comparison-table heading/rows, a non-wrapping KV label, covalent connections in the strand figure, explicit UML guards/dependency directions, and stateful frame panels. No clipped text, missing glyphs, unresolved references, overfull or underfull boxes remain in the final checked build.

[Source-hashed review record](artifacts/deep/ch01-review.json) binds acceptance to manuscript, apparatus, executable source, generated results, storyboard, SVG/TXT and frames. Tests reject stale source, missing manifests and an unreviewed figure. Coordinate rounding makes original SVG generation stable across the two local Python runtimes.

Verification commands:

```sh
make pdf PYTHON=/Users/wenyan/.pyenv/versions/3.13.6/bin/python3
/Users/wenyan/.pyenv/versions/3.13.6/bin/python3 -m pytest -ra
make review-pdf PYTHON=/Users/wenyan/.pyenv/versions/3.13.6/bin/python3
```

Final full-suite acceptance: 122 tests passed, including PDF compilation, citation closure, generated-asset freshness, invalid-plan rejection, exact examples and historical byte-preservation. The machine-specific Python path records the tested environment; a compatible Python with repository test dependencies may be used elsewhere.

## Preservation and consistency

The undergraduate branch is frozen and was not checked out, advanced or synchronized. Its preserved source/artwork/examples and all previously committed PDFs are byte-identical. Main, astra-rewrite and archive/pre-reboot-20260905 retain their original tips:

| Ref | Preserved commit |
| --- | --- |
| astra-undergraduate-rewrite | af8de42e16c71024d3e228a57e1d4d87c8d87276 |
| main | 3895e94ff206a537a846a88966a27435b14f6ae2 |
| astra-rewrite | 58fa55a8097157d297be4afe21f146623048b875 |
| archive/pre-reboot-20260905 | 9df0d006e10e56cd836a4b84400009dab3cbf4f2 |

Both repositories carry identical Book I dependency contracts. DNAD-01 is prototype-available; later dependencies remain planned, not already taught. The 32/52 chapter architectures are preserved.

DOGMA is the non-Transformer DNA-native model and non-Transformer engine line. Hermon DNA is the Transformer-based DNA model and Transformer engine line. Evolutor is the broader theory, research, compiler/runtime and orchestration framework above both. Physical DNA computation, genomic sequence modeling and biologically inspired digital computation remain distinct.

## Limits and next chapter

Independent specialist and real-reader review remain open. No wet-lab validation, calibrated kinetic simulator, trained DNA-native model, optimized production engine, measured comparative advantage or AGI capability is delivered. Sources and index are selective. Semantic TXT helps access but the PDF is not tagged or certified PDF/UA. More lifelike chemical illustrations and moving animations remain possible future improvements, not delivered assets.

Next: EVOD-02, **Learning objectives, data and evaluation**. Develop sequence likelihood and loss, leakage-resistant splits, held-out generalization and uncertainty/calibration. Keep these foundations tied to testable genomic proposals; do not jump to engine implementation.

No Chapter 2 manuscript was authored in this milestone. [CHAPTER_STANDARD.md](CHAPTER_STANDARD.md) records the production lessons; [canonical strategy](CANONICAL_EDITION_STRATEGY.md) freezes parallel undergraduate development.
