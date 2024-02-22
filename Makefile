.PHONY: format
format:
	black -t py39 meggie

.PHONY: check
check:
	black --check -t py39 meggie
	pylama meggie
