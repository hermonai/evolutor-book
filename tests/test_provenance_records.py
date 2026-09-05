import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_provenance import ProvenanceError, validate_file, validate_record  # noqa: E402


def test_checked_in_provenance_records_are_valid() -> None:
    records = sorted((ROOT / "research" / "provenance").glob("*.json"))
    assert records
    for record in records:
        validate_file(record)


def test_claim_requires_immutable_source_identity() -> None:
    record_path = ROOT / "research" / "provenance" / "claim-g012.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["evidence"][0]["source_identity"] = {}
    with pytest.raises(ProvenanceError, match="commit or content_sha256"):
        validate_record(record)


def test_claim_status_is_closed_vocabulary() -> None:
    record_path = ROOT / "research" / "provenance" / "claim-g012.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["status"] = "probably-correct"
    with pytest.raises(ProvenanceError, match="unsupported claim status"):
        validate_record(record)
