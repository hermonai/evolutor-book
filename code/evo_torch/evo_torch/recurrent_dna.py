"""Minimal GRU DNA-language-model baseline with an explicit step API."""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass(frozen=True, slots=True)
class RecurrentDNAConfig:
    vocab_size: int = 5
    model_width: int = 32
    state_width: int = 32
    layers: int = 2


class RecurrentDNA(nn.Module):
    def __init__(self, config: RecurrentDNAConfig) -> None:
        super().__init__()
        self.config = config
        self.embedding = nn.Embedding(config.vocab_size, config.model_width)
        self.recurrence = nn.GRU(
            config.model_width,
            config.state_width,
            num_layers=config.layers,
            batch_first=True,
        )
        self.lm_head = nn.Linear(config.state_width, config.vocab_size)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        logits, _state = self.forward_with_state(input_ids)
        return logits

    def forward_with_state(
        self, input_ids: torch.Tensor, state: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if input_ids.ndim != 2:
            raise ValueError("input_ids must have shape [batch, time]")
        hidden, next_state = self.recurrence(self.embedding(input_ids), state)
        return self.lm_head(hidden), next_state

    def step(
        self, token_ids: torch.Tensor, state: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Advance one token and return `[batch, vocab]` logits plus state."""

        if token_ids.ndim == 1:
            token_ids = token_ids[:, None]
        if token_ids.ndim != 2 or token_ids.shape[1] != 1:
            raise ValueError("step expects one token per batch item")
        logits, next_state = self.forward_with_state(token_ids, state)
        return logits[:, 0, :], next_state

