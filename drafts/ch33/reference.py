"""Bounded data-only checkpoints of Chapters 31–32's actual inference state.

Trusted, serialized caller/producer model; no authentication, durable storage,
GPU concurrency, COW backend, training restart or trained-genomic capability.
"""

from collections import OrderedDict
from dataclasses import asdict, dataclass
import hashlib
import hmac
import importlib.util
import json
import math
from pathlib import Path
import re
import sys

MAX_TOKENS = 4096
MAX_WIDTH = 256
MAX_WIRE = 262144
FORMAT = "evod33-checkpoint-v1"
SEMANTICS = "evod31-causal-diagonal-v1"


def canonical(value):
    """Our Python JSON wire profile, not a universal cross-language standard."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


def sha(value):
    return hashlib.sha256(value).hexdigest()


def integer(value, lower, upper):
    if type(value) is not int or not lower <= value <= upper:
        raise ValueError("bounded integer required, not boolean")
    return value


def identity(value):
    if type(value) is not str or not 1 <= len(value) <= 128:
        raise ValueError("bounded nonempty identity")
    return value


def digest(value):
    if type(value) is not str or re.fullmatch("[0-9a-f]{64}", value) is None:
        raise ValueError("lowercase SHA-256 identifier")
    return value


@dataclass(frozen=True)
class Context:
    tenant: str
    artifact: str
    semantics: str
    tokenizer: str
    width: int
    vocabulary: int
    dtype: str = "float64"


def validate_context(context):
    if not isinstance(context, Context):
        raise ValueError("declared context")
    identity(context.tenant)
    identity(context.semantics)
    digest(context.artifact)
    digest(context.tokenizer)
    integer(context.width, 1, MAX_WIDTH)
    integer(context.vocabulary, 2, 2**31)
    if context.dtype != "float64":
        raise ValueError("this inference schema requires float64")
    return context


def tokens_copy(tokens, context):
    # A finite concrete sequence, not an unbounded or executable iterator.
    if type(tokens) not in (tuple, list) or len(tokens) > MAX_TOKENS:
        raise ValueError("bounded concrete token sequence")
    return tuple(integer(t, 0, context.vocabulary - 1) for t in tokens)


def hidden_copy(hidden, width):
    if type(hidden) not in (tuple, list) or len(hidden) != width:
        raise ValueError("declared hidden width")
    try:
        if any(type(x) not in (int, float) or not math.isfinite(x) for x in hidden):
            raise ValueError("finite numeric hidden values")
        if any(type(x) is int and float(x) != x for x in hidden):
            raise ValueError("integer hidden value loses binary64 precision")
        return tuple(float(x) for x in hidden)
    except OverflowError as error:
        raise ValueError("hidden value outside binary64 domain") from error


def pool_module():
    name = "evod33_actual_pool"
    if name not in sys.modules:
        path = Path(__file__).parent.parent / "ch32/reference.py"
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def context_for(model, tenant, semantics=SEMANTICS):
    if semantics != SEMANTICS:
        raise ValueError("unsupported native semantics")
    native = pool_module().native_module()
    artifact = native.artifact_id(model)
    tokenizer = sha(
        canonical({"mapping": "ordered-vocabulary-v1", "tokens": model.vocabulary})
    )
    return validate_context(
        Context(
            tenant,
            artifact,
            semantics,
            tokenizer,
            model.embedding.shape[1],
            len(model.vocabulary),
        )
    )


@dataclass(frozen=True)
class Checkpoint:
    wire: bytes
    sha256: str


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError("nonfinite JSON constant")


def decode(checkpoint):
    if (
        not isinstance(checkpoint, Checkpoint)
        or type(checkpoint.wire) is not bytes
        or not 1 <= len(checkpoint.wire) <= MAX_WIRE
    ):
        raise ValueError("bounded immutable checkpoint bytes")
    digest(checkpoint.sha256)
    if not hmac.compare_digest(sha(checkpoint.wire), checkpoint.sha256):
        raise ValueError("checkpoint digest mismatch")
    try:
        body = json.loads(
            checkpoint.wire.decode("ascii"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
        if type(body) is not dict or set(body) != {
            "format",
            "context",
            "position",
            "tokens",
            "hidden",
        }:
            raise ValueError("exact checkpoint schema")
        if body["format"] != FORMAT or type(body["context"]) is not dict:
            raise ValueError("format/context")
        if set(body["context"]) != set(Context.__dataclass_fields__):
            raise ValueError("exact context schema")
        context = validate_context(Context(**body["context"]))
        tokens = tokens_copy(body["tokens"], context)
        position = integer(body["position"], 0, MAX_TOKENS)
        if position != len(tokens):
            raise ValueError("position does not equal consumed prefix length")
        hidden_copy(body["hidden"], context.width)
        if canonical(body) != checkpoint.wire:
            raise ValueError("noncanonical wire profile")
    except (UnicodeError, TypeError, RecursionError, OverflowError) as error:
        raise ValueError("invalid checkpoint data") from error
    return body


def checked(checkpoint, context, tokens):
    validate_context(context)
    tokens = tokens_copy(tokens, context)
    body = decode(checkpoint)
    if body["context"] != asdict(context):
        raise ValueError("checkpoint context mismatch")
    if tuple(body["tokens"]) != tokens:
        raise ValueError("exact consumed prefix mismatch")
    return body


def _pool_context(pool, context):
    validate_context(context)
    if pool.artifact != context.artifact or pool.width != context.width:
        raise ValueError("pool/context artifact or width mismatch")


def capture(pool, handle, owner, context, tokens):
    _pool_context(pool, context)
    pool_module().owner_pair(owner)
    if owner[0] != context.tenant:
        raise PermissionError("tenant scope")
    tokens = tokens_copy(tokens, context)
    slot = pool._slot(handle, owner)
    if slot.pins:
        raise RuntimeError("snapshot requires a quiescent semantic boundary")
    snapshot = pool.read(handle, owner)
    if snapshot.position != len(tokens):
        raise ValueError("pool position/prefix mismatch")
    body = {
        "format": FORMAT,
        "context": asdict(context),
        "position": snapshot.position,
        "tokens": tokens,
        "hidden": hidden_copy(snapshot.hidden, context.width),
    }
    wire = canonical(body)
    checkpoint = Checkpoint(wire, sha(wire))
    decode(checkpoint)
    return checkpoint


def restore_many(checkpoint, pool, owners, context, tokens):
    """Preflight all branches before mutation, under serialized exclusive calls."""
    _pool_context(pool, context)
    body = checked(checkpoint, context, tokens)
    if type(owners) not in (tuple, list) or not 1 <= len(owners) <= pool.capacity:
        raise ValueError("bounded nonempty branch group")
    for owner in owners:
        pool_module().owner_pair(owner)
        if owner[0] != context.tenant:
            raise PermissionError("cross-tenant restore not provided")
    if len(set(owners)) != len(owners):
        raise ValueError("distinct branch owners")
    if any(slot.owner in owners for slot in pool._slots if slot.owner is not None):
        raise ValueError("new request owners must not already own pool slots")
    if pool.stats()["free"] < len(owners):
        raise MemoryError("branch group cannot fit, including retiring states")
    snapshot = pool_module().Snapshot(body["position"], tuple(body["hidden"]))
    return tuple(pool.allocate(owner, snapshot) for owner in owners)


def advance(pool, handle, owner, model, context, prefix, suffix):
    """One atomic pool installation after complete bounded native chunk success."""
    _pool_context(pool, context)
    if context_for(model, context.tenant, context.semantics) != context:
        raise ValueError("native model/context mismatch")
    prefix, suffix = tokens_copy(prefix, context), tokens_copy(suffix, context)
    tokens_copy(prefix + suffix, context)
    if owner[0] != context.tenant:
        raise PermissionError("tenant scope")
    slot = pool._slot(handle, owner)
    if slot.pins:
        raise RuntimeError("advance requires quiescent ownership")
    if pool.read(handle, owner).position != len(prefix):
        raise ValueError("prefix position")
    if not suffix:
        return prefix, ()
    native = pool_module().native_module()
    with native.torch.no_grad():
        state = pool_module().to_native(pool, handle, owner)
        state, logits = native.ingest(model, state, suffix, owner)
        pool_module().from_native(pool, handle, owner, model, state)
    return prefix + suffix, tuple(tuple(z.tolist()) for z in logits)


def replay_audit(checkpoint, model, context):
    """Expensive optional consistency check, not producer authentication."""
    body = decode(checkpoint)
    checked(checkpoint, context, body["tokens"])
    if context_for(model, context.tenant, context.semantics) != context:
        raise ValueError("native model/context mismatch")
    native = pool_module().native_module()
    owner = (context.tenant, "replay-audit")
    with native.torch.no_grad():
        state, _ = native.ingest(
            model, native.construct(model, owner), body["tokens"], owner
        )
    return tuple(body["hidden"]) == tuple(state.hidden.tolist())


def prefix_key(context, tokens):
    validate_context(context)
    return sha(
        canonical({"context": asdict(context), "tokens": tokens_copy(tokens, context)})
    )


class PrefixCache:
    """LRU bound on canonical wire bytes only, not Python heap or device bytes."""

    def __init__(self, max_bytes):
        self.max_bytes = integer(max_bytes, 1, 2**31)
        self._items = OrderedDict()
        self.bytes = 0

    def put(self, checkpoint, context, tokens):
        checked(checkpoint, context, tokens)
        key = prefix_key(context, tokens)
        if key in self._items:
            previous = self._items[key]
            checked(previous, context, tokens)
            if previous != checkpoint:
                raise ValueError("conflicting state for identical prefix")
            self._items.move_to_end(key)
            return key
        size = len(checkpoint.wire)
        if size > self.max_bytes:
            raise MemoryError("checkpoint exceeds byte budget")
        while self.bytes + size > self.max_bytes:
            _, evicted = self._items.popitem(last=False)
            self.bytes -= len(evicted.wire)
        self._items[key] = checkpoint
        self.bytes += size
        return key

    def longest(self, context, query):
        validate_context(context)
        query = tokens_copy(query, context)
        for length in range(len(query), -1, -1):
            prefix = query[:length]
            key = prefix_key(context, prefix)
            checkpoint = self._items.get(key)
            if checkpoint is not None:
                checked(checkpoint, context, prefix)
                self._items.move_to_end(key)
                return length, checkpoint
        return 0, None


def checkpoint_cost(length, interval, width):
    integer(length, 1, MAX_TOKENS)
    integer(interval, 1, length)
    integer(width, 1, MAX_WIDTH)
    count = length // interval
    state_bytes = count * width * 8
    token_bytes = 4 * interval * count * (count + 1) // 2
    return {
        "interval": interval,
        "checkpoints": count,
        "state_bytes": state_bytes,
        "token_bytes": token_bytes,
        "total_bytes": state_bytes + token_bytes,
        "expected_replay": (interval - 1) / 2,
    }


TABLES = [
    ("branches", ["Boundary", "$h_1$", "$h_2$"], ["event", "h1", "h2"], "lrr"),
    (
        "costs",
        ["$B$", "States", "State B", "Token B", "Replay"],
        ["interval", "checkpoints", "state_bytes", "token_bytes", "expected_replay"],
        "rrrrr",
    ),
]
PLOTS = [
    ("cost-memory", "costs", "interval", ["state_bytes", "token_bytes"]),
    ("cost-replay", "costs", "interval", ["expected_replay"]),
]
LISTINGS = ["checked", "capture", "restore_many", "PrefixCache.longest"]


def results():
    p = pool_module()
    model = p.native_module().tiny_model()
    context = context_for(model, "tenant-a")
    pool = p.Pool("branches", 3, context.width, context.artifact)
    owner = ("tenant-a", "prompt")
    handle = pool.allocate(owner)
    prefix, _ = advance(pool, handle, owner, model, context, (), (1, 2, 1))
    checkpoint = capture(pool, handle, owner, context, prefix)
    owners = (("tenant-a", "left"), ("tenant-a", "right"))
    left, right = restore_many(checkpoint, pool, owners, context, prefix)
    rows = []
    for event, h, who, suffix in (
        ("shared prefix", handle, owner, ()),
        ("left: token 0", left, owners[0], (0,)),
        ("right: token 2", right, owners[1], (2,)),
    ):
        advance(pool, h, who, model, context, prefix, suffix)
        snap = pool.read(h, who)
        rows.append({"event": event, "h1": snap.hidden[0], "h2": snap.hidden[1]})
    return {
        "branches": rows,
        "checkpoint_sha256": checkpoint.sha256,
        "checkpoint_wire_bytes": len(checkpoint.wire),
        "replay_audit": replay_audit(checkpoint, model, context),
        "costs": [checkpoint_cost(64, b, 8) for b in (1, 2, 4, 8, 16, 32, 64)],
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
