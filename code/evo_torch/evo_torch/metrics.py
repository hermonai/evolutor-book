"""Architecture-neutral reporting helpers."""

from __future__ import annotations

from torch import nn


def parameter_count(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters())

