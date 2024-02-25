.PHONY: format
format:
	black -t py39 meggie

.PHONY: check
check:
	black --check -t py39 meggie
	pylama meggie

.PHONY: test
test:
	pytest -s

.PHONY: update_docs
update_docs:
	rm -fr docs_updated
	cp -fr docs docs_updated
	python update_docs.py docs_updated

.PHONY: serve_docs
serve_docs: update_docs
	mkdocs serve

.PHONY: cov
cov:
	coverage run --source=meggie -m pytest && coverage report
