from pathlib import Path
import importlib.util
import itertools
import json
import torch
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evo21", ROOT / "drafts/ch21/reference.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def parameters():
    w = torch.tensor(
        [[1.0, -1.0], [2.0, 0.0], [3.0, 1.0], [4.0, -2.0]],
        dtype=torch.float64,
    )
    a = torch.tensor([0.5, 0.75], dtype=torch.float64)
    return w, a


def test_generated_results():
    assert m.results() == json.loads(
        (ROOT / "drafts/ch21/results.json").read_text()
    )


@pytest.mark.parametrize("n", range(5))
def test_exhaustive_short_sequences_and_involution(n):
    w, a = parameters()
    complement = str.maketrans("ACGT", "TGCA")
    for bases in itertools.product("ACGT", repeat=n):
        seq = "".join(bases)
        x = m.encode(seq)
        torch.testing.assert_close(
            m.rc(x), m.encode(seq.translate(complement)[::-1])
        )
        torch.testing.assert_close(m.rc(m.rc(x)), x)
        z = m.dual(x, w, a)
        torch.testing.assert_close(
            m.dual(m.rc(x), w, a), m.swap_reverse(z)
        )
        torch.testing.assert_close(m.swap_reverse(m.swap_reverse(z)), z)


@pytest.mark.parametrize("n", [0, 1, 2, 5, 9])
def test_all_three_way_chunk_partitions(n):
    w, a = parameters()
    x = m.encode(("ACGTACGTA")[:n])
    expected = m.dual(x, w, a)
    for i in range(n + 1):
        for j in range(i, n + 1):
            actual = m.chunked_dual([x[:i], x[i:j], x[j:]], w, a)
            torch.testing.assert_close(actual, expected)


def test_closed_form_oracle_and_no_carry_mutation():
    w, a = parameters()
    x = m.encode("ACGA")
    initial = torch.tensor([0.3, -0.2], dtype=x.dtype)
    before = initial.clone()
    y, final = m.causal(x, w, a, initial)
    for t in range(1, len(x) + 1):
        expected = a**t * initial
        for j in range(t):
            expected = expected + a ** (t - 1 - j) * (x[j] @ w)
        torch.testing.assert_close(y[t - 1], expected)
    torch.testing.assert_close(initial, before)
    torch.testing.assert_close(final, y[-1])


def test_head_symmetry_and_palindromic_constraint():
    w, a = parameters()
    x = m.encode("ACGA")
    u = torch.tensor([1.0, 2.0], dtype=x.dtype)
    v = -u / 3
    out = m.strand_head(m.dual(x, w, a), u, v)
    opposite = m.strand_head(m.dual(m.rc(x), w, a), u, v)
    torch.testing.assert_close(opposite, out.flip((0, 1)))
    pal = m.encode("ACGT")
    z = m.dual(pal, w, a)
    torch.testing.assert_close(z, m.swap_reverse(z))
    assert not torch.allclose(
        z[:, :2], z[:, 2:]
    )  # not equal at each position


def test_gradients_and_offline_chunk_parity():
    w, a = parameters()
    w.requires_grad_()
    a.requires_grad_()
    x = m.encode("ACGA").requires_grad_()
    assert torch.autograd.gradcheck(m.dual, (x, w, a))
    z = m.dual(x, w, a)
    g1 = torch.autograd.grad(z.square().sum(), (x, w, a))
    c = m.chunked_dual([x[:1], x[1:3], x[3:]], w, a)
    g2 = torch.autograd.grad(c.square().sum(), (x, w, a))
    for g, h in zip(g1, g2):
        torch.testing.assert_close(g, h)


def test_unshared_weights_and_wrong_chunk_order_are_detected():
    w, a = parameters()
    x = m.encode("ACGTACC")

    def bad(v):
        f, _ = m.causal(v, w, a)
        b, _ = m.causal(m.rc(v), w + 1, a)
        return torch.cat((f, b.flip(0)), dim=1)

    assert not torch.allclose(bad(m.rc(x)), m.swap_reverse(bad(x)))
    chunks = [x[:3], x[3:5], x[5:]]
    wrong = torch.cat([m.rc(c) for c in chunks])
    assert not torch.equal(wrong, m.rc(x))


def test_suffix_dependency_and_causal_prefix_control():
    w, a = parameters()
    x = m.encode("ACGA")
    y = m.encode("ACGT")
    xf, _ = m.causal(x, w, a)
    yf, _ = m.causal(y, w, a)
    torch.testing.assert_close(xf[:3], yf[:3])
    assert not torch.allclose(
        m.dual(x, w, a)[0, 2:], m.dual(y, w, a)[0, 2:]
    )


def test_record_boundaries_are_not_padding():
    w, a = parameters()
    x = m.encode("ACG")
    y = m.encode("TA")
    _, state = m.causal(x, w, a)
    leaked, _ = m.causal(y, w, a, state)
    isolated, _ = m.causal(y, w, a)
    assert not torch.allclose(leaked, isolated)
    # Padding is excluded from the input record before RC, not advanced as bases.
    padded = torch.cat((x, torch.zeros((2, 4), dtype=x.dtype)))
    assert not torch.equal(m.rc(padded)[:3], m.rc(x))


def test_coordinate_interval_and_invalid_inputs():
    for length in range(1, 9):
        for start in range(length):
            for end in range(start + 1, length + 1):
                assert (
                    length - (length - start),
                    length - (length - end),
                ) == (start, end)
    w, a = parameters()
    with pytest.raises(ValueError):
        m.encode("ACNT")
    with pytest.raises(ValueError):
        m.encode("acgt")
    with pytest.raises(ValueError):
        m.rc(torch.ones((3, 5)))
    with pytest.raises(ValueError):
        m.causal(m.encode("A"), w, a + 2)
    with pytest.raises(ValueError):
        m.chunked_dual([], w, a)


def test_symmetrization_is_an_equivariant_projection():
    w, a = parameters()
    x = m.encode("ACGTA")

    def g(v):
        return m.causal(v, w, a)[0]

    def project(f, v):
        return (f(v) + f(m.rc(v)).flip(0)) / 2

    torch.testing.assert_close(project(g, m.rc(x)), project(g, x).flip(0))
    torch.testing.assert_close(
        project(lambda v: project(g, v), x), project(g, x)
    )


def test_transformed_loss_has_identical_parameter_gradients():
    w, a = parameters()
    w.requires_grad_()
    a.requires_grad_()
    x = m.encode("ACGTA")
    target = torch.arange(20, dtype=x.dtype).reshape(5, 4) / 10
    loss = (m.dual(x, w, a) - target).square().sum()
    reverse_loss = (
        (m.dual(m.rc(x), w, a) - m.swap_reverse(target)).square().sum()
    )
    torch.testing.assert_close(loss, reverse_loss)
    for actual, expected in zip(
        torch.autograd.grad(loss, (w, a)),
        torch.autograd.grad(reverse_loss, (w, a)),
    ):
        torch.testing.assert_close(actual, expected)


def test_forward_final_state_cannot_reconstruct_reverse_state():
    # Scalar projected inputs (1, -a) and (0, 0) collide only forward.
    a = 0.5
    first = [1.0, -a]
    second = [0.0, 0.0]

    def reduce(values):
        state = 0.0
        for value in values:
            state = a * state + value
        return state

    assert reduce(first) == reduce(second) == 0
    assert reduce(reversed(first)) == 1 - a**2
    assert reduce(reversed(first)) != reduce(reversed(second))
