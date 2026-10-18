import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/'drafts/ch48/reference.py';s=importlib.util.spec_from_file_location('r',p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def test_rc_known():assert r.rc('AACGTN')=='NACGTT'
def test_rc_involution():assert r.rc(r.rc('ACGTN'))=='ACGTN'
def test_gc():assert r.gc('GGAA')==.5
def test_onehot_shape():assert len(r.onehot('ACG'))==3 and len(r.onehot('ACG')[0])==4
def test_group_split_no_overlap():
 e=[r.Example('a','c1','A',0),r.Example('b','c2','C',1)];a,b=r.group_split(e,{'c2'});assert {x.group for x in a}.isdisjoint({x.group for x in b})
def test_invariant_score():assert r.invariant_score('AACG')==r.invariant_score(r.rc('AACG'))
def test_accuracy():assert r.accuracy([1,0],[1,0])==1
def test_mcc_perfect():assert r.mcc([1,1,0,0],[1,1,0,0])==1
def test_mcc_degenerate_safe():assert r.mcc([1,1],[1,1])==0
def test_brier_perfect():assert r.brier([1,0],[1,0])==0
def test_bootstrap_deterministic():
 y=[1,0,1,0];p=[1,0,1,0];assert r.bootstrap_metric(y,p,r.accuracy,20,3)==r.bootstrap_metric(y,p,r.accuracy,20,3)
def test_unknown_base_rc():assert r.rc('NN')=='NN'
