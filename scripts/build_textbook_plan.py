"""Current planning view layered on the immutable Chapters 1--2 generator."""
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("accepted_deep_plan",ROOT/"scripts/build_deep_plan.py")
legacy=importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
validate=legacy.validate

def outputs(data,contract,outline):
    result=legacy.outputs(data,contract,outline)
    state=json.loads((ROOT/"book/textbook-progress.json").read_text())
    if state["accepted"] != [1,2] or state["review"] != [3] or state["format"] != "latex":
        raise ValueError("Progress must preserve accepted Chapters 1--2 and Chapter 3 review status")
    text=result["ROADMAP.md"]
    note=("Status: canonical deep Chapters 1–2 remain internally reviewed development manuscripts. "
          "Chapter 3 now has an authored LaTeX review manuscript in the combined textbook candidate; "
          "cumulative acceptance and independent review remain open. Chapter 4 onward remains planned. "
          "Prior editions and their accepted source hashes are preserved. "
          "See [the textbook revision](TEXTBOOK_REVISION.md).\n")
    text=re.sub(r"^Status:.*\n",lambda _:note,text,flags=re.M)
    text=re.sub(r"^1\. \*\*Current milestone:\*\*.*\n",
                "1. **Current milestone:** LaTeX-first Chapters 1–3 review candidate, native/vector mechanisms, worked solutions and reproducible source checks.\n",text,flags=re.M)
    next_title=data["chapters"][3]["title"]
    next_line=("2. **Next execution:** close Chapter 3 specialist review and cumulative acceptance gates, then Chapter 4 — "
               +next_title+". Keep authored LaTeX as the new manuscript source.\n")
    text=re.sub(r"^2\. \*\*Next execution:\*\*.*\n",lambda _:next_line,text,flags=re.M)
    result["ROADMAP.md"]=text
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    data,contract,outline=(json.loads((ROOT/p).read_text()) for p in
        ("pedagogy/deep-curriculum.json","pedagogy/deep-book-i-contract.json","pedagogy/deep-ch01-outline.json"))
    generated=outputs(data,contract,outline)
    stale=[]
    for name,text in generated.items():
        if args.check:
            if (ROOT/name).read_text()!=text: stale.append(name)
        elif name=="ROADMAP.md":
            (ROOT/name).write_text(text)
        elif (ROOT/name).read_text()!=text:
            raise SystemExit("Refusing to rewrite accepted planning inputs: "+name)
    if stale: raise SystemExit("Stale current planning view: "+", ".join(stale))
    print("Current planning view agrees; frozen accepted generator is unchanged.")

if __name__=="__main__":
    main()
