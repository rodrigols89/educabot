# ================================
# 🚀 MAKEFILE - PROJECT COMMANDS
# ================================

# Não ecoar comandos no terminal
.SILENT:

# Executar todas as linhas do target no mesmo shell
.ONESHELL:

# Shell padrão
SHELL := /bin/bash


# -------------------------------- ( Paths ) --------------------------------

ROOT := $(CURDIR)

VENV := $(ROOT)/.venv

PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip
UV := $(VENV)/bin/uv

RUFF := $(VENV)/bin/ruff
PYTEST := $(VENV)/bin/pytest
COVERAGE := $(VENV)/bin/coverage
PRECOMMIT := $(VENV)/bin/pre-commit


# ------------------------------- ( PHONY ) ---------------------------------

.PHONY: pre_lint lint \
		test post_test \
		precommit \


# ------------------------------- ( Linting ) -------------------------------

pre_lint:
	cd $(ROOT)
	$(RUFF) check --fix

lint: pre_lint
	cd $(ROOT)
	$(RUFF) check


# ------------------------------ ( pre-commit ) -----------------------------

precommit:
	cd $(ROOT)
	$(PRECOMMIT) run --all-files


# -------------------------------- ( Testing ) ------------------------------

test:
	cd $(ROOT)
	$(PYTEST) -s -x --cov=. -vv
	$(MAKE) --no-print-directory post_test

post_test:
	cd $(ROOT)
	$(COVERAGE) html
