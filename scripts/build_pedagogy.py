"""Generate architecture documents, never manuscript chapters, from reviewed planning data."""
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("BOOK_PLAN.md", "COURSE_MAP.md", "PREREQUISITE_GRAPH.md",
         "CONCEPT_MAPS.md", "VISUAL_STORYBOARD.md", "LEARNING_PROGRESSION.md",
         "TERMINOLOGY_AUDIT.md", "PREVIOUS_EDITION_AUDIT.md")


def validate(data, contract):
    assert data["status"] in {"architecture-only-no-manuscript", "chapter-one-production"}
    chapters = data["chapters"]
    ids = [c["id"] for c in chapters]
    assert len(ids) == len(set(ids)), "duplicate chapter"
    known = set()
    first_terms = set()
    exported = {c["id"] for c in contract["chapters"]}
    figures = set()
    for c in chapters:
        assert c["requires"] == sorted(set(c["requires"])), "duplicate or unordered prerequisites"
        assert set(c["requires"]) <= known, f"forward, missing or cyclic dependency: {c['id']}"
        assert set(c["book1Requires"]) <= exported, "missing Book I export"
        assert c["status"] in {"planned-not-drafted", "internally-reviewed-draft"}
        if c["status"] != "planned-not-drafted":
            assert c is chapters[0], "only Chapter 1 may be active in this phase"
        assert len(c["frames"]) >= 3 and len(c["figures"]) >= 2
        for field in ("readerQuestion", "mathBridge", "codeLab", "exercise"):
            assert c[field].strip(), (c["id"], field)
        for term in c["introduces"]:
            assert term.casefold() not in first_terms, f"duplicate first encounter: {term}"
            first_terms.add(term.casefold())
        for f in c["figures"]:
            assert f["id"] not in figures
            figures.add(f["id"])
        known.add(c["id"])
    for old in data["previousChapterAudit"]:
        assert old["prerequisiteDiagnosis"] and set(old["newChapters"]) <= known
    assert [c["number"] for c in chapters] == list(range(1, len(chapters)+1))
    assert len(chapters) == data.get("plannedChapterCount", len(chapters))
    if "architectureTaxonomy" in data:
        taxonomy = data["architectureTaxonomy"]
        assert taxonomy["DOGMA"]["family"] == "non-Transformer DNA-native", "DOGMA taxonomy reversed"
        assert taxonomy["Hermon DNA"]["family"] == "Transformer-based DNA", "Hermon DNA taxonomy reversed"
        assert taxonomy["DOGMA"]["engine"] == "DOGMA Engine"
        assert taxonomy["Hermon DNA"]["engine"] == "Hermon DNA Engine"
    return True


def outputs(data, contract):
    validate(data, contract)
    chapters = data["chapters"]
    lookup = {c["id"]: c for c in chapters}
    title = data["book"]
    header = f"# {title}: undergraduate-first architecture\n\n"
    notice = ("Status: planning only. No new chapters, finished figures, animations, experiments or "
              "reviewed learning outcomes are claimed. Generated from "
              "[pedagogy/curriculum.json](pedagogy/curriculum.json); edit that source and regenerate.\n\n")
    if data["status"] == "chapter-one-production":
        notice = ("Status: Chapter 1 internally reviewed development draft; all later units remain planned. "
                  "No learner study, independent expert certification or new research-model experiment is claimed. "
                  "Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json). "
                  "See [Chapter 1 storyboard](research/undergraduate-ch01-storyboard.md) for the six produced figures.\n\n")
    if "architectureTaxonomy" in data:
        notice += ("Target taxonomy: **DOGMA = non-Transformer DNA-native architecture + DOGMA Engine; "
                   "Hermon DNA = Transformer-based DNA architecture + Hermon DNA Engine; "
                   "Evolutor = research/theory/runtime above both.** "
                   "These are research targets, not implementation evidence. "
                   "See [taxonomy and lineage](research/architecture-taxonomy.md). "
                   "Stable EVOU IDs differ from printed numbers after EVOU-11.\n\n")
    result = {}
    lines = [header, notice, "## Table of contents\n\n"]
    part = None
    for c in chapters:
        if c["part"] != part:
            part = c["part"]
            lines.append(f"### {part}\n\n")
        lines.append(f"{c['number']}. **{c['id']} — {c['title']}**. {c['readerQuestion']}\n")
        if c is chapters[-1] or chapters[chapters.index(c)+1]["part"] != part:
            lines.append("\n")
    lines.append("Chapter count is provisional, not a promise of one semester. These are small teaching units, "
                 "not equal-length lectures. The full two-book path can span multiple courses. "
                 "No chapter requires an external prerequisite textbook.\n")
    result["BOOK_PLAN.md"] = "".join(lines)

    lines = [header, notice, "## Teaching route and chapter opening maps\n\n",
             "Each opening recalls named prior ideas, introduces only the current step, and identifies what it enables next. "
             "A dependency is a teaching requirement, not a claimed biological causal relation. "
             "Unlisted previous chapters remain available for optional practice; no later chapter may be required.\n\n"]
    for c in chapters:
        local = "; ".join(f"{i}: {lookup[i]['title']}" for i in c["requires"]) or "High-school arithmetic and logical reading"
        external = ", ".join(c["book1Requires"]) or "None"
        nxt = [x["id"] for x in chapters if c["id"] in x["requires"]]
        lines += [f"## {c['id']} — {c['title']}\n\n",
                  f"**Required earlier units (planned unless marked active):** {local}.\n\n",
                  f"**Book I bridge:** {external}. See the planned exit checks in the shared contract.\n\n",
                  f"**First encounters, in planned teaching order:** {' → '.join(c['introduces'])}.\n\n",
                  f"**Tangible opening:** {c['readerQuestion']}\n\n",
                  f"**Why and how the mathematics enters:** {c['mathBridge']}\n\n",
                  f"**Observable exit task:** {c['exercise']}\n\n",
                  f"**Enables next:** {', '.join(nxt) or 'Capstone completion and further research'}.\n\n"]
    result["COURSE_MAP.md"] = "".join(lines)

    lines = [header, notice, "## Canonical Unicode TXT dependency graph\n\n",
             "Read A → B as: teach A before requiring it in B. Multiple incoming arrows mean all listed prerequisites. "
             "ENTRY means only the declared entry assumptions. Book I IDs are explicitly prefixed DNAU; "
             "they describe planned teaching, not competence already delivered by the old draft.\n\n", "```text\n"]
    for c in chapters:
        sources = c["requires"] + c["book1Requires"]
        if not sources:
            sources = ["ENTRY"]
        for s in sources:
            lines.append(f"{s} → {c['id']} : prerequisite for {c['title']}\n")
    lines += ["```\n\n", "## Cross-book handoff\n\n",
              "The versioned [Book I exit contract](pedagogy/book-i-contract.json) lists chapter-specific terms and exit tasks. "
              "Evolutor imports only those explicit chapter outcomes, and recalls them in a short bridge before use. "
              "Its present status is planned-not-yet-taught. Neither unit tests nor this graph activate that contract. "
              "If an imported outcome is removed, either restore it in Book I or teach it locally before use in Book II.\n"]
    result["PREREQUISITE_GRAPH.md"] = "".join(lines)

    domains = sorted({d for c in chapters for d in c["domains"]})
    lines = [header, notice, "## Just-in-time disciplinary maps\n\n",
             "These maps index where each discipline enters the course; arrows follow the reading order. "
             "Exact required edges are in PREREQUISITE_GRAPH.md. They are not detached prerequisite courses.\n\n"]
    for domain in domains:
        selected = [c for c in chapters if domain in c["domains"]]
        lines.append(f"## {domain}\n\n")
        lines.append(" → ".join(c["id"] for c in selected) + "\n\n")
        for c in selected:
            lines.append(f"- **{c['id']}**: {'; '.join(c['introduces'])}.\n")
        lines.append("\n")
    if title == "Evolutor":
        lines.append("## AGI concept map\n\n"
                     "EVOU-04 evaluation on new examples → EVOU-19 fair comparisons → "
                     "EVOU-36 failure and uncertainty → EVOU-38 transfer → "
                     "EVOU-39 operational AGI claims → EVOU-40 reproducible argument. "
                     "AGI means artificial general intelligence; the full reader-facing introduction is reserved for EVOU-39, "
                     "not smuggled into the opening as an assumed capability.\n")
    result["CONCEPT_MAPS.md"] = "".join(lines)

    lines = [header, notice, "## Figure production contract\n\n",
             "Storyboard → semantic TXT companion → editable vector source → teaching caption → "
             "scientific/engineering check → beginner check → rendered-page check. "
             "F1 is the primary teaching sequence. F2 is a small worked-example comparison; it is not automatically "
             "another large figure. Final figure density depends on actual page layout, with a useful visual or worked "
             "example approximately every one or two foundational pages. No quotas override clarity.\n\n"]
    figure_inventory, animation_inventory = [], []
    for c in chapters:
        lines += [f"## {c['id']} — {c['title']}\n\n",
                  f"**Reader question:** {c['readerQuestion']}\n\n",
                  f"**{c['figures'][0]['id']} ({c['figures'][0]['type']}):**\n\n"]
        for i,frame in enumerate(c["frames"],1):
            lines.append(f"{i}. {frame}.\n")
        lines += ["\nKeep objects in stable positions when identity is unchanged. Each frame ledger must mark "
                  "before-state, change, unchanged objects, movement, creation and consumption; use "
                  "'not applicable' rather than inventing a physical process for a software picture.\n\n",
                  f"**Caption teaching target:** {c['mathBridge']}\n\n",
                  f"**{c['figures'][1]['id']} (worked comparison):** "
                  f"Show a correct worked case beside the mistake or boundary tested here: {c['exercise']}\n\n",
                  "**Boundary review:** Label every arrow's meaning. Biology distinguishes covalent links, pairing, "
                  "sequence transfer and control; software distinguishes messages, data, ownership and state transitions. "
                  "Use labels and line styles as well as color.\n\n",
                  f"**Animation decision:** {c['animation']}; storyboard only, no exported frames yet.\n\n"]
        if c["status"] == "internally-reviewed-draft":
            lines.append("**Production override:** the six figure-specific storyboards and actual assets are in "
                         "[research/undergraduate-ch01-storyboard.md](research/undergraduate-ch01-storyboard.md). "
                         "The original F1/F2 course sketches above are planning lineage, not final captions. "
                         "Static vectors produced; animation export remains deferred.\n\n")
        for f in c["figures"]:
            figure_inventory.append({**f,"chapter":c["id"],"readerQuestion":c["readerQuestion"],
                                     "sourcePlan":"Unicode TXT companion plus SVG; reproducible UML source for UML figures",
                                     "reviewStatus":("internally-reviewed-vector" if c["status"] == "internally-reviewed-draft" else "not-drawn-not-reviewed")})
        if c["animation"] == "candidate-keyframe-sequence":
            animation_inventory.append({"id":c["id"]+"-A1","chapter":c["id"],"status":"planned-no-assets",
                                        "frames":[{"number":i,"action":s,"sourceStatus":"not-created"}
                                                  for i,s in enumerate(c["frames"],1)],
                                        "plannedDirectory":"animation/"+c["id"].lower()+"/",
                                        "motionPolicy":"Only animate changes needed to answer the reader question; provide static and reduced-motion alternatives."})
    result["VISUAL_STORYBOARD.md"] = "".join(lines)
    result["pedagogy/figure-inventory.json"] = json.dumps(figure_inventory, indent=2, ensure_ascii=False)+"\n"
    result["pedagogy/animation-inventory.json"] = json.dumps(animation_inventory, indent=2, ensure_ascii=False)+"\n"

    lines = [header, notice, "## Exercises, code and experiments\n\n",
             "Progress through recognition → hand calculation/tracing → application → implementation → "
             "reasoning → research design. Early chapters stop before levels whose tools are untaught. "
             "Every introductory task gets a worked solution or a staged hint and answer check. "
             "Later research tasks get a rubric and explicit acceptable uncertainty, not a fabricated unique answer. "
             "Return to earlier concepts after a delay and interleave worked examples with new attempts.\n\n",
             "Before code: picture, plain-language procedure, trace, pseudocode, then syntax explanation. "
             "No code lab assumes an untaught library. Existing code is audit material, not automatic chapter content.\n\n"]
    for c in chapters:
        lines += [f"## {c['id']}\n\n",
                  f"**Worked example / exercise ladder:** {c['exercise']}\n\n",
                  f"**Code or hands-on progression:** {c['codeLab']}\n\n",
                  "**Solution requirement:** Fully solve the first concrete case; give a second partially worked case, "
                  "then an independent task with answer notes. Ask the learner to explain one wrong answer.\n\n"]
    if title=="Evolutor":
        lines += ["## Training-code route\n\n",
                  "EVOU-03 manual parameter trials → EVOU-06 finite-difference gradient → EVOU-07 tiny network → "
                  "EVOU-08 complete PyTorch loop → EVOU-09 sequence objective → EVOU-10–13 architecture-specific models → "
                  "EVOU-19 common controls → EVOU-29 candidate training → EVOU-36 failures.\n\n",
                  "## Inference-code route\n\n",
                  "EVOU-03 fixed-parameter prediction → EVOU-08 no-update evaluation → EVOU-14 cache parity → "
                  "EVOU-17–18 interpreter and service → EVOU-26 traced request → EVOU-30 runtime → "
                  "EVOU-31 identity → EVOU-32–35 memory, scheduling, profiling and rollback.\n\n",
                  "## Experiment progression\n\n",
                  "Exact hand cases → independent checkers → untouched splits → repeated seeds → nearest conventional "
                  "baselines → declared matched budgets → one-mechanism ablations → failed hypotheses → transfer. "
                  "No training or benchmark is run in this planning milestone.\n"]
    result["LEARNING_PROGRESSION.md"] = "".join(lines)

    lines = [header, notice, "## First-encounter ledger\n\n",
             "This is a planned terminology inventory, not a finished glossary. Definitions, illustrations and glossary "
             "entries must be authored and checked with the chapter. A parser cannot discover every unknown word. "
             "Human noun/acronym audit remains mandatory, including terms inside captions, code and exercises.\n\n",
             "For each term: intuition → everyday example → labeled picture → precise definition → notation. "
             "The eventual digital glossary records short definition, first-use section, related terms and reciprocal "
             "chapter links; the print index records every substantive occurrence. No acronym appears before its "
             "expanded name and explanation.\n\n",
             "| First-use chapter | Terms to teach | Definition / illustration / glossary state |\n",
             "|---|---|---|\n"]
    for c in chapters:
        lines.append(f"| {c['id']} | {'; '.join(c['introduces'])} | " + ("Produced; see Chapter 1 first-sentence audit" if c["status"] == "internally-reviewed-draft" else "Pending chapter production") + " |\n")
    if data["status"] == "chapter-one-production":
        lines.append("\nChapter 1 production overrides the planned inventory: see "
                     "[its first-sentence audit](research/undergraduate-ch01-terminology.md), including "
                     "locally defined preview terms and optional-code vocabulary. Later units deepen these "
                     "ideas rather than assuming the full planned treatment has already occurred.\n")
    result["TERMINOLOGY_AUDIT.md"]="".join(lines)

    lines=[header, notice, "## Complete previous-outline disposition\n\n",
           f"Compared against immutable commit `{data['preservedEdition']['commit']}` on astra-rewrite. "
           "Only its first two chapters were drafted. Planned titles are not treated as existing manuscript content. "
           "Every prior planned topic has an explicit destination, but reuse requires a new prerequisite, scientific and figure audit.\n\n",
           "| Previous chapter | Previous status | Prerequisite diagnosis | New destinations |\n",
           "|---|---|---|---|\n"]
    for c in data["previousChapterAudit"]:
        lines.append(f"| {c['id']} — {c['title']} | {c['previousStatus']} | {c['prerequisiteDiagnosis']} | {', '.join(c['newChapters'])} |\n")
    result["PREVIOUS_EDITION_AUDIT.md"]="".join(lines)
    return {name: text.rstrip() + "\n" for name, text in result.items()}


def main():
    active = json.loads((ROOT/"book/book.json").read_text())
    if active.get("edition") == "4-deep":
        from build_deep_plan import main as deep_main
        return deep_main()
    parser=argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args=parser.parse_args()
    data=json.loads((ROOT/"pedagogy/curriculum.json").read_text())
    contract=json.loads((ROOT/"pedagogy/book-i-contract.json").read_text())
    generated=outputs(data,contract)
    stale=[]
    for name, text in generated.items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text()!=text:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(text)
    if stale:
        raise SystemExit("Stale architecture documents: "+", ".join(stale))
    print(f"Architecture: {len(data['chapters'])} chapters; {len(generated)} generated documents/inventories; "
          + ("fresh" if args.check else "written") + ". This is structural validation, not reader validation.")


if __name__=="__main__":
    main()
