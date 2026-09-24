from pathlib import Path
import importlib.util
import sys
import json
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ch14_reference_tests", ROOT / "drafts/ch14/reference.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

from dataclasses import replace
import numpy as np


def args():
    typ, genes = m.example()
    return dict(
        genes=genes,
        inputs={"x": np.array([1.0, 2.0])},
        input_types={"x": typ},
        parameters={"gain": 2.0},
        states={"memory": np.zeros(2)},
        state_types={"memory": typ},
        enabled={"g1": True, "g2": True},
        version="teaching-v1",
    )


def test_three_step_trace_and_independent_recurrence():
    a = args()
    h = np.zeros(2)
    for tick in range(3):
        a["enabled"]["g2"] = tick != 2
        v, state, trace = m.express(**a)
        expected = 2 * a["inputs"]["x"]
        if tick != 2:
            expected = expected + h
            h = expected.copy()
        np.testing.assert_array_equal(v["y"], expected)
        np.testing.assert_array_equal(state["memory"], h)
        assert trace[-1]["enabled"] == (tick != 2)
        a["states"] = state


def test_no_input_state_output_aliasing():
    a = args()
    original = a["inputs"]["x"].copy()
    v, st, _ = m.express(**a)
    v["y"][:] = 99
    np.testing.assert_array_equal(st["memory"], [2.0, 4.0])
    np.testing.assert_array_equal(a["states"]["memory"], [0.0, 0.0])
    np.testing.assert_array_equal(a["inputs"]["x"], original)


@pytest.mark.parametrize(
    "change", ["source", "output", "identity", "owner", "op"]
)
def test_invalid_genome_fields(change):
    a = args()
    g1, g2 = a["genes"]
    values = {
        "source": "missing",
        "output": "x",
        "identity": "g1",
        "owner": "missing",
        "op": "unknown",
    }
    a["genes"] = (g1, replace(g2, **{change: values[change]}))
    with pytest.raises(ValueError):
        m.express(**a)


def test_semantic_axes_rejected_even_when_shapes_match():
    t1 = m.TensorType(("sample", "feature"), (2, 2))
    t2 = m.TensorType(("feature", "sample"), (2, 2))
    g = m.Gene("g", "scale", "x", "y", t2, "p")
    with pytest.raises(ValueError):
        m.check_genome((g,), {"x": t1}, {"p": 2.0}, {})
    assert t1.sizes == t2.sizes and t1 != t2


def test_state_writer_conflict_even_if_disabled():
    a = args()
    g1, g2 = a["genes"]
    a["genes"] += (replace(g2, identity="g3", source="y", output="z"),)
    a["enabled"]["g3"] = False
    with pytest.raises(ValueError):
        m.express(**a)


def test_disabled_invalid_owner_is_not_hidden():
    a = args()
    g1, g2 = a["genes"]
    a["genes"] = (replace(g1, owner="undeclared"), g2)
    a["enabled"]["g1"] = False
    with pytest.raises(ValueError):
        m.express(**a)


@pytest.mark.parametrize(
    "bad",
    [np.array([1, 2]), np.array([1.0, 2.0, 3.0]), np.array([np.nan, 2.0])],
)
def test_runtime_type_checks(bad):
    a = args()
    a["inputs"]["x"] = bad
    with pytest.raises(ValueError):
        m.express(**a)


def test_exception_after_state_proposal_does_not_mutate_original():
    a = args()
    typ = a["input_types"]["x"]
    a["genes"] += (m.Gene("g3", "scale", "y", "z", typ, "huge"),)
    a["enabled"]["g3"] = True
    a["parameters"]["huge"] = 1e308
    with np.errstate(over="ignore"):
        with pytest.raises(ValueError):
            m.express(**a)
    np.testing.assert_array_equal(a["states"]["memory"], [0.0, 0.0])


def test_explicit_regulator_and_exact_keys():
    for change in ("missing", "nonbool", "extra", "state"):
        a = args()
        if change == "missing":
            del a["enabled"]["g2"]
        if change == "nonbool":
            a["enabled"]["g2"] = 1
        if change == "extra":
            a["inputs"]["extra"] = np.zeros(2)
        if change == "state":
            a["states"] = {}
        with pytest.raises(ValueError):
            m.express(**a)


def test_empty_genome_identity_and_parameter_sharing():
    a = args()
    a["genes"] = ()
    a["enabled"] = {}
    v, st, tr = m.express(**a)
    assert tr == []
    np.testing.assert_array_equal(v["x"], a["inputs"]["x"])
    a = args()
    typ = a["input_types"]["x"]
    a["genes"] = (
        a["genes"][0],
        m.Gene("g2", "scale", "u", "y", typ, "gain"),
    )
    v, _, _ = m.express(**a)
    np.testing.assert_array_equal(v["y"], [4.0, 8.0])


@pytest.mark.parametrize(
    "axes,sizes",
    [(("a", "a"), (2, 2)), (("a",), (0,)), (("a",), (2, 2)), (("",), (2,))],
)
def test_invalid_type_declarations(axes, sizes):
    with pytest.raises(ValueError):
        m.TensorType(axes, sizes)


def test_committed_result_artifact_matches_execution():
    assert (
        json.loads((ROOT / "drafts/ch14/results.json").read_text())
        == m.results()
    )
