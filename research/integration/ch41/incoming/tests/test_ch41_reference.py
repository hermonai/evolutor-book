import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch41/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def test_fixture_verifies():r.verify(r.fixture())
def test_constant_fold():q=r.constant_fold(r.fixture());x=[o for o in q.ops if o.oid=="sum"][0];assert x.kind=="const" and x.attrs["value"]==15
def test_dce_removes_unused_pure():q=r.dce(r.constant_fold(r.fixture()));assert not any(o.oid=="dead" for o in q.ops)
def test_dce_keeps_effect():q=r.dce(r.constant_fold(r.fixture()));assert any(o.kind=="tool" for o in q.ops)
def test_lower_dogma():s=r.lower(r.dce(r.constant_fold(r.fixture())));assert [x["backend"] for x in s if x["oid"]=="d"]==["dogma"]
def test_lower_hermon():s=r.lower(r.dce(r.constant_fold(r.fixture())));assert [x["backend"] for x in s if x["oid"]=="h"]==["hermon"]
def test_retrieve_backend():assert [x["backend"] for x in r.lower(r.fixture()) if x["oid"]=="ret"]==["retriever"]
def test_undefined_rejected():
 p=r.Program({},(r.Op("x","add",("a","b"),"c",r.Ty.INT,{}),),("c",))
 try:r.verify(p);assert False
 except ValueError:pass
def test_type_error_rejected():
 p=r.Program({"a":r.Ty.DOCS,"b":r.Ty.INT},(r.Op("x","add",("a","b"),"c",r.Ty.INT,{}),),("c",))
 try:r.verify(p);assert False
 except TypeError:pass
def test_ssa_redefinition_rejected():
 p=r.Program({"a":r.Ty.INT},(r.Op("x","const",(),"a",r.Ty.INT,{"value":1}),),("a",))
 try:r.verify(p);assert False
 except ValueError:pass
def test_unknown_capability_rejected():
 p=r.Program({},(r.Op("x","engine",(),"y",r.Ty.TOKENS,{"capability":"magic"}),),("y",))
 try:r.lower(p);assert False
 except RuntimeError:pass
def test_peak_positive():assert r.peak_live_values(r.fixture())>0
def test_deterministic_lowering():p=r.dce(r.constant_fold(r.fixture()));assert r.lower(p)==r.lower(p)
