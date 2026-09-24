"""A bounded typed developmental compiler, not biological development or NAS."""

from dataclasses import dataclass
import torch

LISTINGS = [
    "rewrite",
    "compile_program",
    "validate",
    "execute",
    "recursive_oracle",
    "parameter_bank",
    "costs",
]


def rewrite(word, rules, generations, limit=1024):
    """Simultaneous, not in-place, symbol replacement."""
    if type(generations) is not int or generations < 0:
        raise ValueError("nonnegative generation count required")
    if type(limit) is not int or limit < 1 or len(word) > limit:
        raise ValueError(
            "positive budget covering the initial word required"
        )
    history = [word]
    for _ in range(generations):
        if any(s not in rules for s in word):
            raise ValueError("missing production rule")
        if sum(len(rules[s]) for s in word) > limit:
            raise ValueError("rewrite budget exceeded before allocation")
        word = "".join(rules[s] for s in word)
        history.append(word)
    return history


@dataclass(frozen=True)
class Node:
    id: int
    op: str
    inputs: tuple
    width: int
    parameter: str = ""


def compile_program(depth, width, shared=True, budget=1023):
    """Expand R_d(x)=x+R_(d-1),right(R_(d-1),left(x))."""
    if type(depth) is not int or not 0 <= depth <= 20:
        raise ValueError("depth must be an integer from 0 through 20")
    if type(width) is not int or width < 1 or type(shared) is not bool:
        raise ValueError(
            "positive integer width and boolean sharing required"
        )
    if type(budget) is not int or budget < 2 ** (depth + 1) - 1:
        raise ValueError("insufficient expansion budget")
    nodes = []

    def emit(level, source, path):
        if level == 0:
            key = "shared" if shared else path
            node = Node(len(nodes) + 1, "affine", (source,), width, key)
        else:
            left = emit(level - 1, source, path + "L")
            right = emit(level - 1, left, path + "R")
            node = Node(len(nodes) + 1, "add", (source, right), width)
        nodes.append(node)
        return node.id

    output = emit(depth, 0, "root")
    validate(nodes, width)
    return tuple(nodes), output


def validate(nodes, input_width):
    """SSA-like topological order; node 0 is the external input."""
    if type(input_width) is not int or input_width < 1:
        raise ValueError("positive integer input width required")
    widths, owners = {0: input_width}, {}
    for node in nodes:
        if type(node.id) is not int or node.id < 1 or node.id in widths:
            raise ValueError("positive fresh node ID required")
        if type(node.width) is not int or node.width < 1:
            raise ValueError("positive integer node width required")
        arity = {"affine": 1, "add": 2}.get(node.op)
        if arity is None or len(node.inputs) != arity:
            raise ValueError("unknown operation or wrong arity")
        if any(i not in widths for i in node.inputs):
            raise ValueError(
                "inputs must already exist; forward edges forbidden"
            )
        if any(widths[i] != node.width for i in node.inputs):
            raise ValueError("square affine/residual widths must agree")
        if node.op == "affine":
            if not node.parameter:
                raise ValueError("affine parameter owner required")
            if owners.setdefault(node.parameter, node.width) != node.width:
                raise ValueError("shared owner has inconsistent shape")
        elif node.parameter:
            raise ValueError("add must not own affine parameters")
        widths[node.id] = node.width
    return owners


def execute(nodes, output, x, parameters):
    """Row-vector tensors [batch, width]; retain autograd through all uses."""
    if x.ndim != 2:
        raise ValueError("rank-two input required")
    owners = validate(nodes, x.shape[1])
    if set(parameters) != set(owners):
        raise ValueError("parameter owners must exactly match the graph")
    for key, width in owners.items():
        w, b = parameters[key]
        if w.shape != (width, width) or b.shape != (width,):
            raise ValueError("incorrect parameter shape")
    values = {0: x}
    for node in nodes:
        if node.op == "affine":
            w, b = parameters[node.parameter]
            values[node.id] = torch.tanh(values[node.inputs[0]] @ w + b)
        else:
            a, b = node.inputs
            values[node.id] = values[a] + values[b]
    if output not in values:
        raise ValueError("unknown output")
    return values[output]


def recursive_oracle(depth, x, parameters, shared=True, path="root"):
    """Independent tree interpreter; does not read the compiled node list."""
    if depth == 0:
        w, b = parameters["shared" if shared else path]
        return torch.tanh(x @ w + b)
    left = recursive_oracle(depth - 1, x, parameters, shared, path + "L")
    right = recursive_oracle(
        depth - 1, left, parameters, shared, path + "R"
    )
    return x + right


def parameter_bank(nodes, width, seed=17):
    owners = validate(nodes, width)
    generator = torch.Generator().manual_seed(seed)
    return {
        key: (
            torch.randn(
                width, width, generator=generator, dtype=torch.float64
            )
            .mul(0.2)
            .requires_grad_(),
            torch.randn(width, generator=generator, dtype=torch.float64)
            .mul(0.1)
            .requires_grad_(),
        )
        for key in sorted(owners)
    }


def costs(depth, width, shared):
    nodes, _ = compile_program(
        depth, width, shared, budget=2 ** (depth + 1) - 1
    )
    leaves = sum(n.op == "affine" for n in nodes)
    owners = len(validate(nodes, width))
    return dict(
        depth=depth,
        affine_calls=leaves,
        adds=leaves - 1,
        nodes=len(nodes),
        owners=owners,
        parameters=owners * (width**2 + width),
        matrix_macs_per_row=leaves * width**2,
    )


def results():
    x = torch.tensor([[0.4, -0.2]], dtype=torch.float64)
    nodes, out = compile_program(2, 2)
    params = parameter_bank(nodes, 2)
    return dict(
        rewrite=rewrite("S", {"S": "SG", "G": "GG"}, 3),
        graph=[
            dict(
                id=n.id,
                op=n.op,
                inputs=list(n.inputs),
                width=n.width,
                parameter=n.parameter,
            )
            for n in nodes
        ],
        output=execute(nodes, out, x, params).detach().tolist(),
        costs=[
            dict(
                **costs(d, 4, True),
                independent_parameters=costs(d, 4, False)["parameters"],
            )
            for d in range(7)
        ],
    )
