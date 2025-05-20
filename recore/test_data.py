import subprocess
from pathlib import Path
import os
import pytest

def test_parquet_file_exists_and_is_smaller():
    # Run analyze.py to generate Parquet file
    subprocess.run(["python3", "analyze.py"])  # Should create mesh_flux.parquet
    run_dir = Path("run")
    parquet_file = run_dir / "mesh_flux.parquet"
    statepoints = sorted(run_dir.glob("statepoint.*.h5"))
    assert parquet_file.exists(), "Parquet file does not exist!"
    assert statepoints, "No statepoint file found!"
    h5_size = os.path.getsize(statepoints[-1])
    parq_size = os.path.getsize(parquet_file)
    assert parq_size < h5_size, f"Parquet file ({parq_size}) is not smaller than HDF5 ({h5_size})!" 