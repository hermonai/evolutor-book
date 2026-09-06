"""Reject empty or preserved-edition manifests before building the undergraduate PDF."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_book(book, root=ROOT):
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
