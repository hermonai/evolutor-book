"""Check the new source-first candidate without changing accepted review records."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DNA = ROOT.name == "dna-computing-book"

def main():
    name = "dna-computing" if DNA else "evolutor"
    main = (ROOT/"tex"/(name+"-textbook.tex")).read_text()
    chapter = (ROOT/"tex/textbook/ch03.tex").read_text()
    assert r"\input{deep/ch01}" in main and r"\input{deep/ch02}" in main
    assert r"\input{textbook/ch03}" in main
    assert chapter.count(r"\DeepFigure{") == 12
    assert chapter.count(r"\textbf{Solution") >= 12
    assert not re.search(r"\\includegraphics.*\.svg",chapter)
    assert "/Users/" not in chapter and "/tmp/" not in chapter
    builder = (ROOT/"scripts/build-textbook.py").read_text()
    assert '"pandoc"' not in builder and '"manuscript.md"' not in builder
    assert r"\begin{tikzpicture}" in next((ROOT/"tex/textbook/figures").glob("*.tex")).read_text()
    # Bind every previously accepted/standalone-review input, not only its prose.
    checked = 0
    for record_path in sorted((ROOT/"artifacts/deep").glob("ch0*-review.json")):
        record = json.loads(record_path.read_text())
        hashes = record.get("sources", record.get("reviewedSources"))
        assert hashes, record_path
        for rel, digest in hashes.items():
            path = ROOT/rel
            assert path.is_file(), rel
            assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, rel
            checked += 1
        if "pdf" in record and "sha256" in record:
            pdf = ROOT/record["pdf"]
            if pdf.exists():
                assert hashlib.sha256(pdf.read_bytes()).hexdigest() == record["sha256"]
    if DNA:
        path = ROOT/"drafts/ch03/completion_diagnostics.py"
        spec = importlib.util.spec_from_file_location("diagnostic",path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert module.work_depth(4,3) == {"candidates":4,"stages":3,"work":12,"depth":3}
        assert module.work_depth(8,3)["work"] == 24
        for m in (0,1,10,100):
            assert math.isclose(module.coverage(m,.1,.5,.8),1-(1-.04)**m,abs_tol=1e-14)
    else:
        x,w = 2.,3.
        loss = lambda weight: .5*(weight*x)**2
        assert loss(w) == 18
        assert (w*x)*x == 12 and (w*x)*w == 18
        assert math.isclose(loss(w-.01*12),16.5888)
        h = 1e-4
        assert math.isclose((loss(w+h)-loss(w-h))/(2*h),12,abs_tol=1e-9)
    output = ROOT/"build/textbook/checks.json"
    output.parent.mkdir(parents=True,exist_ok=True)
    result = {"edition":"new LaTeX-first review candidate",
              "prior_source_hashes_verified":checked,
              "imported_chapter3_figures":12,"new_native_tikz_figures":1,
              "worked_bridge_calculation":"passed"}
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result))

if __name__ == "__main__":
    main()
