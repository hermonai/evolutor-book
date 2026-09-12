PYTHON ?= python3
.PHONY: textbook textbook-check
textbook:
	$(PYTHON) scripts/build-textbook.py
textbook-check:
	$(PYTHON) scripts/check-textbook.py
