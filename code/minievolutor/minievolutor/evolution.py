"""Verified local replacement; no autonomous evolution."""

from __future__ import annotations

from dataclasses import replace

from .gene import Gene
from .genome import Genome
from .substrate import compile_genome


def replace_gene(genome: Genome, name: str, replacement: Gene) -> Genome:
    """Return a candidate with one named gene replaced."""

    if replacement.name != name:
        raise ValueError("replacement must preserve the gene name")
    if name not in {gene.name for gene in genome.genes}:
        raise ValueError(f"unknown gene {name!r}")
    genes = tuple(replacement if gene.name == name else gene for gene in genome.genes)
    return replace(genome, genes=genes)


def verify_local_replacement(original: Genome, candidate: Genome) -> None:
    """Check the bootstrap structural contract or raise.

    This checks compilation plus stable external/output interfaces. It is not a
    proof of behavioral equivalence or policy safety.
    """

    if candidate.external_inputs != original.external_inputs:
        raise ValueError("candidate changed the external input interface")
    if candidate.outputs != original.outputs:
        raise ValueError("candidate changed the output interface")
    compile_genome(candidate)

