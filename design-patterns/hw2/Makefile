help:
	python3 -m src --help

install: ## Install requirements
	uv sync

lock: ## Lock project dependencies
	uv lock

update: ## Update project dependencies
	uv lock --upgrade
	uv sync

format: ## Run code formatters
	uv run ruff format core infra tests 
	uv run ruff check  core infra tests  --fix

lint: ## Run code linters
	uv run ruff format core infra tests  --check
	uv run ruff check core infra tests 
	uv run mypy core infra tests 

test:  ## Run tests with coverage
	uv run python -m pytest --cov

test-ci:
	uv run python -m pytest tests

run:
	python -m infra.api.app