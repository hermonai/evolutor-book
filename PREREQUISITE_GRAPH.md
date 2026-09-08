# Evolutor: deep technical edition

Status: canonical deep Chapters 1–2 are internally reviewed development manuscripts; Chapter 3 onward remains planned. Prior editions and the Chapter 1-only PDF are preserved. No new wet-lab result, trained model or engine benchmark is delivered. See [Chapter 2 production report](DEEP_CHAPTER_2_REPORT.md).

DOGMA = non-Transformer DNA-native model + DOGMA Engine; Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; Evolutor = broader genomic computation theory, research and eventual runtime above both.

## Semantic TXT prerequisite graph

A → B means that A supplies knowledge required by B; all incoming edges are required. It is not a molecular causal arrow. ENTRY is the explicit technical entry contract. Chapter 1 roadmaps preview later material without requiring it. DNAD imports are one-way from Book I; no reverse dependencies exist.

DNAD-30 → EVOD-01 : prerequisite for Why Genomic Computation?

DNAD-32 → EVOD-01 : prerequisite for Why Genomic Computation?

EVOD-01 → EVOD-02 : prerequisite for Learning objectives, data, tasks, and evaluation

EVOD-02 → EVOD-03 : prerequisite for Differentiation, optimization and tensor programs

EVOD-02 → EVOD-04 : prerequisite for Reproducible PyTorch training

EVOD-03 → EVOD-04 : prerequisite for Reproducible PyTorch training

EVOD-02 → EVOD-05 : prerequisite for Tokenization and sequence representation

EVOD-04 → EVOD-05 : prerequisite for Tokenization and sequence representation

DNAD-05 → EVOD-05 : prerequisite for Tokenization and sequence representation

DNAD-25 → EVOD-05 : prerequisite for Tokenization and sequence representation

EVOD-03 → EVOD-06 : prerequisite for Recurrent models and gated state

EVOD-05 → EVOD-06 : prerequisite for Recurrent models and gated state

EVOD-06 → EVOD-07 : prerequisite for State-space models, selective updates and scans

EVOD-03 → EVOD-08 : prerequisite for Attention and content-addressed computation

EVOD-05 → EVOD-08 : prerequisite for Attention and content-addressed computation

EVOD-04 → EVOD-09 : prerequisite for Transformers and cached execution

EVOD-08 → EVOD-09 : prerequisite for Transformers and cached execution

EVOD-06 → EVOD-10 : prerequisite for Conditional computation and memory alternatives

EVOD-07 → EVOD-10 : prerequisite for Conditional computation and memory alternatives

EVOD-09 → EVOD-10 : prerequisite for Conditional computation and memory alternatives

EVOD-01 → EVOD-11 : prerequisite for Regulation and expression across levels

EVOD-10 → EVOD-11 : prerequisite for Regulation and expression across levels

DNAD-30 → EVOD-11 : prerequisite for Regulation and expression across levels

EVOD-10 → EVOD-12 : prerequisite for Development and generated computational structure

EVOD-11 → EVOD-12 : prerequisite for Development and generated computational structure

DNAD-30 → EVOD-12 : prerequisite for Development and generated computational structure

EVOD-04 → EVOD-13 : prerequisite for Learning, structural adaptation and evolution

EVOD-11 → EVOD-13 : prerequisite for Learning, structural adaptation and evolution

EVOD-12 → EVOD-13 : prerequisite for Learning, structural adaptation and evolution

DNAD-30 → EVOD-13 : prerequisite for Learning, structural adaptation and evolution

EVOD-10 → EVOD-14 : prerequisite for Typed genomic computation systems

EVOD-11 → EVOD-14 : prerequisite for Typed genomic computation systems

EVOD-12 → EVOD-14 : prerequisite for Typed genomic computation systems

EVOD-13 → EVOD-14 : prerequisite for Typed genomic computation systems

DNAD-16 → EVOD-14 : prerequisite for Typed genomic computation systems

DNAD-18 → EVOD-14 : prerequisite for Typed genomic computation systems

DNAD-32 → EVOD-14 : prerequisite for Typed genomic computation systems

EVOD-14 → EVOD-15 : prerequisite for Operational semantics and expression traces

EVOD-07 → EVOD-16 : prerequisite for Expression complexity and resource semantics

EVOD-09 → EVOD-16 : prerequisite for Expression complexity and resource semantics

EVOD-15 → EVOD-16 : prerequisite for Expression complexity and resource semantics

DNAD-04 → EVOD-16 : prerequisite for Expression complexity and resource semantics

DNAD-24 → EVOD-16 : prerequisite for Expression complexity and resource semantics

EVOD-13 → EVOD-17 : prerequisite for Traces, credit and mechanistic evidence

EVOD-15 → EVOD-17 : prerequisite for Traces, credit and mechanistic evidence

EVOD-16 → EVOD-17 : prerequisite for Traces, credit and mechanistic evidence

EVOD-07 → EVOD-18 : prerequisite for DOGMA primitives and state semantics

EVOD-14 → EVOD-18 : prerequisite for DOGMA primitives and state semantics

EVOD-15 → EVOD-18 : prerequisite for DOGMA primitives and state semantics

EVOD-16 → EVOD-18 : prerequisite for DOGMA primitives and state semantics

EVOD-10 → EVOD-19 : prerequisite for DOGMA regulation and selective transformations

EVOD-17 → EVOD-19 : prerequisite for DOGMA regulation and selective transformations

EVOD-18 → EVOD-19 : prerequisite for DOGMA regulation and selective transformations

EVOD-07 → EVOD-20 : prerequisite for Structured memory, locality and timescales

EVOD-16 → EVOD-20 : prerequisite for Structured memory, locality and timescales

EVOD-18 → EVOD-20 : prerequisite for Structured memory, locality and timescales

EVOD-19 → EVOD-20 : prerequisite for Structured memory, locality and timescales

EVOD-05 → EVOD-21 : prerequisite for Strands, complements and dual-state hypotheses

EVOD-18 → EVOD-21 : prerequisite for Strands, complements and dual-state hypotheses

EVOD-20 → EVOD-21 : prerequisite for Strands, complements and dual-state hypotheses

DNAD-05 → EVOD-21 : prerequisite for Strands, complements and dual-state hypotheses

DNAD-30 → EVOD-21 : prerequisite for Strands, complements and dual-state hypotheses

EVOD-04 → EVOD-22 : prerequisite for DOGMA reference model and falsifiable research program

EVOD-17 → EVOD-22 : prerequisite for DOGMA reference model and falsifiable research program

EVOD-19 → EVOD-22 : prerequisite for DOGMA reference model and falsifiable research program

EVOD-20 → EVOD-22 : prerequisite for DOGMA reference model and falsifiable research program

EVOD-21 → EVOD-22 : prerequisite for DOGMA reference model and falsifiable research program

EVOD-05 → EVOD-23 : prerequisite for Hermon DNA reference architecture

EVOD-09 → EVOD-23 : prerequisite for Hermon DNA reference architecture

EVOD-16 → EVOD-23 : prerequisite for Hermon DNA reference architecture

EVOD-10 → EVOD-24 : prerequisite for DNA-aware Transformer mechanisms

EVOD-21 → EVOD-24 : prerequisite for DNA-aware Transformer mechanisms

EVOD-23 → EVOD-24 : prerequisite for DNA-aware Transformer mechanisms

DNAD-25 → EVOD-24 : prerequisite for DNA-aware Transformer mechanisms

DNAD-30 → EVOD-24 : prerequisite for DNA-aware Transformer mechanisms

EVOD-04 → EVOD-25 : prerequisite for Shared experiments without false equivalence

EVOD-22 → EVOD-25 : prerequisite for Shared experiments without false equivalence

EVOD-23 → EVOD-25 : prerequisite for Shared experiments without false equivalence

EVOD-24 → EVOD-25 : prerequisite for Shared experiments without false equivalence

EVOD-07 → EVOD-26 : prerequisite for Training/inference parity and parallel recurrence

EVOD-09 → EVOD-26 : prerequisite for Training/inference parity and parallel recurrence

EVOD-22 → EVOD-26 : prerequisite for Training/inference parity and parallel recurrence

EVOD-23 → EVOD-26 : prerequisite for Training/inference parity and parallel recurrence

EVOD-25 → EVOD-26 : prerequisite for Training/inference parity and parallel recurrence

EVOD-03 → EVOD-27 : prerequisite for Optimization and memory-efficient training

EVOD-04 → EVOD-27 : prerequisite for Optimization and memory-efficient training

EVOD-25 → EVOD-27 : prerequisite for Optimization and memory-efficient training

EVOD-26 → EVOD-27 : prerequisite for Optimization and memory-efficient training

EVOD-25 → EVOD-28 : prerequisite for Distributed training and model artifacts

EVOD-26 → EVOD-28 : prerequisite for Distributed training and model artifacts

EVOD-27 → EVOD-28 : prerequisite for Distributed training and model artifacts

EVOD-16 → EVOD-29 : prerequisite for Benchmark design and comparative evidence

EVOD-17 → EVOD-29 : prerequisite for Benchmark design and comparative evidence

EVOD-22 → EVOD-29 : prerequisite for Benchmark design and comparative evidence

EVOD-24 → EVOD-29 : prerequisite for Benchmark design and comparative evidence

EVOD-26 → EVOD-29 : prerequisite for Benchmark design and comparative evidence

EVOD-27 → EVOD-29 : prerequisite for Benchmark design and comparative evidence

EVOD-15 → EVOD-30 : prerequisite for Runtime contracts and request lifecycles

EVOD-25 → EVOD-30 : prerequisite for Runtime contracts and request lifecycles

EVOD-26 → EVOD-30 : prerequisite for Runtime contracts and request lifecycles

EVOD-28 → EVOD-30 : prerequisite for Runtime contracts and request lifecycles

EVOD-18 → EVOD-31 : prerequisite for DOGMA state construction and execution

EVOD-22 → EVOD-31 : prerequisite for DOGMA state construction and execution

EVOD-26 → EVOD-31 : prerequisite for DOGMA state construction and execution

EVOD-30 → EVOD-31 : prerequisite for DOGMA state construction and execution

EVOD-20 → EVOD-32 : prerequisite for DOGMA state pools and memory ownership

EVOD-28 → EVOD-32 : prerequisite for DOGMA state pools and memory ownership

EVOD-30 → EVOD-32 : prerequisite for DOGMA state pools and memory ownership

EVOD-31 → EVOD-32 : prerequisite for DOGMA state pools and memory ownership

EVOD-28 → EVOD-33 : prerequisite for DOGMA checkpoints, branching and prefix state

EVOD-31 → EVOD-33 : prerequisite for DOGMA checkpoints, branching and prefix state

EVOD-32 → EVOD-33 : prerequisite for DOGMA checkpoints, branching and prefix state

EVOD-07 → EVOD-34 : prerequisite for DOGMA batching and state-native kernels

EVOD-26 → EVOD-34 : prerequisite for DOGMA batching and state-native kernels

EVOD-31 → EVOD-34 : prerequisite for DOGMA batching and state-native kernels

EVOD-32 → EVOD-34 : prerequisite for DOGMA batching and state-native kernels

EVOD-33 → EVOD-34 : prerequisite for DOGMA batching and state-native kernels

EVOD-09 → EVOD-35 : prerequisite for Hermon DNA prefill, decode and KV state

EVOD-23 → EVOD-35 : prerequisite for Hermon DNA prefill, decode and KV state

EVOD-26 → EVOD-35 : prerequisite for Hermon DNA prefill, decode and KV state

EVOD-30 → EVOD-35 : prerequisite for Hermon DNA prefill, decode and KV state

EVOD-28 → EVOD-36 : prerequisite for Paged KV, prefix sharing and allocation

EVOD-30 → EVOD-36 : prerequisite for Paged KV, prefix sharing and allocation

EVOD-35 → EVOD-36 : prerequisite for Paged KV, prefix sharing and allocation

EVOD-27 → EVOD-37 : prerequisite for Continuous batching and precision

EVOD-29 → EVOD-37 : prerequisite for Continuous batching and precision

EVOD-35 → EVOD-37 : prerequisite for Continuous batching and precision

EVOD-36 → EVOD-37 : prerequisite for Continuous batching and precision

EVOD-26 → EVOD-38 : prerequisite for Speculative decoding and attention kernels

EVOD-29 → EVOD-38 : prerequisite for Speculative decoding and attention kernels

EVOD-35 → EVOD-38 : prerequisite for Speculative decoding and attention kernels

EVOD-37 → EVOD-38 : prerequisite for Speculative decoding and attention kernels

EVOD-14 → EVOD-39 : prerequisite for Evolutor runtime above both engines

EVOD-15 → EVOD-39 : prerequisite for Evolutor runtime above both engines

EVOD-30 → EVOD-39 : prerequisite for Evolutor runtime above both engines

EVOD-34 → EVOD-39 : prerequisite for Evolutor runtime above both engines

EVOD-38 → EVOD-39 : prerequisite for Evolutor runtime above both engines

EVOD-10 → EVOD-40 : prerequisite for Hybrid compressed and addressable memory

EVOD-16 → EVOD-40 : prerequisite for Hybrid compressed and addressable memory

EVOD-20 → EVOD-40 : prerequisite for Hybrid compressed and addressable memory

EVOD-29 → EVOD-40 : prerequisite for Hybrid compressed and addressable memory

EVOD-33 → EVOD-40 : prerequisite for Hybrid compressed and addressable memory

EVOD-36 → EVOD-40 : prerequisite for Hybrid compressed and addressable memory

EVOD-39 → EVOD-40 : prerequisite for Hybrid compressed and addressable memory

EVOD-12 → EVOD-41 : prerequisite for Compiler, IR and execution planning

EVOD-14 → EVOD-41 : prerequisite for Compiler, IR and execution planning

EVOD-15 → EVOD-41 : prerequisite for Compiler, IR and execution planning

EVOD-16 → EVOD-41 : prerequisite for Compiler, IR and execution planning

EVOD-39 → EVOD-41 : prerequisite for Compiler, IR and execution planning

EVOD-10 → EVOD-42 : prerequisite for Database engines as a systems comparison

EVOD-16 → EVOD-42 : prerequisite for Database engines as a systems comparison

EVOD-30 → EVOD-42 : prerequisite for Database engines as a systems comparison

EVOD-39 → EVOD-42 : prerequisite for Database engines as a systems comparison

EVOD-41 → EVOD-42 : prerequisite for Database engines as a systems comparison

EVOD-13 → EVOD-43 : prerequisite for Structural adaptation and lifecycle governance

EVOD-17 → EVOD-43 : prerequisite for Structural adaptation and lifecycle governance

EVOD-29 → EVOD-43 : prerequisite for Structural adaptation and lifecycle governance

EVOD-39 → EVOD-43 : prerequisite for Structural adaptation and lifecycle governance

EVOD-41 → EVOD-43 : prerequisite for Structural adaptation and lifecycle governance

EVOD-28 → EVOD-44 : prerequisite for Packaging, deployment and observable services

EVOD-30 → EVOD-44 : prerequisite for Packaging, deployment and observable services

EVOD-39 → EVOD-44 : prerequisite for Packaging, deployment and observable services

EVOD-43 → EVOD-44 : prerequisite for Packaging, deployment and observable services

EVOD-32 → EVOD-45 : prerequisite for Multi-tenancy, isolation and security

EVOD-36 → EVOD-45 : prerequisite for Multi-tenancy, isolation and security

EVOD-39 → EVOD-45 : prerequisite for Multi-tenancy, isolation and security

EVOD-44 → EVOD-45 : prerequisite for Multi-tenancy, isolation and security

EVOD-28 → EVOD-46 : prerequisite for Distributed serving and state placement

EVOD-34 → EVOD-46 : prerequisite for Distributed serving and state placement

EVOD-38 → EVOD-46 : prerequisite for Distributed serving and state placement

EVOD-39 → EVOD-46 : prerequisite for Distributed serving and state placement

EVOD-44 → EVOD-46 : prerequisite for Distributed serving and state placement

EVOD-45 → EVOD-46 : prerequisite for Distributed serving and state placement

EVOD-29 → EVOD-47 : prerequisite for Profiling, performance and hardware backends

EVOD-34 → EVOD-47 : prerequisite for Profiling, performance and hardware backends

EVOD-38 → EVOD-47 : prerequisite for Profiling, performance and hardware backends

EVOD-44 → EVOD-47 : prerequisite for Profiling, performance and hardware backends

EVOD-46 → EVOD-47 : prerequisite for Profiling, performance and hardware backends

EVOD-24 → EVOD-48 : prerequisite for Genomic sequence applications

EVOD-29 → EVOD-48 : prerequisite for Genomic sequence applications

EVOD-40 → EVOD-48 : prerequisite for Genomic sequence applications

EVOD-44 → EVOD-48 : prerequisite for Genomic sequence applications

EVOD-47 → EVOD-48 : prerequisite for Genomic sequence applications

DNAD-25 → EVOD-48 : prerequisite for Genomic sequence applications

DNAD-26 → EVOD-48 : prerequisite for Genomic sequence applications

DNAD-30 → EVOD-48 : prerequisite for Genomic sequence applications

DNAD-31 → EVOD-48 : prerequisite for Genomic sequence applications

EVOD-29 → EVOD-49 : prerequisite for Streaming, language, code and persistent agents

EVOD-33 → EVOD-49 : prerequisite for Streaming, language, code and persistent agents

EVOD-40 → EVOD-49 : prerequisite for Streaming, language, code and persistent agents

EVOD-45 → EVOD-49 : prerequisite for Streaming, language, code and persistent agents

EVOD-47 → EVOD-49 : prerequisite for Streaming, language, code and persistent agents

EVOD-13 → EVOD-50 : prerequisite for Continual learning and population adaptation

EVOD-29 → EVOD-50 : prerequisite for Continual learning and population adaptation

EVOD-40 → EVOD-50 : prerequisite for Continual learning and population adaptation

EVOD-43 → EVOD-50 : prerequisite for Continual learning and population adaptation

EVOD-49 → EVOD-50 : prerequisite for Continual learning and population adaptation

EVOD-29 → EVOD-51 : prerequisite for AGI capability hypotheses and limits

EVOD-43 → EVOD-51 : prerequisite for AGI capability hypotheses and limits

EVOD-48 → EVOD-51 : prerequisite for AGI capability hypotheses and limits

EVOD-49 → EVOD-51 : prerequisite for AGI capability hypotheses and limits

EVOD-50 → EVOD-51 : prerequisite for AGI capability hypotheses and limits

EVOD-29 → EVOD-52 : prerequisite for Failures, open problems and reproducible synthesis

EVOD-43 → EVOD-52 : prerequisite for Failures, open problems and reproducible synthesis

EVOD-47 → EVOD-52 : prerequisite for Failures, open problems and reproducible synthesis

EVOD-48 → EVOD-52 : prerequisite for Failures, open problems and reproducible synthesis

EVOD-49 → EVOD-52 : prerequisite for Failures, open problems and reproducible synthesis

EVOD-50 → EVOD-52 : prerequisite for Failures, open problems and reproducible synthesis

EVOD-51 → EVOD-52 : prerequisite for Failures, open problems and reproducible synthesis

The [deep Book I contract](pedagogy/deep-book-i-contract.json) contains exact exit tasks. A planned link does not establish that a chapter has been taught. Qualified readers may demonstrate equivalent knowledge; otherwise follow the named chapters.
