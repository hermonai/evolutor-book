"""Chapter 2 exact semantics, negative controls, provenance and preservation."""
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
from itertools import permutations, product
from fractions import Fraction
import pytest

ROOT=Path(__file__).resolve().parents[1]
DNA=ROOT.name=="dna-computing-book"
PREFIX="DNAD-02" if DNA else "EVOD-02"
BASE="6046afc3b1ef1bee59b11176a65a3e73778c125f" if DNA else "b319a6abcc834e3630855556761e9ea5714cc3dd"
sys.path.insert(0,str(ROOT/"scripts"))

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

M=load("chapter02_test","examples/deep/ch02.py")
BUILD=load("chapter02_assets","scripts/build_deep_chapter02.py")

def test_artifacts_fresh():
    for path,content in BUILD.outputs().items():
        assert (ROOT/path).read_text()==content,path

@pytest.mark.parametrize("number",range(1,15 if DNA else 14))
def test_vectors_and_semantic_companions(number):
    name=f"{PREFIX}-F{number}"
    svg=ET.fromstring((ROOT/f"book/figures/deep/{name}.svg").read_text())
    ns={"s":"http://www.w3.org/2000/svg"}
    assert svg.attrib["aria-labelledby"]=="title desc"
    assert svg.find("s:title",ns).text and svg.find("s:desc",ns).text
    assert svg.findall(".//s:text",ns) and not svg.findall(".//s:image",ns)
    content=(ROOT/f"book/diagrams/deep/{name}.txt").read_text()
    for heading in ("QUESTION","OBJECTS","RELATION / MECHANISM","STATE TRANSITION","INFERENCE","BOUNDARY","SOURCE"):
        assert heading in content
    assert not set("┌└│─") & set(content)

def test_keyframes_change_actual_content():
    entries=json.loads((ROOT/f"animation/{PREFIX.lower()}/frames.json").read_text())
    assert len(entries)==9
    for sequence in {x["sequence"] for x in entries}:
        selected=[x for x in entries if x["sequence"]==sequence]
        assert [x["phase"] for x in selected]==[1,2,3]
        # Exclude titles/metadata: rendered geometry/text itself must change.
        bodies=[]
        for x in selected:
            tree=ET.fromstring((ROOT/f"animation/{PREFIX.lower()}"/x["source"]).read_text())
            bodies.append(ET.tostring(tree.find("{http://www.w3.org/2000/svg}g")))
        assert len(set(bodies))==3

def test_chapter_one_and_all_preceding_pdfs_unchanged():
    review=json.loads((ROOT/"artifacts/deep/ch01-review.json").read_text())
    paths=list(review["reviewedSources"])+["artifacts/deep/ch01-review.json"]
    paths+=subprocess.check_output(["git","ls-tree","-r","--name-only",BASE,"--","output/pdf"],cwd=ROOT,text=True).splitlines()
    for path in set(paths):
        old=subprocess.check_output(["git","show",BASE+":"+path],cwd=ROOT)
        assert (ROOT/path).read_bytes()==old,path

def test_source_and_reference_closure():
    import re
    body=(ROOT/"tex/deep/ch02.tex").read_text()
    all_body=(ROOT/"tex/deep/ch01.tex").read_text()+body
    bib=(ROOT/"tex/deep/references-ch01-02.tex").read_text()
    keys=re.findall(r"\\bibitem\{([^}]+)\}",bib)
    assert len(keys)==len(set(keys))
    cited={k for g in re.findall(r"\\cite\{([^}]+)\}",all_body) for k in g.split(",")}
    assert cited==set(keys)
    assert len(re.findall(r"\\section\{",body))>=18
    assert len(re.findall(r"\\item ",body))==24
    assert len(re.findall(r"\\DeepFigure\{",body))==(14 if DNA else 13)
    assert not (ROOT/"tex/deep/ch03.tex").exists()

if DNA:
    def test_historical_graph_exact():
        assert M.EDGES==frozenset({(0,1),(0,3),(0,6),(1,2),(1,3),(2,1),(2,3),
                                 (3,2),(3,4),(4,1),(4,5),(5,1),(5,2),(5,6)})
        assert M.oracle()==[tuple(range(7))]

    def test_full_inventory_and_fault_counts():
        pool=M.generate_candidates()
        assert [len(p) for _,p in M.pipeline(pool)]==[1583,9,2,1,1,1,1,1,1]
        pseudo=(0,1,2,4,3,5,6)
        assert [len(p) for _,p in M.pipeline(pool+[pseudo]*10)]==[1593,19,12,11,11,11,11,11,1]
        assert M.pipeline([tuple(range(7))]*3)[-1][1]==[tuple(range(7))]*3

    @pytest.mark.parametrize("edge",[(i,i+1) for i in range(6)])
    def test_remove_each_required_edge(edge):
        assert M.oracle(M.EDGES-{edge})==[]

    @pytest.mark.parametrize("bound",[0,-1,1.5,True,None])
    def test_invalid_walk_bound(bound):
        with pytest.raises(ValueError):M.generate_candidates(bound)

    def test_permutation_differential():
        for order in permutations(range(1,6)):
            p=(0,)+order+(6,)
            direct=all((a,b) in M.EDGES for a,b in zip(p,p[1:]))
            assert M.is_witness(p)==direct
        assert set(M.pipeline(M.generate_candidates())[-1][1])==set(M.oracle())

    def test_sequence_orientation_and_endpoint_lengths():
        assert M.edge_sequence(2,3)=="GTATATCCGAGCTATTCGAG"
        assert M.edge_sequence(3,4)=="CTTAAAGCTAGGCTAGGTAC"
        assert M.complement(M.PUBLISHED_CODES[3])=="CGATAAGCTCGAATTTCGAT"
        fake={0:"A"*20,1:"C"*20,6:"G"*20}
        assert len(M.edge_sequence(0,6,fake))==40
        assert len(M.edge_sequence(0,1,fake))==30
        assert len(M.edge_sequence(1,6,fake))==30
        with pytest.raises(KeyError):M.edge_sequence(0,1)

    @pytest.mark.parametrize("seq",["","AN","acgt","AC G"])
    def test_invalid_base_strings(seq):
        with pytest.raises(ValueError):M.complement(seq)

    def test_complement_involution():
        for xs in product("ACGT",repeat=4):
            s="".join(xs);assert M.complement(M.complement(s))==s

    def test_band_projection_and_lost_multiplicity():
        witness=tuple(range(7))
        assert M.graduated_bands([witness])=={str(v):[20*(v+1)] for v in range(1,7)}
        assert M.graduated_bands([witness]*10)==M.graduated_bands([witness])
        assert M.graduated_bands([(0,3,2,3,4,5,6)])["3"]==[40,80]
        with pytest.raises(ValueError):M.graduated_bands([(1,2,3)])
        with pytest.raises(ValueError):M.graduated_bands([(0,8)])

    def test_survival_exact_and_boundaries():
        r=M.survival(3,1000,Fraction(4,5),Fraction(1,10),5)
        assert r["rows"][-1]=={"stage":5,"true_expected":.98304,"false_expected":.01}
        assert r["zero_true_probability"]==pytest.approx(.303898175111168)
        assert M.survival(3,0,1,0,5)["zero_true_probability"]==0
        assert M.survival(3,0,0,0,5)["zero_true_probability"]==1
        assert M.survival(0,0,1,1,0)["zero_true_probability"]==1

    @pytest.mark.parametrize("args",[(-1,0,1,1,1),(1,0,-.1,1,1),(1,0,1,1.1,1),(1,0,1,1,True)])
    def test_survival_domain(args):
        with pytest.raises(ValueError):M.survival(*args)
else:
    import torch
    from torch import nn
    from evo_torch.causality import prefix_intervention_error, assert_prefix_causal

    def test_split_transitivity_and_row_order():
        records=M.sample_records()
        expected=M.split_records(records)
        assert any({"a1","a2","b1"}<=set(v) for v in expected.values())
        for seed in range(5):
            g=torch.Generator().manual_seed(seed)
            order=torch.randperm(len(records),generator=g).tolist()
            assert M.split_records([records[i] for i in order])==expected
        by_id={r["id"]:r for r in records}
        for a,b in permutations(expected,2):
            for i in expected[a]:
                for j in expected[b]:
                    assert by_id[i]["group"]!=by_id[j]["group"]
                    s,t=by_id[i]["sequence"],by_id[j]["sequence"]
                    assert s!=t and s!=M.reverse_complement(t)

    @pytest.mark.parametrize("fractions",[(1,0,0),(.5,.5,.5),(.5,float("nan"),.5),(.5,.5)])
    def test_split_invalid_fractions(fractions):
        with pytest.raises(ValueError):M.split_records(M.sample_records(),fractions=fractions)

    def test_split_rejects_impossible_and_duplicate_ids():
        records=M.sample_records()
        with pytest.raises(ValueError):M.split_records(records+[records[0]])
        with pytest.raises(ValueError):M.split_records(records[:3])
        with pytest.raises(ValueError):M.split_records([])

    @pytest.mark.parametrize("seed",[11,29,47])
    def test_uniform_entropy_and_future_leak(seed):
        x=torch.randint(4,(8,33),generator=torch.Generator().manual_seed(seed))
        inp,y=x[:,:-1],x[:,1:]
        result=M.token_metrics(torch.zeros(8,32,4,dtype=torch.float64),y)
        assert result["nats_per_base"]==pytest.approx(math.log(4))
        assert result["perplexity"]==pytest.approx(4)
        assert result["bits_per_base"]==pytest.approx(2)
        leaky=M.token_metrics(M.FutureCopy()(inp)[:,:-1],y[:,:-1])
        assert leaky["accuracy"]==1
        assert leaky["nats_per_base"]==pytest.approx(math.log1p(3*math.exp(-8)))

    @pytest.mark.parametrize("boundary",range(1,8))
    def test_intervention_positive_and_negative(boundary):
        ids=torch.tensor([[0,1,2,3,0,1,2,3]])
        assert prefix_intervention_error(M.PrefixCounts(),ids,prefix_length=boundary,vocab_size=4)==0
        assert prefix_intervention_error(M.FutureCopy(),ids,prefix_length=boundary,vocab_size=4)==8
        with pytest.raises(AssertionError):
            assert_prefix_causal(M.FutureCopy(),ids,prefix_length=boundary,vocab_size=4,atol=1e-12)

    @pytest.mark.parametrize("bad",[float("nan"),float("inf"),-1])
    def test_invalid_tolerance_cannot_pass(bad):
        with pytest.raises(ValueError):
            assert_prefix_causal(M.PrefixCounts(),torch.tensor([[0,1]]),prefix_length=1,vocab_size=4,atol=bad)

    def test_nonfinite_and_exception_restore_mixed_modes():
        class Broken(nn.Module):
            def __init__(self,raises):
                super().__init__();self.child=nn.Dropout();self.raises=raises
            def forward(self,ids):
                if self.raises:raise RuntimeError("test failure")
                return torch.full((*ids.shape,4),float("nan"))
        for raises in (True,False):
            model=Broken(raises);model.train();model.child.eval()
            with pytest.raises(RuntimeError if raises else ValueError):
                prefix_intervention_error(model,torch.tensor([[0,1]]),prefix_length=1,vocab_size=4)
            assert model.training and not model.child.training

    @pytest.mark.parametrize("ids,prefix,vocab",[
        (torch.tensor([0,1]),1,4),(torch.tensor([[0.,1.]]),1,4),
        (torch.tensor([[0,4]]),1,4),(torch.tensor([[0,1]]),0,4),
        (torch.tensor([[0,1]]),2,4),(torch.tensor([[0,1]]),True,4),
        (torch.tensor([[0,1]]),1,1)])
    def test_invalid_intervention_domain(ids,prefix,vocab):
        with pytest.raises(ValueError):
            prefix_intervention_error(M.PrefixCounts(),ids,prefix_length=prefix,vocab_size=vocab)

    def test_oracle_alignment_and_edge_cases():
        assert M.delay_oracle([0,1,2,3,0,1],2)==(0,1,2,3)
        assert M.delay_oracle([1,1,1],1)==(1,1)
        assert M.delay_oracle([0,1,2,3],3)==(0,)
        for lag in (0,-1,4,True,1.5):
            with pytest.raises(ValueError):M.delay_oracle([0,1,2,3],lag)

    def test_seed_summary_and_parameter_formulas():
        r=M.seed_summary([.51,.97,.99])
        assert r["mean"]==pytest.approx(.8233333333333334)
        assert r["median"]==.97
        assert r["sample_sd"]==pytest.approx(.2715388247255507)
        assert M.toy_parameter_counts(16,32)=={"recurrent":384,"attention_ffn":2176}
        for values in ([1],[1,float("nan")]):
            with pytest.raises(ValueError):M.seed_summary(values)
        with pytest.raises(ValueError):M.toy_parameter_counts(True,32)

    def test_empty_invalid_logits_and_targets_rejected():
        with pytest.raises(ValueError):M.token_metrics(torch.zeros(1,0,4),torch.zeros(1,0,dtype=torch.long))
        with pytest.raises(ValueError):M.token_metrics(torch.full((1,2,4),float("inf")),torch.zeros(1,2,dtype=torch.long))
        with pytest.raises(ValueError):M.token_metrics(torch.zeros(1,2,4),torch.full((1,2),4,dtype=torch.long))

    def test_registered_spec_hash_and_no_training_claim():
        import hashlib
        result=M.results()
        spec=(ROOT/"research/EVO-EXP01-ch02-spec.json").read_bytes()
        assert result["spec_sha256"]==hashlib.sha256(spec).hexdigest()
        assert "parent training experiment remains NOT RUN" in result["scope"]
