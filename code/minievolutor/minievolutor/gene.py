"""Typed gene records for the minimal reference system."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

Store = Mapping[str, Any]


def _enabled(_context: Store) -> bool:
    return True


@dataclass(frozen=True, slots=True)
class Gene:
    name: str
    inputs: tuple[str, ...]
    output: str
    operation: Callable[[Store], Any]
    output_type: type
    gate: Callable[[Store], bool] = _enabled

    def is_enabled(self, context: Store) -> bool:
        return bool(self.gate(context))

