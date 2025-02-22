.PHONY: format
format:
	black meggie

.PHONY: check
check:
	black --check meggie
	pylama meggie

.PHONY: test
test:
	pytest -s

.PHONY: update_docs
update_docs:
	rm -fr docs_updated
	cp -fr docs docs_updated
	python -m scripts.update_docs docs_updated

.PHONY: serve_docs
serve_docs:
	mkdocs serve

.PHONY: cov
cov:
	coverage run --source=meggie -m pytest && coverage report
