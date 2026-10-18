"""EVOD-38 transparent speculative-decoding and tiled-attention oracles."""
import json, math
import numpy as np
def normalize(x):
    x=np.asarray(x,dtype=np.float64)
    if x.ndim!=1 or np.any(x<0) or not np.isfinite(x).all() or x.sum()<=0: raise ValueError("probabilities")
    return x/x.sum()
def acceptance_probabilities(p,q):
    p,q=normalize(p),normalize(q); a=np.ones_like(p); nz=q>0; a[nz]=np.minimum(1,p[nz]/q[nz]); return a
def correction_distribution(p,q):
    p,q=normalize(p),normalize(q); z=np.maximum(p-q,0); return p.copy() if z.sum()==0 else z/z.sum()
def output_distribution(p,q):
    p,q=normalize(p),normalize(q); accepted=q*acceptance_probabilities(p,q); return accepted+(1-accepted.sum())*correction_distribution(p,q)
def sample_cat(p,rng): return int(rng.choice(len(normalize(p)),p=normalize(p)))
def speculative_one(p,q,rng):
    p,q=normalize(p),normalize(q); x=sample_cat(q,rng); a=min(1,p[x]/q[x]) if q[x]>0 else 1
    return (x,True) if rng.random()<a else (sample_cat(correction_distribution(p,q),rng),False)
def speculative_block(ps,qs,seed=0):
    if len(ps)!=len(qs): raise ValueError("length")
    rng=np.random.default_rng(seed); out=[]; n=0
    for p,q in zip(ps,qs):
        x,ok=speculative_one(p,q,rng); out.append(x)
        if ok:n+=1
        else:break
    return out,n
def softmax1(x):
    x=np.asarray(x,dtype=np.float64); e=np.exp(x-np.max(x)); return e/e.sum()
def dense_attention(q,K,V):
    q=np.asarray(q,dtype=np.float64);K=np.asarray(K,dtype=np.float64);V=np.asarray(V,dtype=np.float64)
    if q.ndim!=1 or K.ndim!=2 or V.ndim!=2 or K.shape[0]!=V.shape[0] or K.shape[1]!=q.shape[0]: raise ValueError("shape")
    return softmax1(K@q/math.sqrt(q.shape[0]))@V
def tiled_online_attention(q,K,V,tile=4):
    q=np.asarray(q,dtype=np.float64);K=np.asarray(K,dtype=np.float64);V=np.asarray(V,dtype=np.float64)
    if tile<=0 or K.ndim!=2 or V.ndim!=2 or K.shape[0]!=V.shape[0] or K.shape[1]!=q.shape[0]: raise ValueError("shape")
    m=-np.inf;l=0.;acc=np.zeros(V.shape[1]);scale=math.sqrt(q.shape[0])
    for i in range(0,len(K),tile):
        s=K[i:i+tile]@q/scale; mt=float(np.max(s)); mn=max(m,mt); alpha=0 if not np.isfinite(m) else math.exp(m-mn); w=np.exp(s-mn)
        acc=acc*alpha+w@V[i:i+tile]; l=l*alpha+w.sum(); m=mn
    return acc/l
def traffic_model(T,dq,dv,b=2,tiled=False):
    base=(dq+T*dq+T*dv+dv)*b; extra=0 if tiled else 2*T*b; return {"base":base,"score_read_write":extra,"total":base+extra}
def results():
    p=np.array([.55,.25,.15,.05]);q=np.array([.45,.35,.15,.05]);m=output_distribution(p,q)
    g=np.random.default_rng(38);K=g.normal(size=(11,4));V=g.normal(size=(11,6));qq=g.normal(size=4);a=dense_attention(qq,K,V);b=tiled_online_attention(qq,K,V,3)
    block,n=speculative_block([p]*3,[q]*3,38)
    return {"spec_max_abs":float(np.max(np.abs(m-normalize(p)))),"expected_acceptance":float(np.minimum(normalize(p),normalize(q)).sum()),"sample_block":block,"accepted_before_stop":n,"attention_max_abs":float(np.max(np.abs(a-b))),"traffic_dense":traffic_model(4096,128,128),"traffic_tiled":traffic_model(4096,128,128,tiled=True)}
if __name__=="__main__": print(json.dumps(results(),indent=2))
