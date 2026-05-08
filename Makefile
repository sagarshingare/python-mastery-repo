SHELL := /bin/bash

.PHONY: install test lint run-api build-image compose-up compose-down

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest

run-api:
	uvicorn api_development.fastapi_app:app --host 0.0.0.0 --port 8000

build-image:
	docker build -t python-mastery-repo:latest .

compose-up:
	docker-compose up --build -d

compose-down:
	docker-compose down
