import pytest

from minievolutor import ExpressionMachine, Gene, Genome, compile_genome, regulate


def make_genome() -> Genome:
    return Genome(
        genes=(
            Gene(
                name="double",
                inputs=("x",),
                output="twice",
                operation=lambda values: values["x"] * 2,
                output_type=int,
            ),
            Gene(
                name="render",
                inputs=("twice",),
                output="answer",
                operation=lambda values: f"value={values['twice']}",
                output_type=str,
                gate=lambda context: context["emit"],
            ),
        ),
        external_inputs=("x", "emit"),
        outputs=("answer",),
    )


def test_compile_regulate_execute_emits_trace() -> None:
    substrate = compile_genome(make_genome())
    context = {"x": 4, "emit": True}
    result = ExpressionMachine().execute(regulate(substrate, context), context)
    assert result.outputs == {"answer": "value=8"}
    assert result.expression_steps == 2
    assert [(event.kind, event.gene) for event in result.trace.events] == [
        ("gate", "double"),
        ("fire", "double"),
        ("gate", "render"),
        ("fire", "render"),
    ]


def test_disabled_required_gene_makes_missing_output_visible() -> None:
    substrate = compile_genome(make_genome())
    context = {"x": 4, "emit": False}
    with pytest.raises(RuntimeError, match="did not produce"):
        ExpressionMachine().execute(regulate(substrate, context), context)


def test_runtime_type_check_rejects_wrong_value() -> None:
    genome = Genome(
        genes=(
            Gene("bad", ("x",), "answer", lambda _values: "not an int", int),
        ),
        external_inputs=("x",),
        outputs=("answer",),
    )
    substrate = compile_genome(genome)
    with pytest.raises(TypeError, match="expected int"):
        ExpressionMachine().execute(regulate(substrate, {"x": 1}), {"x": 1})

