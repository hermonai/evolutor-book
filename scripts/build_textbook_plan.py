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
    # Only this current overlay advances. The accepted generator and all other
    # accepted outputs remain untouched; the authored current template is
    # mirrored to the root so the preservation checks still detect drift.
    template=(ROOT/"docs/roadmap-current.md").read_text()
    result["ROADMAP.md"]=re.sub(r"\]\(\.\./", "](", template)
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
            if (ROOT/name).read_text()!=text:
                stale.append(name)
        elif name=="ROADMAP.md":
            (ROOT/name).write_text(text)
        elif (ROOT/name).read_text()!=text:
            raise SystemExit("Refusing to rewrite accepted planning inputs: "+name)
    if stale:
        raise SystemExit("Stale current planning view: "+", ".join(stale))
    print("Current planning view agrees; frozen accepted generator is unchanged.")

if __name__=="__main__":
    main()
