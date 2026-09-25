"""A proposed DNA-addressed state reference, not a trained DOGMA model."""

from dataclasses import dataclass
import json
import math

BASES = "ACGT"
COMP = dict(zip(BASES, "TGCA"))
PAIRS = tuple(a + b for a in BASES for b in BASES)
LISTINGS = [
    "State",
    "step",
    "scan",
    "reverse_complement",
    "permute_pairs",
    "bidirectional",
]
TABLES = [
    (
        "trace",
        ["Position", "Previous", "Selected pair", "Memory mass"],
        ["position", "previous", "pair", "mass"],
        "rlrr",
    ),
    (
        "counts",
        ["Pair", "Forward", "RC mapped"],
        ["pair", "forward", "mapped"],
        "lrr",
    ),
]
PLOTS = [("mass-plot", "mass", "length", ["unit", "half", "nine"])]


@dataclass(frozen=True)
class State:
    memory: tuple = (0.0,) * 16
    previous: str = ""
    position: int = 0


def validate_state(state):
    if (
        not isinstance(state, State)
        or not isinstance(state.memory, tuple)
        or len(state.memory) != 16
        or any(not math.isfinite(x) or x < 0 for x in state.memory)
        or state.previous not in ("", *BASES)
        or type(state.position) is not int
        or state.position < 0
        or (state.position == 0) != (state.previous == "")
    ):
        raise ValueError("invalid immutable state")


def step(state, symbol, retention=1.0, valid=True):
    validate_state(state)
    if (
        type(valid) is not bool
        or not math.isfinite(retention)
        or not 0 <= retention <= 1
    ):
        raise ValueError("Boolean mask and retention in [0,1] required")
    if not valid:
        return state, None
    if symbol not in tuple(BASES):
        raise ValueError("one canonical DNA base required")
    pair = state.previous + symbol if state.previous else ""
    memory = [retention * x for x in state.memory]
    if pair:
        memory[PAIRS.index(pair)] += 1.0
    nxt = State(tuple(memory), symbol, state.position + 1)
    event = (state, symbol, pair, nxt)
    return nxt, event


def scan(sequence, state=None, retention=1.0, mask=None):
    current = State() if state is None else state
    validate_state(current)
    if not math.isfinite(retention) or not 0 <= retention <= 1:
        raise ValueError("retention in [0,1] required")
    active = (True,) * len(sequence) if mask is None else tuple(mask)
    if len(active) != len(sequence):
        raise ValueError("mask length mismatch")
    events = []
    for symbol, valid in zip(sequence, active):
        current, event = step(current, symbol, retention, valid)
        if event is not None:
            events.append(event)
    return current, tuple(events)


def reverse_complement(sequence):
    if any(b not in COMP for b in sequence):
        raise ValueError("canonical DNA sequence required")
    return "".join(COMP[b] for b in reversed(sequence))


def permute_pairs(memory):
    if len(memory) != 16:
        raise ValueError("sixteen pair channels required")
    return tuple(memory[PAIRS.index(reverse_complement(p))] for p in PAIRS)


def bidirectional(sequence, retention=1.0):
    """Full-record feature; not an online causal update."""
    forward = scan(sequence, retention=retention)[0].memory
    reverse = scan(reverse_complement(sequence), retention=retention)[
        0
    ].memory
    mapped = permute_pairs(reverse)
    return tuple((a + b) / 2 for a, b in zip(forward, mapped))


def results():
    sequence = "ACGAC"
    end, events = scan(sequence)
    mapped = permute_pairs(scan(reverse_complement(sequence))[0].memory)
    return {
        "trace": [
            dict(
                position=e[3].position,
                previous=e[3].previous,
                pair=e[2] or "-",
                mass=sum(e[3].memory),
            )
            for e in events
        ],
        "counts": [
            dict(pair=p, forward=a, mapped=b)
            for p, a, b in zip(PAIRS, end.memory, mapped)
            if a or b
        ],
        "mass": [
            dict(
                length=n,
                unit=sum(scan("A" * n)[0].memory),
                half=sum(scan("A" * n, retention=0.5)[0].memory),
                nine=sum(scan("A" * n, retention=0.9)[0].memory),
            )
            for n in range(1, 31)
        ],
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
