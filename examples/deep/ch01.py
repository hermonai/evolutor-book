"""Original exact routed-program example, not a trained model or inference engine."""
from fractions import Fraction
from itertools import accumulate
from types import MappingProxyType

def clip(xs):
    return tuple(max(Fraction(0),x) for x in xs)

def center(xs):
    if not xs:
        raise ValueError("centering needs at least one sample")
    mean=sum(xs)/len(xs)
    return tuple(x-mean for x in xs)

def prefix(xs):
    return tuple(accumulate(xs))

CATALOG=MappingProxyType({"clip":clip,"center":center,"prefix":prefix})

def select(context):
    if context=="bounded":
        return ("clip","prefix")
    if context=="balanced":
        return ("center","prefix")
    raise ValueError("unknown context")

def execute(plan, values):
    xs=tuple(Fraction(x) for x in values)
    if not xs:
        raise ValueError("nonempty rational sequence required")
    trace=[]
    for name in plan:
        if name not in CATALOG:
            raise ValueError("unknown module")
        before=xs
        xs=CATALOG[name](xs)
        trace.append({"module":name,"before":before,"after":xs})
    return xs,trace

def direct_baseline(context, values):
    """Same specification with conventional branching, no plan/interpreter calls."""
    xs=tuple(Fraction(x) for x in values)
    if not xs:
        raise ValueError("nonempty rational sequence required")
    if context=="bounded":
        transformed=[x if x>0 else Fraction(0) for x in xs]
    elif context=="balanced":
        mean=sum(xs)/len(xs)
        transformed=[x-mean for x in xs]
    else:
        raise ValueError("unknown context")
    result=[]
    running=Fraction(0)
    for x in transformed:
        running+=x
        result.append(running)
    return tuple(result)

def develop(repetitions):
    """A simple program generator, not a biological development model."""
    if type(repetitions) is not int or repetitions<1:
        raise ValueError("positive integer repetitions required")
    return ("prefix",)*repetitions

def memory_bytes(batch,layers,length,kv_heads,head_dim,state_width,bytes_per_scalar):
    dims=(batch,layers,length,kv_heads,head_dim,state_width,bytes_per_scalar)
    if any(type(x) is not int or x<1 for x in dims):
        raise ValueError("positive integer dimensions required")
    return {"kv":2*batch*layers*length*kv_heads*head_dim*bytes_per_scalar,
            "fixed_state":batch*layers*state_width*bytes_per_scalar}

def results():
    records={}
    for context in ("bounded","balanced"):
        y,trace=execute(select(context),(3,-1,2))
        records[context]={"plan":list(select(context)),"output":list(map(str,y)),
                          "trace":[{"module":t["module"],"before":list(map(str,t["before"])),
                                    "after":list(map(str,t["after"]))} for t in trace]}
    return {"input":[3,-1,2],"contexts":records,
            "develop_twice":list(map(str,execute(develop(2),(3,-1,2))[0])),
            "memory":{"configuration":{"batch":1,"layers":24,"length":4096,"kv_heads":8,
                                      "head_dim":64,"state_width":2048,"bytes_per_scalar":2},
                      "bytes":memory_bytes(1,24,4096,8,64,2048,2)},
            "scope":"Exact original digital example and hypothetical memory layout; no trained-model evidence"}

if __name__ == "__main__":
    import json
    print(json.dumps(results(),indent=2))
