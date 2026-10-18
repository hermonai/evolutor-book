from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import pytest

s = importlib.util.spec_from_file_location("evod52", Path(__file__).resolve().parents[1]/"drafts/ch52/reference.py")
r = importlib.util.module_from_spec(s); sys.modules[s.name] = r; s.loader.exec_module(r)


def setup():
    L = r.Ledger(); L.add_claim(r.Claim("C", "bounded claim", "tested", "counterexample", "toy", "a"*64, "b"*64))
    return L


def experiment(eid="E", cid="C", outcome="success"):
    return r.Experiment(eid,cid,"baseline","10 actions","difference",0.,(1,2),"a"*64,"d"*64,"suite","task",
                        outcome, .1 if outcome=="success" else -.1,"team-a", held_out=True)


def test_plan_not_observation():
    L = setup(); e = replace(experiment(), outcome="planned", lower_bound=None, evaluator="")
    L.add_experiment(e)
    with pytest.raises(ValueError): L.promote("C", "benchmark-demonstrated", ("E",))
    assert L.claims["C"].level == "tested"


def test_failure_cross_claim_rejected():
    L = setup(); L.add_claim(r.Claim("D","other","hypothesized","f","scope"))
    L.add_experiment(experiment(cid="D"))
    with pytest.raises(ValueError): L.add_failure(r.Failure("F","C","E","cat","symptom","counter"))


def test_failure_blocks_and_resolution_preserves():
    L = setup(); L.add_experiment(experiment(outcome="failure"))
    L.add_failure(r.Failure("F","C","E","regression","loss","case"))
    L.add_experiment(experiment("E2"))
    with pytest.raises(ValueError): L.promote("C","benchmark-demonstrated",("E2",))
    L.resolve("F","E2")
    L.promote("C","benchmark-demonstrated",("E2",))
    assert L.failures["F"].resolved_by == "E2"
    assert L.capsule()["ledger"]["failures"][0]["counterexample"] == "case"


def test_failed_experiment_cannot_promote():
    L = setup(); L.add_experiment(experiment(outcome="failure"))
    with pytest.raises(ValueError): L.promote("C","benchmark-demonstrated",("E",))


def test_unheldout_observation_cannot_promote():
    L = setup(); L.add_experiment(replace(experiment(), held_out=False))
    with pytest.raises(ValueError): L.promote("C","benchmark-demonstrated",("E",))


def test_replication_uses_ch51_contract():
    L = setup(); L.add_experiment(experiment())
    L.promote("C","benchmark-demonstrated",("E",))
    with pytest.raises(ValueError): L.promote("C","replicated")
    L.add_experiment(replace(experiment("E2"),evaluator="team-b",independent=True))
    L.promote("C","replicated",("E","E2"))
    assert L.claims["C"].level == "replicated"


@pytest.mark.parametrize("changes", [{"seeds": ()},{"seeds":(1,1)},{"budget":""},{"artifact_digest":"fake"},
     {"outcome":"unknown"},{"lower_bound":float('nan')},{"claim_id":"missing"}])
def test_invalid_experiment(changes):
    L = setup()
    with pytest.raises(ValueError): L.add_experiment(replace(experiment(),**changes))


def test_capsule_independent_canonical_oracle():
    L = setup(); a = L.capsule()
    raw = json.dumps(a["ledger"],sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    assert hashlib.sha256(raw).hexdigest() == a["sha256"]
    L.add_experiment(experiment()); assert L.capsule()["sha256"] != a["sha256"]


def test_file_change_and_missing_negative_control(tmp_path):
    (tmp_path/"a").write_text("first"); (tmp_path/"b").write_text("second")
    manifest = r.file_manifest(tmp_path,["a","b"])
    assert r.verify_files(tmp_path,manifest) == {"changed":[],"missing":[]}
    (tmp_path/"a").write_text("changed"); (tmp_path/"b").unlink()
    assert r.verify_files(tmp_path,manifest) == {"changed":["a"],"missing":["b"]}


@pytest.mark.parametrize("name", ["../a","/tmp/a","a/../b","./a",""])
def test_capsule_path_boundary(tmp_path,name):
    with pytest.raises(ValueError): r.file_manifest(tmp_path,[name])


def test_symlink_rejected(tmp_path):
    (tmp_path/"real").write_text("x"); (tmp_path/"link").symlink_to(tmp_path/"real")
    with pytest.raises(ValueError): r.file_manifest(tmp_path,["link"])


def test_envelope_tamper(tmp_path):
    (tmp_path/"a").write_text("x"); manifest = r.file_manifest(tmp_path,["a"])
    manifest["files"]["a"]="a"*64
    with pytest.raises(ValueError): r.verify_files(tmp_path,manifest)


def test_dependency_closure_and_cycle():
    assert r.dependency_order(["a","b","c"],{"a":["b"],"b":["c"],"c":[]}) == ("c","b","a")
    with pytest.raises(ValueError): r.dependency_order(["a"],{"a":["b"]})
    with pytest.raises(ValueError): r.dependency_order(["a","b"],{"a":["b"],"b":["a"]})


def test_actual_owned_reference_hash_closure():
    result = r.results()
    assert result["reference_verification"] == {"missing":[],"changed":[]}
    assert len(result["reference_closure"]["files"]) == 8
    assert result["claim_level"] == "hypothesized"


def test_uniform_entropy_and_finite_sample_counterexample():
    import math
    assert r.expected_uniform_ce([.25]*4) == pytest.approx(math.log(4))
    assert r.expected_uniform_ce([.7,.1,.1,.1]) > math.log(4)
    # One A sampled by chance scores better under a biased independent predictor.
    assert -math.log(.7) < math.log(4)


def test_actual_hermon_causal_suffix_control():
    import torch
    spec = importlib.util.spec_from_file_location("evod52_hermon", r.ROOT/"drafts/ch35/reference.py")
    m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m; spec.loader.exec_module(m)
    model = m.tiny_model()
    a, b = m.full_oracle(model,[0,1,2,3]), m.full_oracle(model,[0,1,0,0])
    assert torch.equal(a[:2],b[:2])
    assert not torch.allclose(a[2:],b[2:],atol=1e-8,rtol=0)
