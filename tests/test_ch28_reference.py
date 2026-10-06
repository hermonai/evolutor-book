"""Independent derivative, coverage, matrix, and byte-loading oracles."""

from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys

import pytest
import torch

p = Path(__file__).parents[1] / "drafts/ch28/reference.py"
spec = importlib.util.spec_from_file_location("evo28", p)
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def test_weighted_collective_independent_autograd_and_scalar_derivative():
    theta = torch.tensor([0.5, -0.25], dtype=torch.float64, requires_grad=True)
    x = torch.tensor(
        [[1.0, 2.0], [3.0, -1.0], [2.0, 0.0], [-1.0, 4.0]], dtype=torch.float64
    )
    y = torch.tensor([1.0, -2.0, 0.5, 3.0], dtype=torch.float64)
    weights = torch.tensor([1.0, 2.0, 3.0, 0.0], dtype=torch.float64)
    loss = (weights * (x @ theta - y) ** 2).sum() / weights.sum()
    expected = torch.autograd.grad(loss, theta)[0]
    numerators = []
    masses = []
    for ids in ([0, 1], [2], [3]):
        n = (weights[ids] * (x[ids] @ theta - y[ids]) ** 2).sum()
        numerators.append(tuple(torch.autograd.grad(n, theta)[0].tolist()))
        masses.append(float(weights[ids].sum()))
    got = r.weighted_reduce(numerators, masses)
    manual = [
        sum(
            2
            * float(weights[i])
            * (float(x[i] @ theta.detach()) - float(y[i]))
            * float(x[i, j])
            for i in range(4)
        )
        / 6
        for j in range(2)
    ]
    assert got == pytest.approx(expected.tolist())
    assert got == pytest.approx(manual)
    scales = r.ddp_local_scales(masses)
    assert r.allreduce_mean(
        [tuple(s * v for v in g) for s, g in zip(scales, numerators)]
    ) == pytest.approx(got)


def test_rank_means_are_a_different_objective():
    good = r.weighted_reduce(((2, 6), (9, 3), (0, 0)), (2, 3, 0))
    bad = r.allreduce_mean(((1, 3), (3, 1), (0, 0)))
    assert good == pytest.approx((2.2, 1.8))
    assert bad == pytest.approx((4 / 3, 4 / 3))
    assert bad != pytest.approx(good)


def test_rank_permutation_and_global_weight_scale():
    ns = ((2, 6), (9, 3), (0, 0))
    ms = (2, 3, 0)
    assert r.weighted_reduce(ns[::-1], ms[::-1]) == pytest.approx(
        r.weighted_reduce(ns, ms)
    )
    assert r.weighted_reduce(
        tuple(tuple(7 * v for v in g) for g in ns), tuple(7 * v for v in ms)
    ) == pytest.approx(r.weighted_reduce(ns, ms))


@pytest.mark.parametrize(
    "ns,ms",
    [
        ((), ()),
        (((1,),), (0,)),
        (((1,),), (-1,)),
        (((1,),), (True,)),
        (((1,),), (float("inf"),)),
        (((1,), ()), (1, 1)),
    ],
)
def test_collective_domain(ns, ms):
    with pytest.raises(ValueError):
        r.weighted_reduce(ns, ms)


@pytest.mark.parametrize("n,world", [(10, 3), (1, 4), (0, 3), (8, 1), (7, 7)])
def test_shard_coverage_independent_arithmetic(n, world):
    parts = r.shard(range(n), world)
    assert r.reconstruct(parts[::-1]) == tuple(range(n))
    for s in parts:
        q, rem = divmod(n, world)
        assert s.start == s.rank * q + min(s.rank, rem)
        assert len(s.values) == q + int(s.rank < rem)


@pytest.mark.parametrize(
    "field,value",
    [
        ("rank", True),
        ("rank", 0),
        ("start", 0),
        ("start", True),
        ("world", True),
        ("total", 10.0),
        ("values", ()),
    ],
)
def test_reconstruction_rejects_mutated_descriptor(field, value):
    parts = list(r.shard(range(10), 3))
    parts[1] = replace(parts[1], **{field: value})
    with pytest.raises(ValueError):
        r.reconstruct(parts)


def test_reconstruction_missing_extra_ranks_and_world_domain():
    parts = r.shard(range(10), 3)
    for bad in (parts[:2], parts + (parts[0],)):
        with pytest.raises(ValueError):
            r.reconstruct(bad)
    for world in (0, -1, True, 1.5):
        with pytest.raises(ValueError):
            r.shard(range(3), world)


@pytest.mark.parametrize("world", [1, 2, 3, 5])
def test_row_parallel_independent_scalar_and_torch_oracle(world):
    x = ((1.0, 2.0, 3.0), (-2.0, 0.0, 4.0))
    w = ((1.0, 2.0), (3.0, 4.0), (5.0, 6.0))
    expected = tuple(
        tuple(sum(x[i][k] * w[k][j] for k in range(3)) for j in range(2))
        for i in range(2)
    )
    assert r.row_parallel(x, w, world) == expected
    assert torch.allclose(
        torch.tensor(r.row_parallel(x, w, world)), torch.tensor(x) @ torch.tensor(w)
    )
    assert r.matmul(x, w) == expected


def test_sum_not_mean_matrix_partials():
    assert r.row_parallel(((1, 2, 3),), ((1, 2), (3, 4), (5, 6)), 4) == ((22.0, 28.0),)
    assert (22 / 4, 28 / 4) != (22, 28)


def specs():
    return {"weight": ((2, 2), "F32"), "bias": ((2,), "F32")}


def validate(m, b, h):
    return r.verify_artifact(
        m,
        b,
        {"kind": "linear", "inputs": 2, "outputs": 2, "bias": True},
        "nt-demo-v1",
        specs(),
        h,
    )


def test_fixture_independent_bytes_and_inference():
    m, b, h = r.artifact_fixture()
    assert validate(m, b, h)
    assert r.linear_reload(m, b, h, (2, -1)) == (0.25, -3.0)
    assert struct.unpack("<4f", b["weight"]) == (1, 2, -1, 0.5)


@pytest.mark.parametrize("mutation", ["truncate", "extend", "flip", "missing", "extra"])
def test_blob_corruption_and_exact_tensor_set(mutation):
    m, b, h = r.artifact_fixture()
    if mutation == "truncate":
        b["weight"] = b["weight"][:-1]
    if mutation == "extend":
        b["weight"] += b"\0"
    if mutation == "flip":
        b["weight"] = bytes([b["weight"][0] ^ 1]) + b["weight"][1:]
    if mutation == "missing":
        del b["bias"]
    if mutation == "extra":
        b["unexpected"] = b""
    with pytest.raises(ValueError):
        validate(m, b, h)


@pytest.mark.parametrize(
    "mutation",
    ["shape", "dtype", "nbytes", "boolshape", "key", "archfloat", "tokenizer", "order"],
)
def test_manifest_schema_even_when_rehashed(mutation):
    m, b, _ = r.artifact_fixture()
    if mutation == "shape":
        m["tensors"]["weight"]["shape"] = [4]
    if mutation == "dtype":
        m["tensors"]["weight"]["dtype"] = "F64"
    if mutation == "nbytes":
        m["tensors"]["weight"]["nbytes"] = 15
    if mutation == "boolshape":
        m["tensors"]["bias"]["shape"] = [True]
    if mutation == "key":
        m["executable"] = "ignored?"
    if mutation == "archfloat":
        m["architecture"]["inputs"] = 2.0
    if mutation == "tokenizer":
        m["tokenizer"] = "other"
    if mutation == "order":
        m["byte_order"] = "big"
    with pytest.raises(ValueError):
        validate(m, b, r.manifest_id(m))


def test_coherent_forgery_rejected_only_with_independent_pin():
    m, b, h = r.artifact_fixture()
    b["weight"] = struct.pack("<4f", 9, 2, -1, 0.5)
    m["tensors"]["weight"]["sha256"] = r.digest(b["weight"])
    with pytest.raises(ValueError, match="pinned"):
        validate(m, b, h)
    # A replaced pin supplied by the same attacker restores integrity but not trust.
    assert validate(m, b, r.manifest_id(m))
    assert r.linear_reload(m, b, r.manifest_id(m), (2, -1)) == (16.25, -3.0)


def test_format_integrity_is_not_finite_inference():
    m, b, _ = r.artifact_fixture()
    b["bias"] = struct.pack("<2f", float("nan"), -0.5)
    m["tensors"]["bias"]["sha256"] = r.digest(b["bias"])
    h = r.manifest_id(m)
    assert validate(m, b, h)
    with pytest.raises(ValueError, match="Nonfinite"):
        r.linear_reload(m, b, h, (2, -1))


def test_scalar_empty_tensor_and_payload_extent():
    assert r.tensor_extent((), "F32") == 4
    assert r.tensor_extent((0, 3), "F64") == 0
    for shape in ((True,), (-1,), [2], (2.0,)):
        with pytest.raises(ValueError):
            r.tensor_extent(shape, "F32")
    with pytest.raises(ValueError):
        r.make_manifest({"a": ((2,), "F32", b"1234")}, {"kind": "x"}, "token")


def test_clean_process_reload_no_training_object_state():
    m, b, h = r.artifact_fixture()
    payload = json.dumps(
        {"manifest": m, "blobs": {k: v.hex() for k, v in b.items()}, "pin": h}
    )
    code = """import importlib.util,json,sys
s=importlib.util.spec_from_file_location('fresh',sys.argv[1])
r=importlib.util.module_from_spec(s);sys.modules[s.name]=r;s.loader.exec_module(r)
d=json.loads(sys.stdin.read())
print(json.dumps(r.linear_reload(d['manifest'],{k:bytes.fromhex(v) for k,v in d['blobs'].items()},d['pin'],(2,-1))))
"""
    out = subprocess.check_output(
        [sys.executable, "-c", code, str(p)], input=payload, text=True
    )
    assert json.loads(out) == [0.25, -3.0]


def test_canonical_profile_and_manifest_map_order():
    m, b, h = r.artifact_fixture()
    reordered = {k: m[k] for k in reversed(m)}
    assert r.manifest_id(reordered) == h
    assert r.canonical_json({"x": 1}) != r.canonical_json({"x": 1.0})
    with pytest.raises(ValueError):
        r.canonical_json({"x": float("nan")})
