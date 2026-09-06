"""Undergraduate Chapter 1 contracts: exact examples, figure artifacts, references and PDF integration."""
from copy import deepcopy
from pathlib import Path
import importlib.util
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import pytest
ROOT=Path(__file__).resolve().parents[1]
DNA=ROOT.name=="dna-computing-book"

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

@pytest.mark.parametrize("case",range(4))
def test_hand_cases_match_executable_rule(case):
    m=module("intro_rule","examples/undergraduate/ch01_rule.py")
    if DNA:
        n,expected=[(0,2),(3,5),(4,6),(7,9)][case]
        assert m.add_two(n)==expected
    else:
        n,expected=[(18,"on"),(20,"off"),(22,"off"),(19,"on")][case]
        assert m.heater(n)==expected

def test_rule_is_stateless_and_boundary_is_strict():
    m=module("intro_rule","examples/undergraduate/ch01_rule.py")
    if DNA:
        assert [m.add_two(n) for n in (3,4,3)]==[5,6,5]
    else:
        assert [m.heater(n) for n in (19.99,20,20.01,19.99)]==["on","off","off","on"]

def test_generated_figures_and_data_are_fresh():
    m=module("undergraduate","scripts/build_undergraduate.py")
    for name,content in m.outputs().items():
        assert (ROOT/name).read_text()==content,name

@pytest.mark.parametrize("number",range(1,7))
def test_svg_is_editable_self_describing_and_has_txt_companion(number):
    prefix="DNAU-01" if DNA else "EVOU-01"
    name=f"{prefix}-F{number}"
    svg=ROOT/f"book/figures/undergraduate/{name}.svg"
    tree=ET.fromstring(svg.read_text())
    ns={"s":"http://www.w3.org/2000/svg"}
    assert tree.attrib["aria-labelledby"]=="title desc"
    assert name in tree.find("s:title",ns).text
    assert tree.find("s:desc",ns).text
    assert tree.findall(".//s:text",ns)
    assert not tree.findall(".//s:image",ns)
    assert not any("href" in key for node in tree.iter() for key in node.attrib)
    txt=(ROOT/f"book/diagrams/undergraduate/{name}.txt").read_text()
    assert "→" in txt and "LIMIT:" in txt and "EVIDENCE:" in txt

def test_storyboard_rejects_missing_steps_and_unknown_drawing():
    m=module("undergraduate","scripts/build_undergraduate.py")
    p=json.loads((ROOT/"pedagogy/ch01-storyboard.json").read_text())
    broken=deepcopy(p);broken["figures"][0]["steps"]=[]
    with pytest.raises(AssertionError):m.validate(broken)
    broken=deepcopy(p["figures"][0]);broken["kind"]="invented-unrepresented"
    with pytest.raises(ValueError):m.figure(broken,"DNA Computing" if DNA else "Evolutor")

def test_terminology_glossary_and_local_references_are_closed():
    m=module("audit","scripts/audit_undergraduate.py")
    for name,content in m.outputs().items():
        assert (ROOT/name).read_text()==content,name
    body=(ROOT/"tex/undergraduate/ch01.tex").read_text()
    glossary=(ROOT/"tex/undergraduate/glossary.tex").read_text()
    keys=set(re.findall(r"\\newglossaryentry\{([^}]+)\}",glossary))
    assert set(re.findall(r"\\Teach\{([^}]+)\}",body))==keys
    labels=set(re.findall(r"\\label\{([^}]+)\}",body))
    # TeachingFigure's third argument creates its label through the shared macro.
    labels.update(re.findall(r"\}\{(fig:[^}]+)\}",body))
    assert set(re.findall(r"\\ref\{([^}]+)\}",body+glossary)) <= labels
    assert set(re.findall(r"\\glslink\{([^}]+)\}",glossary)) <= keys
    terms=json.loads((ROOT/"pedagogy/ch01-terms.json").read_text())
    assert all(t["firstSentenceOrHeadingPreview"] and t["definitionSentence"] and t["figure"] for t in terms)

def test_printed_code_and_citations_use_real_sources():
    body=(ROOT/"tex/undergraduate/ch01.tex").read_text()
    assert "\\VerbatimInput" in body and "../examples/undergraduate/ch01_rule.py" in body
    assert "\\input{undergraduate/ch01-trace}" in body
    refs=set(re.findall(r"\\bibitem\{([^}]+)\}",(ROOT/"tex/undergraduate/references.tex").read_text()))
    cited={k for group in re.findall(r"\\cite\{([^}]+)\}",body) for k in group.split(",")}
    assert cited <= refs
    assert len(re.findall(r"\\TeachingFigure\{",body))==6
    assert len(re.findall(r"\\item ",body))==16

def test_pdf_build_and_textual_publication_contract():
    subprocess.run(["make","pdf","PYTHON="+sys.executable],cwd=ROOT,check=True,capture_output=True)
    name="undergraduate-dna-computing" if DNA else "undergraduate-evolutor"
    pdf=ROOT/f"output/pdf/{name}.pdf"
    assert pdf.read_bytes().startswith(b"%PDF-")
    text=subprocess.check_output(["pdftotext",str(pdf),"-"],text=True)
    assert "Chapter 1 glossary" in text and "Bibliography" in text and "Index" in text
    assert "??" not in text
    assert all(f"Figure 1.{i}:" in text for i in range(1,7))
    log=(ROOT/f"build/{name}.log").read_text()
    assert not re.search(r"Overfull|Underfull|undefined references|undefined citations|Missing character",log)
