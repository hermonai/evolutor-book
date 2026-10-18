import importlib.util
from pathlib import Path
import sys
import hashlib
from dataclasses import replace
from itertools import product
import pytest

spec = importlib.util.spec_from_file_location("evod44", Path(__file__).parents[1]/"drafts/ch44/reference.py")
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def candidate(d, name="a"):
    x = d.register(r.bundle(name, name), True)
    d.canary(x)
    d.health(x, live=True, ready=True)
    return x


def observed(d, x, prefix="r"):
    for i in range(3):
        q = prefix + str(i)
        d.admit(x, q)
        d.complete(x, q, 40 + 20*i)


def test_identity_is_canonical_and_semantically_bound():
    b = r.bundle("r1", "m")
    assert b.digest() == r.bundle("r1", "m").digest()
    for field, value in [("config", "new"), ("tokenizer", "other"),
                         ("state_schema", 2), ("model", "v2")]:
        assert replace(b, **{field: value}).digest() != b.digest()


def capsule():
    payloads={"model":b"weights-v1", "runtime":b"runtime-v1",
              "tokenizer":b"ACGT", "config":b'{"max_output":64}'}
    fields={k:hashlib.sha256(v).hexdigest() for k,v in payloads.items()}
    return r.Bundle("r1",**fields),payloads


def test_actual_capsule_bytes():
    b,p=capsule()
    assert r.verify_capsule(b,p,b.digest())==b.digest()
    assert b.tokenizer=="1dff3e84fe7877e0673b69bbddcf40124e396e3f9943dd890c91b6a09adb9af0"


@pytest.mark.parametrize("change",["corrupt","missing","extra","mutable","oversized"])
def test_capsule_malformed_or_corrupted_rejected(change):
    b,p=capsule()
    if change=="corrupt":p["model"]=b"weights-v2"
    if change=="missing":del p["config"]
    if change=="extra":p["debug"]=b"not-declared"
    if change=="mutable":p["model"]=bytearray(p["model"])
    if change=="oversized":p["runtime"]=b"x"*1_000_001
    with pytest.raises(ValueError):r.verify_capsule(b,p,b.digest())


def test_coherent_capsule_forgery_requires_independent_pin():
    b,p=capsule();old=b.digest();p["model"]=b"replacement"
    forged=replace(b,model=hashlib.sha256(p["model"]).hexdigest())
    with pytest.raises(ValueError):r.verify_capsule(forged,p,old)
    # Internal byte consistency cannot authenticate an attacker-supplied new pin.
    assert r.verify_capsule(forged,p,forged.digest())==forged.digest()


@pytest.mark.parametrize("field,value", [("api",2),("state_schema",2),
    ("policy_schema",2),("backend","cuda"),("api",True),("model","")])
def test_incompatible_or_malformed_bundle(field,value):
    d = r.Deployment()
    with pytest.raises(ValueError):
        d.register(replace(r.bundle("r","m"), **{field:value}), True)
    assert not d.revisions and not d.events


@pytest.mark.parametrize("verified",[False,"false",1,None])
def test_nonempty_provenance_is_not_verification(verified):
    d = r.Deployment()
    with pytest.raises(ValueError):
        d.register(r.bundle("x","m"), verified)


def test_empty_and_one_sample_do_not_promote():
    d = r.Deployment(gate=r.Gate(minimum=3))
    x = candidate(d)
    with pytest.raises(RuntimeError): d.promote(x)
    d.admit(x,"r"); d.complete(x,"r",1)
    with pytest.raises(RuntimeError): d.promote(x)


def test_revision_local_evidence():
    d = r.Deployment(gate=r.Gate(minimum=3))
    a = candidate(d); observed(d,a); d.promote(a)
    b = candidate(d,"b")
    with pytest.raises(RuntimeError): d.promote(b)
    observed(d,b,"b"); d.promote(b)
    assert d.previous == a


@pytest.mark.parametrize("obs", [[(1,False)]*3, [(10,True),(20,True),(900,True)]])
def test_gate_negative_controls(obs):
    assert not r.Gate(3,.1,500).passes(obs)


def test_nearest_rank_detects_small_sample_tail():
    assert r.nearest_rank([10,20,900],.95) == 900


@pytest.mark.parametrize("value", [-1,float("nan"),float("inf"),True])
def test_bad_completion_is_atomic(value):
    d=r.Deployment(); x=candidate(d); d.admit(x,"r")
    with pytest.raises(ValueError): d.complete(x,"r",value)
    assert d.jobs == {"r":x} and d.revisions[x].completed == 0


def test_foreign_duplicate_and_late_completion():
    d=r.Deployment(); a=candidate(d); b=candidate(d,"b"); d.admit(a,"r")
    with pytest.raises(RuntimeError): d.complete(b,"r",10)
    d.drain(a)
    with pytest.raises(RuntimeError): d.terminate(a)
    d.complete(a,"r",10); d.terminate(a)
    with pytest.raises(RuntimeError): d.complete(a,"r",10)
    with pytest.raises(RuntimeError): d.admit(b,"r")
    d.check()


def test_liveness_is_insufficient_and_capacity_is_global():
    d=r.Deployment(capacity=1); a=d.register(r.bundle("a","m"),True); d.canary(a)
    with pytest.raises(RuntimeError): d.admit(a,"x")
    d.health(a,live=True,ready=True); d.admit(a,"x"); b=candidate(d,"b")
    with pytest.raises(RuntimeError): d.admit(b,"y")


def test_rollback_preserves_inflight_and_checks_schema():
    d=r.Deployment(gate=r.Gate(3)); a=candidate(d); observed(d,a); d.promote(a)
    b=candidate(d,"b"); observed(d,b,"b"); d.promote(b); d.admit(b,"late")
    with pytest.raises(RuntimeError): d.rollback(2)
    assert d.active == b
    assert d.rollback(1) == a
    d.complete(b,"late",1); d.drain(b); d.terminate(b); d.check()


def test_all_short_lifecycle_words_against_manual_owner_count():
    # Independent admitted/settled count; rejected actions must not change it.
    for word in product("acdt", repeat=5):
        d=r.Deployment(capacity=2); x=candidate(d); held=set(); finished=set(); draining=False
        for i,event in enumerate(word):
            q="q"+str(i)
            try:
                if event=="a":
                    d.admit(x,q); assert not draining and len(held)<2; held.add(q)
                elif event=="c":
                    target=min(held) if held else "absent"
                    d.complete(x,target,10); held.remove(target); finished.add(target)
                elif event=="d": d.drain(x); draining=True
                else: d.terminate(x); assert draining and not held
            except RuntimeError:
                if event=="a": assert draining or len(held)==2
                if event=="c": assert not held
                if event=="t": assert not draining or held or d.revisions[x].state=="terminated"
            assert set(d.jobs)==held
            assert d.revisions[x].completed==len(finished)
            d.check()
