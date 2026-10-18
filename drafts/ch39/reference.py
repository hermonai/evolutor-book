"""Typed serialized orchestration over actual Ch31 and Ch35 references.

Trusted in-process objects, local echo effects, no production authentication,
concurrent scheduling, persistent journal or learned task capability claim.
"""
from dataclasses import dataclass
from enum import Enum
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import uuid

import torch


def chapter(number):
    name = f"evod39_stable_{number}"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, Path(__file__).parents[1] / f"ch{number}/reference.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def owner_pair(owner):
    if (type(owner) is not tuple or len(owner) != 2 or
            any(type(x) is not str or not 1 <= len(x) <= 128 for x in owner)):
        raise ValueError("bounded tenant/request pair")


class Capability(str, Enum):
    COMPRESSED_STATE = "compressed_state"
    ADDRESSABLE_KV = "addressable_kv"


class Ty(str, Enum):
    INT = "int"
    TOKENS = "tokens"
    LOGITS = "logits"
    DOCS = "docs"
    RECEIPT = "receipt"


@dataclass(frozen=True)
class Value:
    ty: Ty
    data: object
    provenance: tuple = ()


@dataclass(frozen=True)
class Handle:
    adapter: str
    backend: str
    artifact: str
    owner: tuple
    serial: int


class EngineAdapter:
    def __init__(self, backend, model=None):
        if backend not in ("dogma", "hermon"):
            raise ValueError("known backend")
        self.backend = backend
        self.native = chapter(31 if backend == "dogma" else 35)
        self.model = self.native.tiny_model() if model is None else model
        self.artifact = self.native.artifact_id(self.model)
        self.capability = (Capability.COMPRESSED_STATE if backend == "dogma"
                           else Capability.ADDRESSABLE_KV)
        self.identity, self._next, self._states = uuid.uuid4().hex, 0, {}

    def open(self, owner):
        owner_pair(owner)
        if self.native.artifact_id(self.model) != self.artifact:
            raise ValueError("artifact changed")
        state = (self.native.construct(self.model, owner) if self.backend == "dogma"
                 else self.native.empty(self.model, owner))
        h = Handle(self.identity, self.backend, self.artifact, owner, self._next)
        self._next += 1
        self._states[h.serial] = (h, state)
        return h

    def _check(self, handle, owner):
        owner_pair(owner)
        if not isinstance(handle, Handle) or type(handle.serial) is not int:
            raise RuntimeError("handle required")
        stored = self._states.get(handle.serial)
        if (handle.adapter != self.identity or handle.owner != owner or
                stored is None or stored[0] != handle):
            raise RuntimeError("stale, forged or foreign handle")
        return stored[1]

    @torch.no_grad()
    def execute(self, handle, owner, tokens):
        state = self._check(handle, owner)
        if (type(tokens) is not tuple or not tokens or len(tokens) > 512 or
                any(type(x) is not int for x in tokens)):
            raise ValueError("nonempty bounded concrete tokens")
        if self.backend == "dogma":
            candidate, outputs = self.native.ingest(self.model, state, tokens, owner)
            logits = torch.stack(outputs)
        else:
            logits, candidate = self.native.consume(self.model, state, owner, tokens)
        # Both native routines preflight and return fresh state before this commit.
        self._states[handle.serial] = (handle, candidate)
        return Value(Ty.LOGITS, tuple(tuple(x) for x in logits.tolist()),
                     (self.backend, self.artifact))

    def close(self, handle, owner):
        self._check(handle, owner)
        del self._states[handle.serial]  # cleanup remains possible after model mutation


@dataclass(frozen=True)
class Step:
    sid: str
    op: str
    inputs: tuple
    output: str
    out_ty: Ty
    payload: object = None
    capability: Capability | None = None


@dataclass(frozen=True)
class Plan:
    owner: tuple
    inputs: tuple  # ordered (name, Value) pairs
    steps: tuple
    outputs: tuple


def check_value(value):
    if not isinstance(value, Value) or not isinstance(value.ty, Ty):
        raise TypeError("typed value")
    if value.ty == Ty.INT and type(value.data) is not int:
        raise TypeError("exact integer, excluding bool")
    if value.ty == Ty.TOKENS and (type(value.data) is not tuple or
            not 1 <= len(value.data) <= 512 or
            any(type(x) is not int for x in value.data)):
        raise TypeError("concrete tokens")
    if value.ty not in (Ty.INT, Ty.TOKENS):
        raise TypeError("only integer/token external inputs supported")


def validate(plan):
    owner_pair(plan.owner)
    if type(plan.steps) is not tuple or not 1 <= len(plan.steps) <= 128:
        raise ValueError("bounded nonempty plan")
    env, ids = {}, set()
    for name, value in plan.inputs:
        check_value(value)
        if not name or name in env:
            raise ValueError("unique input names")
        env[name] = value.ty
    for s in plan.steps:
        if (not isinstance(s, Step) or not s.sid or s.sid in ids or
                not s.output or s.output in env or type(s.inputs) is not tuple):
            raise ValueError("unique step/output and tuple edges")
        if any(x not in env for x in s.inputs):
            raise ValueError("undefined or forward input")
        types = tuple(env[x] for x in s.inputs)
        if s.op == "engine":
            if (types != (Ty.TOKENS,) or s.out_ty != Ty.LOGITS or
                    not isinstance(s.capability, Capability) or
                    type(s.payload) is not str or len(s.payload) != 64):
                raise TypeError("engine token/logit/capability/artifact contract")
        elif s.op == "retrieve":
            if (types or s.out_ty != Ty.DOCS or type(s.payload) is not tuple or
                    len(s.payload) != 3):
                raise TypeError("(version, query, corpus) retrieval")
            version, query, corpus = s.payload
            if (type(version) is not str or not version or type(query) is not str or
                    not query or type(corpus) is not tuple or
                    any(type(x) is not str for x in corpus)):
                raise TypeError("immutable versioned retrieval fixture")
        elif s.op == "symbolic":
            if types != (Ty.INT, Ty.INT) or s.out_ty != Ty.INT:
                raise TypeError("exact addition")
        elif s.op == "tool":
            if (types != (Ty.INT,) or s.out_ty != Ty.RECEIPT or
                    type(s.payload) is not str or not s.payload):
                raise TypeError("named tool over an integer")
        else:
            raise ValueError("unknown operation")
        ids.add(s.sid)
        env[s.output] = s.out_ty
    if not plan.outputs or any(x not in env for x in plan.outputs):
        raise ValueError("defined program outputs required")
    return env


class Trace:
    def __init__(self, fail_at=None):
        self.events, self.fail_at = (), fail_at

    def emit(self, kind, **data):
        if len(self.events) == self.fail_at:
            raise OSError("injected trace sink failure")
        body = {"seq": len(self.events), "kind": kind, "data": data,
                "previous": self.events[-1][1] if self.events else "0" * 64}
        encoded = json.dumps(body, sort_keys=True, separators=(",", ":"))
        self.events += ((encoded, digest(body)),)


class Policy:
    def __init__(self, grants=()):
        self.grants = frozenset(grants)  # (tenant, tool), configured by caller

    def authorize(self, owner, tool):
        return (owner[0], tool) in self.grants


class Runtime:
    def __init__(self, engines, policy, tool=None, trace=None):
        self.engines, self.policy = tuple(engines), policy
        self.trace = Trace() if trace is None else trace
        self.tool = (lambda name, value: (name, value)) if tool is None else tool

    def route(self, capability, artifact):
        matches = [e for e in self.engines if e.capability == capability
                   and e.artifact == artifact]
        if len(matches) != 1:
            raise RuntimeError("route must resolve uniquely with exact artifact")
        return matches[0]

    def execute(self, plan):
        validate(plan)  # reject the whole malformed graph before any effect
        routes = {s.sid: self.route(s.capability, s.payload)
                  for s in plan.steps if s.op == "engine"}
        env = dict(plan.inputs)
        self.trace.emit("plan_start", owner=plan.owner)
        for s in plan.steps:
            args = [env[x].data for x in s.inputs]
            self.trace.emit("step_start", sid=s.sid, op=s.op)
            if s.op == "engine":
                e = routes[s.sid]
                self.trace.emit("route", sid=s.sid, backend=e.backend,
                                artifact=e.artifact)
                h = e.open(plan.owner)
                try:
                    value = e.execute(h, plan.owner, args[0])
                    self.trace.emit("engine_result", sid=s.sid,
                                    result=digest(value.data))
                finally:
                    e.close(h, plan.owner)
            elif s.op == "retrieve":
                version, query, corpus = s.payload
                hits = tuple((i, doc) for i, doc in enumerate(corpus)
                             if query.casefold() in doc.casefold())
                value = Value(Ty.DOCS, hits, (version, query))
            elif s.op == "symbolic":
                value = Value(Ty.INT, args[0] + args[1], (s.sid, "exact-add"))
            else:
                # Intent must be recorded before policy/callback. A receipt failure
                # after the callback gives an uncertain effect, not a safe retry.
                self.trace.emit("tool_intent", sid=s.sid, name=s.payload)
                if not self.policy.authorize(plan.owner, s.payload):
                    self.trace.emit("tool_denied", sid=s.sid)
                    raise PermissionError(s.payload)
                receipt = self.tool(s.payload, args[0])
                value = Value(Ty.RECEIPT, receipt, (s.sid, "policy-checked"))
            env[s.output] = value
            self.trace.emit("step_result", sid=s.sid, result=digest(value.data))
        self.trace.emit("plan_complete", outputs=plan.outputs)
        return tuple(env[x] for x in plan.outputs)


def fixture():
    engines = (EngineAdapter("dogma"), EngineAdapter("hermon"))
    plan = Plan(("tenant-a", "request-39"),
        (("t", Value(Ty.TOKENS, (1, 2, 1))),
         ("a", Value(Ty.INT, 7)), ("b", Value(Ty.INT, 8))), (
        Step("ret", "retrieve", (), "docs", Ty.DOCS,
             ("corpus-v1", "memory", ("genomic memory", "attention cache"))),
        Step("d", "engine", ("t",), "dz", Ty.LOGITS,
             engines[0].artifact, Capability.COMPRESSED_STATE),
        Step("h", "engine", ("t",), "hz", Ty.LOGITS,
             engines[1].artifact, Capability.ADDRESSABLE_KV),
        Step("sum", "symbolic", ("a", "b"), "n", Ty.INT),
        Step("act", "tool", ("n",), "receipt", Ty.RECEIPT, "echo")),
        ("docs", "dz", "hz", "n", "receipt"))
    return engines, plan


def results():
    engines, plan = fixture()
    rt = Runtime(engines, Policy((("tenant-a", "echo"),)))
    out = rt.execute(plan)
    return {"trace": [{"step": s.sid, "operation": s.op,
             "type": v.ty.value, "items": len(v.data) if type(v.data) is tuple else 1}
             for s, v in zip(plan.steps, out)],
            "sum": out[3].data, "events": len(rt.trace.events),
            "native_state_leaks": sum(len(e._states) for e in engines)}


TABLES = [("trace", ["Step", "Operation", "Type", "Rows/items"],
           ["step", "operation", "type", "items"], "lllr")]
PLOTS = []
LISTINGS = ["EngineAdapter.execute", "Runtime.route", "Runtime.execute"]
