"""Independent graph, paired uncertainty and native-contract tests."""

import importlib.util
import itertools
from pathlib import Path
import statistics

import pytest

p = Path(__file__).parents[1] / "drafts/ch25/reference.py"
spec = importlib.util.spec_from_file_location("evod25", p)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def record(i, sequence, groups=(), label=0):
    return {"id": i, "sequence": sequence, "groups": list(groups), "label": label}


def test_dataset_label_independent_string_search():
    records = r.dataset(100, 24, 25)
    assert all(int("ACGT" in row["sequence"]) == row["label"] for row in records)
    assert records == r.dataset(100, 24, 25)


@pytest.mark.parametrize("args", [(0, 32), (4, 3), (True, 32), (4, 4.0)])
def test_dataset_domain(args):
    with pytest.raises(ValueError):
        r.dataset(*args)


def test_rc_involution_and_palindromic_motif():
    assert r.rc("ACGT") == "ACGT"
    for row in r.dataset(40):
        s = row["sequence"]
        assert r.rc(r.rc(s)) == s
        assert r.motif_oracle(s) == r.motif_oracle(r.rc(s))


def test_transitive_closure_mixed_edge_types():
    records = [
        record("a", "AACG"),
        record("b", "CGTT", ["homology:H"]),
        record("c", "GAAA", ["homology:H"]),
        record("d", "ACAC"),
        record("e", "CCCC"),
    ]
    # a/b are RC; b/c share a declared group; c/d is explicit relation.
    assert r.closure(records, [("c", "d")]) == (("a", "b", "c", "d"), ("e",))


def test_closure_matches_independent_breadth_first_graph():
    records = [
        record("a", "AAAA", ["x"]),
        record("b", "TTTT"),
        record("c", "ACAC", ["x"]),
        record("d", "CCCC"),
        record("e", "ATAT"),
        record("f", "GGGG"),
    ]
    relations = [("c", "e")]
    graph = {x["id"]: set() for x in records}
    for a, b in itertools.combinations(records, 2):
        same = a["sequence"] in (b["sequence"], r.rc(b["sequence"]))
        same |= bool(set(a["groups"]) & set(b["groups"]))
        same |= tuple(sorted((a["id"], b["id"]))) in [
            tuple(sorted(x)) for x in relations
        ]
        if same:
            graph[a["id"]].add(b["id"])
            graph[b["id"]].add(a["id"])
    unseen = set(graph)
    expected = []
    while unseen:
        seed = min(unseen)
        found, stack = set(), [seed]
        while stack:
            node = stack.pop()
            if node not in found:
                found.add(node)
                stack.extend(graph[node])
        unseen -= found
        expected.append(tuple(sorted(found)))
    assert r.closure(records, relations) == tuple(sorted(expected))


def test_split_audit_detects_rc_and_transitive_leak():
    records = [
        record("a", "AACG"),
        record("b", "CGTT"),
        record("c", "CCCC"),
        record("d", "ACAC"),
    ]
    with pytest.raises(ValueError, match="crosses"):
        r.audit_splits(
            records, {"a": "train", "b": "test", "c": "test", "d": "validation"}
        )
    with pytest.raises(ValueError, match="crosses"):
        r.audit_splits(
            records,
            {"a": "train", "b": "train", "c": "test", "d": "validation"},
            [("b", "c")],
        )


def test_partition_nonempty_unique_and_reproducible():
    records = r.dataset(40, 24)
    assignment = r.assign_splits(records)
    assert r.audit_splits(records, assignment)
    assert set(assignment.values()) == {"train", "validation", "test"}
    assert assignment == r.assign_splits(list(reversed(records)))


def test_closure_duplicate_unknown_and_noncanonical_fail():
    for records, relations in [
        ([record("a", "AAAA"), record("a", "CCCC")], []),
        ([record("a", "AAAA")], [("a", "unknown")]),
        ([record("a", "AAAN")], []),
        ([record("a", "AAAA", label=1.0)], []),
    ]:
        with pytest.raises(ValueError):
            r.closure(records, relations)


def test_invalid_split_domain_and_single_component():
    with pytest.raises(ValueError):
        r.assign_splits([record("a", "AAAA"), record("b", "TTTT")])
    for fractions in (
        (0.6, 0.2, 0.3),
        (0, 0.5, 0.5),
        (0.5, 0.5),
        (float("nan"), 0.5, 0.5),
    ):
        with pytest.raises(ValueError):
            r.assign_splits(r.dataset(20), fractions=fractions)


def test_envelope_hash_order_invariant_sensitive_to_semantics():
    records = r.dataset(20)
    assignment = r.assign_splits(records)
    a = r.experiment_hash(records, assignment, "offline")
    assert a == r.experiment_hash(list(reversed(records)), assignment, "offline")
    assert a != r.experiment_hash(records, assignment, "causal")
    changed = [dict(x) for x in records]
    changed[0]["label"] = 1 - changed[0]["label"]
    assert a != r.experiment_hash(changed, assignment, "offline")


def test_train_threshold_includes_all_negative_at_gc_one():
    assert r.fit_threshold([record("a", "CCCC", label=0)]) == 2.0
    assert r.fit_threshold([record("a", "AAAA", label=1)]) == -1.0


def test_threshold_depends_only_on_passed_train():
    train = r.dataset(40)
    threshold = r.fit_threshold(train)
    test = r.dataset(40, seed=999)
    for row in test:
        row["label"] = 1 - row["label"]
    assert r.fit_threshold(train) == threshold


def test_metrics_independent_counts_and_class_imbalance():
    metrics = r.binary_metrics([0, 0, 0, 1], [0, 0, 0, 0])
    assert (metrics["tp"], metrics["tn"], metrics["fp"], metrics["fn"]) == (0, 3, 0, 1)
    assert metrics["accuracy"] == 0.75
    assert metrics["balanced_accuracy"] == 0.5
    assert r.binary_metrics([1, 1], [1, 0])["balanced_accuracy"] is None


@pytest.mark.parametrize(
    "labels,preds", [([], []), ([1], []), ([True], [1]), ([0], [2])]
)
def test_metric_domain(labels, preds):
    with pytest.raises(ValueError):
        r.binary_metrics(labels, preds)


def test_paired_identical_models_exact_zero():
    labels = [0, 1, 0, 1]
    result = r.paired_bootstrap(labels, [1, 1, 0, 0], [1, 1, 0, 0], repetitions=100)
    assert result["observed_delta"] == result["lo95"] == result["hi95"] == 0


def test_paired_variance_matches_independent_expanded_square():
    d = [-1, 0, 1, 1, -1]
    mean = sum(d) / len(d)
    expected = sum((x - mean) ** 2 for x in d) / (len(d) * (len(d) - 1))
    assert r.exact_paired_variance(d) == pytest.approx(expected)


def test_cluster_dependence_counterexample_bounds():
    y = [1] * 32
    a, b = [1] * 16 + [0] * 16, [0] * 16 + [1] * 16
    iid = r.paired_bootstrap(y, a, b, repetitions=2000)
    cluster = r.paired_bootstrap(y, a, b, [i // 8 for i in range(32)], repetitions=2000)
    assert iid["observed_delta"] == cluster["observed_delta"] == 0
    assert cluster["lo95"] == -1 and cluster["hi95"] == 1
    assert iid["lo95"] > -0.6 and iid["hi95"] < 0.6
    exact = sorted(
        statistics.mean(x) for x in itertools.product([-1, -1, 1, 1], repeat=4)
    )
    assert r.quantile(exact, 0.025) == -1 and r.quantile(exact, 0.975) == 1


def test_unequal_clusters_target_record_weighted_estimand():
    y = [1, 1, 1, 1]
    result = r.paired_bootstrap(
        y, [1, 1, 1, 0], [0, 0, 0, 1], ["large"] * 3 + ["small"], repetitions=100
    )
    assert result["observed_delta"] == 0.5  # equal cluster mean would be zero


def test_bootstrap_domain_and_seed_reproducibility():
    y, a, b = [0, 1], [0, 1], [1, 1]
    for clusters, repetitions in [(["one"] * 2, 100), ([0], 100), (None, 0)]:
        with pytest.raises(ValueError):
            r.paired_bootstrap(y, a, b, clusters, repetitions)
    assert r.paired_bootstrap(y, a, b, repetitions=100) == r.paired_bootstrap(
        y, a, b, repetitions=100
    )


def test_native_contracts_and_independent_parameter_arithmetic():
    probe = r.native_probe()
    assert probe["dogma_chunk_feature_error"] == 0
    assert probe["dogma_terminal_state_error"] == 0
    assert probe["hermon_repeated_prefix_error"] < 1e-12
    dogma, hermon = probe["budgets"]
    expected_dogma = (
        4 * 8
        + 2 * (16 * 8 + 8)
        + 2 * (8 * 3 + 3)
        + (8 * 8 + 8)
        + (16 * 8 + 8)
        + (8 * 4 + 4)
    )
    assert dogma["parameters"] == expected_dogma == 602 and hermon["parameters"] == 958
    assert dogma["parameter_bytes"] == expected_dogma * 8
    assert dogma["native_state_bytes"] == 1 * 8 * (1 + 3) * 8
    assert hermon["per_layer_causal_edges"] == 2 * sum(range(1, 9))
