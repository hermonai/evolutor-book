"""EVOD-39 typed Evolutor runtime teaching reference.

The runtime deliberately never opens an engine-native state object. It receives
opaque handles from adapters and validates backend/model/request identity before
every operation. Tools require explicit policy authorization.
"""
from dataclasses import dataclass,field
from enum import Enum
import json,hashlib

class Capability(str,Enum):
    COMPRESSED_STATE="compressed_state"
    ADDRESSABLE_KV="addressable_kv"
    RETRIEVAL="retrieval"
    SYMBOLIC="symbolic"
    TOOL="tool"

@dataclass(frozen=True)
class Handle:
    backend:str; model_id:str; request_id:str; opaque_id:str

@dataclass(frozen=True)
class Step:
    op:str
    capability:Capability|None=None
    payload:object=None

@dataclass(frozen=True)
class Plan:
    request_id:str
    steps:tuple

@dataclass
class Trace:
    events:list=field(default_factory=list)
    def emit(self,kind,**data):
        seq=len(self.events)
        body={"seq":seq,"kind":kind,**data}
        body["digest"]=hashlib.sha256(json.dumps(body,sort_keys=True,default=str).encode()).hexdigest()[:16]
        self.events.append(body)

class EngineAdapter:
    name="abstract"; capabilities=frozenset()
    def __init__(self,model_id):
        self.model_id=model_id;self._states={};self._next=0
    def open(self,request_id):
        oid=f"{self.name}:{self._next}";self._next+=1;self._states[oid]=[]
        return Handle(self.name,self.model_id,request_id,oid)
    def _check(self,h):
        if h.backend!=self.name or h.model_id!=self.model_id or h.opaque_id not in self._states:raise RuntimeError("invalid/foreign engine handle")
    def execute(self,h,tokens):
        self._check(h);self._states[h.opaque_id].extend(tokens)
        # Deterministic teaching output: backend-specific state remains private.
        return (sum(tokens)+len(self._states[h.opaque_id]))%17
    def close(self,h):
        self._check(h);del self._states[h.opaque_id]

class DogmaAdapter(EngineAdapter):
    name="dogma";capabilities=frozenset({Capability.COMPRESSED_STATE})
class HermonAdapter(EngineAdapter):
    name="hermon";capabilities=frozenset({Capability.ADDRESSABLE_KV})

class Policy:
    def __init__(self,allowed_tools=()):self.allowed_tools=set(allowed_tools)
    def authorize_tool(self,name):return name in self.allowed_tools

class Runtime:
    def __init__(self,engines,policy):
        self.engines=list(engines);self.policy=policy;self.trace=Trace()
    def route(self,cap):
        matches=[e for e in self.engines if cap in e.capabilities]
        if len(matches)!=1:raise RuntimeError("capability route must resolve uniquely")
        self.trace.emit("route",capability=cap.value,backend=matches[0].name)
        return matches[0]
    def validate(self,plan):
        if not plan.request_id or not plan.steps:raise ValueError("nonempty plan")
        for s in plan.steps:
            if s.op=="engine" and s.capability not in (Capability.COMPRESSED_STATE,Capability.ADDRESSABLE_KV):raise ValueError("illegal engine capability")
            if s.op=="tool" and not isinstance(s.payload,dict):raise ValueError("tool payload")
            if s.op not in ("engine","retrieve","symbolic","tool"):raise ValueError("unknown op")
    def execute(self,plan):
        self.validate(plan);self.trace.emit("plan_start",request_id=plan.request_id,steps=len(plan.steps));out=[]
        for s in plan.steps:
            if s.op=="engine":
                e=self.route(s.capability);h=e.open(plan.request_id);self.trace.emit("engine_open",backend=e.name,handle=h.opaque_id)
                y=e.execute(h,list(s.payload));out.append(y);self.trace.emit("engine_result",backend=e.name,value=y);e.close(h);self.trace.emit("engine_close",backend=e.name)
            elif s.op=="retrieve":
                corpus=s.payload["corpus"];term=s.payload["term"];hits=[x for x in corpus if term.lower() in x.lower()]
                out.append(hits);self.trace.emit("retrieval",hits=len(hits))
            elif s.op=="symbolic":
                a,b=s.payload;value=a+b;out.append(value);self.trace.emit("symbolic",operator="add",value=value)
            elif s.op=="tool":
                name=s.payload["name"]
                if not self.policy.authorize_tool(name):self.trace.emit("tool_denied",name=name);raise PermissionError(name)
                value={"tool":name,"status":"executed"};out.append(value);self.trace.emit("tool_executed",name=name)
        self.trace.emit("plan_complete",outputs=len(out));return out

def results():
    rt=Runtime([DogmaAdapter("dogma-r1"),HermonAdapter("hermon-r1")],Policy({"safe_echo"}))
    plan=Plan("req-39",(Step("retrieve",payload={"corpus":["genomic memory","attention cache"],"term":"genomic"}),
                        Step("engine",Capability.COMPRESSED_STATE,[1,2,3]),
                        Step("engine",Capability.ADDRESSABLE_KV,[4,5]),
                        Step("symbolic",payload=(7,8)),
                        Step("tool",payload={"name":"safe_echo"})))
    out=rt.execute(plan)
    return {"outputs":out,"trace_events":len(rt.trace.events),"backends":[e["backend"] for e in rt.trace.events if e["kind"]=="route"],"trace_last":rt.trace.events[-1]["kind"]}
if __name__=="__main__":print(json.dumps(results(),indent=2))
