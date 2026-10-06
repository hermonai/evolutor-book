# Continuous authored-source review build

Run Python 3.13: scripts/build-convergence.py --through 30 --refresh-assets.
The explicit range must exist; a partial build is never labeled the full planned
book. --prepare-only assembles source without invoking the compiler.

This entry point is needed because the previous cumulative export did not assemble
the current authored LaTeX chapter candidates. It preserves original draft and
frozen accepted sources, converts native SVG assets, generates tables/listings
through chapter builders, namespaces chapter labels (including AMS display labels),
strictly remaps citations and consolidates exact bibliography identifiers with a
provenance map. It adds one global glossary and index.

Output: output/pdf/evolutor-convergence.pdf.
Source hashes, page count and status: build/convergence/build-record.json.
Compiler warnings are audited before exporting. Successful compilation is not
every-page visual review, independent specialist review or publication acceptance.
Standalone chapter review records do not transfer automatically to this layout.
