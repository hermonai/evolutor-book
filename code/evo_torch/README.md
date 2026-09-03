# evo_torch

`evo_torch` is the semantic neural reference layer. It begins with ordinary causal Transformer and GRU baselines, not a novel architecture.

Shared contracts:

- token tensors are `[batch, time]`;
- logits are `[batch, time, vocabulary]`;
- next-token loss uses shifted targets;
- inference parity is tested against full-sequence execution;
- prefix causality is tested by finite intervention on future tokens.

There is no optimized KV cache, scan kernel, custom runtime, or performance claim yet.

