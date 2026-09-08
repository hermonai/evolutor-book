"""Accept only reviewed edition-specific source; preserve the historical gate."""
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def reviewed_source_paths(root, book):
    """Closed cumulative release surface, including generators and reused helper."""
    required={book["main"],"book/book.json","scripts/build_deep_chapter.py",
              "scripts/build_deep_chapter02.py","scripts/require_active_manuscript.py",
              "research/deep-ch01-sources.md","research/deep-ch02-sources.md",
              "artifacts/deep/ch01-review.json"}
    prior=json.loads((root/"artifacts/deep/ch01-review.json").read_text())
    required.update(prior["reviewedSources"])
    required.update({"Makefile","scripts/review_deep.py","scripts/build_deep_plan.py",
                     "pedagogy/deep-book-i-contract.json","pedagogy/deep-curriculum.json",
                     "pedagogy/deep-figure-inventory.json","pedagogy/deep-animation-inventory.json"})
    for pattern in ("tex/deep/*","book/figures/deep/*.svg","book/diagrams/deep/*.txt",
                    "animation/*/*.svg","animation/*/frames.json","examples/deep/*.py",
                    "pedagogy/deep-ch0*-storyboard.json","artifacts/deep/ch0*-results.json"):
        required.update(str(p.relative_to(root)) for p in root.glob(pattern) if p.is_file())
    if book["title"]=="Evolutor":
        required.update({"code/evo_torch/evo_torch/causality.py","research/EVO-EXP01-ch02-spec.json"})
    return required

def validate_two_chapters(book, root):
    import re
    chapters=book.get("chapters",[])
    slug="dna-computing" if book.get("title")=="DNA Computing" else "evolutor"
    expected_main=f"tex/deep-{slug}-ch01-02.tex"
    if (book.get("edition")!="4-deep" or book.get("status")!="chapter-two-production"
            or len(chapters)!=2 or book.get("main")!=expected_main):
        raise ValueError("no accepted deep manuscript: cumulative reviewed Chapters 1–2 required")
    for i,c in enumerate(chapters,1):
        if (c.get("number")!=i or c.get("source")!=f"tex/deep/ch{i:02}.tex"
                or c.get("status")!="internally-reviewed-draft"):
            raise ValueError("Unexpected or unreviewed active chapter")
    if not (root/expected_main).is_file():
        raise ValueError("Missing cumulative entry point")
    main=(root/expected_main).read_text()
    if re.findall(r"\\input\{deep/(ch\d+)\}",main)!=["ch01","ch02"]:
        raise ValueError("Entry point must include exactly Chapters 1 then 2")
    if "undergraduate/" in main or "chapters/manifest" in main:
        raise ValueError("Preserved edition cannot enter active deep build")
    # Preserve the original Chapter 1 review, including its exact historical inputs.
    for filename in ("artifacts/deep/ch01-review.json","artifacts/deep/ch02-review.json"):
        if not (root/filename).is_file():raise ValueError("Missing review: "+filename)
        review=json.loads((root/filename).read_text())
        if review.get("status")!="author-agent-reviewed" or not all(
                review.get(k) for k in ("scientific","mathematical","clarity","citations","everyPageInspected")):
            raise ValueError("Incomplete author-agent review")
        manifest=review.get("reviewedSources")
        if not isinstance(manifest,dict) or not manifest:
            raise ValueError("Missing reviewed source manifest")
        for path,digest in manifest.items():
            if not (root/path).is_file() or hashlib.sha256((root/path).read_bytes()).hexdigest()!=digest:
                raise ValueError("Source changed after review: "+path)
    if not reviewed_source_paths(root,book)<=set(manifest):
        raise ValueError("Review does not cover cumulative release surface")
    n=review.get("pdfPages",0)
    if n<21 or review.get("inspectedPhysicalPages")!=list(range(1,n+1)):
        raise ValueError("Every cumulative PDF page must be inspected")
    return True


def validate_book(book, root=ROOT):
    if book.get("status")=="chapter-two-production":
        return validate_two_chapters(book,root)
    if book.get("edition") == "4-deep":
        if book.get("status") != "chapter-one-production" or len(book.get("chapters",[])) != 1:
            raise ValueError("no accepted deep manuscript: exactly one reviewed Chapter 1 required")
        chapter=book["chapters"][0]
        dna=book.get("title")=="DNA Computing"
        expected_main="tex/deep-dna-computing.tex" if dna else "tex/deep-evolutor.tex"
        if (chapter.get("source")!="tex/deep/ch01.tex"
                or chapter.get("status")!="internally-reviewed-draft"
                or chapter.get("number")!=1 or book.get("main")!=expected_main):
            raise ValueError("Preserved, later or unreviewed source cannot be the active deep chapter")
        for name in (chapter["source"],book["main"],"artifacts/deep/ch01-review.json"):
            if not (root/name).is_file():
                raise ValueError("Missing deep source or review: "+name)
        main=(root/book["main"]).read_text()
        if r"\input{deep/ch01}" not in main or "undergraduate/" in main or "chapters/manifest" in main:
            raise ValueError("Deep entry point must include only the new deep chapter")
        review=json.loads((root/"artifacts/deep/ch01-review.json").read_text())
        if review.get("status")!="author-agent-reviewed" or not all(
                review.get(k) for k in ("scientific","mathematical","clarity","citations","everyPageInspected")):
            raise ValueError("Incomplete author-agent review")
        if not isinstance(review.get("reviewedSources"),dict):
            raise ValueError("Missing reviewed source manifest")
        for path,digest in review["reviewedSources"].items():
            if not (root/path).is_file() or hashlib.sha256((root/path).read_bytes()).hexdigest()!=digest:
                raise ValueError("Source changed after review: "+path)
        required={chapter["source"],book["main"],"tex/deep/preamble.tex",
                  "tex/deep/references.tex","tex/deep/glossary.tex","examples/deep/ch01.py"}
        for pattern in ("tex/deep/*.tex","book/figures/deep/*.svg","book/diagrams/deep/*.txt",
                        "animation/*/*.svg","animation/*/frames.json"):
            required.update(str(p.relative_to(root)) for p in root.glob(pattern))
        required.update({"pedagogy/deep-ch01-storyboard.json","scripts/build_deep_chapter.py",
                         "artifacts/deep/ch01-results.json","research/deep-ch01-sources.md"})
        if not required<=set(review["reviewedSources"]):
            raise ValueError("Review does not cover manuscript, apparatus and executable source")
        return True
    if book.get("status") != "chapter-one-production" or len(book.get("chapters", [])) != 1:
        raise ValueError("No accepted undergraduate manuscript chapters: this phase requires only the new Chapter 1.")
    chapter = book["chapters"][0]
    if chapter.get("source") != "tex/undergraduate/ch01.tex" or chapter.get("status") != "internally-reviewed-draft":
        raise ValueError("Preserved or unreviewed source cannot be the active undergraduate chapter.")
    if book.get("main") not in {"tex/undergraduate-dna-computing.tex", "tex/undergraduate-evolutor.tex"}:
        raise ValueError("Undergraduate main must be a new edition entry point.")
    for name in (chapter["source"],book["main"]):
        if not (root/name).is_file():
            raise ValueError("Missing manuscript source: "+name)
    return True

if __name__ == "__main__":
    try:
        validate_book(json.loads((ROOT/"book/book.json").read_text()))
    except ValueError as exc:
        raise SystemExit(str(exc))
