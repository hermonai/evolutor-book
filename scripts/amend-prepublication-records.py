"""Rebind chapter review records after a reviewed prepublication edit.

The superseded record is copied unchanged beside the new one. The new record
binds the current source and PDF bytes and states exactly which pages were
re-inspected; raster-identical pages keep their earlier local inspection.
It never sets accepted or independent-review fields. Run after rebuilding
each standalone chapter PDF (drafts/chNN/build.py).
"""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources(number, previous):
    """Rehash the superseded record's exact path set plus current chapter files.

    Records also bind declared dependencies (another chapter's reference or
    the chapter's test file); keeping the previous path set preserves them.
    """
    directory = ROOT / f"drafts/ch{number:02d}"
    paths = set(previous) | {
        str(p.relative_to(ROOT))
        for p in directory.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    return {path: sha(ROOT / path) for path in sorted(paths) if (ROOT / path).is_file()}


def pages(pdf):
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    return int(next(l for l in info.splitlines() if l.startswith("Pages:")).split()[1])


def amend(entry, meta, suffix):
    n = entry["chapter"]
    pdf = ROOT / f"output/pdf/evolutor-ch{n:02d}-review.pdf"
    revision = {
        "date": meta["date"],
        "reviewer": meta["reviewer"],
        "change": entry["change"],
        "changed_pages_reinspected": entry["changed_pages"],
        "inspection": meta["inspection"],
        "unchanged_page_policy": "Raster-identical pages retain the prior local inspection; no new independent review is claimed.",
        "amendment_log": "docs/prepublication/chapter-amendments.json",
    }
    if 4 <= n <= 21:
        path = ROOT / f"artifacts/deep/ch{n:02d}-review.json"
        keep = path.with_name(f"ch{n:02d}-review-superseded-{suffix}.json")
        if not keep.exists():
            shutil.copyfile(path, keep)
        record = json.loads(path.read_text())
        previous = json.loads(keep.read_text())["sources"]
        record.update(sha256=sha(pdf), pages=pages(pdf), sources=sources(n, previous))
        record["prepublicationRevision"] = revision
    else:
        path = ROOT / f"research/integration/ch{n:02d}/local-review.json"
        keep = path.with_name(f"pre-prepublication-local-review-{suffix}.json")
        if not keep.exists():
            shutil.copyfile(path, keep)
        record = json.loads(path.read_text())
        previous = json.loads(keep.read_text())["source_hashes"]
        build = json.loads((ROOT / f"build/ch{n:02d}/build-record.json").read_text())
        if build["sha256"] != sha(pdf):
            raise SystemExit(f"Chapter {n}: build record does not match PDF")
        record.update(pdf_sha256=sha(pdf), pages=pages(pdf), source_hashes=sources(n, previous))
        record["prepublication_revision"] = revision
    if record.get("accepted") or record.get("independent_review"):
        raise SystemExit(f"Chapter {n}: refusing to amend an accepted record")
    path.write_text(json.dumps(record, indent=1) + "\n")
    print(f"chapter {n}: {path.relative_to(ROOT)} (superseded copy {keep.name})")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", default="docs/prepublication/chapter-amendments.json")
    parser.add_argument("--suffix", default="2026-10-19")
    args = parser.parse_args()
    meta = json.loads((ROOT / args.log).read_text())
    for entry in meta["chapters"]:
        amend(entry, meta, args.suffix)


if __name__ == "__main__":
    main()
