"""EVOD-41 small typed IR/compiler reference."""
from dataclasses import dataclass
from enum import Enum
import json

class Ty(str,Enum): INT="int"; TOKENS="tokens"; DOCS="docs"; HANDLE="handle"
@dataclass(frozen=True)
class Op:
    oid:str; kind:str; inputs:tuple; output:str|None; out_ty:Ty|None; attrs:dict
@dataclass(frozen=True)
class Program: inputs:dict; ops:tuple; outputs:tuple

PURE={"const","add","retrieve","engine"}
EFFECT={"tool"}

def verify(p):
    env=dict(p.inputs); ids=set()
    for op in p.ops:
        if op.oid in ids: raise ValueError("duplicate op")
        ids.add(op.oid)
        for x in op.inputs:
            if x not in env: raise ValueError("undefined input")
        if op.kind=="add":
            if len(op.inputs)!=2 or any(env[x]!=Ty.INT for x in op.inputs) or op.out_ty!=Ty.INT: raise TypeError("add")
        elif op.kind=="const":
            if op.inputs or op.out_ty!=Ty.INT: raise TypeError("const")
        elif op.kind=="retrieve":
            if op.out_ty!=Ty.DOCS: raise TypeError("retrieve")
        elif op.kind=="engine":
            if op.out_ty!=Ty.TOKENS or "capability" not in op.attrs: raise TypeError("engine")
        elif op.kind=="tool":
            if op.output is not None or op.out_ty is not None or "name" not in op.attrs: raise TypeError("tool")
        else: raise ValueError("unknown op")
        if op.output:
            if op.output in env: raise ValueError("SSA redefinition")
            env[op.output]=op.out_ty
    for x in p.outputs:
        if x not in env: raise ValueError("bad program output")
    return env

def constant_fold(p):
    verify(p); const={}; out=[]
    for op in p.ops:
        if op.kind=="const": const[op.output]=int(op.attrs["value"]);out.append(op)
        elif op.kind=="add" and all(x in const for x in op.inputs):
            v=const[op.inputs[0]]+const[op.inputs[1]]
            n=Op(op.oid,"const",(),op.output,Ty.INT,{"value":v,"folded_from":"add"});const[op.output]=v;out.append(n)
        else: out.append(op)
    q=Program(p.inputs,tuple(out),p.outputs);verify(q);return q

def dce(p):
    """Remove unused pure ops while retaining all effectful operations."""
    verify(p); live=set(p.outputs); kept=[]
    for op in reversed(p.ops):
        needed=op.kind in EFFECT or (op.output is not None and op.output in live)
        if needed:
            kept.append(op);live.update(op.inputs)
    q=Program(p.inputs,tuple(reversed(kept)),p.outputs);verify(q);return q

BACKENDS={
 "dogma":{"compressed_state","tokens"},
 "hermon":{"addressable_kv","tokens"},
 "retriever":{"retrieval"},
 "host":{"int"},
 "toolhost":{"tool"}
}
def lower(p):
    env=verify(p);schedule=[]
    for op in p.ops:
        if op.kind=="engine":
            cap=op.attrs["capability"];eligible=[b for b,c in BACKENDS.items() if cap in c]
            if len(eligible)!=1: raise RuntimeError("engine capability route")
            backend=eligible[0]
        elif op.kind=="retrieve":backend="retriever"
        elif op.kind in ("const","add"):backend="host"
        elif op.kind=="tool":backend="toolhost"
        else:raise RuntimeError(op.kind)
        schedule.append({"oid":op.oid,"backend":backend,"kind":op.kind,"inputs":list(op.inputs),"output":op.output})
    return schedule

def peak_live_values(p):
    """Simple SSA liveness count after each op; teaching memory-pressure proxy."""
    verify(p); uses={x:0 for x in p.inputs}
    for op in p.ops:
        for x in op.inputs:uses[x]=uses.get(x,0)+1
        if op.output:uses.setdefault(op.output,0)
    live=set(p.inputs);peak=len(live)
    for op in p.ops:
        if op.output:live.add(op.output)
        for x in op.inputs:
            uses[x]-=1
            if uses[x]==0 and x not in p.outputs:live.discard(x)
        peak=max(peak,len(live))
    return peak

def fixture():
    return Program({},(
      Op("c1","const",(),"a",Ty.INT,{"value":7}),
      Op("c2","const",(),"b",Ty.INT,{"value":8}),
      Op("sum","add",("a","b"),"n",Ty.INT,{}),
      Op("dead","const",(),"unused",Ty.INT,{"value":99}),
      Op("ret","retrieve",(),"docs",Ty.DOCS,{"query":"genomic memory"}),
      Op("d","engine",(),"dtok",Ty.TOKENS,{"capability":"compressed_state"}),
      Op("h","engine",(),"htok",Ty.TOKENS,{"capability":"addressable_kv"}),
      Op("act","tool",("n",),None,None,{"name":"safe_action"}),
    ),("n","docs","dtok","htok"))

def results():
    p=fixture();f=constant_fold(p);o=dce(f);s=lower(o)
    return {"original_ops":len(p.ops),"optimized_ops":len(o.ops),"folded_sum_kind":[x.kind for x in o.ops if x.oid=="sum"][0],"dead_removed":not any(x.oid=="dead" for x in o.ops),"tool_preserved":any(x.oid=="act" for x in o.ops),"schedule":s,"peak_live_values":peak_live_values(o)}
if __name__=="__main__":print(json.dumps(results(),indent=2))
