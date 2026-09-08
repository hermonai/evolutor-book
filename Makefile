PYTHON ?= python3
MAIN := deep-evolutor-ch01-02
HISTORICAL_MAIN := undergraduate-evolutor
export PATH := /Library/TeX/texbin:$(PATH)

.PHONY: graphs artifacts test pdf historical-pdf check-pdf manuscript-gate pedagogy deep-artifacts review-pdf

pedagogy:
	$(PYTHON) scripts/build_pedagogy.py --check

manuscript-gate:
	$(PYTHON) scripts/require_active_manuscript.py

graphs:
	$(PYTHON) scripts/render_graphs.py

artifacts:
	$(PYTHON) scripts/chapter01_artifacts.py
	$(PYTHON) scripts/chapter02_artifacts.py

test:
	$(PYTHON) -m pytest

deep-artifacts:
	$(PYTHON) scripts/build_deep_chapter.py --check
	$(PYTHON) scripts/build_deep_chapter02.py --check

pdf: manuscript-gate deep-artifacts
	mkdir -p build/deep-figures output/pdf
	for figure in book/figures/deep/*.svg; do rsvg-convert --format=pdf --output="build/deep-figures/$$(basename "$$figure" .svg).pdf" "$$figure" || exit; done
	cd tex && latexmk -silent -xelatex -interaction=nonstopmode -halt-on-error -outdir=../build $(MAIN).tex
	$(PYTHON) scripts/check_latex_log.py build/$(MAIN).log
	cp build/$(MAIN).pdf output/pdf/$(MAIN).pdf

review-pdf: pdf
	$(PYTHON) scripts/review_deep.py

# Reproduce the preserved edition explicitly; never overwrite its committed PDF.
historical-pdf:
	$(PYTHON) scripts/audit_undergraduate.py --check
	$(PYTHON) scripts/build_undergraduate.py --check
	mkdir -p build/figures output/pdf
	for figure in book/figures/undergraduate/*.svg; do rsvg-convert --format=pdf --output="build/figures/$$(basename "$$figure" .svg).pdf" "$$figure" || exit; done
	cd tex && latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=../build $(HISTORICAL_MAIN).tex

check-pdf: manuscript-gate
	$(PYTHON) scripts/check_latex_log.py build/$(MAIN).log
