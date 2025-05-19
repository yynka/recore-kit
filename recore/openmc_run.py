"""
Spin up a minimalist fast‑spectrum pin‑cell in OpenMC and return
the generated statepoint file.
"""
from pathlib import Path
import argparse
import openmc
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import ctx



def build_pincell(
    fuel_r=0.4, pitch=1.3, enrich=15.0, particles=1_000, batches=20, cwd="run"
) -> Path:
    Path(cwd).mkdir(exist_ok=True)
    old_cwd = os.getcwd()
    os.chdir(cwd)
    try:
        # ----- materials -----
        fuel = openmc.Material(name="U‑Pu‑Zr fuel")
        fuel.add_element("U", 1.0, enrichment=enrich)  # toy enrichment
        fuel.set_density("g/cm3", 19.1)

        clad = openmc.Material(name="HT9")
        clad.add_element("Fe", 1.0)
        clad.set_density("g/cm3", 7.8)

        openmc.Materials([fuel, clad]).export_to_xml()

        # ----- geometry -----
        fuel_cyl = openmc.ZCylinder(r=fuel_r)
        clad_cyl = openmc.ZCylinder(r=fuel_r * 1.05)

        # Add a bounding box with vacuum boundary
        box = openmc.model.RectangularParallelepiped(
            -pitch/2, pitch/2, -pitch/2, pitch/2, -1.0, 1.0, boundary_type='vacuum'
        )

        cells = [
            openmc.Cell(fill=fuel, region=-fuel_cyl & -box),
            openmc.Cell(fill=clad, region=+fuel_cyl & -clad_cyl & -box),
            openmc.Cell(region=+clad_cyl & -box),  # outside = void, inside box
            openmc.Cell(region=+box),  # outside box (vacuum boundary)
        ]
        root = openmc.Universe(cells=cells)
        openmc.Geometry(root).export_to_xml()

        # ----- tally: regular mesh flux -----
        mesh = openmc.RegularMesh()
        mesh.dimension = [10, 10, 1]
        mesh.lower_left = [-pitch/2, -pitch/2, -1.0]
        mesh.upper_right = [pitch/2, pitch/2, 1.0]

        mesh_filter = openmc.MeshFilter(mesh)
        tally = openmc.Tally(name="flux_mesh")
        tally.filters = [mesh_filter]
        tally.scores = ["flux"]
        tallies = openmc.Tallies([tally])
        tallies.export_to_xml()

        # ----- settings -----
        settings = openmc.Settings()
        settings.batches = batches
        settings.inactive = 2
        settings.particles = particles
        settings.export_to_xml()

        # ----- run -----
        openmc.run(cwd=".", threads=1, geometry_debug=False)
        return Path(f"statepoint.{batches:03d}.h5")
    finally:
        os.chdir(old_cwd)


def mesh_flux_figure():
    parquet_file = Path("run/mesh_flux.parquet")
    if not parquet_file.exists():
        return go.Figure()
    df = pd.read_parquet(parquet_file)
    flux2d = df.values
    # Use the same mesh extents as before
    x = np.linspace(-0.65, 0.65, flux2d.shape[0])  # adjust as needed
    y = np.linspace(-0.65, 0.65, flux2d.shape[1])  # adjust as needed
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


if __name__ == "__main__":
    print ("file running....)")
    parser = argparse.ArgumentParser(description="Run a smoke‑test OpenMC job.")
    parser.add_argument("--particles", type=int, default=1000)
    parser.add_argument("--batches", type=int, default=20)
    args = parser.parse_args()

    sp = build_pincell(particles=args.particles, batches=args.batches)
    print("✅  OpenMC finished.  Statepoint →", sp)
