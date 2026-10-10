"""Serialized inference-pool oracle; not GPU concurrency, authentication or secure erase."""

from dataclasses import dataclass, field
import importlib.util
from pathlib import Path
import sys
import math
import re
import uuid


def integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError("integer domain")
    return value


def owner_pair(owner):
    if (
        not isinstance(owner, tuple)
        or len(owner) != 2
        or any(not isinstance(x, str) or not x or len(x) > 128 for x in owner)
    ):
        raise ValueError("tenant/request pair")
    return owner


def values_copy(values, width):
    values = tuple(values)
    if len(values) != width or any(
        type(x) not in (float, int) or not math.isfinite(x) for x in values
    ):
        raise ValueError("finite declared-width payload")
    return tuple(float(x) for x in values)


@dataclass(frozen=True)
class Handle:
    pool: str
    slot: int
    generation: int
    owner: tuple
    artifact: str


@dataclass(frozen=True)
class Snapshot:
    position: int
    hidden: tuple


@dataclass(frozen=True)
class Pin:
    handle: Handle
    serial: int
    version: int
    snapshot: Snapshot


@dataclass
class Slot:
    generation: int = 0
    owner: tuple | None = None
    payload: Snapshot | None = None
    version: int = 0
    retiring: bool = False
    pins: dict = field(default_factory=dict)


class Pool:
    def __init__(self, name, capacity, width, artifact):
        if not isinstance(name, str) or not name:
            raise ValueError("pool display name")
        integer(capacity, 1)
        integer(width, 1)
        if not isinstance(artifact, str) or not re.fullmatch("[0-9a-f]{64}", artifact):
            raise ValueError("artifact digest")
        self.name, self.capacity, self.width, self.artifact = (
            name,
            capacity,
            width,
            artifact,
        )
        self.identity = uuid.uuid4().hex
        self._slots = [
            Slot(payload=Snapshot(0, (0.0,) * width)) for _ in range(capacity)
        ]
        self._serial = 0

    def _slot(self, handle, owner, allow_retiring=False):
        owner_pair(owner)
        if (
            not isinstance(handle, Handle)
            or handle.pool != self.identity
            or type(handle.slot) is not int
            or not 0 <= handle.slot < self.capacity
        ):
            raise RuntimeError("foreign handle")
        slot = self._slots[handle.slot]
        if type(handle.generation) is not int or slot.generation != handle.generation:
            raise RuntimeError("stale generation")
        if (
            slot.owner != owner
            or handle.owner != owner
            or handle.artifact != self.artifact
        ):
            raise PermissionError("owner/artifact mismatch")
        if slot.retiring and not allow_retiring:
            raise RuntimeError("state is retiring")
        return slot

    def _snapshot(self, snapshot):
        if not isinstance(snapshot, Snapshot):
            raise ValueError("snapshot required")
        integer(snapshot.position)
        return Snapshot(snapshot.position, values_copy(snapshot.hidden, self.width))

    def allocate(self, owner, initial=None):
        owner_pair(owner)
        payload = (
            self._snapshot(initial)
            if initial is not None
            else Snapshot(0, (0.0,) * self.width)
        )
        for index, slot in enumerate(self._slots):
            if slot.owner is None:
                slot.payload, slot.owner, slot.version = payload, owner, 0
                slot.retiring = False
                return Handle(
                    self.identity, index, slot.generation, owner, self.artifact
                )
        raise MemoryError("exhausted, including retiring pinned slots")

    def read(self, handle, owner):
        return self._snapshot(self._slot(handle, owner).payload)

    def write(self, handle, owner, snapshot):
        slot = self._slot(handle, owner)
        payload = self._snapshot(snapshot)
        if slot.pins:
            raise RuntimeError("use version-fenced completion while pinned")
        slot.payload = payload
        slot.version += 1

    def pin(self, handle, owner):
        slot = self._slot(handle, owner)
        self._serial += 1
        pin = Pin(handle, self._serial, slot.version, self._snapshot(slot.payload))
        slot.pins[pin.serial] = pin
        return pin

    def complete(self, pin, owner, candidate=None):
        if not isinstance(pin, Pin):
            raise RuntimeError("pin required")
        slot = self._slot(pin.handle, owner, allow_retiring=True)
        if slot.pins.get(pin.serial) is not pin:
            raise RuntimeError("stale or duplicate completion")
        payload = None if candidate is None else self._snapshot(candidate)
        accepted = (
            payload is not None and not slot.retiring and slot.version == pin.version
        )
        if accepted and payload.position != pin.snapshot.position + 1:
            raise ValueError("candidate must consume one live token")
        del slot.pins[pin.serial]
        if accepted:
            slot.payload = payload
            slot.version += 1
        if slot.retiring and not slot.pins:
            self._scrub(slot)
        return accepted

    def _scrub(self, slot):
        if slot.pins:
            raise RuntimeError("cannot scrub in-flight storage")
        slot.payload = Snapshot(0, (0.0,) * self.width)
        slot.owner, slot.retiring, slot.version = None, False, 0
        slot.generation += 1

    def release(self, handle, owner):
        slot = self._slot(handle, owner)
        slot.retiring = True
        if not slot.pins:
            self._scrub(slot)

    def clone(self, handle, owner, new_owner):
        owner_pair(new_owner)
        source = self.read(handle, owner)
        if new_owner[0] != owner[0]:
            raise PermissionError("cross-tenant export policy not provided")
        return self.allocate(new_owner, source)

    def stats(self):
        free = sum(s.owner is None for s in self._slots)
        retiring = sum(s.retiring for s in self._slots)
        return {
            "capacity": self.capacity,
            "free": free,
            "owned": self.capacity - free - retiring,
            "retiring": retiring,
            "pins": sum(len(s.pins) for s in self._slots),
            "payload_bytes": self.capacity * self.width * 8,
        }


class Workspace:
    def __init__(self, width):
        integer(width, 1)
        self._values = (0.0,) * width
        self.closed = False

    def use(self, values):
        if self.closed:
            raise RuntimeError("workspace closed")
        self._values = values_copy(values, len(self._values))
        return tuple(self._values)

    def close(self):
        self._values = (0.0,) * len(self._values)
        self.closed = True


def native_module():
    name = "evod32_ch31_native"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, Path(__file__).parent.parent / "ch31/reference.py"
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def to_native(pool, handle, owner):
    """Fresh inference tensor; no writable alias and no training graph."""
    native = native_module()
    snap = pool.read(handle, owner)
    return native.State(
        owner,
        pool.artifact,
        snap.position,
        native.torch.tensor(snap.hidden, dtype=native.torch.float64),
    )


def from_native(pool, handle, owner, model, state):
    native = native_module()
    native.validate(model, state, owner)
    if state.artifact != pool.artifact:
        raise ValueError("pool/native artifact mismatch")
    pool.write(
        handle, owner, Snapshot(state.position, tuple(state.hidden.detach().tolist()))
    )


TABLES = [
    (
        "timeline",
        ["Event", "Free", "Owned", "Retiring", "Pins"],
        ["event", "free", "owned", "retiring", "pins"],
        "lrrrr",
    )
]
PLOTS = []
LISTINGS = ["Pool._slot", "Pool.allocate", "Pool.complete", "Pool.clone", "to_native"]


def results():
    p = Pool("teaching", 1, 2, "a" * 64)
    owner = ("tenant-a", "r1")
    rows = []

    def record(event):
        rows.append({"event": event, **p.stats()})

    record("initial")
    h = p.allocate(owner, Snapshot(3, (1.0, 2.0)))
    record("allocate")
    pin = p.pin(h, owner)
    record("pin")
    p.release(h, owner)
    record("release")
    accepted = p.complete(pin, owner, Snapshot(4, (3.0, 4.0)))
    record("late result")
    fresh = p.allocate(("tenant-b", "r2"))
    record("reuse")
    return {
        "timeline": rows,
        "late_accepted": accepted,
        "fresh_zero": p.read(fresh, fresh.owner).hidden,
        "generations": [h.generation, fresh.generation],
    }
