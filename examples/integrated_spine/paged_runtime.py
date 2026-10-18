"""Connect actual Chapters 36, 39 and 41 without changing their teaching APIs.

Serialized CPU/float64 reference adapter, not an asynchronous serving engine.
Every row passed to execute is consumed once. Chapter 37's final prediction
and Chapter 38's already-consumed speculative output use different clocks;
neither is silently scheduled by this adapter. Pools stage contiguous caches
internally. No paged GPU append kernel or production isolation is supplied.
"""

import importlib.util
from pathlib import Path
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]


def chapter(number):
    name = f"evod_final_spine_{number}"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, ROOT / f"drafts/ch{number:02d}/reference.py"
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


compiler = chapter(41)
# Reuse the compiler's exact runtime module: same Value/Handle/enum identities.
runtime = compiler.chapter(39)
paging = chapter(36)


class PagedEngineAdapter:
    """Chapter 39's opaque adapter protocol over the actual Chapter 36 pool.

    Fresh request owners, unchanged model identity and serialized calls are
    premises. Native page lifetime checks remain authoritative. Model mutation
    during a live request is outside the pool's release contract; this is not
    the Chapter 30 cancellation/publication/acknowledgement serving shell.
    """

    backend = "hermon-paged"
    capability = runtime.Capability.ADDRESSABLE_KV

    def __init__(self, model=None, capacity=8, page_size=2):
        self.model = paging.native.tiny_model() if model is None else model
        self.pool = paging.PagedKV(self.model, capacity, page_size)
        self.artifact = self.pool.artifact
        self.identity = uuid.uuid4().hex
        self._next, self._states = 0, {}

    def _register(self, owner, native_handle):
        h = runtime.Handle(
            self.identity, self.backend, self.artifact, owner, self._next
        )
        self._next += 1
        self._states[h.serial] = (h, native_handle)
        return h

    def open(self, owner):
        runtime.owner_pair(owner)
        return self._register(owner, self.pool.empty(owner))

    def _check(self, handle, owner):
        runtime.owner_pair(owner)
        if not isinstance(handle, runtime.Handle) or type(handle.serial) is not int:
            raise RuntimeError("opaque runtime handle required")
        stored = self._states.get(handle.serial)
        if (
            handle.adapter != self.identity
            or handle.owner != owner
            or stored is None
            or stored[0] != handle
        ):
            raise RuntimeError("stale, forged or foreign runtime handle")
        return stored[1]

    def execute(self, handle, owner, tokens):
        native_handle = self._check(handle, owner)
        if (
            type(tokens) is not tuple
            or not 1 <= len(tokens) <= 512
            or any(type(t) is not int for t in tokens)
        ):
            raise ValueError("nonempty bounded concrete tokens")
        # PagedKV.consume updates its issued handle in place and returns logits.
        # It does not return Chapter 35's (logits, replacement_cache) pair.
        logits = self.pool.consume(native_handle, owner, tokens)
        return runtime.Value(
            runtime.Ty.LOGITS,
            tuple(tuple(row) for row in logits.tolist()),
            (self.backend, self.artifact),
        )

    def fork(self, handle, owner, new_owner):
        native_handle = self._check(handle, owner)
        child = self.pool.fork(native_handle, owner, new_owner)
        return self._register(new_owner, child)

    def close(self, handle, owner):
        native_handle = self._check(handle, owner)
        self.pool.release(native_handle, owner)
        del self._states[handle.serial]


def example():
    adapter = PagedEngineAdapter()
    r = runtime
    tokens = (0, 1, 2, 3)
    plan = r.Plan(
        ("tenant", "integrated-example"),
        (("tokens", r.Value(r.Ty.TOKENS, tokens)),),
        (
            r.Step(
                "native",
                "engine",
                ("tokens",),
                "z",
                r.Ty.LOGITS,
                adapter.artifact,
                adapter.capability,
            ),
        ),
        ("z",),
    )
    (out,) = r.Runtime((adapter,), r.Policy()).execute(plan)
    return {
        "backend": out.provenance[0],
        "consumed_tokens": len(out.data),
        "logit_width": len(out.data[0]),
        "remaining_runtime_handles": len(adapter._states),
        "page_inventory": adapter.pool.audit(),
        "evidence_class": "serialized untrained CPU reference; no service benchmark",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(example(), indent=2))
