"""The user-authorized taxonomy must not drift or masquerade as implementation evidence."""
from copy import deepcopy
import json
from pathlib import Path
import importlib.util
import pytest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("plan",ROOT/"scripts/build_pedagogy.py")
plan=importlib.util.module_from_spec(spec);spec.loader.exec_module(plan)

@pytest.mark.parametrize("family",["DOGMA","Hermon DNA"])
def test_taxonomy_reversal_is_rejected(family):
    d=json.loads((ROOT/"pedagogy/curriculum.json").read_text())
    c=json.loads((ROOT/"pedagogy/book-i-contract.json").read_text())
    broken=deepcopy(d)
    broken["architectureTaxonomy"][family]["family"]="Transformer-based DNA" if family=="DOGMA" else "non-Transformer DNA-native"
    with pytest.raises(AssertionError,match="taxonomy reversed"):plan.validate(broken,c)

def test_original_ids_and_separate_engine_paths_are_retained():
    d=json.loads((ROOT/"pedagogy/curriculum.json").read_text())
    lookup={c["id"]:c for c in d["chapters"]}
    assert {f"EVOU-{i:02}" for i in range(1,41)} <= lookup.keys()
    assert len({c["part"] for c in d["chapters"]})==14
    assert all(c["status"]=="planned-not-drafted" for c in d["chapters"][1:])
    assert "EVOU-42" in lookup["EVOU-51"]["requires"]
    assert "EVOU-47" in lookup["EVOU-55"]["requires"]
    assert {"EVOU-51","EVOU-55"} <= set(lookup["EVOU-58"]["requires"])
    assert lookup["EVOU-02"]["number"]==2
    assert "EVOU-41" in lookup["EVOU-42"]["requires"]

def test_active_taxonomy_is_visible_in_required_docs():
    for name in ("BOOK_PLAN.md","PEDAGOGICAL_REDESIGN.md","COURSE_MAP.md",
                 "PREREQUISITE_GRAPH.md","VISUAL_STORYBOARD.md","ROADMAP.md",
                 "research/architecture-taxonomy.md"):
        text=(ROOT/name).read_text()
        assert "DOGMA" in text and "Hermon DNA" in text and "non-Transformer" in text,name
