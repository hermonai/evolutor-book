"""EVOD-48 genomic application methodology oracle. Synthetic fixtures only."""
from dataclasses import dataclass
import math,json,random
COMP=str.maketrans('ACGTN','TGCAN')
def rc(seq): return seq.upper().translate(COMP)[::-1]
def gc(seq):
 s=[x for x in seq.upper() if x in 'ACGT']; return 0.0 if not s else sum(x in 'GC' for x in s)/len(s)
def onehot(seq):
 alpha='ACGT'; return [[1 if b==a else 0 for a in alpha] for b in seq.upper()]
@dataclass(frozen=True)
class Example: eid:str; group:str; seq:str; label:int

def group_split(examples,test_groups):
 test=set(test_groups); tr=[x for x in examples if x.group not in test]; te=[x for x in examples if x.group in test]
 assert not ({x.group for x in tr}&{x.group for x in te}); return tr,te

def motif_score(seq,motif='CG'):
 s=seq.upper(); return sum(s[i:i+len(motif)]==motif for i in range(max(0,len(s)-len(motif)+1)))
def invariant_score(seq): return 0.5*(motif_score(seq,'CG')+motif_score(rc(seq),'CG'))
def accuracy(y,p): return sum(int(a==b) for a,b in zip(y,p))/len(y)
def mcc(y,p):
 tp=sum(a==1 and b==1 for a,b in zip(y,p));tn=sum(a==0 and b==0 for a,b in zip(y,p));fp=sum(a==0 and b==1 for a,b in zip(y,p));fn=sum(a==1 and b==0 for a,b in zip(y,p))
 den=math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn)); return 0.0 if den==0 else (tp*tn-fp*fn)/den
def brier(y,prob): return sum((a-b)**2 for a,b in zip(y,prob))/len(y)
def bootstrap_metric(y,p,metric,n=200,seed=7):
 rng=random.Random(seed); vals=[]
 for _ in range(n):
  idx=[rng.randrange(len(y)) for _ in y]; vals.append(metric([y[i] for i in idx],[p[i] for i in idx]))
 vals.sort(); return vals[int(.025*n)],vals[min(n-1,int(.975*n))]
def results():
 ex=[Example('a','chr1','AACGTT',1),Example('b','chr1','TTTTAA',0),Example('c','chr2','CGCGAA',1),Example('d','chr3','ATATAT',0)]
 tr,te=group_split(ex,{'chr3'}); y=[x.label for x in ex]; pred=[int(invariant_score(x.seq)>0) for x in ex]
 return {'rc_example':rc('AACGTN'),'rc_involution':rc(rc('AACGTN'))=='AACGTN','train_groups':sorted({x.group for x in tr}),'test_groups':sorted({x.group for x in te}),'mcc':mcc(y,pred),'accuracy':accuracy(y,pred),'brier_example':brier(y,[.8,.2,.9,.1])}
if __name__=='__main__':print(json.dumps(results(),indent=2))
