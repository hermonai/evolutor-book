import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_textbook_source_and_preservation_contract():
    spec=importlib.util.spec_from_file_location("textbook_checks",ROOT/"scripts/check-textbook.py")
    checks=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)
    checks.main()

def test_new_candidate_does_not_promote_chapter3_to_accepted():
    state=json.loads((ROOT/"book/textbook-progress.json").read_text())
    assert state=={"accepted":[1,2],"review":[3],"format":"latex"}
    accepted=json.loads((ROOT/"book/book.json").read_text())
    assert len(accepted["chapters"])==2

def test_progress_overlay_cannot_rewrite_accepted_outputs():
    spec=importlib.util.spec_from_file_location("textbook_plan",ROOT/"scripts/build_textbook_plan.py")
    plan=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plan)
    inputs=[json.loads((ROOT/p).read_text()) for p in ("pedagogy/deep-curriculum.json","pedagogy/deep-book-i-contract.json","pedagogy/deep-ch01-outline.json")]
    before=plan.legacy.outputs(*inputs)
    after=plan.outputs(*inputs)
    assert {key for key in before if before[key]!=after[key]}=={"ROADMAP.md"}
    assert "cumulative acceptance and independent review remain open" in after["ROADMAP.md"]
