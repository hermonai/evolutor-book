"""Build the LaTeX-first Chapters 1--3 candidate, preserving accepted releases."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
NAME = "dna-computing" if ROOT.name == "dna-computing-book" else "evolutor"

def main():
    build = ROOT/"build/textbook"
    figures = ROOT/"build/deep-figures"
    build.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PATH="/Library/TeX/texbin:"+os.environ["PATH"])
    for source in sorted((ROOT/"book/figures/deep").glob("*.svg")) + sorted((ROOT/"drafts/ch03/figures").glob("*.svg")):
        subprocess.run(["rsvg-convert","-f","pdf","-o",str(figures/(source.stem+".pdf")),str(source)], check=True)
    main = NAME+"-textbook"
    result = subprocess.run(["latexmk","-xelatex","-interaction=nonstopmode","-halt-on-error",
                             "-outdir=../build/textbook", main+".tex"],
                            cwd=ROOT/"tex",env=env,capture_output=True,text=True)
    (build/"console.log").write_text(result.stdout+result.stderr)
    if result.returncode:
        raise SystemExit((result.stdout+result.stderr)[-6000:])
    log = (build/(main+".log")).read_text()
    failures = [line for line in log.splitlines() if any(s in line for s in
        ("Overfull", "Missing character:", "undefined references", "multiply defined",
         "LaTeX Warning: Reference"))]
    if failures:
        raise SystemExit("\n".join(failures))
    output = ROOT/"output/pdf"/(main+".pdf")
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(build/(main+".pdf"), output)
    paths = [ROOT/"tex"/(main+".tex"), ROOT/"scripts/build-textbook.py"]
    paths += sorted((ROOT/"tex/textbook").rglob("*.tex"))
    paths += sorted((ROOT/"tex/deep").glob("*.tex"))
    paths += sorted((ROOT/"book/figures/deep").glob("*.svg"))
    paths += sorted((ROOT/"drafts/ch03/figures").glob("*.svg"))
    record = {"edition":"Chapters 1--3 LaTeX-first review candidate; not cumulative acceptance",
              "pdf":str(output.relative_to(ROOT)),
              "sha256":hashlib.sha256(output.read_bytes()).hexdigest(),
              "sources":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    (build/"build-record.json").write_text(json.dumps(record,indent=2)+"\n")
    print(output)

if __name__ == "__main__":
    main()
