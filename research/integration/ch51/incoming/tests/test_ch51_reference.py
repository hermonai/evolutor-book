import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch51/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def test_known_level(): assert r.valid(r.Claim("x","implemented"))
def test_unknown_level(): assert not r.valid(r.Claim("x","magic"))
def test_demonstrated_requires_benchmark(): assert not r.valid(r.Claim("x","benchmark-demonstrated"))
def test_demonstrated_contract(): assert r.valid(r.Claim("x","benchmark-demonstrated","b",True,True,True))
def test_one_step_promotion(): assert r.promote(r.Claim("x","implemented"),"tested").level=="tested"
def test_skip_rejected():
 try:r.promote(r.Claim("x","implemented"),"benchmark-demonstrated");assert False
 except ValueError:pass
def test_tested_to_demo_without_contract_rejected():
 try:r.promote(r.Claim("x","tested"),"benchmark-demonstrated");assert False
 except ValueError:pass
def test_demo_with_contract(): assert r.promote(r.Claim("x","tested"),"benchmark-demonstrated","b",True,True,True).held_out
def test_replication_requires_existing_contract(): c=r.Claim("x","benchmark-demonstrated","b",True,True,True);assert r.promote(c,"replicated").level=="replicated"
def test_scorecard_omits_invalid(): assert "bad" not in r.scorecard([r.Claim("bad","benchmark-demonstrated")])
def test_agi_hypothesis_is_valid_label_not_proof(): assert r.scorecard([r.Claim("AGI","hypothesized")])["AGI"]=="hypothesized"
def test_results(): assert r.results()["blocked_without_benchmark_contract"]
