import importlib.util
from pathlib import Path
import sys
import random
import pytest

spec = importlib.util.spec_from_file_location("evod42_test", Path(__file__).parents[1] / "drafts/ch42/reference.py")
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def test_all_named_crash_cuts_assigned_answers():
    rows = r.crash_cuts()
    assert [x["recovered"] for x in rows] == ["absent", "absent", "v1", "v1", "v1", "v2", "v2"]
    assert [x["durable"] for x in rows] == [0, 0, 1, 1, 1, 2, 2]


@pytest.mark.parametrize("seed", range(24))
def test_crash_recovery_prefix_oracle_and_idempotence(seed):
    rng, s = random.Random(seed), r.WalStore()
    for i in range(12):
        lsn = s.append(rng.choice(("a", "b", "c")), rng.randint(-100, 100))
        if rng.random() < .65:
            s.flush_log(lsn)
        if s.durable_lsn and rng.random() < .6:
            l, k, v = s.log[s.durable_lsn - 1]
            s.write_page(k, v, l)
        image = s.crash()
        image.recover()
        assert image.data == r.replay_prefix(s.log, s.durable_lsn)
        before = (dict(image.data), dict(image.page_lsn))
        image.recover()
        assert (image.data, image.page_lsn) == before
        assert len(image.log) == image.durable_lsn


def test_early_wrong_or_stale_page_rejected():
    s = r.WalStore(); a = s.append("x", 1)
    with pytest.raises(RuntimeError):
        s.write_page("x", 1, a)
    s.flush_log(a)
    with pytest.raises(ValueError):
        s.write_page("x", 999, a)
    with pytest.raises(ValueError):
        s.write_page("other", 1, a)
    b = s.append("x", 2); s.flush_log(b); s.write_page("x", 2, b)
    with pytest.raises(RuntimeError):
        s.write_page("x", 1, a)


@pytest.mark.parametrize("bad", [-1, 1, 999, True, .5])
def test_nonexistent_flush_rejected(bad):
    with pytest.raises(ValueError):
        r.WalStore().flush_log(bad)


def test_contract_before_cost_and_hard_risk_gate():
    plans = [r.Plan("wrong", "other", 0, 0, 0),
             r.Plan("unsafe", "required", 0, 0, .9),
             r.Plan("legal", "required", 4, 8, .02)]
    assert r.choose(plans, "required", 16, .1).name == "legal"
    with pytest.raises(RuntimeError):
        r.choose(plans, "required", 4, .1)


def test_dimensioned_score_and_tie():
    a, b = r.Plan("a", "s", 2, 1, .1), r.Plan("b", "s", 1, 1, .5)
    assert r.cost(a) == pytest.approx(3.1)
    assert r.choose([a, b], "s", 10, 1) == a
    assert r.choose([r.Plan("z", "s", 1, 1, 0), r.Plan("a", "s", 1, 1, 0)], "s", 10, 1).name == "a"


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -1, True])
def test_bad_cost_numbers(bad):
    with pytest.raises(ValueError):
        r.cost(r.Plan("p", "s", bad, 1, 0))


def test_crash_discards_unflushed_tail():
    s = r.WalStore(); s.append("x", 1); s.flush_log(1); s.append("x", 2)
    image = s.crash(); image.recover()
    assert image.data == {"x": 1} and image.log == [(1, "x", 1)]


@pytest.mark.parametrize("value", [True, 1.0])
def test_equal_but_wrong_scalar_type_rejected(value):
    s = r.WalStore(); s.append("x", 1); s.flush_log(1)
    with pytest.raises(ValueError):
        s.write_page("x", value, 1)
