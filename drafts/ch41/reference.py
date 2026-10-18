"""Straight-line typed IR: exact integer pure region, explicit ordered effects.

This is an inspectable interpreter/compiler, not MLIR/TVM or a device compiler.
Stateful engine/retrieval/memory/tool operations are never silently pure.
"""
from dataclasses import dataclass, replace
from enum import Enum
import importlib.util
from pathlib import Path
import sys
import math


def chapter(n):
    name = f"evod41_owned_{n}"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, Path(__file__).parents[1] / f"ch{n}/reference.py")
        m = importlib.util.module_from_spec(spec)
        sys.modules[name] = m
        spec.loader.exec_module(m)
    return sys.modules[name]


class Ty(str, Enum):
    INT = "int"
    TEXT = "text"
    TOKENS = "tokens"
    DOCS = "docs"
    LOGITS = "logits"


@dataclass(frozen=True)
class Op:
    oid: str
    kind: str
    inputs: tuple
    output: str | None
    out_ty: Ty | None
    attrs: tuple = ()
    effects: tuple = ()


@dataclass(frozen=True)
class Program:
    inputs: tuple
    ops: tuple
    outputs: tuple
    schema: str = "evod41-v1"


EFFECTS = {"const": (), "add": (), "retrieve": ("read_corpus",),
           "engine": ("engine_state",), "tool": ("policy", "external"),
           "mem_get": ("read_memory",), "mem_put": ("write_memory",)}
ATTRS = {"const": {"value"}, "add": set(),
         "retrieve": {"version", "query", "corpus"},
         "engine": {"capability", "artifact"}, "tool": {"name"},
         "mem_get": set(), "mem_put": set()}


def attributes(op):
    if type(op.attrs) is not tuple:
        raise ValueError("immutable attribute pairs")
    a = dict(op.attrs)
    if len(a) != len(op.attrs) or set(a) != ATTRS[op.kind]:
        raise ValueError("exact unique required attributes")
    return a


def verify(p):
    if (not isinstance(p, Program) or p.schema != "evod41-v1" or
            type(p.ops) is not tuple or not 0 <= len(p.ops) <= 256):
        raise ValueError("supported bounded IR schema")
    env, ids = dict(p.inputs), set()
    if len(env) != len(p.inputs) or any(not k or not isinstance(t, Ty)
                                      for k, t in env.items()):
        raise TypeError("unique typed inputs")
    for op in p.ops:
        if (not isinstance(op, Op) or not op.oid or op.oid in ids or
                op.kind not in EFFECTS or type(op.inputs) is not tuple):
            raise ValueError("known operation and unique ID")
        if op.effects != EFFECTS[op.kind]:
            raise ValueError("effect declaration differs from dialect semantics")
        if any(x not in env for x in op.inputs):
            raise ValueError("use before definition")
        a, ts = attributes(op), tuple(env[x] for x in op.inputs)
        signatures = {"const": ((), Ty.INT), "add": ((Ty.INT, Ty.INT), Ty.INT),
            "retrieve": ((), Ty.DOCS), "engine": ((Ty.TOKENS,), Ty.LOGITS),
            "tool": ((Ty.INT,), None), "mem_get": ((Ty.TEXT,), Ty.TEXT),
            "mem_put": ((Ty.TEXT,), Ty.TEXT)}
        if (ts, op.out_ty) != signatures[op.kind]:
            raise TypeError("operation signature mismatch")
        if op.kind == "const" and type(a["value"]) is not int:
            raise TypeError("mathematical integer; no bool/float coercion")
        if op.kind == "engine":
            if (a["capability"] not in ("compressed_state", "addressable_kv") or
                    type(a["artifact"]) is not str or len(a["artifact"]) != 64):
                raise ValueError("known capability and exact artifact identity")
        if op.kind == "retrieve":
            if (not isinstance(a["version"], str) or not a["version"] or
                    type(a["query"]) is not str or not a["query"] or
                    type(a["corpus"]) is not tuple or
                    any(type(d) is not str for d in a["corpus"])):
                raise ValueError("versioned immutable corpus fixture")
        if op.kind == "tool" and (type(a["name"]) is not str or not a["name"]):
            raise ValueError("named tool")
        if op.out_ty is None:
            if op.output is not None:
                raise TypeError("effect-only tool has no SSA result")
        else:
            if not op.output or op.output in env:
                raise ValueError("SSA redefinition/missing output")
            env[op.output] = op.out_ty
        ids.add(op.oid)
    if not p.outputs or any(x not in env for x in p.outputs):
        raise ValueError("defined program outputs")
    return env


def constant_fold(p):
    verify(p)
    constants, ops = {}, []
    for op in p.ops:
        if op.kind == "const":
            constants[op.output] = dict(op.attrs)["value"]
        elif op.kind == "add" and all(x in constants for x in op.inputs):
            value = constants[op.inputs[0]] + constants[op.inputs[1]]
            constants[op.output] = value
            op = replace(op, kind="const", inputs=(), attrs=(("value", value),))
        ops.append(op)
    q = replace(p, ops=tuple(ops))
    verify(q)
    return q


def dce(p):
    verify(p)
    live, kept = set(p.outputs), []
    for op in reversed(p.ops):
        if op.effects or op.output in live:
            kept.append(op)
            live.update(op.inputs)
    q = replace(p, ops=tuple(reversed(kept)))
    verify(q)
    return q


def interpret(p, inputs, effect):
    verify(p)
    if set(inputs) != set(dict(p.inputs)):
        raise ValueError("exact input keys")
    env, events = dict(inputs), []
    for name, ty in p.inputs:
        value = env[name]
        if ((ty == Ty.INT and type(value) is not int) or
                (ty == Ty.TEXT and type(value) is not str) or
                (ty == Ty.TOKENS and (type(value) is not tuple or
                   any(type(t) is not int for t in value)))):
            raise TypeError("runtime input type")
        if ty not in (Ty.INT, Ty.TEXT, Ty.TOKENS):
            raise TypeError("opaque external values not supported")
    for op in p.ops:
        args = tuple(env[x] for x in op.inputs)
        if op.kind == "const":
            value = dict(op.attrs)["value"]
        elif op.kind == "add":
            value = args[0] + args[1]
        else:
            value = effect(op, args)
            events.append((op.oid, op.kind, args, value))
        if op.output is not None:
            if ((op.out_ty == Ty.INT and type(value) is not int) or
                    (op.out_ty == Ty.TEXT and type(value) is not str) or
                    (op.out_ty == Ty.DOCS and (type(value) is not tuple or
                        any(type(d) is not str for d in value)))):
                raise TypeError("handler violated result contract")
            if op.out_ty == Ty.LOGITS:
                if (type(value) is not tuple or not value or
                    any(type(row) is not tuple or not row or
                        any(type(x) not in (int, float) or not math.isfinite(x)
                            for x in row) for row in value) or
                    len({len(row) for row in value}) != 1):
                    raise TypeError("finite rectangular logits required")
            env[op.output] = value
    return tuple(env[x] for x in p.outputs), tuple(events)


def expression_oracle(p, inputs):
    """Independent recursive arithmetic expansion, not sequential interpreter."""
    definitions = {o.output: o for o in p.ops if o.output is not None}
    def evaluate(name):
        if name in inputs:
            return inputs[name]
        op = definitions[name]
        if op.kind == "const":
            return dict(op.attrs)["value"]
        if op.kind == "add":
            return sum(evaluate(x) for x in op.inputs)
        raise ValueError("oracle accepts arithmetic output dependencies only")
    return tuple(evaluate(x) for x in p.outputs)


def lower(p, engines):
    verify(p)
    rt = chapter(39).Runtime(engines, chapter(39).Policy())
    schedule, producer, last_effect = [], {}, None
    for op in p.ops:
        a = dict(op.attrs)
        if op.kind == "engine":
            cap = chapter(39).Capability(a["capability"])
            backend = rt.route(cap, a["artifact"]).backend
        else:
            backend = {"retrieve": "retriever", "tool": "toolhost",
                       "mem_get": "memory", "mem_put": "memory"}.get(op.kind, "host")
        deps = {producer[x] for x in op.inputs if x in producer}
        if op.effects and last_effect is not None:
            deps.add(last_effect)
        schedule.append({"oid": op.oid, "backend": backend,
                         "dependencies": tuple(sorted(deps))})
        if op.effects:
            last_effect = op.oid
        if op.output is not None:
            producer[op.output] = op.oid
    return tuple(schedule)


class Effects:
    """Executable handlers for owned Ch39/40 and stable earlier engines."""
    def __init__(self, engines, owner, policy, memory=None):
        r = chapter(39)
        self.runtime = r.Runtime(engines, policy)
        self.owner, self.memory = owner, memory

    def __call__(self, op, args):
        a, r = dict(op.attrs), chapter(39)
        if op.kind == "engine":
            e = self.runtime.route(r.Capability(a["capability"]), a["artifact"])
            h = e.open(self.owner)
            try:
                return e.execute(h, self.owner, args[0]).data
            finally:
                e.close(h, self.owner)
        if op.kind == "retrieve":
            return tuple(d for d in a["corpus"] if a["query"].casefold() in d.casefold())
        if op.kind == "tool":
            if not self.runtime.policy.authorize(self.owner, a["name"]):
                raise PermissionError(a["name"])
            return (a["name"], args[0])  # local receipt, no external action
        if self.memory is None:
            raise RuntimeError("memory handler not configured")
        if op.kind == "mem_put":
            return self.memory.put_event(self.owner[0], args[0]).rid
        return self.memory.get(self.owner[0], args[0]).payload


def peak_live_values(p):
    """Peak includes allocation before dying inputs are released; counts, not bytes."""
    verify(p)
    uses = {x: 0 for x, _ in p.inputs}
    for op in p.ops:
        for x in op.inputs:
            uses[x] = uses.get(x, 0) + 1
        if op.output is not None:
            uses.setdefault(op.output, 0)
    live = {x for x, _ in p.inputs if uses[x] or x in p.outputs}
    peak = len(live)
    for op in p.ops:
        if op.output is not None:
            live.add(op.output)
        peak = max(peak, len(live))
        for x in op.inputs:
            uses[x] -= 1
            if not uses[x] and x not in p.outputs:
                live.discard(x)
        if op.output is not None and not uses[op.output] and op.output not in p.outputs:
            live.discard(op.output)
    return peak


def fixture():
    return Program((), (
        Op("c1", "const", (), "a", Ty.INT, (("value", 7),)),
        Op("c2", "const", (), "b", Ty.INT, (("value", 8),)),
        Op("sum", "add", ("a", "b"), "n", Ty.INT),
        Op("dead", "const", (), "unused", Ty.INT, (("value", 99),)),
        Op("ret", "retrieve", (), "docs", Ty.DOCS,
           (("version", "v1"), ("query", "memory"), ("corpus", ("genomic memory",))),
           EFFECTS["retrieve"]),
        Op("act", "tool", ("n",), None, None, (("name", "echo"),), EFFECTS["tool"])
    ), ("n",))


def results():
    p = fixture()
    stages = (p, constant_fold(p), dce(constant_fold(p)))
    rows = []
    for name, program in zip(("original", "folded", "DCE"), stages):
        output, events = interpret(program, {}, lambda op, args: args)
        rows.append({"stage": name, "operations": len(program.ops),
                     "peak": peak_live_values(program), "effects": len(events),
                     "answer": output[0]})
    return {"passes": rows, "schedule": lower(stages[-1], ())}


TABLES = [("passes", ["Stage", "Ops", "Peak values", "Effects", "Answer"],
           ["stage", "operations", "peak", "effects", "answer"], "lrrrr")]
PLOTS = []
LISTINGS = ["constant_fold", "dce", "expression_oracle", "lower", "peak_live_values"]
