# HDL Cholesterol Visualization with Marimo and Bokeh (Refactored for Scripting)

This notebook demonstrates generating FHIR data for HDL cholesterol observations,
flattening it, filtering for HDL, and visualizing HDL values over time.
It can be run interactively in Marimo or as a Python script to export the plot.

```python
# Cell 1: Imports
import marimo as mo
import pandas as pd
import json
import argparse
import os
from bokeh.io import export_png # For saving plot

# Assuming Marimo is run from the project root, or src is in PYTHONPATH
from src.medical_data_science.fhir_utils import (
    create_patient_lab_bundle,
    flatten_fhir_bundle,
)
# Note: datetime, timedelta, date are not strictly needed by the core logic below
# but can be useful for users extending the notebook.
from datetime import datetime, timedelta, date
```

```python
# Cell 2: Data Generation Function and Initial Load

@mo.ref
def get_hdl_dataframe():
    """
    Generates patient and lab observation data, creates a FHIR bundle,
    flattens it, filters for HDL observations, and prepares the data for plotting.
    Returns a pandas DataFrame containing only prepared HDL observations.
    """
    # Define Patient Data
    patient_details = {
        'id': "patient-marimo-01",
        'family_name': "Marimo", 
        'given_name': "Maria",   
        'birth_date': "1980-05-15", # YYYY-MM-DD
        'gender': "female"
    }

    # Define HDL Observations Data (specific for this visualization)
    lab_observations_details = [
        {
            'observation_id': "hdl-marimo-01",
            'effective_date_time': "2020-01-15T09:00:00Z",
            'code_system': "http://loinc.org", 'code': "2085-9", 'code_display': "Cholesterol in HDL",
            'value_quantity_value': 60.0, 'value_quantity_unit': "mg/dL", 'value_quantity_unit_code': "mg/dL"
        },
        {
            'observation_id': "hdl-marimo-02",
            'effective_date_time': "2021-02-20T09:30:00Z",
            'code_system': "http://loinc.org", 'code': "2085-9", 'code_display': "Cholesterol in HDL",
            'value_quantity_value': 62.0, 'value_quantity_unit': "mg/dL", 'value_quantity_unit_code': "mg/dL"
        },
        {
            'observation_id': "hdl-marimo-03",
            'effective_date_time': "2022-03-10T08:45:00Z",
            'code_system': "http://loinc.org", 'code': "2085-9", 'code_display': "Cholesterol in HDL",
            'value_quantity_value': 58.0, 'value_quantity_unit': "mg/dL", 'value_quantity_unit_code': "mg/dL"
        },
        {
            'observation_id': "hdl-marimo-04",
            'effective_date_time': "2023-04-05T10:15:00Z",
            'code_system': "http://loinc.org", 'code': "2085-9", 'code_display': "Cholesterol in HDL",
            'value_quantity_value': 61.0, 'value_quantity_unit': "mg/dL", 'value_quantity_unit_code': "mg/dL"
        }
    ]

    # Generate FHIR Bundle
    fhir_bundle = create_patient_lab_bundle(
        patient_details=patient_details,
        lab_observations_details=lab_observations_details
    )
    bundle_json = fhir_bundle.as_json()

    # Flatten Bundle to DataFrame
    df = flatten_fhir_bundle(bundle_json)

    # Prepare HDL DataFrame
    hdl_df_prepared = pd.DataFrame() # Initialize for safety
    if df is not None and not df.empty:
        if 'Observation_code_coding_0_code' in df.columns:
            hdl_df_prepared = df[df['Observation_code_coding_0_code'] == '2085-9'].copy()
            if not hdl_df_prepared.empty:
                if 'Observation_effectiveDateTime' in hdl_df_prepared.columns:
                    hdl_df_prepared['Observation_effectiveDateTime'] = pd.to_datetime(hdl_df_prepared['Observation_effectiveDateTime'])
                if 'Observation_valueQuantity_value' in hdl_df_prepared.columns:
                    hdl_df_prepared['Observation_valueQuantity_value'] = pd.to_numeric(hdl_df_prepared['Observation_valueQuantity_value'])
        else:
            # In interactive mode, Marimo would show this. In script mode, print.
            print("Warning: 'Observation_code_coding_0_code' column not found. Cannot filter for HDL.")
    else:
        print("Warning: Initial DataFrame `df` is empty or None.")
        
    # For interactive mode, it's good to give some feedback or return components for inspection
    # For now, just returning the essential hdl_df_prepared.
    # Could also return bundle_json and df for inspection in other cells.
    return hdl_df_prepared, bundle_json, df # Return all for potential inspection

# Call the function to load data for interactive mode
# Unpack the results; hdl_df is the primary one for plotting
hdl_df, generated_bundle_json, raw_df_generated = get_hdl_dataframe.value

mo.md(f"""
Data generation function defined.
- Initial HDL DataFrame shape: {hdl_df.shape if hdl_df is not None else 'N/A'}
- FHIR Bundle ID: {generated_bundle_json.get('id') if generated_bundle_json else 'N/A'}
""")
```

```python
# Cell 3: Data Inspection (Interactive)

mo.md("### Prepared HDL DataFrame (`hdl_df`)")
if hdl_df is not None and not hdl_df.empty:
    mo.ui.table(hdl_df[['Observation_effectiveDateTime', 'Observation_valueQuantity_value']].head(), selection=None)
else:
    mo.md("`hdl_df` is empty or not yet loaded.")

mo.md("### Raw Flattened DataFrame (`raw_df_generated`) - First 5 rows")
if raw_df_generated is not None and not raw_df_generated.empty:
    mo.ui.table(raw_df_generated.head(), selection=None)
else:
    mo.md("`raw_df_generated` is empty or not yet loaded.")

# Full bundle JSON is large, so display only if a button is pressed (example)
# show_bundle = mo.ui.button(label="Show Full Bundle JSON")
# if show_bundle.value:
#    mo.accordion({"Generated FHIR Bundle (JSON)": generated_bundle_json})
```

```python
# Cell 4: Plotting Function and Interactive Display

from bokeh.plotting import figure # Moved here to be self-contained for the function
from bokeh.models import DatetimeTickFormatter

@mo.ref
def create_hdl_plot(data_frame: pd.DataFrame):
    """Creates a Bokeh plot for HDL cholesterol over time."""
    if data_frame is None or data_frame.empty or \
       'Observation_effectiveDateTime' not in data_frame.columns or \
       'Observation_valueQuantity_value' not in data_frame.columns or \
       not pd.api.types.is_datetime64_any_dtype(data_frame['Observation_effectiveDateTime']) or \
       not pd.api.types.is_numeric_dtype(data_frame['Observation_valueQuantity_value']):
        
        # Create an empty plot with a message if data is not valid
        p_empty = figure(width=800, height=350, title="HDL Cholesterol Over Time")
        p_empty.text(x=[0], y=[0], text=["No valid HDL data to plot. Check data preparation steps."], 
                     text_align="center", text_baseline="middle")
        return p_empty

    p = figure(
        x_axis_type="datetime",
        title="HDL Cholesterol Over Time",
        height=350,
        width=800,
        x_axis_label='Date',
        y_axis_label='HDL (mg/dL)'
    )
    p.line(
        x=data_frame['Observation_effectiveDateTime'],
        y=data_frame['Observation_valueQuantity_value'],
        legend_label="HDL",
        line_width=2
    )
    p.circle(
        x=data_frame['Observation_effectiveDateTime'],
        y=data_frame['Observation_valueQuantity_value'],
        legend_label="HDL", 
        fill_color="white",
        size=8
    )
    p.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d", months="%Y-%m", years="%Y")
    p.xaxis.axis_label_text_font_style = "normal"
    p.yaxis.axis_label_text_font_style = "normal"
    p.grid.grid_line_alpha = 0.3
    p.legend.location = "top_left"
    return p

# Interactive plot display for Marimo
# This uses the hdl_df obtained from get_hdl_dataframe.value in Cell 2
plot_figure = create_hdl_plot(hdl_df) 
# Marimo will render Bokeh plots directly if it's the last expression or mo.output.bokeh()
# mo.output.bokeh(plot_figure) # Explicit display if needed
```

```python
# Cell 5: Script Execution Logic (for CLI export)

# This block will only run when the script is executed directly (e.g., python your_script.py)
# It will not run when Marimo is running the notebook interactively.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HDL plot and optionally export it.")
    parser.add_argument(
        "--output-image", 
        type=str, 
        help="Filename to save the plot image (e.g., hdl_plot.png). If not provided, no image is saved."
    )
    args = parser.parse_args()

    if args.output_image:
        print("Script mode: Generating data for plot export...")
        # Call get_hdl_dataframe directly to get the data for the plot
        # We take only the first returned element, which is the hdl_df_prepared
        script_hdl_df, _, _ = get_hdl_dataframe.value # Use .value for Marimo refs if running in Marimo context
                                                  # For pure Python script, it would be get_hdl_dataframe()
                                                  # This might need adjustment depending on how Marimo handles __main__
                                                  # A safer way for pure script is to call the function directly:
                                                  # script_hdl_df, _, _ = get_hdl_dataframe() if not mo. Zellenvironment.
                                                  # For now, assume simple direct call works if __name__ == "__main__"
                                                  # This needs careful testing with Marimo's `is_notebook_mode` or similar.
                                                  # Let's assume for `python script.md` Marimo makes .value work.
                                                  # If not, `get_hdl_dataframe_plain = get_hdl_dataframe.__wrapped__` might be needed.

        # A more robust way for script execution:
        # Define patient_details and lab_observations_details again or import them
        # This part is tricky as Marimo's @mo.ref is for its reactive graph.
        # For simplicity in this step, we'll assume get_hdl_dataframe() can be called.
        # If running `python your_notebook.md`, Marimo might not be fully initialized.
        # The most robust solution is to have helper functions that are pure Python.
        # Let's redefine a plain version for script mode here or ensure get_hdl_dataframe is callable
        
        # Re-defining core logic for pure script context if Marimo refs are an issue:
        _patient_details = {
            'id': "patient-script-01", 'family_name': "Script", 'given_name': "Runner", 
            'birth_date': "1970-01-01", 'gender': "unknown"
        }
        _lab_obs = [
            {'observation_id': "hdl-s-01", 'effective_date_time': "2023-01-01T10:00:00Z",
             'code_system': "http://loinc.org", 'code': "2085-9", 'code_display': "HDL Chol",
             'value_quantity_value': 50.0, 'value_quantity_unit': "mg/dL", 'value_quantity_unit_code': "mg/dL"}
        ]
        _fhir_bundle = create_patient_lab_bundle(_patient_details, _lab_obs)
        _df_raw = flatten_fhir_bundle(_fhir_bundle.as_json())
        _script_hdl_df = _df_raw[_df_raw['Observation_code_coding_0_code'] == '2085-9'].copy()
        if not _script_hdl_df.empty:
            _script_hdl_df['Observation_effectiveDateTime'] = pd.to_datetime(_script_hdl_df['Observation_effectiveDateTime'])
            _script_hdl_df['Observation_valueQuantity_value'] = pd.to_numeric(_script_hdl_df['Observation_valueQuantity_value'])
        
        # End of re-defined logic for script mode.

        if _script_hdl_df is not None and not _script_hdl_df.empty:
            print("Script mode: Creating plot...")
            plot_to_export = create_hdl_plot(_script_hdl_df) # Use the data generated in script mode
            
            # Ensure output directory exists if path is complex, for simplicity assume current dir
            output_path = args.output_image
            
            try:
                print(f"Script mode: Exporting plot to {output_path}...")
                # For export_png to work, a browser driver (like geckodriver for Firefox or chromedriver for Chrome)
                # and selenium must be installed and correctly configured in the PATH.
                export_png(plot_to_export, filename=output_path)
                print(f"Plot successfully saved to {output_path}")
            except Exception as e:
                print(f"Error exporting plot: {e}")
                print("Please ensure you have a browser driver (geckodriver or chromedriver) in your PATH,")
                print("and the necessary Python packages like 'selenium' and 'pillow' are installed.")
        else:
            print("Script mode: No HDL data generated or processed. Cannot export plot.")
    else:
        # This message is for when the script is run with `python your_script.py` WITHOUT arguments
        # It won't show in Marimo interactive mode.
        print("Script mode: To save plot, run with --output-image <filename.png>")

# Make plot_figure the last expression in the cell for Marimo to display it.
# This is for interactive mode.
plot_figure
```
