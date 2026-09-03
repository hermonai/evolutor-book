"""Clear, intentionally unoptimized autoregressive inference."""

from __future__ import annotations

import torch
from torch import nn


@torch.no_grad()
def greedy_decode(model: nn.Module, prompt: torch.Tensor, new_tokens: int) -> torch.Tensor:
    if prompt.ndim != 2:
        raise ValueError("prompt must have shape [batch, time]")
    generated = prompt.clone()
    for _ in range(new_tokens):
        logits = model(generated)
        next_id = logits[:, -1, :].argmax(dim=-1, keepdim=True)
        generated = torch.cat((generated, next_id), dim=1)
    return generated

