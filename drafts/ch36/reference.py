"""Serialized paged storage refining the actual Chapter 35 layered Hermon cache.

Pages hold all layers at a token span. Flatten/compute stages are intentionally
contiguous and expensive; this is lifetime/refinement evidence, not a GPU kernel.
Python-private registries and SHA seals are not hostile-process authorization.
"""
from collections import Counter
from dataclasses import dataclass, replace
import importlib.util
import math
from pathlib import Path
import sys
import torch


def chapter(no):
    name = f"evod_batch_a_{no}"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, Path(__file__).parent.parent / f"ch{no}/reference.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


native = chapter(35)


def positive(n):
    if type(n) is not int or n < 1:
        raise ValueError("positive concrete integer")
    return n


@dataclass(frozen=True)
class PageRef:
    page_id: int
    generation: int


@dataclass(frozen=True)
class Handle:
    arena: object
    serial: int


@dataclass(frozen=True)
class State:
    owner: tuple
    tokens: tuple
    pages: tuple
    seal: str


@dataclass
class Page:
    generation: int = 0
    refs: int = 0
    layers: tuple = ()
    seal: str = ""


def page_seal(layers):
    return native.digest([(x.k.tolist(), x.v.tolist()) for x in layers])


class PagedKV:
    def __init__(self, model, capacity, page_size):
        self.model = model
        self.artifact = native.artifact_id(model)
        self.capacity, self.page_size = positive(capacity), positive(page_size)
        self.pages = [Page() for _ in range(capacity)]
        self._arena, self._next, self._states = object(), 0, {}

    def _sealed(self, owner, tokens, refs):
        value = [owner, self.artifact, native.MODE, tokens,
                 [(r.page_id, r.generation) for r in refs]]
        return State(owner, tuple(tokens), tuple(refs), native.digest(value))

    def _install(self, state):
        self._next += 1
        h = Handle(self._arena, self._next)
        self._states[h.serial] = state
        return h

    def empty(self, owner):
        native.owner_pair(owner)
        if any(s.owner == owner for s in self._states.values()):
            raise ValueError("fresh owner required")
        return self._install(self._sealed(owner, (), ()))

    def page(self, ref):
        if (type(ref) is not PageRef or type(ref.page_id) is not int
                or not 0 <= ref.page_id < self.capacity
                or type(ref.generation) is not int):
            raise ValueError("page reference")
        p = self.pages[ref.page_id]
        if p.refs < 1 or ref.generation != p.generation:
            raise ValueError("stale page generation")
        if p.seal != page_seal(p.layers):
            raise ValueError("mutated page payload")
        return p

    def state(self, handle, owner):
        native.owner_pair(owner)
        if type(handle) is not Handle or handle.arena is not self._arena:
            raise ValueError("foreign handle")
        if handle.serial not in self._states:
            raise ValueError("released handle")
        s = self._states[handle.serial]
        if s.owner != owner:
            raise PermissionError("owner mismatch")
        if self.artifact != native.artifact_id(self.model):
            raise ValueError("model changed")
        if s != self._sealed(s.owner, s.tokens, s.pages):
            raise ValueError("block table mutated")
        native.tokens_copy(s.tokens, self.model.max_len)
        if len(s.pages) != math.ceil(len(s.tokens) / self.page_size):
            raise ValueError("block table length")
        if len(set(s.pages)) != len(s.pages):
            raise ValueError("duplicate physical page in sequence")
        for i, ref in enumerate(s.pages):
            p = self.page(ref)
            count = min(self.page_size, len(s.tokens) - i * self.page_size)
            if len(p.layers) != len(self.model.blocks):
                raise ValueError("all layers required")
            for kv, block in zip(p.layers, self.model.blocks):
                for x in (kv.k, kv.v):
                    if (x.shape != (block.attn.h, count, block.attn.dh)
                            or x.dtype != torch.float64 or x.device.type != "cpu"
                            or x.requires_grad or not bool(torch.isfinite(x).all())):
                        raise ValueError("page geometry/content")
        return s

    def flatten(self, handle, owner):
        s = self.state(handle, owner)
        if not s.pages:
            return native.empty(self.model, owner)
        layers = []
        for i in range(len(self.model.blocks)):
            parts = [self.page(ref).layers[i] for ref in s.pages]
            layers.append(native.LayerKV(torch.cat([p.k for p in parts], 1),
                                         torch.cat([p.v for p in parts], 1)))
        result = native.sealed(owner, self.artifact, s.tokens, layers)
        native.validate(self.model, result, owner)
        return result

    def _drop(self, ref):
        p = self.pages[ref.page_id]
        p.refs -= 1
        if p.refs == 0:
            p.layers, p.seal = (), ""
            p.generation += 1

    def fork(self, handle, owner, new_owner):
        s = self.state(handle, owner)
        native.owner_pair(new_owner)
        if new_owner[0] != owner[0]:
            raise PermissionError("tenant-scoped sharing")
        if any(x.owner == new_owner for x in self._states.values()):
            raise ValueError("fresh owner required")
        for ref in s.pages:
            self.pages[ref.page_id].refs += 1
        return self._install(self._sealed(new_owner, s.tokens, s.pages))

    def release(self, handle, owner):
        s = self.state(handle, owner)
        for ref in s.pages:
            self._drop(ref)
        del self._states[handle.serial]

    def required_pages(self, handle, owner, count):
        s = self.state(handle, owner)
        if type(count) is not int or not 0 <= count <= self.model.max_len-len(s.tokens):
            raise ValueError("bounded append count")
        if not count:
            return 0
        offset = len(s.tokens) % self.page_size
        if not offset:
            return math.ceil(count / self.page_size)
        cow = int(self.page(s.pages[-1]).refs > 1)
        return cow + math.ceil(max(0, count-(self.page_size-offset))/self.page_size)

    @torch.no_grad()
    def consume(self, handle, owner, tokens):
        """Preflight and stage before a serialized, non-yielding publication."""
        s = self.state(handle, owner)
        tokens = native.tokens_copy(tokens, self.model.max_len-len(s.tokens))
        needed = self.required_pages(handle, owner, len(tokens))
        free = [i for i, p in enumerate(self.pages) if p.refs == 0]
        if len(free) < needed:
            raise MemoryError("insufficient pages; original state unchanged")
        logits, candidate = native.consume(self.model, self.flatten(handle, owner),
                                            owner, tokens)
        if not tokens:
            return logits
        start = len(s.tokens) // self.page_size
        prepared = []
        for b in range(start, math.ceil(len(candidate.tokens)/self.page_size)):
            lo, hi = b*self.page_size, (b+1)*self.page_size
            layers = tuple(native.LayerKV(x.k[:, lo:hi].clone(),
                                          x.v[:, lo:hi].clone())
                           for x in candidate.layers)
            prepared.append((layers, page_seal(layers)))
        # All model arithmetic, validation, tensor allocation and hashes precede
        # publication. Not crash-atomic or a concurrent memory manager.
        refs = list(s.pages[:start])
        writes = []
        old_tail = s.pages[-1] if len(s.tokens) % self.page_size else None
        for i, (layers, seal) in enumerate(prepared):
            private = i == 0 and old_tail and self.pages[old_tail.page_id].refs == 1
            slot = old_tail.page_id if private else free.pop(0)
            writes.append((slot, layers, seal))
            refs.append(PageRef(slot, self.pages[slot].generation))
        new_state = self._sealed(owner, candidate.tokens, refs)
        for slot, layers, seal in writes:
            page = self.pages[slot]
            page.layers, page.seal, page.refs = layers, seal, 1
        if old_tail and refs[start] != old_tail:
            self._drop(old_tail)
        self._states[handle.serial] = new_state
        return logits

    def audit(self):
        expected = Counter()
        for serial, state in self._states.items():
            self.state(Handle(self._arena, serial), state.owner)
            expected.update(r.page_id for r in state.pages)
        for i, p in enumerate(self.pages):
            if p.refs != expected[i] or (p.refs == 0 and (p.layers or p.seal)):
                raise AssertionError("reference conservation/scrub invariant")
        used = sum(p.refs > 0 for p in self.pages)
        rows = sum(p.layers[0].k.shape[1] for p in self.pages if p.refs)
        return {"used_pages": used, "free_pages": self.capacity-used,
                "references": sum(expected.values()), "physical_rows": rows,
                "tail_slots": used*self.page_size-rows}


class PrefixCache:
    """Exact token identity, tenant partition, model-bound pool, bounded LRU."""
    def __init__(self, pool, entries=4):
        self.pool, self.limit, self.items = pool, positive(entries), {}
        self.serial = 0

    def put(self, handle, owner):
        s = self.pool.state(handle, owner)
        key = (owner[0], self.pool.artifact, native.MODE, s.tokens)
        if key in self.items:
            self.evict(key)
        self.serial += 1
        cache_owner = (owner[0], f"@prefix-{self.serial}")
        cached = self.pool.fork(handle, owner, cache_owner)
        self.items[key] = (cached, cache_owner)
        if len(self.items) > self.limit:
            self.evict(next(iter(self.items)))
        return key

    def acquire(self, key, new_owner):
        if key[0] != new_owner[0]:
            raise PermissionError("tenant-scoped prefix")
        h, owner = self.items[key]
        result = self.pool.fork(h, owner, new_owner)
        self.items[key] = self.items.pop(key)
        return result

    def evict(self, key):
        h, owner = self.items[key]
        self.pool.release(h, owner)
        del self.items[key]


def results():
    model, owner = native.tiny_model(), ("tenant", "parent")
    pool = PagedKV(model, 8, 2)
    h = pool.empty(owner)
    pool.consume(h, owner, (0, 1, 2))
    child_owner = ("tenant", "child")
    child = pool.fork(h, owner, child_owner)
    y = pool.consume(child, child_owner, (3,))
    rows = []
    for label, obj, who in (("parent", h, owner), ("child", child, child_owner)):
        state = pool.state(obj, who)
        rows.append({"request": label, "tokens": len(state.tokens),
                     "pages": len(state.pages),
                     "tail_waste": len(state.pages)*2-len(state.tokens)})
    error = (y-native.full_oracle(model, (0, 1, 2, 3))[-1:]).abs().max().item()
    stats = pool.audit()
    return {"branches": rows, "stats": stats, "native_error": error,
            "page_payload_bytes": 2*2*2*2*4*8,
            "geometry": [{"P": p,"pages": math.ceil(13/p),
                          "waste": math.ceil(13/p)*p-13} for p in (1,2,4,8)]}


TABLES = [("branches", ["Request", "Tokens", "Page refs", "Tail slots"],
           ["request", "tokens", "pages", "tail_waste"], "lrrr"),
          ("geometry", ["Page tokens", "Pages for 13", "Unused slots"],
           ["P", "pages", "waste"], "rrr")]
PLOTS = []
LISTINGS = ["PagedKV.required_pages", "PagedKV.consume", "PagedKV.fork", "PagedKV.audit"]
