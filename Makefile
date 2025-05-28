# Makefile for managing the Python project with uv

.PHONY: help install test clean

help:
	@echo "Available targets:"
	@echo "  install    - Create virtual environment using uv and install dependencies"
	@echo "  test       - Run tests using pytest"
	@echo "  clean      - Remove the virtual environment and __pycache__ directories"

ensure-uv:
	@echo "+++ $@"
	@if ! command -v uv > /dev/null; then \
		echo "uv not found, installing with sudo pip install uv..."; \
		sudo pip install uv; \
	fi

uv.lock: pyproject.toml ensure-uv
	@echo "+++ $@"
	@uv lock

.venv/bin/activate: uv.lock
	@echo "+++ $@"
	@uv venv
	@uv sync --all-extras

install: .venv/bin/activate
	@echo "+++ $@"

test: .venv/bin/activate
	@echo "+++ $@"
	@.venv/bin/pytest tests/

clean:
	@echo "+++ $@"
	@rm -rf .venv
	@find . -type d -name "__pycache__" -exec rm -rf {} +

