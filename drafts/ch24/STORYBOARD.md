# EVOD-24 storyboard

1. Token spans: an assigned mutation at base two affects three overlapping
   width-three tokens; token index and nucleotide coordinate are not interchangeable.
2. Information gate: token ACG contains target base two; causal attention on that
   token cannot erase the leaked target, while span [0,2) is legal context.
3. Joint strand action: A in orientation +1 maps to T in orientation -1;
   assigned even features stay fixed and odd features negate exactly.
4. Rotary geometry: two unit vectors rotate by base-coordinate phase; a common
   translation changes directions but not their relative score.
5. Layer relay: source eleven, global zero and query one occupy successive layer
   nodes. Offline two-layer relay is legal; a causal backward edge is forbidden.
6. Ragged kernel: gather only declared edges, normalize a legal row, reduce values;
   independent dense computation exists only as a small validation oracle.

Native editable TikZ, semantic TXT, meaningful captions, restricted claims and
color/line-style differentiation are required before local visual review.
