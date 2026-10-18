import importlib.util
from pathlib import Path
from dataclasses import replace
import sys
import pytest

s = importlib.util.spec_from_file_location("evod51", Path(__file__).resolve().parents[1]/"drafts/ch51/reference.py")
r = importlib.util.module_from_spec(s); sys.modules[s.name] = r; s.loader.exec_module(r)


def claim():
    return r.Claim("retrieval", "tested", "synthetic held-out records", "lower CI <= 0", "a"*64, "b"*64)


def evidence(eid="E1", evaluator="team-a", independent=False):
    return r.Evidence(eid, "retrieval", "suite-v1", "a"*64, "d"*64, "fixed baseline", "100 actions", "task family", .1, 0., True, "success", evaluator, independent)


def test_implemented_requires_content_identity():
    c = r.Claim("x", "implemented", "scope", "falsifier")
    assert not r.valid(c)
    assert r.valid(replace(c, implementation_digest="a"*64))


def test_local_tests_need_artifact():
    assert r.valid(claim())
    assert not r.valid(replace(claim(), tests_digest=""))


def test_no_skip_and_no_empty_contract():
    with pytest.raises(ValueError): r.promote(replace(claim(), level="implemented"), "benchmark-demonstrated")
    with pytest.raises(ValueError): r.promote(claim(), "benchmark-demonstrated")


def test_benchmark_promotion():
    e = evidence(); c = r.promote(claim(), "benchmark-demonstrated", [e], evidence=("E1",))
    assert r.valid(c, [e])


@pytest.mark.parametrize("changes", [{"held_out": False}, {"outcome": "failure"}, {"lower_bound": 0},
    {"lower_bound": float('nan')}, {"budget": ""}, {"data_digest": "fake"}, {"capability": "other"}])
def test_negative_evidence(changes):
    assert not r.supports(replace(evidence(), **changes), "retrieval")


def test_replication_requires_distinct_identity_and_declaration():
    e = evidence(); c = r.promote(claim(), "benchmark-demonstrated", [e], evidence=("E1",))
    with pytest.raises(ValueError): r.promote(c, "replicated", [e])
    b = evidence("E2", "team-a", True)
    with pytest.raises(ValueError): r.promote(c, "replicated", [e,b], evidence=("E1","E2"))
    b = evidence("E2", "team-b", True)
    assert r.valid(r.promote(c, "replicated", [e,b], evidence=("E1","E2")), [e,b])


def test_replication_contract_must_match():
    e, b = evidence(), replace(evidence("E2", "team-b", True), budget="200 actions")
    c = replace(claim(), level="replicated", evidence=("E1","E2"))
    assert not r.valid(c, [e,b])


def test_evidence_for_changed_artifact_does_not_support_old_claim():
    e = replace(evidence(),artifact_digest="f"*64)
    assert not r.valid(replace(claim(),level="benchmark-demonstrated",evidence=("E1",)),[e])


def test_scope_change_is_new_claim():
    with pytest.raises(ValueError): r.promote(claim(), "benchmark-demonstrated", scope="all reasoning")


def test_duplicate_records_and_claims_fail_loudly():
    assert not r.valid(claim(), [evidence(), evidence()])
    with pytest.raises(ValueError): r.scorecard([claim(),claim()])
    with pytest.raises(ValueError): r.scorecard([replace(claim(), level="magic")])


def test_area_hand_and_scaling_oracle():
    assert r.acquisition_area([0,1,2], [0,.8,1]) == pytest.approx(.65)
    assert r.acquisition_area([0,10,20], [0,.8,1]) == pytest.approx(.65)
    assert r.acquisition_area([0,1,2], [0,.2,1]) == pytest.approx(.35)


@pytest.mark.parametrize("x,y", [([1,2],[0,1]), ([0,0],[0,1]), ([0,1],[0,2]), ([0,1],[0])])
def test_invalid_curve(x,y):
    with pytest.raises(ValueError): r.acquisition_area(x,y)


def test_binomial_zero_failure_oracle():
    p = r.zero_failure_upper(100)
    assert (1-p)**100 == pytest.approx(.05)
    assert r.zero_failure_upper(1000) < p


def test_results_do_not_demonstrate_agi():
    assert r.results()["scorecard"]["AGI"] == "speculative"
    assert r.results()["blocked_without_benchmark"]
