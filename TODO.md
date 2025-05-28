# TODO - Project Refactoring Follow-up

This document outlines the state of the project refactoring, challenges encountered by the automated agent (Jules), and recommended next steps.

## Goal

- Refactoring the Marimo notebook (`hdl_visualization.md`) to:
    - Use Bokeh for interactive plotting.
    - Use a non-browser-dependent library for generating static image exports via CLI.
    - Support both interactive use and command-line image generation.

## Refactoring Steps

- Interactive mode (within Marimo environment) continues to use Bokeh.

- Command-line script mode (via `if __name__ == "__main__":`) was refactored to use Matplotlib for generating and saving PNG images, removing the browser dependency for this mode.

**Test Script Update (`tests/test_marimo_export.py`)**:
    - The test was updated to first convert the Marimo notebook (`.md`) to a temporary Python script (`.py`) using `marimo convert <notebook.md> --to script --output temp_script.py`.
    - It then executes this `temp_script.py` using the virtual environment's Python interpreter to test image generation.
    - it should not cleanup temp_script.py or other artifacts if test script errors

## Recommended Next Steps

1. install dependencies: run `make buildenv`
2. run tests: run `make test`
3. review errors, fix errors rerun tests
4. update README.md update TODO.md

