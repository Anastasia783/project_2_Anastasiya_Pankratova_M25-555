install:
	poetry install

run:
	poetry run project

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

test:
	poetry run python -m pytest

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf data
	rm -f db_meta.json

.PHONY: install run lint format test clean