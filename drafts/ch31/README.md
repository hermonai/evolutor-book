# Chapter 31 — DOGMA state construction and execution

Locally authored integration candidate sourced from evolutor-ch31-r01.zip.
Incoming metadata is preserved in research/integration/ch31/incoming; the source
package's claimed checks are not adopted as local review.

## Build and verify

Use Python 3.13.6 at /Users/wenyan/.pyenv/versions/3.13.6/bin/python3.

- Run pytest -q -o addopts='' tests/test_ch31_reference.py.
- Run drafts/ch31/build.py --render for strict LaTeX and color/grayscale review pages.
- Run drafts/ch31/build.py --check to verify computed assets.
- Full regression: pytest -q -o addopts='' --junitxml=build/ch31/regression.xml.
- Continuous manuscript: scripts/build-convergence.py --through 31 --refresh-assets.

Six original TikZ plates have semantic TXT companions. Five literal function
listings, independent arithmetic oracles and twenty worked exercises accompany
the derivations. Tests and author visual review do not confer independent
scientific acceptance. Frozen accepted editions remain unchanged.
