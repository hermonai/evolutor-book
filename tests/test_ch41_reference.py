import importlib.util
from pathlib import Path
import sys
from dataclasses import replace
import random
import pytest

spec = importlib.util.spec_from_file_location("evod41_test", Path(__file__).parents[1] / "drafts/ch41/reference.py")
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


@pytest.mark.parametrize("seed", range(32))
def test_optimization_against_recursive_oracle(seed):
    rng = random.Random(seed)
    ops, names = [], []
    for i in range(15):
        name = f"v{i}"
        if i < 3 or rng.random() < .3:
            op = r.Op(f"o{i}", "const", (), name, r.Ty.INT,
                      (("value", rng.randint(-10**20, 10**20)),))
        else:
            op = r.Op(f"o{i}", "add", tuple(rng.choices(names, k=2)), name, r.Ty.INT)
        ops.append(op); names.append(name)
    p = r.Program((), tuple(ops), (names[-1],))
    expected = r.expression_oracle(p, {})
    q = r.dce(r.constant_fold(p))
    assert r.interpret(p, {}, None)[0] == expected == r.interpret(q, {}, None)[0]
    assert r.dce(q) == q and r.constant_fold(q) == q


def test_unused_retrieval_engine_and_tool_not_pure():
    runtime = r.chapter(39)
    engines, _ = runtime.fixture()
    p = r.Program((("tokens", r.Ty.TOKENS),), (
        r.Op("eng", "engine", ("tokens",), "z", r.Ty.LOGITS,
             (("capability", "compressed_state"), ("artifact", engines[0].artifact)),
             r.EFFECTS["engine"]),
        *r.fixture().ops), ("n",))
    q = r.dce(r.constant_fold(p))
    assert [o.kind for o in q.ops if o.effects] == ["engine", "retrieve", "tool"]
    handlers = r.Effects(engines, ("tenant-a", "r"), runtime.Policy((("tenant-a", "echo"),)))
    a = r.interpret(p, {"tokens": (1, 2)}, handlers)
    b = r.interpret(q, {"tokens": (1, 2)}, handlers)
    assert a == b and all(not e._states for e in engines)


def test_effect_denial_preserved_after_dce():
    runtime = r.chapter(39)
    for p in (r.fixture(), r.dce(r.constant_fold(r.fixture()))):
        with pytest.raises(PermissionError):
            r.interpret(p, {}, r.Effects((), ("t", "r"), runtime.Policy()))


def test_memory_handlers_use_actual_ch40():
    memory = r.chapter(40).Memory()
    p = r.Program((("text", r.Ty.TEXT),), (
        r.Op("put", "mem_put", ("text",), "id", r.Ty.TEXT, (), r.EFFECTS["mem_put"]),
        r.Op("get", "mem_get", ("id",), "out", r.Ty.TEXT, (), r.EFFECTS["mem_get"])
    ), ("out",))
    h = r.Effects((), ("t", "r"), r.chapter(39).Policy(), memory)
    out, events = r.interpret(p, {"text": "evidence only"}, h)
    assert out == ("evidence only",) and [e[0] for e in events] == ["put", "get"]
    assert r.lower(p, ())[1]["dependencies"] == ("put",)


def test_no_return_value_effect_retained_and_ordered():
    p = r.fixture()
    q = replace(p, ops=p.ops + (replace(p.ops[-1], oid="act2"),))
    q = r.dce(r.constant_fold(q))
    schedule = r.lower(q, ())
    assert schedule[-1]["dependencies"] == ("act", "sum")
    assert [o.oid for o in q.ops if o.effects] == ["ret", "act", "act2"]


def test_exact_arithmetic_not_floating_associativity():
    p = r.Program((), (
        r.Op("a", "const", (), "a", r.Ty.INT, (("value", 2**100),)),
        r.Op("b", "const", (), "b", r.Ty.INT, (("value", 1),)),
        r.Op("c", "add", ("a", "b"), "c", r.Ty.INT)), ("c",))
    assert r.interpret(r.constant_fold(p), {}, None)[0] == (2**100 + 1,)
    with pytest.raises(TypeError):
        r.verify(replace(p, ops=(replace(p.ops[0], attrs=(("value", True),)),) + p.ops[1:]))


@pytest.mark.parametrize("change,exc", [
    ({"inputs": ("missing", "b")}, ValueError),
    ({"output": "a"}, ValueError), ({"out_ty": r.Ty.DOCS}, TypeError),
    ({"effects": ("external",)}, ValueError), ({"kind": "magic"}, ValueError),
    ({"attrs": (("extra", 1),)}, ValueError)])
def test_verifier_negative_cases(change, exc):
    p = r.fixture()
    with pytest.raises(exc):
        r.verify(replace(p, ops=p.ops[:2] + (replace(p.ops[2], **change),) + p.ops[3:]))


def test_effect_erasure_rejected_before_optimization():
    p = r.fixture()
    p = replace(p, ops=p.ops[:-1] + (replace(p.ops[-1], effects=()),))
    for transform in (r.verify, r.dce, r.constant_fold):
        with pytest.raises(ValueError):
            transform(p)


def test_unknown_schema_duplicate_op_and_outputs():
    p = r.fixture()
    for q in (replace(p, schema="evod41-v2"), replace(p, outputs=("missing",)),
              replace(p, ops=p.ops + (p.ops[0],))):
        with pytest.raises(ValueError):
            r.verify(q)


def test_peak_includes_output_and_simultaneous_inputs():
    p = r.Program((("a", r.Ty.INT), ("b", r.Ty.INT)),
        (r.Op("sum", "add", ("a", "b"), "c", r.Ty.INT),), ("c",))
    assert r.peak_live_values(p) == 3
    p = r.Program((), (r.Op("a", "const", (), "a", r.Ty.INT, (("value", 1),)),
                      r.Op("z", "const", (), "z", r.Ty.INT, (("value", 2),))), ("a",))
    assert r.peak_live_values(p) == 2  # dead allocation is released immediately


def test_all_operations_can_be_dead_with_input_output():
    p = r.Program((("x", r.Ty.INT),),
        (r.Op("dead", "const", (), "a", r.Ty.INT, (("value", 1),)),), ("x",))
    q = r.dce(p)
    assert q.ops == () and r.interpret(q, {"x": 7}, None)[0] == (7,)


def test_invalid_handler_result_is_rejected():
    p = r.Program((), (r.fixture().ops[-2],), ("docs",))
    with pytest.raises(TypeError):
        r.interpret(p, {}, lambda *args: "untyped flattened text")


@pytest.mark.parametrize("cap", ["compressed_state", "addressable_kv"])
def test_lower_and_execute_real_engine(cap):
    rt = r.chapter(39)
    engine = rt.EngineAdapter("dogma" if cap == "compressed_state" else "hermon")
    p = r.Program((("t", r.Ty.TOKENS),), (r.Op("e", "engine", ("t",), "z", r.Ty.LOGITS,
        (("capability", cap), ("artifact", engine.artifact)), r.EFFECTS["engine"]),), ("z",))
    assert r.lower(p, (engine,))[0]["backend"] == engine.backend
    out, ev = r.interpret(p, {"t": (1, 2)}, r.Effects((engine,), ("t", "r"), rt.Policy()))
    assert len(out[0]) == 2 and len(ev) == 1
    with pytest.raises(RuntimeError):
        r.lower(p, ())
