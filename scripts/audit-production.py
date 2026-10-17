"""Read-only admission checks; never execute a chapter or promote its status.

File presence is not completion. This checks declared evidence against bytes,
not scientific validity, visual quality or completeness of package reuse.
Run after an author's handoff, then perform the manual checks in the report.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
MANUAL_CHECKS = [
    "Read every package-adoption mapping against the incoming section inventory.",
    "Review derivations, sources, native-interface dependencies and negative controls.",
    "Reproduce numerical fixtures and tests after the batch returns ownership.",
    "Inspect rendered pages and the declared color/grayscale review scope.",
    "Resolve cross-batch dependencies before cumulative assembly and regression.",
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


class Evidence:
    """Read only repository-confined files and detect concurrent source edits."""

    def __init__(self, root):
        self.root = Path(root).resolve()
        self.seen = {}
        self.errors = []

    def path(self, relative):
        if not isinstance(relative, str) or not relative:
            raise ValueError("invalid evidence path")
        p = Path(relative)
        if p.is_absolute() or ".." in p.parts:
            raise ValueError(f"non-relative evidence path: {relative}")
        result = (self.root / p).resolve()
        if not result.is_relative_to(self.root):
            raise ValueError(f"evidence escapes checkout: {relative}")
        return result

    def read(self, relative):
        try:
            data = self.path(relative).read_bytes()
            current = digest(data)
            if relative in self.seen and self.seen[relative] != current:
                self.errors.append(f"changed during audit: {relative}")
            self.seen[relative] = current
            return data
        except (OSError, ValueError) as error:
            self.errors.append(f"{relative}: {error}")
            return None

    def document(self, relative):
        data = self.read(relative)
        if data is None:
            return {}
        try:
            value = json.loads(data)
            if not isinstance(value, dict):
                raise ValueError("expected JSON object")
            return value
        except (ValueError, UnicodeError) as error:
            self.errors.append(f"{relative}: {error}")
            return {}

    def hashes(self, mapping, label, required=()):
        if not isinstance(mapping, dict) or not mapping:
            self.errors.append(f"{label}: missing nonempty source-hash mapping")
            return
        for relative in required:
            if relative not in mapping:
                self.errors.append(f"{label}: uncovered source {relative}")
        for relative, expected in mapping.items():
            if not isinstance(expected, str) or not SHA256.fullmatch(expected):
                self.errors.append(f"{label}: malformed digest for {relative}")
                continue
            data = self.read(relative)
            if data is not None and digest(data) != expected:
                self.errors.append(f"{label}: digest mismatch for {relative}")

    def finish(self):
        for relative, expected in self.seen.items():
            try:
                if digest(self.path(relative).read_bytes()) != expected:
                    self.errors.append(f"changed during audit: {relative}")
            except (OSError, ValueError):
                self.errors.append(f"removed or redirected during audit: {relative}")
        return sorted(set(self.errors))


def chapter_audit(root, chapter, package, batch):
    evidence = Evidence(root)
    draft = f"drafts/ch{chapter:02d}"
    research = f"research/integration/ch{chapter:02d}"
    test = f"tests/test_ch{chapter:02d}_reference.py"
    required = [
        f"{draft}/{name}"
        for name in (
            "manuscript.tex",
            "reference.py",
            "results.json",
            "build.py",
            "review.tex",
            "sources.tex",
            "README.md",
            "STORYBOARD.md",
        )
    ] + [test]
    for relative in required + [
        f"{research}/package-adoption.md",
        f"{research}/technical-audit.md",
    ]:
        data = evidence.read(relative)
        if data is not None and not data.strip():
            evidence.errors.append(f"empty required file: {relative}")

    # Include every chapter source, not just the small set of mandatory names.
    # Ignore interpreter caches; do not follow paths outside the checkout.
    directory = Path(root) / draft
    source_files = sorted(
        str(p.relative_to(root))
        for p in directory.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    )
    figure_sources = [
        p for p in source_files if "/figures/" in p and p.endswith(".tex")
    ]
    if not figure_sources:
        evidence.errors.append("missing editable native vector figure sources")
    for relative in figure_sources:
        companion = str(Path(relative).with_suffix(".txt"))
        if companion not in source_files:
            evidence.errors.append(f"missing semantic TXT companion: {companion}")
        for figure_file in (relative, companion):
            data = evidence.read(figure_file)
            if data is not None and not data.strip():
                evidence.errors.append(
                    f"empty figure source/description: {figure_file}"
                )
    required = sorted(set(required + source_files))

    provenance = evidence.document(f"{research}/source-verification.json")
    if provenance.get("chapter") != chapter:
        evidence.errors.append("source verification has wrong/missing chapter identity")
    package_hash = package.get("sha256") if package else None
    if (
        not isinstance(package_hash, str)
        or not SHA256.fullmatch(package_hash)
        or provenance.get("package_sha256") != package_hash
    ):
        evidence.errors.append(
            "source verification does not match audited package digest"
        )
    if provenance.get("inherited_validation_claims_adopted") is not False:
        evidence.errors.append(
            "inherited package validation claims not explicitly excluded"
        )

    build = evidence.document(f"build/ch{chapter:02d}/build-record.json")
    pdf = f"output/pdf/evolutor-ch{chapter:02d}-review.pdf"
    if build.get("pdf") != pdf:
        evidence.errors.append("build record has wrong/missing PDF path")
    pages = build.get("pages")
    if type(pages) is not int or pages <= 0:
        evidence.errors.append("build record has invalid page count")
    expected_pdf = build.get("sha256")
    evidence.hashes({pdf: expected_pdf}, "PDF")
    evidence.hashes(build.get("sources"), "build", required)

    review = evidence.document(f"{research}/local-review.json")
    if review.get("chapter") != chapter or review.get("pdf") != pdf:
        evidence.errors.append("local review has wrong/missing chapter or PDF identity")
    if review.get("pdf_sha256") != expected_pdf or review.get("pages") != pages:
        evidence.errors.append(
            "local review does not match built PDF digest/page count"
        )
    evidence.hashes(review.get("source_hashes"), "review", required)
    dependencies = review.get("transitive_dependencies", {})
    if dependencies:
        evidence.hashes(dependencies, "declared dependency")
    if (
        review.get("accepted") is not False
        or review.get("independent_review") is not False
    ):
        evidence.errors.append(
            "local review must not imply publication/independent acceptance"
        )
    tests = review.get("tests", {})
    if (
        not isinstance(tests, dict)
        or type(tests.get("chapter_passed")) is not int
        or tests["chapter_passed"] <= 0
    ):
        evidence.errors.append("missing positive chapter-specific test declaration")
    visual = review.get("visual_review", {})
    if (
        not isinstance(visual, dict)
        or visual.get("status") not in ("PASS", "PASS WITH NOTES")
        or not visual.get("mode")
    ):
        evidence.errors.append("missing local visual-review pass and explicit scope")
    if batch is None:
        evidence.errors.append("chapter has no dispatched batch owner")
    else:
        handoff = evidence.read(batch.get("handoff"))
        if handoff is not None and not handoff.strip():
            evidence.errors.append("empty batch handoff")

    final_source_files = sorted(
        str(p.relative_to(root))
        for p in directory.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    )
    if final_source_files != source_files:
        evidence.errors.append("chapter source inventory changed during audit")
    blockers = evidence.finish()
    return {
        "chapter": chapter,
        "batch": batch.get("id") if batch else None,
        "present_source_files": len(source_files),
        "native_figure_sources": len(figure_sources),
        "mechanically_ready_for_coordinator_review": not blockers,
        "blockers": blockers,
        "manual_checks_pending": list(MANUAL_CHECKS),
        "integrated": False,
        "independently_reviewed": False,
        "accepted": False,
    }


def audit(root=ROOT, start=36, end=52):
    if not (36 <= start <= end <= 52):
        raise ValueError("production audit is scoped to Chapters 36–52")
    root = Path(root).resolve()
    metadata = Evidence(root)
    dispatch = metadata.document("research/integration/production-batches.json")
    packages = metadata.document("research/integration/package-reuse-audit.json")
    # Reject malformed routing metadata rather than silently assigning an owner.
    batches = dispatch.get("batches", [])
    entries = packages.get("chapters", [])
    if not isinstance(batches, list) or not all(isinstance(b, dict) for b in batches):
        raise ValueError("invalid production batch list")
    if not isinstance(entries, list) or not all(isinstance(p, dict) for p in entries):
        raise ValueError("invalid package audit list")
    chapters = []
    for n in range(start, end + 1):
        owners = [
            b
            for b in batches
            if type(b.get("start")) is int
            and type(b.get("end")) is int
            and b["start"] <= n <= b["end"]
        ]
        matches = [p for p in entries if p.get("chapter") == n]
        result = chapter_audit(
            root,
            n,
            matches[0] if len(matches) == 1 else None,
            owners[0] if len(owners) == 1 else None,
        )
        chapters.append(result)
    metadata_errors = metadata.finish()
    if metadata_errors:
        for result in chapters:
            result["blockers"].extend(metadata_errors)
            result["mechanically_ready_for_coordinator_review"] = False
    return {
        "schema": "evolutor-production-admission-v1",
        "scope": f"Chapters {start}–{end}; local evidence declarations only",
        "policy": "Read-only. Does not run code, certify science or visuals, or promote chapter stages.",
        "mechanically_ready_chapters": [
            r["chapter"]
            for r in chapters
            if r["mechanically_ready_for_coordinator_review"]
        ],
        "chapters": chapters,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--start", type=int, default=36)
    parser.add_argument("--end", type=int, default=52)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="Exit nonzero if any requested chapter is not mechanically ready",
    )
    args = parser.parse_args()
    report = audit(args.root, args.start, args.end)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(report["scope"])
        for item in report["chapters"]:
            state = (
                "ready for manual review"
                if item["mechanically_ready_for_coordinator_review"]
                else f"pending ({len(item['blockers'])} checks)"
            )
            print(
                f"  {item['chapter']:02d}: {state}; {item['present_source_files']} source files, {item['native_figure_sources']} vector figures"
            )
        print(report["policy"])
    if (
        args.require_ready
        and len(report["mechanically_ready_chapters"]) != args.end - args.start + 1
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
