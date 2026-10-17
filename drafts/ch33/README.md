# Chapter 33 — DOGMA checkpoints, branching and prefix state

Uses and substantially extends evolutor-ch33-r01.zip. Incoming metadata lives in
research/integration/ch33/incoming; its checks are not adopted as local evidence.

The actual Chapter 31 recurrence and Chapter 32 pool implement fresh-owner
restore, native branch continuation and a bounded tenant-scoped immutable LRU.
Strict bounded data-only decoding, exact context/prefix binding, independent
rational oracles and rehashed-forgery/collision tests separate integrity from
replay consistency and authority. Six editable vector/TXT plates and twenty
worked exercises accompany a continuation proof, error bound and storage/replay
derivation including repeated-prefix metadata costs.

## Build and verify

Use Python 3.13.6 and OMP_NUM_THREADS=1:

- python3 drafts/ch33/build.py --render
- python3 drafts/ch33/build.py --check
- python3 -m pytest tests/test_ch33_reference.py -q -o addopts=''
- python3 -m pytest -q -o addopts=''
- python3 scripts/build-convergence.py --through 33 --refresh-assets

Serialized trusted in-process inference only. Physical COW, authentication,
durability, training restart, GPU concurrency and capability/speed claims are
outside scope. Next: Chapter 34 batching and state-native kernels.
