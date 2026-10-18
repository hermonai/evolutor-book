import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch36/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)

def make(n=3,page=2):
 a=r.Allocator(16,page);q=r.Sequence(a,"m");o=()
 for t in range(n):
  k=(float(t),);v=(float(t+10),);q.append(k,v);o=r.contiguous_append(o,k,v)
 return a,q,o

def test_paged_equals_contiguous():
 _,q,o=make(7,3);assert q.flatten()==o

def test_block_translation_order_survives_noncontiguous_pages():
 a,q,o=make(4,2);junk=r.Sequence(a,"m");junk.append((99.,),(99.,))
 q.append((4.,),(14.,));o=r.contiguous_append(o,(4.,),(14.,));assert q.flatten()==o

def test_fork_initially_equal():
 _,q,_=make();c=q.fork();assert c.flatten()==q.flatten()

def test_cow_partial_tail_isolates_parent():
 a,q,o=make(3,2);old=q.pages[-1];c=q.fork();assert a._page(old).refcount==2
 c.append((8.,),(18.,));assert q.flatten()==o and c.flatten()[:-1]==o and c.pages[-1]!=q.pages[-1]

def test_full_tail_allocates_new_page_without_copying_old():
 a,q,_=make(2,2);c=q.fork();old=c.pages[-1];c.append((3.,),(13.,));assert c.pages[-2]==old and len(c.pages)==2

def test_release_refcounts_keep_live_branch():
 a,q,o=make(3,2);c=q.fork();q.release();assert c.flatten()==o

def test_final_release_frees_and_advances_generation():
 a,q,_=make(1,2);old=q.pages[0];g=old.generation;q.release()
 n=a.alloc();assert n.page_id==old.page_id and n.generation==g+1

def test_stale_page_ref_rejected():
 a,q,_=make(1,2);old=q.pages[0];q.release();a.alloc()
 try:a.read(old);assert False
 except RuntimeError:pass

def test_prefix_cache_eviction_does_not_break_live_fork():
 a,q,o=make(3,2);c=r.PrefixCache();c.put("x",q);branch=c.fork("x");c.evict("x");assert branch.flatten()==o

def test_waste_bound():
 _,q,_=make(5,4);assert q.internal_waste()==3

def test_capacity_failure():
 a=r.Allocator(1,1);q=r.Sequence(a,"m");q.append((1.,),(1.,))
 try:q.append((2.,),(2.,));assert False
 except MemoryError:pass

def test_shared_page_cannot_mutate_directly():
 a,q,_=make(1,4);q.fork()
 try:a.append_private(q.pages[-1],((2.,),(3.,)));assert False
 except RuntimeError:pass
