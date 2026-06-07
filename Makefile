.PHONY: api test lint format

PYTHONPATH := .:packages/models:packages/pitml

api:
	PYTHONPATH=$(PYTHONPATH) uv run uvicorn apps.api.app.main:app --reload

test:
	PYTHONPATH=$(PYTHONPATH) uv run pytest

lint:
	PYTHONPATH=$(PYTHONPATH) uv run ruff check .

format:
	uv run ruff format .