import pytest

from minievolutor import Gene, Genome, compile_genome


def test_compiler_topologically_orders_dependencies() -> None:
    later = Gene("later", ("middle",), "answer", lambda x: x["middle"], int)
    earlier = Gene("earlier", ("input",), "middle", lambda x: x["input"], int)
    genome = Genome((later, earlier), ("input",), ("answer",))
    substrate = compile_genome(genome)
    assert [gene.name for gene in substrate.schedule] == ["earlier", "later"]
    assert substrate.arcs == (("earlier", "later"),)


def test_compiler_rejects_cycles() -> None:
    genome = Genome(
        genes=(
            Gene("a", ("b_out",), "a_out", lambda x: x["b_out"], int),
            Gene("b", ("a_out",), "b_out", lambda x: x["a_out"], int),
        ),
        external_inputs=(),
        outputs=("a_out",),
    )
    with pytest.raises(ValueError, match="cycle"):
        compile_genome(genome)

