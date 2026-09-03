import torch

from evo_torch.recurrent_dna import RecurrentDNA, RecurrentDNAConfig
from evo_torch.transformer_dna import TransformerDNA, TransformerDNAConfig


def test_recurrent_full_sequence_matches_repeated_step() -> None:
    torch.manual_seed(11)
    model = RecurrentDNA(RecurrentDNAConfig(layers=1))
    model.eval()
    inputs = torch.tensor([[0, 1, 2, 3, 0]])
    full = model(inputs)
    state = None
    steps = []
    for position in range(inputs.shape[1]):
        logits, state = model.step(inputs[:, position], state)
        steps.append(logits)
    repeated = torch.stack(steps, dim=1)
    torch.testing.assert_close(full, repeated)


def test_transformer_prefix_step_matches_full_position() -> None:
    torch.manual_seed(13)
    model = TransformerDNA(TransformerDNAConfig(layers=1, dropout=0.0))
    model.eval()
    inputs = torch.tensor([[0, 1, 2, 3, 0]])
    full = model(inputs)
    for length in range(1, inputs.shape[1] + 1):
        torch.testing.assert_close(model.step(inputs[:, :length]), full[:, length - 1, :])

