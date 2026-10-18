import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch39/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def runtime():return r.Runtime([r.DogmaAdapter("d1"),r.HermonAdapter("h1")],r.Policy({"ok"}))
def test_routes_dogma():assert runtime().route(r.Capability.COMPRESSED_STATE).name=="dogma"
def test_routes_hermon():assert runtime().route(r.Capability.ADDRESSABLE_KV).name=="hermon"
def test_foreign_handle_rejected():
 d=r.DogmaAdapter("d");h=r.HermonAdapter("h");x=d.open("r")
 try:h.execute(x,[1]);assert False
 except RuntimeError:pass
def test_model_bound_handle_rejected():
 a=r.DogmaAdapter("a");b=r.DogmaAdapter("b");x=a.open("r")
 try:b.execute(x,[1]);assert False
 except RuntimeError:pass
def test_closed_handle_rejected():
 e=r.DogmaAdapter("d");h=e.open("r");e.close(h)
 try:e.execute(h,[1]);assert False
 except RuntimeError:pass
def test_tool_denied_before_execution():
 rt=runtime();p=r.Plan("x",(r.Step("tool",payload={"name":"no"}),))
 try:rt.execute(p);assert False
 except PermissionError:pass
 assert any(x["kind"]=="tool_denied" for x in rt.trace.events) and not any(x["kind"]=="tool_executed" for x in rt.trace.events)
def test_tool_allowed():assert runtime().execute(r.Plan("x",(r.Step("tool",payload={"name":"ok"}),)))[0]["status"]=="executed"
def test_retrieval_deterministic():
 rt=runtime();o=rt.execute(r.Plan("x",(r.Step("retrieve",payload={"corpus":["Alpha","beta alpha","gamma"],"term":"alpha"}),)));assert o==[["Alpha","beta alpha"]]
def test_symbolic():assert runtime().execute(r.Plan("x",(r.Step("symbolic",payload=(2,5)),)))==[7]
def test_invalid_plan():
 try:runtime().execute(r.Plan("",()));assert False
 except ValueError:pass
def test_trace_sequence_monotonic():
 rt=runtime();rt.execute(r.Plan("x",(r.Step("engine",r.Capability.COMPRESSED_STATE,[1]),r.Step("symbolic",payload=(1,2)))))
 assert [e["seq"] for e in rt.trace.events]==list(range(len(rt.trace.events)))
def test_trace_digests_present():
 rt=runtime();rt.execute(r.Plan("x",(r.Step("symbolic",payload=(1,2)),)));assert all(len(e["digest"])==16 for e in rt.trace.events)
def test_two_engines_preserve_distinct_capabilities():
 d=r.DogmaAdapter("d");h=r.HermonAdapter("h");assert d.capabilities!=h.capabilities
