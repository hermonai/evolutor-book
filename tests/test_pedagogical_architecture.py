"""Structural planning checks do not claim scientific or pedagogical validation."""
from copy import deepcopy
from pathlib import Path
import importlib.util
import json
import re
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_pedagogy", ROOT / "scripts/build_pedagogy.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def inputs():
    return (json.loads((ROOT / "pedagogy/curriculum.json").read_text()),
            json.loads((ROOT / "pedagogy/book-i-contract.json").read_text()))


def test_architecture_deliverables_and_freshness():
    data, contract = inputs()
    for name in ("PEDAGOGICAL_REDESIGN.md", "BEGINNER_REVIEW.md", "PROFESSIONAL_REVIEW.md",
                 "REVIEW_GATES.md", "FIGURE_SYSTEM.md"):
        assert (ROOT / name).is_file()
    for name, expected in MODULE.outputs(data, contract).items():
        assert (ROOT / name).read_text() == expected, name


def test_dependencies_first_encounters_and_inventory_are_valid():
    data, contract = inputs()
    assert MODULE.validate(data, contract)
    assert len(data["chapters"]) == (36 if data["book"] == "DNA Computing" else 40)
    figures = json.loads((ROOT / "pedagogy/figure-inventory.json").read_text())
    assert len(figures) == 2 * len(data["chapters"])
    assert all(f["reviewStatus"] == "not-drawn-not-reviewed" for f in figures)


@pytest.mark.parametrize("defect", ["forward", "missing-import", "duplicate-term", "missing-frame"])
def test_validator_rejects_broken_architecture(defect):
    data, contract = deepcopy(inputs())
    if defect == "forward":
        data["chapters"][0]["requires"] = [data["chapters"][-1]["id"]]
    elif defect == "missing-import":
        data["chapters"][0]["book1Requires"] = ["DNAU-99"]
    elif defect == "duplicate-term":
        data["chapters"][1]["introduces"].append(data["chapters"][0]["introduces"][0])
    else:
        data["chapters"][0]["frames"] = ["one frame only"]
    with pytest.raises(AssertionError):
        MODULE.validate(data, contract)


def test_previous_outline_has_complete_disposition():
    data, _ = inputs()
    old = subprocess.check_output(["git", "show", data["preservedEdition"]["commit"] + ":BOOK_PLAN.md"],
                                  cwd=ROOT, text=True)
    ids = re.findall(r"\*\*((?:DNA|EVO)-\d+) —", old)
    assert ids == [c["id"] for c in data["previousChapterAudit"]]
    assert sum(c["previousStatus"] == "drafted" for c in data["previousChapterAudit"]) == 2


def test_previous_chapter_sources_remain_byte_identical():
    data, _ = inputs()
    for name in ("tex/chapters/ch01.tex", "tex/chapters/ch02.tex"):
        old = subprocess.check_output(["git", "show", data["preservedEdition"]["commit"] + ":" + name],
                                      cwd=ROOT)
        assert (ROOT / name).read_bytes() == old


def test_no_active_chapters_and_pdf_build_is_blocked():
    book = json.loads((ROOT / "book/book.json").read_text())
    assert book["chapters"] == [] and book["main"] is None and book["graphs"] == []
    assert not re.findall(r"\\input\{", (ROOT / "tex/chapters/manifest.tex").read_text())
    for target in ("pdf", "check-pdf"):
        result = subprocess.run(["make", target, "PYTHON=" + sys.executable], cwd=ROOT,
                                text=True, capture_output=True)
        assert result.returncode != 0
        assert "No accepted undergraduate manuscript chapters" in result.stdout + result.stderr


def test_shared_book_i_contract_has_no_drift():
    data, contract = inputs()
    if data["book"] == "DNA Computing":
        assert [c["id"] for c in contract["chapters"]] == [c["id"] for c in data["chapters"]]
        for entry, chapter in zip(contract["chapters"], data["chapters"]):
            assert entry["terms"] == chapter["introduces"]
            assert entry["exitCheck"] == chapter["exercise"]
    sibling = ROOT.parent / ("evolutor-book" if data["book"] == "DNA Computing" else "dna-computing-book")
    other = sibling / "pedagogy/book-i-contract.json"
    if other.exists():
        assert json.loads(other.read_text()) == contract
    assert contract["status"] == "planned-not-yet-taught"
