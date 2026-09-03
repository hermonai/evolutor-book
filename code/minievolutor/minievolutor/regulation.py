"""Context-only bootstrap regulation semantics."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .substrate import Substrate


@dataclass(frozen=True, slots=True)
class ExpressionPlan:
    substrate: Substrate
    gate_map: dict[str, bool]


def regulate(substrate: Substrate, context: Mapping[str, Any]) -> ExpressionPlan:
    """Evaluate each gene gate against the immutable input context."""

    missing = set(substrate.genome.external_inputs) - set(context)
    if missing:
        raise ValueError(f"missing external inputs: {sorted(missing)}")
    gate_map = {
        gene.name: gene.is_enabled(context) for gene in substrate.schedule
    }
    return ExpressionPlan(substrate=substrate, gate_map=gate_map)

