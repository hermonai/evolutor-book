PYTHON ?= python3
MAIN := evolutor

.PHONY: graphs artifacts test pdf check-pdf

graphs:
	$(PYTHON) scripts/render_graphs.py

artifacts:
	$(PYTHON) scripts/chapter01_artifacts.py

test:
	$(PYTHON) -m pytest

pdf: graphs artifacts
	mkdir -p build/figures output/pdf
	for figure in book/figures/*.svg; do rsvg-convert --format=pdf --output="build/figures/$$(basename "$$figure" .svg).pdf" "$$figure" || exit; done
	cd tex && latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=../build $(MAIN).tex
	cp build/$(MAIN).pdf output/pdf/$(MAIN).pdf

check-pdf:
	$(PYTHON) scripts/check_latex_log.py build/$(MAIN).log
