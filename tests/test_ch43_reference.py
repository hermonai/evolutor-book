import importlib.util
from pathlib import Path
import sys
from dataclasses import FrozenInstanceError
import math
import pytest

spec = importlib.util.spec_from_file_location("evod43_test", Path(__file__).parents[1] / "drafts/ch43/reference.py")
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
GOOD = {"quality": .85, "safety": 1., "latency": 8.}


def serve(reg, payload, parent=None, fingerprint="state-v1"):
    a = reg.create(payload, parent, state_fingerprint=fingerprint)
    assert reg.evaluate(a.aid, GOOD)
    assert reg.canary(a.aid, .05, 20, 0, 8)
    reg.promote(a.aid, reg.revision, drain=True)
    return a


def test_immutable_lineage_dedup_does_not_reset_stage():
    reg = r.Registry(); a = serve(reg, "v1")
    assert reg.create("v1") == a and reg.stages[a.aid] == r.Stage.ACTIVE
    with pytest.raises(FrozenInstanceError):
        a.payload = "changed"
    b = reg.create("v2", a.aid, recipe="structural-rule-v2")
    assert b.parent == a.aid and b.aid != a.aid
    with pytest.raises(KeyError):
        reg.create("v3", "missing")


@pytest.mark.parametrize("metrics", [
    {"quality": .99, "safety": .5, "latency": 1},
    {"quality": .7, "safety": 1, "latency": 1},
    {"quality": .99, "safety": 1, "latency": 11},
    {"quality": .99, "latency": 1}])
def test_all_gates_conjunctive(metrics):
    reg = r.Registry(); a = reg.create("bad")
    assert not reg.evaluate(a.aid, metrics)
    with pytest.raises(RuntimeError):
        reg.canary(a.aid, .01, 20, 0, 8)
    with pytest.raises(RuntimeError):
        reg.rollback(a.aid, 0)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), True])
def test_metrics_fail_closed_without_stage_change(bad):
    reg = r.Registry(); a = reg.create("bad")
    with pytest.raises(ValueError):
        reg.evaluate(a.aid, dict(GOOD, quality=bad))
    assert reg.stages[a.aid] == r.Stage.CANDIDATE


def test_training_or_unknown_evaluation_data_rejected():
    reg = r.Registry(); a = reg.create("x", training_data="heldout-v1")
    with pytest.raises(ValueError):
        reg.evaluate(a.aid, GOOD)
    a = reg.create("y")
    for kw in ({"data": "train-v1"}, {"suite": "new-unreviewed"}, {"budget": 0}):
        with pytest.raises(ValueError):
            reg.evaluate(a.aid, GOOD, **kw)


@pytest.mark.parametrize("method", ["create", "evaluate", "canary", "promote", "rollback"])
def test_authority_separation(method):
    reg = r.Registry(); a = reg.create("x")
    args = {"create": ("x",), "evaluate": (a.aid, GOOD),
            "canary": (a.aid, .01, 20, 0, 8), "promote": (a.aid, 0), "rollback": (a.aid, 0)}
    actor = "lab" if method in ("create", "promote", "rollback", "canary") else "release"
    with pytest.raises(PermissionError):
        getattr(reg, method)(*args[method], actor=actor)


def test_missing_canary_and_cas_release_race():
    reg = r.Registry(); a = reg.create("x"); reg.evaluate(a.aid, GOOD)
    with pytest.raises(RuntimeError):
        reg.promote(a.aid, 0)
    reg.canary(a.aid, .05, 20, 0, 8)
    reg.promote(a.aid, 0)
    b = reg.create("y", a.aid); reg.evaluate(b.aid, GOOD); reg.canary(b.aid, .05, 20, 0, 8)
    before = (reg.active, reg.revision, dict(reg.stages), reg.log)
    with pytest.raises(RuntimeError):
        reg.promote(b.aid, 0)
    assert (reg.active, reg.revision, reg.stages, reg.log) == before


def test_incompatible_promotion_and_rollback_require_reset():
    reg = r.Registry(); a = serve(reg, "v1")
    b = reg.create("v2", a.aid, state_fingerprint="state-v2")
    reg.evaluate(b.aid, GOOD); reg.canary(b.aid, .05, 20, 0, 8)
    with pytest.raises(RuntimeError):
        reg.promote(b.aid, 1)
    reg.promote(b.aid, 1, drain=True)
    with pytest.raises(RuntimeError):
        reg.rollback(a.aid, 2)
    reg.rollback(a.aid, 2, drain=True)
    assert reg.active == a.aid and reg.revision == 3 and reg.log[-1][-1] is True


def test_rollback_never_served_and_current_rejected():
    reg = r.Registry(); base = serve(reg, "v1")
    for stage in (r.Stage.CANDIDATE, r.Stage.EVALUATED, r.Stage.CANARY, r.Stage.REJECTED):
        a = reg.create(stage.value, base.aid)
        reg.stages[a.aid] = stage  # adversarial trusted-state test
        with pytest.raises(RuntimeError):
            reg.rollback(a.aid, 1)
    with pytest.raises(RuntimeError):
        reg.rollback(base.aid, 1)


@pytest.mark.parametrize("errors,p95", [(1, 8), (0, 11)])
def test_canary_failure_does_not_serve(errors, p95):
    reg = r.Registry(); a = reg.create("x"); reg.evaluate(a.aid, GOOD)
    assert not reg.canary(a.aid, .05, 20, errors, p95)
    assert reg.active is None and reg.stages[a.aid] == r.Stage.REJECTED


@pytest.mark.parametrize("fraction,n", [(0, 20), (.11, 20), (.05, 19)])
def test_canary_exposure_bounds(fraction, n):
    reg = r.Registry(); a = reg.create("x"); reg.evaluate(a.aid, GOOD)
    with pytest.raises(ValueError):
        reg.canary(a.aid, fraction, n, 0, 8)


def test_no_stage_reentry_or_empty_gates():
    with pytest.raises(ValueError):
        r.Registry(gates=())
    reg = r.Registry(); a = serve(reg, "x")
    with pytest.raises(RuntimeError):
        reg.evaluate(a.aid, GOOD)


@pytest.mark.parametrize("strength", [0, .1, 1, 10, 100])
def test_ewc_assigned_quadratic_independent_derivative(strength):
    theta = r.ewc_quadratic(2, 0, 1, 3, strength)
    assert theta == pytest.approx(2 / (1 + 3*strength))
    def objective(t):
        return .5*(t-2)**2 + .5*strength*3*t*t
    eps = 1e-5
    derivative = (objective(theta+eps)-objective(theta-eps))/(2*eps)
    assert abs(derivative) < 1e-7
    assert objective(theta) <= min(objective(0), objective(2)) + 1e-12
