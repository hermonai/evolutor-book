from dataclasses import replace
import importlib.util
from pathlib import Path
import sys
import random
import pytest

spec = importlib.util.spec_from_file_location(
    "evo32", Path(__file__).parents[1] / "drafts/ch32/reference.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
OWNER = ("tenant-a", "r1")
DIGEST = "a" * 64


def pool(c=2, d=2):
    return m.Pool("same-display-name", c, d, DIGEST)


@pytest.mark.parametrize("bad", [True, 0, -1, 1.0, None])
def test_pool_dimensions(bad):
    with pytest.raises(ValueError):
        m.Pool("p", bad, 2, DIGEST)


@pytest.mark.parametrize("digest", ["model", "", "A" * 64, "a" * 63])
def test_artifact_domain(digest):
    with pytest.raises(ValueError):
        m.Pool("p", 1, 1, digest)


def test_equal_display_names_do_not_alias_identity():
    p, q = pool(), pool()
    h = p.allocate(OWNER)
    with pytest.raises(RuntimeError):
        q.read(h, OWNER)


@pytest.mark.parametrize(
    "change",
    [
        {"slot": -1},
        {"slot": True},
        {"generation": True},
        {"owner": ("tenant-b", "r1")},
        {"artifact": "b" * 64},
    ],
)
def test_handle_forgery(change):
    p = pool()
    h = p.allocate(OWNER)
    with pytest.raises((RuntimeError, PermissionError)):
        p.read(replace(h, **change), OWNER)


@pytest.mark.parametrize("owner", [("tenant-b", "r1"), ("tenant-a", "r2")])
def test_caller_identity_is_required(owner):
    p = pool()
    h = p.allocate(OWNER)
    with pytest.raises(PermissionError):
        p.read(h, owner)
    with pytest.raises(PermissionError):
        p.release(h, owner)


def test_write_failure_atomicity():
    p = pool()
    h = p.allocate(OWNER)
    before = p.read(h, OWNER)
    with pytest.raises(ValueError):
        p.write(h, OWNER, m.Snapshot(3, (float("nan"), 0)))
    assert p.read(h, OWNER) == before


@pytest.mark.parametrize(
    "snapshot",
    [
        m.Snapshot(-1, (0, 0)),
        m.Snapshot(True, (0, 0)),
        m.Snapshot(0, (1,)),
        m.Snapshot(0, (float("inf"), 0)),
    ],
)
def test_failed_allocation_does_not_reserve_slot(snapshot):
    p = pool(1)
    with pytest.raises(ValueError):
        p.allocate(OWNER, snapshot)
    assert p.stats()["free"] == 1


def test_storage_copy_not_input_alias():
    p = pool()
    values = [1.0, 2.0]
    h = p.allocate(OWNER, m.Snapshot(3, values))
    values[0] = 99
    assert p.read(h, OWNER).hidden == (1, 2)


def test_clone_independent_and_preserves_boundary():
    p = pool()
    a = p.allocate(OWNER, m.Snapshot(3, (1, 2)))
    other = ("tenant-a", "branch")
    b = p.clone(a, OWNER, other)
    p.write(b, other, m.Snapshot(4, (9, 9)))
    assert p.read(a, OWNER) == m.Snapshot(3, (1, 2))
    assert p.read(b, other) == m.Snapshot(4, (9, 9))


def test_cross_tenant_clone_rejected():
    p = pool()
    a = p.allocate(OWNER)
    with pytest.raises(PermissionError):
        p.clone(a, OWNER, ("tenant-b", "r2"))
    assert p.stats()["free"] == 1


def test_clone_capacity_failure_preserves_source():
    p = pool(1)
    a = p.allocate(OWNER, m.Snapshot(2, (1, 2)))
    with pytest.raises(MemoryError):
        p.clone(a, OWNER, ("tenant-a", "branch"))
    assert p.read(a, OWNER) == m.Snapshot(2, (1, 2))


def test_release_scrub_and_generation():
    p = pool(1)
    h = p.allocate(OWNER, m.Snapshot(5, (7, 8)))
    p.release(h, OWNER)
    fresh = p.allocate(("tenant-b", "r2"))
    assert fresh.slot == h.slot and fresh.generation == h.generation + 1
    assert p.read(fresh, fresh.owner) == m.Snapshot(0, (0, 0))
    with pytest.raises(RuntimeError):
        p.read(h, OWNER)


def test_pins_delay_reuse_and_cancel_candidate():
    p = pool(1)
    h = p.allocate(OWNER, m.Snapshot(3, (1, 2)))
    pin = p.pin(h, OWNER)
    p.release(h, OWNER)
    assert p.stats()["retiring"] == 1 and p.stats()["free"] == 0
    with pytest.raises(MemoryError):
        p.allocate(("tenant-b", "r2"))
    with pytest.raises(RuntimeError):
        p.read(h, OWNER)
    assert not p.complete(pin, OWNER, m.Snapshot(4, (9, 9)))
    assert p.stats()["free"] == 1
    fresh = p.allocate(("tenant-b", "r2"))
    assert p.read(fresh, fresh.owner).hidden == (0, 0)


def test_multiple_pins_all_must_settle():
    p = pool(1)
    h = p.allocate(OWNER)
    a, b = p.pin(h, OWNER), p.pin(h, OWNER)
    p.release(h, OWNER)
    assert not p.complete(a, OWNER) and p.stats()["free"] == 0
    assert not p.complete(b, OWNER) and p.stats()["free"] == 1


def test_version_fence_prevents_lost_update():
    p = pool(1)
    h = p.allocate(OWNER)
    a, b = p.pin(h, OWNER), p.pin(h, OWNER)
    assert p.complete(a, OWNER, m.Snapshot(1, (1, 2)))
    assert not p.complete(b, OWNER, m.Snapshot(1, (9, 9)))
    assert p.read(h, OWNER).hidden == (1, 2)


def test_write_forbidden_while_pinned():
    p = pool()
    h = p.allocate(OWNER)
    pin = p.pin(h, OWNER)
    with pytest.raises(RuntimeError):
        p.write(h, OWNER, m.Snapshot(1, (1, 2)))
    p.complete(pin, OWNER)


def test_candidate_position_failure_keeps_pin_for_explicit_discard():
    p = pool()
    h = p.allocate(OWNER)
    pin = p.pin(h, OWNER)
    with pytest.raises(ValueError):
        p.complete(pin, OWNER, m.Snapshot(2, (1, 2)))
    assert p.stats()["pins"] == 1
    assert not p.complete(pin, OWNER)
    assert p.stats()["pins"] == 0


def test_duplicate_completion_rejected():
    p = pool()
    h = p.allocate(OWNER)
    pin = p.pin(h, OWNER)
    p.complete(pin, OWNER)
    with pytest.raises(RuntimeError):
        p.complete(pin, OWNER)


def test_native_bridge_parity_and_no_alias():
    native = m.native_module()
    model = native.tiny_model()
    p = m.Pool("native", 1, 2, native.artifact_id(model))
    h = p.allocate(OWNER)
    state = m.to_native(p, h, OWNER)
    result = native.native_step(model, state, 1, OWNER)
    m.from_native(p, h, OWNER, model, result.state)
    copied = m.to_native(p, h, OWNER)
    assert copied.position == 1 and copied.hidden.tolist() == [0.5, 0]
    copied.hidden[0] = 99
    assert p.read(h, OWNER).hidden == (0.5, 0)


def test_bridge_wrong_artifact_rejected():
    native = m.native_module()
    model = native.tiny_model()
    p = pool()
    h = p.allocate(OWNER)
    state = native.construct(model, OWNER)
    with pytest.raises(ValueError):
        m.from_native(p, h, OWNER, model, state)


@pytest.mark.parametrize("seed", [0, 1, 7, 19])
def test_randomized_canary_reuse_against_ledger(seed):
    rng = random.Random(seed)
    p = pool(4)
    live = {}
    stale = []
    for step in range(200):
        if live and (len(live) == 4 or rng.random() < 0.5):
            owner = rng.choice(list(live))
            h, expected = live.pop(owner)
            assert p.read(h, owner) == expected
            p.release(h, owner)
            stale.append((h, owner))
        else:
            owner = ("t" + str(step % 3), "r" + str(step))
            expected = m.Snapshot(step, (float(step), -float(step)))
            h = p.allocate(owner, expected)
            live[owner] = (h, expected)
        stats = p.stats()
        assert stats["owned"] == len(live)
        assert stats["free"] + stats["owned"] + stats["retiring"] == 4
        for h, owner in stale[-4:]:
            with pytest.raises((RuntimeError, PermissionError)):
                p.read(h, owner)
    for owner, (h, _) in list(live.items()):
        p.release(h, owner)
    assert p.stats()["free"] == 4


def test_workspace_snapshot_and_close():
    w = m.Workspace(2)
    values = [1, 2]
    snap = w.use(values)
    values[0] = 99
    assert snap == (1, 2)
    w.close()
    w.close()
    assert w._values == (0, 0)
    with pytest.raises(RuntimeError):
        w.use([3, 4])
