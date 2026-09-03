from minievolutor import ExpressionMachine, Gene, Genome, compile_genome, regulate

genome = Genome(
    genes=(
        Gene(
            name="add",
            inputs=("left", "right"),
            output="total",
            operation=lambda values: values["left"] + values["right"],
            output_type=int,
            gate=lambda context: context.get("mode") == "sum",
        ),
    ),
    external_inputs=("left", "right", "mode"),
    outputs=("total",),
)
substrate = compile_genome(genome)
context = {"left": 2, "right": 3, "mode": "sum"}
result = ExpressionMachine().execute(regulate(substrate, context), context)
print(result.outputs)
print(result.trace.events)

