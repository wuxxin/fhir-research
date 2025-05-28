import subprocess
import os
import pytest
from pathlib import Path
import tempfile  # For creating a temporary file name

# Define the project root relative to this test file
PROJECT_ROOT = Path(__file__).parent.parent
MARIMO_NOTEBOOK_SCRIPT_MD = PROJECT_ROOT / "notebooks" / "hdl_visualization.md"
TEST_OUTPUT_IMAGE = PROJECT_ROOT / "tests" / "test_hdl_plot.png"


@pytest.fixture
def cleanup_files():
    # Fixture to clean up the generated image file and temporary script
    temp_script_path_to_clean = None  # To store the path of the temporary script

    def _set_temp_script_path(path):
        nonlocal temp_script_path_to_clean
        temp_script_path_to_clean = path

    yield _set_temp_script_path  # Pass the setter to the test

    if TEST_OUTPUT_IMAGE.exists():
        os.remove(TEST_OUTPUT_IMAGE)
    if temp_script_path_to_clean and Path(temp_script_path_to_clean).exists():
        os.remove(temp_script_path_to_clean)


def test_marimo_script_generates_image(cleanup_files):
    """
    Tests if the Marimo notebook's script logic, when converted to a .py file,
    successfully generates an output image.
    """
    notebook_md_path_str = str(MARIMO_NOTEBOOK_SCRIPT_MD.resolve())
    output_image_path_str = str(TEST_OUTPUT_IMAGE.resolve())

    # Path to the virtual environment's marimo and python executable
    venv_marimo_executable = str(PROJECT_ROOT / ".venv" / "bin" / "marimo")
    venv_python_executable = str(PROJECT_ROOT / ".venv" / "bin" / "python")

    # Create a temporary file for the converted Python script
    # We'll use a fixed name in the tests directory for simplicity, managed by cleanup
    temp_script_py = PROJECT_ROOT / "tests" / "temp_hdl_visualization_script.py"
    cleanup_files(str(temp_script_py))  # Register for cleanup

    # 1. Convert Marimo notebook to Python script
    convert_command = [
        venv_marimo_executable,
        "convert",
        notebook_md_path_str,
        "-o",
        str(temp_script_py),
    ]

    print(f"Running convert command: {' '.join(convert_command)}")
    convert_process_result = subprocess.run(
        convert_command, capture_output=True, text=True, cwd=str(PROJECT_ROOT)
    )

    print("Convert STDOUT:", convert_process_result.stdout)
    print("Convert STDERR:", convert_process_result.stderr)
    assert convert_process_result.returncode == 0, (
        f"Marimo convert failed: {convert_process_result.stderr}"
    )
    assert temp_script_py.exists(), f"Converted script '{temp_script_py}' was not created."

    # 2. Execute the converted Python script
    run_command = [
        venv_python_executable,
        str(temp_script_py),
        "--output-image",
        output_image_path_str,
    ]

    print(f"Running execution command: {' '.join(run_command)}")
    process_result = subprocess.run(
        run_command, capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=120
    )  # Added timeout

    print("Execution STDOUT:", process_result.stdout)
    print("Execution STDERR:", process_result.stderr)
    assert process_result.returncode == 0, (
        f"Converted script execution failed: {process_result.stderr}"
    )

    # Check if the output image file was created
    assert TEST_OUTPUT_IMAGE.exists(), (
        f"Output image file '{output_image_path_str}' was not created."
    )
    assert TEST_OUTPUT_IMAGE.stat().st_size > 0, (
        f"Output image file '{output_image_path_str}' is empty."
    )

    # Cleanup is handled by the fixture (no explicit call needed here)
