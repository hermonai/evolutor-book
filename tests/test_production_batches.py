"""Portable coordination checks; does not claim ZIP semantic validation or chapter QA."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_supplied_package_audit_covers_all_twenty_archives():
    audit = json.loads(
        (ROOT / "research/integration/package-reuse-audit.json").read_text()
    )
    inventory = json.loads(
        (ROOT / "research/integration/package-inventory.json").read_text()
    )
    entries = audit["chapters"]
    assert audit["archive_count"] == len(entries) == 20
    assert [e["chapter"] for e in entries] == list(range(33, 53))
    assert audit["declared_file_hashes_verified"] == sum(
        e["manifest_hashes_verified"] for e in entries
    )
    original = {e["chapter"]: e for e in inventory["chapters"]}
    for entry in entries:
        assert entry["sha256"] == original[entry["chapter"]]["package_sha256"]
        assert entry["hash_mismatches"] == []
        assert entry["unsafe_paths_or_symlinks"] == []
        assert entry["independent_validation_claims_adopted"] is False
        assert entry["incoming_section_titles"]


def test_substantial_nonoverlapping_batches_cover_all_remaining_chapters():
    dispatch = json.loads(
        (ROOT / "research/integration/production-batches.json").read_text()
    )
    batches = dispatch["batches"]
    assert len(batches) == 4
    assert len({b["id"] for b in batches}) == 4
    assert len({b["thread_id"] for b in batches}) == 4
    assert all(b["thread_id"] for b in batches)
    owned = [n for b in batches for n in range(b["start"], b["end"] + 1)]
    assert owned == list(range(36, 53))
    assert all(b["end"] - b["start"] + 1 >= 3 for b in batches)
    assert all(
        b["accepted"] is False and b["independently_reviewed"] is False for b in batches
    )
