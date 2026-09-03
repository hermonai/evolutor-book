"""Compilation from a genome to an acyclic dependency substrate."""

from __future__ import annotations

from dataclasses import dataclass

from .gene import Gene
from .genome import Genome


@dataclass(frozen=True, slots=True)
class Substrate:
    genome: Genome
    schedule: tuple[Gene, ...]
    arcs: tuple[tuple[str, str], ...]


def compile_genome(genome: Genome) -> Substrate:
    """Validate and topologically schedule an acyclic genome."""

    genome.validate()
    producer = {gene.output: gene for gene in genome.genes}
    dependencies = {
        gene.name: {producer[key].name for key in gene.inputs if key in producer}
        for gene in genome.genes
    }
    remaining = {gene.name: gene for gene in genome.genes}
    schedule: list[Gene] = []
    completed: set[str] = set()
    while remaining:
        ready = [
            gene
            for gene in remaining.values()
            if dependencies[gene.name] <= completed
        ]
        if not ready:
            raise ValueError("genome dependencies contain a cycle")
        ready.sort(key=lambda gene: gene.name)
        for gene in ready:
            schedule.append(gene)
            completed.add(gene.name)
            remaining.pop(gene.name)
    arcs = tuple(
        sorted(
            (producer[key].name, gene.name)
            for gene in genome.genes
            for key in gene.inputs
            if key in producer
        )
    )
    return Substrate(genome=genome, schedule=tuple(schedule), arcs=arcs)

