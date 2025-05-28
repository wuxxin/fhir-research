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
        # Use model_dump() as flatten_fhir_bundle expects a dictionary
        bundle_dict = fhir_bundle.model_dump() 

        # Flatten Bundle to DataFrame
        df_full = flatten_fhir_bundle(bundle_dict)

        # Prepare Subset DataFrame
        df_subset = pd.DataFrame()
        if df_full is not None and not df_full.empty: # Changed df to df_full
            if filtercolumn:
                if filtercolumn in df_full.columns: # Changed df to df_full
                    df_subset = df_full[df_full[filtercolumn] == filtervalue].copy() # Changed df to df_full
                    if not df_subset.empty:
                        # The following column names might need adjustment based on flatten_fhir_bundle output
                        # Assuming keys like 'effectiveDateTime' and 'valueQuantity_value' exist after flattening
                        date_col = next((col for col in df_subset.columns if 'effectiveDateTime' in col), None)
                        value_col = next((col for col in df_subset.columns if 'valueQuantity_value' in col), None)

                        if date_col:
                            df_subset[date_col] = pd.to_datetime(
                                df_subset[date_col]
                            )
                        if value_col:
                            df_subset[value_col] = pd.to_numeric(
                                df_subset[value_col]
                            )
                else:
                    print(
                        f"Warning: filtercolumn '{filtercolumn}' not found in DataFrame. Cannot filter."
                    )
        else:
            print("Warning: Initial DataFrame `df_full` is empty or None.")

        return df_subset, df_full, bundle_dict

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
        # Check for invalid or empty data first
        if (
            data_frame is None
            or data_frame.empty
            or "effectiveDateTime" not in data_frame.columns # Adjusted to likely actual column name
            or "valueQuantity_value" not in data_frame.columns # Adjusted to likely actual column name
            # Or check for the prefixed names if they are consistently used:
            # or "Observation_effectiveDateTime" not in data_frame.columns
            # or "Observation_valueQuantity_value" not in data_frame.columns
        ):
            print("Script mode: Data for Matplotlib plot is empty or invalid. Creating empty plot.")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No valid HDL data to plot.", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.set_title("HDL Cholesterol Over Time (Matplotlib)")
            ax.set_xlabel("Date")
            ax.set_ylabel("HDL (mg/dL)")
            plt.tight_layout()
            return fig # Return the figure object

        # Proceed with plotting if data is valid
        print("Script mode: Creating plot with Matplotlib...")
        # Always create a new figure and axes for plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Use the potentially correct column names based on df_full output from previous runs
        # (e.g., 'effectiveDateTime', 'valueQuantity_value')
        # If df_subset is created from df_full, it should have these direct names.
        date_column_name = "effectiveDateTime" 
        value_column_name = "valueQuantity_value"

        # Fallback to prefixed names if direct ones are not found (robustness)
        if date_column_name not in data_frame.columns and "Observation_effectiveDateTime" in data_frame.columns:
            date_column_name = "Observation_effectiveDateTime"
        if value_column_name not in data_frame.columns and "Observation_valueQuantity_value" in data_frame.columns:
            value_column_name = "Observation_valueQuantity_value"

        # Final check if columns are actually present before plotting
        if date_column_name not in data_frame.columns or value_column_name not in data_frame.columns:
            print(f"Error: Required columns ('{date_column_name}', '{value_column_name}') not found in DataFrame for Matplotlib plot.")
            # ax = fig.gca() # Already have ax from subplots
            ax.text(0.5, 0.5, "Error: Plotting columns not found.", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.set_title("HDL Cholesterol Over Time (Matplotlib)")
            ax.set_xlabel("Date")
            ax.set_ylabel("HDL (mg/dL)")
            plt.tight_layout()
            return fig


        ax.plot( # Use ax.plot
            data_frame[date_column_name],
            data_frame[value_column_name],
            marker="o",
            linestyle="-",
        )

        ax.set_title("HDL Cholesterol Over Time (Matplotlib)") # Use ax.set_title
        ax.set_xlabel("Date") # Use ax.set_xlabel
        ax.set_ylabel("HDL (mg/dL)") # Use ax.set_ylabel

        # Format x-axis for dates
        # ax = plt.gca() # Already have ax
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax.tick_params(axis='x', rotation=45) # Use ax.tick_params for rotation

        ax.grid(True) # Use ax.grid
        plt.tight_layout()  # Can still be used with fig/ax for overall layout

        return fig # Always return the figure object

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

    df_subset, df_full, bundle_data = get_fhir_dataframe("", "2085-9") # Renamed variable for clarity
    bokeh_plot = create_bokeh_plot(df_subset)
    mpl_plot = create_matplotlib_plot(df_subset) # mpl_plot is a Figure object or plt

    # Use mo.runtime.is_editing() for older Marimo versions
    # This block is for interactive display, less critical for `make test`
    try:
        is_editing_mode = mo.runtime.is_editing()
    except AttributeError:
        # Fallback or assume script mode if .runtime.is_editing() doesn't exist
        # For `make test`, this path means it won't try to render UI elements if the check fails
        is_editing_mode = False

    if is_editing_mode:
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
            # If bundle_data is a dict, and accordion expects JSON string, needs conversion
            # For now, assuming accordion can handle dict or this part is less critical for 'make test'
            mo.accordion({"Generated FHIR Bundle (JSON)": bundle_data})
        
        # Displaying plots in Marimo notebook if they are objects
        # If mpl_plot is a Figure, it can be displayed. If it's `plt`, this line is an error.
        # Bokeh plot is already a Figure object.
        # For now, focusing on `make test` which doesn't run this block.
        # if isinstance(mpl_plot, plt.Figure):
        #     mpl_plot 
        # else: # Assuming it's the plt module
        #     plt.show() # or pass for script mode
        # bokeh_plot

    ## Script Execution Logic (for CLI export)
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(
            description="Generate HDL plot and optionally export it."
        )
        parser.add_argument(
            "-o", "--output-image",  # Added -o
            type=str,
            help="Filename to save the plot image (e.g., hdl_plot.png). If not provided, no image is saved.",
        )
        args = parser.parse_args()
        if args.output_image:
            output_path = args.output_image
            try:
                print(f"Script mode: Saving Matplotlib plot to {output_path}...")
                # Ensure the correct figure is saved.
                # If create_matplotlib_plot returned a figure `fig`, save that.
                # If it returned `plt` (module), then `plt.savefig` is fine.
                if isinstance(mpl_plot, plt.Figure):
                    mpl_plot.savefig(output_path)
                else: # Assuming mpl_plot is the plt module itself, or an error occurred
                    plt.savefig(output_path)
                print(f"Plot successfully saved to {output_path}")
            except Exception as e:
                print(f"Error saving Matplotlib plot: {e}")
            plt.close()  # Close the figure to free memory

    return


if __name__ == "__main__":
    app.run()
