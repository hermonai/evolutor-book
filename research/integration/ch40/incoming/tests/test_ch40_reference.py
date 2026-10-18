import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch40/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def test_event_roundtrip(): m=r.Memory();x=m.put_event("a","hello");assert m.get("a",x.rid).text=="hello"
def test_tenant_isolation():
 m=r.Memory();x=m.put_event("a","secret")
 try:m.get("b",x.rid);assert False
 except PermissionError:pass
def test_summary_provenance(): m=r.Memory();a=m.put_event("t","one two");b=m.put_event("t","two three");s=m.summarize("t",[a.rid,b.rid]);assert s.sources==(a.rid,b.rid)
def test_summary_is_lossy(): m=r.Memory();a=m.put_event("t","one two three four");s=m.summarize("t",[a.rid],2);assert s.text!="one two three four"
def test_rehydrate_sources(): m=r.Memory();a=m.put_event("t","a");b=m.put_event("t","b");s=m.summarize("t",[a.rid,b.rid]);assert [x.rid for x in m.rehydrate("t",s.rid)]==[a.rid,b.rid]
def test_retrieve_rank(): m=r.Memory();a=m.put_event("t","alpha beta");m.put_event("t","alpha");assert m.retrieve("t","alpha beta")[0].rid==a.rid
def test_zero_overlap_not_returned():m=r.Memory();m.put_event("t","alpha");assert m.retrieve("t","zeta")==[]
def test_expiry(): 
 m=r.Memory();x=m.put_event("t","short",ttl=1);m.tick()
 try:m.get("t",x.rid);assert False
 except KeyError:pass
def test_forget_tombstone():
 m=r.Memory();x=m.put_event("t","erase");m.forget("t",x.rid)
 try:m.get("t",x.rid);assert False
 except KeyError:pass
def test_deleted_not_retrieved():m=r.Memory();x=m.put_event("t","alpha");m.forget("t",x.rid);assert m.retrieve("t","alpha")==[]
def test_event_not_rehydrate():
 m=r.Memory();x=m.put_event("t","x")
 try:m.rehydrate("t",x.rid);assert False
 except ValueError:pass
def test_summary_deterministic():m=r.Memory();a=m.put_event("t","a b");assert m.summarize("t",[a.rid]).rid==m.summarize("t",[a.rid]).rid
