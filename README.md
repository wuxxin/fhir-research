# Jules Lab Experiment , **THIS-IS-AN-EXPERIMENT** for coding agent fitness,
  **NO CODE** has been reviewed for any purpose

## Python Medical Data Science Project

This project demonstrates the use of Python for handling and visualizing medical data,
specifically focusing on FHIR resources, 
pandas for data analysis, and Bokeh and matplotlib for visualization.

It includes utilities for creating example FHIR Patient and Observation 
(HDL Cholesterol) data, flattening FHIR bundles for analysis,
and example notebooks in Marimo for visualization.

## Setup

```sh
make buildenv
```

## Running the Code

### Marimo Notebook

```bash
uv run marimo edit notebooks/hdl_visualize.py
```

To export the plot from this notebook as an image, you can run it as a script:

```bash
uv run python notebooks/hdl_visualize.md --output-image hdl_plot.png
```

## Testing and Linting

**Run Tests**:

```bash
make test
```

**Run Linter**:

```bash
make lint
```

## FHIR Profiles

* **Patient Data**: Uses the core FHIR Patient resource.
    *`Patient.name` conforms to `http://fhir.de/StructureDefinition/humanname-de-basis`.
    *`Patient.address` conforms to `http://fhir.de/StructureDefinition/address-de-basis`.
* **HDL Cholesterol Observation**: Uses the core FHIR Observation resource.
    * Category: `laboratory`
    * Code: LOINC `2085-9` ("Cholesterol in HDL [Mass/volume] in Serum or Plasma")
    * Units: `mg/dL` (UCUM code `mg/dL`)

## todo

### make all test pass - [COMPLETED]

- [x] install dependencies: run `make buildenv` ,
- [x] run tests: run `make test`
- [x] review errors, fix errors and warnings if reasonable
- [x] rerun tests, if something get stuck, call make clean, then proceed
- [x] update README.md

