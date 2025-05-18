import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from recore.kinetics import solve

app = dash.Dash(__name__)
server = app.server  # for Flask hosting if needed

def power_fig(rho):
    t, p = solve(rho_step=rho)
    fig = go.Figure(go.Scatter(x=t, y=p, mode="lines"))
    fig.update_layout(xaxis_title="Time (s)", yaxis_title="Relative power",
                      title=f"Step reactivity ρ = {rho:.4f}")
    return fig

app.layout = html.Div(
    [
        html.H3("ReCore‑Kit transient explorer"),
        dcc.Slider(id="rho", min=0.0005, max=0.01, step=0.0005, value=0.002),
        dcc.Graph(id="g"),
    ],
    style={"width": "70%", "margin": "auto"},
)

@app.callback(Output("g", "figure"), Input("rho", "value"))
def update(rho):
    return power_fig(rho)

if __name__ == "__main__":
    app.run(debug=True, port=8051)   # <‑‑ change port