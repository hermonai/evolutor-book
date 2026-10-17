"""Validate the current 52-chapter navigation map without modifying frozen plans."""

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def check():
    data = json.loads((ROOT / "chapter-structure.json").read_text())
    chapters = data["chapters"]
    assert data["planned_chapters"] == len(chapters) == 52
    assert [c["number"] for c in chapters] == list(range(1, 53))
    assert len({c["id"] for c in chapters}) == 52
    parts = data["parts"]
    assert [n for p in parts for n in range(p["start"], p["end"] + 1)] == list(
        range(1, 53)
    )
    inventory = json.loads(
        (ROOT / "research/integration/package-inventory.json").read_text()
    )
    packages = {x["package"] for x in inventory["chapters"]}
    for c in chapters:
        n = c["number"]
        assert c["id"] == f"EVOD-{n:02d}" and c["purpose"]
        assert len(set(c["prerequisites"])) == len(c["prerequisites"])
        assert all(type(d) is int and 1 <= d < n for d in c["prerequisites"])
        part = next(p for p in parts if p["number"] == c["part"])
        assert part["start"] <= n <= part["end"]
        assert c["independent_acceptance"] is False
        assert c["frozen_acceptance_record"] == (n <= 2)
        if n <= data["authored_through"]:
            text = (ROOT / c["source"]).read_text()
            assert re.search(r"\\chapter\{([^}]+)\}", text)[1] == c["title"]
            assert c["authoring_stage"] == "authored_in_continuous_candidate"
        else:
            assert c["source"] is None and c["local_review_stage"] == "not_rerun"
            assert c["authoring_stage"] == "staged_package_not_integrated"
        if n >= 22:
            assert c["package"] in packages
    return data


if __name__ == "__main__":
    value = check()
    print(
        f"52 chapters, {len(value['parts'])} parts; authored through {value['authored_through']}; dependencies acyclic"
    )
