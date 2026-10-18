"""EVOD-37 continuous-batching and precision teaching oracle.

Scheduling uses abstract token-work units, not GPU milliseconds. Precision helpers
measure representation error; they do not claim a hardware speedup.
"""
from dataclasses import dataclass, field
import json, math, numpy as np

@dataclass
class Req:
    rid:str
    arrival:int
    prompt:int
    output:int
    prefilled:int=0
    decoded:int=0
    first_token_tick:int|None=None
    token_ticks:list=field(default_factory=list)
    done:bool=False

def ready(reqs,tick):
    return [r for r in reqs if r.arrival<=tick and not r.done]

def schedule_iteration(reqs,tick,token_budget,prefill_chunk):
    if token_budget<=0 or prefill_chunk<=0:raise ValueError("positive budgets")
    work=[];budget=token_budget
    active=ready(reqs,tick)

    # Decode-first protects ongoing inter-token latency in this teaching policy.
    for r in active:
        if budget==0:break
        if r.prefilled==r.prompt and r.decoded<r.output:
            work.append((r,"decode",1));budget-=1

    # Chunked prefill uses remaining token budget; long prompts cannot monopolize
    # an unbounded iteration.
    for r in active:
        if budget==0:break
        remain=r.prompt-r.prefilled
        if remain>0:
            n=min(remain,prefill_chunk,budget)
            work.append((r,"prefill",n));budget-=n
    return work

def apply_iteration(work,tick):
    for r,kind,n in work:
        if kind=="prefill":
            r.prefilled+=n
        elif kind=="decode":
            r.decoded+=1
            r.token_ticks.append(tick)
            if r.first_token_tick is None:r.first_token_tick=tick
            if r.decoded==r.output:r.done=True
        else:raise ValueError("unknown work")

def simulate(reqs,token_budget=4,prefill_chunk=2,max_ticks=1000):
    tick=0;timeline=[]
    while not all(r.done for r in reqs):
        work=schedule_iteration(reqs,tick,token_budget,prefill_chunk)
        apply_iteration(work,tick)
        timeline.append([(r.rid,k,n) for r,k,n in work])
        tick+=1
        if tick>max_ticks:raise RuntimeError("simulation did not finish")
    return timeline

def metrics(r):
    if r.first_token_tick is None:raise ValueError("no output")
    itl=[b-a for a,b in zip(r.token_ticks,r.token_ticks[1:])]
    return {"ttft":r.first_token_tick-r.arrival,
            "itl_mean":float(np.mean(itl)) if itl else 0.0,
            "itl_max":max(itl) if itl else 0,
            "completion":r.token_ticks[-1]-r.arrival}

def fp16_round(x):
    return np.asarray(x,dtype=np.float16).astype(np.float32)

def bf16_round(x):
    """Round float32 to nearest-ish BF16 by truncating lower 16 mantissa bits.
    This is a representation study, not a substitute for native BF16 kernels."""
    a=np.asarray(x,dtype=np.float32).copy()
    u=a.view(np.uint32)
    # Round-to-nearest-even approximation commonly used for BF16 conversion.
    lsb=(u>>16)&1
    u += np.uint32(0x7FFF)+lsb
    u &= np.uint32(0xFFFF0000)
    return u.view(np.float32)

def int8_symmetric(x):
    x=np.asarray(x,dtype=np.float32)
    m=float(np.max(np.abs(x)))
    if m==0:return np.zeros_like(x,dtype=np.int8),1.0
    scale=m/127.0
    q=np.clip(np.rint(x/scale),-127,127).astype(np.int8)
    return q,scale

def dequant_int8(q,scale):
    return np.asarray(q,dtype=np.float32)*float(scale)

def quality(ref,test):
    ref=np.asarray(ref,dtype=np.float64);test=np.asarray(test,dtype=np.float64)
    if ref.shape!=test.shape:raise ValueError("shape")
    err=np.abs(ref-test)
    denom=np.linalg.norm(ref)
    return {"max_abs":float(err.max()) if err.size else 0.0,
            "rmse":float(np.sqrt(np.mean((ref-test)**2))) if err.size else 0.0,
            "relative_l2":float(np.linalg.norm(ref-test)/(denom if denom else 1.0)),
            "argmax_equal":bool(np.argmax(ref)==np.argmax(test)) if err.size else True}

def gate(report,max_abs,relative_l2,require_argmax=True):
    return (report["max_abs"]<=max_abs and report["relative_l2"]<=relative_l2
            and (report["argmax_equal"] or not require_argmax))

def results():
    reqs=[Req("A",0,5,3),Req("B",1,1,2),Req("C",2,3,1)]
    timeline=simulate(reqs,token_budget=4,prefill_chunk=2)
    x=np.array([0.01,-0.4,1.7,8.2,-3.1],dtype=np.float32)
    q,s=int8_symmetric(x);x8=dequant_int8(q,s)
    logits=np.array([.1,.2,3.0,-1.0],dtype=np.float32)
    report=quality(logits,bf16_round(logits))
    return {"timeline":timeline,"metrics":{r.rid:metrics(r) for r in reqs},
            "int8_scale":s,"int8_report":quality(x,x8),
            "bf16_logit_report":report,
            "bf16_gate":gate(report,max_abs=.02,relative_l2=.01)}
if __name__=="__main__":print(json.dumps(results(),indent=2))
