"""Canonical deep Chapter 1: exact semantics, assets, and publication checks."""
from copy import deepcopy
from fractions import Fraction
from itertools import product, permutations
import importlib.util
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import pytest
ROOT=Path(__file__).resolve().parents[1]
DNA=ROOT.name=="dna-computing-book"
PREFIX="DNAD-01" if DNA else "EVOD-01"
NAME="deep-dna-computing" if DNA else "deep-evolutor"
NAME += "-ch01-02"

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

M=module("chapter","examples/deep/ch01.py")
BUILD=module("deep_assets","scripts/build_deep_chapter.py")

def test_generated_artifacts_match_executable_sources():
    for path,content in BUILD.outputs().items():
        assert (ROOT/path).read_text()==content,path
    assert json.loads((ROOT/"artifacts/deep/ch01-results.json").read_text())==M.results()

@pytest.mark.parametrize("number",range(1,11))
def test_original_vectors_and_semantic_text(number):
    name=f"{PREFIX}-F{number}"
    tree=ET.fromstring((ROOT/f"book/figures/deep/{name}.svg").read_text())
    ns={"s":"http://www.w3.org/2000/svg"}
    assert tree.attrib["aria-labelledby"]=="title desc"
    assert name in tree.find("s:title",ns).text
    assert tree.find("s:desc",ns).text
    assert tree.findall(".//s:text",ns) and not tree.findall(".//s:image",ns)
    text=(ROOT/f"book/diagrams/deep/{name}.txt").read_text()
    assert all(k in text for k in ("PURPOSE:","→","LIMIT:","EVIDENCE:"))
    assert not any(c in text for c in ("┌","└","│","─"))

def test_storyboard_and_frames_have_specific_states():
    story=json.loads((ROOT/"pedagogy/deep-ch01-storyboard.json").read_text())
    bad=deepcopy(story["figures"][0]);bad["kind"]="unknown"
    with pytest.raises(ValueError):BUILD.figure(bad,M)
    frames=json.loads((ROOT/f"animation/{PREFIX.lower()}/frames.json").read_text())
    assert len(frames)==(9 if DNA else 7)
    assert len({f["change"] for f in frames})==len(frames)
    for f in frames:
        assert f["before"] and f["unchanged"] and f["creationConsumption"]
        assert (ROOT/f"animation/{PREFIX.lower()}"/f["source"]).exists()
    if DNA:assert "106" in frames[4]["change"] and "ABCDEF" in frames[-1]["change"]
    else:assert "5/3" in frames[4]["change"] and "No G→G′ update" in frames[-1]["change"]

def test_chapter_citations_figures_labels_and_exercises_are_closed():
    body=(ROOT/"tex/deep/ch01.tex").read_text()
    glossary=(ROOT/"tex/deep/glossary.tex").read_text()
    bib=(ROOT/"tex/deep/references.tex").read_text()
    cited={k for g in re.findall(r"\\cite\{([^}]+)\}",body) for k in g.split(",")}
    assert cited==set(re.findall(r"\\bibitem\{([^}]+)\}",bib))
    assert len(cited)>=10
    labels=set(re.findall(r"\\label\{([^}]+)\}",body))
    labels.update(re.findall(r"\}\{(fig:[^}]+)\}",body))
    assert set(re.findall(r"\\ref\{([^}]+)\}",body+glossary))<=labels
    assert len(re.findall(r"\\DeepFigure\{",body))==10
    assert len(re.findall(r"\\section\{",body))==(13 if DNA else 12)
    assert len(re.findall(r"\\item ",body))==20
    assert "\\input{deep/ch01-code}" in body
    excerpts=(ROOT/"tex/deep/ch01-code.tex").read_text()
    assert "\\VerbatimInput" in excerpts and "../examples/deep/ch01.py" in excerpts
    assert (ROOT/"tex/deep/ch02.tex").exists()
    assert not (ROOT/"tex/deep/ch03.tex").exists()

def test_deep_pdf_build_and_text_contract():
    subprocess.run(["make","pdf","PYTHON="+sys.executable],cwd=ROOT,check=True,capture_output=True)
    pdf=ROOT/f"output/pdf/{NAME}.pdf"
    assert pdf.read_bytes().startswith(b"%PDF-")
    text=subprocess.check_output(["pdftotext",str(pdf),"-"],text=True)
    for phrase in ("Chapter 1 glossary","Bibliography","Index"):
        assert phrase in text
    assert "??" not in text
    assert all(f"Figure 1.{i}:" in text for i in range(1,11))
    log=(ROOT/f"build/{NAME}.log").read_text()
    assert not re.search(r"Overfull|Underfull|undefined references|undefined citations|Missing character",log)

if DNA:
    @pytest.mark.parametrize("route,valid",[
        ("ABCDEF",True),("ACBDEF",True),("ABCBDF",False),("ABDEF",False),
        ("ABECDF",False),("",False),("FABCDE",False),("ABCDEZ",False)])
    def test_hamiltonian_conditions(route,valid):
        assert M.is_hamiltonian(tuple(route)) is valid

    def test_stage_counts_and_independent_permutation_oracle():
        stages=M.filter_pool(M.walks())
        assert [len(p) for _,p in stages]==[106,14,4,2,2]
        assert set(stages[-1][1])==set(M.permutation_oracle())=={tuple("ABCDEF"),tuple("ACBDEF")}
        assert all(M.edge_valid(p) for p in stages[0][1])

    def test_fault_injection_preserves_multiplicity_until_verification():
        stages=M.filter_pool(M.walks()+[tuple("ABECDF")]*10)
        assert [len(p) for _,p in stages]==[116,24,14,12,2]
        assert len(M.filter_pool([tuple("ABCDEF")]*3)[-1][1])==3

    def test_small_graphs_differential_oracle():
        vertices=tuple("ABC")
        possible=[e for e in product(vertices,repeat=2) if e[0]!=e[1]]
        for flags in product((False,True),repeat=len(possible)):
            edges=frozenset(e for e,keep in zip(possible,flags) if keep)
            actual=set(M.filter_pool(M.walks(3,vertices,edges),vertices,edges,"A","C")[-1][1])
            expected=set(M.permutation_oracle(vertices,edges,"A","C"))
            assert actual==expected

    @pytest.mark.parametrize("bound",[0,-1,1.5,True,None])
    def test_walk_bound_rejected(bound):
        with pytest.raises(ValueError):M.walks(bound)

    @pytest.mark.parametrize("p,delta",[(1/24,.01),(1/12,.01),(.2,.1),(.001,.05),(.5,.2)])
    def test_sampling_threshold_minimality(p,delta):
        n=M.required_samples(p,delta)
        assert (1-p)**n<=delta
        assert (1-p)**(n-1)>delta

    @pytest.mark.parametrize("p,delta",[(0,.1),(-.1,.1),(1.1,.1),(.5,0),(.5,1),(float("nan"),.1)])
    def test_invalid_sampling_domains(p,delta):
        with pytest.raises(ValueError):M.required_samples(p,delta)

    def test_boundary_values_and_reverse_complement():
        assert M.required_samples(1,.1)==1
        assert M.required_samples(1/24,.01)==109
        assert M.required_samples(1/12,.01)==53
        assert M.reverse_complement("ACGA")=="TCGT"
        for letters in product("ACGT",repeat=4):
            s="".join(letters)
            assert M.reverse_complement(M.reverse_complement(s))==s
        with pytest.raises(ValueError):M.reverse_complement("AN")
else:
    @pytest.mark.parametrize("context",["bounded","balanced"])
    def test_exact_baseline_equivalence_and_invariants(context):
        for xs in product([Fraction(-2),Fraction(-1,2),Fraction(0),Fraction(3,2)],repeat=3):
            out,trace=M.execute(M.select(context),xs)
            assert out==M.direct_baseline(context,xs)
            assert len(out)==len(xs) and len(trace)==2
            assert trace[0]["before"]==xs and trace[-1]["after"]==out
            if context=="bounded":
                assert all(x>=0 for x in out) and all(a<=b for a,b in zip(out,out[1:]))
            else:assert out[-1]==0

    def test_expected_traces_and_plan_order():
        assert M.execute(M.select("bounded"),(3,-1,2))[0]==(3,3,5)
        assert M.execute(M.select("balanced"),(3,-1,2))[0]==(Fraction(5,3),Fraction(-2,3),0)
        assert M.execute(("prefix","clip"),(3,-1,2))[0]==(3,2,4)
        assert M.execute((),(1,2))[0]==(1,2)
        with pytest.raises(TypeError):M.CATALOG["other"]=M.prefix

    @pytest.mark.parametrize("bad",[0,-1,1.5,True,None])
    def test_development_domain(bad):
        with pytest.raises(ValueError):M.develop(bad)

    def test_development_has_no_learning_and_exact_composition():
        assert M.develop(2)==("prefix","prefix")
        assert M.execute(M.develop(2),(3,-1,2))[0]==(3,5,9)
        assert M.execute(M.develop(3),(3,-1,2))[0]==(3,8,17)

    @pytest.mark.parametrize("context",["","other",None])
    def test_unknown_context_rejected(context):
        with pytest.raises(ValueError):M.select(context)
        with pytest.raises(ValueError):M.direct_baseline(context,(1,))

    def test_empty_data_and_unknown_modules_rejected():
        with pytest.raises(ValueError):M.execute(("center",),())
        with pytest.raises(ValueError):M.execute(("missing",),(1,))
        with pytest.raises(ValueError):M.center(())
        with pytest.raises(ValueError):M.direct_baseline("bounded",())

    @pytest.mark.parametrize("index",range(7))
    def test_memory_dimension_domain(index):
        dims=[1,24,4096,8,64,2048,2];dims[index]=0
        with pytest.raises(ValueError):M.memory_bytes(*dims)

    def test_memory_exact_units_and_scaling():
        a=M.memory_bytes(1,24,4096,8,64,2048,2)
        assert a=={"kv":192*1024**2,"fixed_state":96*1024}
        b=M.memory_bytes(1,24,8192,8,64,2048,2)
        c=M.memory_bytes(2,24,8192,8,64,2048,2)
        assert b["kv"]==2*a["kv"] and b["fixed_state"]==a["fixed_state"]
        assert c=={k:2*v for k,v in b.items()}
