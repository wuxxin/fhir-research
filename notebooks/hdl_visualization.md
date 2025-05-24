# HDL Cholesterol Visualization with Marimo and Bokeh (Refactored)

This notebook demonstrates generating FHIR data for HDL cholesterol observations
using the refactored `fhir_utils`, flattening it into a pandas DataFrame, 
filtering for HDL observations, and visualizing the HDL values over time using Bokeh.

```python
import marimo as mo
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter
# datetime, timedelta, date are not directly used here anymore for data generation
# but might be useful for other ad-hoc manipulations if users extend the notebook.
from datetime import datetime, timedelta, date 
import json

# Assuming Marimo is run from the project root, or src is in PYTHONPATH
from src.medical_data_science.fhir_utils import (
    create_patient_lab_bundle, # Updated import
    flatten_fhir_bundle,
)
```

```python
# Cell 2: Data Generation

# Define Patient Data using the new dictionary structure
patient_details = {
    'id': "patient-marimo-01",
    'family_name': "Marimo", 
    'given_name': "Maria",   
    'birth_date': "1980-05-15", # YYYY-MM-DD
    'gender': "female"
}

# Define HDL Observations Data using the new list of dictionaries structure
# These are specific for HDL observations for this visualization
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
    { # Adding a fourth observation as per original example's count
        'observation_id': "hdl-marimo-04",
        'effective_date_time': "2023-04-05T10:15:00Z",
        'code_system': "http://loinc.org", 'code': "2085-9", 'code_display': "Cholesterol in HDL",
        'value_quantity_value': 61.0, 'value_quantity_unit': "mg/dL", 'value_quantity_unit_code': "mg/dL"
    }
]

# Generate FHIR Bundle using the refactored function
fhir_bundle = create_patient_lab_bundle(
    patient_details=patient_details,
    lab_observations_details=lab_observations_details
)

# Convert bundle to JSON dictionary
bundle_json = fhir_bundle.as_json()

# Flatten Bundle to DataFrame
# This df will contain all observations if more types were added to lab_observations_details
df = flatten_fhir_bundle(bundle_json)

mo.md(f"""
Data generation complete using refactored functions.
- Patient: {patient_details['given_name']} {patient_details['family_name']}
- FHIR Bundle ID: {bundle_json.get('id')}
- Raw DataFrame shape (all observations): {df.shape if df is not None else 'N/A'}
""")
```

```python
# Cell 3: Data Inspection

mo.md("### Generated FHIR Bundle (JSON)")
bundle_json # Marimo can render dictionaries directly

mo.md("### Raw Flattened DataFrame (All Observations)")
df # Marimo will render the DataFrame as a table. This shows all observations from the bundle.
```

```python
# Cell 4: Data Preparation for HDL Plotting

mo.md("### Preparing Data for HDL Cholesterol Plot")

hdl_df = pd.DataFrame() # Initialize empty DataFrame for safety

if df is not None and not df.empty:
    # Filter for HDL observations (LOINC code '2085-9')
    # The column name comes from the flattening logic: resourceType_key_subkey_...
    if 'Observation_code_coding_0_code' in df.columns:
        hdl_df = df[df['Observation_code_coding_0_code'] == '2085-9'].copy()
        mo.md(f"Filtered DataFrame `hdl_df` for HDL (code '2085-9') created. Shape: {hdl_df.shape}")
    else:
        mo.md(mo.Callout("Warning: 'Observation_code_coding_0_code' column not found in DataFrame. Cannot filter for HDL.", kind="warn"))

    if not hdl_df.empty:
        # Ensure 'Observation_effectiveDateTime' is in datetime format
        if 'Observation_effectiveDateTime' in hdl_df.columns:
            hdl_df['Observation_effectiveDateTime'] = pd.to_datetime(hdl_df['Observation_effectiveDateTime'])
        else:
            mo.md(mo.Callout("Warning: 'Observation_effectiveDateTime' column not found in `hdl_df`.", kind="warn"))

        # Ensure 'Observation_valueQuantity_value' is numeric
        if 'Observation_valueQuantity_value' in hdl_df.columns:
            hdl_df['Observation_valueQuantity_value'] = pd.to_numeric(hdl_df['Observation_valueQuantity_value'])
        else:
            mo.md(mo.Callout("Warning: 'Observation_valueQuantity_value' column not found in `hdl_df`.", kind="warn"))
        
        mo.md("#### Prepared HDL Data (first 5 rows):")
        hdl_df[['Observation_effectiveDateTime', 'Observation_valueQuantity_value']].head()
    else:
        mo.md(mo.Callout("Info: `hdl_df` is empty after filtering. No data to plot.", kind="info"))
else:
    mo.md(mo.Callout("Warning: Initial DataFrame `df` is empty or None. Cannot prepare HDL data.", kind="warn"))

```

```python
# Cell 5: Bokeh Plotting for HDL

mo.md("## HDL Cholesterol Over Time (Filtered Data)")

# Check if hdl_df is populated and has the necessary columns
if not hdl_df.empty and \
   'Observation_effectiveDateTime' in hdl_df.columns and \
   'Observation_valueQuantity_value' in hdl_df.columns and \
   pd.api.types.is_datetime64_any_dtype(hdl_df['Observation_effectiveDateTime']) and \
   pd.api.types.is_numeric_dtype(hdl_df['Observation_valueQuantity_value']):

    p = figure(
        x_axis_type="datetime",
        title="HDL Cholesterol Over Time",
        height=350,
        width=800,
        x_axis_label='Date',
        y_axis_label='HDL (mg/dL)'
    )

    # Add a line and circle glyph using hdl_df
    p.line(
        x=hdl_df['Observation_effectiveDateTime'],
        y=hdl_df['Observation_valueQuantity_value'],
        legend_label="HDL",
        line_width=2
    )
    p.circle(
        x=hdl_df['Observation_effectiveDateTime'],
        y=hdl_df['Observation_valueQuantity_value'],
        legend_label="HDL", 
        fill_color="white",
        size=8
    )

    p.xaxis.formatter = DatetimeTickFormatter(
        days="%Y-%m-%d",
        months="%Y-%m",
        years="%Y"
    )
    p.xaxis.axis_label_text_font_style = "normal"
    p.yaxis.axis_label_text_font_style = "normal"
    p.grid.grid_line_alpha = 0.3
    p.legend.location = "top_left"

    p # Marimo will render Bokeh plots directly
else:
    mo.md(mo.Callout(
        title="Plotting Error or No HDL Data",
        body="Could not generate plot. Please check if `hdl_df` is correctly populated and prepared after filtering, "
             "and if 'Observation_effectiveDateTime' and 'Observation_valueQuantity_value' columns are present "
             "with the correct data types.",
        kind="danger"
    ))

```
