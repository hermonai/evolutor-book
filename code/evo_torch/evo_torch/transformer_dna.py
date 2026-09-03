"""Minimal causal Transformer DNA-language-model baseline."""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from torch import nn


@dataclass(frozen=True, slots=True)
class TransformerDNAConfig:
    vocab_size: int = 5
    model_width: int = 32
    layers: int = 2
    heads: int = 4
    ffn_width: int = 64
    max_length: int = 512
    dropout: float = 0.0


class TransformerDNA(nn.Module):
    """Reference-only autoregressive Transformer with learned positions."""

    def __init__(self, config: TransformerDNAConfig) -> None:
        super().__init__()
        self.config = config
        self.token_embedding = nn.Embedding(config.vocab_size, config.model_width)
        self.position_embedding = nn.Embedding(config.max_length, config.model_width)
        layer = nn.TransformerEncoderLayer(
            d_model=config.model_width,
            nhead=config.heads,
            dim_feedforward=config.ffn_width,
            dropout=config.dropout,
            batch_first=True,
            norm_first=True,
            activation="gelu",
        )
        self.blocks = nn.TransformerEncoder(
            layer, num_layers=config.layers, enable_nested_tensor=False
        )
        self.norm = nn.LayerNorm(config.model_width)
        self.lm_head = nn.Linear(config.model_width, config.vocab_size, bias=False)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        if input_ids.ndim != 2:
            raise ValueError("input_ids must have shape [batch, time]")
        _, length = input_ids.shape
        if length > self.config.max_length:
            raise ValueError("sequence exceeds configured max_length")
        positions = torch.arange(length, device=input_ids.device)
        hidden = self.token_embedding(input_ids) * math.sqrt(self.config.model_width)
        hidden = hidden + self.position_embedding(positions)[None, :, :]
        causal_mask = torch.triu(
            torch.full(
                (length, length),
                float("-inf"),
                device=input_ids.device,
                dtype=hidden.dtype,
            ),
            diagonal=1,
        )
        hidden = self.blocks(hidden, mask=causal_mask, is_causal=True)
        return self.lm_head(self.norm(hidden))

    def step(self, prefix_ids: torch.Tensor) -> torch.Tensor:
        """Transparent no-cache inference path returning the last logits."""

        return self(prefix_ids)[:, -1, :]
