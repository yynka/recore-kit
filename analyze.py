import openmc
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import os

# Find the latest statepoint file in the run directory
run_dir = Path("run")
statepoints = sorted(run_dir.glob("statepoint.*.h5"))
if not statepoints:
    raise FileNotFoundError("No statepoint files found in 'run/' directory.")
sp_file = statepoints[-1]
print(f"Loading {sp_file}")

# Load the statepoint file
sp = openmc.StatePoint(str(sp_file))

# Get the mesh tally by name
tally = sp.get_tally(name="flux_mesh")
mesh = tally.filters[0].mesh
flux = tally.get_values(scores=["flux"]).reshape(mesh.dimension)

# Reshape to 2D array (sum over z if 3D)
if mesh.dimension[2] == 1:
    flux2d = flux[:, :, 0]
else:
    flux2d = flux.sum(axis=2)

# Convert to DataFrame for Parquet
df = pd.DataFrame(flux2d)
parquet_file = run_dir / "mesh_flux.parquet"
pq.write_table(pa.Table.from_pandas(df), parquet_file, compression="snappy")

# Print HDF5 and Parquet file sizes
h5_size = os.path.getsize(sp_file) / 1024
parq_size = os.path.getsize(parquet_file) / 1024
print(f"Converted: HDF5 {h5_size:.1f} kB → Parquet {parq_size:.1f} kB")

# (Optional) Plot for visual check
plt.imshow(flux2d.T, origin="lower", extent=(mesh.lower_left[0], mesh.upper_right[0], mesh.lower_left[1], mesh.upper_right[1]), aspect="auto")
plt.xlabel("x [cm]")
plt.ylabel("y [cm]")
plt.title("Mesh Flux")
plt.colorbar(label="Flux")
plt.tight_layout()
plt.show()