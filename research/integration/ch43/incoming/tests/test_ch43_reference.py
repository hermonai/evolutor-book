import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch43/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def base():
 x=r.Registry();a=x.create("v1");assert x.evaluate(a.aid,{"q":1},{"q":.5});x.canary(a.aid);x.promote(a.aid);return x,a
def test_parent_required():
 x=r.Registry()
 try:x.create("v2","missing");assert False
 except KeyError:pass
def test_gate_rejects():x=r.Registry();a=x.create("x");assert not x.evaluate(a.aid,{"q":0},{"q":1});assert x.a[a.aid].stage==r.Stage.REJECTED
def test_cannot_canary_rejected():
 x=r.Registry();a=x.create("x");x.evaluate(a.aid,{"q":0},{"q":1})
 try:x.canary(a.aid);assert False
 except RuntimeError:pass
def test_promote_requires_canary():
 x=r.Registry();a=x.create("x");x.evaluate(a.aid,{"q":1},{"q":1})
 try:x.promote(a.aid);assert False
 except RuntimeError:pass
def test_promotion_retires_old():
 x,a=base();b=x.create("v2",a.aid);x.evaluate(b.aid,{"q":1},{"q":1});x.canary(b.aid);x.promote(b.aid);assert x.a[a.aid].stage==r.Stage.RETIRED
def test_rollback():x,a=base();b=x.create("v2",a.aid);x.evaluate(b.aid,{"q":1},{"q":1});x.canary(b.aid);x.promote(b.aid);x.rollback(a.aid);assert x.active==a.aid
def test_lineage():x,a=base();b=x.create("v2",a.aid);assert b.parent==a.aid
def test_id_deterministic():assert r.aid("p","x")==r.aid("p","x")
