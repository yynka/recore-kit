# ReCore-Kit

A toolkit for nuclear reactor core analysis, featuring a point-reactor kinetics solver and a Dash-based interactive dashboard.

## Setup Instructions

### 1. Clone the Repository
```sh
# From your desired workspace directory:
git clone https://github.com/openmc-dev/openmc.git  # if you need OpenMC source
# (If you already have the repo, skip this step)
```

### 2. Set Up Python Environment
We recommend using conda:
```sh
conda create -n recore-env python=3.12
conda activate recore-env
pip install -r requirements.txt  # if you have a requirements file
# Or install manually:
pip install dash plotly polars pyarrow numba numpy pytest
```

### 3. Build and Install OpenMC (if needed)
If you need OpenMC and are on Apple Silicon (M1/M2/M3):
```sh
brew install gcc
cd openmc
mkdir build && cd build
CC=/opt/homebrew/bin/gcc-14 CXX=/opt/homebrew/bin/g++-14 cmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX
make -j4
make install
cd ..
pip install .
```

### 4. Run the Dashboard
From the project root:
```sh
PYTHONPATH=$(pwd) python3 dashboards/app.py
```
Then open your browser to [http://localhost:8051](http://localhost:8051)

### 5. Run the Tests
From the project root:
```sh
pytest recore/test_kinetics.py
```

## Project Structure
- `recore/kinetics.py` — Point-reactor kinetics solver
- `recore/test_kinetics.py` — Unit tests for the solver
- `dashboards/app.py` — Dash web app for interactive exploration

## Troubleshooting
- If you see `ModuleNotFoundError: No module named 'recore'`, make sure to set `PYTHONPATH` to the project root when running scripts.
- For OpenMC build issues on Apple Silicon, ensure you use Homebrew GCC and follow the build steps above.

---
For more details, see the code comments or contact the project maintainers. 