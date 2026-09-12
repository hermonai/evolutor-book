"""Executable boundary controls for the Chapter 3 review edition."""
import importlib.util
import math
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("completion", ROOT / "drafts/ch03/completion_diagnostics.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

@pytest.mark.parametrize("args", [(-1,.1), (True,.1), (1,-.1), (1,1.1), (1,float("nan")), (1,float("inf")), (1,.1,-.1), (1,.1,1.,2.)])
def test_coverage_rejects_invalid_inputs(args):
    with pytest.raises(ValueError):
        M.coverage(*args)

def test_coverage_boundaries_and_small_probability():
    assert M.coverage(0,1.) == 0
    assert M.coverage(10,0.) == 0
    assert M.coverage(10,1.) == 1
    assert M.coverage(1,.1,.5,.8) == pytest.approx(.04)
    assert M.coverage(10,.1,.5,.8) == pytest.approx(1-.96**10)
    assert M.coverage(100,1e-20) == pytest.approx(1e-18, rel=1e-12, abs=0)
    values = [M.coverage(m,.1,.5,.8) for m in range(100)]
    assert values == sorted(values)
    assert all(0 <= p <= 1 for p in values)

def test_coverage_independent_two_copy_enumeration():
    q=.04
    events={(False,False):(1-q)**2, (True,False):q*(1-q),
            (False,True):(1-q)*q, (True,True):q*q}
    assert M.coverage(2,.1,.5,.8) == pytest.approx(sum(p for outcome,p in events.items() if any(outcome)))

@pytest.mark.parametrize("args", [(0,1),(1,0),(-1,2),(True,3),(2,1.5)])
def test_work_depth_dimensions(args):
    with pytest.raises(ValueError):
        M.work_depth(*args)

def test_work_depth_contract():
    assert M.work_depth(4,3) == dict(candidates=4,stages=3,work=12,depth=3)

@pytest.mark.parametrize("step", [0,-.1,float("nan"),float("inf")])
def test_state_control_step_validation(step):
    with pytest.raises(ValueError):
        M.state_control(step)

def test_controlled_and_uncontrolled_numerical_derivative():
    assert M.state_control() == pytest.approx(10.,abs=1e-10)
    assert M.state_control(advance_state=True) == pytest.approx(-5489.,abs=1e-8)
    assert abs(M.state_control(.0001,True)) > abs(M.state_control(.001,True))

def test_hard_selector_is_not_a_smooth_surrogate():
    assert M.branch_value(0) == 2
    for h in (.1,.01,.001):
        assert (M.branch_value(h)-M.branch_value(-h))/(2*h) == pytest.approx(3/(2*h))

@pytest.mark.skipif(ROOT.name != "evolutor-book", reason="PyTorch examples belong to Evolutor")
def test_momentum_state_golden_trace_and_reset_counterexample():
    rows=M.momentum_trace()
    for actual, expected in zip(rows, [(1.,1.,1.,.9),(.9,.9,1.8,.72)]):
        assert tuple(actual[k] for k in ("before","gradient","buffer","after")) == pytest.approx(expected)
    reset_after = .9 - .1*.9
    assert reset_after == pytest.approx(.81)
    assert reset_after != pytest.approx(rows[-1]["after"])

@pytest.mark.skipif(ROOT.name != "evolutor-book", reason="PyTorch examples belong to Evolutor")
def test_selected_parameter_gradient_does_not_differentiate_the_selector():
    import torch
    r=torch.tensor(.2,dtype=torch.float64,requires_grad=True)
    a=torch.tensor(2.,dtype=torch.float64,requires_grad=True)
    b=torch.tensor(-1.,dtype=torch.float64,requires_grad=True)
    output=torch.where(r>=0,a,b)
    grad_r,grad_a,grad_b=torch.autograd.grad(output,(r,a,b),allow_unused=True)
    assert grad_r is None
    assert grad_a.item() == 1
    assert grad_b.item() == 0

def test_review_record_binds_the_reviewed_sources():
    import hashlib
    import json
    record=json.loads((ROOT/"artifacts/deep/ch03-review.json").read_text())
    assert record["edition"] == "standalone review candidate; not cumulative acceptance"
    assert record["allPagesInspected"]
    assert record["figures"] == 12
    assert record["openGates"]
    for path,digest in record["sources"].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, path

def test_local_review_pdf_matches_record_when_available():
    import hashlib
    import json
    record=json.loads((ROOT/"artifacts/deep/ch03-review.json").read_text())
    path=ROOT/record["pdf"]
    if not path.exists():
        pytest.skip("Local review PDF is a generated, gitignored artifact")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
