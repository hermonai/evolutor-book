"""Explicit cost conventions; no timings or hardware throughput claims."""

from collections import Counter
import json

LISTINGS = ["routing_cost", "peak_live", "trace_buffer"]


def positive(*values):
    if any(type(v) is not int or v < 1 for v in values):
        raise ValueError("positive integer dimensions required")


def routing_cost(
    routes, experts, width, hidden, capacity=None, padded=False
):
    """Top-k routes; overflow is dropped in input order; bytes are dispatch only."""
    positive(experts, width, hidden)
    if not routes or any(not r for r in routes):
        raise ValueError("nonempty routing batch required")
    k = len(routes[0])
    if any(
        len(r) != k
        or len(set(r)) != k
        or any(type(e) is not int or not 0 <= e < experts for e in r)
        for r in routes
    ):
        raise ValueError("equal top-k distinct expert IDs required")
    if capacity is not None:
        positive(capacity)
    if padded and capacity is None:
        raise ValueError("padding needs explicit capacity")
    counts = Counter(e for row in routes for e in row)
    accepted = {
        e: min(n, capacity) if capacity is not None else n
        for e, n in counts.items()
    }
    useful = sum(accepted.values())
    slots = experts * capacity if padded else useful
    return {
        "stored_parameters": experts * (2 * width * hidden + width),
        "active_expert_parameters": len(accepted) * 2 * width * hidden,
        "router_macs": len(routes) * width * experts,
        "useful_expert_macs": useful * 2 * width * hidden,
        "executed_expert_macs": slots * 2 * width * hidden,
        "dropped_assignments": len(routes) * k - useful,
        "dispatch_bytes": useful * 2 * width * 4,
    }


def validate_layout(sizes, inputs, dependencies, schedule, outputs):
    """Validate declarations before executing a buffer schedule."""
    if any(type(v) is not int or v < 1 for v in sizes.values()):
        raise ValueError("positive allocation sizes required")
    if set(inputs) & set(dependencies) or set(sizes) != set(inputs) | set(
        dependencies
    ):
        raise ValueError("exact unique buffer declarations required")
    if (
        set(outputs) - set(sizes)
        or set(schedule) != set(dependencies)
        or len(schedule) != len(dependencies)
    ):
        raise ValueError(
            "complete unique schedule and declared outputs required"
        )
    if any(v not in sizes for deps in dependencies.values() for v in deps):
        raise ValueError("undefined dependency")


def peak_live(sizes, inputs, dependencies, schedule, outputs):
    """Abstract bytes; allocate result before freeing last-use operands."""
    validate_layout(sizes, inputs, dependencies, schedule, outputs)
    remaining = Counter(v for deps in dependencies.values() for v in deps)
    live = set(inputs)
    peak = sum(sizes[v] for v in live)
    trace = []
    for node in schedule:
        deps = dependencies[node]
        if any(v not in live for v in deps):
            raise ValueError("dependency not available")
        live.add(node)
        allocated = sum(sizes[v] for v in live)
        peak = max(peak, allocated)
        for v in deps:
            remaining[v] -= 1
            if remaining[v] == 0 and v not in outputs:
                live.discard(v)
        if remaining[node] == 0 and node not in outputs:
            live.discard(node)
        trace.append(
            {
                "node": node,
                "allocated": allocated,
                "after": sum(sizes[v] for v in live),
            }
        )
    return peak, trace


def trace_buffer(events):
    """Count writes plus copies in a doubling vector; empty buffer has capacity 0."""
    if type(events) is not int or events < 0:
        raise ValueError("nonnegative event count required")
    size, capacity, total = 0, 0, 0
    rows = []
    for _ in range(events):
        old_phi = 2 * size - capacity
        copied = 0
        if size == capacity:
            copied = size
            capacity = max(1, 2 * capacity)
        size += 1
        actual = 1 + copied
        phi = 2 * size - capacity
        amortized = actual + phi - old_phi
        total += actual
        rows.append(
            dict(
                size=size,
                capacity=capacity,
                actual=actual,
                potential=phi,
                amortized=amortized,
                total=total,
            )
        )
    return rows


def results():
    routes = [(0,), (0,), (0,), (1,)]
    sizes = {"x": 100, "a": 100, "b": 100, "c": 10, "d": 10, "y": 10}
    deps = {
        "a": ("x",),
        "b": ("x",),
        "c": ("a",),
        "d": ("b",),
        "y": ("c", "d"),
    }
    schedules = [("a", "b", "c", "d", "y"), ("a", "c", "b", "d", "y")]
    return {
        "routing": [
            {"name": name, **routing_cost(routes, 4, 8, 16, cap, padded)}
            for name, cap, padded in [
                ("ragged", None, False),
                ("padded", 4, True),
                ("capped", 2, True),
            ]
        ],
        "memory": [
            {
                "order": list(s),
                "peak": peak_live(sizes, ("x",), deps, s, ("y",))[0],
                "trace": peak_live(sizes, ("x",), deps, s, ("y",))[1],
            }
            for s in schedules
        ],
        "buffer": trace_buffer(16),
        "roofline": [
            {"intensity": i, "throughput": min(100.0, 10.0 * i)}
            for i in [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]
        ],
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
