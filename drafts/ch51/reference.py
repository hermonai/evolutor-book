"""Metadata gates for bounded capability claims, not verification of real evidence."""
from dataclasses import dataclass, replace
import math
import re

LEVELS = ("speculative", "hypothesized", "implemented", "tested", "benchmark-demonstrated", "replicated")


def sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


@dataclass(frozen=True)
class Evidence:
    eid: str
    capability: str
    suite: str
    artifact_digest: str
    data_digest: str
    baseline: str
    budget: str
    unit: str
    lower_bound: float
    threshold: float
    held_out: bool
    outcome: str
    evaluator: str
    independent: bool = False


@dataclass(frozen=True)
class Claim:
    capability: str
    level: str
    scope: str
    falsifier: str
    implementation_digest: str = ""
    tests_digest: str = ""
    evidence: tuple = ()


def supports(e, capability):
    return (isinstance(e, Evidence) and e.capability == capability
            and all(isinstance(v, str) and bool(v) for v in
                    (e.eid, e.suite, e.baseline, e.budget, e.unit, e.evaluator))
            and sha(e.artifact_digest) and sha(e.data_digest)
            and e.held_out is True and type(e.independent) is bool
            and e.outcome == "success"
            and math.isfinite(e.lower_bound) and math.isfinite(e.threshold)
            and e.lower_bound > e.threshold)


def valid(c, records=()):
    if (not isinstance(c, Claim) or c.level not in LEVELS
            or not all(isinstance(v, str) and bool(v) for v in
                       (c.capability, c.scope, c.falsifier))
            or not isinstance(c.evidence, tuple) or len(set(c.evidence)) != len(c.evidence)):
        return False
    stage = LEVELS.index(c.level)
    if stage >= 2 and not sha(c.implementation_digest):
        return False
    if stage >= 3 and not sha(c.tests_digest):
        return False
    records = tuple(records)
    by_id = {e.eid: e for e in records}
    if len(by_id) != len(records) or any(eid not in by_id for eid in c.evidence):
        return False
    chosen = [by_id[eid] for eid in c.evidence]
    supporting = [e for e in chosen if supports(e, c.capability)
                  and e.artifact_digest == c.implementation_digest]
    if stage >= 4 and not supporting:
        return False
    if stage >= 5:
        # A declaration of independence is necessary metadata, not proof of it.
        return any(a.eid != b.eid and a.evaluator != b.evaluator and b.independent
                   and a.suite == b.suite and a.data_digest == b.data_digest
                   and a.artifact_digest == b.artifact_digest
                   and a.baseline == b.baseline and a.budget == b.budget
                   and a.unit == b.unit and a.threshold == b.threshold
                   for a in supporting for b in supporting)
    return True


def promote(c, new_level, records=(), **changes):
    if not valid(c, records) or new_level not in LEVELS:
        raise ValueError("valid source claim and target level required")
    if LEVELS.index(new_level) != LEVELS.index(c.level)+1:
        raise ValueError("one evidence step at a time")
    if set(changes)-{"implementation_digest", "tests_digest", "evidence"}:
        raise ValueError("promotion cannot silently change scope or falsifier")
    candidate = replace(c, level=new_level, **changes)
    if not valid(candidate, records):
        raise ValueError("missing distinct supporting evidence")
    return candidate


def scorecard(claims, records=()):
    claims = tuple(claims)
    if len({c.capability for c in claims}) != len(claims):
        raise ValueError("duplicate capability would hide scope")
    if any(not valid(c, records) for c in claims):
        raise ValueError("invalid claim must remain visible as an error")
    return {c.capability: c.level for c in claims}


def acquisition_area(actions, quality):
    """Normalized trapezoidal area over one declared action-budget axis."""
    x, y = tuple(actions), tuple(quality)
    if (len(x) != len(y) or len(x) < 2 or x[0] != 0
            or any(not math.isfinite(v) for v in x+y)
            or any(b <= a for a, b in zip(x, x[1:]))
            or any(not 0 <= v <= 1 for v in y)):
        raise ValueError("increasing nonnegative budget and aligned quality")
    return sum((b-a)*(u+v)/2 for a, b, u, v in zip(x, x[1:], y, y[1:]))/x[-1]


def zero_failure_upper(n, alpha=.05):
    """One-sided exact upper bound after zero independent Bernoulli failures."""
    if type(n) is not int or n < 1 or not 0 < alpha < 1:
        raise ValueError("positive sample size, alpha in (0,1)")
    return -math.expm1(math.log(alpha)/n)


def results():
    toy = Claim("toy-retrieval", "tested", "fixed synthetic records only",
                "fails held-out retrieval criterion", "a"*64, "b"*64)
    blocked = False
    try:
        promote(toy, "benchmark-demonstrated")
    except ValueError:
        blocked = True
    return {"blocked_without_benchmark": blocked,
            "areas": [{"method": "Early acquisition", "area": acquisition_area([0,1,2],[0,.8,1])},
                      {"method": "Late acquisition", "area": acquisition_area([0,1,2],[0,.2,1])}],
            "zero_failures": [{"trials": n, "upper": zero_failure_upper(n)} for n in [10,100,1000]],
            "scorecard": scorecard([toy, Claim("AGI", "speculative", "unestablished breadth", "fails preregistered breadth tests")])}


TABLES = [("areas", ["Illustrative curve", "Normalized area"], ["method", "area"], "lr"),
          ("zero_failures", ["Independent trials", "95 percent upper failure bound"], ["trials", "upper"], "rr")]
PLOTS = []
LISTINGS = ["supports", "valid", "promote", "acquisition_area", "zero_failure_upper"]
