import torch

from evo_torch import (
    DNATokenizer,
    RecurrentDNA,
    RecurrentDNAConfig,
    TransformerDNA,
    TransformerDNAConfig,
)
from evo_torch.training import next_token_loss


def test_shared_forward_contract_and_loss() -> None:
    tokenizer = DNATokenizer()
    inputs = tokenizer.encode("ACGTAC")[None, :]
    models = [
        TransformerDNA(
            TransformerDNAConfig(vocab_size=tokenizer.vocab_size, layers=1)
        ),
        RecurrentDNA(RecurrentDNAConfig(vocab_size=tokenizer.vocab_size, layers=1)),
    ]
    for model in models:
        logits = model(inputs)
        assert logits.shape == (1, 6, tokenizer.vocab_size)
        assert torch.isfinite(next_token_loss(logits, inputs))


def test_tokenizer_round_trip() -> None:
    tokenizer = DNATokenizer()
    assert tokenizer.decode(tokenizer.encode("ac gt")) == "ACGT"

