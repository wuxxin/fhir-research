# HDL Cholesterol Visualization with Marimo and Bokeh

This notebook demonstrates generating FHIR data for HDL cholesterol observations,
flattening it into a pandas DataFrame, and visualizing the HDL values over time
using Bokeh.

```python
import marimo as mo
import pandas as pd
from bokeh.plotting import figure # Removed 'show' as Marimo handles display
from bokeh.models import DatetimeTickFormatter
from datetime import datetime, timedelta, date # Added date for birth_date consistency
import json

# Assuming Marimo is run from the project root, or src is in PYTHONPATH
from src.medical_data_science.fhir_utils import (
    create_patient_hdl_observation,
    flatten_fhir_bundle,
)
```

```python
# Cell 2: Data Generation

# Define Patient Data
patient_id = "patient-marimo-01"
patient_family_name = "Marimo"
patient_given_name = "Maria"
patient_birth_date_str = "1980-05-15" # YYYY-MM-DD
patient_gender = "female"

# Define HDL Observations Data
hdl_observations_data = [
    {
        "value": 60.0,
        "effective_date_time": "2020-01-15T09:00:00Z",
        "observation_id": "hdl-obs-marimo-01",
    },
    {
        "value": 62.5,
        "effective_date_time": "2021-02-20T09:30:00Z",
        "observation_id": "hdl-obs-marimo-02",
    },
    {
        "value": 58.0,
        "effective_date_time": "2022-03-10T08:45:00Z",
        "observation_id": "hdl-obs-marimo-03",
    },
    {
        "value": 61.0,
        "effective_date_time": "2023-04-05T10:15:00Z",
        "observation_id": "hdl-obs-marimo-04",
    },
]

# Generate FHIR Bundle
fhir_bundle = create_patient_hdl_observation(
    patient_id=patient_id,
    patient_family_name=patient_family_name,
    patient_given_name=patient_given_name,
    patient_birth_date=patient_birth_date_str,
    patient_gender=patient_gender,
    hdl_observations=hdl_observations_data,
)

# Convert bundle to JSON dictionary
bundle_json = fhir_bundle.as_json()

# Flatten Bundle to DataFrame
df = flatten_fhir_bundle(bundle_json)

# Output a success message (optional, Marimo shows cell output by default)
mo.md(f"""
Data generation complete.
- Patient: {patient_given_name} {patient_family_name}
- FHIR Bundle ID: {bundle_json.get('id')}
- DataFrame shape: {df.shape if df is not None else 'N/A'}
""")
```

```python
# Cell 3: Data Inspection

mo.md("### Generated FHIR Bundle (JSON)")
# mo.output.json(bundle_json) # mo.output.json is one way, or just let Marimo render the dict
bundle_json # Marimo can render dictionaries directly

mo.md("### Flattened DataFrame")
df # Marimo will render the DataFrame as a table
```

```python
# Cell 4: Data Preparation for Plotting

# Ensure 'Observation_effectiveDateTime' is in datetime format
# The flatten_fhir_bundle should output string ISO dates, so conversion is needed.
if 'Observation_effectiveDateTime' in df.columns:
    df['Observation_effectiveDateTime'] = pd.to_datetime(df['Observation_effectiveDateTime'])
else:
    mo.md(mo.Callout("Warning: 'Observation_effectiveDateTime' column not found in DataFrame.", kind="warn"))

# Ensure 'Observation_valueQuantity_value' is numeric (it should be from fhir_utils)
if 'Observation_valueQuantity_value' in df.columns:
    df['Observation_valueQuantity_value'] = pd.to_numeric(df['Observation_valueQuantity_value'])
else:
    mo.md(mo.Callout("Warning: 'Observation_valueQuantity_value' column not found in DataFrame.", kind="warn"))

# Display prepared data types (optional)
# mo.md(f"Data types after preparation:\n{df[['Observation_effectiveDateTime', 'Observation_valueQuantity_value']].dtypes}")
df[['Observation_effectiveDateTime', 'Observation_valueQuantity_value']].head()
```

```python
# Cell 5: Bokeh Plotting

mo.md("## HDL Cholesterol Over Time")

# Check if necessary columns exist and data is not empty
if df is not None and not df.empty and \
   'Observation_effectiveDateTime' in df.columns and \
   'Observation_valueQuantity_value' in df.columns and \
   pd.api.types.is_datetime64_any_dtype(df['Observation_effectiveDateTime']) and \
   pd.api.types.is_numeric_dtype(df['Observation_valueQuantity_value']):

    p = figure(
        x_axis_type="datetime",
        title="HDL Cholesterol Over Time",
        height=350,
        width=800,
        x_axis_label='Date',
        y_axis_label='HDL (mg/dL)'
    )

    # Add a line and circle glyph
    p.line(
        x=df['Observation_effectiveDateTime'],
        y=df['Observation_valueQuantity_value'],
        legend_label="HDL",
        line_width=2
    )
    p.circle(
        x=df['Observation_effectiveDateTime'],
        y=df['Observation_valueQuantity_value'],
        legend_label="HDL", # Usually only need one legend entry for combined glyphs
        fill_color="white",
        size=8
    )

    # Format the x-axis to display dates nicely
    p.xaxis.formatter = DatetimeTickFormatter(
        days="%Y-%m-%d",
        months="%Y-%m", # Show month and year for month ticks
        years="%Y"       # Show only year for year ticks
    )
    p.xaxis.axis_label_text_font_style = "normal" # Ensure label font is not italic (default for some themes)
    p.yaxis.axis_label_text_font_style = "normal"


    # Customize plot appearance (optional)
    p.grid.grid_line_alpha = 0.3
    p.legend.location = "top_left"

    # Output the plot
    p # Marimo will render Bokeh plots directly
else:
    mo.md(mo.Callout(
        title="Plotting Error",
        body="Could not generate plot. Please check if the DataFrame `df` is correctly populated and prepared, "
             "and if 'Observation_effectiveDateTime' and 'Observation_valueQuantity_value' columns are present "
             "with the correct data types.",
        kind="danger"
    ))

```
