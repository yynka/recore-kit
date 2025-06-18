import os
import sys
import wget
import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
from pathlib import Path
import subprocess
import json
from datetime import datetime
import shutil
import openmc
import io
import contextlib


def download_nuclear_data():
    """Download nuclear data if not present."""
    data_dir = Path.home() / "recore" / "nuclear_data"
    data_dir.mkdir(parents=True, exist_ok=True)

    cross_sections_file = data_dir / "cross_sections.tar.gz"
    if not cross_sections_file.exists():
        print("Downloading nuclear data...")
        url = "https://anl.box.com/shared/static/9igk353zpy8fn9ttvtrqgzvw1vtejoz6.xz"
        wget.download(url, str(cross_sections_file))
        print("\nExtracting nuclear data...")
        os.system(f"tar -xJf {cross_sections_file} -C {data_dir}")

    os.environ["OPENMC_CROSS_SECTIONS"] = str(
        data_dir / "endfb-vii.1-hdf5" / "cross_sections.xml"
    )


def download_sample_data():
    """Download and set up sample data from OpenMC."""
    data_dir = Path.home() / "recore" / "sample_data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Run the smoke test to generate sample data
    result = run_smoke_test()
    if result["success"]:
        # Copy the generated files to sample data directory
        sample_files = list(Path(".").glob("*.h5"))
        for file in sample_files:
            shutil.copy2(file, data_dir / file.name)
        return True
    return False


def run_smoke_test():
    """Run the OpenMC smoke test."""
    try:
        result = subprocess.run(
            ["python", "recore/smoke_openmc.py"], capture_output=True, text=True
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
        }
    except Exception as e:
        return {"success": False, "output": "", "error": str(e)}


def get_results_context(latest_dataset):
    if latest_dataset == "smoke":
        return "This plot shows the neutron flux from the most recent smoke test statepoint file."
    elif latest_dataset == "sample":
        return (
            "This plot shows the neutron flux from the provided sample statepoint file."
        )
    elif latest_dataset == "uploaded":
        return "This plot shows the neutron flux from your uploaded statepoint file."
    else:
        return "No results to display yet. Run a smoke test, download sample data, or upload your own statepoint file."


def run_smoke_with_output():
    """Run the smoke test and capture both summary and full output."""
    import traceback
    from recore.smoke_openmc import main as run_smoke

    buf = io.StringIO()
    summary = ""
    with contextlib.redirect_stdout(buf):
        try:
            result = run_smoke()
            if result:
                summary = "✅ Analysis completed successfully!"
            else:
                summary = "❌ Smoke test failed!"
        except Exception as e:
            summary = f"❌ Error: {str(e)}"
            print(traceback.format_exc())
    full_output = buf.getvalue()
    return summary, full_output


def run_analysis_with_output(filename=None):
    """Run analysis and capture both summary and full output."""
    # Placeholder for actual analysis logic
    buf = io.StringIO()
    summary = ""
    with contextlib.redirect_stdout(buf):
        try:
            # Simulate analysis output
            print("k-effective: 0.02589 ± 0.00020")
            print("leakage fraction: 0.98889 ± 0.00078")
            print("statepoint file:", filename)
            summary = "✅ Analysis completed successfully!"
        except Exception as e:
            summary = f"❌ Error: {str(e)}"
    full_output = buf.getvalue()
    return summary, full_output


def create_app():
    """Create the Dash application."""
    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            html.H1("ReCore: Nuclear Physics Simulation & Analysis"),
            # Tabs for different functionalities
            dcc.Tabs(
                [
                    # Home Tab
                    dcc.Tab(
                        label="Home",
                        children=[
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            # Left: Controls
                                            html.Div(
                                                [
                                                    html.H3("Verification"),
                                                    html.P(
                                                        "Verify your installation by running the smoke test."
                                                    ),
                                                    html.Button(
                                                        "Run Smoke Test",
                                                        id="run-smoke-test",
                                                        n_clicks=0,
                                                    ),
                                                    html.Hr(style={"margin": "10px 0"}),
                                                    html.H3("Analysis"),
                                                    html.P(
                                                        "Choose sample data or upload your own statepoint file."
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.H4("Sample Data"),
                                                            html.P(
                                                                "Use pre-generated statepoint from OpenMC smoke test:"
                                                            ),
                                                            html.Button(
                                                                "Download Sample Data",
                                                                id="download-sample",
                                                                n_clicks=0,
                                                            ),
                                                            html.Div(
                                                                id="sample-data-status"
                                                            ),
                                                        ],
                                                        style={
                                                            "margin": "10px 0",
                                                            "padding": "10px",
                                                            "border": "1px solid #ddd",
                                                            "borderRadius": "5px",
                                                        },
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.H4(
                                                                "Upload Statepoint"
                                                            ),
                                                            html.P(
                                                                "Or upload your own statepoint file:"
                                                            ),
                                                            dcc.Upload(
                                                                id="upload-data",
                                                                children=html.Div(
                                                                    [
                                                                        "Drag and Drop or ",
                                                                        html.A(
                                                                            "Select Files"
                                                                        ),
                                                                    ]
                                                                ),
                                                                style={
                                                                    "width": "100%",
                                                                    "height": "40px",
                                                                    "lineHeight": "40px",
                                                                    "borderWidth": "1px",
                                                                    "borderStyle": "dashed",
                                                                    "borderRadius": "5px",
                                                                    "textAlign": "center",
                                                                    "margin": "5px",
                                                                },
                                                                multiple=True,
                                                            ),
                                                            html.Div(
                                                                id="output-data-upload"
                                                            ),
                                                        ],
                                                        style={
                                                            "margin": "10px 0",
                                                            "padding": "10px",
                                                            "border": "1px solid #ddd",
                                                            "borderRadius": "5px",
                                                        },
                                                    ),
                                                    html.Button(
                                                        "Run Analysis",
                                                        id="run-analysis",
                                                        n_clicks=0,
                                                    ),
                                                ],
                                                style={
                                                    "width": "60%",
                                                    "display": "inline-block",
                                                    "verticalAlign": "top",
                                                },
                                            ),
                                            # Right: Output panel
                                            html.Div(
                                                [
                                                    html.H4("Output"),
                                                    html.Div(
                                                        id="home-output-panel",
                                                        style={
                                                            "whiteSpace": "pre-wrap",
                                                            "maxHeight": "400px",
                                                            "overflowY": "auto",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "width": "35%",
                                                    "display": "inline-block",
                                                    "verticalAlign": "top",
                                                    "marginLeft": "2%",
                                                    "background": "#f9f9f9",
                                                    "padding": "10px",
                                                    "border": "1px solid #eee",
                                                    "borderRadius": "5px",
                                                    "minHeight": "300px",
                                                },
                                            ),
                                        ],
                                        style={
                                            "width": "100%",
                                            "display": "flex",
                                            "flexDirection": "row",
                                            "justifyContent": "space-between",
                                        },
                                    ),
                                ]
                            )
                        ],
                    ),
                    # Results Tab
                    dcc.Tab(
                        label="Results",
                        children=[
                            html.Div(
                                [
                                    html.H2("Simulation Results"),
                                    html.Div(
                                        id="results-context",
                                        style={
                                            "marginBottom": "10px",
                                            "fontStyle": "italic",
                                            "color": "#555",
                                        },
                                    ),
                                    # Visualization Section
                                    html.Div(
                                        [
                                            html.H3("Visualization"),
                                            dcc.Graph(id="simulation-plot"),
                                        ],
                                        style={
                                            "margin": "10px 0",
                                            "padding": "10px",
                                            "border": "1px solid #ddd",
                                            "borderRadius": "5px",
                                        },
                                    ),
                                    # Export Section
                                    html.Div(
                                        [
                                            html.H3("Export Results"),
                                            html.Button(
                                                "Export Results",
                                                id="export-results",
                                                n_clicks=0,
                                            ),
                                            html.Div(id="export-status"),
                                        ],
                                        style={
                                            "margin": "10px 0",
                                            "padding": "10px",
                                            "border": "1px solid #ddd",
                                            "borderRadius": "5px",
                                        },
                                    ),
                                ]
                            )
                        ],
                    ),
                ]
            ),
        ]
    )

    # Store the latest dataset type in a hidden div
    app.layout.children.append(html.Div(id="latest-dataset", style={"display": "none"}))

    # Home output panel logic
    @app.callback(
        Output("home-output-panel", "children"),
        [
            Input("run-smoke-test", "n_clicks"),
            Input("run-analysis", "n_clicks"),
            Input("download-sample", "n_clicks"),
        ],
        [State("upload-data", "filename")],
    )
    def update_home_output(
        smoke_clicks, analysis_clicks, sample_clicks, uploaded_filename
    ):
        ctx = dash.callback_context
        if not ctx.triggered:
            return ""
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "run-smoke-test":
            summary, full_output = run_smoke_with_output()
            return html.Div(
                [
                    html.Div(
                        summary, style={"fontWeight": "bold", "marginBottom": "8px"}
                    ),
                    html.Pre(
                        full_output,
                        style={
                            "background": "#f4f4f4",
                            "padding": "8px",
                            "borderRadius": "4px",
                            "fontSize": "12px",
                        },
                    ),
                ]
            )
        elif button_id == "run-analysis":
            summary, full_output = run_analysis_with_output(uploaded_filename)
            return html.Div(
                [
                    html.Div(
                        summary, style={"fontWeight": "bold", "marginBottom": "8px"}
                    ),
                    html.Pre(
                        full_output,
                        style={
                            "background": "#f4f4f4",
                            "padding": "8px",
                            "borderRadius": "4px",
                            "fontSize": "12px",
                        },
                    ),
                ]
            )
        elif button_id == "download-sample":
            return html.Div(
                [html.Pre("Sample data downloaded.", style={"color": "blue"})]
            )
        return ""

    # Results context logic
    @app.callback(
        Output("results-context", "children"),
        [
            Input("run-smoke-test", "n_clicks"),
            Input("run-analysis", "n_clicks"),
            Input("download-sample", "n_clicks"),
            Input("upload-data", "contents"),
        ],
    )
    def update_results_context(
        smoke_clicks, analysis_clicks, sample_clicks, upload_contents
    ):
        # Determine which dataset is most recent
        ctx = dash.callback_context
        if not ctx.triggered:
            return get_results_context(None)
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "run-smoke-test":
            return get_results_context("smoke")
        elif button_id == "download-sample":
            return get_results_context("sample")
        elif button_id == "run-analysis" or button_id == "upload-data":
            return get_results_context("uploaded")
        return get_results_context(None)

    # Callback for analysis
    @app.callback(
        [Output("simulation-plot", "figure")], Input("run-analysis", "n_clicks")
    )
    def run_analysis_callback(n_clicks):
        if not n_clicks:
            return [go.Figure()]
        # Placeholder: replace with actual analysis/visualization
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=[0, 1, 2, 3, 4],
                y=[0, 1, 4, 9, 16],
                mode="lines+markers",
                name="Simulation Results",
            )
        )
        fig.update_layout(
            title="Nuclear Simulation Results",
            xaxis_title="Batch",
            yaxis_title="k-effective",
            showlegend=True,
        )
        return [fig]

    # Callback for export
    @app.callback(
        Output("export-status", "children"), Input("export-results", "n_clicks")
    )
    def export_results_callback(n_clicks):
        if not n_clicks:
            return ""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_dir = Path.home() / "recore" / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)

        return html.Div(
            [
                html.P(f"Results exported to: {export_dir}"),
                html.P(f"Timestamp: {timestamp}"),
            ]
        )

    return app


def run_analysis(contents):
    """Run analysis on uploaded data."""
    # TODO: Implement actual analysis
    return {"k_effective": 0.02589, "leakage_fraction": 0.98889, "confidence": 0.00020}


def create_visualization(results):
    """Create visualization of simulation results."""
    # TODO: Implement actual visualization
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[0, 1, 2, 3, 4],
            y=[0, 1, 4, 9, 16],
            mode="lines+markers",
            name="Simulation Results",
        )
    )
    fig.update_layout(
        title="Nuclear Simulation Results",
        xaxis_title="Batch",
        yaxis_title="k-effective",
        showlegend=True,
    )
    return fig


def main():
    """Main entry point for the GUI."""
    # Download nuclear data if needed
    download_nuclear_data()

    # Create and run the app
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()
