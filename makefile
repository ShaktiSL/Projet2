PYTHON = python3

.PHONY: doctest

doctest:
	@find . -name "*.py" | while read file; do \
		$(PYTHON) run_doctest.py $$file; \
	done
