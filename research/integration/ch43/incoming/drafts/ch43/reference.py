"""Governed structural-adaptation lifecycle oracle."""
from dataclasses import dataclass
from enum import Enum
import hashlib,json
class Stage(str,Enum): CANDIDATE="candidate";EVALUATED="evaluated";CANARY="canary";ACTIVE="active";RETIRED="retired";REJECTED="rejected"
@dataclass(frozen=True)
class Artifact:
 aid:str;parent:str|None;payload:str;stage:Stage;metrics:dict
def aid(parent,payload):return hashlib.sha256(json.dumps([parent,payload]).encode()).hexdigest()[:16]
class Registry:
 def __init__(self):self.a={};self.active=None;self.log=[]
 def create(self,payload,parent=None):
  if parent and parent not in self.a:raise KeyError("parent")
  x=Artifact(aid(parent,payload),parent,payload,Stage.CANDIDATE,{})
  self.a[x.aid]=x;self.log.append(("create",x.aid));return x
 def evaluate(self,xid,metrics,gates):
  x=self.a[xid];ok=all(metrics.get(k,float("-inf"))>=v for k,v in gates.items())
  st=Stage.EVALUATED if ok else Stage.REJECTED;self.a[xid]=Artifact(x.aid,x.parent,x.payload,st,dict(metrics));self.log.append(("evaluate",xid,ok));return ok
 def canary(self,xid):
  x=self.a[xid]
  if x.stage!=Stage.EVALUATED:raise RuntimeError("not evaluated")
  self.a[xid]=Artifact(x.aid,x.parent,x.payload,Stage.CANARY,x.metrics)
 def promote(self,xid):
  x=self.a[xid]
  if x.stage!=Stage.CANARY:raise RuntimeError("not canary")
  old=self.active
  if old:
   o=self.a[old];self.a[old]=Artifact(o.aid,o.parent,o.payload,Stage.RETIRED,o.metrics)
  self.a[xid]=Artifact(x.aid,x.parent,x.payload,Stage.ACTIVE,x.metrics);self.active=xid;self.log.append(("promote",xid))
 def rollback(self,target):
  if target not in self.a:raise KeyError(target)
  if self.active:
   o=self.a[self.active];self.a[o.aid]=Artifact(o.aid,o.parent,o.payload,Stage.RETIRED,o.metrics)
  t=self.a[target];self.a[target]=Artifact(t.aid,t.parent,t.payload,Stage.ACTIVE,t.metrics);self.active=target;self.log.append(("rollback",target))
def results():
 r=Registry();base=r.create("v1");r.evaluate(base.aid,{"quality":.8,"safety":1.0},{"quality":.7,"safety":1});r.canary(base.aid);r.promote(base.aid)
 cand=r.create("v2",base.aid);ok=r.evaluate(cand.aid,{"quality":.85,"safety":.5},{"quality":.8,"safety":1})
 return {"active":r.active,"bad_candidate_promotable":ok,"bad_stage":r.a[cand.aid].stage.value,"lineage_parent":r.a[cand.aid].parent,"events":len(r.log)}
if __name__=="__main__":print(json.dumps(results(),indent=2))
