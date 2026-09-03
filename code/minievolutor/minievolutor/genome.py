"""Persistent genome container and structural validation."""

from __future__ import annotations

from dataclasses import dataclass

from .gene import Gene


@dataclass(frozen=True, slots=True)
class Genome:
    genes: tuple[Gene, ...]
    external_inputs: tuple[str, ...]
    outputs: tuple[str, ...]

    def validate(self) -> None:
        names = [gene.name for gene in self.genes]
        produced = [gene.output for gene in self.genes]
        if len(names) != len(set(names)):
            raise ValueError("gene names must be unique")
        if len(produced) != len(set(produced)):
            raise ValueError("gene output keys must be unique")
        if set(self.external_inputs) & set(produced):
            raise ValueError("external and produced keys must be disjoint")
        available = set(self.external_inputs) | set(produced)
        missing = {
            key for gene in self.genes for key in gene.inputs if key not in available
        }
        if missing:
            raise ValueError(f"unknown gene inputs: {sorted(missing)}")
        unknown_outputs = set(self.outputs) - available
        if unknown_outputs:
            raise ValueError(f"unknown genome outputs: {sorted(unknown_outputs)}")

