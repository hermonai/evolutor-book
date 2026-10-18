import importlib.util
from pathlib import Path
import sys
from dataclasses import replace
import hashlib
import pytest

spec=importlib.util.spec_from_file_location("evod46",Path(__file__).parents[1]/"drafts/ch46/reference.py")
r=importlib.util.module_from_spec(spec);sys.modules[spec.name]=r;spec.loader.exec_module(r)


def cluster():
    return r.Cluster([r.Worker("a","z1","dogma",2),r.Worker("b","z2","dogma",2),
                      r.Worker("p","z1","prefill",1),r.Worker("d","z1","decode",1)])


def make(c):return c.create("A","m","dogma",b"state","z1")


@pytest.mark.parametrize("field,value",[("backend","hermon"),("schema",2),
    ("tenants",frozenset({"X"})),("artifacts",frozenset({"other"}))])
def test_hard_constraints_before_cost(field,value):
    c=r.Cluster([replace(r.Worker("a","z1","dogma",2),**{field:value})])
    with pytest.raises(RuntimeError):make(c)
    assert c.used=={"a":0}


def test_migrate_preserves_identity_and_fences_old_owner():
    c=cluster();h=make(c);t=c.prepare(h,"b")
    assert c.read(h)==b"state"
    with pytest.raises(RuntimeError):c.write(h,b"new")
    n=c.commit(t,b"state")
    assert replace(n,owner=h.owner,epoch=h.epoch)==h
    assert c.read(n)==b"state" and c.used["a"]==0 and c.used["b"]==1
    with pytest.raises(RuntimeError):c.read(h)
    with pytest.raises(RuntimeError):c.commit(t,b"state")
    c.check()


def test_corruption_retains_old_authority_until_explicit_abort():
    c=cluster();h=make(c);t=c.prepare(h,"b")
    with pytest.raises(RuntimeError):c.commit(t,b"corrupt")
    assert c.read(h)==b"state" and c.reserved["b"]==1
    c.abort(t);c.write(h,b"new");assert c.read(h)==b"new";c.check()


@pytest.mark.parametrize("phase",["before","prepared","committed"])
def test_cancel_at_each_phase_never_resurrects(phase):
    c=cluster();h=make(c);t=None
    if phase!="before":t=c.prepare(h,"b")
    if phase=="committed":h=c.commit(t,t.payload)
    c.cancel(h)
    with pytest.raises(RuntimeError):c.read(h)
    if t:
        with pytest.raises(RuntimeError):c.commit(t,t.payload)
    assert sum(c.used.values())==0 and sum(c.reserved.values())==0;c.check()


@pytest.mark.parametrize("failed",["a","b"])
def test_crash_during_copy(failed):
    c=cluster();h=make(c);t=c.prepare(h,"b");c.fail(failed)
    with pytest.raises(RuntimeError):c.commit(t,t.payload)
    c.abort(t);c.check()
    if failed=="a":
        n=c.recover(h,"b",b"state",hashlib.sha256(b"state").hexdigest())
        assert c.read(n)==b"state" and n.epoch==1;c.check()
    else:assert c.read(h)==b"state"


def test_wrong_backend_destination_and_foreign_handle():
    c=cluster();h=make(c)
    with pytest.raises(RuntimeError):c.prepare(h,"p")
    with pytest.raises(RuntimeError):c.read(replace(h,tenant="B"))


def test_copied_transfer_is_not_issued():
    c=cluster();h=make(c);t=c.prepare(h,"b")
    with pytest.raises(RuntimeError):c.commit(replace(t),t.payload)
    c.abort(t);c.check()


def test_destination_reservation_prevents_overcommit():
    c=cluster();h=make(c);x=make(c);t=c.prepare(h,"b");u=c.prepare(x,"b")
    assert c.reserved["b"]==2
    with pytest.raises(RuntimeError):c.create("A","m","dogma",b"x","z2")
    # a is also full, so no fallback worker exists.
    c.abort(t);c.abort(u);c.check()


def test_recovery_does_not_trust_arbitrary_replay_payload():
    c=cluster();h=make(c);c.fail("a")
    with pytest.raises(RuntimeError):c.recover(h,"b",b"fake",hashlib.sha256(b"state").hexdigest())
    assert c.used["a"]==1 and c.used["b"]==0;c.check()


def test_downstream_reservation_is_all_or_none_and_releasable():
    c=cluster();ticket,pair=r.pd_reserve(c,"A","m","z1");c.check()
    assert pair==("p","d")
    before=dict(c.reserved)
    with pytest.raises(RuntimeError):r.pd_reserve(c,"B","m")
    assert c.reserved==before
    r.pd_release(c,ticket);c.check()
    with pytest.raises(RuntimeError):r.pd_release(c,ticket)


def test_empty_decode_pool_does_not_leak_prefill_reservation():
    c=cluster();c.fail("d")
    with pytest.raises(RuntimeError):r.pd_reserve(c,"A","m")
    assert sum(c.reserved.values())==0


def test_many_back_and_forth_migrations_conserve_capacity():
    c=cluster();h=make(c)
    for i in range(20):
        t=c.prepare(h,"b" if h.owner=="a" else "a");h=c.commit(t,t.payload)
        assert h.epoch==i+1 and sum(c.used.values())==1;c.check()


def test_payload_model_uses_bytes_per_second():
    assert r.transfer_ms(1_000_000,1_000_000_000,.1)==1.1


@pytest.mark.parametrize("nn",[31,35])
def test_actual_model_snapshot_roundtrip_and_suffix_continuation(nn):
    # Test-local, trusted data-only adapter. No loader for arbitrary files.
    import json
    import torch
    path=Path(__file__).parents[1]/f"drafts/ch{nn}/reference.py"
    spec=importlib.util.spec_from_file_location(f"evod46_fixture{nn}",path)
    m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
    model=m.tiny_model();owner=("A","request")
    if nn==31:
        state,_=m.ingest(model,m.construct(model,owner),(0,1),owner)
        body=dict(hidden=state.hidden.tolist(),position=state.position)
    else:
        _,state=m.prefill(model,owner,(0,1))
        body=dict(tokens=state.tokens,layers=[(x.k.tolist(),x.v.tolist()) for x in state.layers])
    artifact=m.artifact_id(model)
    c=r.Cluster([r.Worker(w,z,"native" if nn==31 else "kv",2,
                          artifacts=frozenset({artifact})) for w,z in [("a","z1"),("b","z2")]])
    payload=json.dumps(body,sort_keys=True,allow_nan=False).encode()
    h=c.create("A",artifact,"native" if nn==31 else "kv",payload,"z1")
    t=c.prepare(h,"b");n=c.commit(t,t.payload);restored=json.loads(c.read(n))
    if nn==31:
        rebuilt=m.State(owner,artifact,restored["position"],torch.tensor(restored["hidden"],dtype=torch.float64))
        expected=m.native_step(model,state,2,owner);actual=m.native_step(model,rebuilt,2,owner)
        torch.testing.assert_close(actual.logits,expected.logits,atol=0,rtol=0)
    else:
        layers=[m.LayerKV(torch.tensor(k,dtype=torch.float64),torch.tensor(v,dtype=torch.float64))
                for k,v in restored["layers"]]
        rebuilt=m.sealed(owner,artifact,tuple(restored["tokens"]),layers)
        expected,_=m.decode_one(model,state,owner,2)
        actual,_=m.decode_one(model,rebuilt,owner,2)
        torch.testing.assert_close(actual,expected,atol=0,rtol=0)
    c.check()
