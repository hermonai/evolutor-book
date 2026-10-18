"""EVOD-49 persistent agent/session teaching oracle."""
from dataclasses import dataclass,field
import hashlib,json
@dataclass(frozen=True)
class Event: seq:int; kind:str; payload:dict
@dataclass(frozen=True)
class Checkpoint: session:str; upto:int; digest:str
class Session:
 def __init__(self,sid,max_context=4):self.sid=sid;self.max_context=max_context;self.events=[];self.tool_results={};self.closed=False
 def append(self,kind,**payload):
  if self.closed:raise RuntimeError('closed')
  e=Event(len(self.events),kind,payload);self.events.append(e);return e
 def context(self):return self.events[-self.max_context:]
 def digest(self,upto=None):
  es=self.events if upto is None else self.events[:upto+1]
  raw=json.dumps([e.__dict__ for e in es],sort_keys=True,separators=(',',':')).encode();return hashlib.sha256(raw).hexdigest()
 def checkpoint(self):
  upto=len(self.events)-1;return Checkpoint(self.sid,upto,self.digest(upto))
 def verify(self,cp):return cp.session==self.sid and cp.upto<len(self.events) and self.digest(cp.upto)==cp.digest
 def tool(self,key,name,authorized):
  if key in self.tool_results:return self.tool_results[key]
  if not authorized:raise PermissionError('tool denied')
  result={'name':name,'status':'ok','idempotency_key':key};self.tool_results[key]=result;self.append('tool_result',**result);return result
 def close(self):self.closed=True
class Stream:
 def __init__(self,capacity):self.capacity=capacity;self.q=[]
 def push(self,item):
  if len(self.q)>=self.capacity:raise RuntimeError('backpressure')
  self.q.append(item)
 def pop(self):return self.q.pop(0) if self.q else None

def resume(events,cp,max_context=4):
 s=Session(cp.session,max_context);s.events=list(events)
 if not s.verify(cp):raise ValueError('checkpoint mismatch')
 return s

def results():
 s=Session('agent-1',3);s.append('user',text='inspect repo');s.append('model_proposal',action='read');cp=s.checkpoint();r=s.tool('k1','read_file',True);again=s.tool('k1','read_file',True);q=Stream(1);q.push('event');blocked=False
 try:q.push('overflow')
 except RuntimeError:blocked=True
 return {'checkpoint_valid':s.verify(cp),'context_len':len(s.context()),'tool_idempotent':r==again,'tool_events':sum(e.kind=='tool_result' for e in s.events),'backpressure':blocked}
if __name__=='__main__':print(json.dumps(results(),indent=2))
