.PHONY: help
.DEFAULT_GOAL := help

RELEASE = $(shell git rev-parse HEAD)

help:
	python3 -m src --help

install:
	uv sync

lock:
	uv lock

update:
	uv lock --upgrade
	uv sync

format:
	uv run ruff format src tests 
	uv run ruff check  src tests --fix

lint:
	uv run ruff format src tests --check
	uv run ruff check  src tests
	uv run mypy src tests

test:
	uv run python -m pytest --cov

test-ci:
	uv run python -m pytest tests

run:
	python3 -m src