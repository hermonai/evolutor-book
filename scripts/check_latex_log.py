"""Fail publication QA on errors, missing glyphs and unresolved layout/references."""
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
patterns = [r"^! ", r"Missing character:", r"Overfull \\[hv]box",
            r"(?:Citation|Reference).*undefined", r"There were undefined",
            r"Label\(s\) may have changed", r"multiply defined"]
failures = [line for line in text.splitlines() if any(re.search(p, line) for p in patterns)]
if failures:
    raise SystemExit("\n".join(failures))
print("LaTeX log: no errors, missing glyphs, undefined references or overfull boxes.")
