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
		open_db open_evolution \
		log_postgres log_redis log_evolution \
		server check_server kill_server \
		init_project init_service \
		service_status service_stop service_restart service_logs \
		menu


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

menu:
	cd $(ROOT)
	bash scripts/menu.sh


# ---------------------------- ( Docker Management ) ------------------------

start_compose:
	cd $(ROOT)
	docker compose up -d

down_compose:
	cd $(ROOT)
	docker compose down

restart_compose:
	cd $(ROOT)
	docker compose restart

build_compose:
	cd $(ROOT)
	docker compose up --build -d

clean_compose:
	docker stop $$(docker ps -aq) 2>/dev/null || true
	docker rm $$(docker ps -aq) 2>/dev/null || true
	docker rmi -f $$(docker images -aq) 2>/dev/null || true
	docker volume rm $$(docker volume ls -q) 2>/dev/null || true
	docker system prune -a --volumes -f


# ------------------------------- ( Docker Exec ) ---------------------------

open_db:
	docker exec -it educabot_postgres psql -U educabotuser -d educabot_db

open_evolution:
	docker exec -it educabot_evolution sh


# ----------------------------- ( Container Logs ) --------------------------

log_postgres:
	cd $(ROOT)
	docker logs -f educabot_postgres

log_redis:
	cd $(ROOT)
	docker logs -f educabot_redis

log_evolution:
	cd $(ROOT)
	docker logs -f educabot_evolution


# ------------------------------- ( Servers ) -------------------------------

server:
	cd $(ROOT)
	$(UVICORN) app.main:app \
		--host 0.0.0.0 \
		--port 8001 \
		--reload &

check_server:
	ss -ltnp '( sport = :8001 )' || true

kill_server:
	kill $$(lsof -t -i:8001) 2>/dev/null || true
	pkill -f "uvicorn app.main:app" 2>/dev/null || true


# -------------------------- ( Initialization Scripts ) ---------------------

init_project:
	cd $(ROOT)
	bash scripts/init_project.sh

init_service:
	cd $(ROOT)
	bash scripts/init_service.sh


# ------------------------------ ( Service Status ) -------------------------

service_status:
	cd $(ROOT)
	systemctl status educabot.service

service_stop:
	cd $(ROOT)
	systemctl stop educabot.service

service_restart:
	cd $(ROOT)
	systemctl restart educabot.service

service_logs:
	cd $(ROOT)
	journalctl -u educabot.service -f
