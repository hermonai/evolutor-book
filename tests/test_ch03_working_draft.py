"""Prepublication derivative controls, separate from the reviewed manuscript."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import torch
from torch.nn import functional as F
import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_working_artifacts_and_diagram_contract():
    import xml.etree.ElementTree as ET
    build_spec = importlib.util.spec_from_file_location("ch03_draft_builder", ROOT / "drafts/ch03/build_assets.py")
    builder = importlib.util.module_from_spec(build_spec)
    build_spec.loader.exec_module(builder)
    for name, content in builder.outputs().items():
        assert (ROOT / "drafts/ch03" / name).read_text() == content, name
    storyboard = json.loads((ROOT / "drafts/ch03/storyboard.json").read_text())
    assert len(storyboard["figures"]) == 12
    for figure in storyboard["figures"][:4]:
        folder = ROOT / "drafts/ch03/figures"
        svg = ET.fromstring((folder / (figure["id"] + ".svg")).read_text())
        assert svg.attrib["aria-labelledby"] == "title desc"
        assert svg.find("{http://www.w3.org/2000/svg}title").text
        assert svg.find("{http://www.w3.org/2000/svg}desc").text
        assert not svg.findall(".//{http://www.w3.org/2000/svg}image")
        text = (folder / (figure["id"] + ".txt")).read_text()
        assert not set("┌└│─") & set(text)
        for section in ("QUESTION", "OBJECTS", "RELATION / MECHANISM", "INFERENCE", "BOUNDARY", "SOURCE"):
            assert section in text


spec = importlib.util.spec_from_file_location("evo_ch03_draft", ROOT / "drafts/ch03/reference.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def test_manual_autograd_finite_difference_and_gradcheck():
    x, y, p = M.fixture()
    before = [t.clone() for t in p]
    manual = M.manual_gradients(x, y, p)
    assert M.maximum_error(manual, M.autodiff_gradients(x, y, p)) < 1e-12
    assert M.maximum_error(manual, M.finite_difference_gradients(x, y, p)) < 1e-8
    assert torch.autograd.gradcheck(lambda *q: M.objective(x, y, q),
                                   tuple(t.clone().requires_grad_() for t in p))
    assert all(torch.equal(a, b) for a, b in zip(before, p))


def test_zero_fixture_has_hand_computable_output_bias_gradient():
    x, y, p = M.fixture()
    p = tuple(torch.zeros_like(t) for t in p)
    assert float(M.objective(x, y, p)) == pytest.approx(math.log(3))
    gradient = M.manual_gradients(x, torch.zeros_like(y), p)
    for g in gradient[:-1]:
        assert torch.count_nonzero(g) == 0
    assert torch.allclose(gradient[-1], torch.tensor([-2/3, 1/3, 1/3], dtype=torch.float64))


@pytest.mark.parametrize("shape", [(1, 3, 2, 4), (4, 2, 3, 2), (2, 4, 1, 3)])
def test_nonsquare_dimensions(shape):
    batch, dim, hidden, vocab = shape
    def fixed(rows, cols):
        return torch.sin(torch.arange(rows*cols, dtype=torch.float64).reshape(rows, cols) + .3) / 3
    x = fixed(batch, dim)
    y = torch.arange(batch) % vocab
    p = (fixed(dim, hidden), fixed(1, hidden)[0], fixed(hidden, vocab), fixed(1, vocab)[0])
    manual = M.manual_gradients(x, y, p)
    assert M.maximum_error(manual, M.autodiff_gradients(x, y, p)) < 1e-12
    assert M.maximum_error(manual, M.finite_difference_gradients(x, y, p)) < 1e-8


def test_noncontiguous_parameter_views():
    x, y, p = M.fixture()
    u = p[2].T.contiguous().T
    assert not u.is_contiguous()
    p = (p[0], p[1], u, p[3])
    assert M.maximum_error(M.manual_gradients(x, y, p),
                           M.finite_difference_gradients(x, y, p)) < 1e-8


def test_broadcast_bias_gradient_equals_sum_not_mean():
    x, y, p = M.fixture()
    w, b, u, c = p
    hidden = torch.tanh(x @ w + b)
    error = (torch.softmax(hidden @ u + c, 1) - F.one_hot(y, 3)) / len(y)
    da = (error @ u.T) * (1 - hidden.square())
    gradient = M.manual_gradients(x, y, p)[1]
    assert torch.allclose(gradient, da.sum(0), atol=1e-14)
    assert not torch.allclose(gradient, da.mean(0), atol=1e-8)


def test_negative_control_is_actually_detected():
    result = M.detached_negative_control()
    assert result["autograd_derivative"] == 2.
    assert result["finite_difference"] == pytest.approx(4., abs=1e-9)
    assert abs(result["finite_difference"] - result["autograd_derivative"]) > 1.9


@pytest.mark.parametrize("eta,relation", [(0., "equal"), (.1, "decrease"), (.5, "equal"), (.6, "increase")])
def test_quadratic_stability_boundary(eta, relation):
    rows = M.quadratic_trace(4., eta)
    losses = [r["loss"] for r in rows]
    for a, b in zip(losses, losses[1:]):
        assert {"equal": a == b, "decrease": b < a, "increase": b > a}[relation]


def test_stable_loss_large_logits_and_shift_invariance():
    z = torch.tensor([[1000., 1001., 999.], [-1000., -1001., -999.]], dtype=torch.float64)
    y = torch.tensor([1, 2])
    assert not torch.isfinite(z.exp()).all()
    expected = math.log(1 + math.exp(-1) + math.exp(-2))
    assert float(M.stable_nll(z, y)) == pytest.approx(expected, abs=1e-14)
    assert torch.allclose(M.stable_nll(z, y), F.cross_entropy(z, y))
    assert torch.allclose(M.stable_nll(z + 10000, y), M.stable_nll(z, y))


def test_loss_stability_gradient_matches_cross_entropy():
    z = torch.tensor([[3., -1., 2.]], dtype=torch.float64, requires_grad=True)
    y = torch.tensor([2])
    a = torch.autograd.grad(M.stable_nll(z, y), z)[0]
    b = torch.autograd.grad(F.cross_entropy(z, y), z)[0]
    assert torch.allclose(a, b, atol=1e-14)


def test_backward_accumulates_until_cleared():
    x = torch.tensor(2., dtype=torch.float64, requires_grad=True)
    (x*x).backward()
    assert float(x.grad) == 4.
    (x*x).backward()
    assert float(x.grad) == 8.
    x.grad = None
    (x*x).backward()
    assert float(x.grad) == 4.


def test_unequal_microbatches_need_target_weighting():
    x, y, p = M.fixture()
    full = M.manual_gradients(x, y, p)
    first = M.manual_gradients(x[:1], y[:1], p)
    rest = M.manual_gradients(x[1:], y[1:], p)
    weighted = tuple((a + 2*b)/3 for a, b in zip(first, rest))
    wrong = tuple((a+b)/2 for a, b in zip(first, rest))
    assert M.maximum_error(full, weighted) < 1e-14
    assert M.maximum_error(full, wrong) > 1e-3


def test_fixed_toy_update_decreases_this_loss_only():
    x, y, p = M.fixture()
    g = M.manual_gradients(x, y, p)
    updated = tuple(a - .1*b for a, b in zip(p, g))
    assert M.objective(x, y, updated) < M.objective(x, y, p)


@pytest.mark.parametrize("h", [0, -1, float("nan"), float("inf"), 1e-30])
def test_invalid_or_vanishing_perturbations(h):
    with pytest.raises(ValueError):
        M.finite_difference_gradients(*M.fixture(), h=h)


@pytest.mark.parametrize("defect", ["float32", "nan", "shape", "target", "empty"])
def test_tensor_contract_rejects_invalid_inputs(defect):
    x, y, p = M.fixture()
    if defect == "float32": x = x.float()
    if defect == "nan": x[0, 0] = float("nan")
    if defect == "shape": p = (p[0], p[1][:1], *p[2:])
    if defect == "target": y[0] = 3
    if defect == "empty": x, y = x[:0], y[:0]
    with pytest.raises(ValueError): M.objective(x, y, p)


def test_cancellation_fixture():
    assert M.cancellation_example() == {"torch.float32": 0., "torch.float64": 1.}


def test_nonfinite_comparison_cannot_pass():
    with pytest.raises(ValueError):
        M.maximum_error((torch.tensor(float("nan")),), (torch.tensor(0.),))


def test_published_release_is_untouched():
    release = "7dab3ecb7fc0a2cc431ebeb34aa3ce523d21d680"
    review = json.loads((ROOT / "artifacts/deep/ch02-review.json").read_text())
    for path, digest in review["reviewedSources"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    for path in ("artifacts/deep/ch02-review.json", "output/pdf/deep-evolutor-ch01-02.pdf"):
        assert (ROOT / path).read_bytes() == subprocess.check_output(["git", "show", release + ":" + path], cwd=ROOT)
    assert len(json.loads((ROOT / "book/book.json").read_text())["chapters"]) == 2
