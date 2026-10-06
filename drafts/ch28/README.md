# EVOD-28 / locally authored integration candidate

Original derive–implement–trace–test treatment of weighted collective algebra, independent autograd and scalar derivatives, labeled reconstruction, matrix operators and pinned raw-byte inference reload.

- 46 chapter tests; five complete-function listings; six editable TikZ illustrations with semantic TXT companions; twenty worked exercises.
- Incoming package preserved in staging and its metadata under research/integration/ch28/incoming/. This chapter is a semantic rewrite, not a bulk archive copy.
- Full-book assembly uses authored LaTeX; independent scientific/reader review and publication acceptance remain open.

Use Python 3.13.6; Evolutor tests require the installed PyTorch 2.10.0. From this repository:

```sh
OMP_NUM_THREADS=1 /Users/wenyan/.pyenv/versions/3.13.6/bin/python3 -m pytest tests/test_ch28_reference.py -q -o addopts=''
OMP_NUM_THREADS=1 /Users/wenyan/.pyenv/versions/3.13.6/bin/python3 drafts/ch28/build.py --render
/Users/wenyan/.pyenv/versions/3.13.6/bin/python3 drafts/ch28/build.py --check
/Users/wenyan/.pyenv/versions/3.13.6/bin/python3 scripts/build-convergence.py --through 28 --refresh-assets
```

The standalone review PDF is generated under output/pdf/. A strict build rejects overfull boxes, missing characters, and unresolved/duplicate references. Local review is bound separately to source/PDF hashes and regression evidence. No acceptance status is inferred from a successful build.

Collective/matrix fixtures run locally, not across a process group. The named raw-byte demo is not safetensors, a full DOGMA/Hermon checkpoint, or an authenticated release format. A clean subprocess checks only fixed linear inference, not a training restart or hardware benchmark.
