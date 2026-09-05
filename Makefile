PYTHON ?= python3
MAIN := evolutor

.PHONY: graphs test pdf check-pdf

graphs:
	$(PYTHON) scripts/render_graphs.py

test:
	$(PYTHON) -m pytest

pdf: graphs
	mkdir -p build/figures output/pdf
	rsvg-convert --format=pdf --output=build/figures/evo-g04.pdf book/figures/evo-g04.svg
	cd tex && latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=../build $(MAIN).tex
	cp build/$(MAIN).pdf output/pdf/$(MAIN).pdf

check-pdf:
	$(PYTHON) scripts/check_latex_log.py build/$(MAIN).log
