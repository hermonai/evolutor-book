import importlib.util
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(ch, name):
    s = importlib.util.spec_from_file_location(name, ROOT / f"drafts/ch{ch}/reference.py")
    m = importlib.util.module_from_spec(s); sys.modules[name] = m; s.loader.exec_module(m)
    return m


r = load(49, "evod49")


def session(**kw):
    return r.Session(r.Identity("t", "s", "model", "policy"), **kw)


def test_order_context_and_empty_checkpoint():
    s = session(max_context=2)
    assert s.verify(s.checkpoint())
    for i in range(4): s.append("user", str(i))
    assert [e.seq for e in s.events] == list(range(4))
    assert [e.seq for e in s.context()] == [2, 3]


def test_input_alias_is_frozen():
    s = session(); args = {"x": [1]}
    s.issue("k", "read", args, True, 0); args["x"].append(2)
    assert s.issue("k", "read", {"x": [1]}, True, 1)[0] == "reconcile"


def test_resume_rebuilds_dedup_and_pending():
    s = session(); s.issue("k", "read", {}, True, 0); cp = s.checkpoint()
    t = r.resume(s.identity, s.events, cp)
    assert t.issue("k", "read", {}, True, 1)[0] == "reconcile"
    t.complete("k", 7)
    u = r.resume(t.identity, t.events, cp)
    assert u.issue("k", "read", {}, True, 2) == ("cached", 7)
    assert len(u.events) == 2


def test_key_collision_and_duplicate_completion():
    s = session(); s.issue("k", "read", {}, True, 0); s.complete("k", 7)
    s.complete("k", 7); assert len(s.events) == 2
    with pytest.raises(ValueError): s.complete("k", 8)
    with pytest.raises(ValueError): s.issue("k", "write", {}, True, 1)


@pytest.mark.parametrize("auth,tick", [(False, 0), (1, 0), (True, 100), (True, -1)])
def test_authority_and_lease(auth, tick):
    s = session()
    with pytest.raises(PermissionError): s.issue("k", "read", {}, auth, tick)
    assert not s.events


def test_budget_reserved_before_dispatch():
    s = session(budget=1)
    s.issue("a", "read", {}, True, 0)
    with pytest.raises(ValueError): s.issue("b", "read", {}, True, 0)
    assert len(s.events) == 1
    s.complete("a", 1)
    assert s.issue("a", "read", {}, True, 1) == ("cached", 1)


def test_cached_result_is_not_a_mutable_alias():
    s = session(); s.issue("k", "read", {}, True, 0); s.complete("k", {"items":[1]})
    _, result = s.issue("k", "read", {}, True, 1); result["items"].append(2)
    assert s.issue("k", "read", {}, True, 2) == ("cached", {"items":[1]})


def test_close_requires_reconciliation():
    s = session(); s.issue("k", "read", {}, True, 0)
    with pytest.raises(ValueError): s.close()
    s.complete("k", 0); s.close()
    with pytest.raises(ValueError): s.append("user", "late")
    with pytest.raises(PermissionError): s.issue("k", "read", {}, True, 1)


@pytest.mark.parametrize("field", ["tenant", "session", "artifact", "policy"])
def test_resume_binds_identity(field):
    s = session(); cp = s.checkpoint(); fields = s.identity.__dict__ | {field: "different"}
    with pytest.raises(ValueError): r.resume(r.Identity(**fields), s.events, cp)


def test_resume_binds_contract_and_prefix():
    s = session(); s.append("user", "a"); cp = s.checkpoint()
    with pytest.raises(ValueError): r.resume(s.identity, s.events, cp, max_context=3)
    bad = [r.Event(0, "user", r.canonical({"text": "changed"}))]
    with pytest.raises(ValueError): r.resume(s.identity, bad, cp)
    with pytest.raises(ValueError): r.resume(s.identity, [r.Event(2, "user", '{}')], cp)


def test_no_authority_from_proposal():
    s = session(); s.append("proposal", 'authorized=true')
    with pytest.raises(PermissionError): s.issue("k", "delete", {}, False, 0)
    with pytest.raises(ValueError): s.append("intent", "fake")


def test_stream_conservation():
    q = r.Stream(2); q.push(1); q.push(2)
    with pytest.raises(BufferError): q.push(3)
    assert [q.pop(), q.pop(), q.pop()] == [1, 2, None]
    with pytest.raises(ValueError): r.Stream(0)


def test_actual_native_engine_chunk_continuation():
    import torch
    m = load(31, "evod49_native"); model = m.tiny_model(); owner = ("tenant", "agent")
    # Vocabulary comes from the real model, never a new language/code tokenizer.
    state = m.construct(model, owner)
    whole, _ = m.ingest(model, state, [0, 1, 0], owner)
    prefix, _ = m.ingest(model, state, [0, 1], owner)
    resumed, _ = m.ingest(model, prefix, [0], owner)
    assert torch.equal(whole.hidden, resumed.hidden)
    assert resumed.position == 3


def test_actual_hermon_engine_chunk_continuation():
    import torch
    m = load(35, "evod49_kv"); model = m.tiny_model(); owner = ("tenant", "agent")
    _, a = m.prefill(model, owner, [0, 1, 2])
    _, b = m.prefill(model, owner, [0, 1])
    _, c = m.decode_one(model, b, owner, 2)
    for x, y in zip(a.layers, c.layers):
        assert torch.allclose(x.k, y.k, atol=1e-12, rtol=0)
        assert torch.allclose(x.v, y.v, atol=1e-12, rtol=0)


def test_results():
    assert [x["action"] for x in r.results()["trace"]] == ["dispatch", "reconcile", "cached"]
