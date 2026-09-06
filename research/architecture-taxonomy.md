# Architecture taxonomy and historical lineage

Status: user-authorized target research taxonomy, 6 September 2026. No architecture, engine, training run, kernel or performance result is implemented by this amendment. Chapter 1 production continues separately.

## Target taxonomy

| Name | Level and architecture | Engine |
|---|---|---|
| Evolutor | Higher-level genomic computation theory, planning, research and eventual orchestration | Runtime above both engines |
| DOGMA | **Non-Transformer DNA-native** architecture family | DOGMA Engine |
| Hermon DNA | **Transformer-based DNA** architecture family | Hermon DNA Engine |

DOGMA is not merely an RNN with biological names, a Transformer without attention, absence of KV caching, or constant memory. Hermon DNA is not the non-Transformer line.

## Semantic TXT hierarchy

Evolutor research → DOGMA : investigates non-Transformer DNA-native computation
Evolutor research → Hermon DNA : investigates Transformer DNA computation
DOGMA → DOGMA Engine : candidate state semantics constrain implementation
Hermon DNA → Hermon DNA Engine : Transformer semantics constrain implementation
DOGMA Engine → Evolutor runtime : candidate integration
Hermon DNA Engine → Evolutor runtime : candidate integration
Evolutor runtime → shared serving and hardware : target orchestration, not deployed evidence

Arrows express design responsibility, not molecular reactions.

## Curriculum reconciliation

The 40 original EVOU IDs remain stable. Twenty-one new units EVOU-41 through EVOU-61 are inserted by prerequisite order, giving **61 teaching units in 14 parts**. IDs are not printed chapter numbers after EVOU-11. Chapter 1 and Chapter 2 retain their numbers and titles. This is a multi-course plan, not 61 equal lectures in one semester.

Existing foundations and previous-edition topic destinations remain. EVOU-37 now audits historical artifacts and comparative evidence after the two engine paths; it no longer leaves the target name mapping undecided. The [curriculum](../pedagogy/curriculum.json) is authoritative for order, prerequisite edges, vocabulary, storyboard frames, mathematics and experiments.

## DOGMA agenda

EVOU-41 teaches strong recurrent alternatives before DOGMA: finite-state machines, linear recurrence, RNN, LSTM, GRU, SSM, Mamba-like selective models, RWKV-like models, hybrids and valid scans. Each requires primary-paper/source review before drafting.

EVOU-42–46 investigate State, Regulator, Expression, Strand, Complement, Gate, Memory locus, Module and Trace only when each has a precise operation, nearest alternative, falsifier and ablation.

A candidate token transition transforms previous state into next state. Fix prediction timing: after consuming x_t, a next-token head may read s_(t+1). A head reading s_t is a different convention and must not silently claim to have consumed x_t. Regulation → expression → update is a candidate decomposition, not DOGMA's final definition. Compare gates, SSM selection, MoE routing, dispatch and dynamic execution; report equivalence honestly.

Modular working/regulatory/motif/structural memory, locality and fast/slow/structural timescales need explicit update, ownership and reset semantics. Dual-state or strand interactions are optional hypotheses, not forced metaphors. Full reverse-complement input may reveal future tokens: separate offline symmetry from causal streaming and compare augmentation/equivariant controls. Traces must show utility beyond ordinary activation logging; a log is not automatically a causal explanation. Indefinite ingestion does not imply perfect retention.

## Separate implementation gates

DOGMA semantics → PyTorch reference → state/logit/gradient tests → profiled runtime → native kernels
Hermon DNA mathematics → PyTorch reference → full/incremental KV parity → profiled engine → native kernels

Recurrence does not automatically forbid parallel training. Associative scans, convolution forms, blockwise updates and chunking are allowed only when mathematically valid and tested; state-dependent nonlinear selection can invalidate a proposed scan.

EVOU-49 plans shared data, training, inference, causality, evaluation and benchmarks with separate dogma and hermon_dna model packages. No package is claimed to exist yet. A prepare/step interface must declare logits versus sampled tokens and preserve family-specific opaque state.

## Two engine paths

DOGMA EVOU-51–54: prompt ingestion/state construction, native steps, independent state slots, allocation/reset/reuse/clone, checkpoint/restore, prefix-state cache and scheduling compatible state transitions. Do not impose KV or Transformer prefill terminology. Measure clone/restore costs. Separate weights, per-request state, temporary buffers, token history, external memory and trace storage; bounded carried state is not constant total memory.

Hermon DNA EVOU-47–48 and EVOU-55–57: tokenization, embeddings, shaped Q/K/V, masks, heads, feed-forward layers, residuals, normalization, positions, blocks and output head; then prefill, decode, appended K/V, actual cache layout, paging/fragmentation, prefix ownership, continuous batching and quantization. Derive cache costs from length, layers, KV heads, head dimension and precision. DNA-specific attention, strand embeddings, k-mers, motifs, positions, sparse/long-context and retrieval variants require strong Transformer controls.

EVOU-60 gates kernels on measured PyTorch bottlenecks and parity. Candidate DOGMA kernels include transition, selection, scan, regulation, mixing, strand interaction, normalization and projection. Metadata beyond weights—architecture/state/regulation schemas, tokenizer and provenance—is added only when actual semantics require it.

## Comparisons and composition

DOGMA: token + carried state → transition → next state + scores
Hermon DNA: token + cached K/V → attention → updated K/V + scores

Compression and addressability are different strategies, not a ranking. Attention access does not guarantee exact retrieval; finite carried state does not guarantee complete historical retention.

EVOU-61 plans next-token, copying, associative retrieval, motifs, statistics, parity, pointer/state-machine, long genomic, language and code tasks. Streaming, edge and persistent-agent uses remain hypotheses. Report quality, convergence, training/inference throughput, latency, weights, runtime/context/temporary memory and batch size; power only if measured. No universal winner is presumed.

EVOU-58–59 place Evolutor above both. A regulator choosing compressed versus addressable memory is a research hypothesis, to compare with known hybrid-memory/routing methods. It is not an AGI result.

## Historical lineage

The immediately preceding undergraduate plan at 252def4c94f256a731917aa7e8a210ab7dea483b deferred the mapping to EVOU-37. The amendment fixes target intent while retaining an artifact audit.

Preserved astra-rewrite: 58fa55a8097157d297be4afe21f146623048b875.
Preserved pre-reboot snapshot: 9df0d006e10e56cd836a4b84400009dab3cbf4f2.

Historical files and earlier chapter sources are not silently renamed. Future audits must record historical name, commit, observed architecture, target family and migration decision separately. An old Transformer artifact cannot be called non-Transformer merely because its historical name was DOGMA. This amendment makes no claim that existing external repositories already implement the target architectures.
