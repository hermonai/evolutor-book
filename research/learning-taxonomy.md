# Learning and change taxonomy

Separate the object that changes from the method used to change it.

- **Inference:** state advances under a fixed model; updating a KV cache is not weight learning.
- **Parameter learning:** gradients, local rules or black-box optimization change weights.
- **Memory writing:** stores new records; learning claims require measuring later use and interference.
- **Structural learning:** modifies graph, modules or program composition; compare with NAS and program synthesis.
- **Development:** constructs a phenotype from a representation and environment; need not optimize a loss online.
- **Population search:** maintains variation and selection over candidates; a single accepted edit is not itself a population.
- **Meta-learning:** learns an adaptation procedure; test on separated tasks.
- **Continual learning:** adapts without unacceptable loss of earlier competence; retention, transfer and resource growth all count.

Fast/medium/slow timescales are an experimental design choice, not a biological law. For example, a structural repair can occur faster than a long training run. E-S06–E-S09 are starting comparisons. Do not present a gradient-plus-edit diagram as proof of effective credit assignment.
