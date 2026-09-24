from pathlib import Path
import importlib.util
import json
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evolutor_book_ch15", ROOT / "drafts/ch15/reference.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_committed_results_match_execution():
    assert m.results() == json.loads(
        (ROOT / "drafts/ch15/results.json").read_text()
    )


@pytest.mark.parametrize("n", range(51))
def test_closed_form_and_exact_fuel(n):
    env = {"n": n, "s": 0}
    status, end, trace = m.run(m.PROGRAM, env, 4 * n + 2)
    assert status == "halt"
    assert dict(end.registers) == {"n": 0, "s": n * (n + 1) // 2}
    assert len(trace) == 4 * n + 2 and env == {"n": n, "s": 0}
    status, _, _ = m.run(m.PROGRAM, env, 4 * n + 1)
    assert status == "exhausted"
    assert m.replay(m.PROGRAM, m.configuration(0, env), trace) == end


def test_resume_and_trace_tamper():
    env = {"n": 4, "s": 0}
    status, c, t = m.run(m.PROGRAM, env, 7)
    assert status == "exhausted"
    status, end, tail = m.run(m.PROGRAM, dict(c.registers), 11, pc=c.pc)
    full = m.run(m.PROGRAM, env, 18)
    assert status == "halt" and end == full[1] and t + tail == full[2]
    bad = list(full[2])
    bad[2] = bad[1]
    with pytest.raises(ValueError):
        m.replay(m.PROGRAM, m.configuration(0, env), bad)


def test_exhaustion_is_not_divergence_and_effect_order():
    status, _, _ = m.run((("jump", 0),), {}, 10)
    assert status == "exhausted"
    left = m.run(
        (("add", "s", "n"), ("dec", "n"), ("halt",)), {"n": 3, "s": 0}, 3
    )
    right = m.run(
        (("dec", "n"), ("add", "s", "n"), ("halt",)), {"n": 3, "s": 0}, 3
    )
    assert dict(left[1].registers)["s"] == 3
    assert dict(right[1].registers)["s"] == 2
    assert m.run((("dec", "n"),), {"n": 0}, 2)[0] == "error"
    assert m.run((("dec", "n"),), {"n": 0}, 1)[0] == "error"


@pytest.mark.parametrize(
    "program",
    [
        (("jump", -1),),
        (("jump", 1),),
        (("unknown",),),
        (("add", "x", "missing"),),
        (("halt", 1),),
        (),
        [("halt",)],
    ],
)
def test_invalid_program_rejected(program):
    with pytest.raises(ValueError):
        m.run(program, {"x": 0}, 5)


def test_domain_and_no_mutation():
    with pytest.raises(ValueError):
        m.run(m.PROGRAM, {"n": True, "s": 0}, 8)
    with pytest.raises(ValueError):
        m.run(m.PROGRAM, {"n": 2, "s": 0}, -1)
    assert m.run(m.PROGRAM, {"n": -1, "s": 0}, 12)[0] == "exhausted"
