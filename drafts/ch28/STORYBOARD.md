# Chapter 28 visual teaching plan

## 01-axes

Data parallel ownership partitions examples and replicates weights. Tensor parallel ownership partitions contraction or output coordinates. Pipeline ownership partitions layers and communicates activations. State sharding partitions persistent arrays and may combine with the other three. Three owner tiles in each panel indicate logical ranks, not a measured deployment. Ownership does not imply transient all-gather buffers are absent.

## 02-ddp

Three rank nodes emit numerator gradients and valid mass, including a zero-mass rank. Their sum node yields gradient numerator (11,9) and global denominator 5. A single normalization edge yields (2.2,1.8). For a mean collective each rank backpropagates D Nr/Z; for a sum collective it uses Nr/Z. Rank-local means are a tested counterexample. This is local algebra, not a launched process group.

## 03-shard

The global ten-coordinate tensor is partitioned into rank0 [0,4), rank1 [4,7), rank2 [7,10), with extents4/3/3. Descriptor nodes bind rank/world/offset/total/immutable payload. Reconstruction validates unique complete rank identities and expected balanced coverage, then sorts by rank. Empty owners are explicit when world>length; neither total extent alone nor file order proves reconstruction.

## 04-hybrid

Contraction-axis partition sends matched Xr/Wr blocks to local products, each full-size BxO, then sums partial outputs. Output-axis partition sends replicated X and disjoint output-column blocks Wr to local products, then concatenates output coordinates. Bias is added once after a contraction sum. Matrix dimensions, not framework naming, define the decomposition and the required backward ownership.

## 05-boundary

Manifest contract metadata and exact raw tensor bytes feed a content-identity node. Verification compares that identity with an independently trusted pin, checks schema and expected tensor set, and checks extents and hashes. A coherent attacker can replace payload/manifest/pin consistently, so internal hashes are not authenticity. Finite numerical interpretation is separate from byte integrity. This named demo is not safetensors.

## 06-manifest

Release JSON/raw bytes/independent pin pass strict schema and content gates, then a fresh interpreter decodes little-endian F32, checks finite numerical weights, and evaluates a fixed two-input linear model. Independent expected logits are(.25,-3). A dashed separate training-restart branch requires optimizer/schedule/sampler/random state; session continuation additionally requires the appropriate DOGMA carry or Hermon Transformer cache. Weight-only inference parity is not restart equivalence.

All figures use editable vector sources, numbered captions and semantic TXT companions. Shape, position, solid/dashed lines and explicit labels preserve meaning in grayscale. Charts are generated from the tested reference, not invented visual data. Original artwork; no copied textbook illustrations.
