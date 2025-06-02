import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium", app_title="fhir-research")

with app.setup:
    # Initialization code that runs before all other cells
    # test
    pass


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Cholesterol Visualization with Marimo, Bokeh and Matplotlib

    This notebook demonstrates generating FHIR data observations,
    flattening it, filtering for cholesterol, and visualizing values over time.
    It can be run interactively in Marimo or as a Python script to export the plot.
    """
    )
    return


@app.cell(hide_code=True)
def _():
    import os
    import sys
    import argparse

    import pandas as pd
    import bokeh
    import matplotlib
    import altair as alt

    if "pyodide" in sys.modules:
        import micropip
    else:
        micropip = None
    return argparse, alt, bokeh, matplotlib, micropip, os, pd, sys


@app.cell(hide_code=True)
async def _(micropip, mo, os, sys):
    module_name = "fhir_research-0.1.0-py3-none-any.whl"
    module_path = os.path.join(mo.notebook_location(), "public", module_name)
    if "pyodide" in sys.modules:
        await micropip.install(module_path)
    import fhir_research

    return (fhir_research,)


@app.cell(hide_code=True)
def _(fhir_research):
    ## Data Processing, Inspection and Visualisaztion (Interactive)

    # Use the new German lab example bundle
    fhir_bundle = fhir_research.examples.fhir_bundle_german_lab_example()
    bundle_dict = fhir_bundle.model_dump()
    df_full = fhir_research.utils.flatten_fhir_bundle(bundle_dict)

    # Filter for Cholesterol, HDL, and Triglycerides
    target_loinc_codes = ["2093-3", "2085-9", "2571-8"]
    df_subset = fhir_research.utils.filter_fhir_dataframe(
        df_full, column_name="code_coding_0_code", codes=target_loinc_codes
    )
    return (df_subset,)


@app.cell
def _(mo):
    mo.md(r"""## Filtered SubSet DataFrame (First 5)""")
    return


@app.cell(hide_code=True)
def _(df_subset, mo):
    mo.ui.table(df_subset.head(), selection=None)
    return


@app.cell
def _(alt, df_subset, pd):
    ## Plotting Functions

    def create_altair_chart(data_frame: pd.DataFrame):
        # Creates an Altair chart for laboratory values over time.
        required_cols = ["effectiveDateTime", "valueQuantity_value", "code_coding_0_display"]
        if (
            data_frame is None
            or data_frame.empty
            or not all(col in data_frame.columns for col in required_cols)
        ):
            print("Data for Altair plot is empty or invalid. Creating empty chart.")
            # Return an empty chart with a text annotation
            return alt.Chart().mark_text(
                text="No valid data to plot. Check data preparation steps.",
                align="center",
                baseline="middle"
            ).properties(
                title="Laboratory Values Over Time (Altair)",
                width=800,
                height=400
            )

        chart = alt.Chart(data_frame).mark_point().encode(
            x=alt.X('effectiveDateTime:T', title='Date', axis=alt.Axis(format='%Y-%m-%d')),
            y=alt.Y('valueQuantity_value:Q', title='Value (mg/dL)'),
            color='code_coding_0_display:N',
            tooltip=['code_coding_0_display', 'effectiveDateTime', 'valueQuantity_value']
        ).properties(
            title="Laboratory Values Over Time (Altair)",
            width=960,
            height=600
        ).interactive()
        return chart
    return (create_altair_chart,)


@app.cell
def _(bokeh, df_subset, pd):
    def create_bokeh_plot(data_frame: pd.DataFrame):
        # Creates a Bokeh plot for laboratory values over time.
        required_cols = ["effectiveDateTime", "valueQuantity_value", "code_coding_0_display"]
        if (
            data_frame is None
            or data_frame.empty
            or not all(col in data_frame.columns for col in required_cols)
            or not pd.api.types.is_datetime64_any_dtype(data_frame["effectiveDateTime"])
            or not pd.api.types.is_numeric_dtype(data_frame["valueQuantity_value"])
        ):
            print("Data for Bokeh plot is empty or invalid. Creating empty plot.")
            p_empty = bokeh.plotting.figure(
                width=800, height=400, title="Laboratory Values Over Time"
            )
            p_empty.text(
                x=[0],
                y=[0],
                text=["No valid data to plot. Check data preparation steps."],
                text_align="center",
                text_baseline="middle",
            )
            return p_empty

        p = bokeh.plotting.figure(
            x_axis_type="datetime",
            title="Laboratory Values Over Time",
            width=960,
            height=600,
            x_axis_label="Date",
            y_axis_label="Value (mg/dL)",  # Generic Y-axis label
        )

        # Define a color palette for multiple lines
        from bokeh.palettes import Category10

        colors = Category10[10]  # Palette for up to 10 lines

        grouped = data_frame.groupby("code_coding_0_display")

        for i, (analyte_name, group) in enumerate(grouped):
            color = colors[i % len(colors)]  # Cycle through colors
            p.line(
                x=group["effectiveDateTime"],
                y=group["valueQuantity_value"],
                legend_label=analyte_name,
                line_width=2,
                color=color,
            )
            p.circle(
                x=group["effectiveDateTime"],
                y=group["valueQuantity_value"],
                legend_label=analyte_name,
                fill_color="white",
                size=8,
                color=color,
            )

        p.xaxis.formatter = bokeh.models.DatetimeTickFormatter(
            days="%Y-%m-%d", months="%Y-%m", years="%Y"
        )
        p.xaxis.axis_label_text_font_style = "normal"
        p.yaxis.axis_label_text_font_style = "normal"
        p.grid.grid_line_alpha = 0.3
        p.legend.location = "top_left"
        return p

    create_bokeh_plot(df_subset)
    return


@app.cell
def _(df_subset, matplotlib, pd):
    def create_matplotlib_plot(data_frame: pd.DataFrame):
        date_column_name = "effectiveDateTime"
        value_column_name = "valueQuantity_value"
        display_name_column = "code_coding_0_display"

        # It's good practice to call tight_layout() after all plotting elements are added,
        # or at least before saving/showing the plot, so moving it later.
        # matplotlib.pyplot.tight_layout()

        fig, ax = matplotlib.pyplot.subplots(figsize=(10, 6))
        ax.set_title("Laboratory Values Over Time (Matplotlib)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value (mg/dL)")  # Generic Y-axis label

        required_cols = [date_column_name, value_column_name, display_name_column]
        if (
            data_frame is None
            or data_frame.empty
            or not all(col in data_frame.columns for col in required_cols)
        ):
            print("Data for Matplotlib plot is empty or invalid. Creating empty plot.")
            ax.text(
                0.5,
                0.5,
                "No valid data to plot.",
                horizontalalignment="center",
                verticalalignment="center",
                transform=ax.transAxes,
            )
        else:
            grouped = data_frame.groupby(display_name_column)
            for analyte_name, group in grouped:
                ax.plot(
                    group[date_column_name],
                    group[value_column_name],
                    marker="o",
                    linestyle="-",
                    label=analyte_name,
                )

            ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y-%m-%d"))
            ax.tick_params(axis="x", rotation=45)
            ax.grid(True)
            ax.legend()  # Add legend to display labels

        matplotlib.pyplot.tight_layout()  # Call tight_layout before returning
        return fig  # Always return the figure object

    create_matplotlib_plot(df_subset)
    return (create_matplotlib_plot,)


@app.cell
def _(create_altair_chart, df_subset):
    create_altair_chart(df_subset)
    return


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
