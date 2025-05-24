import subprocess
import os
import pytest
from pathlib import Path

# Define the project root relative to this test file
# Assuming this test file is in 'tests/' directory at the project root
PROJECT_ROOT = Path(__file__).parent.parent 
MARIMO_NOTEBOOK_SCRIPT = PROJECT_ROOT / "notebooks" / "hdl_visualization.md"
TEST_OUTPUT_IMAGE = PROJECT_ROOT / "tests" / "test_hdl_plot.png" # Save in tests dir

@pytest.fixture
def cleanup_test_image():
    # Fixture to clean up the generated image file after the test runs
    yield
    if TEST_OUTPUT_IMAGE.exists():
        os.remove(TEST_OUTPUT_IMAGE)

def test_marimo_script_generates_image(cleanup_test_image):
    """
    Tests if the Marimo notebook, when run as a script,
    successfully generates an output image.
    Assumes necessary dependencies (including browser driver) are in PATH.
    """
    # Ensure the notebook path and output image path are absolute or correctly relative
    notebook_path_str = str(MARIMO_NOTEBOOK_SCRIPT.resolve())
    output_image_path_str = str(TEST_OUTPUT_IMAGE.resolve())

    # Command to execute the Marimo notebook as a script
    # Ensure that the execution context has the `src` directory in PYTHONPATH
    # This can be achieved by running pytest from the project root.
    command = [
        "python", 
        notebook_path_str,
        "--output-image", 
        output_image_path_str
    ]

    # Execute the command
    # We need to run this from the project root for `src` imports to work in the notebook
    process_result = subprocess.run(command, capture_output=True, text=True, cwd=str(PROJECT_ROOT))

    # Print stdout and stderr for debugging in case of failure
    print("STDOUT:", process_result.stdout)
    print("STDERR:", process_result.stderr)

    # Check if the script executed successfully
    assert process_result.returncode == 0, f"Marimo script execution failed with error: {process_result.stderr}"

    # Check if the output image file was created
    assert TEST_OUTPUT_IMAGE.exists(), f"Output image file '{output_image_path_str}' was not created."

    # Optionally, check if the file is not empty (basic check)
    assert TEST_OUTPUT_IMAGE.stat().st_size > 0, f"Output image file '{output_image_path_str}' is empty."

    # Cleanup is handled by the fixture
```
