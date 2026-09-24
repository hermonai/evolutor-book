"""Assigned promoter weights and mean-expression dynamics; not fitted biology."""

from dataclasses import dataclass
import math

LISTINGS = [
    "occupancy",
    "expression_step",
    "regulated_step",
    "steady_state",
    "simulate",
]


def finite_nonnegative(*values):
    if any(not math.isfinite(v) or v < 0 for v in values):
        raise ValueError("finite nonnegative quantities required")


def occupancy(polymerase, repressor):
    """Weights relative to empty promoter; mutually exclusive binding."""
    finite_nonnegative(polymerase, repressor)
    # Scaling avoids overflow when summing large but finite weights.
    scale = max(1.0, polymerase, repressor)
    weights = [1.0 / scale, polymerase / scale, repressor / scale]
    total = sum(weights)
    return tuple(w / total for w in weights)


@dataclass(frozen=True)
class Definition:
    max_transcription: float
    translation: float
    rna_loss: float
    protein_loss: float


@dataclass(frozen=True)
class State:
    rna: float = 0.0
    protein: float = 0.0


def expression_step(
    state, production, translation, rna_loss, protein_loss, dt
):
    """Exact constant-input two-stage linear dynamics, positive loss rates."""
    finite_nonnegative(
        state.rna,
        state.protein,
        production,
        translation,
        rna_loss,
        protein_loss,
        dt,
    )
    if rna_loss == 0 or protein_loss == 0:
        raise ValueError("strictly positive loss rates required")
    m_star = production / rna_loss
    em, ep = math.exp(-rna_loss * dt), math.exp(-protein_loss * dt)
    gap = abs(protein_loss - rna_loss)
    if gap == 0:
        mixed = dt * em
    else:
        mixed = (
            math.exp(-min(rna_loss, protein_loss) * dt)
            * -math.expm1(-gap * dt)
            / gap
        )
    integral = -math.expm1(-protein_loss * dt) / protein_loss
    m = m_star + (state.rna - m_star) * em
    p = state.protein * ep + translation * (
        m_star * integral + (state.rna - m_star) * mixed
    )
    return State(m, p)


def regulated_step(
    definition, state, polymerase, repressor, accessible, dt
):
    """No hard selector: accessibility scales conditional promoter activity."""
    finite_nonnegative(accessible, definition.max_transcription)
    if accessible > 1:
        raise ValueError("accessibility must lie in [0, 1]")
    bound = occupancy(polymerase, repressor)[1]
    source = definition.max_transcription * accessible * bound
    return expression_step(
        state,
        source,
        definition.translation,
        definition.rna_loss,
        definition.protein_loss,
        dt,
    )


def steady_state(production, translation, rna_loss, protein_loss):
    finite_nonnegative(production, translation, rna_loss, protein_loss)
    if min(rna_loss, protein_loss) <= 0:
        raise ValueError("positive loss rates required")
    m = production / rna_loss
    return State(m, translation * m / protein_loss)


def simulate(definition, intervals, initial=State()):
    """Each interval is (duration, polymerase weight, repressor weight, access)."""
    time, state = 0.0, initial
    records = [dict(time=time, rna=state.rna, protein=state.protein)]
    for dt, u, r, access in intervals:
        state = regulated_step(definition, state, u, r, access, dt)
        time += dt
        records.append(
            dict(time=time, rna=state.rna, protein=state.protein)
        )
    return records


def results():
    definition = Definition(12, 2, 1, 0.5)
    # u=.2 gives activity 1/6, hence source 2; close access at t=4.
    schedule = [(0.25, 0.2, 0, 1 if i < 16 else 0) for i in range(48)]
    response = simulate(definition, schedule)
    alternatives = []
    for t in [0, 0.5, 1, 2, 4, 8]:
        a = expression_step(State(), 2, 2, 1, 0.5, t)
        b = expression_step(State(), 1, 4, 1, 0.5, t)
        c = expression_step(State(), 4, 2, 2, 0.5, t)
        alternatives.append(
            dict(
                time=t,
                rna_a=a.rna,
                protein_a=a.protein,
                rna_b=b.rna,
                protein_b=b.protein,
                protein_c=c.protein,
            )
        )
    return dict(
        occupancy=[
            dict(
                repressor=r,
                active=occupancy(0.2, r)[1],
                fold=occupancy(0.2, r)[1] / occupancy(0.2, 0)[1],
            )
            for r in [0, 0.2, 1, 4, 10]
        ],
        response=response,
        alternatives=alternatives,
        steady=steady_state(2, 2, 1, 0.5).__dict__,
        memory=[
            regulated_step(definition, s, 0.2, 0, 0, 1).__dict__
            for s in [State(), State(2, 8)]
        ],
    )
