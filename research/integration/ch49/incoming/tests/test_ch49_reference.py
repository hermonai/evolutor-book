import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/'drafts/ch49/reference.py';s=importlib.util.spec_from_file_location('r',p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def test_seq_monotonic():s=r.Session('x');assert [s.append('e').seq,s.append('e').seq]==[0,1]
def test_context_bounded():s=r.Session('x',2);[s.append('e',i=i) for i in range(4)];assert [e.seq for e in s.context()]==[2,3]
def test_checkpoint_valid():s=r.Session('x');s.append('a');assert s.verify(s.checkpoint())
def test_checkpoint_detects_mutation():s=r.Session('x');s.append('a',v=1);cp=s.checkpoint();s.events[0]=r.Event(0,'a',{'v':2});assert not s.verify(cp)
def test_resume():s=r.Session('x');s.append('a');cp=s.checkpoint();t=r.resume(s.events,cp);assert t.verify(cp)
def test_tool_denied():
 s=r.Session('x')
 try:s.tool('k','danger',False);assert False
 except PermissionError:pass
def test_tool_idempotent():s=r.Session('x');a=s.tool('k','read',True);b=s.tool('k','read',True);assert a==b and sum(e.kind=='tool_result' for e in s.events)==1
def test_stream_backpressure():
 q=r.Stream(1);q.push(1)
 try:q.push(2);assert False
 except RuntimeError:pass
def test_stream_fifo():q=r.Stream(2);q.push(1);q.push(2);assert [q.pop(),q.pop()]==[1,2]
def test_closed_session_rejects_append():
 s=r.Session('x');s.close()
 try:s.append('x');assert False
 except RuntimeError:pass
def test_checkpoint_prefix_survives_later_events():s=r.Session('x');s.append('a');cp=s.checkpoint();s.append('b');assert s.verify(cp)
def test_digest_deterministic():s=r.Session('x');s.append('a',v=1);assert s.digest()==s.digest()
