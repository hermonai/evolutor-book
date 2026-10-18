# Current complete candidate. The original Makefile is hash-frozen with Ch1–2.
PYTHON ?= python3
export PATH := /Library/TeX/texbin:/opt/homebrew/bin:$(PATH)
.PHONY: complete-book complete-book-fresh complete-book-render

complete-book:
	OMP_NUM_THREADS=1 $(PYTHON) scripts/build-convergence.py --through 52

complete-book-fresh:
	OMP_NUM_THREADS=1 $(PYTHON) scripts/build-convergence.py --through 52 --refresh-assets

complete-book-render:
	$(PYTHON) scripts/review-convergence.py --pages all
