# Chapter source notes before the 2026-10-19 prepublication edit

The *Sources and evidence* notes below are kept verbatim as they stood before the
2026-10-19 prepublication pass. That pass removed production-provenance wording
(supplied or incoming packages, adoption maps, coordinator tests) from the printed
notes and kept every statement about how deeply an external source was read. The
adoption records themselves remain in `research/integration/chNN/`.

## Chapter 23 (`drafts/ch23/sources.tex`)

SHA-256 `1f8f283f4b478c495cfa5b7f6769797dbaf8c080882f5591733db4b1eb7458e6`

```latex
\section*{Sources and evidence}
\addcontentsline{toc}{section}{Sources and evidence}
Local checks on 6 October 2026 inspected Transformer, DNABERT-2, HyenaDNA and
Caduceus arXiv abstracts/version records, not their full experiments.
DNABERT's original author repository supplied its citation and README
pretraining/tokenization contract; direct publisher access did not expose the
methods text in this check. Nucleotide Transformer was verified through indexed
primary abstract/metadata; direct publisher and PMC full-text access failed.
Evo 2 was checked in publisher HTML for abstract and publication metadata.
Its Nature version of record replaces the package's outdated preprint-only status.
Access depths and unresolved replication gates are recorded separately.

All equations, literal reference listings, assigned-tensor trace, tests and local
three-seed pilots are teaching artifacts. Prior reported performance is not
reproduced or attributed to Hermon. No biological mechanism, genomic capability,
optimized engine or independent specialist review is established by this chapter.

\begin{thebibliography}{9}
\bibitem{transformer2017} A. Vaswani et al. \emph{Attention Is All You Need}.
arXiv:1706.03762 (2017; record revised 2023).
\url{https://arxiv.org/abs/1706.03762}.
\bibitem{dnabert2021} Y. Ji, Z. Zhou, H. Liu and R. V. Davuluri.
\emph{DNABERT: pre-trained Bidirectional Encoder Representations from Transformers
model for DNA-language in genome}. Bioinformatics 37 (2021), 2112--2120.
\url{https://doi.org/10.1093/bioinformatics/btab083}.
Author implementation: \url{https://github.com/jerryji1993/DNABERT}.
\bibitem{nt2025} H. Dalla-Torre et al.
\emph{Nucleotide Transformer: building and evaluating robust foundation models
for human genomics}. Nature Methods 22 (2025), 287--297.
\url{https://doi.org/10.1038/s41592-024-02523-z}.
\bibitem{dnabert2} Z. Zhou et al.
\emph{DNABERT-2: Efficient Foundation Model and Benchmark For Multi-Species Genome}.
arXiv:2306.15006 (2023; version 2, 18 March 2024; ICLR 2024).
\url{https://arxiv.org/abs/2306.15006}.
\bibitem{hyenadna} E. Nguyen et al.
\emph{HyenaDNA: Long-Range Genomic Sequence Modeling at Single Nucleotide Resolution}.
arXiv:2306.15794 (2023; version 2, 14 November 2023).
\url{https://arxiv.org/abs/2306.15794}.
\bibitem{caduceus} Y. Schiff et al.
\emph{Caduceus: Bi-Directional Equivariant Long-Range DNA Sequence Modeling}.
arXiv:2403.03234 (2024; version 2, 5 June 2024; ICML 2024).
\url{https://arxiv.org/abs/2403.03234}.
\bibitem{evo2} G. Brixi et al.
\emph{Genome modelling and design across all domains of life with Evo 2}.
Nature 652 (2026), 1349--1361; published 4 March 2026.
\url{https://doi.org/10.1038/s41586-026-10176-5}.
\end{thebibliography}
```

## Chapter 25 (`drafts/ch25/sources.tex`)

SHA-256 `b03204819ca22e5bc143f1987810a339925d834a9e02dddfe91543fe001a3553`

```latex
\chapter*{Evidence and source boundaries}
The split-closure algorithm, synthetic comparison, paired/cluster calculations
and native execution probes are inspectable teaching references. The uncertainty
derivation is conditional on its declared sampling unit; it is not a clinical
or general biological inference guarantee. Model probes use the actual integrated
Chapter 22/23 references, but neither train nor compare their capability here.

Primary abstract/metadata records for Dodge, Bouthillier and Dehghani were
inspected on 6 October 2026. They support reporting, variance and benchmark-choice
context, not a claim that this harness reproduces those studies.
The integrated Chapters 22--24 were inspected in full for native state,
mask/span and current-pilot continuity. The incoming 47.7-percent single-pilot
statement remains package provenance, not the current Chapter 23 result.
Independent specialist and reader review remain separate from these checks.

\begin{thebibliography}{99}
\bibitem{dodge} J. Dodge, S. Gururangan, D. Card, R. Schwartz and N. A. Smith.
Show Your Work: Improved Reporting of Experimental Results.
\emph{EMNLP-IJCNLP} 2185--2194 (2019).
\url{https://doi.org/10.18653/v1/D19-1224}.
\bibitem{variance} X. Bouthillier et al. Accounting for Variance in Machine Learning
Benchmarks. Primary preprint arXiv:2103.03098v1 (2021); abstract and author metadata.
\url{https://arxiv.org/abs/2103.03098v1}.
\bibitem{lottery} M. Dehghani et al. The Benchmark Lottery.
Primary preprint arXiv:2107.07002v1 (2021).
\url{https://arxiv.org/abs/2107.07002v1}.
\end{thebibliography}
```

## Chapter 33 (`drafts/ch33/sources.tex`)

SHA-256 `a1a38ce498e3cd5b8004a3aa0ff720a7e8fd511d8d0501ae2023aa8e25df8aaa`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}

Access checked 17 October 2026. The actual Chapter 31 recurrence and Chapter 32
pool were read and imported; the supplied Chapter 33 ZIP was inspected and all
35 declared file hashes verified. The local integration adds strict schema
validation, native continuation, tenant-scoped restoration, bounded LRU and
independent rational/collision/failure oracles. Incoming validation labels
remain provenance, not local evidence.

The primary documentation sections below were read for the specific contracts
cited, not to reproduce an entire external engine or serialization system.
The PyTorch stable URL redirected to its 2.14 documentation; local tests use
installed PyTorch 2.10 CPU and do not call its object loader. Python documentation
was read on the 3.13 branch. Live vLLM pages are dated access snapshots, not a
pinned implementation or a measured comparative benchmark.

The continuation induction, approximation bound, branch arithmetic, cost model,
code, figures and exercises are original teaching artifacts. Physical COW,
authenticated checkpoint exchange, crash durability and production GPU
concurrency are not implemented. Local tests and render inspection do not
replace independent specialist or reader review.

\begin{thebibliography}{9}
\bibitem{python-json} Python Software Foundation.
\emph{json: JSON encoder and decoder}, Python 3.13 documentation.
Standard compliance, repeated object names, nonfinite numbers, hooks and
implementation limits inspected.
\url{https://docs.python.org/3.13/library/json.html}.
\bibitem{pytorch-load} PyTorch contributors.
\emph{Serialization semantics}, restricted-loading security section.
PyTorch 2.14 documentation reached by stable redirect; limits inspected,
not an end-to-end loader security audit.
\url{https://docs.pytorch.org/docs/2.14/notes/serialization.html}.
\bibitem{vllm-design} vLLM contributors.
\emph{Automatic Prefix Caching}, design documentation.
Hash components, exact tokens, additional identities, cache salting,
reference tracking and eviction sections inspected.
\url{https://docs.vllm.ai/en/stable/design/prefix_caching/}.
\bibitem{vllm-apc} vLLM contributors.
\emph{Automatic Prefix Caching}, user documentation.
Introduction, hybrid Mamba boundary/checkpoint conditions and limits inspected.
\url{https://docs.vllm.ai/en/stable/features/automatic_prefix_caching/}.
\bibitem{vllm-args} vLLM contributors.
\emph{Engine Arguments}. Recurrent cache mode, prefix match granularity,
retention interval and shared-prefix checkpoint entries inspected.
\url{https://docs.vllm.ai/en/stable/configuration/engine_args/}.
\bibitem{nist} NIST. \emph{FIPS 180-4: Secure Hash Standard} (2015).
Official publication metadata and abstract inspected for digest/integrity
context; no independent cryptographic implementation audit claimed.
\url{https://doi.org/10.6028/NIST.FIPS.180-4}.
\end{thebibliography}
```

## Chapter 34 (`drafts/ch34/sources.tex`)

SHA-256 `e2757b35c6e0014d256fcd0549db967b239dc8bfc5a5ba78c37dfda621fd9090`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}
Access checked 17 October 2026. The supplied Chapter 34 package was inspected
as source material, not executed as a trusted build. Its detached recurrence,
simple slot dictionary and byte model were replaced by the actual Chapter
31--33 native/pool/checkpoint contracts. The incoming scheduling, masking,
layout and fusion topics remain; local tests, tables, code and illustrations
are newly source-bound.

The USENIX Orca presentation-page abstract was inspected for iteration-level
scheduling, not for a reproduced serving implementation. NVIDIA's live
CUDA Best Practices Guide 13.4 was inspected on profiling, verification and
coalesced accesses. No external benchmark is reproduced or transferred to
DOGMA. Mathematical derivations and arithmetic models in this chapter are
original and explicitly restricted to the declared recurrence.

The CPU reference is not a fused device kernel, concurrent service, durable
work journal, authenticated ownership system or measured genomic model.
Local technical and visual review does not replace independent review.
\begin{thebibliography}{9}
\bibitem{orca} Gyeong-In Yu, Joo Seong Jeong, Geon-Woo Kim, Soojeong Kim
and Byung-Gon Chun. \emph{Orca: A Distributed Serving System for
Transformer-Based Generative Models}. OSDI 2022, pp.\ 521--538.
Presentation-page abstract inspected.
\url{https://www.usenix.org/conference/osdi22/presentation/yu}.
\bibitem{cuda} NVIDIA. \emph{CUDA C++ Best Practices Guide}, version 13.4,
sections on profiling, reference comparison, numerical accuracy and
coalesced access to global memory. Live documentation inspected; no
hardware performance validation performed.
\url{https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html}.
\end{thebibliography}
```

## Chapter 35 (`drafts/ch35/sources.tex`)

SHA-256 `33cdda8632274fa30a4df3b7ea62e162adbfff16dee978ec70d021cc18e88e14`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}
Access checked 17 October 2026. The original Chapter 23 model was read and
imported, including learned absolute positions, pre-normalized blocks,
mask conventions and offline/causal separation. The supplied Chapter 35
package's rotary single-head attention was not silently adopted as Hermon's
architecture. Its prefill/decode and storage questions were retained and
extended into a full-model adapter with explicit offset masks and layered
cache validation. The Chapter 36 allocation handoff was inspected, not
integrated.

The Transformer HTML paper's attention and multi-head sections were inspected.
PyTorch 2.10 SDPA documentation was read for boolean-mask polarity,
non-square causal alignment, inference dropout and numerical backend limits;
local tests use installed PyTorch 2.10 CPU float64. FlashAttention and GQA
primary abstracts were inspected for the narrow comparisons cited, not
reimplemented or independently benchmarked. The original parity proof,
cache adapter, copying derivation, figures and exercises do not reproduce
those papers' empirical results.

This reference implements neither paging, GQA conversion, rotary positions,
quantized KV, optimized attention kernels nor a trained genomic benchmark.
Content seals are not authentication or replay proofs. Local source/test
and render review remains distinct from independent specialist or reader review.
\begin{thebibliography}{9}
\bibitem{vaswani} Ashish Vaswani et al.
\emph{Attention Is All You Need}. 2017.
Sections 3.2.1--3.2.3 inspected in the author's paper HTML.
\url{https://arxiv.org/abs/1706.03762}.
\bibitem{sdpa} PyTorch contributors.
\emph{torch.nn.functional.scaled\_dot\_product\_attention},
PyTorch 2.10 documentation. Mask, dropout, causal alignment and
numerical implementation contract inspected.
\url{https://docs.pytorch.org/docs/2.10/generated/torch.nn.functional.scaled_dot_product_attention.html}.
\bibitem{flash} Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra and
Christopher R\'e. \emph{FlashAttention: Fast and Memory-Efficient Exact
Attention with IO-Awareness}. 2022. Primary abstract inspected.
\url{https://arxiv.org/abs/2205.14135}.
\bibitem{gqa} Joshua Ainslie et al.
\emph{GQA: Training Generalized Multi-Query Transformer Models from
Multi-Head Checkpoints}. 2023. Primary abstract inspected.
\url{https://arxiv.org/abs/2305.13245}.
\end{thebibliography}
```

## Chapter 36 (`drafts/ch36/sources.tex`)

SHA-256 `1587c0fae8eed575e75978e6d07ec44e2b387b318ac8ea606a88068f77a95191`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}
Source access checked 17 October 2026. Kwon et al.'s primary HTML paper was
inspected for Sections 4.1--4.4, including block tables, partial-tail COW and
shared-prefix ownership. Its measurements were not reproduced. The actual
Chapter 35 implementation and Chapter 23 model were read and imported;
the relevant Chapter 32 generation/pin and Chapter 33 COW contracts were
inspected. This chapter's proofs assume serialized trusted callers.
Generation checks, hashes and refcounts do not establish authentication,
hostile-process isolation or asynchronous device safety.

The supplied r01 manuscript, allocator, tests, six figure pairs, storyboard
and source ledger are retained as text-only provenance. Its tuple allocator
is extended into actual multi-layer KV storage, and its logical-multiplicity
ratio is corrected to distinguish physical utilization. The adoption map
records section-level destinations; packaged caches and QA flags are not evidence.
\begin{thebibliography}{9}
\bibitem{evod36:kwon} Woosuk Kwon et al.
\emph{Efficient Memory Management for Large Language Model Serving with
PagedAttention}. SOSP, 2023. Primary HTML Sections 4.1--4.4 inspected.
\url{https://arxiv.org/html/2309.06180}.
\end{thebibliography}
```

## Chapter 37 (`drafts/ch37/sources.tex`)

SHA-256 `8b11a9cbf7ec1c6a9af7b0d0ec437d28dfa02cb07646f2ba29dd896853179f0a`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}
Source access checked 17 October 2026. Orca and VTC were inspected at their
official USENIX abstract/proceedings pages; their full proofs, artifacts
and experimental results were not independently audited. Sarathi-Serve's
primary HTML Section 4, including Algorithm 3 and token-budget/chunk
discussion, was inspected. SmoothQuant's primary HTML Sections 3--4 and
calibration/implementation discussion were inspected. These sources motivate
specific comparisons, not inherited speed or fairness claims.

Actual Chapters 35--36 implementations were read and executed. Native CPU
FP16/BF16 casts and declared INT8 reconstruction are local representation
experiments; no native FP8/INT8 engine or compressed KV pool is supplied.
An attempted NVIDIA FP8 primer access failed, so no current device-support
claim is based on it. The incoming r01 sections, tests, figures, source
leads and work examples are mapped in the package-adoption record.
The original extra-decode timing and flattened-argmax metric are corrected.
Local author review is not independent specialist or task-quality acceptance.
\begin{thebibliography}{9}
\bibitem{evod37:orca} Gyeong-In Yu et al.
\emph{Orca: A Distributed Serving System for Transformer-Based Generative
Models}. OSDI, 2022. Official abstract inspected.
\url{https://www.usenix.org/conference/osdi22/presentation/yu}.
\bibitem{evod37:sarathi} Amey Agrawal et al.
\emph{Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve}.
2024. Primary HTML Section 4 inspected.
\url{https://arxiv.org/html/2403.02310v3}.
\bibitem{evod37:fairness} Ying Sheng et al.
\emph{Fairness in Serving Large Language Models}. OSDI, 2024.
Official abstract inspected; VTC guarantees are not attributed to our scheduler.
\url{https://www.usenix.org/conference/osdi24/presentation/sheng}.
\bibitem{evod37:smoothquant} Guangxuan Xiao et al.
\emph{SmoothQuant: Accurate and Efficient Post-Training Quantization for
Large Language Models}. 2022/2023. Primary method and calibration text inspected.
\url{https://arxiv.org/html/2211.10438}.
\end{thebibliography}
```

## Chapter 38 (`drafts/ch38/sources.tex`)

SHA-256 `e92d0913479796145a22d84867cb88d468397cf76283d40558b9c2453b8fda07`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}
Source access checked 17 October 2026. Leviathan et al.'s primary HTML
Section 2/Algorithm 1 and Appendix A.1 proof were inspected. Chen et al.'s
Algorithm 2 and Section 4 conditional-scoring discussion were inspected;
that paper reverses our target/draft letter convention. FlashAttention's
primary HTML online-softmax derivation, Algorithm 1 and correctness/IO
theorem statements were inspected; no CUDA implementation or empirical
result was reproduced. FlashAttention-2 was inspected at abstract depth only.
PyTorch 2.10 SDPA's boolean-mask, non-square causal, dropout and backend
numerics documentation was inspected, and local tests use its CPU float64 path.

The supplied r01 rejection algebra, TV relationship, worked distributions,
online-softmax recurrence, traffic example, exercises and source leads are
retained and deepened. Its list-of-distributions block is replaced by actual
history-conditioned proposals and native paged speculative state. Complete
Hermon online-attention continuation is tested separately from the paged
attention visitor; neither is represented as a measured GPU kernel.
The adoption map and technical audit record the exact boundaries.
\begin{thebibliography}{9}
\bibitem{evod38:leviathan} Yaniv Leviathan, Matan Kalman and Yossi Matias.
\emph{Fast Inference from Transformers via Speculative Decoding}. 2023.
Section 2 and Appendix A.1 inspected.
\url{https://arxiv.org/html/2211.17192v2}.
\bibitem{evod38:chen} Charlie Chen et al.
\emph{Accelerating Large Language Model Decoding with Speculative Sampling}.
2023. Algorithm 2 and Section 4 inspected.
\url{https://arxiv.org/html/2302.01318v1}.
\bibitem{evod38:flash} Tri Dao et al.
\emph{FlashAttention: Fast and Memory-Efficient Exact Attention with
IO-Awareness}. 2022. Online reduction and Algorithm 1 inspected.
\url{https://arxiv.org/html/2205.14135}.
\bibitem{evod38:flash2} Tri Dao.
\emph{FlashAttention-2: Faster Attention with Better Parallelism and Work
Partitioning}. 2023. Primary abstract inspected.
\url{https://arxiv.org/abs/2307.08691}.
\bibitem{evod38:sdpa} PyTorch contributors.
\emph{scaled\_dot\_product\_attention}. Version 2.10 documentation.
\url{https://docs.pytorch.org/docs/2.10/generated/torch.nn.functional.scaled_dot_product_attention.html}.
\end{thebibliography}
```

## Chapter 39 (`drafts/ch39/sources.tex`)

SHA-256 `eda5fe0784589194f4df71867eab24556b77e63245d6734d709b75c6f8eeadfd`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}
Access checked 17 October 2026. The supplied Chapter 39 package was read in
full and retained as text-only provenance. Its runtime/module separation,
capability routing, planner/router distinction, opaque-state questions,
policy-before-effect rule and observable trace scope were retained and expanded.
The original mock adapters were replaced by imports of the stable Chapter 31
native recurrence and Chapter 35 layered cache over the actual Chapter 23
Transformer. Full source interfaces were inspected. Chapter 30's lifecycle,
Chapter 32's ownership and Chapter 33's checkpoint contracts were read for
the integration boundary; those are not replaced by this serialized coordinator.

The typed workflow, ownership proof, failure windows, figures, code and
exercises are chapter-defined engineering contracts. No external novelty,
biological-capability or performance claim depends on them. The package's
Chapter 36--38 continuity descriptions were not adopted as passing executable
dependencies. Physical allocation and serving-shell integration remain explicit
coordinator tests. Chapter-local source/adoption records retain exact scope.
Local author review is not independent specialist review or acceptance.
\begingroup
\renewcommand{\bibname}{References}
\let\chapter\section
\begin{thebibliography}{9}
\bibitem{evod39:internal} Evolutor companion sources. Chapters 14--16, 20,
23 and 30--35. Typed semantics, memory distinctions, lifecycle and actual
native/attention reference implementations. Repository-local primary sources,
inspected at the hashes recorded in the chapter-local review.
\end{thebibliography}
\endgroup
```

## Chapter 40 (`drafts/ch40/sources.tex`)

SHA-256 `fd02fec4b2724c725a50668748c108ee41170754e5e3c3143bada39fc40c0c76`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}
Access checked 17 October 2026. The supplied memory package's full manuscript,
reference, tests, storyboard, figure sources and ledger were read. Its memory
roles, lossy summary/source links, retrieval, rehydration, retention,
tombstones and evidence firewall were retained. The new reference adds
transitive availability, non-resurrecting occurrence IDs, provenance-depth
and store bounds, dual rehydration budgets, immutable context and explicit
issued-context revocation limits. Chapter 20's compression arguments and the
actual Chapter 35 cache contract were read for continuity.

MemGPT and Self-RAG were accessed at their primary arXiv abstract pages.
Only the narrow memory-hierarchy and adaptive-retrieval claims are used;
the full algorithms and experiments were not independently reproduced.
No retrieval SOTA, security certification, physical erasure or learned utility
claim follows from the deterministic lexical fixture. Package caches and QA
labels were not adopted. Local review remains distinct from acceptance.
\begingroup
\renewcommand{\bibname}{References}
\let\chapter\section
\begin{thebibliography}{9}
\bibitem{evod40:memgpt} Charles Packer et al.
\emph{MemGPT: Towards LLMs as Operating Systems}. 2023; arXiv v2, 2024.
Primary abstract inspected for virtual context management and tier movement.
\url{https://arxiv.org/abs/2310.08560}.
\bibitem{evod40:selfrag} Akari Asai et al.
\emph{Self-RAG: Learning to Retrieve, Generate, and Critique through
Self-Reflection}. 2023. Primary abstract inspected for on-demand retrieval.
\url{https://arxiv.org/abs/2310.11511}.
\end{thebibliography}
\endgroup
```

## Chapter 41 (`drafts/ch41/sources.tex`)

SHA-256 `5b9c8d9736d8dbdc2d0bc00479b5d4b83c121ccb85d3d60510eda2358aa45640`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}
Access checked 17 October 2026. The supplied compiler package was read in full.
SSA, verification, folding, DCE, capability lowering, costs, liveness, source
IDs and exercises were retained and deepened. Its classification of engine
and retrieval operations as freely pure was not retained: our dialect preserves
those observations and checks declared effects against operation semantics.
The independent recursive arithmetic oracle and actual Chapter 39/40
handlers test a more precise contract. Chapter 14 tensor typing,
Chapter 15 transition semantics and Chapter 16 resource conventions were
inspected; this finite IR does not implement every earlier language.

The official MLIR language reference's high-level operation/value model and
side-effect rationale's categorization/modeling sections were inspected.
The TVM primary arXiv abstract was inspected for compiler organization only.
This reference implements neither framework, target code generation nor
hardware experiments. Chapter 36 integration and production serialization remain open.
\begingroup
\renewcommand{\bibname}{References}
\let\chapter\section
\begin{thebibliography}{9}
\bibitem{evod41:mlir} MLIR contributors.
\emph{MLIR Language Reference}. Official documentation, high-level structure
and operations/values inspected 17 October 2026.
\url{https://mlir.llvm.org/docs/LangRef/}.
\bibitem{evod41:effects} MLIR contributors.
\emph{Side Effects \& Speculation}. Official rationale, overview,
categorization and modeling sections inspected 17 October 2026.
\url{https://mlir.llvm.org/docs/Rationale/SideEffectsAndSpeculation/}.
\bibitem{evod41:tvm} Tianqi Chen et al.
\emph{TVM: An Automated End-to-End Optimizing Compiler for Deep Learning}.
2018. Primary abstract inspected; no benchmark reproduction.
\url{https://arxiv.org/abs/1802.04799}.
\end{thebibliography}
\endgroup
```

## Chapter 42 (`drafts/ch42/sources.tex`)

SHA-256 `b3e3d9918c9e9783e20567d24169e76c8840cc735fd9cf952eed3561a043ef8f`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}
Access checked 17 October 2026. The supplied database-comparison package was
read in full. Logical/physical plans, Volcano/Cascades, buffering,
transactions, indexes, statistics, materialization, recovery/replay and analogy
limits were retained. The WAL was strengthened with exact log/page
binding, bounded flushes, stale-write rejection, crash images and an independent
durable-prefix oracle. It remains committed-redo-only, not an ARIES clone.

Volcano's primary-paper text was inspected for the standard interface,
buffer-manager mechanism/policy separation and exchange description. Cascades'
primary-paper sections on optimization tasks, memoization and on-demand
exploration were inspected. ARIES access was narrower: publisher metadata/
abstract and an indexed primary-paper excerpt on log forcing/LSNs were read;
two attempted full-PDF retrievals timed out. No full-paper reconstruction or
ARIES implementation is claimed. The WAL proof is self-contained under this
chapter's stated crash model. Source records distinguish these depths.
\begingroup
\renewcommand{\bibname}{References}
\let\chapter\section
\begin{thebibliography}{9}
\bibitem{evod42:volcano} Goetz Graefe.
\emph{Volcano---An Extensible and Parallel Query Evaluation System}.
IEEE TKDE 6(1), 120--135, 1994. Primary interface/buffer/exchange passages.
\url{https://people.eecs.berkeley.edu/~prabal/teaching/resources/eecs582/graefe94volcano.pdf}.
\bibitem{evod42:cascades} Goetz Graefe.
\emph{The Cascades Framework for Query Optimization}.
IEEE Data Engineering Bulletin 18(3), 19--29, 1995. Primary paper,
optimization tasks and exploration sections.
\url{https://15721.courses.cs.cmu.edu/spring2019/papers/22-optimizer1/graefe-ieee1995.pdf}.
\bibitem{evod42:aries} C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh
and Peter Schwarz.
\emph{ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking
and Partial Rollbacks Using Write-Ahead Logging}. ACM TODS 17(1), 94--162, 1992.
Publisher record and indexed primary excerpt; full-PDF access incomplete.
\url{https://doi.org/10.1145/128765.128770}.
\end{thebibliography}
\endgroup
```

## Chapter 43 (`drafts/ch43/sources.tex`)

SHA-256 `290f278d4bd6f7e95b8526c1c5eff681b894f98c8abbca030ee7d2eb474800b2`

```latex
\chapter*{Sources and further reading}
\addcontentsline{toc}{chapter}{Sources and further reading}
Access checked 17 October 2026. The supplied governance package was read in
full. Its adaptation categories, immutable lineage, lifecycle, conjunctive gates,
EWC comparison, shadow/canary, authority separation, promotion, rollback and
monitoring were retained. The reference now separates content from stage,
fixes unrestricted rollback, records immutable evidence, rejects nonfinite/
missing metrics and empty gates, requires a current release revision and
asserted reset for incompatible state. Role labels, data labels and drain flags
are trusted assertions, not cryptographic deployment evidence.

The primary EWC paper HTML was inspected in its method discussion and
Equations 1--3, with experimental context. Only its approximate parametric
regularization mechanism is summarized. The quadratic example is independently
derived arithmetic, not trained EWC. Chapter 13's state/weight/structure/population
distinctions and Chapter 30/31/35 artifact-bound state conventions were
read for continuity. Production signatures, durable CAS and request draining
remain separate requirements. Local author review is not independent acceptance.
\begingroup
\renewcommand{\bibname}{References}
\let\chapter\section
\begin{thebibliography}{9}
\bibitem{evod43:ewc} James Kirkpatrick et al.
\emph{Overcoming catastrophic forgetting in neural networks}.
PNAS 114(13), 3521--3526, 2017. Primary method HTML, approximate posterior and
Fisher-weighted penalty, Equations 1--3.
\url{https://arxiv.org/html/1612.00796v2}.
\url{https://doi.org/10.1073/pnas.1611835114}.
\end{thebibliography}
\endgroup
```

## Chapter 44 (`drafts/ch44/sources.tex`)

SHA-256 `59220d9c2d2248ba0bc900afaa400d20dfa7b41bd7357046ba7be3c387ee4901`

```latex
\begin{thebibliography}{9}
\addcontentsline{toc}{chapter}{Sources and references}
\bibitem{slsa44} SLSA contributors. \emph{SLSA v1.2: Provenance}.
Official approved definition inspected.
\url{https://slsa.dev/spec/v1.2/provenance}.
\bibitem{otel44} OpenTelemetry contributors. \emph{Specification: Overview}.
Signal, span/context, metric and log overview inspected; semantic-convention
terminology only, no exhaustive convention audit.
\url{https://opentelemetry.io/docs/specs/otel/overview/}.
\bibitem{probes44} Kubernetes contributors.
\emph{Liveness, Readiness, and Startup Probes}. Official conceptual documentation,
probe purposes inspected.
\url{https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/}.
\end{thebibliography}

\section*{Evidence scope}
Access checked 17 October 2026. Official SLSA v1.2 provenance definition,
OpenTelemetry overview signal/context sections and Kubernetes probe semantics
were inspected. These support the narrow terminology comparisons, not the
correctness of a deployed Evolutor service. The bundle, evidence gate,
conservation derivation, lifecycle oracle and figures are original teaching
constructions extending the supplied package. No signing, artifact build
reproduction, telemetry exporter or deployment experiment was performed.
Local author review does not constitute independent specialist review.
```

## Chapter 45 (`drafts/ch45/sources.tex`)

SHA-256 `49242dd2ddad05322546b576445403482af71e3f9624e6494ff9a1a7ce5609ce`

```latex
\begin{thebibliography}{9}
\addcontentsline{toc}{chapter}{Sources and references}
\bibitem{nist45} Scott Rose, Oliver Borchert, Stu Mitchell and Sean Connelly.
\emph{Zero Trust Architecture}. NIST SP 800-207, 2020. Official publication
overview inspected for resource authentication/authorization and network-location
trust boundary.
\url{https://csrc.nist.gov/pubs/sp/800/207/final}.
\bibitem{injection45} OWASP Gen AI Security Project.
\emph{LLM01:2025 Prompt Injection}. Types and mitigation sections inspected.
\url{https://genai.owasp.org/llmrisk/llm01-prompt-injection/}.
\bibitem{boundary45} OWASP Gen AI Security Project.
\emph{LLM07:2025 System Prompt Leakage}. Mitigation/privilege-boundary guidance
inspected. \url{https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/}.
\end{thebibliography}

\section*{Evidence scope}
Access checked 17 October 2026. NIST's publication overview was inspected for
the no-implicit-network-trust principle; this is not a full implementation
audit against every SP 800-207 requirement. OWASP's current LLM01:2025 and
LLM07:2025 pages were inspected for mitigation and external authorization
boundaries. Their recommendations are source leads, not authorization to test
live systems. No penetration test was performed. The capability registry,
namespace proof, quota oracle, local adversaries and mechanism figures are
original extensions of the supplied scenarios. They assume trusted serialized
host code and do not establish cryptographic or hardware isolation.
```

## Chapter 46 (`drafts/ch46/sources.tex`)

SHA-256 `37a93feb37084524779c9ab1178d8119af3e06db2bab6b767f0fd0a3025afe1c`

```latex
\begin{thebibliography}{9}
\addcontentsline{toc}{chapter}{Sources and references}
\bibitem{distserve46} Yinmin Zhong et al.
\emph{DistServe: Disaggregating Prefill and Decoding for Goodput-optimized
Large Language Model Serving}. OSDI 2024, pp. 193--210.
Primary PDF, selected mechanism sections inspected.
\url{https://www.usenix.org/system/files/osdi24-zhong-yinmin.pdf}.
\end{thebibliography}

\section*{Evidence scope}
Access checked 17 October 2026. DistServe's primary OSDI paper PDF was accessed;
abstract/introduction and selected architecture/phase-allocation passages were
inspected, not every evaluation or appendix. The chapter cites the disaggregation
and bandwidth-aware placement mechanism without adopting its performance
numbers. The serial ownership proof, transfer/capacity oracle, fault fixtures
and illustrations are original extensions of the package's migration scenario.
Actual Chapter 31/35 and transitive Chapter 23 sources provide local model
interfaces for test-only snapshot continuation. This is not a production
distributed engine or a proof of consensus, transport authentication, durable
recovery or exactly-once tools. Independent review remains open.
```

## Chapter 47 (`drafts/ch47/sources.tex`)

SHA-256 `1fb42b5d213a6470376e19a449d1feb2ac1b77122c7d54c37ad64a31c2e34953`

```latex
\begin{thebibliography}{99}
\addcontentsline{toc}{chapter}{Sources and references}
\bibitem{roofline47} Samuel Williams, Andrew Waterman and David Patterson.
\emph{Roofline: An Insightful Visual Performance Model for Floating-Point
Programs and Multicore Architectures}. UCB/EECS-2008-134, 2008.
Primary author technical report, Section 3 inspected; predecessor of the
2009 CACM publication.
\url{https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.pdf}.
\bibitem{distserve47} Yinmin Zhong et al. \emph{DistServe}. OSDI 2024.
Selected mechanism/metric passages inspected, not reproduced.
\url{https://www.usenix.org/system/files/osdi24-zhong-yinmin.pdf}.
\bibitem{flash47} Tri Dao et al. \emph{FlashAttention: Fast and Memory-Efficient
Exact Attention with IO-Awareness}. 2022. Primary abstract only.
\url{https://arxiv.org/abs/2205.14135}.
\bibitem{torch47} PyTorch contributors. \emph{torch.profiler}, version 2.10.
API, scheduling and shape/stack overhead guidance inspected.
\url{https://docs.pytorch.org/docs/2.10/profiler.html}.
\bibitem{nsys47} NVIDIA. \emph{Nsight Systems User Guide}. Timeline, focused
collection/NVTX and overhead guidance inspected.
\url{https://docs.nvidia.com/nsight-systems/UserGuide/index.html}.
\bibitem{ncu47} NVIDIA. \emph{Nsight Compute Profiling Guide}.
Kernel-profiling and counter/replay overview inspected.
\url{https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html}.
\bibitem{metal47} Apple. \emph{Metal Developer Tools}. Tools, dependencies and
memory-inspection overview inspected; not an API benchmark.
\url{https://developer.apple.com/metal/tools/}.
\bibitem{vulkan47} Khronos. \emph{Vulkan Guide: Synchronization}.
Synchronization, validation and pipeline-barrier overview inspected.
\url{https://docs.vulkan.org/guide/latest/synchronization.html}.
\end{thebibliography}

\section*{Evidence scope}
Access checked 17 October 2026. The packaged Roofline URL was inaccessible;
the authors' Berkeley 2008 technical-report version was accessed instead,
especially Section 3's memory-boundary definition and ceiling formula.
DistServe's abstract/introduction and selected phase/placement passages were
inspected. FlashAttention access was abstract-only. Official profiler guides
were inspected at overview/API and relevant overhead/synchronization passages;
no profiler was run. Apple's tools overview and Khronos's synchronization
overview support narrow platform distinctions, not backend performance rankings.
All chapter traces, ceilings and operation/byte rows are assigned or analytic.
No real-backend result is supplied. Original analysis/tests and figures are
not copied empirical results or independent validation.
```

