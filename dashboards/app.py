import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from recore.kinetics import solve
import numpy as np
import pandas as pd
from pathlib import Path
import subprocess
import os
from dash import ctx

app = dash.Dash(__name__)
server = app.server  # for Flask hosting if needed

# Helper to get mesh extents (if needed, adjust as appropriate)
def get_mesh_extents(flux2d):
    # These should match the mesh extents in your OpenMC model
    # For a 10x10 mesh and pitch=1.3:
    x = np.linspace(-0.65, 0.65, flux2d.shape[0])
    y = np.linspace(-0.65, 0.65, flux2d.shape[1])
    return x, y

def power_fig(rho):
    t, p = solve(rho_step=rho)
    fig = go.Figure(go.Scatter(x=t, y=p, mode="lines"))
    fig.update_layout(xaxis_title="Time (s)", yaxis_title="Relative power",
                      title=f"Step reactivity ρ = {rho:.4f}")
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

app.layout = html.Div([
    html.H3("ReCore‑Kit transient explorer"),
    dcc.Slider(id="rho", min=0.0005, max=0.01, step=0.0005, value=0.002),
    dcc.Graph(id="g"),
    html.Hr(),
    html.H4("Mesh Flux Tally"),
    html.Button("Re-analyze Mesh Tally", id="reanalyze-btn", n_clicks=0),
    dcc.Loading(
        dcc.Graph(id="mesh-flux-graph"),
        type="circle"
    ),
    html.Div(id="reanalyze-status", style={"marginTop": "1em", "color": "#0074D9"}),
], style={"width": "70%", "margin": "auto"})

@app.callback(Output("g", "figure"), Input("rho", "value"))
def update(rho):
    return power_fig(rho)

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
    app.run(debug=True, port=8051)   # <‑‑ change port