"""Database-engine comparison oracle: logical alternatives, physical costs, WAL ordering."""
from dataclasses import dataclass
import json
@dataclass(frozen=True)
class Plan: name:str; latency:float; memory:float; risk:float
def cost(p,w=(1.,.1,10.)): return w[0]*p.latency+w[1]*p.memory+w[2]*p.risk
def choose(plans,w=(1.,.1,10.)): return min(plans,key=lambda p:(cost(p,w),p.name))
class WalStore:
 def __init__(self): self.log=[];self.durable_lsn=0;self.data={};self.page_lsn={}
 def append(self,key,value): self.log.append((len(self.log)+1,key,value));return len(self.log)
 def flush_log(self,lsn): self.durable_lsn=max(self.durable_lsn,lsn)
 def write_page(self,key,value,lsn):
  if lsn>self.durable_lsn: raise RuntimeError("WAL violation")
  self.data[key]=value;self.page_lsn[key]=lsn
 def recover(self):
  for lsn,k,v in self.log:
   if lsn<=self.durable_lsn and self.page_lsn.get(k,0)<lsn:self.data[k]=v;self.page_lsn[k]=lsn
def inference_breaks_sql():
 return {"row_operator":"token step is stateful/prefix-dependent","transaction":"sampling is not ACID commit","buffer_page":"KV/native state has model semantics","optimizer":"quality/risk joins latency/memory cost"}
def results():
 ps=[Plan("dogma",5,4,.03),Plan("hermon",4,8,.02)];best=choose(ps)
 s=WalStore();l=s.append("artifact","v2")
 blocked=False
 try:s.write_page("artifact","v2",l)
 except RuntimeError:blocked=True
 s.flush_log(l);s.write_page("artifact","v2",l)
 return {"best":best.name,"wal_blocked_before_flush":blocked,"recovered":s.data["artifact"],"analogy_breaks":len(inference_breaks_sql())}
if __name__=="__main__":print(json.dumps(results(),indent=2))
