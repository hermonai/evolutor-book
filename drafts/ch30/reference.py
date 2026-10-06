"""EVOD-30 serialized request oracle; no sockets, device kernels or authentication."""

from dataclasses import dataclass
from enum import Enum
import itertools
import json
import re


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(name)
    return value


def identity(value, name):
    if not isinstance(value, str) or not value or len(value) > 128:
        raise ValueError(name)
    return value


@dataclass(frozen=True)
class Request:
    request_id: str
    tenant_id: str
    model_id: str
    deadline_ms: int
    max_tokens: int = 3
    queue_items: int = 2
    queue_bytes: int = 8
    item_bytes: int = 4

    def __post_init__(self):
        identity(self.request_id, "request")
        identity(self.tenant_id, "tenant")
        if not isinstance(self.model_id, str) or not re.fullmatch(
            "[0-9a-f]{64}", self.model_id
        ):
            raise ValueError("pinned SHA-256 identity required")
        integer(self.deadline_ms, "deadline")
        for field in ("max_tokens", "queue_items", "queue_bytes", "item_bytes"):
            integer(getattr(self, field), field, 1)
        if self.item_bytes > self.queue_bytes:
            raise ValueError("one maximum item must fit")


@dataclass(frozen=True)
class Lease:
    state_id: str
    generation: int
    owner: tuple


class StateRegistry:
    def __init__(self):
        self._live = {}
        self._generation = {}

    def claim(self, state_id, req):
        identity(state_id, "state")
        if state_id in self._live:
            raise RuntimeError("state already owned")
        generation = self._generation.get(state_id, 0) + 1
        lease = Lease(
            state_id, generation, (req.tenant_id, req.request_id, req.model_id)
        )
        self._generation[state_id] = generation
        self._live[state_id] = lease
        return lease

    def validate(self, lease):
        if not isinstance(lease, Lease) or self._live.get(lease.state_id) != lease:
            raise RuntimeError("stale or foreign lease")

    def release(self, lease):
        self.validate(lease)
        del self._live[lease.state_id]

    def live_count(self):
        return len(self._live)


class Phase(str, Enum):
    RECEIVED = "received"
    ADMITTED = "admitted"
    ACTIVE = "active"
    TERMINAL = "terminal"


@dataclass(frozen=True)
class Ticket:
    lease: Lease
    revision: int
    launch_id: int


@dataclass(frozen=True)
class Event:
    seq: int
    time_ms: int
    kind: str
    metadata: tuple


class Runtime:
    def __init__(self, req, registry):
        if not isinstance(req, Request) or not isinstance(registry, StateRegistry):
            raise ValueError("request and registry required")
        self.req, self.registry = req, registry
        self.phase, self.reason = Phase.RECEIVED, None
        self.cleaned = False
        self.worker = self.lease = self.pending = None
        self.revision = self.last_ms = 0
        self.queue = []  # (sequence, immutable UTF-8 bytes)
        self.events = []
        self.launched = self.settled = self.generated = 0
        self.delivered = self.discarded = self.discarded_work = 0
        self._event("received")

    def _event(self, kind, **data):
        self.events.append(
            Event(len(self.events), self.last_ms, kind, tuple(sorted(data.items())))
        )

    def _clock(self, now):
        integer(now, "monotonic clock")
        if now < self.last_ms:
            raise ValueError("clock moved backwards")
        self.last_ms = now

    def _require(self, phase):
        if self.phase != phase or self.cleaned:
            raise RuntimeError("illegal lifecycle operation")

    def terminate(self, reason, now):
        """One serialized winner; terminal reason is not overwritten by cleanup."""
        self._clock(now)
        if reason not in ("completed", "cancelled", "deadline", "failed", "rejected"):
            raise ValueError("stable reason required")
        if self.phase == Phase.TERMINAL:
            return False
        if now >= self.req.deadline_ms:
            reason = "deadline"
        elif reason == "deadline":
            raise ValueError("deadline has not arrived")
        if reason == "completed" and (
            self.phase != Phase.ACTIVE or self.pending is not None
        ):
            raise RuntimeError("completion requires active quiescent state")
        self.phase, self.reason = Phase.TERMINAL, reason
        self._event("terminal", reason=reason)
        return True

    def check_deadline(self, now):
        self._clock(now)
        if self.phase != Phase.TERMINAL and now >= self.req.deadline_ms:
            self.terminate("deadline", now)
        return self.phase == Phase.TERMINAL

    def admit(self, worker, now, allowed=True, available=True):
        self._require(Phase.RECEIVED)
        identity(worker, "worker")
        if type(allowed) is not bool or type(available) is not bool:
            raise ValueError("explicit policy/model availability decisions")
        if self.check_deadline(now):
            return False
        if not allowed or not available:
            self.terminate("rejected", now)
            return False
        self.worker, self.phase = worker, Phase.ADMITTED
        self._event("admitted")
        return True

    def allocate(self, state_id, now):
        self._require(Phase.ADMITTED)
        if self.check_deadline(now):
            return False
        # Claim before local publication. A conflict leaves admitted state unchanged.
        lease = self.registry.claim(state_id, self.req)
        self.lease, self.phase = lease, Phase.ACTIVE
        self._event("allocated", generation=lease.generation)
        return True

    def launch(self, now):
        """Reserve worst-case output capacity before starting one logical step."""
        self._require(Phase.ACTIVE)
        if self.check_deadline(now):
            return None
        self.registry.validate(self.lease)
        if self.pending is not None:
            raise RuntimeError("one in-flight step per request")
        queued_bytes = sum(len(v) for _, v in self.queue)
        if (
            len(self.queue) >= self.req.queue_items
            or queued_bytes + self.req.item_bytes > self.req.queue_bytes
        ):
            self._event("backpressure", queued=len(self.queue))
            return None
        self.launched += 1
        self.pending = Ticket(self.lease, self.revision, self.launched)
        self._event("launch", launch=self.launched)
        return self.pending

    def commit(self, ticket, item, now):
        """Fence completion, then commit state revision and output together."""
        self._clock(now)
        if ticket != self.pending or self.pending is None:
            raise RuntimeError("foreign, stale or duplicate completion")
        self.registry.validate(ticket.lease)
        self.check_deadline(now)
        self.pending = None
        self.settled += 1
        if self.phase == Phase.TERMINAL:
            self.discarded_work += 1
            self._event("discard_work")
            return False
        if not isinstance(item, str):
            self.discarded_work += 1
            self.terminate("failed", now)
            return False
        try:
            payload = item.encode("utf-8")
        except UnicodeEncodeError:
            payload = b""
        if not payload or len(payload) > self.req.item_bytes:
            self.discarded_work += 1
            self.terminate("failed", now)
            return False
        self.revision += 1
        self.generated += 1
        self.queue.append((self.generated, payload))
        self._event("commit", item=self.generated, bytes=len(payload))
        if self.generated == self.req.max_tokens:
            self.terminate("completed", now)
        return True

    def consume(self, now):
        self._clock(now)
        if self.cleaned or self.phase not in (Phase.ACTIVE, Phase.TERMINAL):
            raise RuntimeError("no stream to consume")
        # Committed bytes remain readable after every terminal reason until cleanup.
        self.check_deadline(now)
        if not self.queue:
            return None
        seq, payload = self.queue.pop(0)
        self.delivered += 1  # local dequeue, not proof of remote receipt
        self._event("consume", item=seq)
        return seq, payload.decode("utf-8")

    def cancel(self, now):
        if self.check_deadline(now):
            return False
        return self.terminate("cancelled", now)

    def cleanup(self, now, discard_queue=False):
        """Physical quiescence precedes lease release; queued-output loss is explicit."""
        self._clock(now)
        if type(discard_queue) is not bool:
            raise ValueError("explicit queue disposition")
        if self.cleaned:
            return False
        if self.phase != Phase.TERMINAL or self.pending is not None:
            raise RuntimeError("terminal and quiescent required")
        if self.queue and not discard_queue:
            raise RuntimeError("drain or explicitly discard committed output")
        if self.lease is not None:
            self.registry.release(self.lease)
        self.discarded += len(self.queue)
        self.queue.clear()
        self.worker = self.lease = None
        self.cleaned = True
        self._event("cleaned", discarded=self.discarded)
        return True

    def accounting(self):
        return {
            "launched": self.launched,
            "settled": self.settled,
            "pending": int(self.pending is not None),
            "discarded_work": self.discarded_work,
            "generated": self.generated,
            "queued": len(self.queue),
            "dequeued": self.delivered,
            "discarded_output": self.discarded,
            "revision": self.revision,
        }


def race_trace(order):
    reg = StateRegistry()
    rt = Runtime(Request("r30", "tenantA", "a" * 64, 100), reg)
    rt.admit("worker1", 0)
    rt.allocate("s1", 0)
    for event in order:
        rt.terminate(event, 1)
    rt.cleanup(2)
    return rt.reason, tuple(e.kind for e in rt.events), reg.live_count()


def results():
    reg = StateRegistry()
    rt = Runtime(Request("r30", "tenantA", "a" * 64, 100), reg)
    rt.admit("w", 0)
    rt.allocate("s", 0)
    accepted = []
    for item in ("a", "b"):
        accepted.append(rt.commit(rt.launch(1), item, 1))
    blocked = rt.launch(2) is None
    first = rt.consume(3)
    rt.commit(rt.launch(4), "c", 4)  # auto completion; two items still buffered
    retained = len(rt.queue)
    remaining = [rt.consume(5), rt.consume(5)]
    rt.cleanup(6)
    interrupted = Runtime(Request("r31", "tenantB", "b" * 64, 10), reg)
    interrupted.admit("w", 0)
    interrupted.allocate("s", 0)
    ticket = interrupted.launch(1)
    interrupted.cancel(2)
    discarded = not interrupted.commit(ticket, "x", 3)
    interrupted.cleanup(4)
    return {
        "stream": [dict(item=seq, text=text) for seq, text in [first] + remaining],
        "accepted_first_two": accepted,
        "backpressure": blocked,
        "retained_at_completion": retained,
        "accounting": rt.accounting(),
        "cancelled_work_discarded": discarded,
        "cancelled_accounting": interrupted.accounting(),
        "events": [dict(seq=e.seq, time=e.time_ms, kind=e.kind) for e in rt.events],
        "races": [
            dict(order=" / ".join(order), winner=race_trace(order)[0])
            for order in itertools.permutations(("completed", "cancelled", "failed"))
        ],
        "live_after_cleanup": reg.live_count(),
    }


TABLES = [
    ("stream", ["Sequence", "UTF-8 item"], ["item", "text"], "rl"),
    ("events", ["Event", "Time (ms)", "Kind"], ["seq", "time", "kind"], "rrl"),
]
PLOTS = []
LISTINGS = [
    "Request",
    "Runtime.terminate",
    "Runtime.launch",
    "Runtime.commit",
    "Runtime.cleanup",
]

if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
