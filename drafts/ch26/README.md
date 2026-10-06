# EVOD-26: Training/inference parity and parallel recurrence

Substantial original rewrite of the r01 package. An input-conditioned affine core has literal loop, inclusive scan, chunked and independent product/sum oracles. Resets and padding fold into affine maps; manual reverse derivatives and finite differences check gradients. A detach intervention and float64 cancellation counterexample expose limits of forward parity. Complete DOGMA state is not certified scan-compatible.

30 chapter tests; five whole-function listings; six original editable TikZ plates with detailed semantic TXT companions; twenty worked questions.

Run in Python 3.13 with PyTorch:

- OMP_NUM_THREADS=1 python3 -m pytest -q -o addopts='' tests/test_ch26_reference.py
- python3 drafts/ch26/build.py --assets-only
- python3 drafts/ch26/build.py --check
- python3 drafts/ch26/build.py --render
- python3 scripts/build-convergence.py --through 26 --refresh-assets

Incoming QA is provenance only. Current build/test/source-review records are separately bound in research/integration/ch26/. No independent-review or publication-acceptance promotion.
