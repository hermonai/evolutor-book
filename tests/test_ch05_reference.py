import importlib.util
import sys
from itertools import product
from pathlib import Path
import copy
import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_review_record_binds_complete_authored_source_set():
    import hashlib
    import json

    record = json.loads(
        (ROOT / "artifacts/deep/ch05-review.json").read_text()
    )
    actual = {
        str(p.relative_to(ROOT))
        for p in (ROOT / "drafts/ch05").rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    assert set(record["sources"]) == actual
    for path, digest in record["sources"].items():
        assert (
            hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
        )
    assert record["allPagesInspected"]
    assert record["figures"] == 5 and record["exercises"] == 12
    assert record["status"].endswith("no acceptance promotion")
    assert record["openGates"]
    assert (
        len(json.loads((ROOT / "book/book.json").read_text())["chapters"])
        == 2
    )
    figures = ROOT / "drafts/ch05/figures"
    assert len(list(figures.glob("*.tex"))) == 5
    assert {p.stem for p in figures.glob("*.tex")} == {
        p.stem for p in figures.glob("*.txt")
    }


def test_local_pdf_matches_review_when_available():
    import hashlib
    import json

    record = json.loads(
        (ROOT / "artifacts/deep/ch05-review.json").read_text()
    )
    path = ROOT / record["pdf"]
    if not path.exists():
        pytest.skip("Review PDF is generated and gitignored")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]


spec = importlib.util.spec_from_file_location(
    "evo05", ROOT / "drafts/ch05/reference.py"
)
M = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = M
spec.loader.exec_module(M)


@pytest.mark.parametrize("k", range(1, 5))
def test_base_four_exhaustive_bijection(k):
    words = ["".join(v) for v in product("ACGT", repeat=k)]
    assert [M.encode_kmer(w) for w in words] == list(range(4**k))
    assert [M.decode_kmer(i, k) for i in range(4**k)] == words
    assert M.encode_kmer("ACG") == 6


@pytest.mark.parametrize("mode", ["overlap", "disjoint"])
def test_all_short_strings_roundtrip(mode):
    for n in range(6):
        for v in product("ACGT", repeat=n):
            s = "".join(v)
            for k in (1, 2, 3):
                assert M.reconstruct(M.tokenize(s, k, mode)) == s
                assert M.decode_record(M.encode_record(s, k, mode), k) == s


def test_tail_offsets_and_record_identity():
    r = M.encode_record("ACGTACG", 3)
    assert [t["id"] for t in r["tokens"]] == [29, 72, 5]
    bad = copy.deepcopy(r)
    bad["vocabulary_sha256"] = "wrong"
    with pytest.raises(ValueError):
        M.decode_record(bad, 3)
    bad = copy.deepcopy(r)
    bad["tokens"][0]["id"] = 0
    with pytest.raises(ValueError):
        M.decode_record(bad, 3)


@pytest.mark.parametrize(
    "tokens",
    [
        [M.Token("AC", 0, 2), M.Token("TT", 1, 3)],
        [M.Token("AC", 1, 3)],
        [M.Token("", 0, 0)],
    ],
)
def test_gap_or_inconsistent_overlap_rejected(tokens):
    with pytest.raises(ValueError):
        M.reconstruct(tokens)


def test_overlap_target_reach_and_nonleakage():
    s = "ACGTACG"
    examples = M.safe_next_base_examples(s, 3)
    assert examples == [
        ("ACG", "T", 3),
        ("CGT", "A", 4),
        ("GTA", "C", 5),
        ("TAC", "G", 6),
    ]
    for word, target, position in examples:
        assert word == s[position - 3 : position] and target == s[position]
    assert M.tokenize("ACGAAA", 3)[0] == M.tokenize("ACGTTT", 3)[0]
    assert M.tokenize(s, 3)[0].text[1:] == M.tokenize(s, 3)[1].text[:-1]


def test_reverse_complement_alignment_and_disjoint_counterexample():
    s = "ACGTACG"
    left = [t.text for t in M.tokenize(M.reverse_complement(s), 3)]
    right = [
        M.reverse_complement(t.text) for t in reversed(M.tokenize(s, 3))
    ]
    assert left == right
    assert [
        t.text for t in M.tokenize(M.reverse_complement(s), 3, "disjoint")
    ] != [
        M.reverse_complement(t.text)
        for t in reversed(M.tokenize(s, 3, "disjoint"))
    ]
    assert M.canonicalize("TTT") == ("AAA", True)
    assert M.canonicalize("AAA") == ("AAA", False)


def test_embedding_forward_and_backward_contract():
    r = M.embedding_example()
    assert r["one_hot_matches"]
    assert r["gradient"] == [
        [2.0, 2.0, 2.0],
        [0.0, 0.0, 0.0],
        [1.0, 1.0, 1.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
    ]
    assert r["padding_value"] == [12.0, 13.0, 14.0]


@pytest.mark.parametrize("s", ["N", "AC U", "acg", "A-C", None])
def test_invalid_sequence(s):
    with pytest.raises(ValueError):
        M.tokenize(s, 3)


@pytest.mark.parametrize(
    "value,k", [(-1, 3), (64, 3), (0, 0), (True, 3), (1, 1.5)]
)
def test_invalid_integer_encoding(value, k):
    with pytest.raises(ValueError):
        M.decode_kmer(value, k)


def test_vocabulary_size_and_distinct_specials():
    assert len(M.vocabulary(3)) == 87
    assert len(set(M.vocabulary(3))) == 87
    with pytest.raises(ValueError):
        M.vocabulary(7)


def test_generated_results():
    import json

    assert (
        json.loads((ROOT / "drafts/ch05/results.json").read_text())
        == M.results()
    )


def test_changed_future_changes_target_not_input():
    left = M.safe_next_base_examples("ACGAAA", 3)[0]
    right = M.safe_next_base_examples("ACGTTT", 3)[0]
    assert left[0] == right[0] == "ACG"
    assert left[1] == "A" and right[1] == "T"
    assert left[2] == right[2] == 3


def test_record_rejects_consistent_but_wrong_segmentation():
    record = M.encode_record("ACGTACG", 3, "overlap")
    record["mode"] = "disjoint"
    with pytest.raises(ValueError, match="segmentation"):
        M.decode_record(record, 3)


def test_one_hot_backward_does_not_inherit_padding_rule():
    torch = M.torch
    weight = torch.arange(15, dtype=torch.float64).reshape(5, 3)
    weight = weight.clone().requires_grad_()
    ids = torch.tensor([[0, 2, 0, 4]])
    (M.F.one_hot(ids, 5).to(torch.float64) @ weight).sum().backward()
    assert weight.grad[4].tolist() == [1.0, 1.0, 1.0]
    assert M.embedding_example()["gradient"][4] == [0.0, 0.0, 0.0]


def test_resource_accounting_and_fixed_width_metadata():
    assert M.decode_kmer(1, 1) == "C"
    assert M.decode_kmer(1, 3) == "AAC"
    row = M.results()["vocabulary_rows"][-1]
    assert row["with_tails_and_specials"] == 5463
    assert row["embedding_bytes_d64_float32"] == 1398528
    assert row["disjoint_tokens_1000"] == 167
    assert row["overlap_tokens_1000"] == 995
