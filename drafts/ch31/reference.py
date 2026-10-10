"""Restricted input-gated diagonal recurrence; not full DOGMA implementation parity."""

from dataclasses import dataclass
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import torch


def tensor(value, shape):
    if (
        not isinstance(value, torch.Tensor)
        or tuple(value.shape) != shape
        or value.dtype != torch.float64
        or value.device.type != "cpu"
        or not torch.isfinite(value).all()
    ):
        raise ValueError("finite CPU float64 tensor with declared shape required")


def identity(value):
    if not isinstance(value, str) or not value or len(value) > 128:
        raise ValueError("bounded nonempty identity")


@dataclass(frozen=True)
class Model:
    vocabulary: tuple
    embedding: torch.Tensor
    retention: torch.Tensor
    write: torch.Tensor
    head: torch.Tensor


def artifact_id(model):
    if not isinstance(model, Model):
        raise ValueError("model required")
    vocab = model.vocabulary
    if (
        not isinstance(vocab, tuple)
        or len(vocab) < 2
        or len(set(vocab)) != len(vocab)
        or any(not isinstance(v, str) or not v for v in vocab)
    ):
        raise ValueError("ordered unique vocabulary required")
    if model.embedding.ndim != 2:
        raise ValueError("embedding rank")
    v, d = model.embedding.shape
    if v != len(vocab) or d < 1:
        raise ValueError("embedding vocabulary/width")
    tensor(model.embedding, (v, d))
    tensor(model.retention, (d,))
    tensor(model.write, (d,))
    tensor(model.head, (d, v))
    if not ((model.retention >= 0) & (model.retention < 1)).all():
        raise ValueError("0 <= retention < 1")
    payload = {
        "schema": "evod31-input-gated-diagonal-v1",
        "dtype": "float64",
        "device": "cpu",
        "vocabulary": vocab,
        "parameters": [
            p.detach().tolist()
            for p in (model.embedding, model.retention, model.write, model.head)
        ],
    }
    return hashlib.sha256(
        json.dumps(
            payload, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
    ).hexdigest()


@dataclass(frozen=True)
class State:
    owner: tuple
    artifact: str
    position: int
    hidden: torch.Tensor


def construct(model, owner):
    if not isinstance(owner, tuple) or len(owner) != 2:
        raise ValueError("tenant/request pair")
    for value in owner:
        identity(value)
    digest = artifact_id(model)
    return State(
        owner, digest, 0, torch.zeros(model.embedding.shape[1], dtype=torch.float64)
    )


def validate(model, state, owner):
    if not isinstance(state, State) or state.owner != owner:
        raise ValueError("foreign state")
    if not isinstance(owner, tuple) or len(owner) != 2:
        raise ValueError("tenant/request pair")
    for value in owner:
        identity(value)
    if type(state.position) is not int or state.position < 0:
        raise ValueError("nonnegative integer position")
    if state.artifact != artifact_id(model):
        raise ValueError("artifact mismatch, including in-place parameter changes")
    tensor(state.hidden, (model.embedding.shape[1],))


@dataclass(frozen=True)
class Result:
    state: State
    logits: torch.Tensor


def native_step(model, state, token, owner):
    validate(model, state, owner)
    if type(token) is not int or not 0 <= token < len(model.vocabulary):
        raise ValueError("integer token in vocabulary")
    e = model.embedding[token]
    hidden = model.retention * state.hidden + torch.sigmoid(model.write * e) * e
    logits = hidden @ model.head
    tensor(hidden, tuple(state.hidden.shape))
    tensor(logits, (len(model.vocabulary),))
    return Result(State(owner, state.artifact, state.position + 1, hidden), logits)


def ingest(model, state, tokens, owner, valid=None):
    """Preflight complete chunk; padding rows do not consume tokens or advance position."""
    validate(model, state, owner)
    tokens = tuple(tokens)
    valid = (True,) * len(tokens) if valid is None else tuple(valid)
    if (
        len(tokens) > 10000
        or len(tokens) != len(valid)
        or any(type(v) is not bool for v in valid)
    ):
        raise ValueError("bounded chunk with boolean mask")
    for token, live in zip(tokens, valid):
        if live and (type(token) is not int or not 0 <= token < len(model.vocabulary)):
            raise ValueError("invalid live token")
    outputs = []
    for token, live in zip(tokens, valid):
        if live:
            result = native_step(model, state, token, owner)
            state = result.state
            outputs.append(result.logits)
        else:
            outputs.append(torch.zeros(len(model.vocabulary), dtype=torch.float64))
    return state, tuple(outputs)


def scalar_closed_form(model, tokens, initial=None):
    """Independent scalar expansion, not repeated native_step calls."""
    artifact_id(model)
    e = model.embedding.detach().tolist()
    a, w, head = (
        p.detach().tolist() for p in (model.retention, model.write, model.head)
    )
    initial = [0.0] * len(a) if initial is None else initial
    t = len(tokens)
    h = []
    import math

    for j in range(len(a)):
        value = a[j] ** t * initial[j]
        for k, token in enumerate(tokens):
            x = w[j] * e[token][j]
            gate = 1 / (1 + math.exp(-x)) if x >= 0 else math.exp(x) / (1 + math.exp(x))
            value += a[j] ** (t - 1 - k) * gate * e[token][j]
        h.append(value)
    return h, [
        sum(h[j] * head[j][k] for j in range(len(a))) for k in range(len(head[0]))
    ]


def runtime_module():
    name = "evod31_ch30_runtime"
    if name not in sys.modules:
        path = Path(__file__).resolve().parent.parent / "ch30/reference.py"
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def state_stamp(state):
    return (
        state.owner,
        state.artifact,
        state.position,
        tuple(state.hidden.detach().tolist()),
    )


@dataclass(frozen=True)
class Pending:
    ticket: object
    before: tuple
    candidate: Result
    token: int
    after: tuple
    logits: tuple


class Session:
    """Serialized in-process adapter; trusted objects, not authentication or crash durability."""

    def __init__(self, model, result, owner, runtime):
        self.model, self.result, self.owner, self.runtime = (
            model,
            result,
            owner,
            runtime,
        )
        self.pending = None
        self._validate()
        if runtime.revision != 0:
            raise ValueError("new session requires zero decode revision")
        if result.state.position == 0:
            raise ValueError("consume a prompt or explicit BOS before decode")
        if runtime.phase != runtime_module().Phase.ACTIVE:
            raise ValueError("active allocated shell required")
        runtime.registry.validate(runtime.lease)
        self.prompt_position = result.state.position

    def _validate(self):
        validate(self.model, self.result.state, self.owner)
        tensor(self.result.logits, (len(self.model.vocabulary),))
        if not torch.equal(
            self.result.logits, self.result.state.hidden @ self.model.head
        ):
            raise ValueError("logits not bound to current state")
        if (self.runtime.req.tenant_id, self.runtime.req.request_id) != self.owner:
            raise ValueError("shell owner mismatch")
        if self.runtime.req.model_id != self.result.state.artifact:
            raise ValueError("shell artifact mismatch")

    def prepare(self, now):
        self._validate()
        if self.pending is not None:
            raise RuntimeError("one staged step")
        if self.result.state.position != self.prompt_position + self.runtime.revision:
            raise ValueError("native/shell revision mismatch")
        ticket = self.runtime.launch(now)
        if ticket is None:
            return None
        try:
            token = int(torch.argmax(self.result.logits))
            candidate = native_step(self.model, self.result.state, token, self.owner)
        except Exception:
            self.runtime.commit(ticket, "", now)
            raise
        self.pending = Pending(
            ticket,
            state_stamp(self.result.state),
            candidate,
            token,
            state_stamp(candidate.state),
            tuple(candidate.logits.detach().tolist()),
        )
        return self.pending

    def finish(self, pending, now):
        if pending is not self.pending or pending is None:
            raise RuntimeError("foreign or duplicate staged completion")
        try:
            self._validate()
            if state_stamp(self.result.state) != pending.before:
                raise ValueError("native state changed while work was pending")
            validate(self.model, pending.candidate.state, self.owner)
            if (
                state_stamp(pending.candidate.state) != pending.after
                or tuple(pending.candidate.logits.detach().tolist()) != pending.logits
            ):
                raise ValueError("staged candidate was mutated")
            if pending.candidate.state.position != self.result.state.position + 1:
                raise ValueError("candidate position")
            if not torch.equal(
                pending.candidate.logits,
                pending.candidate.state.hidden @ self.model.head,
            ):
                raise ValueError("candidate logits")
        except Exception:
            self.runtime.commit(pending.ticket, "", now)
            self.pending = None
            raise
        accepted = self.runtime.commit(
            pending.ticket, self.model.vocabulary[pending.token], now
        )
        self.pending = None
        if accepted:
            self.result = pending.candidate
        return accepted


def tiny_model():
    return Model(
        ("0", "1", "2"),
        torch.tensor([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]], dtype=torch.float64),
        torch.tensor([0.5, 0.25], dtype=torch.float64),
        torch.zeros(2, dtype=torch.float64),
        torch.tensor([[0.0, 1.0, -1.0], [0.0, -1.0, 1.0]], dtype=torch.float64),
    )


TABLES = [
    (
        "trace",
        ["Position", "Token", "$h_1$", "$h_2$", "$z_1$", "$z_2$"],
        ["position", "token", "h1", "h2", "z1", "z2"],
        "rrrrrr",
    )
]
PLOTS = []
LISTINGS = [
    "artifact_id",
    "native_step",
    "ingest",
    "scalar_closed_form",
    "Session.finish",
]


def results():
    model, owner = tiny_model(), ("tenant-a", "request-a")
    state = construct(model, owner)
    trace = []
    for token in [1, 2, 1]:
        result = native_step(model, state, token, owner)
        state = result.state
        trace.append(
            {
                "position": state.position,
                "token": token,
                "h1": float(state.hidden[0]),
                "h2": float(state.hidden[1]),
                "z1": float(result.logits[1]),
                "z2": float(result.logits[2]),
            }
        )
    h, z = scalar_closed_form(model, [1, 2, 1])
    return {
        "trace": trace,
        "artifact": artifact_id(model),
        "oracle_hidden": h,
        "oracle_logits": z,
        "next_token": int(torch.argmax(result.logits)),
    }
