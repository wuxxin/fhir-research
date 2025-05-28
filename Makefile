# Makefile for managing the Python project with uv

.PHONY: help install test clean

help:
	@echo "Available targets:"
	@echo "  buildenv   - Create build environment"
	@echo "  test       - Run Tests"
	@echo "  lint       - Run Linting"
	@echo "  clean      - Remove test and build artifacts"

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

buildenv: .venv/bin/activate
	@echo "+++ $@"

test: buildenv
	@echo "+++ $@"
	@mkdir -p build
	@uv run scripts/generate_fhir_example.py
	@uv run notebooks/hdl_visualize.py -o build/hdl-matplotlib.png

lint: buildenv
	@echo "+++ $@"
	@uv run flake8 . --exclude .venv --count --select=E9,F63,F7,F82 --show-source --statistics
	@uv run flake8 . --exclude .venv --count --exit-zero --max-complexity=10 --max-line-length=95 --statistics

clean:
	@echo "+++ $@"
	@rm -rf .venv __marimo__ .pytest_cache build
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@for i in uv.lock; do if test -e "$$i"; then rm "$$i"; fi; done
