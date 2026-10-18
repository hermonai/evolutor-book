"""EVOD-40 hybrid compressed/addressable memory reference."""
from dataclasses import dataclass
import hashlib,json,re

@dataclass(frozen=True)
class Record:
    rid:str; tenant:str; kind:str; text:str; sources:tuple; created:int; expires:int|None=None

class Memory:
    def __init__(self): self.records={}; self.tombstones=set(); self.clock=0
    def _id(self,tenant,kind,text,sources):
        body=json.dumps([tenant,kind,text,list(sources)],sort_keys=True)
        return hashlib.sha256(body.encode()).hexdigest()[:16]
    def put_event(self,tenant,text,ttl=None):
        rid=self._id(tenant,"event",text,()); rec=Record(rid,tenant,"event",text,(),self.clock,None if ttl is None else self.clock+ttl)
        self.records[rid]=rec; return rec
    def summarize(self,tenant,source_ids,max_words=12):
        src=[self.get(tenant,x) for x in source_ids]
        words=[]
        for r in src:
            for w in r.text.split():
                if w not in words: words.append(w)
        text=" ".join(words[:max_words])
        rid=self._id(tenant,"summary",text,tuple(source_ids))
        rec=Record(rid,tenant,"summary",text,tuple(source_ids),self.clock)
        self.records[rid]=rec; return rec
    def get(self,tenant,rid):
        if rid in self.tombstones or rid not in self.records: raise KeyError(rid)
        r=self.records[rid]
        if r.tenant!=tenant: raise PermissionError("tenant")
        if r.expires is not None and self.clock>=r.expires: raise KeyError("expired")
        return r
    def retrieve(self,tenant,query,k=3):
        terms=set(re.findall(r"[a-z0-9]+",query.lower())); scored=[]
        for r in self.records.values():
            if r.rid in self.tombstones or r.tenant!=tenant or (r.expires is not None and self.clock>=r.expires): continue
            rt=set(re.findall(r"[a-z0-9]+",r.text.lower()))
            score=len(terms & rt)
            if score: scored.append((score,-r.created,r.rid,r))
        scored.sort(reverse=True); return [x[3] for x in scored[:k]]
    def forget(self,tenant,rid):
        self.get(tenant,rid); self.tombstones.add(rid)
    def tick(self,n=1): self.clock+=n
    def rehydrate(self,tenant,summary_id,max_sources=4):
        s=self.get(tenant,summary_id)
        if s.kind!="summary": raise ValueError("summary required")
        return [self.get(tenant,x) for x in s.sources[:max_sources]]
    def provenance(self,tenant,rid):
        r=self.get(tenant,rid); return {"rid":r.rid,"kind":r.kind,"sources":list(r.sources)}

def results():
    m=Memory()
    a=m.put_event("t1","DOGMA compressed state supports streaming continuity")
    b=m.put_event("t1","Hermon KV memory supports addressable token history")
    c=m.put_event("t1","retrieval returns evidence with provenance",ttl=2)
    s=m.summarize("t1",[a.rid,b.rid,c.rid],10)
    hits=m.retrieve("t1","memory provenance retrieval",3)
    before=[x.rid for x in hits]
    # Rehydrate while all sources are still live; provenance is not a promise that
    # a source will remain retained forever.
    rehydrated_before=[x.rid for x in m.rehydrate("t1",s.rid)]
    m.tick(2)
    after=[x.rid for x in m.retrieve("t1","memory provenance retrieval",3)]
    expired_source_available=True
    try:
        m.get("t1",c.rid)
    except KeyError:
        expired_source_available=False
    return {"summary":s.text,"summary_sources":len(s.sources),
            "retrieval_before":before,"retrieval_after_expiry":after,
            "rehydrated_before_expiry":rehydrated_before,
            "expired_source_available":expired_source_available}
if __name__=="__main__": print(json.dumps(results(),indent=2))
