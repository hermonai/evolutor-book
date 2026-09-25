from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_review_record_binds_complete_authored_source_set():
    import hashlib
    import json

    record = json.loads(
        (ROOT / "artifacts/deep/ch18-review.json").read_text()
    )
    actual = {
        str(p.relative_to(ROOT))
        for p in (ROOT / "drafts/ch18").rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    assert set(record["sources"]) == actual
    for path, digest in record["sources"].items():
        assert (
            hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
        )
    assert record["allPagesInspected"]
    assert record["figures"] == 5 and record["exercises"] == 12
    assert record["status"].endswith("no acceptance promotion")
    assert record["openGates"]
    assert (
        len(json.loads((ROOT / "book/book.json").read_text())["chapters"])
        == 2
    )
    figures = ROOT / "drafts/ch18/figures"
    assert len(list(figures.glob("*.tex"))) == 5
    assert {p.stem for p in figures.glob("*.tex")} == {
        p.stem for p in figures.glob("*.txt")
    }


def test_local_pdf_matches_review_when_available():
    import hashlib
    import json

    record = json.loads(
        (ROOT / "artifacts/deep/ch18-review.json").read_text()
    )
    path = ROOT / record["pdf"]
    if not path.exists():
        pytest.skip("Review PDF is generated and gitignored")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
