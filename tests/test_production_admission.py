"""Admission checks on synthetic files only; never run changing chapter code."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

SPEC = importlib.util.spec_from_file_location(
    "production_admission", Path(__file__).parents[1] / "scripts/audit-production.py"
)
r = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)


def put(root, name, value):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) if isinstance(value, (dict, list)) else value)


def amend(root, name, fn):
    value = json.loads((root / name).read_text())
    fn(value)
    put(root, name, value)


BUILD = "build/ch36/build-record.json"
REVIEW = "research/integration/ch36/local-review.json"
PROVENANCE = "research/integration/ch36/source-verification.json"
PDF = "output/pdf/evolutor-ch36-review.pdf"
DISPATCH = "research/integration/production-batches.json"


@pytest.fixture
def candidate(tmp_path):
    root = tmp_path / "checkout with spaces"
    files = {
        f"drafts/ch36/{name}": f"synthetic {name}"
        for name in (
            "manuscript.tex",
            "results.json",
            "build.py",
            "review.tex",
            "sources.tex",
            "README.md",
            "STORYBOARD.md",
            "figures/01-mechanism.tex",
            "figures/01-mechanism.txt",
        )
    }
    # A sentinel proves the checker must not import or run these sources.
    files["drafts/ch36/reference.py"] = 'raise RuntimeError("never execute")'
    files["tests/test_ch36_reference.py"] = 'raise RuntimeError("never execute")'
    for path, value in files.items():
        put(root, path, value)
    hashes = {path: r.digest((root / path).read_bytes()) for path in files}
    put(root, PDF, "%PDF-synthetic fixture, not a rendered document")
    pdf_hash = r.digest((root / PDF).read_bytes())
    package_hash = "a" * 64
    put(
        root,
        "research/integration/package-reuse-audit.json",
        {
            "chapters": [{"chapter": 36, "sha256": package_hash}],
        },
    )
    put(
        root,
        DISPATCH,
        {
            "batches": [
                {
                    "id": "A",
                    "start": 36,
                    "end": 38,
                    "handoff": "research/integration/batches/A-handoff.md",
                }
            ]
        },
    )
    put(root, "research/integration/batches/A-handoff.md", "Synthetic handoff")
    put(
        root,
        "research/integration/ch36/package-adoption.md",
        "Mapping requires manual inspection",
    )
    put(root, "research/integration/ch36/technical-audit.md", "Premises and controls")
    put(
        root,
        PROVENANCE,
        {
            "chapter": 36,
            "package_sha256": package_hash,
            "inherited_validation_claims_adopted": False,
        },
    )
    put(
        root,
        BUILD,
        {
            "pdf": PDF,
            "pages": 2,
            "sha256": pdf_hash,
            "sources": hashes,
        },
    )
    put(
        root,
        REVIEW,
        {
            "chapter": 36,
            "pdf": PDF,
            "pdf_sha256": pdf_hash,
            "pages": 2,
            "source_hashes": hashes,
            "independent_review": False,
            "accepted": False,
            "tests": {"chapter_passed": 5},
            "visual_review": {
                "status": "PASS WITH NOTES",
                "mode": "all pages color and grayscale",
            },
        },
    )
    return root


def result(root):
    return r.audit(root, 36, 36)["chapters"][0]


def test_complete_declarations_only_admit_manual_review(candidate):
    before = {str(p): p.read_bytes() for p in candidate.rglob("*") if p.is_file()}
    value = result(candidate)
    assert value["mechanically_ready_for_coordinator_review"]
    assert value["blockers"] == []
    assert value["manual_checks_pending"] == r.MANUAL_CHECKS
    assert (
        not value["integrated"]
        and not value["accepted"]
        and not value["independently_reviewed"]
    )
    assert before == {
        str(p): p.read_bytes() for p in candidate.rglob("*") if p.is_file()
    }


@pytest.mark.parametrize(
    "path",
    [
        "drafts/ch36/manuscript.tex",
        "drafts/ch36/reference.py",
        "drafts/ch36/figures/01-mechanism.txt",
        "tests/test_ch36_reference.py",
        "research/integration/ch36/package-adoption.md",
        "research/integration/ch36/technical-audit.md",
        "research/integration/batches/A-handoff.md",
        PDF,
        BUILD,
        REVIEW,
        PROVENANCE,
    ],
)
def test_presence_of_directory_does_not_close_missing_evidence(candidate, path):
    (candidate / path).unlink()
    value = result(candidate)
    assert not value["mechanically_ready_for_coordinator_review"]
    assert value["blockers"]


@pytest.mark.parametrize(
    "path",
    [
        "drafts/ch36/manuscript.tex",
        "drafts/ch36/reference.py",
        "drafts/ch36/figures/01-mechanism.tex",
        "tests/test_ch36_reference.py",
        PDF,
    ],
)
def test_stale_pdf_or_source_record_cannot_pass(candidate, path):
    with (candidate / path).open("a") as stream:
        stream.write("changed")
    assert any("digest mismatch" in e for e in result(candidate)["blockers"])


@pytest.mark.parametrize("record,key", [(BUILD, "sources"), (REVIEW, "source_hashes")])
def test_hash_mapping_must_cover_entire_chapter(candidate, record, key):
    amend(candidate, record, lambda v: v[key].pop("drafts/ch36/reference.py"))
    assert any("uncovered source" in e for e in result(candidate)["blockers"])


def test_late_added_source_is_not_silently_outside_review(candidate):
    put(candidate, "drafts/ch36/helper.py", "unreviewed source")
    assert any(
        "uncovered source drafts/ch36/helper.py" in e
        for e in result(candidate)["blockers"]
    )


def test_interpreter_cache_is_not_an_authored_source(candidate):
    put(candidate, "drafts/ch36/__pycache__/reference.cpython.pyc", "cache")
    assert result(candidate)["mechanically_ready_for_coordinator_review"]


@pytest.mark.parametrize(
    "record,key,value",
    [
        (BUILD, "pages", True),
        (BUILD, "pages", 0),
        (BUILD, "pages", -1),
        (BUILD, "sha256", "bad"),
        (BUILD, "pdf", "other.pdf"),
        (REVIEW, "pages", 3),
        (REVIEW, "chapter", 37),
        (REVIEW, "pdf_sha256", "f" * 64),
        (REVIEW, "accepted", True),
        (REVIEW, "independent_review", True),
        (REVIEW, "tests", []),
        (REVIEW, "tests", {"chapter_passed": True}),
        (REVIEW, "tests", {"chapter_passed": 0}),
        (REVIEW, "visual_review", []),
        (REVIEW, "visual_review", {"status": "FAIL", "mode": "all"}),
        (REVIEW, "visual_review", {"status": "PASSIVE", "mode": "all"}),
        (PROVENANCE, "chapter", 37),
        (PROVENANCE, "package_sha256", "b" * 64),
        (PROVENANCE, "inherited_validation_claims_adopted", True),
    ],
)
def test_wrong_or_overclaimed_records_are_not_admitted(candidate, record, key, value):
    amend(candidate, record, lambda v: v.update({key: value}))
    assert not result(candidate)["mechanically_ready_for_coordinator_review"]


@pytest.mark.parametrize("path", [BUILD, REVIEW, PROVENANCE])
@pytest.mark.parametrize("content", ["not JSON", "[]", "null"])
def test_malformed_evidence_reports_blocker_not_success(candidate, path, content):
    put(candidate, path, content)
    assert not result(candidate)["mechanically_ready_for_coordinator_review"]


def test_declared_transitive_dependency_is_hash_checked(candidate):
    put(candidate, "drafts/ch35/reference.py", "stable predecessor")
    sha = r.digest((candidate / "drafts/ch35/reference.py").read_bytes())
    amend(
        candidate,
        REVIEW,
        lambda v: v.update(
            {"transitive_dependencies": {"drafts/ch35/reference.py": sha}}
        ),
    )
    assert result(candidate)["mechanically_ready_for_coordinator_review"]
    put(candidate, "drafts/ch35/reference.py", "changed predecessor")
    assert any(
        "declared dependency: digest mismatch" in e
        for e in result(candidate)["blockers"]
    )


@pytest.mark.parametrize("path", ["../outside.txt", "/etc/passwd"])
def test_hash_records_cannot_read_outside_checkout(candidate, path):
    amend(candidate, BUILD, lambda v: v["sources"].update({path: "0" * 64}))
    assert any("non-relative evidence path" in e for e in result(candidate)["blockers"])


def test_external_symlink_cannot_supply_evidence(candidate):
    target = candidate.parent / "outside.txt"
    target.write_text("outside")
    link = candidate / "drafts/ch36/escape.txt"
    link.symlink_to(target)
    amend(
        candidate,
        BUILD,
        lambda v: v["sources"].update({"drafts/ch36/escape.txt": r.digest(b"outside")}),
    )
    assert any("evidence escapes checkout" in e for e in result(candidate)["blockers"])


def test_concurrent_edit_is_detected_without_executing_sources(candidate):
    e = r.Evidence(candidate)
    e.read("drafts/ch36/reference.py")
    put(candidate, "drafts/ch36/reference.py", "changed while auditing")
    assert e.finish() == ["changed during audit: drafts/ch36/reference.py"]


def test_source_added_during_scan_cannot_escape_coverage(candidate, monkeypatch):
    original = r.Evidence.document

    def read_then_add(self, name):
        value = original(self, name)
        if name == REVIEW:
            put(candidate, "drafts/ch36/late-helper.py", "late addition")
        return value

    monkeypatch.setattr(r.Evidence, "document", read_then_add)
    assert (
        "chapter source inventory changed during audit" in result(candidate)["blockers"]
    )


def test_cli_require_ready_and_read_only_progress_modes(candidate):
    command = [
        sys.executable,
        str(SPEC.origin),
        "--root",
        str(candidate),
        "--start",
        "36",
        "--end",
        "36",
        "--json",
    ]
    complete = subprocess.run(
        command + ["--require-ready"], capture_output=True, text=True
    )
    assert complete.returncode == 0
    assert json.loads(complete.stdout)["mechanically_ready_chapters"] == [36]
    (candidate / REVIEW).unlink()
    progress = subprocess.run(command, capture_output=True, text=True)
    assert progress.returncode == 0
    assert json.loads(progress.stdout)["mechanically_ready_chapters"] == []
    admission = subprocess.run(
        command + ["--require-ready"], capture_output=True, text=True
    )
    assert admission.returncode == 1


def test_duplicate_owner_or_package_fails_closed(candidate):
    amend(candidate, DISPATCH, lambda v: v["batches"].append(dict(v["batches"][0])))
    assert "chapter has no dispatched batch owner" in result(candidate)["blockers"]
    amend(
        candidate,
        "research/integration/package-reuse-audit.json",
        lambda v: v["chapters"].append(dict(v["chapters"][0])),
    )
    assert (
        "source verification does not match audited package digest"
        in result(candidate)["blockers"]
    )


def test_missing_digest_in_both_provenance_records_cannot_pass(candidate):
    amend(candidate, PROVENANCE, lambda v: v.pop("package_sha256"))
    amend(
        candidate,
        "research/integration/package-reuse-audit.json",
        lambda v: v["chapters"][0].pop("sha256"),
    )
    assert not result(candidate)["mechanically_ready_for_coordinator_review"]


def test_empty_semantic_description_cannot_pass(candidate):
    put(candidate, "drafts/ch36/figures/01-mechanism.txt", " ")
    assert any(
        "empty figure source/description" in e for e in result(candidate)["blockers"]
    )


@pytest.mark.parametrize("start,end", [(35, 36), (36, 53), (40, 39)])
def test_scope_cannot_promote_historical_or_unplanned_chapters(candidate, start, end):
    with pytest.raises(ValueError, match="scoped"):
        r.audit(candidate, start, end)
