"""Exact quadratic adaptation and budgeted selection, not trained model evidence."""
from dataclasses import dataclass
import math


def vector(x):
    x = tuple(x)
    if not x or any(not isinstance(v, (float, int)) or not math.isfinite(v) for v in x):
        raise ValueError("nonempty finite vector")
    return x


def aligned(a, b):
    a, b = vector(a), vector(b)
    if len(a) != len(b):
        raise ValueError("equal dimensions")
    return a, b


def quality(theta, target):
    theta, target = aligned(theta, target)
    return max(0.0, 1-sum((a-b)**2 for a, b in zip(theta, target))/4)


def step(theta, target, lr=.5, anchor=None, importance=None, lam=0.0):
    theta, target = aligned(theta, target)
    if not math.isfinite(lr) or lr <= 0 or not math.isfinite(lam) or lam < 0:
        raise ValueError("positive learning rate and nonnegative penalty")
    if anchor is None:
        if importance is not None or lam != 0:
            raise ValueError("penalty needs an anchor")
        anchor, importance = theta, (0.0,)*len(theta)
    else:
        anchor, importance = aligned(anchor, importance)
        if len(anchor) != len(theta) or any(f < 0 for f in importance):
            raise ValueError("aligned nonnegative importance")
    return tuple(x-lr*((x-t)+lam*f*(x-a))
                 for x, t, a, f in zip(theta, target, anchor, importance))


def closed_form(theta, target, steps, lr=.5, anchor=None, importance=None, lam=0.0):
    """Solve diagonal affine dynamics independently of repeated step calls."""
    theta, target = aligned(theta, target)
    if type(steps) is not int or steps < 0:
        raise ValueError("nonnegative step count")
    step(theta, target, lr, anchor, importance, lam)  # input contract only
    if anchor is None:
        anchor, importance = theta, (0.0,)*len(theta)
    out = []
    for x, t, a, f in zip(theta, target, anchor, importance):
        curvature = 1+lam*f
        optimum = (t+lam*f*a)/curvature
        out.append(optimum+(1-lr*curvature)**steps*(x-optimum))
    return tuple(out)


def accuracy_matrix(targets, steps=4, lam=0.0):
    """Historical API name retained; entries are synthetic quality, not accuracy."""
    targets = tuple(vector(t) for t in targets)
    if (len(targets) != 2 or any(len(t) != 2 for t in targets)
            or type(steps) is not int or steps < 1):
        raise ValueError("two two-dimensional tasks, positive steps")
    theta, rows = (0.0, 0.0), []
    anchor = None
    for k, target in enumerate(targets):
        if k == 1:
            anchor = theta
        for _ in range(steps):
            theta = step(theta, target, anchor=anchor,
                         importance=(1., 1.) if anchor is not None else None,
                         lam=lam if anchor is not None else 0.)
        rows.append([quality(theta, t) for t in targets])
    return rows, theta


def matrix(A):
    A = tuple(tuple(row) for row in A)
    if (not A or any(len(row) != len(A) for row in A)
            or any(not math.isfinite(v) or not 0 <= v <= 1 for row in A for v in row)):
        raise ValueError("square finite quality matrix in [0,1]")
    return A


def forgetting(A):
    A = matrix(A)
    # Best observed since acquisition, including final row: nonnegative convention.
    return [max(A[t][j] for t in range(j, len(A)))-A[-1][j] for j in range(len(A))]


def backward_transfer(A):
    A = matrix(A)
    return None if len(A) == 1 else sum(A[-1][j]-A[j][j] for j in range(len(A)-1))/(len(A)-1)


def replay_step(theta, new, old, rho=.5, lr=.5):
    theta, new = aligned(theta, new)
    _, old = aligned(theta, old)
    if not 0 <= rho <= 1 or not math.isfinite(rho):
        raise ValueError("old-data fraction in [0,1]")
    target = tuple((1-rho)*n+rho*o for n, o in zip(new, old))
    return step(theta, target, lr)


@dataclass(frozen=True)
class Candidate:
    cid: str
    quality: float
    cost: float
    risk: float
    forgetting: float


def pareto(candidates, max_risk):
    """Hard risk feasibility, then maximize quality and minimize cost/forgetting."""
    candidates = tuple(candidates)
    if len({c.cid for c in candidates}) != len(candidates) or not math.isfinite(max_risk) or max_risk < 0:
        raise ValueError("unique candidates and finite nonnegative risk ceiling")
    for c in candidates:
        if (not c.cid or any(not math.isfinite(v) for v in (c.quality, c.cost, c.risk, c.forgetting))
                or not 0 <= c.quality <= 1 or min(c.cost, c.risk, c.forgetting) < 0):
            raise ValueError("valid candidate measurements")
    feasible = [c for c in candidates if c.risk <= max_risk]

    def dominates(a, b):
        va, vb = (-a.quality, a.cost, a.forgetting), (-b.quality, b.cost, b.forgetting)
        return all(x <= y for x, y in zip(va, vb)) and any(x < y for x, y in zip(va, vb))

    return tuple(sorted(c.cid for c in feasible if not any(dominates(d, c) for d in feasible)))


def population_step(pop, targets, evaluation_budget):
    """Retain deterministic exploit/mutate fixture with explicit evaluation count."""
    pop, targets = tuple(vector(p) for p in pop), tuple(vector(t) for t in targets)
    if (not pop or not targets or type(evaluation_budget) is not int
            or evaluation_budget < len(pop)*len(targets)):
        raise ValueError("insufficient candidate-task evaluation budget")
    scores = [(sum(quality(x, t) for t in targets)/len(targets), i, x) for i, x in enumerate(pop)]
    elite = min(scores, key=lambda row: (-row[0], row[1]))[2]
    if len(elite) != 2:
        raise ValueError("two-coordinate mutation fixture")
    return (elite, (elite[0]+.1, elite[1]), (elite[0], elite[1]-.1)), len(pop)*len(targets)


def results():
    targets = [(1., 0.), (0., 1.)]
    rows = []
    for name, lam in (("Sequential", 0.), ("Anchored", 1.)):
        A, theta = accuracy_matrix(targets, lam=lam)
        rows.append({"method": name, "old": A[-1][0], "new": A[-1][1],
                     "forget": forgetting(A)[0], "bwt": backward_transfer(A)})
    return {"adaptation": rows,
            "naive_matrix": accuracy_matrix(targets)[0],
            "anchored_matrix": accuracy_matrix(targets, lam=1)[0],
            "pareto": pareto([Candidate("a", .9, 10, .01, .1), Candidate("b", .85, 5, .01, .05),
                              Candidate("c", .8, 12, .01, .2), Candidate("unsafe", 1., 1, .5, 0.)], .02),
            "population": population_step([(0, 0), (1, 0), (0, 1)], targets, 6)}


TABLES = [("adaptation", ["Update", "Old Q", "New Q", "Forgetting", "BWT"],
           ["method", "old", "new", "forget", "bwt"], "lrrrr")]
PLOTS = []
LISTINGS = ["step", "closed_form", "forgetting", "replay_step", "pareto"]
