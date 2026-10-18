import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch42/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def test_cost_choice():assert r.choose([r.Plan("a",2,1,.1),r.Plan("b",1,1,.5)]).name=="a"
def test_tie_deterministic():assert r.choose([r.Plan("b",1,1,0),r.Plan("a",1,1,0)]).name=="a"
def test_wal_rejects_early_page():
 s=r.WalStore();l=s.append("x",1)
 try:s.write_page("x",1,l);assert False
 except RuntimeError:pass
def test_wal_after_flush():s=r.WalStore();l=s.append("x",1);s.flush_log(l);s.write_page("x",1,l);assert s.data["x"]==1
def test_recovery_redo():s=r.WalStore();l=s.append("x",1);s.flush_log(l);s.recover();assert s.data["x"]==1
def test_recovery_idempotent():s=r.WalStore();l=s.append("x",1);s.flush_log(l);s.recover();s.recover();assert s.page_lsn["x"]==1
def test_breaks_are_explicit():assert len(r.inference_breaks_sql())==4
def test_cost_nonnegative():assert r.cost(r.Plan("x",1,2,.1))>=0
