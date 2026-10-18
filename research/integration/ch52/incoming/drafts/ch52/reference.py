"""EVOD-52 reproducible-research ledger oracle."""
from dataclasses import dataclass, asdict
import json, hashlib

LEVELS=("speculative","hypothesized","implemented","tested","benchmark-demonstrated","replicated")

@dataclass(frozen=True)
class Claim:
    cid:str; text:str; level:str; falsifier:str

@dataclass(frozen=True)
class Experiment:
    eid:str; claim_id:str; baseline:str; budget:str; metric:str; threshold:str
    seeds:tuple; artifact_digest:str

@dataclass(frozen=True)
class Failure:
    fid:str; claim_id:str; experiment_id:str; category:str; symptom:str; counterexample:str

class Ledger:
    def __init__(self):
        self.claims={}; self.experiments={}; self.failures={}
    def add_claim(self,c):
        if c.cid in self.claims or c.level not in LEVELS or not c.falsifier: raise ValueError("invalid claim")
        self.claims[c.cid]=c
    def add_experiment(self,e):
        if e.eid in self.experiments or e.claim_id not in self.claims: raise ValueError("invalid experiment")
        if not all((e.baseline,e.budget,e.metric,e.threshold,e.seeds,e.artifact_digest)): raise ValueError("incomplete experiment")
        self.experiments[e.eid]=e
    def add_failure(self,f):
        if f.fid in self.failures or f.claim_id not in self.claims or f.experiment_id not in self.experiments:
            raise ValueError("invalid failure")
        self.failures[f.fid]=f
    def promote(self,cid,new_level,evidence_eid=None):
        old=self.claims[cid]
        if LEVELS.index(new_level)!=LEVELS.index(old.level)+1: raise ValueError("one level at a time")
        if new_level in ("benchmark-demonstrated","replicated"):
            if evidence_eid not in self.experiments: raise ValueError("benchmark evidence required")
            e=self.experiments[evidence_eid]
            if e.claim_id!=cid: raise ValueError("wrong claim evidence")
        self.claims[cid]=Claim(old.cid,old.text,new_level,old.falsifier)
    def capsule(self):
        obj={"claims":[asdict(x) for x in sorted(self.claims.values(),key=lambda z:z.cid)],
             "experiments":[asdict(x) for x in sorted(self.experiments.values(),key=lambda z:z.eid)],
             "failures":[asdict(x) for x in sorted(self.failures.values(),key=lambda z:z.fid)]}
        raw=json.dumps(obj,sort_keys=True,separators=(",",":")).encode()
        return {"ledger":obj,"sha256":hashlib.sha256(raw).hexdigest()}

def results():
    L=Ledger()
    L.add_claim(Claim("C1","DOGMA state yields a general efficiency advantage","hypothesized",
                      "Fails capacity/compute-matched recurrent/SSM baselines across preregistered tasks/seeds."))
    L.add_experiment(Experiment("E1","C1","GRU+SSM+Transformer","100 accelerator-hours",
                                "quality-at-fixed-latency","DOGMA > best baseline with CI excluding 0",
                                (11,22,33),"sha256:model+data+code"))
    L.add_failure(Failure("F1","C1","E1","baseline-regression","one task loses",
                          "SSM exceeds DOGMA at matched budget on preregistered task X"))
    cap=L.capsule()
    return {"claims":len(L.claims),"experiments":len(L.experiments),"failures":len(L.failures),
            "claim_level":L.claims["C1"].level,"capsule_sha256":cap["sha256"]}
if __name__=="__main__": print(json.dumps(results(),indent=2))
