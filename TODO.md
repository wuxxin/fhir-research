# TODO - Project Refactoring Follow-up

This document outlines the state of the project refactoring, challenges encountered by the automated agent (Jules), and recommended next steps.

## Initial Goal

The primary goal was to refactor the project by:
- Removing `jupyterlab` and `selenium` dependencies.
- Deleting the Jupyter notebook, keeping only the Marimo notebook.
- Renaming `medical_data_science` to `mds` and `fhir_utils` to `fhirutils`.
- Refactoring the Marimo notebook (`hdl_visualization.md`) to:
    - Use Bokeh for interactive plotting.
    - Use a non-browser-dependent library for generating static image exports via CLI.
    - Support both interactive use and command-line image generation.
- Creating a `Makefile` for environment setup (`uv`) and testing (`pytest`).

## Refactoring Steps Completed by Agent

The agent successfully performed the following modifications to the codebase:
1.  **Dependency Changes**:
    - `jupyterlab` and `selenium` were removed from `pyproject.toml`.
    - `matplotlib` was added to `pyproject.toml`.
2.  **Directory/File Renaming**:
    - `src/medical_data_science` renamed to `src/mds`.
    - `src/mds/fhir_utils.py` renamed to `src/mds/fhirutils.py`.
    - Import paths in `notebooks/hdl_visualization.md` were updated.
3.  **Jupyter Notebook Removal**:
    - `notebooks/hdl_visualization.ipynb` was deleted.
4.  **Marimo Notebook Refactoring (`notebooks/hdl_visualization.md`)**:
    - Interactive mode (within Marimo environment) continues to use Bokeh.
    - Command-line script mode (via `if __name__ == "__main__":`) was refactored to use Matplotlib for generating and saving PNG images, removing the browser dependency for this mode.
    - Conditional logic (`if mo.get_context().execution_mode == 'notebook':`) was added to ensure Marimo-specific UI calls do not interfere with script execution.
5.  **Makefile Creation**:
    - A `Makefile` was added with `install` (using `uv venv` and `uv pip sync`), `test`, and `clean` targets.
6.  **Test Script Update (`tests/test_marimo_export.py`)**:
    - The test was updated to first convert the Marimo notebook (`.md`) to a temporary Python script (`.py`) using `marimo convert <notebook.md> --to script --output temp_script.py`.
    - It then executes this `temp_script.py` using the virtual environment's Python interpreter to test image generation.

## Testing Journey & Challenges

The agent encountered several challenges during the testing phase:

1.  **Initial Test Failures**:
    - A `SyntaxError` in `tests/test_marimo_export.py` (erroneously reported as a markdown fence). This was resolved.
    - A `SyntaxError` when `tests/test_marimo_export.py` attempted to run the `notebooks/hdl_visualization.md` file directly using `python notebooks/hdl_visualization.md`. This was due to the Python interpreter trying to parse Markdown content.

2.  **Attempts to Execute Marimo Notebook Correctly for CLI Testing**:
    - **`marimo run ...`**: The test script was modified to use `marimo run notebooks/hdl_visualization.md --output-image ...`.
        - This led to `FileNotFoundError` for `marimo` if not using the venv path. Corrected to use `.venv/bin/marimo`.
        - `marimo run` did not recognize `--output-image` as a script argument. Corrected to use `marimo run ... -- --output-image ...`.
        - **Persistent Timeout**: `marimo run` (even with correct arguments) caused the test process to hang and time out (after 400s). It was hypothesized that `marimo run` keeps the server/process alive and is not suitable for simple script execution and exit.

3.  **Shift to `marimo convert` then `python temp_script.py`**:
    - The test script was changed to first convert the notebook to a temporary `.py` file and then execute that.
    - **Persistent Timeout**: This approach also resulted in timeouts (400s for `make test`, despite a 120s timeout on the specific subprocess call).

4.  **Hypothesis for Timeouts with Bokeh Export**:
    - The timeouts were suspected to be caused by Bokeh's `export_png` function within the (converted) script, which requires a browser driver (`geckodriver` or `chromedriver`) and can hang or be very slow in headless environments if the driver is missing or misconfigured.

5.  **Attempt to Install Browser Drivers**:
    - An attempt was made to install `firefox-esr` and `geckodriver` via `apt-get`.
    - This failed because `sudo apt-get update` itself timed out repeatedly, indicating potential underlying VM or network connectivity issues for the agent.

## User Directive and Strategy Pivot

- Due to the persistent timeouts and the inability to install browser drivers, the user observed that the agent's VM might be stuck or unstable for such operations.
- The user directed the agent to **change the strategy**:
    - For command-line image generation, switch from Bokeh's `export_png` to a library without browser dependencies.
    - Matplotlib was chosen for this purpose.
- The agent then proceeded to add `matplotlib` as a dependency and refactor the Marimo notebook's script mode to use Matplotlib.

## State Before Last Submission (Commit: `feature/mds-refactor-matplotlib`)

The codebase was submitted with the following conditions:
- **`pyproject.toml`**: Updated with `matplotlib` dependency.
- **Marimo Notebook**: Refactored for Matplotlib in CLI mode.
- **Test Script**: Updated to use `marimo convert` and run the resulting Python script (which now uses Matplotlib).
- **`uv.lock`**: **NOT updated** to include `matplotlib`. The subtask to run `uv lock` was cancelled due to user concerns about VM stability.
- **`make install` (with Matplotlib)**: **NOT run** by the agent.
- **`make test` (with Matplotlib changes)**: **NOT run** by the agent.
- The user requested to push the changes for review in this state, acknowledging the skipped final steps.

## Recommended Next Steps

1.  **Update Lockfile**: Manually run `uv lock` (or `uv pip compile pyproject.toml -o uv.lock`) in your local environment to update `uv.lock` with Matplotlib and its sub-dependencies. Commit the updated `uv.lock`.
2.  **Install Dependencies**: Run `make install`. This will create a virtual environment (if not present) and install all dependencies using the (now updated) `uv.lock`.
3.  **Run Tests**: Execute `make test`. This will:
    - Convert the Marimo notebook to a Python script.
    - Run that script, which should now use Matplotlib to generate an image.
    - Verify that the image is created as expected.
    - Troubleshoot any test failures. Given the switch to Matplotlib, the previous timeout issues related to browser drivers should be resolved.
4.  **Code Review**: Review the submitted code changes, particularly:
    - The Matplotlib implementation in `notebooks/hdl_visualization.md`.
    - The logic in `tests/test_marimo_export.py`.
    - The `Makefile`.
5.  **Finalize**: Address any issues found during testing or review and merge.
