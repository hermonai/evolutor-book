"""EVOD-47 measurement-analysis teaching oracle. Synthetic inputs only."""
from dataclasses import dataclass
import math,json

def percentile(xs,q):
    if not xs: raise ValueError("empty")
    ys=sorted(float(x) for x in xs)
    # nearest-rank style index for deterministic teaching use
    i=max(0,min(len(ys)-1,math.ceil(q*len(ys))-1))
    return ys[i]

def arithmetic_intensity(flops,bytes_moved):
    if bytes_moved<=0: raise ValueError("bytes")
    return flops/bytes_moved

def roofline_bound(flops,bytes_moved,peak_flops,bandwidth):
    """Upper-bound throughput in FLOP/s = min(compute peak, bandwidth*AI)."""
    ai=arithmetic_intensity(flops,bytes_moved)
    return min(float(peak_flops),float(bandwidth)*ai)

def classify(ai,peak_flops,bandwidth):
    ridge=peak_flops/bandwidth
    return "memory-bound-region" if ai<ridge else "compute-bound-region"

@dataclass(frozen=True)
class Request:
    arrival_ms:float; first_token_ms:float; token_times_ms:tuple; ok:bool=True
    def ttft(self): return self.first_token_ms-self.arrival_ms
    def itls(self):
        t=(self.first_token_ms,)+self.token_times_ms
        return tuple(t[i]-t[i-1] for i in range(1,len(t)))
    def completion(self): return self.token_times_ms[-1] if self.token_times_ms else self.first_token_ms

def metrics(reqs,window_ms,ttft_slo,itl_slo):
    tt=[r.ttft() for r in reqs]; itl=[x for r in reqs for x in r.itls()]
    out_tokens=sum(1+len(r.token_times_ms) for r in reqs)
    good=0
    for r in reqs:
        if r.ok and r.ttft()<=ttft_slo and all(x<=itl_slo for x in r.itls()): good+=1
    return {"requests":len(reqs),"p50_ttft":percentile(tt,.50),"p95_ttft":percentile(tt,.95),
            "p95_itl":percentile(itl,.95) if itl else 0.0,
            "output_tokens_per_s":out_tokens/(window_ms/1000.0),
            "goodput_req_per_s":good/(window_ms/1000.0),"slo_attainment":good/len(reqs)}

def speedup(base_ms,new_ms):
    if base_ms<=0 or new_ms<=0: raise ValueError("time")
    return base_ms/new_ms

def results():
    reqs=[Request(0,40,(55,70,85)),Request(10,70,(90,110,130)),Request(20,150,(180,210),True)]
    m=metrics(reqs,250,100,25)
    ai=arithmetic_intensity(2e12,1e12)
    return {"metrics":m,"ai_flop_per_byte":ai,
            "roofline_tflops":roofline_bound(2e12,1e12,100e12,2e12)/1e12,
            "region":classify(ai,100e12,2e12),"speedup_example":speedup(20,10)}
if __name__=="__main__":print(json.dumps(results(),indent=2))
