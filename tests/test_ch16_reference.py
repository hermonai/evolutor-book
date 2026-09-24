from pathlib import Path
import importlib.util
import json
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evolutor_book_ch16", ROOT / "drafts/ch16/reference.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_committed_results_match_execution():
    assert m.results() == json.loads(
        (ROOT / "drafts/ch16/results.json").read_text()
    )


def test_routing_accounting_and_padding():
    r = m.results()["routing"]
    a, b, c = r
    assert a["stored_parameters"] == 4 * (256 + 8)
    assert a["active_expert_parameters"] == 512
    assert a["router_macs"] == 128
    assert a["useful_expert_macs"] == 1024
    assert a["executed_expert_macs"] == 1024
    assert b["executed_expert_macs"] == 4096
    assert b["useful_expert_macs"] == 1024
    assert c["dropped_assignments"] == 1
    assert c["useful_expert_macs"] == 768
    assert c["executed_expert_macs"] == 2048
    assert a["dispatch_bytes"] == 256


def test_expert_permutation():
    a = m.routing_cost([(0, 1), (1, 2)], 3, 4, 8)
    b = m.routing_cost([(2, 0), (0, 1)], 3, 4, 8)
    assert a == b


def test_liveness_all_legal_schedules():
    from itertools import permutations

    sizes = {"x": 100, "a": 100, "b": 100, "c": 10, "d": 10, "y": 10}
    deps = {
        "a": ("x",),
        "b": ("x",),
        "c": ("a",),
        "d": ("b",),
        "y": ("c", "d"),
    }
    peaks = []
    for order in permutations(deps):
        done = {"x"}
        legal = True
        for node in order:
            if not set(deps[node]) <= done:
                legal = False
                break
            done.add(node)
        if legal:
            peak, trace = m.peak_live(sizes, ("x",), deps, order, ("y",))
            peaks.append(peak)
            # Independent interval-overlap oracle, allocate before release.
            position = {node: i for i, node in enumerate(order)}
            intervals = []
            for node in sizes:
                start = -1 if node == "x" else position[node]
                uses = [position[v] for v, ds in deps.items() if node in ds]
                end = (
                    len(order) if node == "y" else max(uses, default=start)
                )
                intervals.append((start, end, sizes[node]))
            oracle = max(
                sum(
                    size
                    for start, end, size in intervals
                    if start <= t <= end
                )
                for t in range(-1, len(order))
            )
            assert peak == oracle and trace[-1]["after"] == 10
    assert min(peaks) == 210 and max(peaks) == 300


@pytest.mark.parametrize("n", range(129))
def test_potential_and_aggregate(n):
    rows = m.trace_buffer(n)
    assert all(r["potential"] >= 0 and r["amortized"] <= 3 for r in rows)
    if n:
        assert (
            rows[-1]["total"]
            == sum(r["amortized"] for r in rows) - rows[-1]["potential"]
        )
        assert rows[-1]["total"] <= 3 * n
    else:
        assert rows == []


def test_invalid_cost_contracts():
    for routes in [[(0, 0)], [(4,)], [], [()]]:
        with pytest.raises(ValueError):
            m.routing_cost(routes, 4, 8, 16)
    with pytest.raises(ValueError):
        m.routing_cost([(0,)], 4, 8, 16, padded=True)
    with pytest.raises(ValueError):
        m.peak_live({"x": 1, "a": 1}, ("x",), {"a": ("a",)}, ("a",), ("a",))
    with pytest.raises(ValueError):
        m.trace_buffer(-1)
