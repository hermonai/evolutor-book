import importlib.util
from pathlib import Path
import sys
from dataclasses import replace
import json

import pytest
import torch

spec = importlib.util.spec_from_file_location("evod39_test", Path(__file__).parents[1] / "drafts/ch39/reference.py")
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
torch.set_num_threads(1)
OWNER = ("tenant-a", "r")


@pytest.mark.parametrize("backend", ["dogma", "hermon"])
@pytest.mark.parametrize("split", [1, 2, 3])
def test_real_native_all_splits(backend, split):
    e = r.EngineAdapter(backend)
    h = e.open(OWNER)
    tokens = (1, 2, 1, 0)
    a = e.execute(h, OWNER, tokens[:split])
    b = e.execute(h, OWNER, tokens[split:])
    got = torch.tensor(a.data + b.data, dtype=torch.float64)
    if backend == "hermon":
        expected = e.native.full_oracle(e.model, tokens)
    else:
        rows = [e.native.scalar_closed_form(e.model, tokens[:i])[1] for i in range(1, 5)]
        expected = torch.tensor(rows, dtype=torch.float64)
    torch.testing.assert_close(got, expected, atol=2e-12, rtol=2e-12)
    e.close(h, OWNER)
    assert not e._states


@pytest.mark.parametrize("backend", ["dogma", "hermon"])
@pytest.mark.parametrize("change", ["owner", "adapter", "artifact", "serial", "backend"])
def test_handle_identity(backend, change):
    e = r.EngineAdapter(backend)
    h = e.open(OWNER)
    altered = replace(h, **{change: {"owner": ("evil", "r"), "adapter": "other",
        "artifact": "0" * 64, "serial": 500, "backend": "other"}[change]})
    with pytest.raises(RuntimeError):
        e.execute(altered, OWNER, (1,))
    assert len(e._states) == 1


@pytest.mark.parametrize("backend", ["dogma", "hermon"])
def test_cross_instance_and_closed_handle(backend):
    e, other = r.EngineAdapter(backend), r.EngineAdapter(backend)
    h = e.open(OWNER)
    other.open(OWNER)  # serial collision must not imply adapter identity
    with pytest.raises(RuntimeError):
        other.execute(h, OWNER, (1,))
    e.close(h, OWNER)
    with pytest.raises(RuntimeError):
        e.close(h, OWNER)
    fresh = e.open(OWNER)
    assert fresh.serial != h.serial


@pytest.mark.parametrize("backend", ["dogma", "hermon"])
def test_invalid_chunk_leaves_state_unchanged(backend):
    e = r.EngineAdapter(backend)
    h = e.open(OWNER)
    old = e._states[h.serial]
    with pytest.raises(ValueError):
        e.execute(h, OWNER, (1, 999))
    assert e._states[h.serial] is old


def test_real_model_mutation_invalidates_but_can_close():
    e = r.EngineAdapter("dogma")
    h = e.open(OWNER)
    e.model.embedding[0, 0] = .1
    with pytest.raises(ValueError):
        e.execute(h, OWNER, (1,))
    e.close(h, OWNER)


def test_boolean_serial_cannot_alias_integer_serial():
    e = r.EngineAdapter("dogma")
    e.open(OWNER); h = e.open(OWNER)
    assert h.serial == 1
    with pytest.raises(RuntimeError):
        e.execute(replace(h, serial=True), OWNER, (1,))


def test_fixture_and_typed_outputs():
    engines, p = r.fixture()
    rt = r.Runtime(engines, r.Policy((("tenant-a", "echo"),)))
    out = rt.execute(p)
    assert out[3].data == 15 and out[4].data == ("echo", 15)
    assert out[0].data == ((0, "genomic memory"),)
    assert all(not e._states for e in engines)
    assert len(out[1].data[0]) == 3 and len(out[2].data[0]) == 4


def test_complete_preflight_before_earlier_tool():
    engines, p = r.fixture()
    calls = []
    bad = replace(p, steps=(p.steps[-1], replace(p.steps[3], inputs=("missing", "a"))))
    rt = r.Runtime(engines, r.Policy((("tenant-a", "echo"),)), lambda *x: calls.append(x))
    with pytest.raises(ValueError):
        rt.execute(bad)
    assert calls == [] and not rt.trace.events


def test_no_route_or_ambiguous_route():
    e = r.EngineAdapter("dogma")
    for engines in ((), (e, e)):
        with pytest.raises(RuntimeError):
            r.Runtime(engines, r.Policy()).route(e.capability, e.artifact)
    with pytest.raises(RuntimeError):
        r.Runtime((e,), r.Policy()).route(r.Capability.ADDRESSABLE_KV, e.artifact)


def test_denial_and_revocation_are_checked_at_call():
    engines, p = r.fixture()
    calls, policy = [], r.Policy((("tenant-a", "echo"),))
    policy.grants = frozenset()
    rt = r.Runtime(engines, policy, lambda *x: calls.append(x))
    with pytest.raises(PermissionError):
        rt.execute(p)
    assert not calls and all(not e._states for e in engines)
    assert json.loads(rt.trace.events[-1][0])["kind"] == "tool_denied"


def test_failure_after_open_closes_handle():
    engines, p = r.fixture()
    bad_inputs = tuple((k, replace(v, data=(1, 999))) if k == "t" else (k, v)
                       for k, v in p.inputs)
    with pytest.raises(ValueError):
        r.Runtime(engines, r.Policy()).execute(replace(p, inputs=bad_inputs))
    assert all(not e._states for e in engines)


def test_trace_chain_detects_changed_body():
    tr = r.Trace()
    tr.emit("one", x=1); tr.emit("two", x=2)
    for i, (encoded, seal) in enumerate(tr.events):
        body = json.loads(encoded)
        assert r.digest(body) == seal and body["seq"] == i
        assert body["previous"] == (tr.events[i-1][1] if i else "0" * 64)
    body["data"]["x"] = 100
    assert r.digest(body) != seal


def test_trace_failure_before_effect_blocks_callback():
    p = r.Plan(OWNER, (("n", r.Value(r.Ty.INT, 7)),),
        (r.Step("act", "tool", ("n",), "receipt", r.Ty.RECEIPT, "echo"),), ("receipt",))
    for fail_at in (0, 1, 2):
        calls = []
        rt = r.Runtime((), r.Policy(((OWNER[0], "echo"),)),
                       lambda *x: calls.append(x), r.Trace(fail_at))
        with pytest.raises(OSError):
            rt.execute(p)
        assert not calls


def test_receipt_trace_failure_does_not_undo_effect():
    p = r.Plan(OWNER, (("n", r.Value(r.Ty.INT, 7)),),
        (r.Step("act", "tool", ("n",), "receipt", r.Ty.RECEIPT, "echo"),), ("receipt",))
    calls = []
    rt = r.Runtime((), r.Policy(((OWNER[0], "echo"),)),
                   lambda *x: calls.append(x), r.Trace(3))
    with pytest.raises(OSError):
        rt.execute(p)
    assert len(calls) == 1  # explicitly uncertain completion, unsafe blind retry


@pytest.mark.parametrize("mutation", ["redefine", "forward", "type", "op"])
def test_bad_graph(mutation):
    engines, p = r.fixture()
    s = p.steps[3]
    kw = {"redefine": {"output": "a"}, "forward": {"inputs": ("n", "b")},
          "type": {"out_ty": r.Ty.DOCS}, "op": {"op": "magic"}}[mutation]
    with pytest.raises((ValueError, TypeError)):
        r.validate(replace(p, steps=p.steps[:3] + (replace(s, **kw),) + p.steps[4:]))
