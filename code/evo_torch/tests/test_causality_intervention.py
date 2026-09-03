import torch

from evo_torch.causality import assert_prefix_causal
from evo_torch.recurrent_dna import RecurrentDNA, RecurrentDNAConfig
from evo_torch.transformer_dna import TransformerDNA, TransformerDNAConfig


def test_future_intervention_does_not_change_prefix_logits() -> None:
    torch.manual_seed(7)
    inputs = torch.tensor([[0, 1, 2, 3, 0, 1, 2, 3]])
    models = [
        TransformerDNA(TransformerDNAConfig(layers=1, dropout=0.0)),
        RecurrentDNA(RecurrentDNAConfig(layers=1)),
    ]
    for model in models:
        assert_prefix_causal(
            model,
            inputs,
            prefix_length=4,
            vocab_size=5,
            atol=1e-6,
        )

