"""EVOD-50 continual-learning/population teaching oracle."""
import json, math

def quality(theta,target):
    return max(0.0, 1.0 - sum((a-b)**2 for a,b in zip(theta,target))/4.0)

def step(theta,target,lr=.5,anchor=None,importance=None,lam=0.0):
    # Gradient of 1/2 ||theta-target||^2 plus EWC-like quadratic anchor.
    out=[]
    for i,(x,t) in enumerate(zip(theta,target)):
        g=x-t
        if anchor is not None: g += lam*importance[i]*(x-anchor[i])
        out.append(x-lr*g)
    return tuple(out)

def accuracy_matrix(targets,steps=4,lam=0.0):
    theta=(0.0,0.0); rows=[]; anchor=None; importance=(1.0,1.0)
    for k,target in enumerate(targets):
        if k==1: anchor=theta
        for _ in range(steps): theta=step(theta,target,anchor=anchor,importance=importance,lam=lam if k else 0.0)
        rows.append([quality(theta,t) for t in targets])
    return rows,theta

def forgetting(A):
    T=len(A)
    return [max(A[t][j] for t in range(j,T))-A[-1][j] for j in range(T)]

def population_step(pop,targets):
    scored=sorted(((sum(quality(x,t) for t in targets)/len(targets),x) for x in pop),reverse=True)
    elite=scored[0][1]
    # deterministic symmetric mutations around elite
    return [elite,(elite[0]+.1,elite[1]),(elite[0],elite[1]-.1)]

def results():
    targets=[(1.0,0.0),(0.0,1.0)]
    naive,_=accuracy_matrix(targets,lam=0.0)
    ewc,_=accuracy_matrix(targets,lam=1.0)
    pop=population_step([(0,0),(1,0),(0,1)],targets)
    return {"naive_matrix":naive,"ewc_matrix":ewc,"naive_forgetting":forgetting(naive),
            "ewc_forgetting":forgetting(ewc),"population":pop}
if __name__=="__main__": print(json.dumps(results(),indent=2))
