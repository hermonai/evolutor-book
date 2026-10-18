# Chapter 41 figure decisions (before prose)

1. SSA arithmetic data edges a,b to n; ordered effect chain retrieval then tool. Show effects cannot disappear because docs have no output use.
2. Before/after exact integer folding and DCE, retaining original operation IDs for sum and effect ordering. No substitution of floating-point reassociation.
3. Live-value timeline: allocate result while both operands remain live; release after use. Explain count proxy versus real bytes and external handle pins.
