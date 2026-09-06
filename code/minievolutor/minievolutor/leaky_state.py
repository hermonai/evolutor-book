"""Exact discrete leaky-state control. Not fitted biological kinetics."""
from dataclasses import dataclass
from fractions import Fraction
from collections.abc import Iterable


def rational(value, name):
    if type(value) not in (int, Fraction):
        raise TypeError(f"{name} must be int or Fraction; floats are not exact inputs")
    return Fraction(value)


@dataclass(frozen=True)
class Step:
    time: int
    signal: int
    before: Fraction
    after: Fraction
    instantaneous: Fraction


def response(signals: Iterable[int], *, production=2, loss=Fraction(1, 2), initial=0):
    """Update x[t+1]=(1-loss)*x[t]+production*u[t] in arbitrary units.

    loss is a fraction per discrete update, not a continuous-time rate.
    No genome, regulation network, learning or inheritance is implemented.
    """
    p, d, x = (rational(production, "production"), rational(loss, "loss"),
               rational(initial, "initial"))
    if p < 0 or x < 0 or not 0 <= d <= 1:
        raise ValueError("require nonnegative production/state and loss in [0,1]")
    inputs = tuple(signals)
    if any(type(u) is not int or u not in (0, 1) for u in inputs):
        raise ValueError("signals must be integer zero or one")
    steps = []
    for time, signal in enumerate(inputs):
        after = (1 - d) * x + p * signal
        steps.append(Step(time, signal, x, after, p * signal))
        x = after
    return tuple(steps)


def closed_form(signals: Iterable[int], *, production=2, loss=Fraction(1, 2), initial=0):
    """Independent convolution expression for the final state; validates via response."""
    inputs = tuple(signals)
    response(inputs, production=production, loss=loss, initial=initial)
    p, d, start = Fraction(production), Fraction(loss), Fraction(initial)
    a, count = 1 - d, len(inputs)
    return a**count * start + p * sum((a**(count - 1 - j) * u
                                      for j, u in enumerate(inputs)), Fraction(0))


def chapter_example():
    return response((1, 1, 0, 0, 0, 1))
