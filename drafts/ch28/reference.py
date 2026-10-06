"""EVOD-28: local collective algebra and strict demo artifact, not a cluster backend."""

from dataclasses import dataclass
import hashlib
import json
import math
import struct

FORMAT = "evolutor-tensor-demo/1"
WIDTH = {"F32": 4, "F64": 8}


def finite(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("Finite numeric scalar required")
    return float(value)


def positive_int(value):
    if type(value) is not int or value < 1:
        raise ValueError("Positive exact integer required")
    return value


def allreduce_mean(grads):
    if not isinstance(grads, (tuple, list)) or not grads:
        raise ValueError("Nonempty rank vectors required")
    if not all(isinstance(g, (tuple, list)) for g in grads):
        raise ValueError("Explicit vectors required")
    size = len(grads[0])
    if any(len(g) != size for g in grads):
        raise ValueError("Rank vector shape mismatch")
    return tuple(
        math.fsum(finite(g[i]) for g in grads) / len(grads) for i in range(size)
    )


def weighted_reduce(numerators, masses):
    """Global numerator-gradient sum / global valid-element mass."""
    if len(numerators) != len(masses) or not numerators:
        raise ValueError("Matching nonempty rank axis required")
    masses = tuple(finite(v) for v in masses)
    if min(masses) < 0:
        raise ValueError("Negative rank mass")
    total = math.fsum(masses)
    if not math.isfinite(total) or total <= 0:
        raise ValueError("Finite positive global mass required")
    mean = allreduce_mean(numerators)
    return tuple(v * len(numerators) / total for v in mean)


def ddp_local_scales(masses):
    """For a backend that MEANS gradients, backward N_r*D/Z on every rank."""
    masses = tuple(finite(v) for v in masses)
    if not masses or min(masses) < 0 or not 0 < math.fsum(masses) < math.inf:
        raise ValueError("Finite nonnegative masses with positive global sum required")
    return (len(masses) / math.fsum(masses),) * len(masses)


@dataclass(frozen=True)
class Shard:
    rank: int
    world: int
    start: int
    total: int
    values: tuple


def shard(values, world):
    world = positive_int(world)
    values = tuple(values)
    out = []
    start = 0
    for rank in range(world):
        size = len(values) // world + int(rank < len(values) % world)
        out.append(Shard(rank, world, start, len(values), values[start : start + size]))
        start += size
    return tuple(out)


def reconstruct(parts):
    """Rank/offset coverage checked; never concatenate unlabeled rank files."""
    parts = tuple(parts)
    if not parts or not all(isinstance(s, Shard) for s in parts):
        raise ValueError("Typed shard descriptors required")
    world = positive_int(parts[0].world)
    total = parts[0].total
    if type(total) is not int or total < 0 or len(parts) != world:
        raise ValueError("Missing rank or invalid total")
    if any(type(s.rank) is not int for s in parts) or {s.rank for s in parts} != set(
        range(world)
    ):
        raise ValueError("Duplicate or missing rank identities")
    out = []
    offset = 0
    for s in sorted(parts, key=lambda p: p.rank):
        expected = total // world + int(s.rank < total % world)
        if (
            type(s.world) is not int
            or type(s.total) is not int
            or s.world != world
            or s.total != total
            or type(s.start) is not int
            or s.start != offset
        ):
            raise ValueError("Incompatible shard metadata or coverage gap/overlap")
        if type(s.values) is not tuple or len(s.values) != expected:
            raise ValueError("Unexpected shard extent")
        out.extend(s.values)
        offset += expected
    if offset != total:
        raise ValueError("Incomplete global coverage")
    return tuple(out)


def matmul(x, w):
    if not x or not w or any(len(row) != len(w[0]) for row in w):
        raise ValueError("Nonempty rectangular matrices required")
    if any(len(row) != len(w) for row in x):
        raise ValueError("Contraction dimension mismatch")
    return tuple(
        tuple(
            math.fsum(finite(a) * finite(w[k][j]) for k, a in enumerate(row))
            for j in range(len(w[0]))
        )
        for row in x
    )


def row_parallel(x, w, world):
    """Split contraction axis; each rank produces a full-size partial output."""
    world = positive_int(world)
    parts = shard(tuple(range(len(w))), world)
    if not x or not w or any(len(row) != len(w) for row in x):
        raise ValueError("Matching nonempty contraction axis required")
    width = len(w[0])
    if width == 0 or any(len(row) != width for row in w):
        raise ValueError("Nonempty rectangular weight required")
    outputs = []
    for part in parts:
        outputs.append(
            tuple(
                tuple(
                    math.fsum(finite(row[k]) * finite(w[k][j]) for k in part.values)
                    for j in range(width)
                )
                for row in x
            )
        )
    return tuple(
        tuple(math.fsum(out[i][j] for out in outputs) for j in range(width))
        for i in range(len(x))
    )


def canonical_json(value):
    """Declared Python JSON profile, not RFC8785 canonicalization."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


def digest(value):
    if type(value) is not bytes:
        raise ValueError("Exact bytes required")
    return hashlib.sha256(value).hexdigest()


def identity(value):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError("Nonempty stripped identity required")
    return value


def tensor_extent(shape, dtype):
    if type(shape) is not tuple or any(type(d) is not int or d < 0 for d in shape):
        raise ValueError("Immutable exact nonnegative tensor dimensions required")
    if dtype not in WIDTH:
        raise ValueError("Demo supports only little-endian F32/F64")
    return math.prod(shape) * WIDTH[dtype]


def make_manifest(tensors, architecture, tokenizer):
    """Exact raw-tensor payload sizes; no executable object deserialization."""
    if not isinstance(tensors, dict) or not tensors:
        raise ValueError("Nonempty tensor map required")
    if not isinstance(architecture, dict) or not architecture:
        raise ValueError("Explicit architecture config required")
    identity(tokenizer)
    canonical_json(architecture)
    records = {}
    for name, (shape, dtype, payload) in sorted(tensors.items()):
        identity(name)
        nbytes = tensor_extent(shape, dtype)
        if type(payload) is not bytes or len(payload) != nbytes:
            raise ValueError("Tensor byte extent does not match shape/dtype")
        records[name] = {
            "shape": list(shape),
            "dtype": dtype,
            "nbytes": nbytes,
            "sha256": digest(payload),
        }
    return {
        "format": FORMAT,
        "byte_order": "little",
        "layout": "contiguous-row-major",
        "architecture": architecture,
        "tokenizer": tokenizer,
        "tensors": records,
    }


def manifest_id(manifest):
    return digest(canonical_json(manifest))


def verify_artifact(manifest, blobs, architecture, tokenizer, specs, trusted_id):
    """Fail closed on content, schema, exact tensor set, config and pinned identity."""
    if not isinstance(manifest, dict) or set(manifest) != {
        "format",
        "byte_order",
        "layout",
        "architecture",
        "tokenizer",
        "tensors",
    }:
        raise ValueError("Exact manifest schema required")
    if (
        manifest["format"] != FORMAT
        or manifest["byte_order"] != "little"
        or manifest["layout"] != "contiguous-row-major"
    ):
        raise ValueError("Unsupported tensor encoding")
    if (
        canonical_json(manifest["architecture"]) != canonical_json(architecture)
        or manifest["tokenizer"] != tokenizer
    ):
        raise ValueError("Architecture/tokenizer contract mismatch")
    if (
        not isinstance(manifest["tensors"], dict)
        or set(manifest["tensors"]) != set(specs)
        or set(blobs) != set(specs)
    ):
        raise ValueError("Missing/unexpected tensor identity")
    if manifest_id(manifest) != trusted_id:
        raise ValueError("Manifest differs from independently pinned identity")
    for name, (shape, dtype) in specs.items():
        meta = manifest["tensors"][name]
        if not isinstance(meta, dict) or set(meta) != {
            "shape",
            "dtype",
            "nbytes",
            "sha256",
        }:
            raise ValueError("Exact tensor metadata schema required")
        size = tensor_extent(shape, dtype)
        if (
            type(meta["shape"]) is not list
            or meta["shape"] != list(shape)
            or meta["dtype"] != dtype
        ):
            raise ValueError("Expected tensor shape/dtype mismatch")
        if (
            any(type(d) is not int for d in meta["shape"])
            or type(meta["nbytes"]) is not int
            or meta["nbytes"] != size
        ):
            raise ValueError("Invalid tensor byte extent")
        if (
            type(blobs[name]) is not bytes
            or len(blobs[name]) != size
            or digest(blobs[name]) != meta["sha256"]
        ):
            raise ValueError("Corrupt tensor bytes")
    return True


def linear_reload(manifest, blobs, trusted_id, x):
    """Independent raw-byte inference loader for a fixed two-input/two-output fixture."""
    config = {"kind": "linear", "inputs": 2, "outputs": 2, "bias": True}
    specs = {"weight": ((2, 2), "F32"), "bias": ((2,), "F32")}
    verify_artifact(manifest, blobs, config, "nt-demo-v1", specs, trusted_id)
    if len(x) != 2:
        raise ValueError("Two features required")
    w = struct.unpack("<4f", blobs["weight"])
    b = struct.unpack("<2f", blobs["bias"])
    if not all(math.isfinite(v) for v in w + b):
        raise ValueError("Nonfinite inference tensor")
    return tuple(
        math.fsum((w[2 * i] * finite(x[0]), w[2 * i + 1] * finite(x[1]), b[i]))
        for i in range(2)
    )


def artifact_fixture():
    config = {"kind": "linear", "inputs": 2, "outputs": 2, "bias": True}
    blobs = {
        "weight": struct.pack("<4f", 1, 2, -1, 0.5),
        "bias": struct.pack("<2f", 0.25, -0.5),
    }
    tensors = {
        "weight": ((2, 2), "F32", blobs["weight"]),
        "bias": ((2,), "F32", blobs["bias"]),
    }
    m = make_manifest(tensors, config, "nt-demo-v1")
    return m, blobs, manifest_id(m)


def results():
    numerators = ((2.0, 6.0), (9.0, 3.0), (0.0, 0.0))
    masses = (2.0, 3.0, 0.0)
    correct = weighted_reduce(numerators, masses)
    bad = allreduce_mean(((1.0, 3.0), (3.0, 1.0), (0.0, 0.0)))
    pieces = shard(range(10), 3)
    m, b, h = artifact_fixture()
    return {
        "weighted_gradient": correct,
        "incorrect_rank_mean": bad,
        "ddp_backward_scale": ddp_local_scales(masses),
        "shards": [
            {"rank": s.rank, "start": s.start, "size": len(s.values)} for s in pieces
        ],
        "reconstruct_ok": reconstruct(pieces) == tuple(range(10)),
        "matrix_output": row_parallel(
            ((1.0, 2.0, 3.0),), ((1.0, 2.0), (3.0, 4.0), (5.0, 6.0)), 4
        ),
        "manifest_id": h,
        "linear_logits": linear_reload(m, b, h, (2.0, -1.0)),
        "scope": "local collective/matrix algebra and fixed raw-byte demo loader; not NCCL/FSDP/ZeRO benchmark or safetensors implementation",
    }


TABLES = [("shards", ["Rank", "Offset", "Extent"], ["rank", "start", "size"], "rrr")]
PLOTS = []
LISTINGS = [
    "weighted_reduce",
    "reconstruct",
    "row_parallel",
    "verify_artifact",
    "linear_reload",
]

if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
