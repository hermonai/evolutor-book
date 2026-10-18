"""EVOD-44 deployment and observability teaching oracle."""
from dataclasses import dataclass, field
import hashlib, json

@dataclass(frozen=True)
class Bundle:
    revision:str; model_digest:str; runtime_digest:str; config_digest:str; schema:int; provenance:str
    def digest(self):
        body=json.dumps(self.__dict__,sort_keys=True,separators=(",",":")).encode()
        return hashlib.sha256(body).hexdigest()

@dataclass
class Revision:
    bundle:Bundle; state:str="registered"; ready:bool=False; inflight:int=0

@dataclass
class Telemetry:
    requests:int=0; errors:int=0; latencies:list=field(default_factory=list)
    events:list=field(default_factory=list)
    def emit(self,kind,**attrs): self.events.append({"seq":len(self.events),"kind":kind,**attrs})
    def record(self,latency_ms,ok=True):
        self.requests+=1; self.latencies.append(float(latency_ms)); self.errors+=0 if ok else 1
    def error_rate(self): return 0.0 if not self.requests else self.errors/self.requests
    def p(self,q):
        if not self.latencies:return 0.0
        x=sorted(self.latencies); i=min(len(x)-1,max(0,int((len(x)-1)*q))); return x[i]

class Deployment:
    def __init__(self,supported_schema=1):
        self.supported_schema=supported_schema; self.revisions={}; self.active=None; self.previous=None; self.telemetry=Telemetry()
    def register(self,b):
        if b.schema!=self.supported_schema: raise ValueError("schema incompatible")
        if not all((b.model_digest,b.runtime_digest,b.config_digest,b.provenance)): raise ValueError("incomplete bundle")
        d=b.digest()
        if d in self.revisions: raise ValueError("duplicate bundle")
        self.revisions[d]=Revision(b); self.telemetry.emit("registered",digest=d); return d
    def canary(self,d):
        r=self.revisions[d]
        if r.state not in ("registered","rolled_back"): raise RuntimeError("bad state")
        r.state="canary"; r.ready=True; self.telemetry.emit("canary",digest=d)
    def promote(self,d,max_error=.01,max_p95_ms=500):
        r=self.revisions[d]
        if r.state!="canary" or not r.ready: raise RuntimeError("not ready canary")
        if self.telemetry.error_rate()>max_error or self.telemetry.p(.95)>max_p95_ms: raise RuntimeError("SLO gate")
        if self.active:
            self.previous=self.active; self.revisions[self.active].state="superseded"
        self.active=d; r.state="active"; self.telemetry.emit("promoted",digest=d)
    def admit(self,d):
        r=self.revisions[d]
        if not r.ready or r.state not in ("canary","active"): raise RuntimeError("not admitting")
        r.inflight+=1; self.telemetry.emit("admit",digest=d,inflight=r.inflight)
    def complete(self,d,latency_ms,ok=True):
        r=self.revisions[d]
        if r.inflight<=0: raise RuntimeError("no inflight")
        r.inflight-=1; self.telemetry.record(latency_ms,ok); self.telemetry.emit("complete",digest=d,ok=ok)
    def drain(self,d):
        r=self.revisions[d]; r.ready=False; r.state="draining"; self.telemetry.emit("drain",digest=d)
    def terminate(self,d):
        r=self.revisions[d]
        if r.state!="draining" or r.inflight: raise RuntimeError("not drained")
        r.state="terminated"; self.telemetry.emit("terminated",digest=d)
    def rollback(self):
        if not self.active or not self.previous: raise RuntimeError("no rollback target")
        bad=self.active; target=self.previous
        self.revisions[bad].ready=False; self.revisions[bad].state="rolled_back"
        self.revisions[target].state="active"; self.revisions[target].ready=True
        self.active=target; self.previous=None; self.telemetry.emit("rollback",from_digest=bad,to_digest=target)
        return target

def bundle(rev,model):
    return Bundle(rev,model,"runtime-44","config-44",1,"builder://verified")
def results():
    d=Deployment(); a=d.register(bundle("r1","model-a")); d.canary(a); d.promote(a)
    b=d.register(bundle("r2","model-b")); d.canary(b); d.admit(b); d.complete(b,40,True); d.promote(b)
    target=d.rollback()
    return {"active_after_rollback":d.revisions[target].bundle.revision,
            "states":{x.bundle.revision:x.state for x in d.revisions.values()},
            "requests":d.telemetry.requests,"error_rate":d.telemetry.error_rate(),
            "events":len(d.telemetry.events)}
if __name__=="__main__": print(json.dumps(results(),indent=2))
