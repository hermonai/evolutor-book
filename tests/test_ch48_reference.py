import importlib.util
import itertools
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evod48", ROOT / "drafts/ch48/reference.py")
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def test_rc_known():
    assert r.rc("AACGTN") == "NACGTT"


@pytest.mark.parametrize("n", range(5))
def test_exhaustive_rc_and_symmetry(n):
    for letters in itertools.product("ACGTN", repeat=n):
        s = "".join(letters)
        assert r.rc(r.rc(s)) == s
        if s:
            assert r.invariant_score(s) == r.invariant_score(r.rc(s))


@pytest.mark.parametrize("seq", ["AX", "U", " A", "ac-g", ""])
def test_invalid_dna(seq):
    with pytest.raises(ValueError):
        r.onehot(seq)


def test_unknown_is_masked_not_adenine():
    assert r.onehot("AN") == ([[1, 0, 0, 0], [0, 0, 0, 0]], [True, False])
    assert r.gc("NN") is None
    assert r.gc("NGGAA") == .5


def example(i, start, end, hom="", contig="chr1"):
    return r.Example(i, "assembly-v1", contig, start, end, hom, "A"*(end-start), 0)


def test_transitive_split_closure():
    ex = [example("a", 0, 4), example("b", 3, 7, "h"),
          example("c", 20, 24, "h"), example("d", 24, 28)]
    assert r.components(ex) == (("a", "b", "c"), ("d",))
    tr, te = r.group_split(ex, {"a"})
    assert [x.eid for x in tr] == ["d"]
    assert [x.eid for x in te] == ["a", "b", "c"]


def test_split_rejects_unknown_and_duplicate():
    ex = [example("a", 0, 4)]
    with pytest.raises(ValueError): r.group_split(ex, {"z"})
    with pytest.raises(ValueError): r.components(ex+ex)


def test_metric_hand_calculation():
    assert r.confusion([1, 1, 0, 0], [1, 0, 1, 0]) == (1, 1, 1, 1)
    assert r.mcc([1, 0], [0, 1]) == -1
    assert r.mcc([0, 0], [0, 0]) is None
    assert r.brier([1, 0], [.8, .2]) == pytest.approx(.04)
    assert r.average_precision([1, 0, 1], [.9, .8, .7]) == pytest.approx(5/6)


def test_ties_and_prevalence():
    assert r.average_precision([1, 0, 0, 0], [.5]*4) == .25
    assert r.average_precision([0, 1, 0, 0], [.5]*4) == .25
    assert r.average_precision([0, 0], [.1, .9]) is None


@pytest.mark.parametrize("y,p", [([], []), ([1], []), ([2], [0]), ([1], [float('nan')]), ([0], [2])])
def test_metric_rejects_malformed(y, p):
    with pytest.raises(ValueError): r.brier(y, p)


def test_cluster_bootstrap_independent_oracle():
    # Each sampled cluster is entirely right or entirely wrong, equal sizes.
    import random
    rng = random.Random(7)
    vals = sorted(sum(rng.choice([1, 0]) for _ in range(2))/2 for _ in range(200))
    expected = vals[int(.025*199)], vals[int(.975*199)]
    assert r.cluster_interval([1, 1, 1, 1], [1, 1, 0, 0], ["a", "a", "b", "b"], 200) == expected
    with pytest.raises(ValueError): r.cluster_interval([1], [1], ["a"])


def test_snv_commutes_with_strand_normalization():
    x = "AACGTT"
    a = r.snv(x, 2, "C", "A")
    assert r.rc(a) == r.snv(r.rc(x), len(x)-1-2, "G", "T")
    assert r.invariant_score(a)-r.invariant_score(x) == -1
    with pytest.raises(ValueError): r.snv(x, 2, "G", "A")


def test_actual_hermon_offline_invariant_path():
    import torch
    s = importlib.util.spec_from_file_location("evod48_hermon", ROOT / "drafts/ch23/reference.py")
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    with torch.random.fork_rng():
        torch.manual_seed(48)
        model = m.HermonDNA(max_len=8, d=8, h=2, layers=2).double().eval()
    x = torch.tensor([[0, 0, 1, 2, 3, 3]])
    with torch.no_grad():
        assert torch.allclose(model.offline_rc_symmetric_logits(x), model.offline_rc_symmetric_logits(m.rc_ids(x)), atol=1e-12, rtol=0)


def test_generated_results():
    assert r.results()["delta"] == -1
