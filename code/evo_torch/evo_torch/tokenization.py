"""A transparent character-level DNA tokenizer."""

from __future__ import annotations

import torch


class DNATokenizer:
    symbols = ("A", "C", "G", "T", "<pad>")

    def __init__(self) -> None:
        self.token_to_id = {token: index for index, token in enumerate(self.symbols)}
        self.id_to_token = dict(enumerate(self.symbols))

    @property
    def vocab_size(self) -> int:
        return len(self.symbols)

    def encode(self, sequence: str) -> torch.Tensor:
        normalized = "".join(sequence.split()).upper()
        invalid = sorted(set(normalized) - set(self.symbols[:4]))
        if invalid:
            raise ValueError(f"invalid DNA bases: {invalid}")
        return torch.tensor([self.token_to_id[base] for base in normalized])

    def decode(self, token_ids: torch.Tensor) -> str:
        tokens = [self.id_to_token[int(index)] for index in token_ids.flatten()]
        return "".join(token for token in tokens if token != "<pad>")

