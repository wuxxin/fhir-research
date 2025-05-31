import marimo

__generated_with = "0.13.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # HDL Cholesterol Visualization with Marimo, Bokeh and Matplotlib

    This notebook demonstrates generating FHIR data for HDL cholesterol observations,
    flattening it, filtering for HDL, and visualizing HDL values over time.
    It can be run interactively in Marimo or as a Python script to export the plot.
    """
    )
    return


@app.cell
def _(mo):
    import pandas as pd
    import json
    import argparse
    import os
    import sys

    from datetime import datetime, timedelta, date

    from bokeh.plotting import figure
    from bokeh.models import DatetimeTickFormatter
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    def list_all_files(base_dir):
        for root, _, files in os.walk(base_dir):
            for file in files:
                yield os.path.join(root, file)

    try:
        from fhir_research.utils import (
            flatten_fhir_bundle,
            filter_fhir_dataframe,
            create_patient_lab_bundle,
        )
        from fhir_research.examples import fhir_bundle_marimo_max
    except ModuleNotFoundError:
        print("Standard import failed. Attempting WASM public folder import...")
        notebook_dir = mo.notebook_location()
        current_dir = os.getcwd()
        print(f"Notebook_dir: {notebook_dir}")
        print(f"current_dir: {current_dir}")
        with open(os.path.join(current_dir, "test.py")) as f:
            f.write("import os\n")
        for file_path in list_all_files(current_dir):
            print(file_path)

        public_fhir_path = os.path.join(current_dir, "public")
        prospective_path_to_lib_parent = public_fhir_path
        prospective_lib_dir = os.path.join(public_fhir_path, "fhir_research")

        if os.path.isdir(prospective_lib_dir) and os.path.exists(
            os.path.join(prospective_lib_dir, "__init__.py")
        ):
            print(f"Found 'fhir_research' directory at: {prospective_lib_dir}")
            if prospective_path_to_lib_parent not in sys.path:
                sys.path.insert(0, prospective_path_to_lib_parent)
                print(f"Added to sys.path: {prospective_path_to_lib_parent}")
            else:
                print(f"Path already in sys.path: {prospective_path_to_lib_parent}")

            # Retry import
            from fhir_research.utils import (
                flatten_fhir_bundle,
                filter_fhir_dataframe,
                create_patient_lab_bundle,
            )
            from fhir_research.examples import fhir_bundle_marimo_max

            print(
                "Successfully imported fhir_research from public folder after adding to sys.path."
            )
        else:
            print(
                f"Error: Could not find 'fhir_research' in public folder. Looked for dir at: {prospective_lib_dir}. sys.path: {sys.path}"
            )
            raise

    return (
        DatetimeTickFormatter,
        argparse,
        fhir_bundle_marimo_max,
        figure,
        filter_fhir_dataframe,
        flatten_fhir_bundle,
        mdates,
        pd,
        plt,
    )


@app.cell
def _(fhir_bundle_marimo_max, filter_fhir_dataframe, flatten_fhir_bundle):
    ## Data Processing, Inspection and Visualisaztion (Interactive)

    fhir_bundle = fhir_bundle_marimo_max()
    bundle_dict = fhir_bundle.model_dump()
    df_full = flatten_fhir_bundle(bundle_dict)
    df_subset = filter_fhir_dataframe(df_full, "code_coding_0_code", "2085-9")
    return df_full, df_subset


@app.cell
def _(df_full, df_subset, mo):
    mo.md("### Subset DataFrame")
    if df_subset is not None and not df_subset.empty:
        mo.ui.table(
            df_subset[["effectiveDateTime", "valueQuantity_value"]].head(),
            selection=None,
        )
    else:
        mo.md("`df_subset` is empty or not yet loaded.")

    mo.md("### All DataFrame  - First 5 rows")
    if df_full is not None and not df_full.empty:
        mo.ui.table(df_full.head(), selection=None)
    else:
        mo.md("`df_full` is empty or not yet loaded.")
    return


@app.cell
def _(DatetimeTickFormatter, df_subset, figure, pd):
    ## Plotting Functions

    def create_bokeh_plot(data_frame: pd.DataFrame):
        # Creates a Bokeh plot for HDL cholesterol over time.
        if (
            data_frame is None
            or data_frame.empty
            or "effectiveDateTime" not in data_frame.columns
            or "valueQuantity_value" not in data_frame.columns
            or not pd.api.types.is_datetime64_any_dtype(data_frame["effectiveDateTime"])
            or not pd.api.types.is_numeric_dtype(data_frame["valueQuantity_value"])
        ):
            print("Data for Bokeh plot is empty or invalid. Creating empty plot.")
            p_empty = figure(width=800, height=350, title="HDL Cholesterol Over Time")
            p_empty.text(
                x=[0],
                y=[0],
                text=["No valid HDL data to plot. Check data preparation steps."],
                text_align="center",
                text_baseline="middle",
            )
            return p_empty

        p = figure(
            x_axis_type="datetime",
            title="HDL Cholesterol Over Time",
            height=350,
            width=800,
            x_axis_label="Date",
            y_axis_label="HDL (mg/dL)",
        )
        p.line(
            x=data_frame["effectiveDateTime"],
            y=data_frame["valueQuantity_value"],
            legend_label="HDL",
            line_width=2,
        )
        p.circle(
            x=data_frame["effectiveDateTime"],
            y=data_frame["valueQuantity_value"],
            legend_label="HDL",
            fill_color="white",
            size=8,
        )
        p.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d", months="%Y-%m", years="%Y")
        p.xaxis.axis_label_text_font_style = "normal"
        p.yaxis.axis_label_text_font_style = "normal"
        p.grid.grid_line_alpha = 0.3
        p.legend.location = "top_left"
        return p

    create_bokeh_plot(df_subset)
    return


@app.cell
def _(df_subset, mdates, pd, plt):
    def create_matplotlib_plot(data_frame: pd.DataFrame):
        date_column_name = "effectiveDateTime"
        value_column_name = "valueQuantity_value"
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("HDL Cholesterol Over Time (Matplotlib)")
        ax.set_xlabel("Date")
        ax.set_ylabel("HDL (mg/dL)")

        if (
            data_frame is None
            or data_frame.empty
            or date_column_name not in data_frame.columns
            or value_column_name not in data_frame.columns
        ):
            print("Data for Matplotlib plot is empty or invalid. Creating empty plot.")
            ax.text(
                0.5,
                0.5,
                "No valid HDL data to plot.",
                horizontalalignment="center",
                verticalalignment="center",
                transform=ax.transAxes,
            )
            plt.tight_layout()
            return fig  # Return the figure object

        ax.plot(
            data_frame[date_column_name],
            data_frame[value_column_name],
            marker="o",
            linestyle="-",
        )
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True)
        plt.tight_layout()

        return fig  # Always return the figure object

    create_matplotlib_plot(df_subset)
    return (create_matplotlib_plot,)


@app.cell
def _(argparse, create_matplotlib_plot, df_subset):
    ## Script Execution Logic (for CLI export)
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(
            description="Generate HDL plot and optionally export it."
        )
        parser.add_argument(
            "-o",
            "--output-image",
            type=str,
            help="Filename to save the plot image",
        )
        args = parser.parse_args()
        if args.output_image:
            output_path = args.output_image
            print(f"Script mode: Saving Matplotlib plot to {output_path}...")
            create_matplotlib_plot(df_subset).savefig(output_path)
    return


if __name__ == "__main__":
    app.run()
