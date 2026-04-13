.PHONY: help install install-dev web run lint format typecheck test check clean

help:
	@echo "Claude Code Trainer - Available targets:"
	@echo "  make install       - Install dependencies"
	@echo "  make install-dev   - Install with dev tools (ruff, mypy, pytest)"
	@echo "  make web           - Run Gradio Web UI (http://localhost:7860)"
	@echo "  make run [ARGS]    - Run CLI (e.g., make run ARGS='translate --help')"
	@echo "  make lint          - Check code with ruff"
	@echo "  make format        - Format code with ruff"
	@echo "  make typecheck     - Type check with mypy"
	@echo "  make test          - Run pytest"
	@echo "  make check         - Run lint + typecheck + test"
	@echo "  make clean         - Remove __pycache__, .pytest_cache, etc."

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio pytest-mock ruff mypy

web:
	python app/web_ui.py

run:
	python app/main.py $(ARGS)

lint:
	ruff check app/ tests/

format:
	ruff format app/ tests/

typecheck:
	mypy app/

test:
	pytest tests/ -v

check: lint typecheck test
	@echo "✓ All checks passed!"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	rm -rf .coverage htmlcov/
	@echo "✓ Cleaned up!"

.DEFAULT_GOAL := help
