"""Small, explicit diagnostics for the Chapter 3 boundary mechanisms."""
import math

def coverage(copies, probability, survival=1., detection=1.):
    if type(copies) is not int or copies < 0:
        raise ValueError("copies must be a nonnegative integer")
    for p in (probability, survival, detection):
        if not math.isfinite(p) or not 0 <= p <= 1:
            raise ValueError("probabilities must lie in [0,1]")
    q=probability*survival*detection
    if copies == 0 or q == 0: return 0.
    if q == 1: return 1.
    return -math.expm1(copies*math.log1p(-q))

def work_depth(candidates, stages):
    if any(type(v) is not int or v < 1 for v in (candidates,stages)):
        raise ValueError("positive integer dimensions required")
    return {"candidates":candidates,"stages":stages,
            "work":candidates*stages,"depth":stages}

def momentum_trace():
    import torch
    p=torch.tensor(1.,dtype=torch.float64,requires_grad=True)
    opt=torch.optim.SGD([p],lr=.1,momentum=.9,weight_decay=0.,dampening=0.)
    rows=[]
    for _ in range(2):
        opt.zero_grad(set_to_none=True)
        before=float(p.detach())
        (.5*p.square()).backward()
        gradient=float(p.grad)
        opt.step()
        rows.append({"before":before,"gradient":gradient,
                     "buffer":float(opt.state[p]["momentum_buffer"]),
                     "after":float(p.detach())})
    return rows

def branch_value(r):
    return 2. if r >= 0. else -1.

def state_control(h=.001, advance_state=False):
    # L(theta;s)=(theta+s)^2. Only the second evaluation changes s in the bad control.
    if not math.isfinite(h) or h <= 0: raise ValueError("positive finite step required")
    plus=(2.+h+3.)**2
    minus=(2.-h+(4. if advance_state else 3.))**2
    return (plus-minus)/(2*h)

def results(dna):
    if dna:
        return {"status":"synthetic independent-copy model, not calibrated chemistry",
                "work_depth":work_depth(4,3),
                "coverage":[{"copies":m,"signal_probability":coverage(m,.1,.5,.8)}
                            for m in (0,1,10,100)],
                "per_copy_signal_probability":.04}
    return {"status":"CPU float64 teaching diagnostics, not a trained genomic model",
            "momentum":momentum_trace(),
            "branch":{"left":branch_value(-.001),"right":branch_value(.001),
                      "central_difference":(branch_value(.001)-branch_value(-.001))/.002},
            "fixed_state_difference":state_control(),
            "changed_state_difference":state_control(advance_state=True)}
