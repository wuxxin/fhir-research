# Makefile for managing the Python project with uv

.PHONY: help install test clean

# Default Python interpreter to use for creating the virtual environment (uv might not need this explicitly)
# PYTHON ?= python3 
# Name of the virtual environment directory
VENV_DIR ?= .venv

help:
	@echo "Available targets:"
	@echo "  install    - Create virtual environment using uv and install dependencies from uv.lock"
	@echo "  test       - Run tests using pytest"
	@echo "  clean      - Remove the virtual environment and __pycache__ directories"

# Target to create virtual environment and install dependencies
# Assumes uv.lock is present and managed
install: $(VENV_DIR)/pyvenv.cfg

$(VENV_DIR)/pyvenv.cfg: pyproject.toml uv.lock
	@echo "Creating virtual environment in $(VENV_DIR) using uv..."
	@uv venv $(VENV_DIR)
	@echo "Installing dependencies from uv.lock using uv..."
	# Let's use the same uv for sync.
	@uv pip sync --python $(VENV_DIR)/bin/python uv.lock
	@echo "Installation complete. Activate with: source $(VENV_DIR)/bin/activate"
	@# Touch a file inside the venv to signify completion for make, pyvenv.cfg is standard.
	@# No, pyvenv.cfg is created by 'uv venv'. The rule depends on it.

# Target to run tests
test: $(VENV_DIR)/pyvenv.cfg
	@echo "Running tests..."
	@$(VENV_DIR)/bin/pytest tests/

# Target to clean up
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV_DIR)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Clean up complete."
