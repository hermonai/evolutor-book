"""Review-only scientific recalibration; preserve the accepted edition."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DNA = ROOT.name == "dna-computing-book"
COMMON = """# Shared terminology and evidence boundary

DNA computing uses physical molecular systems or explicit formal models of them.
Genomic computation investigates transferable information-processing principles;
training a model on DNA alone does not establish a genomic architecture.
A genome is persistent structural/program information in the proposed abstraction;
expression is context-dependent execution; state is a separately owned evolving
value; evolution changes structure across a longer declared timescale.

DOGMA: non-Transformer DNA-native research architecture plus its prospective
training system and DOGMA Engine. It is not proven novel by avoiding attention.
Hermon DNA: Transformer-based genomic research architecture, training system and
Hermon DNA Engine. Evolutor: research, evidence and eventual orchestration above
both. These are research identities, not proof of validated new architectures.

Keep ESTABLISHED biology, PUBLISHED results, IMPLEMENTED teaching examples,
EXPERIMENTAL candidates, PROPOSED systems and SPECULATIVE capability claims apart.
A biological mechanism → abstraction arrow must name what it discards.
"""
DNA_MAPS = {
"dna-computing-field-map": ("DNA field and computational boundary", [
("Origins / complexity", "1–4, 12–13", "Directed paths and selection; count verification work separately from material.", "Complete Chapter 3 before resource Chapter 4."),
("Formal systems", "14–18", "Sticker, splicing and paired automata have different states and transition rules.", "Specify each exact variant; do not infer laboratory universality from formal universality."),
("Molecular programs", "19–22", "Displacement, CRNs, circuits and assembly connect local interaction to programs.", "Read full algorithms and physical assumptions before implementing."),
("Digital bridge", "27–32", "A simulator represents molecular assumptions; a learned model adds a different objective.", "No generic ML detour without a DNA-specific question.")]),
"molecular-foundations-map": ("Molecular mechanism prerequisites", [
("Backbone and orientation", "5; reminder in 2–3", "Covalent 3′–5′ links differ from inter-strand pairing; aligned strands are antiparallel.", "Draw strand identity, end labels and nick separately."),
("Hybridization", "6–7", "Free energy, concentration, salt, temperature and kinetics condition association.", "Symbolic complement matching is not a calibrated binding predictor."),
("Enzymatic operations", "8–9", "Polymerase extends a primer; ligase seals suitable nicks; cleavage has substrate specificity.", "Show substrates, reaction state and limitations rather than a generic operation box."),
("Measurement", "10, 23–26", "Signal reflects a sampled population with losses and detection limits.", "Separate no witness from no measured signal.")]),
"computational-models-map": ("Formal models and proof obligations", [
("Generate / filter / verify", "2–4,12", "Predicate soundness and population coverage are distinct.", "Use independent enumeration and explicit loss assumptions."),
("Sticker / splicing / automata", "14–18", "Registers, rewriting and automaton configurations are different formal objects.", "Do not merge models solely because they use DNA names."),
("Reaction networks", "20,28", "Stoichiometric state and reaction rates define a dynamical model.", "Declare stochastic versus deterministic approximation."),
("Assembly", "22", "Geometry, tile glues and attachment rules define computation.", "Model-specific assembly assumptions must precede a universality claim.")]),
"laboratory-reality-map": ("Experimental reality plane", [
("Abstract algorithm", "2–4,12", "An existential predicate defines the desired answer.", "Proof is not a measurement."),
("Encoding / operation", "5–11", "Sequence design, substrates and physical conditions implement a noisy realization.", "Record off-target binding, yield, bias and resource cost."),
("Readout / controls", "10,23,26", "Positive controls, blanks and an independent verifier answer different questions.", "A positive control does not establish complete witness coverage."),
("Reproduction", "26,31", "Provenance includes designs, lots, conditions, measurement and analysis.", "No wet-lab work was performed in this pass.")]),
"modern-field-status": ("Source-bounded field refresh: 2026-09-10", [
("CRN compilation", "19–21", "Soloveichik, Seelig and Winfree (2010) describe DNA constructions approximating coupled reaction dynamics.", "Primary abstract accessed; full-text retrieval failed, so detailed compilation and supplement remain a research gate."),
("Current capability", "31", "This pass is not an exhaustive 2026 laboratory survey.", "Do not advertise frontier speed, circuit scale or synthesis capability from old evidence."),
("Chapter 3", "3", "MIT's cycle-to-path construction was reopened; local proofs and finite enumeration remain explicit.", "The upstream hardness theorem is an attributed premise, not a newly reconstructed Cook/Karp proof.")])
}
EVO_MAPS = {
"genomic-computation-landscape": ("Genomic computation versus genomic prediction", [
("Caduceus", "7,21,24,29", "Published bidirectional, reverse-complement-equivariant Mamba-derived sequence modelling.", "Prior art for symmetry; not a causal next-token baseline without task alignment."),
("CrossDNA", "21,24,29", "A 2026 primary abstract describes explicit cross-strand communication with recurrent and sliding-window-attention components.", "Abstract-level novelty conflict; no independent reproduction or performance adoption."),
("DOGMA / Hermon DNA", "18–24", "Target identities preserved; current teaching fixtures are not either architecture.", "Do not fill unknown mechanism or memory complexity with invented answers.")]),
"genomic-mechanism-map": ("Mechanism ledger: hypotheses, not discoveries", [
("Complementary strands", "21,24", "Biology: paired sequence orientation. Abstraction: RC symmetry or two related representations.", "Compare RC augmentation/equivariant baselines; ablate strand relation at fixed capacity."),
("Regulation", "11,19", "Biology: binding context changes expression. Abstraction: conditional module selection.", "Compare ordinary gating/MoE; show added state and cost; no binary biochemical guarantee."),
("Duplication / recombination", "12–13,43,50", "Biology motivates structural copy and recomposition, not arbitrary tensor noise.", "Compare module cloning, architecture search and random search; count search cost."),
("Multiple timescales", "20,40,50", "Separate fast state, parameters, regulatory state and lineage.", "Match state capacity and retention tasks; reject a renamed ordinary recurrence.")]),
"biological-inspiration-boundaries": ("Biology → abstraction → software", [
("Transcription control", "11,19", "Established binding/recruitment mechanisms motivate a question about conditional execution.", "No claim that a hard software threshold reproduces molecular occupancy or cellular regulation."),
("Genome", "12,14", "Persistent structural information can be represented as a typed program.", "A tensor collection is not literally a chromosome."),
("Mutation", "13,43", "Specify value change versus connectivity/program change.", "Parameter noise alone is not demonstrated structural evolution."),
("Evolution", "43,50", "Population and lineage are explicit experimental objects.", "Adaptation speed must include evaluation/training/search budgets.")]),
"architecture-space": ("Three research layers with unknowns preserved", [
("DOGMA", "18–22,30–34", "Representation → local operators → regulation → state → output is a research map.", "Derive the operator contract; test equivalence to RNN/SSM and absence of hidden attention before novelty claims."),
("Hermon DNA", "23–24,35–38", "Baseline Transformer → one genomic intervention → ablation → reference inference.", "Keep generic attention/KV machinery visually separate from the tested intervention."),
("Evolutor", "39–43", "Evidence registry, selection and adaptation above heterogeneous models.", "Demonstrate value over a simpler experiment runner before adding orchestration complexity.")]),
"training-paradigms": ("Independent training tracks, shared evidence contracts", [
("Reference first", "3–4,25–27", "PyTorch expresses differentiable candidates before specialized infrastructure.", "Checkpoint parameters, optimizer and relevant RNG/state; check local derivatives separately from generalization."),
("DOGMA training", "22,25–28", "Gradient updates apply only where the derived operator supports them; structural search is a separate update.", "Selected-branch autograd is not a derivative of discrete genome editing."),
("Hermon DNA training", "23–28", "Train a baseline before adding a genomic intervention.", "Equalize data, targets, budget, masking and evaluation access."),
("Structural search", "43,50", "Parameter, regulatory and structural evolution use distinct state transitions.", "Count population, training, evaluation, memory and wall-clock costs.")]),
"inference-engine-map": ("Reference inference before specialized engines", [
("DOGMA Engine", "30–34", "Load a validated candidate; derive sequence state, reset, clone, chunking and batching contracts.", "Persistent state shape, cacheability and static/dynamic execution remain architecture-dependent."),
("Hermon DNA Engine", "35–38", "Transformer prefill/decode and KV plus only justified genomic state.", "A genomic intervention can invalidate ordinary reuse or batching assumptions."),
("Runtime / compiler", "39–47", "Profile a correct reference, then select lowering and memory policies.", "Do not build a branded engine before a bottleneck or semantic requirement exists.")]),
"prior-art-map": ("Novelty conflict and research queue", [
("Dual strand / RC", "21,24", "Caduceus and CrossDNA make broad novelty claims unsafe.", "Read full methods/code and align causal versus bidirectional tasks before comparison."),
("Regulatory routing", "10–11,19", "Nearest comparisons include MoE, gating, dynamic networks and selective-state models.", "A renamed gate is a negative novelty finding, not a new primitive."),
("Generated structure", "12–13,43", "Compare hypernetworks, NAS, genetic programming and module growth.", "Sources are a research queue here, not a completed priority audit."),
("Historical DOGMA results", "22,29,52", "Preserve historical lineage without inheriting claimed superiority.", "Revalidate causality, random-target floor, capacity, strong baselines and seeds; no historical performance was rerun here.")])
}

def make():
    data=json.loads((ROOT/"pedagogy/deep-curriculum.json").read_text())
    chapters=data["chapters"]
    ids={c["id"] for c in chapters}
    assert len(ids)==(32 if DNA else 52)
    seen=set()
    for c in chapters:
        assert set(c["requires"]) <= seen
        seen.add(c["id"])
    outputs={"research/shared-genomic-terminology.md":COMMON}
    maps=DNA_MAPS if DNA else EVO_MAPS
    for name,(title,rows) in maps.items():
        lines=["# "+title,"","2026-09-10 · bounded author audit, not independent review.","",
               "| Domain | Chapter home | Mechanism / current finding | Limit / action |",
               "| --- | --- | --- | --- |"]
        lines += ["| "+" | ".join(row)+" |" for row in rows]
        lines += ["","Evidence and access depth: [source ledger](scientific-recalibration-sources.md).",""]
        baseline=ROOT/"research/pre-recalibration"/(name+".md")
        prior=baseline.read_text()+"\n---\n\n" if baseline.exists() else ""
        outputs["research/"+name+".md"]=prior+"\n".join(lines)
    architecture=["# Deep scientific architecture: refinement proposal","",
        "Preserve the current "+str(len(chapters))+" chapters and "+str(len({c['part'] for c in chapters}))+" parts.",
        "No chapter files are moved. Chapters 1–2 retain acceptance; Chapter 3 is the next unfinished chapter.",
        "This source-derived map adds scientific gates; it does not turn planned chapters into manuscripts.",""]
    migration=["# Architecture migration decisions","","| Chapter | Action | Reason |","| --- | --- | --- |"]
    visuals=["# Mechanism-first visual production map","",
        "Biology uses structures and reaction states; mathematics uses graphs and equations;",
        "software uses UML and explicit state. Every figure needs a semantic TXT companion.",
        "A molecular drawing labels 5′/3′ orientation, covalent backbone versus pairing,",
        "binding/cleavage sites and what changes. Color is redundant with labels and shapes.",
        "These per-chapter entries are plans, not a claim of completed artwork.",""]
    graph=["Scientific prerequisite spine (canonical dependencies)",""]
    for c in chapters:
        bio=("Molecular interpretation and limitations must accompany the formal object." if DNA
             else "Name the genomic question or explain why this mathematical prerequisite is needed; do not add biological decoration.")
        architecture += ["## "+c["id"]+" · "+c["title"],"",
            "- **Central question:** How do "+", ".join(c["topics"])+" support this chapter's stated mechanism?",
            "- **Scientific context:** "+bio,
            "- **Prerequisites:** "+(", ".join(c["requires"]) or "Declared entry assumptions")+".",
            "- **Book I imports:** "+(", ".join(c["book1Requires"]) or "None additional")+".",
            "- **Mathematics:** "+c["math"],
            "- **Implementation / experiment:** "+c["exercise"],
            "- **Principal figure:** "+c["visual"]+".",
            "- **Keyframes:** "+" → ".join(c["frames"])+".",
            "- **Research status:** "+c["status"]+" in canonical metadata; Chapter 3 has a separate working draft.",
            "- **Acceptance:** source-level evidence, stated assumptions, independent numerical/logic check, failure case and every-page visual review.",""]
        action="KEEP" if c["number"]<=2 else "DEEPEN IN PLACE"
        migration.append("| "+c["id"]+" · "+c["title"]+" | "+action+" | Preserve IDs/dependencies; "+("no change to reviewed source." if c["number"]<=2 else "apply the mechanism/evidence gate during bounded production.")+" |")
        visuals += ["## "+c["id"]+" · "+c["title"],"",c["visual"]+".",
            "State sequence: "+" → ".join(c["frames"])+".",
            "Question/test anchor: "+c["exercise"],""]
        graph += [c["id"]+" ⇐ "+(", ".join(c["requires"]) or "entry"),
                  "  Book I imports: "+(", ".join(c["book1Requires"]) or "none")]
    outputs["docs/DEEP_SCIENTIFIC_BOOK_ARCHITECTURE.md"]="\n".join(architecture)
    outputs["docs/DEEP_ARCHITECTURE_MIGRATION.md"]="\n".join(migration)+"\n"
    outputs["docs/SCIENTIFIC_VISUAL_MAP.md"]="\n".join(visuals)
    outputs["docs/scientific-dependencies.txt"]="\n".join(graph)+"\n"
    outputs["docs/scientific-dependencies.json"]=json.dumps({c["id"]:c["requires"] for c in chapters},indent=2)+"\n"
    return outputs

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");a=p.parse_args()
    for name,text in make().items():
        dest=ROOT/name
        if a.check:
            assert dest.exists() and dest.read_text()==text, name
        else:
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
    print("Scientific refinement maps verified" if a.check else "Scientific refinement maps generated")
