SHELL := /bin/bash
PYTHON := $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null || echo python)

.PHONY: install test lint run-api build-image compose-up compose-down check validate py_compile

install:
	$(PYTHON) -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q

check: test py_compile

validate: check

py_compile:
	find . -name '*.py' -not -path './.venv/*' -not -path './.git/*' -not -path './python_mastery_repo.egg-info/*' | sort | xargs $(PYTHON) -m py_compile

run-api:
	$(PYTHON) -m uvicorn api_development.fastapi_app:app --host 0.0.0.0 --port 8000

build-image:
	docker build -t python-mastery-repo:latest .

compose-up:
	docker-compose up --build -d

compose-down:
	docker-compose down
