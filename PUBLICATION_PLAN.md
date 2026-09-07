# Deep-edition publication plan

The active book metadata identifies edition 4-deep, status architecture-only-no-manuscript, an empty chapter list and no main entry point. The default PDF gate rejects this state deliberately. Never rename a preserved PDF or point the deep manifest at old source to bypass the gate.

The next manuscript milestone creates a distinct tex/deep/ source tree and distinct deep-edition PDF filename after Chapter 1 meets CHAPTER_STANDARD.md. Do not create these files during the planning-only milestone. Retain LaTeX equations, theorem/proof environments where useful, algorithms, source-linked code, references, index and selective glossary. Render and inspect every actual page before delivery; no PDF/UA claim without appropriate accessibility work.

Historical reproduction is explicit: make historical-pdf uses tex/undergraduate-evolutor.tex and builds only under build/. The committed output/pdf/undergraduate-evolutor.pdf remains byte-identical. The historical gate accepts the preserved edition metadata for regression tests but not as the active deep manuscript.

Plan checks: python3 scripts/build_deep_plan.py --check and the complete pytest suite. Changes are confined to astra-deep-rewrite. Never merge to main or modify protected historical branches implicitly; publication pushes require user authorization.
