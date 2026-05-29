# ============================================================================
# 🚀 MAKEFILE - PROJECT COMMANDS                                            #
# ============================================================================

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

UVICORN := $(VENV)/bin/uvicorn
RUFF := $(VENV)/bin/ruff
PYTEST := $(VENV)/bin/pytest
COVERAGE := $(VENV)/bin/coverage
PRECOMMIT := $(VENV)/bin/pre-commit


# ------------------------------- ( PHONY ) ---------------------------------

.PHONY: pre_lint lint \
		precommit \
		test post_test \
		export_dev export_prod \
		start_compose down_compose restart_compose build_compose clean_compose \
		server check_server kill_server


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


# --------------------------- ( Project Management ) ------------------------

export_dev:
	cd $(ROOT)
	$(UV) export --dev --no-hashes -o requirements-dev.txt

export_prod:
	cd $(ROOT)
	$(UV) export --no-dev --no-hashes -o requirements.txt


# ---------------------------- ( Docker Management ) ------------------------

start_compose:
	cd $(ROOT)
	docker compose up -d

down_compose:
	cd $(ROOT)
	docker compose down

restart_compose:
	cd $(ROOT)
	docker restart $$(docker ps -q)

build_compose:
	cd $(ROOT)
	docker compose up --build -d

clean_compose:
	docker stop $$(docker ps -aq) 2>/dev/null || true
	docker rm $$(docker ps -aq) 2>/dev/null || true
	docker rmi -f $$(docker images -aq) 2>/dev/null || true
	docker volume rm $$(docker volume ls -q) 2>/dev/null || true
	docker system prune -a --volumes -f


# ------------------------------- ( Servers ) -------------------------------

server:
	cd $(ROOT)
	$(UVICORN) app.main:app \
		--host 0.0.0.0 \
		--port 8000 \
		--reload &

check_server:
	ss -ltnp '( sport = :8000 )' || true

kill_server:
	kill $$(lsof -t -i:8000) 2>/dev/null || true
	pkill -f "uvicorn app.main:app" 2>/dev/null || true
