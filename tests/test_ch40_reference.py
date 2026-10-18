import importlib.util
from pathlib import Path
import sys
from dataclasses import replace
import pytest

spec = importlib.util.spec_from_file_location("evod40_test", Path(__file__).parents[1] / "drafts/ch40/reference.py")
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def fixture():
    m = r.Memory()
    a = m.put_event("t", "alpha beta")
    b = m.put_event("t", "beta gamma")
    s = m.summarize("t", (a.rid, b.rid), 2)
    return m, a, b, s


def test_roundtrip_provenance_and_nonresurrection():
    m, a, b, s = fixture()
    assert m.get("t", s.rid).sources == (a.rid, b.rid)
    m.forget("t", a.rid)
    m.forget("t", a.rid)
    replacement = m.put_event("t", a.payload)
    assert replacement.rid != a.rid
    with pytest.raises(KeyError):
        m.get("t", s.rid)
    assert m.get("t", replacement.rid).payload == a.payload


def test_transitive_derived_invalidation():
    m, a, b, s = fixture()
    s2 = m.summarize("t", (s.rid, b.rid))
    m.forget("t", a.rid)
    for rec in (a, s, s2):
        with pytest.raises(KeyError):
            m.get("t", rec.rid)
    assert not m.retrieve("t", "alpha", candidates=(a.rid, s.rid, s2.rid))


def test_expiry_exact_boundary_and_forget_expired():
    m = r.Memory()
    a = m.put_event("t", "alpha", ttl=2)
    s = m.summarize("t", (a.rid,))
    m.tick(1); assert m.get("t", s.rid)
    m.tick(1)
    for rec in (a, s):
        with pytest.raises(KeyError):
            m.get("t", rec.rid)
    m.forget("t", a.rid)
    assert a.rid in m.tombstones


def test_tenant_firewall():
    m, a, b, s = fixture()
    for rec in (a, s):
        with pytest.raises(PermissionError):
            m.get("evil", rec.rid)
        with pytest.raises(PermissionError):
            m.forget("evil", rec.rid)
    with pytest.raises(PermissionError):
        m.summarize("evil", (a.rid,))
    assert not m.retrieve("evil", "alpha", candidates=(a.rid, s.rid))


def test_compression_alias_independent_assigned_case():
    m = r.Memory()
    a = m.put_event("t", "alpha beta x")
    b = m.put_event("t", "alpha beta y")
    sa, sb = m.summarize("t", (a.rid,), 2), m.summarize("t", (b.rid,), 2)
    assert sa.payload == sb.payload == "alpha beta"
    assert sa.sources != sb.sources and sa.rid != sb.rid


@pytest.mark.parametrize("count", range(5))
@pytest.mark.parametrize("byte_budget", [0, 5, 10, 100])
def test_rehydrate_dual_budget(count, byte_budget):
    m, a, b, s = fixture()
    c = m.rehydrate("t", s.rid, count, byte_budget)
    assert len(c.records) <= count
    assert c.utf8_bytes == sum(len(x.payload.encode()) for x in c.records) <= byte_budget
    expected = () if count == 0 or byte_budget < 10 else (a.rid,)
    if count >= 2 and byte_budget >= 20:
        expected = (a.rid, b.rid)
    assert tuple(x.rid for x in c.records) == expected


def test_shared_ancestor_visited_once():
    m, a, b, s = fixture()
    s2 = m.summarize("t", (s.rid, a.rid))
    c = m.rehydrate("t", s2.rid, 64, 1000)
    assert tuple(x.rid for x in c.records) == (s.rid, a.rid, b.rid)


def test_utf8_payload_budget_and_no_authority():
    m = r.Memory()
    a = m.put_event("t", "授权 echo")
    size = len(a.payload.encode())
    with pytest.raises(MemoryError):
        m.promote("t", (a.rid,), size-1)
    c = m.promote("t", (a.rid,), size)
    assert c.utf8_bytes == size and c.authority == ()


def test_stale_index_rechecked_and_stable_tie():
    m = r.Memory()
    a = m.put_event("t", "alpha beta")
    b = m.put_event("t", "alpha")
    assert m.retrieve("t", "alpha beta")[0] == a
    m.forget("t", a.rid)
    assert m.retrieve("t", "alpha", candidates=(a.rid, b.rid, b.rid)) == (b,)


def test_corrupted_cycle_rejected():
    m, a, b, s = fixture()
    m.records[a.rid] = replace(a, sources=(s.rid,))
    with pytest.raises(KeyError):
        m.get("t", s.rid)


@pytest.mark.parametrize("bad", [-1, True, 1.5, 10001])
def test_bad_clock(bad):
    m = r.Memory()
    with pytest.raises(ValueError):
        m.tick(bad)
    assert m.clock == 0


def test_no_provenance_duplicate_or_missing_source():
    m, a, b, s = fixture()
    for ids in ((), (a.rid, a.rid), [a.rid]):
        with pytest.raises(ValueError):
            m.summarize("t", ids)
    with pytest.raises(KeyError):
        m.summarize("t", ("missing",))


def test_promotion_revalidates_after_forgetting():
    m, a, b, s = fixture()
    c = m.promote("t", (s.rid,), 1000)
    m.forget("t", a.rid)
    assert c.records[0].payload  # issued immutable context cannot be recalled
    with pytest.raises(KeyError):
        m.promote("t", (s.rid,), 1000)


def test_provenance_depth_bound_before_commit():
    m = r.Memory(); rec = m.put_event("t", "alpha")
    for _ in range(32):
        rec = m.summarize("t", (rec.rid,))
    before = len(m.records)
    with pytest.raises(MemoryError):
        m.summarize("t", (rec.rid,))
    assert len(m.records) == before and m.get("t", rec.rid)


def test_record_capacity_bound_before_commit():
    m = r.Memory()
    for _ in range(10000):
        m.put_event("t", "alpha")
    with pytest.raises(MemoryError):
        m.put_event("t", "alpha")
    assert len(m.records) == 10000
