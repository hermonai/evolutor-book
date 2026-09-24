"""A deterministic integer register machine, not a production runtime."""

from dataclasses import dataclass
import json

LISTINGS = ["Configuration", "validate", "step", "run", "replay"]
PROGRAM = (
    ("jz", "n", 4),
    ("add", "s", "n"),
    ("dec", "n"),
    ("jump", 0),
    ("halt",),
)


@dataclass(frozen=True)
class Configuration:
    pc: int
    registers: tuple


def configuration(pc, env):
    if type(pc) is not int or pc < 0:
        raise ValueError("invalid program counter")
    if any(
        not isinstance(k, str) or not k or type(v) is not int
        for k, v in env.items()
    ):
        raise ValueError("named integer registers required")
    return Configuration(pc, tuple(sorted(env.items())))


def validate(program, env):
    if not isinstance(program, tuple) or not program:
        raise ValueError("nonempty program tuple required")
    for ins in program:
        if not isinstance(ins, tuple) or not ins:
            raise ValueError("instruction tuple required")
        op, args = ins[0], ins[1:]
        arity = {"jz": 2, "add": 2, "dec": 1, "jump": 1, "halt": 0}
        if op not in arity or len(args) != arity[op]:
            raise ValueError("unknown or malformed instruction")
        regs = (
            args[:1] if op in ("jz", "dec") else args if op == "add" else ()
        )
        if any(r not in env for r in regs):
            raise ValueError("undefined register")
        if op in ("jz", "jump"):
            target = args[-1]
            if type(target) is not int or not 0 <= target < len(program):
                raise ValueError("invalid branch target")


def step(program, config):
    """One rule application; integer values are mathematical, not machine words."""
    env = dict(config.registers)
    if not 0 <= config.pc < len(program):
        raise ValueError("no instruction at program counter")
    ins = program[config.pc]
    op, args = ins[0], ins[1:]
    pc = config.pc + 1
    if op == "add":
        env[args[0]] += env[args[1]]
    elif op == "dec":
        env[args[0]] -= 1
    elif op == "jump":
        pc = args[0]
    elif op == "jz":
        pc = args[1] if env[args[0]] == 0 else pc
    elif op == "halt":
        pc = len(program)
    else:
        raise ValueError("unknown operation")
    nxt = configuration(pc, env)
    event = (config.pc, tuple(ins), config.registers, nxt.pc, nxt.registers)
    return nxt, event, op == "halt"


def run(program, env, fuel, pc=0):
    """Validate first; return halt/exhausted/error and an immutable checkpoint."""
    config = configuration(pc, env)
    validate(program, env)
    if type(fuel) is not int or fuel < 0 or pc >= len(program):
        raise ValueError("invalid fuel or initial counter")
    trace = []
    for _ in range(fuel):
        try:
            nxt, event, halted = step(program, config)
        except ValueError:
            return "error", config, tuple(trace)
        config = nxt
        trace.append(event)
        if halted:
            return "halt", config, tuple(trace)
        if config.pc >= len(program):
            return "error", config, tuple(trace)
    return "exhausted", config, tuple(trace)


def replay(program, initial, events):
    """Recompute every transition. An empty or partial trace is allowed."""
    validate(program, dict(initial.registers))
    current = initial
    for event in events:
        nxt, expected, _ = step(program, current)
        if event != expected:
            raise ValueError("trace does not match transition semantics")
        current = nxt
    return current


def results():
    status, end, trace = run(PROGRAM, {"n": 3, "s": 0}, 14)
    return {
        "status": status,
        "result": dict(end.registers),
        "trace": [
            {
                "step": i + 1,
                "pc": e[0],
                "op": e[1][0],
                "n": dict(e[4])["n"],
                "s": dict(e[4])["s"],
                "next": e[3],
            }
            for i, e in enumerate(trace)
        ],
        "costs": [
            {
                "n": n,
                "steps": len(run(PROGRAM, {"n": n, "s": 0}, 4 * n + 2)[2]),
            }
            for n in range(9)
        ],
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
