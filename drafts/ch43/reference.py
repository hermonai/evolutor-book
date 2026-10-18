"""Immutable lineage and serialized governance state machine.

Role labels are caller-supplied trust assumptions, not cryptographic identity.
CAS is simulated with a revision; no database atomicity or live deployment.
"""
from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import math


class Stage(str, Enum):
    CANDIDATE = "candidate"
    EVALUATED = "evaluated"
    CANARY = "canary"
    ACTIVE = "active"
    RETIRED = "retired"
    REJECTED = "rejected"


@dataclass(frozen=True)
class Artifact:
    aid: str
    parent: str | None
    payload: str
    recipe: str
    training_data: str
    state_fingerprint: str


@dataclass(frozen=True)
class Gate:
    metric: str
    direction: str
    threshold: float


@dataclass(frozen=True)
class Evaluation:
    artifact: str
    suite: str
    data: str
    evaluator: str
    budget: int
    metrics: tuple
    passed: bool


def finite(x):
    if type(x) not in (int, float) or not math.isfinite(x):
        raise ValueError("finite scalar, excluding bool")
    return x


def gates_pass(metrics, gates):
    if not gates or len({g.metric for g in gates}) != len(gates):
        raise ValueError("nonempty unique gates")
    for g in gates:
        finite(g.threshold)
        if g.direction not in ("min", "max"):
            raise ValueError("known gate direction")
    for value in metrics.values():
        finite(value)
    return all(g.metric in metrics and
        (metrics[g.metric] >= g.threshold if g.direction == "min"
         else metrics[g.metric] <= g.threshold) for g in gates)


class Registry:
    def __init__(self, gates=None):
        self.gates = tuple(gates) if gates is not None else (
            Gate("quality", "min", .8), Gate("safety", "min", 1.),
            Gate("latency", "max", 10.))
        gates_pass({}, self.gates)
        self.artifacts, self.stages, self.evaluations, self.canaries = {}, {}, {}, {}
        self.active, self.revision, self.history, self.log = None, 0, (), ()
        self.roles = {"search": "proposer", "lab": "evaluator", "release": "promoter"}
        self.suite, self.heldout = "regression-v1", "heldout-v1"

    def _role(self, actor, role):
        if self.roles.get(actor) != role:
            raise PermissionError("wrong governance role")

    def create(self, payload, parent=None, recipe="identity", training_data="train-v1",
               state_fingerprint="state-v1", actor="search"):
        self._role(actor, "proposer")
        if parent is not None and parent not in self.artifacts:
            raise KeyError("registered parent required")
        values = (payload, recipe, training_data, state_fingerprint)
        if any(type(x) is not str or not 1 <= len(x) <= 4096 for x in values):
            raise ValueError("bounded nonempty provenance strings")
        body = (parent, *values)
        aid = hashlib.sha256(json.dumps(body, separators=(",", ":")).encode()).hexdigest()
        if aid in self.artifacts:
            return self.artifacts[aid]  # never reset an existing stage/evaluation
        a = Artifact(aid, parent, *values)
        self.artifacts[aid], self.stages[aid] = a, Stage.CANDIDATE
        self.log += (("create", aid, actor),)
        return a

    def evaluate(self, aid, metrics, data="heldout-v1", suite="regression-v1",
                 budget=100, actor="lab"):
        self._role(actor, "evaluator")
        a = self.artifacts[aid]
        if self.stages[aid] != Stage.CANDIDATE:
            raise RuntimeError("evaluate candidate once; new evidence needs new candidate")
        if (data != self.heldout or data == a.training_data or suite != self.suite or
                type(budget) is not int or budget < 1):
            raise ValueError("approved held-out suite and declared budget")
        passed = gates_pass(metrics, self.gates)
        report = Evaluation(aid, suite, data, actor, budget,
                            tuple(sorted(metrics.items())), passed)
        self.evaluations[aid] = report
        self.stages[aid] = Stage.EVALUATED if passed else Stage.REJECTED
        self.log += (("evaluate", aid, passed),)
        return passed

    def canary(self, aid, fraction, observations, errors, p95_ms, actor="release"):
        self._role(actor, "promoter")
        finite(fraction); finite(p95_ms)
        if self.stages[aid] != Stage.EVALUATED:
            raise RuntimeError("offline gates precede canary")
        if (not 0 < fraction <= .1 or type(observations) is not int or observations < 20
                or type(errors) is not int or not 0 <= errors <= observations or p95_ms < 0):
            raise ValueError("bounded exposure and valid observed counts")
        passed = errors == 0 and p95_ms <= 10
        self.canaries[aid] = (fraction, observations, errors, p95_ms, passed)
        self.stages[aid] = Stage.CANARY if passed else Stage.REJECTED
        self.log += (("canary", aid, passed),)
        return passed

    def _switch(self, target, expected_revision, drain, event):
        if type(expected_revision) is not int or expected_revision != self.revision:
            raise RuntimeError("stale release revision")
        if type(drain) is not bool:
            raise ValueError("explicit boolean drain policy")
        current = self.artifacts.get(self.active)
        changed_state = (current is not None and current.state_fingerprint !=
                         self.artifacts[target].state_fingerprint)
        if changed_state and not drain:
            raise RuntimeError("state incompatible: drain/reset required")
        # All checks completed before serialized pointer/stage mutation.
        if self.active is not None:
            self.stages[self.active] = Stage.RETIRED
        self.active = target
        self.stages[target] = Stage.ACTIVE
        self.revision += 1
        self.history += (target,)
        self.log += ((event, target, self.revision, changed_state),)

    def promote(self, aid, expected_revision, drain=False, actor="release"):
        self._role(actor, "promoter")
        if (self.stages[aid] != Stage.CANARY or
                not self.evaluations[aid].passed or not self.canaries[aid][-1]):
            raise RuntimeError("passed offline and canary evidence required")
        if self.evaluations[aid].evaluator == actor:
            raise PermissionError("evaluator cannot self-promote")
        self._switch(aid, expected_revision, drain, "promote")

    def rollback(self, target, expected_revision, drain=False, actor="release"):
        self._role(actor, "promoter")
        if (target not in self.history or self.stages[target] != Stage.RETIRED or
                not self.evaluations[target].passed):
            raise RuntimeError("rollback only to previously served validated artifact")
        self._switch(target, expected_revision, drain, "rollback")


def ewc_quadratic(new_optimum, old_optimum, curvature, importance, strength):
    """Closed minimizer of a stipulated separable quadratic, not trained EWC."""
    values = (new_optimum, old_optimum, curvature, importance, strength)
    for x in values:
        finite(x)
    if curvature <= 0 or importance < 0 or strength < 0:
        raise ValueError("positive task curvature, nonnegative penalty")
    return ((curvature * new_optimum + strength * importance * old_optimum) /
            (curvature + strength * importance))


def results():
    r = Registry()
    base = r.create("baseline")
    r.evaluate(base.aid, {"quality": .8, "safety": 1, "latency": 9})
    r.canary(base.aid, .05, 20, 0, 9)
    r.promote(base.aid, 0)
    bad = r.create("quality-up-safety-down", base.aid, recipe="rule-change")
    r.evaluate(bad.aid, {"quality": .95, "safety": .5, "latency": 8})
    good = r.create("candidate-v2", base.aid, recipe="compiler-rule-v2",
                    state_fingerprint="state-v2")
    r.evaluate(good.aid, {"quality": .85, "safety": 1, "latency": 8})
    r.canary(good.aid, .05, 20, 0, 8)
    r.promote(good.aid, 1, drain=True)
    r.rollback(base.aid, 2, drain=True)
    return {"lineage": [{"candidate": name, "stage": r.stages[a.aid].value,
                         "served": int(a.aid in r.history)}
                       for name, a in (("base", base), ("unsafe", bad), ("v2", good))],
            "revision": r.revision, "active_restored": r.active == base.aid,
            "quadratic": [{"strength": x, "optimum": ewc_quadratic(2, 0, 1, 3, x)}
                          for x in (0, 1, 3, 10)]}


TABLES = [("lineage", ["Candidate", "Final stage", "Ever served"],
           ["candidate", "stage", "served"], "llr"),
          ("quadratic", ["Penalty strength", "Stipulated optimum"],
           ["strength", "optimum"], "rr")]
PLOTS = []
LISTINGS = ["gates_pass", "Registry.create", "Registry._switch", "Registry.rollback"]
