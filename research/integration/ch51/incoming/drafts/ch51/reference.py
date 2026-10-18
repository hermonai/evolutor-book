"""EVOD-51 capability/evidence ledger oracle."""
from dataclasses import dataclass, asdict
import json
LEVELS=("speculative","hypothesized","implemented","tested","benchmark-demonstrated","replicated")
@dataclass
class Claim:
    capability:str; level:str; benchmark:str=""; held_out:bool=False; baseline:bool=False; budget_declared:bool=False
def valid(c):
    if c.level not in LEVELS:return False
    if c.level in ("benchmark-demonstrated","replicated"):
        return bool(c.benchmark and c.held_out and c.baseline and c.budget_declared)
    return True
def promote(c,new_level,benchmark="",held_out=False,baseline=False,budget_declared=False):
    if LEVELS.index(new_level)!=LEVELS.index(c.level)+1: raise ValueError("promotion must be one evidence step")
    n=Claim(c.capability,new_level,benchmark or c.benchmark,held_out or c.held_out,baseline or c.baseline,budget_declared or c.budget_declared)
    if not valid(n): raise ValueError("missing evidence contract")
    return n
def scorecard(claims):
    return {c.capability:c.level for c in claims if valid(c)}
def results():
    c=Claim("persistent-memory","implemented")
    c=promote(c,"tested")
    blocked=False
    try: promote(c,"benchmark-demonstrated")
    except ValueError: blocked=True
    d=promote(c,"benchmark-demonstrated","heldout-memory-suite",True,True,True)
    return {"blocked_without_benchmark_contract":blocked,"demonstrated":asdict(d),"scorecard":scorecard([d,Claim("AGI","hypothesized")])}
if __name__=="__main__": print(json.dumps(results(),indent=2))
