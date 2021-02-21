.DEFAULT_GOAL := all

.PHONY: all
all: check test

.PHONY: clean
clean:
	rm -rf *.pyc

.PHONY: check
check:
	flake8 .

.PHONY: test
test:
	nosetests

.PHONY: coverage
coverage:
	coverage run --source=. -m unittest discover
