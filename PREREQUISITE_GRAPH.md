# Evolutor: undergraduate-first architecture

Status: planning only. No new chapters, finished figures, animations, experiments or reviewed learning outcomes are claimed. Generated from [pedagogy/curriculum.json](pedagogy/curriculum.json); edit that source and regenerate.

## Canonical Unicode TXT dependency graph

Read A → B as: teach A before requiring it in B. Multiple incoming arrows mean all listed prerequisites. ENTRY means only the declared entry assumptions. Book I IDs are explicitly prefixed DNAU; they describe planned teaching, not competence already delivered by the old draft.

```text
DNAU-03 → EVOU-01 : prerequisite for Programs, genomes and the question of Evolutor
DNAU-09 → EVOU-01 : prerequisite for Programs, genomes and the question of Evolutor
DNAU-32 → EVOU-01 : prerequisite for Programs, genomes and the question of Evolutor
EVOU-01 → EVOU-02 : prerequisite for Programs that choose and remember
DNAU-03 → EVOU-02 : prerequisite for Programs that choose and remember
DNAU-04 → EVOU-02 : prerequisite for Programs that choose and remember
EVOU-02 → EVOU-03 : prerequisite for Machine learning with one tiny model
DNAU-03 → EVOU-03 : prerequisite for Machine learning with one tiny model
DNAU-34 → EVOU-03 : prerequisite for Machine learning with one tiny model
EVOU-03 → EVOU-04 : prerequisite for Data, uncertainty and fair evaluation
DNAU-12 → EVOU-04 : prerequisite for Data, uncertainty and fair evaluation
EVOU-03 → EVOU-05 : prerequisite for Vectors, matrices and tensors as data containers
DNAU-34 → EVOU-05 : prerequisite for Vectors, matrices and tensors as data containers
EVOU-03 → EVOU-06 : prerequisite for Slopes, gradients and improving a prediction
EVOU-04 → EVOU-06 : prerequisite for Slopes, gradients and improving a prediction
EVOU-05 → EVOU-06 : prerequisite for Slopes, gradients and improving a prediction
DNAU-08 → EVOU-06 : prerequisite for Slopes, gradients and improving a prediction
DNAU-34 → EVOU-06 : prerequisite for Slopes, gradients and improving a prediction
EVOU-05 → EVOU-07 : prerequisite for Neural networks built one layer at a time
EVOU-06 → EVOU-07 : prerequisite for Neural networks built one layer at a time
DNAU-03 → EVOU-07 : prerequisite for Neural networks built one layer at a time
DNAU-34 → EVOU-07 : prerequisite for Neural networks built one layer at a time
EVOU-04 → EVOU-08 : prerequisite for A complete small training loop in PyTorch
EVOU-06 → EVOU-08 : prerequisite for A complete small training loop in PyTorch
EVOU-07 → EVOU-08 : prerequisite for A complete small training loop in PyTorch
DNAU-04 → EVOU-08 : prerequisite for A complete small training loop in PyTorch
EVOU-05 → EVOU-09 : prerequisite for Tokens, embeddings and predicting the next symbol
EVOU-07 → EVOU-09 : prerequisite for Tokens, embeddings and predicting the next symbol
EVOU-08 → EVOU-09 : prerequisite for Tokens, embeddings and predicting the next symbol
DNAU-02 → EVOU-09 : prerequisite for Tokens, embeddings and predicting the next symbol
DNAU-12 → EVOU-09 : prerequisite for Tokens, embeddings and predicting the next symbol
DNAU-33 → EVOU-09 : prerequisite for Tokens, embeddings and predicting the next symbol
EVOU-02 → EVOU-10 : prerequisite for Recurrence: remembering one step at a time
EVOU-06 → EVOU-10 : prerequisite for Recurrence: remembering one step at a time
EVOU-08 → EVOU-10 : prerequisite for Recurrence: remembering one step at a time
EVOU-09 → EVOU-10 : prerequisite for Recurrence: remembering one step at a time
DNAU-28 → EVOU-10 : prerequisite for Recurrence: remembering one step at a time
EVOU-05 → EVOU-11 : prerequisite for Gates and state-space models
EVOU-10 → EVOU-11 : prerequisite for Gates and state-space models
DNAU-28 → EVOU-11 : prerequisite for Gates and state-space models
DNAU-34 → EVOU-11 : prerequisite for Gates and state-space models
EVOU-05 → EVOU-12 : prerequisite for Attention as a weighted lookup
EVOU-06 → EVOU-12 : prerequisite for Attention as a weighted lookup
EVOU-09 → EVOU-12 : prerequisite for Attention as a weighted lookup
DNAU-12 → EVOU-12 : prerequisite for Attention as a weighted lookup
DNAU-34 → EVOU-12 : prerequisite for Attention as a weighted lookup
EVOU-07 → EVOU-13 : prerequisite for From one attention head to a Transformer
EVOU-08 → EVOU-13 : prerequisite for From one attention head to a Transformer
EVOU-12 → EVOU-13 : prerequisite for From one attention head to a Transformer
DNAU-34 → EVOU-13 : prerequisite for From one attention head to a Transformer
EVOU-10 → EVOU-14 : prerequisite for Caches, retrieval and external memory
EVOU-13 → EVOU-14 : prerequisite for Caches, retrieval and external memory
DNAU-33 → EVOU-14 : prerequisite for Caches, retrieval and external memory
EVOU-02 → EVOU-15 : prerequisite for If/else, dispatch, plugins and dynamic routing
EVOU-04 → EVOU-15 : prerequisite for If/else, dispatch, plugins and dynamic routing
DNAU-03 → EVOU-15 : prerequisite for If/else, dispatch, plugins and dynamic routing
DNAU-04 → EVOU-15 : prerequisite for If/else, dispatch, plugins and dynamic routing
DNAU-06 → EVOU-15 : prerequisite for If/else, dispatch, plugins and dynamic routing
EVOU-04 → EVOU-16 : prerequisite for Mixture of experts and learned routing
EVOU-08 → EVOU-16 : prerequisite for Mixture of experts and learned routing
EVOU-13 → EVOU-16 : prerequisite for Mixture of experts and learned routing
EVOU-15 → EVOU-16 : prerequisite for Mixture of experts and learned routing
DNAU-06 → EVOU-16 : prerequisite for Mixture of experts and learned routing
DNAU-34 → EVOU-16 : prerequisite for Mixture of experts and learned routing
EVOU-02 → EVOU-17 : prerequisite for Source code, compilers, runtimes and interfaces
EVOU-15 → EVOU-17 : prerequisite for Source code, compilers, runtimes and interfaces
DNAU-04 → EVOU-17 : prerequisite for Source code, compilers, runtimes and interfaces
DNAU-25 → EVOU-17 : prerequisite for Source code, compilers, runtimes and interfaces
EVOU-14 → EVOU-18 : prerequisite for Services, databases, protocols and scheduling
EVOU-17 → EVOU-18 : prerequisite for Services, databases, protocols and scheduling
DNAU-03 → EVOU-18 : prerequisite for Services, databases, protocols and scheduling
DNAU-35 → EVOU-18 : prerequisite for Services, databases, protocols and scheduling
EVOU-04 → EVOU-19 : prerequisite for Baselines, oracles and resource-matched experiments
EVOU-08 → EVOU-19 : prerequisite for Baselines, oracles and resource-matched experiments
EVOU-11 → EVOU-19 : prerequisite for Baselines, oracles and resource-matched experiments
EVOU-13 → EVOU-19 : prerequisite for Baselines, oracles and resource-matched experiments
EVOU-16 → EVOU-19 : prerequisite for Baselines, oracles and resource-matched experiments
EVOU-18 → EVOU-19 : prerequisite for Baselines, oracles and resource-matched experiments
DNAU-06 → EVOU-19 : prerequisite for Baselines, oracles and resource-matched experiments
DNAU-12 → EVOU-19 : prerequisite for Baselines, oracles and resource-matched experiments
DNAU-24 → EVOU-19 : prerequisite for Baselines, oracles and resource-matched experiments
DNAU-36 → EVOU-19 : prerequisite for Baselines, oracles and resource-matched experiments
EVOU-01 → EVOU-20 : prerequisite for Regulation, expression and different timescales
EVOU-10 → EVOU-20 : prerequisite for Regulation, expression and different timescales
EVOU-19 → EVOU-20 : prerequisite for Regulation, expression and different timescales
DNAU-13 → EVOU-20 : prerequisite for Regulation, expression and different timescales
DNAU-32 → EVOU-20 : prerequisite for Regulation, expression and different timescales
EVOU-15 → EVOU-21 : prerequisite for Analogies that can fail
EVOU-16 → EVOU-21 : prerequisite for Analogies that can fail
EVOU-18 → EVOU-21 : prerequisite for Analogies that can fail
EVOU-19 → EVOU-21 : prerequisite for Analogies that can fail
EVOU-20 → EVOU-21 : prerequisite for Analogies that can fail
DNAU-32 → EVOU-21 : prerequisite for Analogies that can fail
DNAU-36 → EVOU-21 : prerequisite for Analogies that can fail
EVOU-06 → EVOU-22 : prerequisite for Learning parameters and changing structure
EVOU-19 → EVOU-22 : prerequisite for Learning parameters and changing structure
EVOU-21 → EVOU-22 : prerequisite for Learning parameters and changing structure
DNAU-05 → EVOU-22 : prerequisite for Learning parameters and changing structure
DNAU-06 → EVOU-22 : prerequisite for Learning parameters and changing structure
DNAU-32 → EVOU-22 : prerequisite for Learning parameters and changing structure
EVOU-17 → EVOU-23 : prerequisite for Development as building a representation
EVOU-21 → EVOU-23 : prerequisite for Development as building a representation
EVOU-22 → EVOU-23 : prerequisite for Development as building a representation
DNAU-25 → EVOU-23 : prerequisite for Development as building a representation
DNAU-31 → EVOU-23 : prerequisite for Development as building a representation
DNAU-32 → EVOU-23 : prerequisite for Development as building a representation
EVOU-19 → EVOU-24 : prerequisite for A minimal genomic-computation hypothesis
EVOU-20 → EVOU-24 : prerequisite for A minimal genomic-computation hypothesis
EVOU-21 → EVOU-24 : prerequisite for A minimal genomic-computation hypothesis
EVOU-22 → EVOU-24 : prerequisite for A minimal genomic-computation hypothesis
EVOU-23 → EVOU-24 : prerequisite for A minimal genomic-computation hypothesis
DNAU-25 → EVOU-24 : prerequisite for A minimal genomic-computation hypothesis
DNAU-32 → EVOU-24 : prerequisite for A minimal genomic-computation hypothesis
DNAU-35 → EVOU-24 : prerequisite for A minimal genomic-computation hypothesis
EVOU-17 → EVOU-25 : prerequisite for Classes, interfaces and a UML model
EVOU-24 → EVOU-25 : prerequisite for Classes, interfaces and a UML model
DNAU-03 → EVOU-25 : prerequisite for Classes, interfaces and a UML model
EVOU-18 → EVOU-26 : prerequisite for From a request to an expression trace
EVOU-25 → EVOU-26 : prerequisite for From a request to an expression trace
DNAU-03 → EVOU-26 : prerequisite for From a request to an expression trace
EVOU-06 → EVOU-27 : prerequisite for Traces, credit and explanations
EVOU-19 → EVOU-27 : prerequisite for Traces, credit and explanations
EVOU-26 → EVOU-27 : prerequisite for Traces, credit and explanations
DNAU-12 → EVOU-27 : prerequisite for Traces, credit and explanations
DNAU-36 → EVOU-27 : prerequisite for Traces, credit and explanations
EVOU-22 → EVOU-28 : prerequisite for Structural proposals and their lifecycle
EVOU-25 → EVOU-28 : prerequisite for Structural proposals and their lifecycle
EVOU-27 → EVOU-28 : prerequisite for Structural proposals and their lifecycle
DNAU-06 → EVOU-28 : prerequisite for Structural proposals and their lifecycle
DNAU-32 → EVOU-28 : prerequisite for Structural proposals and their lifecycle
EVOU-08 → EVOU-29 : prerequisite for Training a candidate Evolutor model
EVOU-19 → EVOU-29 : prerequisite for Training a candidate Evolutor model
EVOU-24 → EVOU-29 : prerequisite for Training a candidate Evolutor model
EVOU-27 → EVOU-29 : prerequisite for Training a candidate Evolutor model
EVOU-28 → EVOU-29 : prerequisite for Training a candidate Evolutor model
DNAU-34 → EVOU-29 : prerequisite for Training a candidate Evolutor model
DNAU-36 → EVOU-29 : prerequisite for Training a candidate Evolutor model
EVOU-17 → EVOU-30 : prerequisite for An inference runtime with clear boundaries
EVOU-26 → EVOU-30 : prerequisite for An inference runtime with clear boundaries
EVOU-29 → EVOU-30 : prerequisite for An inference runtime with clear boundaries
DNAU-03 → EVOU-30 : prerequisite for An inference runtime with clear boundaries
DNAU-35 → EVOU-30 : prerequisite for An inference runtime with clear boundaries
EVOU-29 → EVOU-31 : prerequisite for Model identity, formats and checkpoints
EVOU-30 → EVOU-31 : prerequisite for Model identity, formats and checkpoints
DNAU-33 → EVOU-31 : prerequisite for Model identity, formats and checkpoints
DNAU-35 → EVOU-31 : prerequisite for Model identity, formats and checkpoints
EVOU-14 → EVOU-32 : prerequisite for Managing recurrent state, KV and external memory
EVOU-18 → EVOU-32 : prerequisite for Managing recurrent state, KV and external memory
EVOU-30 → EVOU-32 : prerequisite for Managing recurrent state, KV and external memory
EVOU-31 → EVOU-32 : prerequisite for Managing recurrent state, KV and external memory
DNAU-35 → EVOU-32 : prerequisite for Managing recurrent state, KV and external memory
EVOU-18 → EVOU-33 : prerequisite for Batching, queues and latency
EVOU-32 → EVOU-33 : prerequisite for Batching, queues and latency
DNAU-12 → EVOU-33 : prerequisite for Batching, queues and latency
DNAU-35 → EVOU-33 : prerequisite for Batching, queues and latency
EVOU-19 → EVOU-34 : prerequisite for Parity, profiling and optimization
EVOU-30 → EVOU-34 : prerequisite for Parity, profiling and optimization
EVOU-32 → EVOU-34 : prerequisite for Parity, profiling and optimization
EVOU-33 → EVOU-34 : prerequisite for Parity, profiling and optimization
DNAU-35 → EVOU-34 : prerequisite for Parity, profiling and optimization
DNAU-36 → EVOU-34 : prerequisite for Parity, profiling and optimization
EVOU-28 → EVOU-35 : prerequisite for Serving, observability and safe rollback
EVOU-31 → EVOU-35 : prerequisite for Serving, observability and safe rollback
EVOU-33 → EVOU-35 : prerequisite for Serving, observability and safe rollback
EVOU-34 → EVOU-35 : prerequisite for Serving, observability and safe rollback
DNAU-35 → EVOU-35 : prerequisite for Serving, observability and safe rollback
EVOU-29 → EVOU-36 : prerequisite for Failed ideas as a source of knowledge
EVOU-34 → EVOU-36 : prerequisite for Failed ideas as a source of knowledge
EVOU-35 → EVOU-36 : prerequisite for Failed ideas as a source of knowledge
DNAU-12 → EVOU-36 : prerequisite for Failed ideas as a source of knowledge
DNAU-36 → EVOU-36 : prerequisite for Failed ideas as a source of knowledge
EVOU-11 → EVOU-37 : prerequisite for DNA sequence models: DOGMA and Hermon DNA as questions
EVOU-13 → EVOU-37 : prerequisite for DNA sequence models: DOGMA and Hermon DNA as questions
EVOU-29 → EVOU-37 : prerequisite for DNA sequence models: DOGMA and Hermon DNA as questions
EVOU-31 → EVOU-37 : prerequisite for DNA sequence models: DOGMA and Hermon DNA as questions
EVOU-36 → EVOU-37 : prerequisite for DNA sequence models: DOGMA and Hermon DNA as questions
DNAU-11 → EVOU-37 : prerequisite for DNA sequence models: DOGMA and Hermon DNA as questions
DNAU-34 → EVOU-37 : prerequisite for DNA sequence models: DOGMA and Hermon DNA as questions
DNAU-36 → EVOU-37 : prerequisite for DNA sequence models: DOGMA and Hermon DNA as questions
EVOU-22 → EVOU-38 : prerequisite for Transfer, continual learning and populations
EVOU-28 → EVOU-38 : prerequisite for Transfer, continual learning and populations
EVOU-36 → EVOU-38 : prerequisite for Transfer, continual learning and populations
EVOU-37 → EVOU-38 : prerequisite for Transfer, continual learning and populations
DNAU-12 → EVOU-38 : prerequisite for Transfer, continual learning and populations
DNAU-32 → EVOU-38 : prerequisite for Transfer, continual learning and populations
DNAU-36 → EVOU-38 : prerequisite for Transfer, continual learning and populations
EVOU-19 → EVOU-39 : prerequisite for AGI claims and an operational scorecard
EVOU-36 → EVOU-39 : prerequisite for AGI claims and an operational scorecard
EVOU-38 → EVOU-39 : prerequisite for AGI claims and an operational scorecard
DNAU-36 → EVOU-39 : prerequisite for AGI claims and an operational scorecard
EVOU-24 → EVOU-40 : prerequisite for Capstone: a reproducible research-engineering argument
EVOU-35 → EVOU-40 : prerequisite for Capstone: a reproducible research-engineering argument
EVOU-36 → EVOU-40 : prerequisite for Capstone: a reproducible research-engineering argument
EVOU-37 → EVOU-40 : prerequisite for Capstone: a reproducible research-engineering argument
EVOU-38 → EVOU-40 : prerequisite for Capstone: a reproducible research-engineering argument
EVOU-39 → EVOU-40 : prerequisite for Capstone: a reproducible research-engineering argument
DNAU-36 → EVOU-40 : prerequisite for Capstone: a reproducible research-engineering argument
```

## Cross-book handoff

The versioned [Book I exit contract](pedagogy/book-i-contract.json) lists chapter-specific terms and exit tasks. Evolutor imports only those explicit chapter outcomes, and recalls them in a short bridge before use. Its present status is planned-not-yet-taught. Neither unit tests nor this graph activate that contract. If an imported outcome is removed, either restore it in Book I or teach it locally before use in Book II.
