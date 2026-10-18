"""Serialized session/recovery contract; no external effects or durable storage."""
from dataclasses import dataclass
import hashlib
import json


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


@dataclass(frozen=True)
class Identity:
    tenant: str
    session: str
    artifact: str
    policy: str


@dataclass(frozen=True)
class Event:
    seq: int
    kind: str
    payload: str  # canonical JSON freezes nested values rather than aliasing dicts


@dataclass(frozen=True)
class Checkpoint:
    identity: Identity
    count: int
    digest: str


class Session:
    def __init__(self, identity, max_context=4, budget=3, expires=100):
        if (not isinstance(identity, Identity) or
                any(not isinstance(v, str) or not v or len(v) > 128
                    for v in identity.__dict__.values()) or
                type(max_context) is not int or max_context < 1 or
                type(budget) is not int or budget < 0 or
                type(expires) is not int or expires < 0):
            raise ValueError("bounded identity, context, budget and lease")
        self.identity = identity
        self.max_context, self.budget, self.expires = max_context, budget, expires
        self._events, self._intents, self._results = [], {}, {}
        self.closed = False

    @property
    def events(self):
        return tuple(self._events)

    def _record(self, kind, payload):
        event = Event(len(self._events), kind, canonical(payload))
        self._apply(event)
        return event

    def _apply(self, event):
        if (not isinstance(event, Event) or type(event.seq) is not int
                or event.seq != len(self._events) or self.closed):
            raise ValueError("ordered open session required")
        p = json.loads(event.payload)
        if not isinstance(p, dict) or canonical(p) != event.payload:
            raise ValueError("canonical object payload")
        if event.kind in ("user", "proposal", "output"):
            if set(p) != {"text"} or not isinstance(p["text"], str):
                raise ValueError("text event schema")
        elif event.kind == "intent":
            if (set(p) != {"key", "command", "tick"} or not isinstance(p["key"], str)
                    or not p["key"] or p["key"] in self._intents
                    or not isinstance(p["command"], dict) or
                    set(p["command"]) != {"name", "args"} or
                    not isinstance(p["command"]["name"], str) or not p["command"]["name"]
                    or not isinstance(p["command"]["args"], dict)
                    or type(p["tick"]) is not int or not 0 <= p["tick"] < self.expires
                    or len(self._intents) >= self.budget):
                raise ValueError("invalid or over-budget intent")
            self._intents[p["key"]] = p["command"]
        elif event.kind == "result":
            if (set(p) != {"key", "value"} or p["key"] not in self._intents
                    or p["key"] in self._results):
                raise ValueError("result without unique intent")
            self._results[p["key"]] = p["value"]
        elif event.kind == "close":
            if p or set(self._intents) != set(self._results):
                raise ValueError("reconcile pending actions before close")
            self.closed = True
        else:
            raise ValueError("unknown event kind")
        self._events.append(event)

    def append(self, kind, text):
        if kind not in ("user", "proposal", "output"):
            raise ValueError("authority events use typed methods")
        return self._record(kind, {"text": text})

    def context(self):
        return self.events[-self.max_context:]

    def prefix_digest(self, count):
        if type(count) is not int or not 0 <= count <= len(self._events):
            raise ValueError("valid event count")
        return digest({"identity": self.identity.__dict__,
                       "contract": [self.max_context, self.budget, self.expires],
                       "events": [e.__dict__ for e in self._events[:count]]})

    def checkpoint(self):
        n = len(self._events)
        return Checkpoint(self.identity, n, self.prefix_digest(n))

    def verify(self, cp):
        return (isinstance(cp, Checkpoint) and cp.identity == self.identity
                and type(cp.count) is int and 0 <= cp.count <= len(self._events)
                and self.prefix_digest(cp.count) == cp.digest)

    def issue(self, key, name, args, authorized, tick):
        """Reserve before dispatch; existing unresolved intent requests reconciliation."""
        if self.closed or authorized is not True:
            raise PermissionError("closed or unauthorized")
        if type(tick) is not int or not 0 <= tick < self.expires:
            raise PermissionError("lease expired")
        command = json.loads(canonical({"name": name, "args": args}))
        if key in self._intents:
            if self._intents[key] != command:
                raise ValueError("idempotency key reused for different command")
            if key in self._results:
                return "cached", json.loads(canonical(self._results[key]))
            return "reconcile", None
        self._record("intent", {"key": key, "command": command, "tick": tick})
        return "dispatch", None

    def complete(self, key, value):
        # Observation of a previously admitted action may arrive after lease expiry.
        value = json.loads(canonical(value))
        if key in self._results:
            if self._results[key] != value:
                raise ValueError("conflicting duplicate completion")
            return
        self._record("result", {"key": key, "value": value})

    def close(self):
        self._record("close", {})


def resume(identity, events, cp, max_context=4, budget=3, expires=100):
    session = Session(identity, max_context, budget, expires)
    for event in tuple(events):
        session._apply(event)
    if not session.verify(cp):
        raise ValueError("checkpoint identity/prefix/contract mismatch")
    return session


class Stream:
    def __init__(self, capacity):
        if type(capacity) is not int or capacity < 1:
            raise ValueError("positive queue capacity")
        self.capacity, self.q = capacity, []

    def push(self, item):
        if len(self.q) == self.capacity:
            raise BufferError("backpressure")
        self.q.append(item)

    def pop(self):
        return self.q.pop(0) if self.q else None


def results():
    ident = Identity("tenant-a", "agent-1", "model-v1", "policy-v1")
    s = Session(ident, 2, 1, 10)
    s.append("user", "inspect repository")
    first = s.issue("k1", "read", {"path": "a.py"}, True, 1)[0]
    cp = s.checkpoint()
    t = resume(ident, s.events, cp, 2, 1, 10)
    pending = t.issue("k1", "read", {"path": "a.py"}, True, 2)[0]
    t.complete("k1", {"content_digest": "example"})
    cached = t.issue("k1", "read", {"path": "a.py"}, True, 3)[0]
    return {"trace": [{"phase": "First admission", "action": first},
                      {"phase": "Resume unresolved", "action": pending},
                      {"phase": "Observed completion", "action": cached}],
            "events": len(t.events), "context": len(t.context()),
            "checkpoint_still_valid": t.verify(cp)}


TABLES = [("trace", ["State", "Next instruction"], ["phase", "action"], "ll")]
PLOTS = []
LISTINGS = ["Session.issue", "Session.complete", "resume", "Stream"]
