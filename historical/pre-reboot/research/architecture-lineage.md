# Architecture lineage

## Observed lineage

| Artifact | Name in artifact | Family actually implemented/described | Evidence identity |
| --- | --- | --- | --- |
| `dogma/docs/ARCHITECTURE.md` | DOGMA | recurrent selective state, no sequence self-attention | unborn repo; hash file before citation |
| `dogma/docs/BOOK_GENERATION_SYSTEM_PROMPT.md` | DOGMA | recurrent training + fixed-state inference | unborn repo; source prompt |
| `evo-trainer` corrected core | DOGMA / dogma-core / dogma-scan | recurrent/non-transformer | commit `610117f0c6f...`, dirty tree; artifacts need hashes |
| `hermon` | Hermon | Transformer-oriented inference with attention and paged KV | commit `472a44cdb511...` |
| Evolutor v1.4.1 | Evolutor / GCS | umbrella formal computation model | local TeX/PDF |
| intended future line A | DOGMA | Transformer DNA-LLM | target naming proposal |
| intended future line B | Hermon DNA | non-Transformer DNA-LLM / GCS | target naming proposal |

## Non-contamination rule

Historical experiments stay attached to their producing code and architecture. A recurrent result labeled DOGMA does not become Transformer evidence after a brand migration. Hermon's paged-KV implementation does not become evidence for a future recurrent Hermon DNA model.

## Qualified vocabulary during migration

- **DOGMA-R**: historical/current recurrent DOGMA.
- **Hermon Engine**: historical/current Transformer-serving runtime.
- **DOGMA-T**: proposed target Transformer DNA line.
- **Hermon DNA-R**: proposed target non-Transformer line.

These qualifiers are documentation devices, not package renames.

