"""EVOD-46 distributed placement/migration teaching oracle."""
from dataclasses import dataclass, field
import hashlib, json

@dataclass(frozen=True)
class Worker:
    wid:str; zone:str; backend:str; capacity:int
@dataclass(frozen=True)
class StateHandle:
    sid:str; tenant:str; artifact:str; schema:int; owner:str; epoch:int
@dataclass
class State:
    handle:StateHandle; payload:tuple
@dataclass
class EventLog:
    events:list=field(default_factory=list)
    def emit(self,kind,**kw): self.events.append({"seq":len(self.events),"kind":kind,**kw})

class Cluster:
    def __init__(self,workers):
        self.workers={w.wid:w for w in workers}; self.used={w.wid:0 for w in workers}
        self.states={}; self.log=EventLog()
    def place(self,tenant,artifact,backend,prefer_zone=None):
        candidates=[w for w in self.workers.values() if w.backend==backend and self.used[w.wid]<w.capacity]
        if prefer_zone:
            local=[w for w in candidates if w.zone==prefer_zone]
            if local:candidates=local
        if not candidates: raise RuntimeError("no capacity")
        # Deterministic least-loaded placement, then worker ID.
        candidates.sort(key=lambda w:(self.used[w.wid]/w.capacity,w.wid))
        w=candidates[0]; self.log.emit("placed",tenant=tenant,artifact=artifact,worker=w.wid); return w.wid
    def create_state(self,tenant,artifact,schema,backend,payload,prefer_zone=None):
        owner=self.place(tenant,artifact,backend,prefer_zone)
        sid=hashlib.sha256(f"{tenant}|{artifact}|{len(self.states)}".encode()).hexdigest()[:16]
        h=StateHandle(sid,tenant,artifact,schema,owner,0)
        self.states[sid]=State(h,tuple(payload));self.used[owner]+=1
        self.log.emit("state_created",sid=sid,owner=owner,epoch=0);return h
    def read(self,h):
        s=self.states[h.sid]
        if h!=s.handle: raise RuntimeError("stale/foreign handle")
        if s.handle.owner not in self.workers: raise RuntimeError("owner unavailable")
        return s.payload
    def migrate(self,h,dst):
        s=self.states[h.sid]
        if h!=s.handle: raise RuntimeError("stale migration handle")
        if dst==h.owner or dst not in self.workers: raise RuntimeError("bad destination")
        if self.used[dst]>=self.workers[dst].capacity: raise RuntimeError("destination full")
        src=h.owner
        # Prepare/copy/verify before commit. Payload digest stands in for transport integrity.
        digest=hashlib.sha256(json.dumps(list(s.payload)).encode()).hexdigest()
        self.log.emit("migration_prepare",sid=h.sid,src=src,dst=dst,epoch=h.epoch)
        copied=tuple(s.payload)
        verify=hashlib.sha256(json.dumps(list(copied)).encode()).hexdigest()
        if verify!=digest: raise RuntimeError("transfer corruption")
        nh=StateHandle(h.sid,h.tenant,h.artifact,h.schema,dst,h.epoch+1)
        # Commit atomically in the oracle: new owner+epoch become authoritative together.
        s.handle=nh;s.payload=copied;self.used[src]-=1;self.used[dst]+=1
        self.log.emit("migration_commit",sid=h.sid,src=src,dst=dst,epoch=nh.epoch)
        return nh
    def fail_worker(self,wid):
        if wid not in self.workers: return
        del self.workers[wid];self.log.emit("worker_failed",worker=wid)
    def recover_by_replay(self,h,dst,replayed_payload):
        s=self.states[h.sid]
        if s.handle!=h or h.owner in self.workers: raise RuntimeError("recovery precondition")
        if dst not in self.workers or self.used[dst]>=self.workers[dst].capacity: raise RuntimeError("recovery destination")
        nh=StateHandle(h.sid,h.tenant,h.artifact,h.schema,dst,h.epoch+1)
        s.handle=nh;s.payload=tuple(replayed_payload);self.used[dst]+=1
        self.log.emit("recovered",sid=h.sid,dst=dst,epoch=nh.epoch);return nh
    def pd_route(self,tenant,artifact,prefill_zone,decode_zone):
        p=self.place(tenant,artifact,"prefill",prefill_zone)
        d=self.place(tenant,artifact,"decode",decode_zone)
        self.log.emit("pd_route",prefill=p,decode=d,cross_zone=self.workers[p].zone!=self.workers[d].zone)
        return p,d

def results():
    ws=[Worker("d0","z1","dogma",2),Worker("d1","z2","dogma",2),
        Worker("p0","z1","prefill",4),Worker("k0","z1","decode",4)]
    c=Cluster(ws);h=c.create_state("A","dogma-r1",1,"dogma",[1,2,3],"z1")
    nh=c.migrate(h,"d1")
    stale_rejected=False
    try:c.read(h)
    except RuntimeError:stale_rejected=True
    p,d=c.pd_route("A","hermon-r1","z1","z1")
    return {"new_owner":nh.owner,"epoch":nh.epoch,"payload":list(c.read(nh)),
            "stale_rejected":stale_rejected,"pd_same_zone":c.workers[p].zone==c.workers[d].zone,
            "events":len(c.log.events)}
if __name__=="__main__":print(json.dumps(results(),indent=2))
