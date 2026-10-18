# Approved author storyboard — Chapter 36

The incoming six figure questions are retained in five mechanism plates.
1. Translation: five logical token ordinals map through [0,2,3] to scattered physical pages; every cell is an all-layer K/V token slice. Distinguish layer/head geometry from page capacity.
2. COW: parent/child share a full block and a partial tail; append leaves parent rows unchanged and redirects only the child's tail. Dashed unused cells are capacity, not tokens.
3. Lifetime: three owning tables become two after cache eviction, then one, then zero; only the zero transition scrubs and advances generation.
4. Atomic append: a two-page request with only one free slot is rejected before any publication; metadata and payload snapshots remain equal.
5. Geometry: P=2/4/8 for T=13 exposes exact tail-slot arithmetic. Sharing multiplicity is not physical utilization.

All arrows denote software lookup, ownership or publication; no biological mechanism is implied. Use labels, solid/dashed styles and cell boundaries in grayscale. Review at final print size.
