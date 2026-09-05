# Industrial roadmap

Model semantics, reference implementation, optimized backend and serving system are distinct artifacts.

1. **Reproducible laboratory:** stable task/model interfaces, immutable configuration, checkpoint format and honest error reporting.
2. **Candidate interpreter:** typed operations, explicit effect permissions, deterministic trace schema and costed planning. First compare ordinary dispatch or workflow orchestration.
3. **Parity contract:** full-sequence and incremental outputs/state, defined precision tolerances, versioned state migration.
4. **Measured engine:** profile a real workload; optimize the limiting memory/kernel/scheduler path. KV, recurrent and external memory need different managers.
5. **Serving:** admission control, cancellation, batching, isolation, observability, persistence, fault recovery and rollback.
6. **Structural updates:** propose → simulate → verify → evaluate → accept/reject. Store architecture, parameters, optimizer, memory schema, module versions and provenance; never allow a raw model proposal to mutate production by default.

Industrial scorecard cells remain unmeasured: cost, latency, throughput, peak memory, scalability, deployment effort, observability, fault isolation, maintenance, security and hardware portability. A unified protocol or heterogeneous runtime is a candidate engineering architecture, not a validated research result. No new framework or exotic hardware before its workload and missing primitive are demonstrated.
