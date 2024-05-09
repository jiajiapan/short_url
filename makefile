.PHONY: venv setup fmt lint test

WORKDIR?=.
VENVDIR?=$(WORKDIR)/.venv
VENV=$(VENVDIR)/bin

venv:
	python3 -m venv $(VENVDIR)
	$(VENV)/python3 -m pip install --upgrade pip

setup:
	$(VENV)/pip3 install -r requirements.txt

fmt: setup
	$(VENV)/black $(WORKDIR)

lint: setup
	$(VENV)/black --check -diff $(WORKDIR)

test: setup
	$(VENV)/pytest -v