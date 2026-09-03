"""Append-only trace values produced by the expression machine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class TraceEvent:
    kind: str
    gene: str
    detail: Any = None


@dataclass(slots=True)
class Trace:
    events: list[TraceEvent] = field(default_factory=list)

    def append(self, kind: str, gene: str, detail: Any = None) -> None:
        self.events.append(TraceEvent(kind=kind, gene=gene, detail=detail))

