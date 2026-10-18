import importlib.util
from pathlib import Path
import sys
import pytest

spec = importlib.util.spec_from_file_location("evod50", Path(__file__).resolve().parents[1]/"drafts/ch50/reference.py")
r = importlib.util.module_from_spec(spec); sys.modules[spec.name] = r; spec.loader.exec_module(r)


@pytest.mark.parametrize("lam", [0, .5, 1, 4])
@pytest.mark.parametrize("n", [0, 1, 2, 8])
def test_closed_form_independent(lam, n):
    theta, target, anchor, F = (.2, -.4), (1, 0), (.1, .3), (1, 2)
    start = theta
    for _ in range(n): theta = r.step(theta, target, .1, anchor, F, lam)
    assert theta == pytest.approx(r.closed_form(start, target, n, .1, anchor, F, lam))


def test_exact_rational_oracle():
    from fractions import Fraction as F
    x = [F(0), F(0)]
    for _ in range(4): x = [(x[0]+1)/2, x[1]/2]
    assert tuple(x) == (F(15,16), F(0))
    A, theta = r.accuracy_matrix([(1,0),(0,1)])
    assert theta == (15/256, 15/16)
    assert A[0][0] == 1-1/1024


def test_anchor_tradeoff_not_free_gain():
    a = r.results()["adaptation"]
    assert a[1]["forget"] < a[0]["forget"]
    assert a[1]["new"] < a[0]["new"]


def test_zero_importance_and_zero_lambda():
    base = r.step((.2,.3), (1,0))
    assert r.step((.2,.3), (1,0), anchor=(0,0), importance=(1,1), lam=0) == base
    assert r.step((.2,.3), (1,0), anchor=(0,0), importance=(0,0), lam=7) == base


def test_gradient_finite_difference():
    x, target, anchor, f, lam = .2, 1., -.3, 2., .7
    loss = lambda z: .5*(z-target)**2+.5*lam*f*(z-anchor)**2
    h = 1e-6; numerical = (loss(x+h)-loss(x-h))/(2*h)
    actual = (x-r.step((x,), (target,), .1, (anchor,), (f,), lam)[0])/.1
    assert actual == pytest.approx(numerical, abs=1e-8)


def test_forgetting_and_transfer_conventions():
    A = [[.6,.2],[.8,.7]]
    assert r.forgetting(A) == [0,0]
    assert r.backward_transfer(A) == pytest.approx(.2)
    assert r.backward_transfer([[.5]]) is None


def test_replay_mixture_gradient():
    assert r.replay_step((0,0), (0,1), (1,0), .5) == (.25,.25)
    assert r.replay_step((0,0), (0,1), (1,0), 0) == (0,.5)


def test_population_budget_and_ties():
    pop = [(1,0),(0,1)]
    out, used = r.population_step(pop, [(1,0),(0,1)], 4)
    assert out[0] == (1,0) and used == 4
    with pytest.raises(ValueError): r.population_step(pop, [(1,0),(0,1)], 3)


def test_pareto_and_hard_risk():
    C = r.Candidate
    assert r.pareto([C("a",.9,10,0,.1), C("b",.8,5,0,.1), C("c",.8,11,0,.2), C("u",1,1,1,0)], .1) == ("a","b")
    assert r.pareto([C("u",1,1,1,0)], .1) == ()


@pytest.mark.parametrize("args", [((0,), (1,2)), ((float('nan'),), (1,)), ((), ())])
def test_shape_and_finite(args):
    with pytest.raises(ValueError): r.quality(*args)


def test_invalid_importance_and_matrix():
    with pytest.raises(ValueError): r.step((0,), (1,), anchor=(0,), importance=(-1,), lam=1)
    with pytest.raises(ValueError): r.forgetting([[1,0]])
    with pytest.raises(ValueError): r.step((0,), (1,), lr=-1)


def test_one_step_curvature_instability_is_visible():
    # Correct arithmetic can still be a bad optimization configuration.
    assert abs(r.step((1,), (0,), lr=3)[0]) > 1
