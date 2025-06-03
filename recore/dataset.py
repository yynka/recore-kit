"""
Convert an OpenMC statepoint (HDF5) to compressed Parquet.
"""

from pathlib import Path
import argparse
import openmc
import pyarrow as pa
import pyarrow.parquet as pq


class Dataset:
    def __init__(self, statepoint: Path):
        self.sp = openmc.StatePoint(statepoint)

    def to_parquet(self, outfile: Path = Path("results.parquet")) -> Path:
        df = self.sp.tallies[1].get_pandas_dataframe()  # flux tally
        pq.write_table(pa.Table.from_pandas(df), outfile, compression="snappy")
        return outfile


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="HDF5 → Parquet converter")
    ap.add_argument("statepoint", type=Path)
    ap.add_argument("-o", "--out", type=Path, default=Path("results.parquet"))
    ns = ap.parse_args()

    out = Dataset(ns.statepoint).to_parquet(ns.out)
    h5_size = ns.statepoint.stat().st_size / 1024
    pq_size = out.stat().st_size / 1024
    print(f"✅  Wrote {out}  ({h5_size:.1f} kB → {pq_size:.1f} kB)")
