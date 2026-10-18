"""Serialized ownership/migration specification, not a distributed implementation."""
from dataclasses import dataclass, replace
import hashlib
import math


@dataclass(frozen=True)
class Worker:
    wid: str
    zone: str
    backend: str
    capacity: int
    artifacts: frozenset = frozenset({"m"})
    tenants: frozenset = frozenset({"A", "B"})
    schema: int = 1
    queue_ms: float = 0


@dataclass(frozen=True)
class StateHandle:
    sid: int
    tenant: str
    artifact: str
    schema: int
    backend: str
    owner: str
    epoch: int


@dataclass
class State:
    handle: StateHandle
    payload: bytes
    status: str = "active"


@dataclass(frozen=True)
class Transfer:
    handle: StateHandle
    dst: str
    payload: bytes
    sha256: str


class Cluster:
    def __init__(self, workers):
        self.workers = {w.wid: w for w in workers}
        if len(self.workers) != len(workers):
            raise ValueError("unique workers")
        for w in workers:
            if (type(w.capacity) is not int or w.capacity < 1
                    or type(w.schema) is not int or w.schema < 1
                    or not math.isfinite(w.queue_ms) or w.queue_ms < 0):
                raise ValueError("worker contract")
        self.alive = set(self.workers)
        self.used = {w.wid: 0 for w in workers}
        self.reserved = {w.wid: 0 for w in workers}
        self.states, self.pending, self.events, self.pd = {}, {}, [], {}

    def emit(self, kind, h, dst=None):
        self.events.append(dict(seq=len(self.events), kind=kind, sid=h.sid,
                                tenant=h.tenant, artifact=h.artifact,
                                owner=h.owner, epoch=h.epoch, dst=dst))

    def eligible(self, w, tenant, artifact, schema, backend):
        return (w.wid in self.alive and w.backend == backend
                and w.schema == schema and tenant in w.tenants
                and artifact in w.artifacts
                and self.used[w.wid] + self.reserved[w.wid] < w.capacity)

    def place(self, tenant, artifact, schema, backend, prefer_zone=None):
        ws = [w for w in self.workers.values()
              if self.eligible(w, tenant, artifact, schema, backend)]
        if not ws:
            raise RuntimeError("empty feasible set")
        # Zone penalty is a declared synthetic estimate in milliseconds.
        return min(ws, key=lambda w: (w.queue_ms +
                   (10 if prefer_zone and w.zone != prefer_zone else 0),
                   self.used[w.wid] / w.capacity, w.wid)).wid

    def create(self, tenant, artifact, backend, payload, zone=None, schema=1):
        if type(payload) is not bytes or len(payload) > 1_000_000:
            raise ValueError("bounded byte snapshot")
        owner = self.place(tenant, artifact, schema, backend, zone)
        h = StateHandle(len(self.states), tenant, artifact, schema, backend, owner, 0)
        self.states[h.sid] = State(h, payload)
        self.used[owner] += 1
        self.emit("create", h)
        return h

    def current(self, h, *, live=True):
        s = self.states[h.sid]
        if s.handle != h or s.status == "cancelled":
            raise RuntimeError("stale/foreign/cancelled handle")
        if live and h.owner not in self.alive:
            raise RuntimeError("owner unavailable")
        return s

    def read(self, h):
        return self.current(h).payload

    def write(self, h, payload):
        s = self.current(h)
        if s.status != "active" or type(payload) is not bytes:
            raise RuntimeError("frozen/non-byte state")
        s.payload = payload

    def prepare(self, h, dst):
        s = self.current(h)
        if s.status != "active" or dst == h.owner or dst not in self.workers:
            raise RuntimeError("invalid prepare")
        w = self.workers[dst]
        if not self.eligible(w, h.tenant, h.artifact, h.schema, h.backend):
            raise RuntimeError("incompatible/full destination")
        t = Transfer(h, dst, s.payload, hashlib.sha256(s.payload).hexdigest())
        self.reserved[dst] += 1
        s.status = "frozen"
        self.pending[h.sid] = t
        self.emit("prepare", h, dst)
        return t

    def abort(self, t):
        if self.pending.get(t.handle.sid) is not t:
            raise RuntimeError("unissued transfer")
        del self.pending[t.handle.sid]
        self.reserved[t.dst] -= 1
        s = self.states[t.handle.sid]
        if s.status != "cancelled":
            s.status = "active"
        self.emit("abort", t.handle, t.dst)

    def commit(self, t, received):
        if self.pending.get(t.handle.sid) is not t:
            raise RuntimeError("unissued/settled transfer")
        s = self.current(t.handle)
        if s.status != "frozen" or t.dst not in self.alive:
            raise RuntimeError("not commit-ready")
        if type(received) is not bytes or hashlib.sha256(received).hexdigest() != t.sha256:
            raise RuntimeError("transfer integrity")
        # One serialized authority transition is the specification's linearization point.
        h = replace(t.handle, owner=t.dst, epoch=t.handle.epoch + 1)
        s.handle, s.payload, s.status = h, received, "active"
        del self.pending[h.sid]
        self.reserved[t.dst] -= 1
        self.used[t.handle.owner] -= 1
        self.used[t.dst] += 1
        self.emit("commit", h, t.dst)
        return h

    def cancel(self, h):
        s = self.current(h, live=False)
        if h.sid in self.pending:
            self.abort(self.pending[h.sid])
        s.status = "cancelled"
        self.used[h.owner] -= 1
        s.handle = replace(h, epoch=h.epoch + 1)
        self.emit("cancel", s.handle)

    def fail(self, wid):
        self.alive.discard(wid)

    def recover(self, h, dst, replayed, expected_digest):
        s = self.current(h, live=False)
        if h.owner in self.alive or s.status != "active":
            raise RuntimeError("failed active owner required")
        if dst not in self.workers or not self.eligible(
                self.workers[dst], h.tenant, h.artifact, h.schema, h.backend):
            raise RuntimeError("incompatible recovery destination")
        if type(replayed) is not bytes or hashlib.sha256(replayed).hexdigest() != expected_digest:
            raise RuntimeError("trusted replay evidence mismatch")
        nh = replace(h, owner=dst, epoch=h.epoch + 1)
        s.handle, s.payload = nh, replayed
        self.used[h.owner] -= 1
        self.used[dst] += 1
        self.emit("recover", nh)
        return nh

    def check(self):
        for wid, w in self.workers.items():
            owners = sum(s.status != "cancelled" and s.handle.owner == wid
                         for s in self.states.values())
            copies = sum(t.dst == wid for t in self.pending.values())
            copies += sum(pair.count(wid) for pair in self.pd.values())
            assert owners == self.used[wid] and copies == self.reserved[wid]
            assert 0 <= owners + copies <= w.capacity


def pd_reserve(cluster, tenant, artifact, zone=None):
    # No mutation until both constrained pools can reserve a slot.
    p = cluster.place(tenant, artifact, 1, "prefill", zone)
    d = cluster.place(tenant, artifact, 1, "decode", zone)
    cluster.reserved[p] += 1
    cluster.reserved[d] += 1
    pair = (p, d)
    ticket = object()
    cluster.pd[ticket] = pair
    return ticket, pair


def pd_release(cluster, ticket):
    if ticket not in cluster.pd:
        raise RuntimeError("unissued/settled downstream reservation")
    for wid in cluster.pd.pop(ticket):
        cluster.reserved[wid] -= 1


def transfer_ms(nbytes, bandwidth_bytes_s, fixed_ms=0):
    if (type(nbytes) is not int or nbytes < 0 or
            not math.isfinite(bandwidth_bytes_s) or bandwidth_bytes_s <= 0
            or not math.isfinite(fixed_ms) or fixed_ms < 0):
        raise ValueError("bytes, positive bandwidth and nonnegative fixed cost")
    return fixed_ms + 1000 * nbytes / bandwidth_bytes_s


def results():
    c = Cluster([Worker("a", "z1", "dogma", 2), Worker("b", "z2", "dogma", 2)])
    h = c.create("A", "m", "dogma", b"snapshot", "z1")
    t = c.prepare(h, "b")
    n = c.commit(t, t.payload)
    c.check()
    return dict(owner=n.owner, epoch=n.epoch,
                transfer=[dict(kind=k, nbytes=b, ms=transfer_ms(b, 1e9, .1))
                          for k, b in (("Native", 8192), ("KV", 402653184))],
                source="synthetic ownership and payload model")


TABLES = [("transfer", ["Payload", "Bytes", "Model ms"],
           ["kind", "nbytes", "ms"], "lrr")]
PLOTS = []
LISTINGS = ["Cluster.eligible", "Cluster.prepare", "Cluster.commit",
            "Cluster.recover", "pd_reserve"]
