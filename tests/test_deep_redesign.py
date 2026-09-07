"""Deep-edition planning, isolation and preservation contracts, not scientific certification."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

PLAN = module("deep_plan", "scripts/build_deep_plan.py")

def inputs():
    return tuple(json.loads((ROOT/p).read_text()) for p in (
        "pedagogy/deep-curriculum.json", "pedagogy/deep-book-i-contract.json",
        "pedagogy/deep-ch01-outline.json"))

def test_deep_deliverables_are_fresh_and_complete():
    data, contract, outline = inputs()
    assert PLAN.validate(data, contract, outline)
    for name, text in PLAN.outputs(data, contract, outline).items():
        assert (ROOT/name).read_text() == text, name
    for name in ("DEEP_REDESIGN.md", "TECHNICAL_LEVEL_RESET.md", "CHAPTER_STANDARD.md",
                 "REVIEW_GATES.md", "research/deep-source-register.md"):
        assert (ROOT/name).is_file()

@pytest.mark.parametrize("defect", [
    "forward", "duplicate-id", "missing-import", "missing-math", "missing-frame",
    "wrong-count", "active-chapter", "dogma", "hermon", "runtime", "title",
    "missing-destination", "figure-status", "missing-exercise",
])
def test_invalid_plans_are_rejected(defect):
    data, contract, outline = deepcopy(inputs())
    if defect == "forward":
        data["chapters"][0]["requires"] = [data["chapters"][-1]["id"]]
    elif defect == "duplicate-id":
        data["chapters"][1]["id"] = data["chapters"][0]["id"]
    elif defect == "missing-import":
        data["chapters"][0]["book1Requires"] = ["DNAD-99"]
    elif defect == "missing-math":
        data["chapters"][0]["math"] = ""
    elif defect == "missing-frame":
        data["chapters"][0]["frames"] = ["one"]
    elif defect == "wrong-count":
        data["plannedChapterCount"] += 1
    elif defect == "active-chapter":
        data["chapters"][1]["status"] = "internally-reviewed-draft"
    elif defect in {"dogma","hermon"}:
        family = "DOGMA" if defect == "dogma" else "Hermon DNA"
        data["architectureTaxonomy"][family]["family"] = "reversed"
    elif defect == "runtime":
        data["architectureTaxonomy"]["Evolutor"]["role"] = "DOGMA only"
    elif defect == "title":
        outline["title"] = "Old beginner opening"
    elif defect == "missing-destination":
        data["previousChapterAudit"][0]["destinations"] = []
    elif defect == "figure-status":
        outline["sections"][0]["figure"]["status"] = "finished"
    else:
        outline["sections"][0]["workedExample"] = ""
    with pytest.raises(ValueError):
        PLAN.validate(data, contract, outline)

def test_every_preceding_topic_is_accounted_for():
    data, _, _ = inputs()
    old = json.loads(subprocess.check_output(
        ["git","show",data["startingCommit"]+":pedagogy/curriculum.json"],cwd=ROOT,text=True))
    assert [c["id"] for c in old["chapters"]] == [a["id"] for a in data["previousChapterAudit"]]
    assert [c["title"] for c in old["chapters"]] == [a["title"] for a in data["previousChapterAudit"]]
    assert data["previousChapterAudit"][0]["action"] == "ARCHIVE"
    assert sum(a["previousStatus"] == "internally-reviewed-draft" for a in data["previousChapterAudit"]) == 1

def test_new_edition_cannot_build_a_preserved_manuscript():
    book = json.loads((ROOT/"book/book.json").read_text())
    gate = module("deep_gate", "scripts/require_active_manuscript.py")
    assert book["edition"] == "4-deep" and gate.validate_book(book)
    for defect in ("empty","preserved","later","unreviewed","old-main"):
        attempt=deepcopy(book)
        if defect=="empty":attempt["chapters"]=[]
        elif defect=="preserved":attempt["chapters"][0]["source"]="tex/undergraduate/ch01.tex"
        elif defect=="later":attempt["chapters"][0]["number"]=2
        elif defect=="unreviewed":attempt["chapters"][0]["status"]="planned-not-drafted"
        else:attempt["main"]="tex/undergraduate-evolutor.tex"
        with pytest.raises(ValueError):gate.validate_book(attempt)

def test_prior_manuscripts_artwork_examples_and_pdfs_are_byte_identical():
    data, _, _ = inputs()
    prefixes = ["tex/undergraduate", "tex/chapters", "book/figures/undergraduate",
                "book/diagrams/undergraduate", "examples/undergraduate", "output/pdf",
                "historical"]
    paths = subprocess.check_output(["git","ls-tree","-r","--name-only",data["startingCommit"],
                                     "--",*prefixes],cwd=ROOT,text=True).splitlines()
    assert any(p.endswith(".pdf") for p in paths)
    for path in paths:
        before = subprocess.check_output(["git","show",data["startingCommit"]+":"+path],cwd=ROOT)
        assert (ROOT/path).read_bytes() == before, path

def test_shared_contract_matches_sibling_and_all_exports_remain_planned():
    data, contract, _ = inputs()
    sibling = ROOT.parent/("evolutor-book" if data["book"]=="DNA Computing" else "dna-computing-book")
    path = sibling/"pedagogy/deep-book-i-contract.json"
    if path.exists():
        assert json.loads(path.read_text()) == contract
    assert contract["chapters"][0]["status"] == "prototype-available"
    assert all(c["status"] == "planned-not-yet-taught" for c in contract["chapters"][1:])

def test_separate_model_engine_and_runtime_dependencies():
    data, _, _ = inputs()
    if data["book"] != "Evolutor":
        return
    lookup = {c["id"]:c for c in data["chapters"]}
    assert "EVOD-18" in lookup["EVOD-31"]["requires"]
    assert "EVOD-23" in lookup["EVOD-35"]["requires"]
    assert {"EVOD-34","EVOD-38"} <= set(lookup["EVOD-39"]["requires"])
    assert "EVOD-7" not in lookup
    assert "EVOD-07" in lookup["EVOD-18"]["requires"]
    assert lookup["EVOD-51"]["number"] > lookup["EVOD-47"]["number"]

def test_active_documents_keep_taxonomy_and_allow_abstraction():
    for name in ("BOOK_PLAN.md","COURSE_MAP.md","PREREQUISITE_GRAPH.md","VISUAL_STORYBOARD.md",
                 "ROADMAP.md","PEDAGOGICAL_REDESIGN.md"):
        text = (ROOT/name).read_text()
        assert "DOGMA = non-Transformer DNA-native" in text, name
        assert "Hermon DNA = Transformer-based DNA" in text, name
    policy = (ROOT/"DEEP_REDESIGN.md").read_text()
    assert "Useful abstraction is welcome" in policy
    assert "No artificial university-level ceiling" in json.dumps(inputs()[0])
    assert "no accepted deep manuscript" in (ROOT/"scripts/require_active_manuscript.py").read_text()

def test_inventories_distinguish_produced_chapter_one_from_future_plans():
    figures=json.loads((ROOT/"pedagogy/deep-figure-inventory.json").read_text())
    animations=json.loads((ROOT/"pedagogy/deep-animation-inventory.json").read_text())
    assert len({f["id"] for f in figures})==len(figures)
    assert len(figures)==len(inputs()[0]["chapters"])+9
    assert all(f["status"]=="internally-reviewed-produced" for f in figures[:10])
    assert all(f["status"]=="planned-no-assets" for f in figures[10:])
    assert animations[0]["status"]=="static-keyframes-produced-not-moving-media"
    assert all(f["sourceStatus"]=="created" for f in animations[0]["frames"])
    assert all(a["status"]=="storyboard-candidate-no-assets" for a in animations[1:])
    assert (ROOT/"tex/deep/ch01.tex").exists()
    assert not (ROOT/"tex/deep/ch02.tex").exists()

@pytest.mark.parametrize("defect", ["stale", "missing-manifest", "unreviewed-figure"])
def test_review_is_bound_to_actual_sources(tmp_path, defect):
    import shutil
    gate = module("hashed_gate", "scripts/require_active_manuscript.py")
    review = json.loads((ROOT/"artifacts/deep/ch01-review.json").read_text())
    for path in review["reviewedSources"]:
        target = tmp_path/path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/path, target)
    if defect == "stale":
        (tmp_path/"tex/deep/ch01.tex").write_text("changed after inspection")
    elif defect == "missing-manifest":
        review.pop("reviewedSources")
    else:
        path = next(p for p in review["reviewedSources"] if p.endswith(".svg"))
        review["reviewedSources"].pop(path)
    target = tmp_path/"artifacts/deep/ch01-review.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(review))
    book = json.loads((ROOT/"book/book.json").read_text())
    with pytest.raises(ValueError):
        gate.validate_book(book, tmp_path)
