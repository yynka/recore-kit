import dash
from dash import dcc, html, Input, Output, ctx
import plotly.graph_objects as go
from recore.kinetics import solve
import numpy as np
import pandas as pd
from pathlib import Path
import subprocess
import os

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # for Flask hosting if needed

# --- Helper functions ---
def get_mesh_extents(flux2d):
    # These should match the mesh extents in your OpenMC model
    # For a 10x10 mesh and pitch=1.3:
    x = np.linspace(-0.65, 0.65, flux2d.shape[0])
    y = np.linspace(-0.65, 0.65, flux2d.shape[1])
    return x, y

def power_fig(rho):
    t, p = solve(rho_step=rho)
    fig = go.Figure(go.Scatter(x=t, y=p, mode="lines"))
    fig.update_layout(
        xaxis_title="Time (s)",
        yaxis_title="Relative power",
        title=f"Step reactivity ρ = {rho:.4f}"
    )
    return fig

def mesh_flux_figure():
    parquet_file = Path("run/mesh_flux.parquet")
    if not parquet_file.exists():
        return go.Figure()
    df = pd.read_parquet(parquet_file)
    flux2d = df.values
    x, y = get_mesh_extents(flux2d)
    fig = go.Figure(
        data=go.Heatmap(
            z=flux2d.T,
            x=x,
            y=y,
            colorbar=dict(title="Flux"),
        )
    )
    fig.update_layout(
        xaxis_title="x [cm]",
        yaxis_title="y [cm]",
        title="Mesh Flux (from Parquet)"
    )
    return fig

# --- Layout ---
app.layout = html.Div([
    html.H2("ReCore‑Kit Dashboard"),
    dcc.Tabs(id="tabs", value="tab-kinetics", children=[
        dcc.Tab(label="Transient Explorer", value="tab-kinetics"),
        dcc.Tab(label="Mesh Flux Tally", value="tab-flux"),
    ]),
    html.Div(id="tab-content"),
    html.Div(id="reanalyze-status", style={"marginTop": "1em", "color": "#0074D9"}),
], style={"width": "70%", "margin": "auto"})

# --- Tab content callback ---
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
)
def render_tab(tab):
    if tab == "tab-kinetics":
        return html.Div([
            html.Label("Step Reactivity (ρ):"),
            dcc.Slider(id="rho", min=0.0005, max=0.01, step=0.0005, value=0.002, 
                       marks={i/10000: f"{i/10000:.4f}" for i in range(5, 101, 10)}),
            dcc.Graph(id="g"),
        ], style={"marginTop": 30})
    elif tab == "tab-flux":
        return html.Div([
            html.Button("Re-analyze Mesh Tally", id="reanalyze-btn", n_clicks=0),
            dcc.Loading(
                dcc.Graph(id="mesh-flux-graph"),
                type="circle"
            ),
        ], style={"marginTop": 30})

# --- Power plot callback ---
@app.callback(
    Output("g", "figure"),
    Input("rho", "value")
)
def update_power_plot(rho):
    return power_fig(rho)

# --- Mesh flux plot and re-analyze callback ---
@app.callback(
    Output("mesh-flux-graph", "figure"),
    Output("reanalyze-status", "children"),
    Input("reanalyze-btn", "n_clicks"),
    Input("mesh-flux-graph", "id"),
    prevent_initial_call=False
)
def mesh_flux_update(n_clicks, _):
    trigger = ctx.triggered_id if hasattr(ctx, "triggered_id") else dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    status = ""
    if trigger == "reanalyze-btn" and n_clicks:
        try:
            result = subprocess.run(["python3", "analyze.py"], capture_output=True, text=True, timeout=60)
            status = result.stdout.splitlines()[-1] if result.stdout else "Re-analysis complete."
        except Exception as e:
            status = f"Error: {e}"
    fig = mesh_flux_figure()
    return fig, status

if __name__ == "__main__":
    app.run(debug=True, port=8051)