"""EVOD-36 paged KV cache semantic oracle.

The implementation is deliberately small but enforces the invariants that matter:
logical token order is independent of physical page placement; page references are
generational; sharing is refcounted; a shared partial page is copied before append;
and a page is returned to the free list only after its final reference disappears.
"""
from dataclasses import dataclass, field
import json, math

@dataclass(frozen=True)
class PageRef:
    page_id:int
    generation:int

@dataclass
class Page:
    generation:int=0
    refcount:int=0
    rows:list=field(default_factory=list)

class Allocator:
    def __init__(self,capacity,page_size):
        if capacity<=0 or page_size<=0: raise ValueError("positive capacity/page_size")
        self.capacity=capacity; self.page_size=page_size
        self.pages=[Page() for _ in range(capacity)]

    def alloc(self,initial=()):
        rows=[tuple(x) for x in initial]
        if len(rows)>self.page_size: raise ValueError("page overflow")
        for i,p in enumerate(self.pages):
            if p.refcount==0:
                if p.rows: raise RuntimeError("free page not scrubbed")
                p.refcount=1; p.rows=list(rows)
                return PageRef(i,p.generation)
        raise MemoryError("no free KV page")

    def _page(self,ref):
        if not 0<=ref.page_id<self.capacity: raise RuntimeError("foreign page")
        p=self.pages[ref.page_id]
        if p.generation!=ref.generation or p.refcount<=0: raise RuntimeError("stale page reference")
        return p

    def incref(self,ref):
        self._page(ref).refcount+=1

    def decref(self,ref):
        p=self._page(ref); p.refcount-=1
        if p.refcount==0:
            p.rows=[]            # scrub logical contents before reuse
            p.generation+=1      # invalidate every old PageRef

    def read(self,ref):
        return tuple(self._page(ref).rows)

    def append_private(self,ref,row):
        p=self._page(ref)
        if p.refcount!=1: raise RuntimeError("page must be private before mutation")
        if len(p.rows)>=self.page_size: raise RuntimeError("page full")
        p.rows.append(tuple(row))

    def copy_page(self,ref):
        return self.alloc(self.read(ref))

    def stats(self):
        used=sum(p.refcount>0 for p in self.pages)
        refs=sum(p.refcount for p in self.pages)
        payload=sum(len(p.rows) for p in self.pages if p.refcount>0)
        return {"pages":self.capacity,"used_pages":used,"free_pages":self.capacity-used,
                "references":refs,"payload_rows":payload}

@dataclass
class Sequence:
    allocator:Allocator
    model_id:str
    pages:list=field(default_factory=list)
    length:int=0

    def fork(self):
        child=Sequence(self.allocator,self.model_id,list(self.pages),self.length)
        for ref in child.pages:self.allocator.incref(ref)
        return child

    def append(self,krow,vrow):
        row=(tuple(krow),tuple(vrow))
        ps=self.allocator.page_size
        offset=self.length%ps
        if offset==0:
            self.pages.append(self.allocator.alloc())
        else:
            tail=self.pages[-1]
            p=self.allocator._page(tail)
            if p.refcount>1:
                # Copy-on-write: child receives a private physical tail.
                new=self.allocator.copy_page(tail)
                self.allocator.decref(tail)
                self.pages[-1]=new
        self.allocator.append_private(self.pages[-1],row)
        self.length+=1

    def flatten(self):
        rows=[]
        for ref in self.pages:rows.extend(self.allocator.read(ref))
        rows=rows[:self.length]
        return tuple(rows)

    def release(self):
        for ref in self.pages:self.allocator.decref(ref)
        self.pages=[]; self.length=0

    def internal_waste(self):
        if not self.pages:return 0
        return len(self.pages)*self.allocator.page_size-self.length

class PrefixCache:
    def __init__(self):self.items={}
    def put(self,key,seq):
        if key in self.items:self.evict(key)
        refs=list(seq.pages)
        for ref in refs:seq.allocator.incref(ref)
        self.items[key]=(seq.allocator,seq.model_id,seq.length,refs)
    def fork(self,key):
        alloc,model,length,refs=self.items[key]
        out=Sequence(alloc,model,list(refs),length)
        for ref in refs:alloc.incref(ref)
        return out
    def evict(self,key):
        alloc,_,_,refs=self.items.pop(key)
        for ref in refs:alloc.decref(ref)

def contiguous_append(rows,k,v):
    return tuple(list(rows)+[(tuple(k),tuple(v))])

def results():
    a=Allocator(capacity=8,page_size=2)
    s=Sequence(a,"hermon")
    oracle=()
    for t in range(3):
        k=(float(t),float(t)+.1);v=(float(t)+1,float(t)+2)
        s.append(k,v);oracle=contiguous_append(oracle,k,v)
    child=s.fork()
    # Both share a partially full second page. Child append must COW that tail.
    child.append((9.,9.1),(10.,11.))
    before_parent=s.flatten()
    cache=PrefixCache();cache.put("prefix3",s);from_cache=cache.fork("prefix3")
    cache.evict("prefix3")
    return {"parent_matches_contiguous":s.flatten()==oracle,
      "parent_unchanged_after_child":before_parent==oracle,
      "child_length":child.length,"parent_length":s.length,
      "cache_fork_matches":from_cache.flatten()==s.flatten(),
      "parent_waste_rows":s.internal_waste(),"stats":a.stats()}
if __name__=="__main__":print(json.dumps(results(),indent=2))
