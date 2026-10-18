"""Serial deployment specification. No cluster, secret resolver or authenticator."""
from dataclasses import dataclass, field, asdict
import hashlib
import json
import math


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def text(value):
    if type(value) is not str or not 1 <= len(value) <= 128:
        raise ValueError("bounded identity")


@dataclass(frozen=True)
class Bundle:
    revision: str
    model: str
    runtime: str
    tokenizer: str
    config: str
    api: int = 1
    state_schema: int = 1
    policy_schema: int = 1
    backend: str = "cpu-f64"
    provenance: str = "fixture-builder"

    def digest(self):
        for k, v in asdict(self).items():
            if k in ("api", "state_schema", "policy_schema"):
                if type(v) is not int or v < 1:
                    raise ValueError("positive schema")
            else:
                text(v)
        return digest(asdict(self))


@dataclass(frozen=True)
class Contract:
    api: int = 1
    state_schema: int = 1
    policy_schema: int = 1
    backend: str = "cpu-f64"

    def accepts(self, bundle):
        return all(getattr(self, k) == getattr(bundle, k)
                   for k in asdict(self))


def verify_capsule(bundle, payloads, trusted_digest):
    """Data-only bounded capsule; trusted identity is independently supplied."""
    if bundle.digest() != trusted_digest:
        raise ValueError("release identity differs from trusted pin")
    roles = ("model", "runtime", "tokenizer", "config")
    if type(payloads) is not dict or set(payloads) != set(roles):
        raise ValueError("exact payload role set")
    for role in roles:
        blob = payloads[role]
        if type(blob) is not bytes or len(blob) > 1_000_000:
            raise ValueError("bounded immutable payload")
        if hashlib.sha256(blob).hexdigest() != getattr(bundle, role):
            raise ValueError("payload content mismatch")
    return trusted_digest


def nearest_rank(xs, q):
    if (not xs or type(q) not in (int, float)
            or not math.isfinite(q) or not 0 < q <= 1):
        raise ValueError("nonempty samples and 0 < q <= 1")
    if any(type(x) not in (float, int) or not math.isfinite(x) or x < 0
           for x in xs):
        raise ValueError("finite nonnegative duration")
    return sorted(xs)[math.ceil(q * len(xs)) - 1]


@dataclass(frozen=True)
class Gate:
    minimum: int = 20
    max_error: float = .01
    p95_ms: float = 500

    def passes(self, observations):
        if (type(self.minimum) is not int or self.minimum < 1
                or not math.isfinite(self.max_error)
                or not 0 <= self.max_error <= 1
                or not math.isfinite(self.p95_ms) or self.p95_ms < 0):
            raise ValueError("invalid evidence gate")
        if len(observations) < self.minimum:
            return False
        return (sum(not ok for _, ok in observations) / len(observations)
                <= self.max_error and
                nearest_rank([ms for ms, _ in observations], .95)
                <= self.p95_ms)


@dataclass
class Revision:
    bundle: Bundle
    state: str = "registered"
    ready: bool = False
    live: bool = True
    observations: list = field(default_factory=list)
    admitted: int = 0
    completed: int = 0


class Deployment:
    def __init__(self, capacity=4, contract=Contract(), gate=Gate()):
        if type(capacity) is not int or capacity < 1:
            raise ValueError("positive capacity")
        self.capacity, self.contract, self.gate = capacity, contract, gate
        self.revisions, self.jobs, self.done = {}, {}, set()
        self.active, self.previous = None, None
        self.events = []

    def emit(self, kind, revision, request=None):
        self.events.append(dict(seq=len(self.events), kind=kind,
                                revision=revision, request=request))

    def register(self, bundle, trusted_provenance):
        identity = bundle.digest()
        if (not self.contract.accepts(bundle)
                or type(trusted_provenance) is not bool or not trusted_provenance):
            raise ValueError("compatibility/provenance gate")
        if identity in self.revisions:
            raise ValueError("duplicate")
        self.revisions[identity] = Revision(bundle)
        self.emit("registered", identity)
        return identity

    def canary(self, d):
        r = self.revisions[d]
        if r.state != "registered":
            raise RuntimeError("registered revision required")
        r.state = "canary"
        self.emit("canary", d)

    def health(self, d, *, live, ready):
        r = self.revisions[d]
        if type(live) is not bool or type(ready) is not bool:
            raise ValueError("boolean health")
        if ready and (not live or r.state not in ("canary", "active")):
            raise RuntimeError("cannot become ready")
        r.live, r.ready = live, ready

    def admit(self, d, request):
        text(request)
        r = self.revisions[d]
        if request in self.jobs or request in self.done:
            raise RuntimeError("request identity already used")
        if not r.ready or not r.live or r.state not in ("canary", "active"):
            raise RuntimeError("admission closed")
        if len(self.jobs) >= self.capacity:
            raise RuntimeError("global capacity")
        self.jobs[request] = d
        r.admitted += 1
        self.emit("admit", d, request)

    def complete(self, d, request, latency_ms, ok=True):
        nearest_rank([latency_ms], 1)
        if type(ok) is not bool:
            raise ValueError("boolean outcome")
        if self.jobs.get(request) != d:
            raise RuntimeError("unissued/foreign/already completed request")
        r = self.revisions[d]
        del self.jobs[request]
        self.done.add(request)
        r.completed += 1
        r.observations.append((latency_ms, ok))
        self.emit("complete", d, request)

    def promote(self, d):
        r = self.revisions[d]
        if r.state != "canary" or not r.ready or not r.live:
            raise RuntimeError("ready canary required")
        if not self.gate.passes(r.observations):
            raise RuntimeError("insufficient or failing revision-local evidence")
        if self.active is not None:
            self.previous = self.active
            old = self.revisions[self.active]
            old.state, old.ready = "superseded", False
        self.active, r.state = d, "active"
        self.emit("promoted", d)

    def drain(self, d):
        r = self.revisions[d]
        if r.state not in ("active", "canary", "superseded", "rolled_back"):
            raise RuntimeError("cannot drain")
        r.state, r.ready = "draining", False
        if self.active == d:
            self.active = None
        self.emit("drain", d)

    def terminate(self, d):
        r = self.revisions[d]
        if r.state != "draining" or d in self.jobs.values():
            raise RuntimeError("ownership must reach zero")
        r.state, r.live, r.ready = "terminated", False, False
        self.emit("terminated", d)

    def rollback(self, durable_schema):
        if self.active is None or self.previous is None:
            raise RuntimeError("no rollback pair")
        bad, target = self.active, self.previous
        r = self.revisions[target]
        if (r.state != "superseded" or not r.live
                or r.bundle.state_schema != durable_schema
                or not self.contract.accepts(r.bundle)):
            raise RuntimeError("rollback incompatible/unavailable")
        self.revisions[bad].state = "rolled_back"
        self.revisions[bad].ready = False
        r.state, r.ready = "active", True
        self.active, self.previous = target, None
        self.emit("rollback", target)
        return target

    def check(self):
        for d, r in self.revisions.items():
            assert r.admitted == r.completed + list(self.jobs.values()).count(d)
            if r.state == "terminated":
                assert d not in self.jobs.values() and not r.ready
        assert len(self.jobs) <= self.capacity
        assert [e["seq"] for e in self.events] == list(range(len(self.events)))


def bundle(revision, model):
    return Bundle(revision, digest(model), digest("runtime"), digest("ACGT"),
                  digest({"max_output": 64}))


def results():
    d = Deployment(gate=Gate(minimum=3))
    trace = []
    for version in ("r1", "r2"):
        x = d.register(bundle(version, version), True)
        d.canary(x)
        d.health(x, live=True, ready=True)
        for i, ms in enumerate((40, 60, 130)):
            rid = version + str(i)
            d.admit(x, rid)
            d.complete(x, rid, ms)
        d.promote(x)
        trace.append(dict(revision=version, n=3, p95=130, errors=0))
    target = d.rollback(1)
    d.check()
    return dict(gates=trace, active=d.revisions[target].bundle.revision,
                events=len(d.events), source="synthetic lifecycle")


TABLES = [("gates", ["Revision", "$n$", "p95 (ms)", "Errors"],
           ["revision", "n", "p95", "errors"], "lrrr")]
PLOTS = []
LISTINGS = ["Bundle.digest", "Gate.passes", "Deployment.admit",
            "Deployment.complete", "Deployment.promote", "Deployment.rollback",
            "verify_capsule"]
