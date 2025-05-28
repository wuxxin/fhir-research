# Jules Lab Experiment , **THIS-IS-AN-EXPERIMENT** for coding agent fitness, **NO CODE** has been reviewed for any purpose
## Python Medical Data Science Project

This project demonstrates the use of Python for handling and visualizing medical data, specifically focusing on FHIR resources, pandas for data analysis, and Bokeh for visualization. It includes utilities for creating example FHIR Patient and Observation (HDL Cholesterol) data, flattening FHIR bundles for analysis, and example notebooks in Marimo and Jupyter formats for visualization.

## Setup

```sh
make buildenv
```

## Running the Code

### Marimo Notebook

```bash
marimo edit notebooks/hdl_visualization.md
```

(Or `marimo run notebooks/hdl_visualization.md` for run-only mode).

To export the plot from this notebook as an image, you can run it as a script:
```bash
python notebooks/hdl_visualization.md --output-image hdl_plot.png
```

## Testing

**Run Tests**:

```bash
make test
```


## FHIR Profiles

*   **Patient Data**: Uses the core FHIR Patient resource.
    *   `Patient.name` conforms to `http://fhir.de/StructureDefinition/humanname-de-basis`.
    *   `Patient.address` conforms to `http://fhir.de/StructureDefinition/address-de-basis`.
*   **HDL Cholesterol Observation**: Uses the core FHIR Observation resource.
    *   Category: `laboratory`
    *   Code: LOINC `2085-9` ("Cholesterol in HDL [Mass/volume] in Serum or Plasma")
    *   Units: `mg/dL` (UCUM code `mg/dL`)
```
