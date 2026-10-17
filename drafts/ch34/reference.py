"""Inference-only row lift of the actual Ch31 recurrence through Ch32/33 ownership.

Serialized trusted callers; no device kernel, concurrent transaction or shell
output publication. Pins fence lane completion; cancellation retires storage.
"""

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys

import torch


def checkpoint_module():
    name = "evod34_actual_checkpoints"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, Path(__file__).parent.parent / "ch33/reference.py"
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def pool_module():
    return checkpoint_module().pool_module()


def native_module():
    return pool_module().native_module()


@torch.no_grad()
def batched_step(model, hidden, tokens, active):
    """Only active lanes read token IDs; inactive state is an exact identity."""
    native = native_module()
    native.artifact_id(model)
    if hidden.ndim != 2 or not 1 <= hidden.shape[0] <= 256:
        raise ValueError("bounded nonempty [B,D] hidden")
    b, d = hidden.shape
    native.tensor(hidden, (b, model.embedding.shape[1]))
    if (
        type(tokens) not in (tuple, list)
        or type(active) not in (tuple, list)
        or len(tokens) != b
        or len(active) != b
        or any(type(x) is not bool for x in active)
    ):
        raise ValueError("matching concrete tokens and boolean activity")
    for token, live in zip(tokens, active):
        if live and (type(token) is not int or not 0 <= token < len(model.vocabulary)):
            raise ValueError("live token outside vocabulary")
    rows = [i for i, live in enumerate(active) if live]
    result = hidden.clone()
    logits = torch.zeros(b, len(model.vocabulary), dtype=torch.float64)
    if rows:
        e = model.embedding[[tokens[i] for i in rows]]
        candidate = model.retention * hidden[rows] + torch.sigmoid(model.write * e) * e
        z = candidate @ model.head
        native.tensor(candidate, (len(rows), d))
        native.tensor(z, (len(rows), len(model.vocabulary)))
        result[rows], logits[rows] = candidate, z
    return result, logits


@dataclass(frozen=True)
class Lane:
    handle: object
    owner: tuple
    token: object
    active: bool = True


@dataclass(frozen=True)
class Job:
    artifact: str
    lanes: tuple
    pins: tuple
    candidates: tuple
    logits: tuple


class Engine:
    def __init__(self, pool, model):
        self.pool, self.model = pool, model
        self._pending = {}
        self._context()

    def _context(self):
        if (
            native_module().artifact_id(self.model) != self.pool.artifact
            or self.model.embedding.shape[1] != self.pool.width
        ):
            raise ValueError("pool/model context mismatch")

    def prepare(self, lanes):
        """Preflight and compute before acquiring pins; serialized calls only."""
        self._context()
        if type(lanes) not in (tuple, list) or not 1 <= len(lanes) <= 256:
            raise ValueError("bounded nonempty lane group")
        slots, snapshots = set(), []
        for lane in lanes:
            if not isinstance(lane, Lane) or type(lane.active) is not bool:
                raise ValueError("lane contract")
            slot = self.pool._slot(lane.handle, lane.owner)
            if lane.handle.slot in slots:
                raise ValueError("duplicate slot, including inactive aliases")
            if slot.pins:
                raise RuntimeError("one in-flight batch per slot")
            slots.add(lane.handle.slot)
            snapshots.append(self.pool.read(lane.handle, lane.owner))
        hidden = torch.tensor([s.hidden for s in snapshots], dtype=torch.float64)
        h, z = batched_step(
            self.model, hidden, [x.token for x in lanes], [x.active for x in lanes]
        )
        p = pool_module()
        candidates = tuple(
            p.Snapshot(s.position + int(x.active), tuple(row.tolist()))
            for s, x, row in zip(snapshots, lanes, h)
        )
        pins = tuple(
            self.pool.pin(x.handle, x.owner) if x.active else None for x in lanes
        )
        job = Job(
            self.pool.artifact,
            tuple(lanes),
            pins,
            candidates,
            tuple(tuple(row.tolist()) for row in z),
        )
        self._pending[id(job)] = job
        return job

    def finish(self, job, discard=False):
        """Settle each lane once; only accepted lanes expose model logits."""
        if self._pending.get(id(job)) is not job or type(discard) is not bool:
            raise RuntimeError("foreign/duplicate completion or discard policy")
        try:
            self._context()
            context_ok = True
        except ValueError:
            context_ok = False
        accepted, published = [], []
        for lane, pin, candidate, logits in zip(
            job.lanes, job.pins, job.candidates, job.logits
        ):
            ok = (
                False
                if pin is None
                else self.pool.complete(
                    pin, lane.owner, candidate if context_ok and not discard else None
                )
            )
            accepted.append(ok)
            published.append(logits if ok else None)
        del self._pending[id(job)]
        if not context_ok:
            raise ValueError("model changed; all prepared pins discarded")
        return tuple(accepted), tuple(published)


class RoundRobin:
    """Scheduler over a caller's ready-list indices; no latency guarantee."""

    def __init__(self):
        self.next = 0

    def choose(self, ready, limit):
        if (
            type(ready) not in (tuple, list)
            or any(type(x) is not bool for x in ready)
            or type(limit) is not int
            or not 1 <= limit <= 256
        ):
            raise ValueError("boolean ready list and positive bounded limit")
        if not ready:
            return ()
        order = [(self.next + i) % len(ready) for i in range(len(ready))]
        selected = tuple(i for i in order if ready[i])[:limit]
        if selected:
            self.next = (selected[-1] + 1) % len(ready)
        return selected


def traffic(batch, width, vocabulary, element_bytes=8, fused=True, staged=True):
    """Logical payload model, excluding weights/metadata/cache lines/sigmoid cost."""
    for x in (batch, width, vocabulary, element_bytes):
        if type(x) is not int or x < 1:
            raise ValueError("positive integer geometry")
    if type(fused) is not bool or type(staged) is not bool:
        raise ValueError("boolean traffic policy")
    base = batch * (3 * width + vocabulary) * element_bytes
    intermediate = 0 if fused else 2 * batch * width * element_bytes
    staging = 4 * batch * width * element_bytes if staged else 0
    return {
        "batch": batch,
        "base": base,
        "intermediate": intermediate,
        "staging": staging,
        "total": base + intermediate + staging,
        "arithmetic": 2 * batch * width * vocabulary + 4 * batch * width,
    }


def results():
    p = pool_module()
    model = native_module().tiny_model()
    pool = p.Pool("batch", 3, 2, native_module().artifact_id(model))
    owners = tuple(("tenant-a", name) for name in ("A", "B", "C"))
    handles = tuple(pool.allocate(x) for x in owners)
    sequences, cursors, trace = ((1, 2, 1), (2,), (1, 1)), [0, 0, 0], []
    engine = Engine(pool, model)
    # Stable priority makes the incoming package's three-tick example explicit.
    while any(c < len(seq) for c, seq in zip(cursors, sequences)):
        selected = [i for i in range(3) if cursors[i] < len(sequences[i])][:2]
        job = engine.prepare(
            [Lane(handles[i], owners[i], sequences[i][cursors[i]]) for i in selected]
        )
        accepted, _ = engine.finish(job)
        for i, ok in zip(selected, accepted):
            cursors[i] += int(ok)
        trace.append(
            {
                "tick": len(trace) + 1,
                "members": ",".join(owners[i][1] for i in selected),
                "a": cursors[0],
                "b": cursors[1],
                "c": cursors[2],
            }
        )
    return {
        "trace": trace,
        "final_hidden": [list(pool.read(h, o).hidden) for h, o in zip(handles, owners)],
        "traffic": [
            dict(traffic(8, 64, 4, fused=f, staged=s), policy=name)
            for name, f, s in (
                ("resident fused", True, False),
                ("staged fused", True, True),
                ("staged unfused", False, True),
            )
        ],
    }


TABLES = [
    (
        "trace",
        ["Tick", "Members", "$t_A$", "$t_B$", "$t_C$"],
        ["tick", "members", "a", "b", "c"],
        "rlrrr",
    ),
    (
        "traffic",
        ["Policy", "Base B", "Stage B", "Temp B", "Total B"],
        ["policy", "base", "staging", "intermediate", "total"],
        "lrrrr",
    ),
]
PLOTS = []
LISTINGS = ["batched_step", "Engine.prepare", "Engine.finish", "RoundRobin.choose"]
