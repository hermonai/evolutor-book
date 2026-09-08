"""Finite-intervention prefix-causality checks."""

from __future__ import annotations

import torch
import math
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

    if (input_ids.ndim != 2 or input_ids.shape[0] < 1
            or input_ids.dtype != torch.long):
        raise ValueError("nonempty batch of integer token IDs [B,T] required")
    if type(vocab_size) is not int or vocab_size < 2:
        raise ValueError("vocab_size must permit a nontrivial intervention")
    if type(prefix_length) is not int or not 0 < prefix_length < input_ids.shape[1]:
        raise ValueError("prefix_length must leave both prefix and future positions")
    if input_ids.min() < 0 or input_ids.max() >= vocab_size:
        raise ValueError("input token outside vocabulary")
    intervened = input_ids.clone()
    intervened[:, prefix_length:] = (
        intervened[:, prefix_length:] + 1
    ) % vocab_size
    modes = [(module, module.training) for module in model.modules()]
    try:
        model.eval()
        outputs = []
        for ids in (input_ids, intervened):
            output = model(ids)
            if (not isinstance(output, torch.Tensor) or output.ndim != 3
                    or output.shape[:2] != ids.shape or output.shape[2] < 1
                    or not output.is_floating_point() or not torch.isfinite(output).all()):
                raise ValueError("finite floating logits [B,T,V] required")
            outputs.append(output[:, :prefix_length, :].clone())
        if outputs[0].shape != outputs[1].shape:
            raise ValueError("output shape changed under intervention")
        error = float((outputs[0] - outputs[1]).abs().max())
        if not math.isfinite(error):
            raise ValueError("non-finite intervention difference")
        return error
    finally:
        # Preserve mixed train/eval child modes even if forward raises.
        for module, training in modes:
            module.training = training


def assert_prefix_causal(
    model: nn.Module,
    input_ids: torch.Tensor,
    *,
    prefix_length: int,
    vocab_size: int,
    atol: float = 1e-6,
) -> None:
    if not math.isfinite(atol) or atol < 0:
        raise ValueError("finite nonnegative tolerance required")
    error = prefix_intervention_error(
        model,
        input_ids,
        prefix_length=prefix_length,
        vocab_size=vocab_size,
    )
    if error > atol:
        raise AssertionError(f"future intervention changed prefix logits by {error}")
