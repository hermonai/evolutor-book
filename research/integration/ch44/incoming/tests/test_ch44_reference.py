import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch44/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def B(n):return r.bundle(n,"m-"+n)
def test_digest_deterministic():assert B("x").digest()==B("x").digest()
def test_schema_rejected():
 d=r.Deployment()
 try:d.register(r.Bundle("x","m","r","c",2,"p"));assert False
 except ValueError:pass
def test_canary_ready():d=r.Deployment();x=d.register(B("x"));d.canary(x);assert d.revisions[x].ready
def test_promote_requires_canary():
 d=r.Deployment();x=d.register(B("x"))
 try:d.promote(x);assert False
 except RuntimeError:pass
def test_admission_requires_ready():
 d=r.Deployment();x=d.register(B("x"))
 try:d.admit(x);assert False
 except RuntimeError:pass
def test_drain_blocks_admission():
 d=r.Deployment();x=d.register(B("x"));d.canary(x);d.drain(x)
 try:d.admit(x);assert False
 except RuntimeError:pass
def test_terminate_waits_inflight():
 d=r.Deployment();x=d.register(B("x"));d.canary(x);d.admit(x);d.drain(x)
 try:d.terminate(x);assert False
 except RuntimeError:pass
 d.complete(x,10);d.terminate(x);assert d.revisions[x].state=="terminated"
def test_slo_error_gate():
 d=r.Deployment();x=d.register(B("x"));d.canary(x);d.admit(x);d.complete(x,10,False)
 try:d.promote(x,max_error=.1);assert False
 except RuntimeError:pass
def test_slo_latency_gate():
 d=r.Deployment();x=d.register(B("x"));d.canary(x)
 for v in [10,20,900]:
  d.admit(x);d.complete(x,v)
 try:d.promote(x,max_p95_ms=15);assert False
 except RuntimeError:pass
def test_rollback():
 d=r.Deployment();a=d.register(B("a"));d.canary(a);d.promote(a);b=d.register(B("b"));d.canary(b);d.promote(b);assert d.rollback()==a
def test_trace_sequence():d=r.Deployment();x=d.register(B("x"));d.canary(x);assert [e["seq"] for e in d.telemetry.events]==[0,1]
def test_complete_without_request_rejected():
 d=r.Deployment();x=d.register(B("x"));d.canary(x)
 try:d.complete(x,1);assert False
 except RuntimeError:pass
