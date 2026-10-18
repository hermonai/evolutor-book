import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch52/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def claim(): return r.Claim("C","x","hypothesized","counterexample")
def test_claim_requires_falsifier():
 L=r.Ledger()
 try:L.add_claim(r.Claim("C","x","hypothesized",""));assert False
 except ValueError:pass
def test_unknown_level_rejected():
 L=r.Ledger()
 try:L.add_claim(r.Claim("C","x","magic","f"));assert False
 except ValueError:pass
def test_experiment_requires_claim():
 L=r.Ledger()
 try:L.add_experiment(r.Experiment("E","missing","b","budget","m","t",(1,),"d"));assert False
 except ValueError:pass
def test_experiment_requires_budget():
 L=r.Ledger();L.add_claim(claim())
 try:L.add_experiment(r.Experiment("E","C","b","","m","t",(1,),"d"));assert False
 except ValueError:pass
def test_failure_requires_experiment():
 L=r.Ledger();L.add_claim(claim())
 try:L.add_failure(r.Failure("F","C","E","cat","s","c"));assert False
 except ValueError:pass
def test_one_level_promotion():
 L=r.Ledger();L.add_claim(claim());L.promote("C","implemented");assert L.claims["C"].level=="implemented"
def test_skip_promotion_rejected():
 L=r.Ledger();L.add_claim(claim())
 try:L.promote("C","tested");assert False
 except ValueError:pass
def test_benchmark_promotion_requires_evidence():
 L=r.Ledger();L.add_claim(r.Claim("C","x","tested","f"))
 try:L.promote("C","benchmark-demonstrated");assert False
 except ValueError:pass
def test_wrong_claim_evidence_rejected():
 L=r.Ledger();L.add_claim(r.Claim("C","x","tested","f"));L.add_claim(claim().__class__("D","y","tested","f"))
 L.add_experiment(r.Experiment("E","D","b","budget","m","t",(1,),"d"))
 try:L.promote("C","benchmark-demonstrated","E");assert False
 except ValueError:pass
def test_capsule_deterministic():
 L=r.Ledger();L.add_claim(claim());assert L.capsule()["sha256"]==L.capsule()["sha256"]
def test_failure_first_class():
 L=r.Ledger();L.add_claim(claim());L.add_experiment(r.Experiment("E","C","b","budget","m","t",(1,),"d"));L.add_failure(r.Failure("F","C","E","cat","s","counter"));assert "F" in L.failures
def test_fixture_counts():x=r.results();assert (x["claims"],x["experiments"],x["failures"])==(1,1,1)
def test_fixture_does_not_promote_failed_hypothesis():assert r.results()["claim_level"]=="hypothesized"
def test_capsule_digest_shape():assert len(r.results()["capsule_sha256"])==64
