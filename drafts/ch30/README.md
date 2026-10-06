# Chapter 30 — Runtime contracts and request lifecycles

Source candidate: evolutor-ch30-r01.zip. Incoming metadata is retained under
research/integration/ch30/incoming. The lifecycle toy was rewritten around one
integrated ownership, queue, terminal and cleanup contract.

Derive a serialized lifecycle with immutable request/model identity, fenced
leases and state revisions. Keep terminal reason, physical quiescence and cleanup
separate. Conservative launch reservations enforce item and byte bounds
independently of the total generation ceiling. Late work settles without output
commit; previously committed output has an explicit drain/discard policy.
Work and output obey different conservation identities.

Six editable TikZ plates/TXT companions, five complete tested listings and twenty
worked exercises expose the operational contract before throughput claims.

Run from this repository with Python 3.13. The verified local interpreter is
/Users/wenyan/.pyenv/versions/3.13.6/bin/python3:

    python3.13 -m pytest tests/test_ch30_reference.py -q -o addopts=''
    python3.13 drafts/ch30/build.py --render
    python3.13 drafts/ch30/build.py --check

46 tests include all 7,776 length-five event words against an independent
state-machine oracle, terminal permutations, deadlines, ABA reuse, invalid
UTF-8 results and release failure. A thread test uses an external lock;
it does not certify thread safety. Output: output/pdf/evolutor-ch30-review.pdf.
Source/PDF hashes and diagnostics live in build/ch30; author review is recorded
separately after inspection. No network server, durable journal, authorization
system, device kernel or complete DOGMA/HermonDNA engine is implemented.
Independent and cumulative acceptance remain open.
Do not run PDF-mutating builds alongside repository preservation tests.

Next: evolutor-ch31-r01.zip supplies the native-state candidate. All later packages
through evolutor-ch52-r01.zip remain tracked for sequential semantic integration
with their own source, test and review gates.
