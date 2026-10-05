import importlib.util
import math
import torch
import pytest
from pathlib import Path

P = Path(__file__).parents[1] / "drafts/ch23/reference.py"
s = importlib.util.spec_from_file_location("r", P)
r = importlib.util.module_from_spec(s)
s.loader.exec_module(r)


def test_rc_involution():
    x = torch.tensor([[0, 1, 2, 3, 2]])
    assert torch.equal(r.rc_ids(r.rc_ids(x)), x)


def test_attention_matches_independent_oracle():
    torch.manual_seed(1)
    m = r.MHA(16, 4)
    x = torch.randn(2, 5, 16)
    mask = r.causal_mask(5, x.device)
    y, a = m(x, mask)
    yo, ao = r.attention_oracle(m, x, mask)
    assert torch.allclose(y, yo, atol=1e-6) and torch.allclose(a, ao, atol=1e-6)


def test_causal_prefix_invariance():
    torch.manual_seed(2)
    m = r.HermonDNA(max_len=16, d=16, h=4, layers=1)
    a = torch.tensor([[0, 1, 2, 3, 0, 0]])
    b = torch.tensor([[0, 1, 2, 3, 3, 3]])
    assert torch.allclose(
        m.causal_logits(a)[:, :4], m.causal_logits(b)[:, :4], atol=1e-6
    )


def test_offline_rc_symmetric_head():
    torch.manual_seed(2)
    m = r.HermonDNA(max_len=16, d=16, h=4, layers=1)
    x = torch.tensor([[0, 1, 2, 3, 0, 2]])
    assert torch.allclose(
        m.offline_rc_symmetric_logits(x),
        m.offline_rc_symmetric_logits(r.rc_ids(x)),
        atol=1e-6,
    )


def test_future_attention_is_zero():
    torch.manual_seed(3)
    m = r.MHA(16, 4)
    x = torch.randn(1, 6, 16)
    _, a = m(x, r.causal_mask(6, x.device))
    assert torch.equal(a[0, :, 0, 1:], torch.zeros_like(a[0, :, 0, 1:]))


def test_gradients_flow():
    torch.manual_seed(4)
    m = r.HermonDNA(max_len=16, d=16, h=4, layers=1)
    x = torch.tensor([[0, 1, 2, 3]])
    m.causal_logits(x).square().mean().backward()
    assert m.blocks[0].attn.qkv.weight.grad.abs().sum() > 0


@pytest.mark.parametrize("causal", [False, True])
def test_padding_invariance_and_zero_queries(causal):
    torch.manual_seed(40)
    m = r.HermonDNA(max_len=12, d=8, h=2, layers=2).double()
    single = torch.tensor([[0, 1, 2, 3]])
    padded = torch.tensor([[0, 1, 2, 3, 2, 1], [3, 2, 1, 0, 0, 0]])
    valid = torch.tensor([[1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1]], dtype=torch.bool)
    z, att = m.encode(padded, causal, valid)
    assert torch.allclose(z[0, :4], m.encode(single, causal)[0][0], atol=1e-12, rtol=0)
    assert torch.equal(z[~valid], torch.zeros_like(z[~valid]))
    for a in att:
        assert torch.equal(a[0, :, 4:, :], torch.zeros_like(a[0, :, 4:, :]))
        assert torch.equal(
            a[0, :, :, :][:, :, 4:], torch.zeros_like(a[0, :, :, :][:, :, 4:])
        )
    assert torch.allclose(
        m.offline_rc_symmetric_logits(single),
        m.offline_rc_symmetric_logits(padded[:1], valid[:1]),
        atol=1e-12,
        rtol=0,
    )


def test_all_masked_rows_are_finite_and_zero():
    m = r.MHA(8, 2).double()
    x = torch.randn(2, 3, 8, dtype=torch.float64, requires_grad=True)
    mask = torch.ones(2, 3, 3, dtype=torch.bool)
    y, a = m(x, mask)
    yo, ao = r.attention_oracle(m, x, mask)
    assert torch.equal(y, yo) and torch.equal(a, ao)
    assert torch.equal(y, torch.zeros_like(y))
    y.sum().backward()
    assert torch.isfinite(x.grad).all()


def test_attention_value_and_gradient_oracle():
    torch.manual_seed(42)
    m = r.MHA(8, 2).double()
    x = torch.randn(2, 4, 8, dtype=torch.float64, requires_grad=True)
    valid = torch.tensor([[1, 1, 1, 0], [0, 1, 1, 1]], dtype=torch.bool)
    mask = r.legality(valid, True)
    y, a = m(x, mask)
    yo, ao = r.attention_oracle(m, x, mask)
    assert torch.allclose(y, yo, atol=1e-12, rtol=0)
    assert torch.allclose(a, ao, atol=1e-12, rtol=0)
    params = (x, *m.parameters())
    ga = torch.autograd.grad(y.square().sum(), params, retain_graph=True)
    gb = torch.autograd.grad(yo.square().sum(), params)
    for u, v in zip(ga, gb):
        assert torch.allclose(u, v, atol=1e-11, rtol=1e-11)


def test_finite_difference_future_feature_causality():
    torch.manual_seed(43)
    m = r.MHA(8, 2).double()
    x = torch.randn(1, 5, 8, dtype=torch.float64)
    changed = x.clone()
    changed[:, 3:] += 1e-4
    mask = r.causal_mask(5, x.device)
    assert torch.allclose(
        m(x, mask)[0][:, :3], m(changed, mask)[0][:, :3], atol=1e-12, rtol=0
    )
    assert not torch.allclose(m(x)[0][:, :3], m(changed)[0][:, :3], atol=1e-10, rtol=0)


def test_attention_gradcheck():
    torch.manual_seed(44)
    m = r.MHA(4, 2).double()
    x = torch.randn(1, 3, 4, dtype=torch.float64, requires_grad=True)
    assert torch.autograd.gradcheck(lambda z: m(z, r.causal_mask(3, z.device))[0], (x,))


def test_empty_record_and_invalid_contract_rejected():
    m = r.HermonDNA(max_len=4, d=8, h=2, layers=1)
    for x in (
        torch.empty(1, 0, dtype=torch.long),
        torch.tensor([[4]]),
        torch.tensor([[-1]]),
        torch.tensor([[0.0]]),
        torch.zeros(1, 5, dtype=torch.long),
    ):
        with pytest.raises(ValueError):
            m.causal_logits(x)
    x = torch.tensor([[0, 1]])
    invalid = torch.zeros_like(x, dtype=torch.bool)
    assert torch.equal(m.causal_logits(x, invalid), torch.zeros(1, 2, 4))
    with pytest.raises(ValueError):
        m.offline_logits(x, invalid)
    with pytest.raises(ValueError):
        m.encode(x, valid=torch.ones(1, 2))
    with pytest.raises(ValueError):
        r.MHA(7, 2)
    with pytest.raises(ValueError):
        r.HermonDNA(vocab=5)


def test_mask_shape_is_not_silently_broadcast():
    m = r.MHA(8, 2)
    x = torch.randn(2, 4, 8)
    for mask in (
        torch.zeros(4, 4),
        torch.zeros(1, 4, 4, dtype=torch.bool),
        torch.zeros(4, 3, dtype=torch.bool),
    ):
        with pytest.raises(ValueError):
            m(x, mask)


@pytest.mark.parametrize("seed", [13, 17, 19])
def test_motif_oracle_and_palindromic_pattern(seed):
    x, y = r.make_motif(100, 16, seed)
    assert torch.equal(r.motif_oracle(x), y)
    assert torch.equal(r.motif_oracle(r.rc_ids(x)), y)
    assert torch.equal(
        r.rc_ids(torch.tensor([[0, 1, 2, 3]])), torch.tensor([[0, 1, 2, 3]])
    )


def test_assigned_attention_trace_independent_first_two_rows():
    rows = r.assigned_attention()
    assert (rows[0]["a1"], rows[0]["a2"], rows[0]["a3"]) == (1, 0, 0)
    p = 1 / (1 + math.exp(1 / math.sqrt(2)))
    assert rows[1]["a1"] == pytest.approx(p)
    assert rows[1]["o1"] == pytest.approx(p)
    assert rows[1]["o2"] == pytest.approx(2 * (1 - p))


def test_parameter_count_formula():
    d = 12
    layers = 2
    t = 32
    c = 2
    m = r.HermonDNA(max_len=t, d=d, h=3, layers=layers, classes=c)
    expected = (
        (4 + t) * d + layers * (8 * d * d + 11 * d) + 2 * d + 4 * (d + 1) + c * (d + 1)
    )
    assert sum(p.numel() for p in m.parameters()) == expected
