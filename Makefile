PYTHON ?= python3
MAIN := undergraduate-evolutor

.PHONY: graphs artifacts test pdf historical-pdf check-pdf manuscript-gate pedagogy

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

pdf: manuscript-gate

# Reproduce the preserved edition explicitly; never overwrite its committed PDF.
historical-pdf:
	$(PYTHON) scripts/audit_undergraduate.py --check
	$(PYTHON) scripts/build_undergraduate.py --check
	mkdir -p build/figures output/pdf
	for figure in book/figures/undergraduate/*.svg; do rsvg-convert --format=pdf --output="build/figures/$$(basename "$$figure" .svg).pdf" "$$figure" || exit; done
	cd tex && latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=../build $(MAIN).tex

check-pdf: manuscript-gate
	$(PYTHON) scripts/check_latex_log.py build/$(MAIN).log
