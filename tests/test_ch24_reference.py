import importlib.util
import sys
from pathlib import Path
import math
import pytest
import torch

spec = importlib.util.spec_from_file_location(
    "evo24", Path(__file__).parents[1] / "drafts/ch24/reference.py"
)
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def test_span_coordinates_mutation_and_reverse_action():
    spans = r.tokenize("ACGTAC", 3)
    assert [(s.token, s.start, s.end) for s in spans] == [
        ("ACG", 0, 3),
        ("CGT", 1, 4),
        ("GTA", 2, 5),
        ("TAC", 3, 6),
    ]
    assert r.mutation_footprint(spans, 2) == [0, 1, 2]
    assert list(reversed([r.reverse_span(s, 6) for s in spans])) == r.tokenize(
        r.rc("ACGTAC"), 3
    )
    assert r.reverse_span(r.reverse_span(spans[0], 6), 6) == spans[0]


def test_stride_tail_breaks_rc_tokenizer_commutation():
    sequence = "ACGTA"
    spans = r.tokenize(sequence, 2, 2)
    assert list(reversed([r.reverse_span(s, 5) for s in spans])) != r.tokenize(
        r.rc(sequence), 2, 2
    )


def test_base_causality_is_stronger_than_token_triangle():
    spans = r.tokenize("ACGTAC", 3)
    # First input token ACG already contains target base G at index two.
    assert r.causal_span_leaks(spans[:1], 2) == [0]
    assert r.causal_span_leaks(spans[:1], 3) == []
    assert r.mutation_footprint(spans, 0) == [0]


@pytest.mark.parametrize("orientation", [-1, 1])
def test_tied_strand_even_odd_joint_equivariance(orientation):
    torch.manual_seed(24)
    model = r.StrandEmbedding(4).double()
    ids = torch.tensor([[0, 1, 1, 2, 3], [3, 2, 1, 0, 0]], dtype=torch.long)
    signs = torch.full((2,), float(orientation), dtype=torch.float64)
    result = model(r.rc_ids(ids), -signs)
    torch.testing.assert_close(
        result, r.rc_feature_action(model(ids, signs)), rtol=0, atol=0
    )


def test_orientation_must_flip_with_record():
    torch.manual_seed(24)
    model = r.StrandEmbedding(4).double()
    ids = torch.tensor([[0, 1, 2]], dtype=torch.long)
    signs = torch.ones(1, dtype=torch.float64)
    correct = r.rc_feature_action(model(ids, signs))
    assert not torch.allclose(model(r.rc_ids(ids), signs), correct)


def test_strand_embedding_parameter_gradients_and_batch_isolation():
    model = r.StrandEmbedding(3).double()
    ids = torch.tensor([[0, 1, 2, 3], [3, 2, 1, 0]], dtype=torch.long)
    signs = torch.tensor([1.0, -1.0], dtype=torch.float64)
    output = model(ids, signs)
    output[0].square().sum().backward()
    assert all(
        p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters()
    )
    torch.testing.assert_close(output[:1], model(ids[:1], signs[:1]))


def test_rotary_independent_matrix_oracle_norm_and_shift():
    generator = torch.Generator().manual_seed(24)
    q, k = [
        torch.randn(2, 3, 5, 6, generator=generator, dtype=torch.float64)
        for _ in range(2)
    ]
    positions = torch.arange(5, dtype=torch.float64)
    frequencies = torch.tensor([1.0, 0.01, 0.0001], dtype=torch.float64)
    rq, rk = [r.rotary(x, positions, frequencies) for x in (q, k)]
    torch.testing.assert_close(rq, r.rotary_matrix_oracle(q, positions, frequencies))
    torch.testing.assert_close(rq.norm(dim=-1), q.norm(dim=-1))
    sq, sk = [r.rotary(x, positions + 100, frequencies) for x in (q, k)]
    torch.testing.assert_close(
        rq @ rk.transpose(-2, -1), sq @ sk.transpose(-2, -1), rtol=1e-12, atol=1e-12
    )


def test_rotary_gradcheck():
    q = torch.randn(1, 1, 3, 4, dtype=torch.float64, requires_grad=True)
    positions = torch.arange(3, dtype=torch.float64)
    frequencies = torch.tensor([1.0, 0.01], dtype=torch.float64)
    assert torch.autograd.gradcheck(lambda x: r.rotary(x, positions, frequencies), (q,))


def test_rotary_assigned_two_dimensional_trace():
    q = torch.tensor([[[[1.0, 0.0], [1.0, 0.0]]]], dtype=torch.float64)
    result = r.rotary(
        q,
        torch.tensor([0.0, 2.0], dtype=torch.float64),
        torch.tensor([math.pi / 4], dtype=torch.float64),
    )
    torch.testing.assert_close(
        result[0, 0, 0], torch.tensor([1.0, 0.0], dtype=torch.float64)
    )
    assert result[0, 0, 0] @ result[0, 0, 1] == pytest.approx(0, abs=1e-15)


@pytest.mark.parametrize("causal", [False, True])
def test_edge_legality_independent_nested_loop(causal):
    valid = [True, True, False, True, True, True]
    edges = r.edge_lists(6, 1, causal, globals_=(0, 5), valid=valid)
    expected = [
        [
            j
            for j in range(6)
            if valid[i]
            and valid[j]
            and (abs(i - j) <= 1 or i in (0, 5) or j in (0, 5))
            and (not causal or j <= i)
        ]
        for i in range(6)
    ]
    assert edges == expected


@pytest.mark.parametrize("causal", [False, True])
def test_sparse_dense_value_and_all_qkv_gradients(causal):
    generator = torch.Generator().manual_seed(240)
    values = [
        torch.randn(6, 4, generator=generator, dtype=torch.float64, requires_grad=True)
        for _ in range(3)
    ]
    edges = r.edge_lists(
        6, 1, causal, globals_=(0,), valid=[True, True, False, True, True, True]
    )
    a = r.sparse_attention(*values, edges)
    b = r.dense_attention_oracle(*values, edges)
    torch.testing.assert_close(a, b, rtol=1e-12, atol=1e-12)
    weight = torch.arange(24, dtype=torch.float64).reshape(6, 4) / 24
    ga = torch.autograd.grad((a * weight).sum(), values, retain_graph=True)
    gb = torch.autograd.grad((b * weight).sum(), values)
    for x, y in zip(ga, gb):
        torch.testing.assert_close(x, y, rtol=1e-11, atol=1e-12)
    assert torch.equal(a[2], torch.zeros(4, dtype=torch.float64))


def test_sparse_attention_gradcheck():
    values = tuple(
        torch.randn(3, 2, dtype=torch.float64, requires_grad=True) for _ in range(3)
    )
    edges = r.edge_lists(3, 1, True)
    assert torch.autograd.gradcheck(lambda *x: r.sparse_attention(*x, edges), values)


def test_causal_suffix_finite_intervention_despite_globals():
    generator = torch.Generator().manual_seed(24)
    q, k, v = [
        torch.randn(8, 4, generator=generator, dtype=torch.float64) for _ in range(3)
    ]
    edges = r.edge_lists(8, 1, True, globals_=(0, 7))
    output = r.sparse_attention(q, k, v, edges)
    q2, k2, v2 = [x.clone() for x in (q, k, v)]
    for x in (q2, k2, v2):
        x[4:] += 100
    torch.testing.assert_close(
        output[:4], r.sparse_attention(q2, k2, v2, edges)[:4], rtol=0, atol=0
    )
    offline = r.edge_lists(8, 1, False, globals_=(0, 7))
    assert not torch.allclose(
        r.sparse_attention(q, k, v, offline)[:4],
        r.sparse_attention(q2, k2, v2, offline)[:4],
    )


def test_global_relay_needs_two_layers():
    local = r.edge_lists(12, 1)
    global_graph = r.edge_lists(12, 1, globals_=(0,))
    assert r.reachable_sources(local, 1, 2) == [0, 1, 2, 3]
    assert 11 not in r.reachable_sources(global_graph, 1, 1)
    assert r.reachable_sources(global_graph, 1, 2) == list(range(12))
    assert r.reachable_sources(global_graph, 1, 0) == [1]
    causal = r.edge_lists(12, 1, True, globals_=(0,))
    assert r.reachable_sources(causal, 1, 20) == [0, 1]


def test_sparse_edge_count_bound_not_actual_speedup():
    length, radius, g = 1024, 4, 2
    edges = r.edge_lists(length, radius, globals_=(0, length - 1))
    assert sum(map(len, edges)) <= length * (2 * radius + 1 + 2 * g)
    assert sum(map(len, edges)) < length * length / 50


@pytest.mark.parametrize(
    "sequence,k,stride",
    [("ACGN", 1, 1), ("", 1, 1), ("ACGT", 0, 1), ("ACGT", 2, 0), ("ACGT", 5, 1)],
)
def test_invalid_token_contract(sequence, k, stride):
    with pytest.raises(ValueError):
        r.tokenize(sequence, k, stride)


def test_invalid_tensor_and_edge_contracts():
    with pytest.raises(ValueError):
        r.rc_ids(torch.tensor([[4]]))
    with pytest.raises(ValueError):
        r.edge_lists(3, 1, globals_=(3,))
    with pytest.raises(ValueError):
        r.edge_lists(3, 1, valid=[True, 1, True])
    with pytest.raises(ValueError):
        r.rotary(torch.ones(1, 1, 2, 3), torch.arange(2.0), torch.ones(1))
    with pytest.raises(ValueError):
        r.rotary(torch.ones(1, 1, 0, 2), torch.empty(0), torch.ones(1))
    values = [torch.ones(3, 2, dtype=torch.float64) for _ in range(3)]
    with pytest.raises(ValueError):
        r.sparse_attention(*values, [[0, 0], [1], [2]])
