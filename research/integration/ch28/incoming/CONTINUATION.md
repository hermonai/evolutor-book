# Continuity contract
EVOD-27 decomposed training memory into parameters, gradients, optimizer state,
activations and temporaries. EVOD-28 assigns ownership/communication to those states.
It distinguishes replicated DDP, state sharding/FSDP/ZeRO, tensor and pipeline
parallelism, and requires collective-semantics oracles. A training checkpoint is not
automatically a portable model artifact: artifact manifests separately bind tensor
names/shapes/dtypes, architecture/config, tokenizer/data contract, provenance,
checksums and compatibility.
