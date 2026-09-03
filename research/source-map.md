# Source map

Snapshot date: 2026-09-04. Sources were inspected in place and are not copied into this repository.

## Evolutor theory sources

| Source | Identity | Role | Status |
| --- | --- | --- | --- |
| Evolutor v1.4.1 TeX/PDF | `/Users/wenyan/Evolutor/Paper/Evolutor - A Theory of Genomic Computation v1.4.1.{tex,pdf}`; 893 TeX lines; 17 PDF pages | prompt-specified theory baseline | audited into theorem ledger |
| Evolutor v1.7.0 TeX/PDF | same directory, v1.7.0; 1,064 TeX lines | later revision with expanded proof statements/open problems | version-difference audit pending |
| DOGMA audit errata | `/Users/wenyan/Evolutor/Paper/DOGMA_AUDIT_ERRATA_2026-08-02.md` | supersedes empirical/universality claims in older DOGMA papers | current correction source |
| Core Evolutor new design | `/Users/wenyan/Evolutor/CORE_EVOLUTOR_NEW_DESIGN.md` | product/runtime direction | proposal, not proof |
| Prior Evolutor implementation/book | `/Users/wenyan/Evolutor/evolutor` | Rust/Python/docs reference | unborn Git repo; 16 untracked roots; do not modify |

The Evolutor v1.4.1 TeX is the definition source for this bootstrap. The PDF was checked for identity and pagination. v1.7.0 is recorded as a later lineage, not silently substituted.

## DNA-computing foundation source

`/Users/wenyan/ClaudeProjects/dna2agi/DNAComputingFoundations.pdf` is a 170-page, July 2026 author-created textbook. Its title page, front matter, complete structure, bibliography region, and relevant DNA computing/regulation/ML sections were inspected. It is a pedagogical lead, not a primary authority.

The separately named Kari/Seki/Sosik source in the execution prompt was not found as a distinct file. `[RESEARCH NEEDED: obtain an authorized copy or exact bibliographic identity.]`

## Architecture and implementation repositories

| Repository | Commit / state | Architecture evidence |
| --- | --- | --- |
| `/Users/wenyan/ClaudeProjects/dna2agi` | `49e6fa790a6faaa2b470881f058fdf8fcd69e1ab`, branch `paper/capacity-is-all-you-measured`, 50 changed paths | prior books, correction paper, branch terminology |
| `/Users/wenyan/ClaudeProjects/evo-trainer` | `610117f0c6f73eed12d7bfba1478696512fb52c2`, branch `fix/dogma-causality`, 59 changed paths | PyTorch recurrent DOGMA, GIR/evolution contracts, audits |
| `/Users/wenyan/ClaudeProjects/dogma` | unborn `main`, 9 changed paths | recurrent-state engine, fixed-state versus KV architecture |
| `/Users/wenyan/ClaudeProjects/hermon` | `472a44cdb511b2dae6c9569e59543db8f8350b25`, `main`, 1 changed path | transformer-oriented engine, attention, `hermon-paged-kv`, prefix radix |
| `/Users/wenyan/Evolutor/evolutor` | unborn `main`, 16 untracked roots | older GCS runtime and mdBook scaffold |

Existing working trees were not modified. An embedded credential was observed in the old Evolutor remote and kept redacted; that remote must not be copied into new repositories.

## Source priority

1. For a definition, cite the named Evolutor version.
2. For a proof, independently check the proof; a TeX theorem environment is not proof status.
3. For current implementation, require a clean commit or file/artifact hash.
4. For biology or DNA computing, cite primary external literature.
5. For measurements, require the full experiment identity in `experimental-controls.md`.

