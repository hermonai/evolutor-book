# Chapter 7 visual reasoning plan

Original editable TikZ figures; semantic TXT companions explain every mechanism.
No copied artwork or ASCII diagrams. Numerical plots are generated from tested code.

## Figure 7.1: Affine recurrence dependency contract

Source: figures/01-state-update.tex

Previous state is multiplied coordinatewise by retention a; write b is added. Current input and parameters produce a and b without a dependency on the previous recurrent state in this teaching layer. Readout is a separate map. Dashed gate arrow controls multiplication; solid arrows carry values. State N is computational, not a physical genomic quantity.

## Figure 7.2: Two homogeneous decay coordinates

Source: figures/02-timescales.tex

From initial value one and zero drive, curves exp(-step) and exp(-0.1 step) compare retention at internal intervals of length one. Line styles distinguish coordinates in grayscale. The horizontal coordinate is not seconds or base pairs, and retention is not measured learned ability.

## Figure 7.3: Why time invariance produces a shared causal kernel

Source: figures/03-kernel.tex

Four by four lower triangular matrix has entry 0.5^(row-column) on and below the diagonal, zero above. Columns are inputs x_j and rows outputs y_t. Equal lags have equal coefficients with zero initial state and unit gains. Input-dependent transitions generally remove this fixed-kernel structure.

## Figure 7.4: Compose adjacent intervals without reordering

Source: figures/04-scan-tree.tex

Pairs p1,p2 combine to p1:2 and p3,p4 to p3:4. Combine these to p1:4. Reconstruct missing p1:3 by composing p1:2 with p3. The four requested prefixes are p1,p1:2,p1:3,p1:4. Solid edges are reduction; dashed edges reconstruct. This is a computational DAG, not a claim that the Python loops execute concurrently.

## Figure 7.5: Same shape, three state policies

Source: figures/05-boundaries.tex

Padding uses identity (1,0) and leaves the state unchanged. Reset before consuming a record's current input uses (0,b), removing previous-record information but keeping the current write. A chunk continuation uses normal (a,b) with actual carry. Loss masks and coefficient-network buffers are separate contracts.
