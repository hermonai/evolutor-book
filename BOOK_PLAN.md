# Evolutor: deep technical edition

Status: canonical deep Chapter 1 is an internally reviewed prototype; all later chapters remain plans. The undergraduate edition is frozen. No trained model, engine or wet-lab result is delivered. See [production report](DEEP_CHAPTER_1_REPORT.md) and [edition strategy](CANONICAL_EDITION_STRATEGY.md).

DOGMA = non-Transformer DNA-native model + DOGMA Engine; Hermon DNA = Transformer-based DNA model + Hermon DNA Engine; Evolutor = broader genomic computation theory, research and eventual runtime above both.

## Macro table of contents

### I · The research question

1. **Why Genomic Computation?** (EVOD-01). programs; neural models; genomes; stored and expressed computation; development; adaptation.

### II · Learning and sequence-model foundations

2. **Learning objectives, data and evaluation** (EVOD-02). prediction; likelihood; splits; uncertainty; controls; capacity.

3. **Differentiation, optimization and tensor programs** (EVOD-03). tensor shapes; gradients; autograd; optimization; numerical precision.

4. **Reproducible PyTorch training** (EVOD-04). datasets; batching; masking; optimizer; checkpoints; seeds.

5. **Tokenization and sequence representation** (EVOD-05). DNA tokens; k-mers; embeddings; positions; strand orientation.

6. **Recurrent models and gated state** (EVOD-06). RNN; LSTM; GRU; state transition; retention; gradients.

7. **State-space models, selective updates and scans** (EVOD-07). linear recurrence; S4/S5; selective SSM; Mamba; RWKV; chunking.

8. **Attention and content-addressed computation** (EVOD-08). Q/K/V; scores; masks; heads; softmax; retrieval.

9. **Transformers and cached execution** (EVOD-09). residuals; normalization; MLP; positions; blocks; KV; prefill; decode.

10. **Conditional computation and memory alternatives** (EVOD-10). dispatch; MoE; retrieval; external memory; dynamic graphs; hybrid models.

### III · From biology to formal computational hypotheses

11. **Regulation and expression across levels** (EVOD-11). biological regulation; stored modules; selection; execution; context.

12. **Development and generated computational structure** (EVOD-12). genotype/phenotype; developmental encoding; compilation; program synthesis; NAS.

13. **Learning, structural adaptation and evolution** (EVOD-13). state change; parameter learning; structural learning; populations; selection.

14. **Typed genomic computation systems** (EVOD-14). alphabet; computational gene; genome; regulator; expression; state; trace.

15. **Operational semantics and expression traces** (EVOD-15). configuration; transition; evaluation rule; effects; termination; trace.

16. **Expression complexity and resource semantics** (EVOD-16). stored size; routing; active work; state; communication; trace; adaptation.

17. **Traces, credit and mechanistic evidence** (EVOD-17). logging; causal interventions; credit assignment; structural proposals.

### IV · DOGMA: non-Transformer DNA-native computation

18. **DOGMA primitives and state semantics** (EVOD-18). State; Regulator; Expression; Strand; Complement; Gate; Memory locus; Module; Trace.

19. **DOGMA regulation and selective transformations** (EVOD-19). regulation; expression; conditional state update; routing; ablation.

20. **Structured memory, locality and timescales** (EVOD-20). local/global state; modular memory; regulatory state; fast/slow state; capacity.

21. **Strands, complements and dual-state hypotheses** (EVOD-21). paired states; reverse complement; equivariance; causal streaming.

22. **DOGMA reference model and falsifiable research program** (EVOD-22). reference implementation; state trace; objective; baseline; ablation; negative evidence.

### V · Hermon DNA: Transformer-based DNA computation

23. **Hermon DNA reference architecture** (EVOD-23). DNA tokenizer; Transformer blocks; output head; causal positions.

24. **DNA-aware Transformer mechanisms** (EVOD-24). strand embeddings; motifs; k-mers; multi-scale positions; sparse/long context; retrieval.

### VI · Training systems and fair experiments

25. **Shared experiments without false equivalence** (EVOD-25). data contracts; model interfaces; state types; losses; benchmarks.

26. **Training/inference parity and parallel recurrence** (EVOD-26). sequential; chunked; scan; full sequence; incremental; gradients.

27. **Optimization and memory-efficient training** (EVOD-27). mixed precision; accumulation; checkpointing; optimizer state; stability.

28. **Distributed training and model artifacts** (EVOD-28). data/tensor/pipeline parallelism; communication; sharding; formats; provenance.

29. **Benchmark design and comparative evidence** (EVOD-29). oracles; budgets; multi-seed evaluation; capacity controls; causality; transplant tests.

### VII · DOGMA Engine: state-native inference

30. **Runtime contracts and request lifecycles** (EVOD-30). request; model identity; state ownership; cancellation; streaming; errors.

31. **DOGMA state construction and execution** (EVOD-31). prompt ingestion; native step; chunking; output head; state tracing.

32. **DOGMA state pools and memory ownership** (EVOD-32). allocation; reset; reuse; clone; isolation; temporary buffers.

33. **DOGMA checkpoints, branching and prefix state** (EVOD-33). checkpoint; restore; state clone; versioning; shared prefixes.

34. **DOGMA batching and state-native kernels** (EVOD-34). state-transition batching; scheduling; scans; locality; kernel profiling.

### VIII · Hermon DNA Engine: attention-native inference

35. **Hermon DNA prefill, decode and KV state** (EVOD-35). prefill; decode; cache layout; positions; memory growth.

36. **Paged KV, prefix sharing and allocation** (EVOD-36). pages; blocks; fragmentation; prefix cache; reference counting; eviction.

37. **Continuous batching and precision** (EVOD-37). admission; prefill/decode scheduling; quantization; quality; tails.

38. **Speculative decoding and attention kernels** (EVOD-38). draft/verify; acceptance; numerical parity; memory traffic; fused kernels.

### IX · Evolutor: heterogeneous execution

39. **Evolutor runtime above both engines** (EVOD-39). planner; router; adapters; tools; retrieval; symbolic modules; trace.

40. **Hybrid compressed and addressable memory** (EVOD-40). compression; addressability; forgetting; retrieval; memory routing.

41. **Compiler, IR and execution planning** (EVOD-41). IR; typing; optimization; lowering; backend legality; cost model.

42. **Database engines as a systems comparison** (EVOD-42). parser; logical plan; optimizer; physical operators; buffer pool; transactions.

43. **Structural adaptation and lifecycle governance** (EVOD-43). proposals; validation; evaluation; promotion; rollback; lineage.

### X · Industrial engineering

44. **Packaging, deployment and observable services** (EVOD-44). versioning; APIs; tracing; metrics; streaming; fault handling; rollback.

45. **Multi-tenancy, isolation and security** (EVOD-45). ownership; quotas; untrusted inputs; tool authority; state leakage; threat model.

46. **Distributed serving and state placement** (EVOD-46). replication; partitioning; tensor/pipeline parallelism; sharding; migration.

47. **Profiling, performance and hardware backends** (EVOD-47). TTFT; ITL; throughput; memory; power; utilization; roofline intuition.

### XI · Applications and capability research

48. **Genomic sequence applications** (EVOD-48). regulatory sequence analysis; motifs; long context; strand symmetry; uncertainty.

49. **Streaming, language, code and persistent agents** (EVOD-49). statistics; retrieval; copying; code; tools; persistent state; planning.

50. **Continual learning and population adaptation** (EVOD-50). transfer; forgetting; structural search; populations; open-ended learning.

51. **AGI capability hypotheses and limits** (EVOD-51). reasoning; planning; world models; transfer; tools; self-modification; generalization.

### XII · Research synthesis

52. **Failures, open problems and reproducible synthesis** (EVOD-52). failed mechanisms; causality leaks; capacity confounds; negative results; historical lineage.

52 substantial chapters; counts follow coherent arguments rather than fixed page or lecture quotas. Chapter 1 previews the field; later chapters reconstruct mechanisms and proofs in depth. See DEEP_REDESIGN.md for assumed knowledge and reading routes.
