"""Prevent a preserved manuscript from being mistaken for the new edition."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
book = json.loads((ROOT / "book/book.json").read_text())
if book["status"] == "architecture-only-no-manuscript" or not book["chapters"] or not book["main"]:
    raise SystemExit("No accepted undergraduate manuscript chapters. This branch is architecture-only; "
                     "use the preserved astra-rewrite commit to reproduce the earlier PDF.")
