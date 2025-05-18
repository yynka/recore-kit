from pathlib import Path
import openmc
import pyarrow as pa
import pyarrow.parquet as pq
import polars as pl   # handy for later analysis

class Dataset:
    """Wrap a statepoint and expose quick Parquet I/O."""

    def __init__(self, statepoint: Path):
        self.sp = openmc.StatePoint(statepoint)

    def to_parquet(self, outfile: Path = Path("results.parquet")) -> Path:
        # this grabs the default flux tally (ID 1).  Adjust if you add more tallies.
        df = self.sp.tallies[1].get_pandas_dataframe()
        pq.write_table(pa.Table.from_pandas(df), outfile, compression="snappy")
        return outfile

    @staticmethod
    def benchmark(sp_path: Path):
        import time, os
        start = time.perf_counter()
        size_h5 = sp_path.stat().st_size
        dset = Dataset(sp_path)
        parquet = dset.to_parquet(sp_path.with_suffix(".parquet"))
        size_parq = parquet.stat().st_size
        elapsed = time.perf_counter() - start
        print(f"Converted in {elapsed:.2f}s → HDF5 {size_h5/1e3:.1f} kB → "
              f"Parquet {size_parq/1e3:.1f} kB")
