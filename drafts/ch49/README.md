# Chapter 49: Streaming, language, code and persistent agents

Authored-LaTeX standalone integration candidate. Package concepts and exercises are retained and expanded; see ../../research/integration/ch49/package-adoption.md for every incoming section. This is local author review, not independent scientific acceptance.

Use the Python 3.13.6 environment with pytest, Pillow and torch 2.10.0 (torch is used by actual earlier-model integration tests). The default /usr/bin/python3 on this Mac lacks torch/Pillow. TeX and Poppler are host installations.

```sh
/Users/wenyan/.pyenv/versions/3.13.6/bin/python3 -m pytest tests/test_ch49_reference.py -q -o addopts=''
/Users/wenyan/.pyenv/versions/3.13.6/bin/python3 drafts/ch49/build.py --render
/Users/wenyan/.pyenv/versions/3.13.6/bin/python3 drafts/ch49/build.py --check
```

The builder derives tables/results and whole-function listings from reference.py, compiles authored manuscript.tex with the local review wrapper, rejects overfull boxes and unresolved references/citations, and renders all pages plus color/grayscale contact sheets under tmp/pdfs/ch49-review/. Generated assets are in build/ch49/; final PDF is output/pdf/evolutor-ch49-review.pdf. Short functions reserve enough page space; longer source functions may continue with line numbers. Source/PDF hashes and actual review scope live in ../../research/integration/ch49/local-review.json.

Run only owned chapter tests/builds during parallel authoring. Shared navigation, cumulative compilation, whole-repository regression and final integration are the original integrator's work. No commit, staging or push is performed by this batch.
