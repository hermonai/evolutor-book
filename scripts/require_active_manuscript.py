"""Accept only reviewed edition-specific source; preserve the historical gate."""
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_book(book, root=ROOT):
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
