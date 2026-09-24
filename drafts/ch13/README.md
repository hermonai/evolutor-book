# Chapter 13: Learning, structural adaptation and evolution

Standalone authored-LaTeX review candidate. Prior accepted editions are unchanged.

Read manuscript.tex; reference.py implements original teaching models, not laboratory or production systems. Results and printed listings are generated from tested code. Figure source is editable TikZ with semantic TXT companions. Twelve exercises include worked answers or evaluation rubrics.

From repository root:

```sh
python3 drafts/ch13/build.py --assets-only
python3 -m pytest tests/test_ch13_reference.py
python3 drafts/ch13/build.py --render
python3 drafts/ch13/build.py --check
```

Output: output/pdf/evolutor-ch13-review.pdf.

Source access is recorded in sources.tex. Independent specialist review, reader feedback and cumulative integration remain open.
