all: fmt lint migrations test

fmt:
	uv run ruff format
	uv run ruff check --select I --fix
	uv run ruff check --fix

lint:
	uv run ruff check .
	uv run mypy .

migrations:
	uv run alembic check

test:
	uv run pytest
