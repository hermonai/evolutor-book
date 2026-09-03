"""Shared next-token objective for reference models."""

from __future__ import annotations

import torch
from torch.nn import functional as F


def next_token_loss(logits: torch.Tensor, input_ids: torch.Tensor) -> torch.Tensor:
    if logits.ndim != 3 or input_ids.ndim != 2:
        raise ValueError("expected logits [B,T,V] and input_ids [B,T]")
    if logits.shape[:2] != input_ids.shape:
        raise ValueError("logit and token batch/time dimensions must match")
    if input_ids.shape[1] < 2:
        raise ValueError("next-token loss requires at least two positions")
    return F.cross_entropy(
        logits[:, :-1, :].reshape(-1, logits.shape[-1]),
        input_ids[:, 1:].reshape(-1),
    )

