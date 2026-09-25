from pathlib import Path
import importlib.util
import json
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evolutor_book_ch18", ROOT / "drafts/ch18/reference.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_results_are_reproducible():
    assert m.results() == json.loads(
        (ROOT / "drafts/ch18/results.json").read_text()
    )


from itertools import product
from collections import Counter


@pytest.mark.parametrize("length", range(6))
def test_counts_rc_and_involution_exhaustive(length):
    for letters in product("ACGT", repeat=length):
        seq = "".join(letters)
        state, _ = m.scan(seq)
        expected = Counter(
            seq[i : i + 2] for i in range(max(0, length - 1))
        )
        assert state.memory == tuple(expected[p] for p in m.PAIRS)
        rc = m.reverse_complement(seq)
        assert m.reverse_complement(rc) == seq
        assert m.scan(rc)[0].memory == m.permute_pairs(state.memory)
        assert (
            m.permute_pairs(m.permute_pairs(state.memory)) == state.memory
        )


@pytest.mark.parametrize("retention", [0, 0.5, 0.9, 1])
def test_chunk_trace_and_mass(retention):
    seq = "ACGACTT"
    full, events = m.scan(seq, retention=retention)
    for k in range(len(seq) + 1):
        first, a = m.scan(seq[:k], retention=retention)
        final, b = m.scan(seq[k:], first, retention)
        assert final == full and a + b == events
    mass = sum(retention**j for j in range(len(seq) - 1))
    assert sum(full.memory) == pytest.approx(mass)


def test_padding_reset_and_no_mutation():
    initial = m.State()
    padded, events = m.scan("ANCG", mask=(True, False, True, True))
    assert padded == m.scan("ACG")[0] and len(events) == 3
    assert initial == m.State()
    assert m.step(padded, "N", valid=False) == (padded, None)
    assert sum(m.scan("G", m.State())[0].memory) == 0
    assert sum(m.scan("G", m.scan("AC")[0])[0].memory) == 2
    with pytest.raises(ValueError):
        m.scan("AN")
    assert initial == m.State()


def test_decay_breaks_one_pass_symmetry_but_two_pass_restores_it():
    s = "AAC"
    h = m.scan(s, retention=0.5)[0].memory
    rh = m.scan(m.reverse_complement(s), retention=0.5)[0].memory
    assert rh != m.permute_pairs(h)
    for retention in (0, 0.5, 0.9, 1):
        z = m.bidirectional(s, retention)
        rz = m.bidirectional(m.reverse_complement(s), retention)
        assert rz == pytest.approx(m.permute_pairs(z))


def test_invalid_state_mask_and_parameters():
    for bad in (
        m.State((0.0,)),
        m.State(previous="A"),
        m.State(position=-1),
    ):
        with pytest.raises(ValueError):
            m.step(bad, "A")
    with pytest.raises(ValueError):
        m.scan("AC", mask=(True,))
    with pytest.raises(ValueError):
        m.scan("A", mask=(1,))
    with pytest.raises(ValueError):
        m.scan("", retention=2)
    with pytest.raises(ValueError):
        m.reverse_complement("N")


def test_distinct_sequences_can_have_identical_complete_state():
    a, trace_a = m.scan("AACA")
    b, trace_b = m.scan("ACAA")
    assert a == b
    assert trace_a != trace_b
    assert a.position == 4 and a.previous == "A"
    assert {p for p, v in zip(m.PAIRS, a.memory) if v} == {"AA", "AC", "CA"}
