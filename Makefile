# Makefile for managing the Python project with uv

.PHONY: help buildenv test docs lint clean
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | sort

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
	@uv pip install -e "."

buildenv: .venv/bin/activate ## Create build environment
	@echo "+++ $@"

test: buildenv ## Run Tests
	@echo "+++ $@"
	@mkdir -p build
	@uv run scripts/generate_fhir_example.py

docs: buildenv ## Make Documentation and Onlinepage
	@echo "+++ $@"
	@mkdir -p build/test build/site
	@uv run notebooks/hdl_visualize.py -o build/test/hdl-matplotlib.png
	@uv run mkdocs build -f mkdocs.yml
	@printf "n\n" | uv run marimo export html-wasm notebooks/hdl_visualize.py -o build/site/marimo --mode run

lint: buildenv ## Run Linting
	@echo "+++ $@"
	@uv run flake8 . --exclude .git,__pycache__,build,.venv \
		--select=E9,F63,F7,F82 --show-source --statistics
	@uv run flake8 . --exclude .git,__pycache__,build,.venv \
		--count --exit-zero --max-complexity=10 --max-line-length=95 --statistics --output-file build/test/flake8.txt

clean: ## Remove test and build artifacts
	@echo "+++ $@"
	@rm -rf .venv __marimo__ .pytest_cache build
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@for i in uv.lock; do if test -e "$$i"; then rm "$$i"; fi; done
