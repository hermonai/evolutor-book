"""Generate the deep-edition planning documents; never manuscript or artwork."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = ("DOGMA = non-Transformer DNA-native model + DOGMA Engine; "
            "Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; "
            "Evolutor = broader genomic computation theory, research and eventual runtime above both.")
OUTPUT_NAMES = ("BOOK_PLAN.md", "COURSE_MAP.md", "PREREQUISITE_GRAPH.md", "CONCEPT_MAPS.md",
                "VISUAL_STORYBOARD.md", "LEARNING_PROGRESSION.md", "TERMINOLOGY_AUDIT.md",
                "PREVIOUS_EDITION_AUDIT.md", "ROADMAP.md", "CHAPTER_1_OUTLINE.md",
                "pedagogy/deep-figure-inventory.json", "pedagogy/deep-animation-inventory.json")


def validate(data, contract, outline):
    if data["status"] not in {"architecture-only-no-manuscript","chapter-one-production","chapter-two-production"}:
        raise ValueError("Unknown deep production milestone")
    produced_count={"architecture-only-no-manuscript":0,"chapter-one-production":1,"chapter-two-production":2}[data["status"]]
    chapters = data["chapters"]
    ids = [c["id"] for c in chapters]
    if not chapters or len(ids) != len(set(ids)):
        raise ValueError("Empty or duplicate chapter IDs")
    if len(chapters) != data["plannedChapterCount"]:
        raise ValueError("Chapter count drift")
    if [c["number"] for c in chapters] != list(range(1, len(chapters)+1)):
        raise ValueError("Printed chapter numbers must be sequential")
    expected_prefix = "DNAD-" if data["book"] == "DNA Computing" else "EVOD-"
    if any(c["id"] != expected_prefix+f"{c['number']:02}" for c in chapters):
        raise ValueError("Chapter identity/number mismatch")
    exports = {c["id"] for c in contract["chapters"]}
    if len(exports) != len(contract["chapters"]) or contract["status"] not in {"planned-not-yet-taught","chapter-one-prototype-available","chapters-one-two-available"}:
        raise ValueError("Invalid Book I export contract")
    known = set()
    for c in chapters:
        if len(c["requires"]) != len(set(c["requires"])) or not set(c["requires"]) <= known:
            raise ValueError("Forward, cyclic, duplicate or missing prerequisite: "+c["id"])
        if not set(c["book1Requires"]) <= exports:
            raise ValueError("Unknown Book I import: "+c["id"])
        if data["book"] == "DNA Computing" and c["book1Requires"]:
            raise ValueError("Book I cannot import itself or Book II")
        expected_status = "internally-reviewed-draft" if c["number"] <= produced_count else "planned-not-drafted"
        if c["status"] != expected_status:
            raise ValueError("Only chapters within the reviewed milestone may be active")
        for field in ("title", "part", "math", "exercise", "visual", "evidenceGate"):
            if not c[field].strip():
                raise ValueError("Missing chapter depth field: "+field)
        if len(c["topics"]) < 3 or len(c["frames"]) < 3:
            raise ValueError("Missing mechanism/visual progression")
        known.add(c["id"])
    for family, expected in (("DOGMA", "non-Transformer DNA-native"),
                             ("Hermon DNA", "Transformer-based DNA")):
        if data["architectureTaxonomy"][family]["family"] != expected:
            raise ValueError(f"{family} taxonomy reversed")
        if data["architectureTaxonomy"][family]["engine"] != family+" Engine":
            raise ValueError("Engine taxonomy drift")
    if "above both" not in data["architectureTaxonomy"]["Evolutor"]["role"]:
        raise ValueError("Evolutor must remain above both families")
    audits = data["previousChapterAudit"]
    if len({a["id"] for a in audits}) != len(audits):
        raise ValueError("Duplicate previous chapter disposition")
    for a in audits:
        if a["action"] not in {"KEEP", "REWRITE", "MERGE", "MOVE TO PREFACE", "ARCHIVE"}:
            raise ValueError("Unknown disposition")
        if not a["destinations"] or not set(a["destinations"]) <= known or not a["reason"]:
            raise ValueError("Missing migration destination")
    if outline["chapter"] != chapters[0]["id"] or outline["title"] != chapters[0]["title"]:
        raise ValueError("Chapter 1 title or ID drift")
    if outline["status"] != "detailed-outline-only" or len(outline["sections"]) != 8:
        raise ValueError("Chapter 1 outline scope drift")
    if [s["number"] for s in outline["sections"]] != list(range(1,9)):
        raise ValueError("Outline section numbering drift")
    for s in outline["sections"]:
        if not all(s[f].strip() for f in ("title","purpose","formalism","workedExample","sourceGate")):
            raise ValueError("Incomplete section")
        f = s["figure"]
        if f["id"] != outline["chapter"]+f"-F{s['number']}" or f["status"] != "planned-no-assets":
            raise ValueError("Outline figure identity/status drift")
        if not f["frames"] or not f["grammar"]:
            raise ValueError("Missing figure storyboard")
    if data["book"] == "DNA Computing":
        expected = [{"id":c["id"], "title":c["title"], "topics":c["topics"],
                     "exitCheck":c["exercise"], "status":("prototype-available" if c["number"] <= produced_count else "planned-not-yet-taught")} for c in chapters]
        if contract["chapters"] != expected:
            raise ValueError("Book I exports drift from actual plan")
    return True


def outputs(data, contract, outline):
    validate(data, contract, outline)
    cs = data["chapters"]
    head = f"# {data['book']}: deep technical edition\n\n"
    note = ("Status: architecture and detailed outlines only; no new manuscript, final figures, "
            "animation frames, models, engines or experiments are delivered. "
            "Canonical source: [deep curriculum](pedagogy/deep-curriculum.json). "
            "Prior editions remain historical references, not the active teaching level.\n\n"
            + TAXONOMY + "\n\n")
    produced_count={"architecture-only-no-manuscript":0,"chapter-one-production":1,"chapter-two-production":2}[data["status"]]
    produced = produced_count > 0
    if produced:
        note = ("Status: canonical deep Chapter 1 is an internally reviewed prototype; all later chapters remain plans. "
                "The undergraduate edition is frozen. No trained model, engine or wet-lab result is delivered. "
                "See [production report](DEEP_CHAPTER_1_REPORT.md) and [edition strategy](CANONICAL_EDITION_STRATEGY.md).\n\n"
                + TAXONOMY + "\n\n")
    if produced_count==2:
        note=("Status: canonical deep Chapters 1–2 are internally reviewed development manuscripts; Chapter 3 onward remains planned. "
              "Prior editions and the Chapter 1-only PDF are preserved. No new wet-lab result, trained model or engine benchmark is delivered. "
              "See [Chapter 2 production report](DEEP_CHAPTER_2_REPORT.md).\n\n"+TAXONOMY+"\n\n")
    result = {}
    def page(title):
        return [head, note, "## "+title+"\n\n"]
    lines = page("Macro table of contents")
    part = None
    for c in cs:
        if c["part"] != part:
            part = c["part"]
            lines.append("### "+part+"\n\n")
        lines.append(f"{c['number']}. **{c['title']}** ({c['id']}). "+ "; ".join(c["topics"])+".\n\n")
    lines.append(f"{len(cs)} substantial chapters; counts follow coherent arguments rather than "
                 "fixed page or lecture quotas. Chapter 1 previews the field; later chapters reconstruct "
                 "mechanisms and proofs in depth. See DEEP_REDESIGN.md for assumed knowledge and reading routes.\n")
    result["BOOK_PLAN.md"] = "".join(lines)

    lines = page("Chapter dependencies, mechanisms and exit tasks")
    lines.append("Entry assumptions: "+"; ".join(data["entryAssumptions"])+".\n\n")
    for c in cs:
        downstream = [x["id"] for x in cs if c["id"] in x["requires"]]
        lines += [f"### {c['id']} — {c['title']}\n\n",
                  "**Required earlier chapters:** "+(", ".join(c["requires"]) or "Declared entry assumptions")+".\n\n",
                  "**Book I imports:** "+(", ".join(c["book1Requires"]) or "None")+". Consult the shared contract for available chapters; planned imports are not completed outcomes.\n\n",
                  "**Mechanisms and concepts:** "+"; ".join(c["topics"])+".\n\n",
                  "**Formal/mathematical development:** "+c["math"]+"\n\n",
                  "**Implementation / assessment:** "+c["exercise"]+"\n\n",
                  "**Enables:** "+(", ".join(downstream) or "Research synthesis")+".\n\n"]
    result["COURSE_MAP.md"] = "".join(lines)

    lines = page("Semantic TXT prerequisite graph")
    lines.append("A → B means that A supplies knowledge required by B; all incoming edges are required. "
                 "It is not a molecular causal arrow. ENTRY is the explicit technical entry contract. "
                 "Chapter 1 roadmaps preview later material without requiring it. "
                 "DNAD imports are one-way from Book I; no reverse dependencies exist.\n\n")
    for c in cs:
        for dep in c["requires"]+c["book1Requires"] or ["ENTRY"]:
            lines.append(f"{dep} → {c['id']} : prerequisite for {c['title']}\n\n")
    lines.append("The [deep Book I contract](pedagogy/deep-book-i-contract.json) contains exact exit tasks. "
                 "A planned link does not establish that a chapter has been taught. "
                 "Qualified readers may demonstrate equivalent knowledge; otherwise follow the named chapters.\n")
    result["PREREQUISITE_GRAPH.md"] = "".join(lines)

    lines = page("Knowledge organization and reading routes")
    for part in dict.fromkeys(c["part"] for c in cs):
        selected = [c for c in cs if c["part"] == part]
        lines += ["### "+part+"\n\n", " → ".join(c["id"] for c in selected)+"\n\n"]
        for c in selected:
            lines.append(f"- {c['id']}: "+"; ".join(c["topics"])+".\n")
        lines.append("\n")
    lines.append("Arrows here indicate reading order, not extra hard prerequisites. "
                 "Use PREREQUISITE_GRAPH.md for minimal dependency closure. Domain abstractions are "
                 "deliberate: explain the mapping, preserved properties and omitted phenomena.\n")
    result["CONCEPT_MAPS.md"] = "".join(lines)

    figures, animations = [], []
    lines = page("Figure and animation strategy")
    lines.append("Each primary visual below is a production brief, not a finished asset or a one-figure quota. "
                 "Use oriented molecular illustrations, chemical reaction/energy diagrams, graphs, tensor flows, "
                 "UML and memory layouts as appropriate. Preserve semantic Unicode TXT companions; no ASCII box art. "
                 "Create figure-specific frame ledgers before prose: before-state, changed/unchanged objects, "
                 "movement, creation/consumption, meaning of arrows, caption and scientific risk. "
                 "Abstraction is allowed, but its relation to the mechanism must be explicit.\n\n")
    for c in cs:
        fs = [s["figure"] for s in outline["sections"]] if c is cs[0] else [
            {"id":c["id"]+"-F1", "title":c["visual"], "grammar":c["visual"],
             "frames":c["frames"], "status":"planned-no-assets"}]
        if produced and c is cs[0]:
            storyboard = json.loads((ROOT/"pedagogy/deep-ch01-storyboard.json").read_text())
            fs = [{"id":f["id"],"title":f["title"],"grammar":f["teachingPurpose"],
                   "frames":f["steps"],"status":"internally-reviewed-produced"} for f in storyboard["figures"]]
        if produced_count==2 and c is cs[1]:
            storyboard=json.loads((ROOT/"pedagogy/deep-ch02-storyboard.json").read_text())
            fs=[{"id":f["id"],"title":f["title"],"grammar":f["mechanism"],
                 "frames":[f["sequence"]],"status":"internally-reviewed-produced"} for f in storyboard["figures"]]
        lines.append(f"### {c['id']} — {c['title']}\n\n")
        for f in fs:
            lines.append(f"**{f['id']} — {f['title']}**. {f['grammar']}\n\n")
            for i, frame in enumerate(f["frames"],1):
                lines.append(f"{i}. {frame}.\n")
            lines.append("\n")
            figures.append({**f,"chapter":c["id"],"sourcePlan":"Editable SVG/TikZ/Graphviz/PlantUML as appropriate + Unicode TXT companion",
                            "reviewStatus":("author-agent-reviewed" if c["number"] <= produced_count else "not-drawn-not-reviewed")})
        # Every chapter has a static sequence brief; only selected mechanisms are animation candidates.
        candidates = ({2,7,8,9,12,15,17,19,20,21,22,26,27,28,30} if data["book"]=="DNA Computing"
                      else {4,6,7,8,9,11,12,13,15,18,19,20,21,26,27,28,30,31,32,33,34,35,36,37,38,39,41,43,44,46,50})
        if c["number"] in candidates or c["number"] <= produced_count:
            frames = (outline["sections"][4]["figure"]["frames"] if data["book"]=="DNA Computing" and c is cs[0]
                      else c["frames"])
            animations.append({"id":c["id"]+"-A1","chapter":c["id"],"status":"storyboard-candidate-no-assets",
                               "frames":[{"number":i,"action":f,"sourceStatus":"not-created"} for i,f in enumerate(frames,1)],
                               "plannedDirectory":"animation/"+c["id"].lower()+"/",
                               "policy":"Decide at chapter storyboard review whether motion adds information; preserve static and reduced-motion versions."})
    if produced:
        actual = json.loads((ROOT/"animation"/cs[0]["id"].lower()/"frames.json").read_text())
        animations[0].update(status="static-keyframes-produced-not-moving-media",
                             frames=[{"number":f["frame"],"action":f["change"],"sourceStatus":"created",
                                      "source":f["source"]} for f in actual])
    if produced_count==2:
        actual=json.loads((ROOT/"animation"/cs[1]["id"].lower()/"frames.json").read_text())
        entry=next(a for a in animations if a["chapter"]==cs[1]["id"])
        entry.update(status="static-keyframes-produced-not-moving-media",
                     frames=[{"number":i,"action":f["sequence"]+" phase "+str(f["phase"]),
                              "sourceStatus":"created","source":f["source"]} for i,f in enumerate(actual,1)])
    result["VISUAL_STORYBOARD.md"] = "".join(lines)
    result["pedagogy/deep-figure-inventory.json"] = json.dumps(figures,indent=2,ensure_ascii=False)+"\n"
    result["pedagogy/deep-animation-inventory.json"] = json.dumps(animations,indent=2,ensure_ascii=False)+"\n"

    lines = page("Mathematics, implementation and evidence")
    lines.append("Motivate the problem → explain the mechanism → define the abstraction → derive → interpret "
                 "→ work an example → implement → test → examine limits. This is a reasoning discipline, "
                 "not a rigid chapter template. Basic programming is assumed; library-specific and domain-specific "
                 "semantics are taught. Proofs, differential equations and formal systems are welcome.\n\n")
    for c in cs:
        lines += [f"### {c['id']}\n\n", c["math"]+"\n\n",c["exercise"]+"\n\n"]
    result["LEARNING_PROGRESSION.md"] = "".join(lines)

    lines = page("Domain terminology and notation plan")
    lines.append("This is a teaching-location index, not a claim that every term is first encountered here. "
                 "Entry mathematics and programming may be used directly. Expand domain acronyms, define symbols "
                 "before substantive use, show shapes/units, and keep a selective glossary plus comprehensive index. "
                 "Do not repeat basic vocabulary merely to pad a chapter. Chapter 1 previews are labeled as such.\n\n")
    lines += ["| Chapter | Domain vocabulary / concepts |\n","|---|---|\n"]
    for c in cs:
        lines.append(f"| {c['id']} | "+"; ".join(c["topics"])+" |\n")
    result["TERMINOLOGY_AUDIT.md"] = "".join(lines)

    lines = page("Complete preceding-outline disposition")
    lines.append(f"Preserved undergraduate branch: astra-undergraduate-rewrite at {data['startingCommit']}. "
                 "Only Chapter 1 was drafted; the other rows are plans, not manuscripts. "
                 "ARCHIVE preserves the old opening and rewrites the new opening from scratch; MERGE retains "
                 "the topic in a deeper treatment, not automatic prose reuse. "
                 "Earlier astra-rewrite and pre-reboot snapshots remain untouched.\n\n")
    lines += ["| Prior ID / title | Prior status | Disposition | New destinations | Reason |\n",
              "|---|---|---|---|---|\n"]
    for a in data["previousChapterAudit"]:
        lines.append(f"| {a['id']} — {a['title']} | {a['previousStatus']} | {a['action']} | "
                     +", ".join(a["destinations"])+" | "+a["reason"]+" |\n")
    result["PREVIOUS_EDITION_AUDIT.md"] = "".join(lines)

    lines = page("Research and production roadmap")
    lines += ["1. **This milestone:** technical reset, macro TOC, dependency graph, visual strategy and detailed Chapter 1 outline. No chapter drafting.\n",
              "2. **Next execution:** fresh deep Chapter 1 as the quality prototype; source audit, exact worked examples, editable figures, tests, LaTeX and every-page visual review.\n",
              "3. **Subsequent production:** follow chapter dependencies; retain negative evidence and verify cross-book imports before assuming them.\n",
              "4. **Research and engineering:** formal semantics → reference implementation → exact/parity tests → experiments → profile → optimized systems.\n",
              "5. **Release:** independent subject and reader review, rights/provenance audit, accessibility work and full reproducibility checks.\n\n",
              "No first-pass figure brief is artwork; no plan is an engine. "
              "New training libraries or IRs require demonstrated need. "
              "Keep the main text focused on mechanisms and reasoning; place full evidence ledgers in research appendices.\n"]
    if produced:
        lines[3] = "1. **Current milestone:** canonical deep Chapter 1, ten original figures, executable example, tests, LaTeX and every-page review.\n"
        lines[4] = "2. **Next execution:** Chapter 2 only, following its source and dependency gates; no undergraduate parallel manuscript.\n"
    if produced_count==2:
        lines[3]="1. **Current milestone:** canonical deep Chapters 1–2; source-backed mechanisms, exact examples, editable vectors/TXT, tests and rendered-page review.\n"
        lines[4]="2. **Next execution:** Chapter 3 — "+cs[2]["title"]+". Do not maintain a second parallel introductory manuscript.\n"
    result["ROADMAP.md"] = "".join(lines)

    lines = page("Detailed Chapter 1 outline: "+outline["title"])
    if produced:
        lines.append("This is the preserved eight-section preproduction outline. Production deliberately expanded it to "
                     +("13" if data["book"]=="DNA Computing" else "12")+
                     " sections and ten figures; see the production report and tex/deep/ch01.tex for the actual chapter.\n\n")
    lines += [outline["scope"]+"\n\n",outline["sizePolicy"]+"\n\n"]
    for s in outline["sections"]:
        lines += [f"### 1.{s['number']} {s['title']}\n\n",
                  s["purpose"]+"\n\n","**Formal depth:** "+s["formalism"]+"\n\n",
                  "**Worked sequence:** "+s["workedExample"]+"\n\n",
                  "**Visual:** "+s["figure"]["id"]+" — "+s["figure"]["title"]+". "+s["figure"]["grammar"]+"\n\n",
                  "**Evidence gate:** "+s["sourceGate"]+"\n\n"]
    lines += ["## Executable example scope\n\n",outline["codePlan"]+"\n\n",
              "## Exercises\n\n",outline["exercisePolicy"]+"\n\n",
              "## Acceptance\n\n"]
    lines += ["- "+item+"\n" for item in outline["acceptance"]]
    result["CHAPTER_1_OUTLINE.md"] = "".join(lines)
    assert set(result) == set(OUTPUT_NAMES)
    return {name:text.rstrip()+"\n" for name,text in result.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads((ROOT/"pedagogy/deep-curriculum.json").read_text())
    contract = json.loads((ROOT/"pedagogy/deep-book-i-contract.json").read_text())
    outline = json.loads((ROOT/"pedagogy/deep-ch01-outline.json").read_text())
    generated = outputs(data, contract, outline)
    stale = []
    for name,text in generated.items():
        path = ROOT/name
        if args.check:
            if not path.exists() or path.read_text() != text:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(text)
    if stale:
        raise SystemExit("Stale deep-edition plan: "+", ".join(stale))
    print(f"Deep plan: {len(data['chapters'])} chapters, {len(generated)} outputs; "
          +("fresh" if args.check else "written")+". Structural checks are not scientific or reader validation.")


if __name__ == "__main__":
    main()
