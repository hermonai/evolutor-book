"""Finite-intervention prefix-causality checks."""

from __future__ import annotations

import torch
from torch import nn


@torch.no_grad()
def prefix_intervention_error(
    model: nn.Module,
    input_ids: torch.Tensor,
    *,
    prefix_length: int,
    vocab_size: int,
) -> float:
    """Change every future token and measure the largest prefix-logit change."""

    if not 0 < prefix_length < input_ids.shape[1]:
        raise ValueError("prefix_length must leave both prefix and future positions")
    intervened = input_ids.clone()
    intervened[:, prefix_length:] = (
        intervened[:, prefix_length:] + 1
    ) % vocab_size
    was_training = model.training
    model.eval()
    baseline = model(input_ids)[:, :prefix_length, :]
    changed = model(intervened)[:, :prefix_length, :]
    model.train(was_training)
    return float((baseline - changed).abs().max())


def assert_prefix_causal(
    model: nn.Module,
    input_ids: torch.Tensor,
    *,
    prefix_length: int,
    vocab_size: int,
    atol: float = 1e-6,
) -> None:
    error = prefix_intervention_error(
        model,
        input_ids,
        prefix_length=prefix_length,
        vocab_size=vocab_size,
    )
    if error > atol:
        raise AssertionError(f"future intervention changed prefix logits by {error}")

