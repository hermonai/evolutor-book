"""Deterministic plan execution with visible gate and firing traces."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .regulation import ExpressionPlan
from .trace import Trace


@dataclass(frozen=True, slots=True)
class ExpressionResult:
    outputs: dict[str, Any]
    store: dict[str, Any]
    trace: Trace
    expression_steps: int


class ExpressionMachine:
    def execute(
        self, plan: ExpressionPlan, context: Mapping[str, Any]
    ) -> ExpressionResult:
        store: dict[str, Any] = dict(context)
        trace = Trace()
        steps = 0
        for gene in plan.substrate.schedule:
            enabled = plan.gate_map[gene.name]
            trace.append("gate", gene.name, enabled)
            if not enabled:
                trace.append("skip", gene.name, "disabled")
                continue
            missing = set(gene.inputs) - set(store)
            if missing:
                raise RuntimeError(
                    f"enabled gene {gene.name!r} is missing inputs {sorted(missing)}"
                )
            arguments = {key: store[key] for key in gene.inputs}
            value = gene.operation(arguments)
            if not isinstance(value, gene.output_type):
                raise TypeError(
                    f"gene {gene.name!r} produced {type(value).__name__}; "
                    f"expected {gene.output_type.__name__}"
                )
            store[gene.output] = value
            steps += 1
            trace.append("fire", gene.name, {"output": gene.output})
        missing_outputs = set(plan.substrate.genome.outputs) - set(store)
        if missing_outputs:
            raise RuntimeError(f"expression did not produce {sorted(missing_outputs)}")
        outputs = {key: store[key] for key in plan.substrate.genome.outputs}
        return ExpressionResult(outputs, store, trace, steps)

