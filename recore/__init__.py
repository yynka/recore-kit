"""
ReCore‑Kit: tiny end‑to‑end fast‑reactor workflow.
"""

import os
from pathlib import Path

# Set up OpenMC cross sections path
nuclear_data_dir = Path.home() / "recore" / "nuclear_data"
cross_sections_path = nuclear_data_dir / "endfb-vii.1-hdf5" / "cross_sections.xml"
if cross_sections_path.exists():
    os.environ["OPENMC_CROSS_SECTIONS"] = str(cross_sections_path)

__version__ = "0.1.0"

__all__ = ["openmc_runner", "dataset", "kinetics"]
