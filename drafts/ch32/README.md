# Chapter 32 — DOGMA state pools and memory ownership

Integration candidate using evolutor-ch32-r01.zip; incoming metadata is preserved
under research/integration/ch32/incoming, not adopted as local evidence.

Bounded serialized inference pool: caller-bound ownership, artifact identity,
allocation generation, in-flight pins, retiring slots, versioned completion and
independent same-tenant clones. The actual Chapter 31 model supplies the native
inference bridge. Six vector/TXT plates and twenty worked exercises teach
reclamation and isolation.

## Build and verify

Use Python 3.13.6 at /Users/wenyan/.pyenv/versions/3.13.6/bin/python3.

- OMP_NUM_THREADS=1 pytest -q -o addopts='' tests/test_ch32_reference.py
- drafts/ch32/build.py --render
- drafts/ch32/build.py --check
- OMP_NUM_THREADS=1 pytest -q -o addopts='' --junitxml=build/ch32/regression.xml
- scripts/build-convergence.py --through 32 --refresh-assets

Logical zeroing is not secure erasure; serialized tests are not GPU race,
security or durability proof. Scalar reload intentionally severs autograd.
Next: Chapter 33 checkpoints, branches and shared prefixes with fresh ownership.
