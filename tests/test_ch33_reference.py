"""Independent arithmetic, malformed inputs, isolation and lifetime falsifiers."""

from dataclasses import replace
from fractions import Fraction
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evod33_local_reference", ROOT / "drafts/ch33/reference.py"
)
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def fixture(tokens=(1, 2, 1), capacity=8):
    p = r.pool_module()
    model = p.native_module().tiny_model()
    context = r.context_for(model, "tenant-a")
    pool = p.Pool("test", capacity, context.width, context.artifact)
    owner = (context.tenant, "source")
    handle = pool.allocate(owner)
    prefix, _ = r.advance(pool, handle, owner, model, context, (), tokens)
    cp = r.capture(pool, handle, owner, context, prefix)
    return p, model, context, pool, owner, handle, cp


def resign(body):
    wire = r.canonical(body)
    return r.Checkpoint(wire, r.sha(wire))


def manual_hidden(tokens):
    # Exact rational oracle: no call into the checkpoint or native recurrence.
    h = [Fraction(0), Fraction(0)]
    for token in tokens:
        h = [h[0] / 2 + Fraction(token == 1, 2), h[1] / 4 + Fraction(token == 2, 2)]
    return tuple(float(x) for x in h)


def test_boundary_and_known_branch_values():
    values = r.results()
    assert [(x["h1"], x["h2"]) for x in values["branches"]] == [
        (0.625, 0.125),
        (0.3125, 0.03125),
        (0.3125, 0.53125),
    ]
    assert values["replay_audit"] is True


def test_restore_every_cut_and_all_short_suffixes():
    p, model, context, pool, owner, handle, _ = fixture((), 2)
    for length in range(4):
        for tokens in product(range(3), repeat=length):
            pool.write(handle, owner, p.Snapshot(0, (0.0, 0.0)))
            prefix, _ = r.advance(pool, handle, owner, model, context, (), tokens)
            assert pool.read(handle, owner).hidden == manual_hidden(tokens)
            cp = r.capture(pool, handle, owner, context, prefix)
            assert r.replay_audit(cp, model, context)
            for suffix in product(range(3), repeat=2):
                who = (context.tenant, "continuation")
                (branch,) = r.restore_many(cp, pool, (who,), context, prefix)
                full, logits = r.advance(
                    pool, branch, who, model, context, prefix, suffix
                )
                hidden = pool.read(branch, who).hidden
                assert hidden == manual_hidden(tokens + suffix)
                assert full == tokens + suffix
                assert logits[-1] == (0.0, hidden[0] - hidden[1], hidden[1] - hidden[0])
                pool.release(branch, who)


def test_data_only_deterministic_roundtrip_and_decoded_mutation_isolated():
    _, _, context, pool, owner, handle, cp = fixture()
    assert cp == r.capture(pool, handle, owner, context, (1, 2, 1))
    body = r.decode(cp)
    body["hidden"][0] = 900
    body["tokens"][0] = 0
    assert r.decode(cp)["hidden"] == [0.625, 0.125]
    assert r.checked(cp, context, (1, 2, 1))["position"] == 3


@pytest.mark.parametrize(
    "field,value",
    [
        ("format", "other"),
        ("position", True),
        ("position", -1),
        ("position", 2),
        ("position", 3.0),
        ("tokens", [1, 2, True]),
        ("tokens", [1, 2, -1]),
        ("tokens", [1, 2, 3]),
        ("tokens", [1, 2, 1.0]),
        ("tokens", None),
        ("hidden", []),
        ("hidden", [True, 0.0]),
        ("hidden", ["1", 0.0]),
        ("hidden", [1.0]),
        ("hidden", [1.0, 2.0, 3.0]),
        ("context", []),
    ],
)
def test_rehashed_malformed_schema_is_rejected(field, value):
    *_, cp = fixture()
    body = r.decode(cp)
    body[field] = value
    with pytest.raises(ValueError):
        r.decode(resign(body))


@pytest.mark.parametrize(
    "field,value",
    [
        ("width", 0),
        ("width", True),
        ("width", r.MAX_WIDTH + 1),
        ("vocabulary", 1),
        ("vocabulary", True),
        ("tenant", ""),
        ("artifact", "name"),
        ("tokenizer", "ABC"),
        ("semantics", ""),
        ("dtype", "float32"),
    ],
)
def test_context_schema_is_strict_even_with_valid_digest(field, value):
    *_, cp = fixture()
    body = r.decode(cp)
    body["context"][field] = value
    with pytest.raises(ValueError):
        r.decode(resign(body))


@pytest.mark.parametrize(
    "raw",
    [
        b"null",
        b"[]",
        b"{}",
        b"{",
        b"\xff",
        b'{"format":1,"format":2}',
        b'{"hidden":[NaN]}',
        b'{"hidden":[Infinity]}',
        b'{"hidden":[-Infinity]}',
    ],
)
def test_untrusted_wire_rejected(raw):
    with pytest.raises(ValueError):
        r.decode(r.Checkpoint(raw, r.sha(raw)))


def test_overflow_numbers_unknown_fields_and_missing_fields():
    *_, cp = fixture()
    for raw in (
        cp.wire.replace(b"0.625", b"1e999"),
        cp.wire.replace(b"0.625", b"9" * 4000),
    ):
        with pytest.raises(ValueError):
            r.decode(r.Checkpoint(raw, r.sha(raw)))
    body = r.decode(cp)
    for modified in (
        {**body, "extra": 0},
        {k: v for k, v in body.items() if k != "tokens"},
    ):
        with pytest.raises(ValueError):
            r.decode(resign(modified))
    body["context"]["extra"] = 0
    with pytest.raises(ValueError):
        r.decode(resign(body))


def test_corruption_and_noncanonical_wire_rejected():
    *_, cp = fixture()
    with pytest.raises(ValueError, match="digest"):
        r.decode(replace(cp, wire=cp.wire.replace(b"0.625", b"0.626")))
    raw = json.dumps(r.decode(cp), indent=2).encode()
    with pytest.raises(ValueError, match="noncanonical"):
        r.decode(r.Checkpoint(raw, r.sha(raw)))


def test_hidden_integer_cannot_silently_round_on_restore():
    *_, cp = fixture()
    body = r.decode(cp)
    body["hidden"][0] = 2**53 + 1
    with pytest.raises(ValueError, match="precision"):
        r.decode(resign(body))


def test_bounds_reject_before_json_loader(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("parser must not be reached")

    monkeypatch.setattr(r.json, "loads", forbidden)
    for wire in (b"", b" " * (r.MAX_WIRE + 1), bytearray(b"{}")):
        with pytest.raises(ValueError):
            r.decode(r.Checkpoint(wire, "a" * 64))


def test_nested_wire_fails_without_crashing():
    raw = b"[" * 2000 + b"0" + b"]" * 2000
    with pytest.raises(ValueError):
        r.decode(r.Checkpoint(raw, r.sha(raw)))


@pytest.mark.parametrize(
    "field,value",
    [
        ("tenant", "tenant-b"),
        ("artifact", "f" * 64),
        ("semantics", "v-next"),
        ("tokenizer", "f" * 64),
        ("width", 3),
        ("vocabulary", 4),
    ],
)
def test_context_and_prefix_participate_in_identity(field, value):
    _, _, context, _, _, _, cp = fixture()
    changed = replace(context, **{field: value})
    assert r.prefix_key(changed, (1, 2, 1)) != r.prefix_key(context, (1, 2, 1))
    with pytest.raises(ValueError, match="context"):
        r.checked(cp, changed, (1, 2, 1))
    with pytest.raises(ValueError, match="prefix"):
        r.checked(cp, context, (1, 1, 2))


def test_native_context_rejects_unimplemented_semantics():
    p = r.pool_module()
    with pytest.raises(ValueError, match="unsupported"):
        r.context_for(p.native_module().tiny_model(), "tenant-a", "future-model")


def test_self_consistent_forgery_is_not_authenticated_or_replay_proven():
    _, model, context, _, _, _, cp = fixture()
    body = r.decode(cp)
    body["hidden"][0] = 11.0
    forged = resign(body)
    assert r.checked(forged, context, (1, 2, 1))
    assert not r.replay_audit(forged, model, context)


def test_capture_refuses_pins_foreign_owner_wrong_position_and_retirement():
    _, _, context, pool, owner, handle, _ = fixture()
    before = pool.read(handle, owner)
    with pytest.raises(ValueError, match="position"):
        r.capture(pool, handle, owner, context, (1, 2))
    with pytest.raises(PermissionError):
        r.capture(pool, handle, ("tenant-b", "x"), context, (1, 2, 1))
    pin = pool.pin(handle, owner)
    with pytest.raises(RuntimeError, match="quiescent"):
        r.capture(pool, handle, owner, context, (1, 2, 1))
    pool.release(handle, owner)
    with pytest.raises(RuntimeError, match="retiring"):
        r.capture(pool, handle, owner, context, (1, 2, 1))
    assert pool.complete(pin, owner, None) is False
    assert before.position == 3


def test_restore_never_resurrects_old_generation():
    _, _, context, pool, owner, handle, cp = fixture(capacity=1)
    pool.release(handle, owner)
    new_owner = (context.tenant, "fresh")
    (fresh,) = r.restore_many(cp, pool, [new_owner], context, (1, 2, 1))
    assert fresh.slot == handle.slot and fresh.generation != handle.generation
    assert pool.read(fresh, new_owner).hidden == (0.625, 0.125)
    with pytest.raises(RuntimeError, match="stale"):
        pool.read(handle, owner)


@pytest.mark.parametrize(
    "owners",
    [
        [],
        [("tenant-a", "source")],
        [("tenant-a", "a"), ("tenant-a", "a")],
        [("tenant-b", "other")],
        [("tenant-a", "")],
    ],
)
def test_branch_preflight_failure_has_no_partial_allocation(owners):
    _, _, context, pool, owner, handle, cp = fixture()
    before, state = pool.stats(), pool.read(handle, owner)
    with pytest.raises((ValueError, PermissionError)):
        r.restore_many(cp, pool, owners, context, (1, 2, 1))
    assert pool.stats() == before and pool.read(handle, owner) == state


def test_group_capacity_includes_retiring_pinned_storage():
    _, _, context, pool, owner, handle, cp = fixture(capacity=2)
    pin = pool.pin(handle, owner)
    pool.release(handle, owner)
    before = pool.stats()
    with pytest.raises(MemoryError):
        r.restore_many(
            cp, pool, [("tenant-a", "a"), ("tenant-a", "b")], context, (1, 2, 1)
        )
    assert pool.stats() == before
    pool.complete(pin, owner)
    branches = r.restore_many(
        cp, pool, [("tenant-a", "a"), ("tenant-a", "b")], context, (1, 2, 1)
    )
    assert len(branches) == 2


def test_independent_suffix_state_and_tensor_storage_after_eviction():
    p, model, context, pool, owner, source, cp = fixture()
    owners = [("tenant-a", "left"), ("tenant-a", "right")]
    left, right = r.restore_many(cp, pool, owners, context, (1, 2, 1))
    tensor_left = p.to_native(pool, left, owners[0]).hidden
    tensor_right = p.to_native(pool, right, owners[1]).hidden
    assert tensor_left.data_ptr() != tensor_right.data_ptr()
    tensor_left[0] = 999
    assert pool.read(left, owners[0]).hidden == pool.read(right, owners[1]).hidden
    r.advance(pool, left, owners[0], model, context, (1, 2, 1), (0,))
    assert pool.read(right, owners[1]).hidden == (0.625, 0.125)
    assert pool.read(source, owner).hidden == (0.625, 0.125)
    cache = r.PrefixCache(len(cp.wire))
    cache.put(cp, context, (1, 2, 1))
    other = r.capture(pool, left, owners[0], context, (1, 2, 1, 0))
    # Bigger checkpoint cannot fit: failure must not evict the previous entry.
    with pytest.raises(MemoryError):
        cache.put(other, context, (1, 2, 1, 0))
    assert cache.longest(context, (1, 2, 1))[1] == cp
    roomy = r.PrefixCache(max(len(cp.wire), len(other.wire)))
    roomy.put(cp, context, (1, 2, 1))
    roomy.put(other, context, (1, 2, 1, 0))
    assert roomy.longest(context, (1, 2, 1))[1] is None
    assert pool.read(right, owners[1]).hidden == (0.625, 0.125)


def test_inference_reload_does_not_preserve_autograd():
    p, model, context, pool, owner, handle, cp = fixture()
    model.embedding.requires_grad_(True)
    result = p.to_native(pool, handle, owner)
    assert not result.hidden.requires_grad and result.hidden.grad_fn is None
    assert r.replay_audit(cp, model, context)
    r.advance(pool, handle, owner, model, context, (1, 2, 1), (2,))
    assert not p.to_native(pool, handle, owner).hidden.requires_grad


def test_invalid_suffix_and_changed_model_do_not_install_partial_state():
    _, model, context, pool, owner, handle, _ = fixture()
    before = pool.read(handle, owner)
    for suffix in ((0, True), (0, -1), (0, 3), (1,) * (r.MAX_TOKENS + 1)):
        with pytest.raises(ValueError):
            r.advance(pool, handle, owner, model, context, (1, 2, 1), suffix)
        assert pool.read(handle, owner) == before
    model.head[0, 0] += 0.125
    with pytest.raises(ValueError, match="context"):
        r.advance(pool, handle, owner, model, context, (1, 2, 1), (0,))
    assert pool.read(handle, owner) == before


def test_longest_prefix_and_tenant_miss():
    _, _, context, pool, owner, handle, cp = fixture()
    cache = r.PrefixCache(2000)
    cache.put(cp, context, (1, 2, 1))
    assert cache.longest(context, (1, 2, 1, 2)) == (3, cp)
    assert cache.longest(context, (1, 2, 0))[1] is None
    assert cache.longest(replace(context, tenant="tenant-b"), (1, 2, 1))[1] is None
    empty = r.PrefixCache(2000)
    assert empty.longest(context, ())[1] is None


def test_zero_length_checkpoint_is_a_real_hit_not_a_miss():
    _, _, context, _, _, _, cp = fixture(())
    cache = r.PrefixCache(2000)
    cache.put(cp, context, ())
    assert cache.longest(context, (1, 2)) == (0, cp)


def test_corrupted_cache_hit_and_conflicting_prefix_rejected():
    _, _, context, _, _, _, cp = fixture()
    cache = r.PrefixCache(2000)
    key = cache.put(cp, context, (1, 2, 1))
    body = r.decode(cp)
    body["hidden"][0] = 7.0
    with pytest.raises(ValueError, match="conflicting"):
        cache.put(resign(body), context, (1, 2, 1))
    cache._items[key] = replace(cp, sha256="0" * 64)
    with pytest.raises(ValueError, match="digest"):
        cache.longest(context, (1, 2, 1))


def test_injected_hash_collision_cannot_select_a_wrong_prefix(monkeypatch):
    _, _, context, _, _, _, cp = fixture()
    monkeypatch.setattr(r, "prefix_key", lambda *args: "collision")
    cache = r.PrefixCache(2000)
    cache.put(cp, context, (1, 2, 1))
    with pytest.raises(ValueError, match="prefix"):
        cache.longest(context, (1, 2, 2))


def test_lru_eviction_touches_a_hit_and_budget_is_exact_wire_bytes():
    _, model, context, pool, owner, handle, cp1 = fixture((1,))
    prefix, _ = r.advance(pool, handle, owner, model, context, (1,), (2,))
    cp2 = r.capture(pool, handle, owner, context, prefix)
    prefix, _ = r.advance(pool, handle, owner, model, context, prefix, (1,))
    cp3 = r.capture(pool, handle, owner, context, prefix)
    cache = r.PrefixCache(len(cp1.wire) + len(cp3.wire))
    cache.put(cp1, context, (1,))
    cache.put(cp2, context, (1, 2))
    assert cache.longest(context, (1,))[1] == cp1
    cache.put(cp3, context, (1, 2, 1))
    assert r.prefix_key(context, (1, 2)) not in cache._items
    assert cache.bytes == len(cp1.wire) + len(cp3.wire) <= cache.max_bytes


def test_actual_native_error_contraction_does_not_guarantee_argmax():
    p, model, _, pool, owner, handle, _ = fixture()
    native = p.native_module()
    original = p.to_native(pool, handle, owner)
    perturbed = replace(
        original,
        hidden=original.hidden
        + native.torch.tensor([0.125, -0.125], dtype=native.torch.float64),
    )
    for k, token in enumerate((0, 2, 1, 0), 1):
        original = native.native_step(model, original, token, owner).state
        perturbed = native.native_step(model, perturbed, token, owner).state
        expected = native.torch.tensor(
            [0.125 * 0.5**k, -0.125 * 0.25**k], dtype=native.torch.float64
        )
        assert native.torch.equal(perturbed.hidden - original.hidden, expected)
    zero = native.construct(model, owner).hidden
    epsilon = native.torch.tensor([2**-20, 0.0], dtype=native.torch.float64)
    assert int(native.torch.argmax(zero @ model.head)) == 0
    assert int(native.torch.argmax((zero + epsilon) @ model.head)) == 1


def test_checkpoint_cost_matches_literal_storage_enumeration():
    for length in range(1, 65):
        for interval in range(1, length + 1):
            out = r.checkpoint_cost(length, interval, 8)
            points = list(range(interval, length + 1, interval))
            assert out["state_bytes"] == sum(8 * 8 for _ in points)
            assert out["token_bytes"] == sum(4 * t for t in points)
            assert out["expected_replay"] == sum(range(interval)) / interval


def test_missing_auxiliary_clock_is_not_a_sufficient_snapshot():
    # Same stored h, different unrecorded phase: equal tensors do not imply continuation.
    h = 0

    def next_output(phase):
        return h + (1 if phase == 0 else -1)

    assert next_output(0) != next_output(1)


def test_fixture_assets_and_literal_listings_match_code():
    spec = importlib.util.spec_from_file_location(
        "ch33_builder", ROOT / "drafts/ch33/build.py"
    )
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    for path, expected in builder.derived().items():
        assert path.read_text() == expected
    source = (ROOT / "drafts/ch33/reference.py").read_text()
    for name in r.LISTINGS:
        assert (ROOT / "build/ch33" / (name + ".py")).read_text().strip() in source
