import importlib.util
from pathlib import Path

path = Path(__file__).parents[1] / "drafts/ch46/reference.py"
spec = importlib.util.spec_from_file_location("r", path)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

def cluster():
    return r.Cluster([
        r.Worker("a", "z1", "dogma", 2),
        r.Worker("b", "z2", "dogma", 2),
        r.Worker("p", "z1", "prefill", 2),
        r.Worker("d", "z1", "decode", 2),
    ])

def test_zone_affinity():
    c = cluster()
    h = c.create_state("t", "m", 1, "dogma", [1], "z1")
    assert h.owner == "a"

def test_capacity_enforced():
    c = r.Cluster([r.Worker("a", "z", "dogma", 1)])
    c.create_state("t", "m", 1, "dogma", [1])
    try:
        c.create_state("t", "m", 1, "dogma", [2])
        assert False
    except RuntimeError:
        pass

def test_migration_preserves_payload():
    c = cluster()
    h = c.create_state("t", "m", 1, "dogma", [1, 2])
    n = c.migrate(h, "b")
    assert c.read(n) == (1, 2)

def test_migration_increments_epoch():
    c = cluster()
    h = c.create_state("t", "m", 1, "dogma", [1])
    assert c.migrate(h, "b").epoch == 1

def test_stale_handle_rejected():
    c = cluster()
    h = c.create_state("t", "m", 1, "dogma", [1])
    c.migrate(h, "b")
    try:
        c.read(h)
        assert False
    except RuntimeError:
        pass

def test_foreign_modified_handle_rejected():
    c = cluster()
    h = c.create_state("t", "m", 1, "dogma", [1])
    f = r.StateHandle(h.sid, "X", h.artifact, h.schema, h.owner, h.epoch)
    try:
        c.read(f)
        assert False
    except RuntimeError:
        pass

def test_destination_capacity():
    c = cluster()
    c.create_state("x", "m", 1, "dogma", [9], "z2")
    c.create_state("y", "m", 1, "dogma", [8], "z2")
    h = c.create_state("t", "m", 1, "dogma", [1], "z1")
    try:
        c.migrate(h, "b")
        assert False
    except RuntimeError:
        pass

def test_failed_owner_unreadable():
    c = cluster()
    h = c.create_state("t", "m", 1, "dogma", [1])
    c.fail_worker(h.owner)
    try:
        c.read(h)
        assert False
    except RuntimeError:
        pass

def test_recovery_new_epoch():
    c = cluster()
    h = c.create_state("t", "m", 1, "dogma", [1])
    c.fail_worker(h.owner)
    n = c.recover_by_replay(h, "b", [1])
    assert n.epoch == 1 and c.read(n) == (1,)

def test_recovery_requires_failed_owner():
    c = cluster()
    h = c.create_state("t", "m", 1, "dogma", [1])
    try:
        c.recover_by_replay(h, "b", [1])
        assert False
    except RuntimeError:
        pass

def test_pd_same_zone():
    c = cluster()
    p, d = c.pd_route("t", "m", "z1", "z1")
    assert c.workers[p].zone == c.workers[d].zone

def test_log_monotonic():
    c = cluster()
    h = c.create_state("t", "m", 1, "dogma", [1])
    c.migrate(h, "b")
    assert [e["seq"] for e in c.log.events] == list(range(len(c.log.events)))

def test_migration_events_order():
    c = cluster()
    h = c.create_state("t", "m", 1, "dogma", [1])
    c.migrate(h, "b")
    kinds = [e["kind"] for e in c.log.events]
    assert kinds.index("migration_prepare") < kinds.index("migration_commit")
