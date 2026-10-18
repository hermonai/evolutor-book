import importlib.util
from pathlib import Path
import sys
from dataclasses import replace
import itertools
import pytest
import torch

P = Path(__file__).parents[1]/"drafts/ch36/reference.py"
S = importlib.util.spec_from_file_location("evod_batch_a_36", P)
r = importlib.util.module_from_spec(S)
sys.modules[S.name] = r
S.loader.exec_module(r)
torch.set_num_threads(1)


def make(n=3, page=2, capacity=20):
    m = r.native.tiny_model()
    a = r.PagedKV(m, capacity, page)
    owner = ("tenant", "parent")
    h = a.empty(owner)
    tokens = tuple(i % 4 for i in range(n))
    a.consume(h, owner, tokens)
    return m,a,h,owner,tokens


@pytest.mark.parametrize("page",[1,2,3,4,8])
@pytest.mark.parametrize("split",[1,2,3,4,5,6])
def test_all_layers_actual_model_chunk_parity(page,split):
    m,a,h,o,_ = make(0,page)
    tokens = (0,1,2,3,0,2)
    y = [a.consume(h,o,tokens[:split]),a.consume(h,o,tokens[split:])]
    torch.testing.assert_close(torch.cat(y),r.native.full_oracle(m,tokens),rtol=2e-12,atol=2e-12)
    _,expected = r.native.prefill(m,o,tokens)
    got = a.flatten(h,o)
    for x,z in zip(got.layers,expected.layers):
        torch.testing.assert_close(x.k,z.k,rtol=2e-12,atol=2e-12)
        torch.testing.assert_close(x.v,z.v,rtol=2e-12,atol=2e-12)
    a.audit()


@pytest.mark.parametrize("n",[1,2,3,4,5])
def test_forks_partial_cow_and_full_immutability(n):
    m,a,h,o,tokens = make(n)
    before = a.flatten(h,o)
    refs = a.state(h,o).pages
    c = a.fork(h,o,("tenant","child"))
    y = a.consume(c,("tenant","child"),(3,))
    assert a.state(h,o).pages == refs
    assert a.state(c,("tenant","child")).pages[:n//2] == refs[:n//2]
    if n % 2:
        assert a.state(c,("tenant","child")).pages[-1] != refs[-1]
    torch.testing.assert_close(y,r.native.full_oracle(m,tokens+(3,))[-1:],rtol=2e-12,atol=2e-12)
    assert before.seal == a.flatten(h,o).seal
    a.release(h,o)
    a.audit()
    a.release(c,("tenant","child"))
    assert a.audit()["used_pages"] == 0


def test_noncontiguous_physical_order():
    m,a,h,o,_ = make(2)
    junk = a.empty(("tenant","junk"))
    a.consume(junk,("tenant","junk"),(3,3))
    a.consume(h,o,(2,3))
    assert [x.page_id for x in a.state(h,o).pages] == [0,2]
    assert a.flatten(h,o).tokens == (0,1,2,3)
    a.audit()


def test_generation_stale_and_foreign_handle():
    _,a,h,o,_ = make(1)
    ref = a.state(h,o).pages[0]
    a.release(h,o)
    fresh = a.empty(("tenant","new"))
    a.consume(fresh,("tenant","new"),(0,))
    new_ref = a.state(fresh,("tenant","new")).pages[0]
    assert new_ref.page_id == ref.page_id and new_ref.generation == ref.generation+1
    with pytest.raises(ValueError): a.page(ref)
    with pytest.raises(ValueError): a.flatten(h,o)
    other = r.PagedKV(a.model,3,2)
    with pytest.raises(ValueError): other.flatten(fresh,("tenant","new"))


def test_prefix_cache_eviction_and_lru_ownership():
    _,a,h,o,tokens = make()
    cache = r.PrefixCache(a,1)
    key = cache.put(h,o)
    branch = cache.acquire(key,("tenant","branch"))
    cache.evict(key)
    a.release(h,o)
    assert a.flatten(branch,("tenant","branch")).tokens == tokens
    assert a.audit()["references"] == 2
    with pytest.raises(PermissionError): a.fork(branch,("tenant","branch"),("other","x"))
    with pytest.raises(PermissionError): cache.acquire(key,("other","x"))


@pytest.mark.parametrize("n,cap,chunk",[(2,1,(0,)),(1,1,(0,)),(1,2,(0,1,2,3,0))])
def test_oom_is_atomic_including_multi_page_and_cow(n,cap,chunk):
    _,a,h,o,_ = make(n,2,cap)
    c = a.fork(h,o,("tenant","child"))
    before = (a.flatten(h,o).seal,a.flatten(c,("tenant","child")).seal,a.audit())
    with pytest.raises(MemoryError): a.consume(c,("tenant","child"),chunk)
    assert before == (a.flatten(h,o).seal,a.flatten(c,("tenant","child")).seal,a.audit())


def test_private_tail_needs_no_free_page():
    _,a,h,o,_ = make(1,2,1)
    assert a.required_pages(h,o,1) == 0
    a.consume(h,o,(2,))
    assert a.audit()["physical_rows"] == 2


@pytest.mark.parametrize("bad",[(-1,), (True,), (4,), (0.0,), "AC"])
def test_invalid_append_no_mutation(bad):
    _,a,h,o,_ = make()
    before = a.flatten(h,o).seal,a.audit()
    with pytest.raises(ValueError): a.consume(h,o,bad)
    assert before == (a.flatten(h,o).seal,a.audit())


def test_table_and_payload_corruption_detected():
    _,a,h,o,_ = make(4)
    s = a.state(h,o)
    a._states[h.serial] = replace(s,pages=tuple(reversed(s.pages)))
    with pytest.raises(ValueError,match="block table mutated"): a.flatten(h,o)
    a._states[h.serial] = s
    a.page(s.pages[0]).layers[1].v[0,0,0] += 1
    with pytest.raises(ValueError,match="mutated page"): a.flatten(h,o)


def test_refcount_audit_negative_control():
    _,a,h,o,_ = make()
    a.pages[a.state(h,o).pages[0].page_id].refs += 1
    with pytest.raises(AssertionError): a.audit()


def test_empty_identity_and_fresh_owner():
    _,a,h,o,_ = make()
    before = a.state(h,o),a.audit()
    assert a.consume(h,o,()).shape == (0,4)
    assert before == (a.state(h,o),a.audit())
    with pytest.raises(ValueError): a.empty(o)
    with pytest.raises(ValueError): a.fork(h,o,o)
    with pytest.raises(PermissionError): a.flatten(h,("tenant","wrong"))


def test_exhaustive_short_branch_release_orders():
    for order in itertools.permutations(range(3)):
        _,a,h,o,tokens = make()
        owners = [o,("tenant","b"),("tenant","c")]
        handles = [h,a.fork(h,o,owners[1]),a.fork(h,o,owners[2])]
        for i in order:
            a.release(handles[i],owners[i]);a.audit()
        assert a.audit()["used_pages"] == 0


def test_two_writers_and_flatten_snapshot_isolation():
    m,a,h,o,tokens = make(3)
    child_owner=("tenant","child")
    c=a.fork(h,o,child_owner)
    snapshot=a.flatten(h,o)
    snapshot.layers[0].k.fill_(999)  # exported copy cannot mutate page payload
    a.consume(c,child_owner,(3,))
    a.consume(h,o,(0,))  # remaining parent tail is now private
    for handle,owner,suffix in ((h,o,(0,)),(c,child_owner,(3,))):
        _,expected=r.native.prefill(m,owner,tokens+suffix)
        actual=a.flatten(handle,owner)
        for x,y in zip(actual.layers,expected.layers):
            torch.testing.assert_close(x.k,y.k,atol=2e-12,rtol=2e-12)
            torch.testing.assert_close(x.v,y.v,atol=2e-12,rtol=2e-12)
    a.audit()
