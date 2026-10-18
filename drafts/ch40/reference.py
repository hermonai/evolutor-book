"""Serialized memory DAG with deletion-dominant reads and bounded context.

Logical unavailability is not physical erasure; authority is configured outside
this store. Unicode UTF-8 bytes, logical integer ticks and lexical ranking.
"""
from dataclasses import dataclass
import hashlib
import json
import re


def bound(x, minimum=0, maximum=10000):
    if type(x) is not int or not minimum <= x <= maximum:
        raise ValueError("bounded integer")
    return x


def text(x):
    if type(x) is not str or not 1 <= len(x.encode()) <= 10000:
        raise ValueError("bounded nonempty text")
    return x


@dataclass(frozen=True)
class Record:
    rid: str
    tenant: str
    kind: str
    payload: str
    sources: tuple
    created: int
    expires: int | None
    artifact: str


@dataclass(frozen=True)
class Context:
    records: tuple
    utf8_bytes: int
    authority: tuple = ()


class Memory:
    def __init__(self):
        self.records, self.tombstones, self.clock, self._serial = {}, set(), 0, 0
        self.depth = {}

    def _put(self, tenant, kind, payload, sources, ttl, artifact):
        text(tenant); text(payload); text(artifact)
        if ttl is not None:
            bound(ttl, 1)
        depth = 0 if not sources else 1 + max(self.depth[s] for s in sources)
        if depth > 32 or len(self.records) >= 10000:
            raise MemoryError("bounded provenance depth/store capacity")
        created = self.clock
        expires = None if ttl is None else created + ttl
        body = (tenant, kind, payload, sources, created, expires, artifact, self._serial)
        rid = hashlib.sha256(json.dumps(body, ensure_ascii=False).encode()).hexdigest()
        rec = Record(rid, tenant, kind, payload, sources, created, expires, artifact)
        self.records[rid] = rec
        self.depth[rid] = depth
        self._serial += 1
        return rec

    def put_event(self, tenant, payload, ttl=None, artifact="event-schema-v1"):
        return self._put(tenant, "event", payload, (), ttl, artifact)

    def _available(self, tenant, rid, seen, memo=None):
        memo = {} if memo is None else memo
        if rid in memo:
            return memo[rid]
        if rid in seen:
            return False  # defense if trusted internal storage is corrupted
        r = self.records.get(rid)
        if (r is None or r.tenant != tenant or rid in self.tombstones or
                (r.expires is not None and self.clock >= r.expires)):
            return False
        result = all(self._available(tenant, x, seen | {rid}, memo) for x in r.sources)
        memo[rid] = result
        return result

    def get(self, tenant, rid):
        text(tenant)
        r = self.records.get(rid)
        if r is not None and r.tenant != tenant:
            raise PermissionError("foreign record")
        if not self._available(tenant, rid, set()):
            raise KeyError("missing, expired, forgotten or stale-derived record")
        return r

    def summarize(self, tenant, source_ids, max_words=12, ttl=None):
        bound(max_words, 1, 1000)
        if (type(source_ids) is not tuple or not 1 <= len(source_ids) <= 64 or
                len(set(source_ids)) != len(source_ids)):
            raise ValueError("bounded distinct source tuple")
        sources = [self.get(tenant, rid) for rid in source_ids]
        words = list(dict.fromkeys(w for r in sources for w in r.payload.split()))
        payload = " ".join(words[:max_words])
        return self._put(tenant, "summary", payload, source_ids, ttl,
                         f"first-distinct-words-v1:{max_words}")

    def retrieve(self, tenant, query, k=3, candidates=None):
        text(tenant); text(query); bound(k, 0, 64)
        terms = set(re.findall(r"[a-z0-9]+", query.lower()))
        # Candidate IDs can come from a stale index; object-store checks dominate.
        ids = tuple(self.records) if candidates is None else tuple(candidates)
        scored = []
        for rid in set(ids):
            if not self._available(tenant, rid, set()):
                continue
            r = self.records[rid]
            score = len(terms & set(re.findall(r"[a-z0-9]+", r.payload.lower())))
            if score:
                scored.append((-score, r.created, rid, r))
        return tuple(x[3] for x in sorted(scored)[:k])

    def rehydrate(self, tenant, summary_id, max_sources=4, max_bytes=1000):
        bound(max_sources, 0, 64); bound(max_bytes, 0, 100000)
        root = self.get(tenant, summary_id)
        if root.kind != "summary":
            raise ValueError("summary required")
        pending, visited, result, used = list(root.sources), set(), [], 0
        # Traverse unique nodes breadth-first. Existing-source DAG creation and
        # strict summary availability make every visited ancestor readable.
        while pending and len(result) < max_sources:
            rid = pending.pop(0)
            if rid in visited:
                continue
            visited.add(rid)
            r = self.get(tenant, rid)
            size = len(r.payload.encode("utf-8"))
            if used + size > max_bytes:
                break  # deterministic prefix policy, no partial records
            used += size
            result.append(r)
            pending.extend(r.sources)
        return Context(tuple(result), used)

    def promote(self, tenant, ids, max_bytes):
        bound(max_bytes, 0, 100000)
        if type(ids) is not tuple or len(ids) > 64 or len(ids) != len(set(ids)):
            raise ValueError("bounded unique record IDs")
        rows = tuple(self.get(tenant, rid) for rid in ids)
        size = sum(len(r.payload.encode("utf-8")) for r in rows)
        if size > max_bytes:
            raise MemoryError("whole working set exceeds UTF-8 payload budget")
        return Context(rows, size)  # never carries grants or tool permissions

    def forget(self, tenant, rid):
        text(tenant)
        r = self.records.get(rid)
        if r is None:
            raise KeyError(rid)
        if r.tenant != tenant:
            raise PermissionError("foreign record")
        self.tombstones.add(rid)  # idempotent, including expired records

    def tick(self, n=1):
        self.clock += bound(n)


def results():
    m = Memory()
    a = m.put_event("t", "alpha beta gamma", ttl=2)
    b = m.put_event("t", "delta epsilon")
    s = m.summarize("t", (a.rid, b.rid), max_words=3)
    source_bytes = len(a.payload.encode()) + len(b.payload.encode())
    rows = []
    for phase in ("live", "expired"):
        rows.append({"phase": phase, "events": len(m.retrieve("t", "alpha delta")),
                     "summary_visible": int(m._available("t", s.rid, set()))})
        m.tick(2)
    # Equal summaries with distinct source histories are a lossy negative control.
    x = m.put_event("t", "alpha beta omitted-x")
    y = m.put_event("t", "alpha beta omitted-y")
    sx, sy = m.summarize("t", (x.rid,), 2), m.summarize("t", (y.rid,), 2)
    return {"visibility": rows, "source_bytes": source_bytes,
            "summary_bytes": len(s.payload.encode()),
            "payload_ratio": len(s.payload.encode()) / source_bytes,
            "alias_text_equal": sx.payload == sy.payload,
            "alias_provenance_different": sx.sources != sy.sources}


TABLES = [("visibility", ["Phase", "Ranked hits", "Summary available"],
           ["phase", "events", "summary_visible"], "lrr")]
PLOTS = []
LISTINGS = ["Memory._available", "Memory.summarize", "Memory.rehydrate", "Memory.promote"]
