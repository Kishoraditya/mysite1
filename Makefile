.PHONY: build run test lint format migrate static shell clean help

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER_EXEC = $(DOCKER_COMPOSE) exec web
MANAGE_PY = python manage.py

help:
	@echo "Available commands:"
	@echo "  make build       - Build Docker containers"
	@echo "  make run         - Run the application"
	@echo "  make test        - Run tests with pytest"
	@echo "  make lint        - Run linting tools"
	@echo "  make format      - Format code with isort and black"
	@echo "  make migrate     - Run database migrations"
	@echo "  make static      - Collect static files"
	@echo "  make shell       - Open Django shell"
	@echo "  make clean       - Remove Docker containers and volumes"

build:
	$(DOCKER_COMPOSE) build

run:
	$(DOCKER_COMPOSE) up

test:
	$(DOCKER_EXEC) pytest --cov=. --cov-report=html

lint:
	$(DOCKER_EXEC) flake8 .
	$(DOCKER_EXEC) isort --check-only --profile black .

format:
	$(DOCKER_EXEC) isort --profile black .
	$(DOCKER_EXEC) black .

migrate:
	$(DOCKER_EXEC) $(MANAGE_PY) migrate

static:
	$(DOCKER_EXEC) $(MANAGE_PY) collectstatic --noinput

shell:
	$(DOCKER_EXEC) $(MANAGE_PY) shell

clean:
	$(DOCKER_COMPOSE) down -v
