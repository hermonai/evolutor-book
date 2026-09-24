from pathlib import Path
import importlib.util
import sys
import json
import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ch12_reference_tests", ROOT / "drafts/ch12/reference.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


torch.set_num_threads(1)


def test_parallel_rewrite_and_preallocation_budget():
    assert m.rewrite("S", {"S": "SG", "G": "GG"}, 3) == [
        "S",
        "SG",
        "SGGG",
        "SGGGGGGG",
    ]
    with pytest.raises(ValueError):
        m.rewrite("S", {"S": "SG", "G": "GG"}, 3, limit=7)
    with pytest.raises(ValueError):
        m.rewrite("X", {"S": "SG"}, 1)


@pytest.mark.parametrize("depth", range(4))
@pytest.mark.parametrize("shared", [True, False])
def test_compiler_forward_and_all_gradients_match_tree(depth, shared):
    nodes, out = m.compile_program(depth, 2, shared)
    bank = m.parameter_bank(nodes, 2)
    x = torch.tensor(
        [[0.4, -0.2], [0.1, 0.3]], dtype=torch.float64, requires_grad=True
    )
    y = m.execute(nodes, out, x, bank)
    oracle = m.recursive_oracle(depth, x, bank, shared)
    torch.testing.assert_close(y, oracle)
    args = [x] + [t for pair in bank.values() for t in pair]
    a = torch.autograd.grad(y.square().sum(), args, retain_graph=True)
    b = torch.autograd.grad(oracle.square().sum(), args)
    for aa, bb in zip(a, b):
        torch.testing.assert_close(aa, bb)
    assert len(nodes) == 2 ** (depth + 1) - 1
    assert len(bank) == (1 if shared else 2**depth)


def test_shared_gradient_is_sum_of_tied_occurrence_gradients():
    ns, os = m.compile_program(2, 2, True)
    ni, oi = m.compile_program(2, 2, False)
    shared = m.parameter_bank(ns, 2)
    w, b = shared["shared"]
    independent = {
        key: (
            w.detach().clone().requires_grad_(),
            b.detach().clone().requires_grad_(),
        )
        for key in m.validate(ni, 2)
    }
    x = torch.tensor([[0.4, -0.2]], dtype=torch.float64)
    ys = m.execute(ns, os, x, shared)
    yi = m.execute(ni, oi, x, independent)
    torch.testing.assert_close(ys, yi)
    gs = torch.autograd.grad(ys.sum(), [w, b])
    gi = torch.autograd.grad(
        yi.sum(), [v for pair in independent.values() for v in pair]
    )
    torch.testing.assert_close(gs[0], sum(gi[::2]))
    torch.testing.assert_close(gs[1], sum(gi[1::2]))
    assert not torch.allclose(
        gs[0], gi[0]
    )  # catching overwrite, not accumulation


def test_autograd_finite_difference_check():
    nodes, out = m.compile_program(1, 2)
    bank = m.parameter_bank(nodes, 2)
    x = torch.tensor([[0.2, -0.1]], dtype=torch.float64, requires_grad=True)
    w, b = bank["shared"]
    assert torch.autograd.gradcheck(
        lambda a, c, d: m.execute(nodes, out, a, {"shared": (c, d)}),
        (x, w, b),
    )


@pytest.mark.parametrize(
    "nodes",
    [
        [m.Node(1, "add", (0, 1), 2)],
        [m.Node(1, "affine", (0,), 3, "p")],
        [m.Node(1, "add", (0,), 2)],
        [m.Node(1, "unknown", (0,), 2)],
        [m.Node(1, "affine", (0,), 2, "")],
        [m.Node(1, "add", (0, 0), 2), m.Node(1, "add", (0, 0), 2)],
    ],
)
def test_type_and_order_rejections(nodes):
    with pytest.raises(ValueError):
        m.validate(nodes, 2)


def test_compile_budget_rejects_before_large_expansion():
    with pytest.raises(ValueError):
        m.compile_program(10, 4, budget=1023)
    with pytest.raises(ValueError):
        m.compile_program(-1, 4)


def test_parameter_shape_mismatch_is_not_silently_broadcast():
    nodes, out = m.compile_program(0, 2)
    with pytest.raises(ValueError):
        m.execute(
            nodes,
            out,
            torch.ones(1, 2),
            {"shared": (torch.ones(2, 2), torch.ones(1))},
        )


def test_execution_order_matters_with_distinct_owners():
    nodes, out = m.compile_program(1, 1, False)
    x = torch.tensor([[0.4]], dtype=torch.float64)
    bank = {
        "rootL": (
            torch.tensor([[0.2]], dtype=torch.float64),
            torch.tensor([0.1], dtype=torch.float64),
        ),
        "rootR": (
            torch.tensor([[0.8]], dtype=torch.float64),
            torch.tensor([-0.3], dtype=torch.float64),
        ),
    }
    swapped = {"rootL": bank["rootR"], "rootR": bank["rootL"]}
    assert not torch.allclose(
        m.execute(nodes, out, x, bank), m.execute(nodes, out, x, swapped)
    )


def test_costs_and_generated_results():
    assert m.costs(6, 4, True)["parameters"] == 20
    assert m.costs(6, 4, False)["parameters"] == 1280
    assert m.costs(6, 4, True)["matrix_macs_per_row"] == 1024
    assert m.results() == json.loads(
        (ROOT / "drafts/ch12/results.json").read_text()
    )
