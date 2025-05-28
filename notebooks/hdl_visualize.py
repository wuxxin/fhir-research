import marimo

__generated_with = "0.13.14"
app = marimo.App()


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
def _():
    import pandas as pd
    import json
    import argparse
    import os

    from datetime import datetime, timedelta, date

    from bokeh.plotting import figure
    from bokeh.models import DatetimeTickFormatter
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    from fhir_research.utils import (
        create_patient_lab_bundle,
        flatten_fhir_bundle,
    )

    return (
        DatetimeTickFormatter,
        argparse,
        create_patient_lab_bundle,
        figure,
        flatten_fhir_bundle,
        mdates,
        pd,
        plt,
    )


@app.cell
def _(
    DatetimeTickFormatter,
    create_patient_lab_bundle,
    df,
    figure,
    flatten_fhir_bundle,
    mdates,
    pd,
    plt,
):
    ## Data Generation Function

    def get_fhir_dataframe(filtercolumn="", filtervalue=None):
        """Generates patient and lab observation data, creates a FHIR bundle,
        flattens it, optionaly filters for code (string) observations,
        and prepares the data for plotting.
        Returns a pandas DataFrame containing only prepared observations.
        """
        # Define Patient Data
        patient_details = {
            "id": "patient-marimo-01",
            "family_name": "Marimo",
            "given_name": "Maria",
            "birth_date": "1980-05-15",  # YYYY-MM-DD
            "gender": "female",
        }

        # Define HDL Observations Data (specific for this visualization)
        lab_observations_details = [
            {
                "observation_id": "hdl-marimo-01",
                "effective_date_time": "2020-01-15T09:00:00Z",
                "code_system": "http://loinc.org",
                "code": "2085-9",
                "code_display": "Cholesterol in HDL",
                "value_quantity_value": 60.0,
                "value_quantity_unit": "mg/dL",
                "value_quantity_unit_code": "mg/dL",
            },
            {
                "observation_id": "hdl-marimo-02",
                "effective_date_time": "2021-02-20T09:30:00Z",
                "code_system": "http://loinc.org",
                "code": "2085-9",
                "code_display": "Cholesterol in HDL",
                "value_quantity_value": 62.0,
                "value_quantity_unit": "mg/dL",
                "value_quantity_unit_code": "mg/dL",
            },
            {
                "observation_id": "hdl-marimo-03",
                "effective_date_time": "2022-03-10T08:45:00Z",
                "code_system": "http://loinc.org",
                "code": "2085-9",
                "code_display": "Cholesterol in HDL",
                "value_quantity_value": 58.0,
                "value_quantity_unit": "mg/dL",
                "value_quantity_unit_code": "mg/dL",
            },
            {
                "observation_id": "hdl-marimo-04",
                "effective_date_time": "2023-04-05T10:15:00Z",
                "code_system": "http://loinc.org",
                "code": "2085-9",
                "code_display": "Cholesterol in HDL",
                "value_quantity_value": 61.0,
                "value_quantity_unit": "mg/dL",
                "value_quantity_unit_code": "mg/dL",
            },
        ]

        # Generate FHIR Bundle
        fhir_bundle = create_patient_lab_bundle(
            patient_details=patient_details, lab_observations_details=lab_observations_details
        )
        bundle_json = fhir_bundle.as_json()

        # Flatten Bundle to DataFrame
        df_full = flatten_fhir_bundle(bundle_json)

        # Prepare Subset DataFrame
        df_subset = pd.DataFrame()
        if df is not None and not df.empty:
            if filtercolumn:
                if filtercolumn in df.columns:
                    df_subset = df[df[filtercolumn] == filtervalue].copy()
                    if not df_subset.empty:
                        if "Observation_effectiveDateTime" in df_subset.columns:
                            df_subset["Observation_effectiveDateTime"] = pd.to_datetime(
                                df_subset["Observation_effectiveDateTime"]
                            )
                        if "Observation_valueQuantity_value" in df_subset.columns:
                            df_subset["Observation_valueQuantity_value"] = pd.to_numeric(
                                df_subset["Observation_valueQuantity_value"]
                            )
                else:
                    print(
                        f"Warning: filtercolumn column not found. Cannot filter for {filtercolumn}"
                    )
        else:
            print("Warning: Initial DataFrame `df_full` is empty or None.")

        return df_subset, df_full, bundle_json

    ## Plotting Functions

    def create_bokeh_plot(data_frame: pd.DataFrame):
        # Creates a Bokeh plot for HDL cholesterol over time.
        if (
            data_frame is None
            or data_frame.empty
            or "Observation_effectiveDateTime" not in data_frame.columns
            or "Observation_valueQuantity_value" not in data_frame.columns
            or not pd.api.types.is_datetime64_any_dtype(
                data_frame["Observation_effectiveDateTime"]
            )
            or not pd.api.types.is_numeric_dtype(data_frame["Observation_valueQuantity_value"])
        ):
            # Create an empty plot with a message if data is not valid
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
            x=data_frame["Observation_effectiveDateTime"],
            y=data_frame["Observation_valueQuantity_value"],
            legend_label="HDL",
            line_width=2,
        )
        p.circle(
            x=data_frame["Observation_effectiveDateTime"],
            y=data_frame["Observation_valueQuantity_value"],
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

    def create_matplotlib_plot(data_frame: pd.DataFrame):
        if (
            data_frame is None
            or data_frame.empty
            or "Observation_effectiveDateTime" not in data_frame.columns
            or "Observation_valueQuantity_value" not in data_frame.columns
        ):
            print("Script mode: Creating plot with Matplotlib...")
            plt.figure(figsize=(10, 6))  # Similar size to Bokeh's width=800, height=350
            plt.plot(
                data_frame["Observation_effectiveDateTime"],
                data_frame["Observation_valueQuantity_value"],
                marker="o",
                linestyle="-",
            )

            plt.title("HDL Cholesterol Over Time (Matplotlib)")
            plt.xlabel("Date")
            plt.ylabel("HDL (mg/dL)")

            # Format x-axis for dates
            ax = plt.gca()
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plt.xticks(rotation=45)  # Rotate labels for better readability

            plt.grid(True)
            plt.tight_layout()  # Adjust layout to prevent labels from being cut off

            return plt

    return create_bokeh_plot, create_matplotlib_plot, get_fhir_dataframe


@app.cell
def _(
    argparse,
    create_bokeh_plot,
    create_matplotlib_plot,
    get_fhir_dataframe,
    mo,
    plt,
):
    ## Data Processing, Inspection and Visualisaztion (Interactive)

    df_subset, df_full, bundle_json = get_fhir_dataframe("", "2085-9")
    bokeh_plot = create_bokeh_plot(df_subset)
    mpl_plot = create_matplotlib_plot(df_subset)

    if mo.get_context().execution_mode == "notebook":
        mo.md("### Subset DataFrame")
        if df_subset is not None and not df_subset.empty:
            mo.ui.table(
                df_subset[
                    ["Observation_effectiveDateTime", "Observation_valueQuantity_value"]
                ].head(),
                selection=None,
            )
        else:
            mo.md("`df_subset` is empty or not yet loaded.")

        mo.md("### All DataFrame  - First 5 rows")
        if df_full is not None and not df_full.empty:
            mo.ui.table(df_full.head(), selection=None)
        else:
            mo.md("`df_full` is empty or not yet loaded.")

        show_bundle = mo.ui.button(label="Show Full Bundle JSON")
        if show_bundle.value:
            mo.accordion({"Generated FHIR Bundle (JSON)": bundle_json})

        mpl_plot.figure()
        bokeh_plot.figure()

    ## Script Execution Logic (for CLI export)
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(
            description="Generate HDL plot and optionally export it."
        )
        parser.add_argument(
            "--output-image",
            type=str,
            help="Filename to save the plot image (e.g., hdl_plot.png). If not provided, no image is saved.",
        )
        args = parser.parse_args()
        if args.output_image:
            output_path = args.output_image
            try:
                print(f"Script mode: Saving Matplotlib plot to {output_path}...")
                plt.savefig(output_path)
                print(f"Plot successfully saved to {output_path}")
            except Exception as e:
                print(f"Error saving Matplotlib plot: {e}")
            plt.close()  # Close the figure to free memory

    return


if __name__ == "__main__":
    app.run()
