# EVO-02 review record

Date: 2026-09-06. Outline: distinguish analogy, abstraction and literal model; sequence transfer versus regulatory control; a minimal stateful response versus an instantaneous gate; exact recurrence, limits and controls; three update timescales; exercises.

Sources inspected: Crick (1970), [original article reprint](https://www.dna.caltech.edu/courses/cs191/paperscs191/CrickCentralDogma1970.pdf), pages 561–563, including the explicit distinction between sequence transfer and control mechanisms; [publisher metadata](https://www.nature.com/articles/227561a0). The final scanned page contains a neighboring article that is not used. Cooper (2000), [Transcription in Prokaryotes](https://www.ncbi.nlm.nih.gov/books/NBK9850/), negative-control/cis/trans sections. These support a bounded biological account, not a comprehensive review of modern regulation.

Avoided source shortcuts: do not describe the full lac operon as a single binary switch, import the simplified lactose/inducer wording as a chemical binding model, or treat a protein-to-DNA control arrow as reverse translation. No clinical or organism-engineering claim is involved.

Original work: the discrete leaky-state recurrence, exact rational trajectory, closed-form proof and synthetic pulse example. Parameters have arbitrary teaching units and are not fitted to cells. This is not a gene-regulatory-network simulator or a reproduction of a published biological experiment.

The source-derived biological discussion is deliberately bounded; the rest of the chapter develops original computational definitions, counterexamples and experimental obligations. The nearest control for the new recurrence is an ordinary leaky integrator, not an AGI model. No genome, learning, inheritance or fitness mechanism is implemented by this example.

Figure review: solid sequence-transfer arrows and a separately typed inhibitory control line; explicit scope excluding a complete central-dogma map; an exact synthetic trajectory with step indices, units and both input and output boundary definitions. Internal review is not independent peer review. See CHAPTER_02_REPORT.md for verification.
