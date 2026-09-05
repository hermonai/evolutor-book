#!/usr/bin/env python3
"""Validate the book's lightweight JSON provenance records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ARCHITECTURE_FIELDS = {
    "schema_version",
    "record_type",
    "architecture_id",
    "lineage_name",
    "family",
    "architecture_version",
    "attention",
    "recurrence",
    "state_model",
    "context_memory",
    "training_semantics",
    "inference_semantics",
    "checkpoint_format",
    "reference_implementation",
    "optimized_implementations",
    "evidence",
    "limitations",
}

CLAIM_FIELDS = {
    "schema_version",
    "record_type",
    "claim_id",
    "claim",
    "classification",
    "status",
    "architecture_ids",
    "evidence",
    "limitations",
}

ALLOWED_CLAIM_STATUSES = {
    "proposed",
    "active",
    "quarantined",
    "narrowed",
    "withdrawn",
    "superseded",
    "reinstated",
}


class ProvenanceError(ValueError):
    """Raised when a provenance record violates the local schema."""


def _require_fields(record: dict[str, Any], required: set[str]) -> None:
    missing = sorted(required - record.keys())
    if missing:
        raise ProvenanceError(f"missing required fields: {', '.join(missing)}")


def _require_nonempty_text(record: dict[str, Any], fields: tuple[str, ...]) -> None:
    for field in fields:
        value = record[field]
        if not isinstance(value, str) or not value.strip():
            raise ProvenanceError(f"{field} must be non-empty text")


def _validate_source_identity(source: dict[str, Any]) -> None:
    if not isinstance(source, dict):
        raise ProvenanceError("each evidence entry must be an object")
    _require_fields(source, {"repository", "path", "source_identity"})
    _require_nonempty_text(source, ("repository", "path"))
    identity = source["source_identity"]
    if not isinstance(identity, dict):
        raise ProvenanceError("source_identity must be an object")
    accepted = {"commit", "content_sha256"}
    present = [key for key in accepted if isinstance(identity.get(key), str) and identity[key]]
    if not present:
        raise ProvenanceError("source_identity needs a commit or content_sha256")


def validate_record(record: dict[str, Any]) -> None:
    """Validate one decoded provenance record or raise ``ProvenanceError``."""

    if not isinstance(record, dict):
        raise ProvenanceError("record must be a JSON object")
    if record.get("schema_version") != 1:
        raise ProvenanceError("schema_version must be 1")

    record_type = record.get("record_type")
    if record_type == "architecture":
        _require_fields(record, ARCHITECTURE_FIELDS)
        _require_nonempty_text(
            record,
            (
                "architecture_id",
                "lineage_name",
                "family",
                "architecture_version",
                "state_model",
                "context_memory",
                "training_semantics",
                "inference_semantics",
                "checkpoint_format",
                "reference_implementation",
            ),
        )
        if not isinstance(record["attention"], bool) or not isinstance(record["recurrence"], bool):
            raise ProvenanceError("attention and recurrence must be booleans")
        if not isinstance(record["optimized_implementations"], list):
            raise ProvenanceError("optimized_implementations must be a list")
    elif record_type == "claim":
        _require_fields(record, CLAIM_FIELDS)
        _require_nonempty_text(record, ("claim_id", "claim", "classification", "status"))
        if record["status"] not in ALLOWED_CLAIM_STATUSES:
            raise ProvenanceError(f"unsupported claim status: {record['status']}")
        if not isinstance(record["architecture_ids"], list) or not record["architecture_ids"]:
            raise ProvenanceError("architecture_ids must be a non-empty list")
    else:
        raise ProvenanceError("record_type must be architecture or claim")

    evidence = record["evidence"]
    if not isinstance(evidence, list) or not evidence:
        raise ProvenanceError("evidence must be a non-empty list")
    for source in evidence:
        _validate_source_identity(source)
    if not isinstance(record["limitations"], list) or not record["limitations"]:
        raise ProvenanceError("limitations must be a non-empty list")


def validate_file(record_path: Path) -> None:
    """Load and validate a JSON provenance record."""

    with record_path.open(encoding="utf-8") as handle:
        record = json.load(handle)
    validate_record(record)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path)
    args = parser.parse_args()
    for record_path in args.records:
        validate_file(record_path)
        print(f"valid: {record_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
