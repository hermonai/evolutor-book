"""Small typed expression interpreter. Not an Evolutor runtime or compiler."""

from dataclasses import dataclass
import numpy as np

LISTINGS = ["TensorType", "Gene", "check_genome", "evaluate_checked"]


@dataclass(frozen=True)
class TensorType:
    axes: tuple[str, ...]
    sizes: tuple[int, ...]
    dtype: str = "float64"

    def __post_init__(self):
        if (
            type(self.axes) is not tuple
            or type(self.sizes) is not tuple
            or len(self.axes) != len(self.sizes)
            or len(set(self.axes)) != len(self.axes)
            or any(not isinstance(a, str) or not a for a in self.axes)
            or any(type(d) is not int or d < 1 for d in self.sizes)
            or self.dtype != "float64"
        ):
            raise ValueError(
                "distinct axes, positive sizes, float64 required"
            )

    def check(self, value):
        if (
            not isinstance(value, np.ndarray)
            or value.shape != self.sizes
            or str(value.dtype) != self.dtype
            or not np.isfinite(value).all()
        ):
            raise ValueError("runtime value violates declared type")


@dataclass(frozen=True)
class Gene:
    identity: str
    op: str
    source: str
    output: str
    type: TensorType
    owner: str


def check_genome(genes, inputs, parameters, states):
    """SSA values, exact semantic types, and one writer per state owner."""
    env, ids, writers = dict(inputs), set(), set()
    for gene in genes:
        if not gene.identity or gene.identity in ids or gene.output in env:
            raise ValueError("duplicate identity or output")
        if gene.source not in env or env[gene.source] != gene.type:
            raise ValueError("missing input or incompatible semantic type")
        if gene.op == "scale":
            if gene.owner not in parameters:
                raise ValueError("undeclared parameter owner")
        elif gene.op == "accumulate":
            if states.get(gene.owner) != gene.type or gene.owner in writers:
                raise ValueError(
                    "state mismatch or competing state writers"
                )
            writers.add(gene.owner)
        else:
            raise ValueError("unknown operation")
        ids.add(gene.identity)
        env[gene.output] = gene.type
    return env


def express(
    genes,
    inputs,
    input_types,
    parameters,
    states,
    state_types,
    enabled,
    version,
):
    """Validate, evaluate against a snapshot, return a new state on success."""
    check_genome(genes, input_types, parameters, state_types)
    if set(inputs) != set(input_types) or set(states) != set(state_types):
        raise ValueError("runtime keys must match declarations")
    if set(enabled) != {g.identity for g in genes}:
        raise ValueError(
            "explicit regulator decision for every gene required"
        )
    if any(type(v) is not bool for v in enabled.values()) or not version:
        raise ValueError("boolean decisions and a version required")
    for key, typ in input_types.items():
        typ.check(inputs[key])
    for key, typ in state_types.items():
        typ.check(states[key])
    if any(
        np.ndim(p) != 0 or not np.isfinite(p) for p in parameters.values()
    ):
        raise ValueError("finite scalar parameters required")
    return evaluate_checked(
        genes, inputs, parameters, states, enabled, version
    )


def evaluate_checked(genes, inputs, parameters, states, enabled, version):
    """Internal evaluator; express() validates the complete contract first."""
    values = {k: v.copy() for k, v in inputs.items()}
    next_state = {k: v.copy() for k, v in states.items()}
    trace = []
    for gene in genes:
        x = values[gene.source]
        on = enabled[gene.identity]
        if not on:
            y = x.copy()  # declared bypass, not missing output
        elif gene.op == "scale":
            y = x * parameters[gene.owner]
        else:
            y = x + states[gene.owner]  # read old snapshot
            next_state[gene.owner] = y.copy()
        gene.type.check(y)
        values[gene.output] = y
        trace.append(
            dict(
                version=version,
                gene=gene.identity,
                enabled=on,
                output=y.tolist(),
            )
        )
    return values, next_state, trace


def example():
    typ = TensorType(("feature",), (2,))
    genes = (
        Gene("g1", "scale", "x", "u", typ, "gain"),
        Gene("g2", "accumulate", "u", "y", typ, "memory"),
    )
    return typ, genes


def results():
    typ, genes = example()
    states = {"memory": np.zeros(2)}
    rows = []
    for tick in range(3):
        enabled = {"g1": True, "g2": tick != 2}
        values, states, trace = express(
            genes,
            {"x": np.array([1.0, 2.0])},
            {"x": typ},
            {"gain": 2.0},
            states,
            {"memory": typ},
            enabled,
            "teaching-v1",
        )
        rows.append(
            dict(
                tick=tick,
                enabled=enabled["g2"],
                output=values["y"].tolist(),
                state=states["memory"].tolist(),
                trace=trace,
            )
        )
    return dict(steps=rows)
