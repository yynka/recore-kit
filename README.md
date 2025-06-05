# <span style="vertical-align: middle;">Recore-Kit</span>
<p align="center">
  <a href="#docker-installation"><img src="readme-assets/docker.svg" alt="Docker" height="60" style="vertical-align: middle; margin: 0 48px;"/></a>
  <a href="#gitlab-installation"><img src="readme-assets/gitlab.svg" alt="GitLab" height="60" style="vertical-align: middle; margin: 0 48px;"/></a>
  <a href="#github-installation"><img src="readme-assets/github.svg" alt="GitHub" height="60" style="vertical-align: middle; margin: 0 48px;"/></a>
</p>
<br><br>

> **A reproducible, portable, and fully automated toolkit for nuclear reactor core simulation, analysis, and visualization. Run OpenMC-based physics simulations, analyze results, and explore data interactively—all with a single command, on any platform.**

- ⚛️ **Full nuclear simulation workflow:** OpenMC-based fast-spectrum pin-cell simulations and analysis.
- 🔁 **Reproducible & portable:** All dependencies, nuclear data, and environment setup are automated.
- 🐳 **Run anywhere:** Use Docker for a one-command setup, or install via GitLab/GitHub for development and CI/CD.
- 📊 **Interactive dashboard:** Visualize and explore results with a built-in Dash web app.
- ✅ **Continuous integration:** Every commit is tested for code quality, simulation correctness, and analysis validity.

---

## Docker Installation    (Recommended) <a id="docker-installation"></a> <img src="readme-assets/docker.svg" alt="Docker" height="40" align="right"/>

### 1. Build the Docker image
```sh
docker build -t recore-kit .
```

### 2. Run the OpenMC simulation (smoke test)
```sh
docker run --rm recore-kit
```

### 3. Run the analysis
```sh
docker run --rm recore-kit python analyze.py
```

### 4. Run the dashboard (optional)
```sh
docker run --rm -p 8051:8051 recore-kit python dashboards/app.py
```
Then open your browser to [http://localhost:8051](http://localhost:8051)

You can override the default command to run any script in the container as needed.

---

## GitLab Installation <a id="gitlab-installation"></a> <img src="readme-assets/gitlab.svg" alt="GitLab" height="40" align="right"/>

### 1. Clone the Repository
```sh
git clone https://gitlab.com/yynka/recore-kit.git
cd recore-kit
```

### 2. Set Up Python Environment

**Mamba (recommended for speed):**
```sh
mamba create -n recore-env -c conda-forge python=3.12 openmc pyarrow polars numba dash plotly pytest black wget xz
conda activate recore-env

pip install -r requirements.txt
```

**Micromamba:**
```sh
micromamba create -y -n recore-env -c conda-forge python=3.12 openmc pyarrow polars numba dash plotly pytest black wget xz
micromamba activate recore-env

pip install -r requirements.txt
```

**Conda:**
```sh
conda create -n recore-env -c conda-forge python=3.12 openmc pyarrow polars numba dash plotly pytest black wget xz
conda activate recore-env

pip install -r requirements.txt
```

### 3. Download and Extract Nuclear Data
You must download the OpenMC cross section data (ENDF/B-VII.1 HDF5):
```sh
mkdir -p nuclear_data
wget -O nuclear_data/cross_sections.tar.gz "https://anl.box.com/shared/static/9igk353zpy8fn9ttvtrqgzvw1vtejoz6.xz"
tar -xJf nuclear_data/cross_sections.tar.gz -C nuclear_data
```

Set the environment variable so OpenMC can find the data:
```sh
export OPENMC_CROSS_SECTIONS="$PWD/nuclear_data/endfb-vii.1-hdf5/cross_sections.xml"
```

### 4. Run the OpenMC Simulation (Smoke Test)
From the project root:
```sh
python recore/smoke_openmc.py
```
This will run a minimalist fast-spectrum pin-cell simulation and produce a statepoint file (e.g., `statepoint.020.h5`).

### 5. Run the Analysis
```sh
python analyze.py
```
This will process the simulation output. You can also run additional tests:
```sh
pytest recore/test_data.py
```

### 6. Run the Dashboard (Optional)
From the project root:
```sh
PYTHONPATH=$(pwd) python3 dashboards/app.py
```

Then open your browser to [http://localhost:8051](http://localhost:8051)

### 7. Run the Kinetics Solver Tests (Optional)
```sh
pytest recore/test_kinetics.py
```

---

## GitHub Installation <a id="github-installation"></a> <img src="readme-assets/github.svg" alt="GitHub" height="40" align="right"/>

### 1. Clone the Repository
```sh
git clone https://github.com/yynka/recore-kit.git
cd recore-kit
```

### 2. Set Up Python Environment

**Mamba (recommended for speed):**
```sh
mamba create -n recore-env -c conda-forge python=3.12 openmc pyarrow polars numba dash plotly pytest black wget xz
conda activate recore-env

pip install -r requirements.txt
```

**Micromamba:**
```sh
micromamba create -y -n recore-env -c conda-forge python=3.12 openmc pyarrow polars numba dash plotly pytest black wget xz
micromamba activate recore-env

pip install -r requirements.txt
```

**Conda:**
```sh
conda create -n recore-env -c conda-forge python=3.12 openmc pyarrow polars numba dash plotly pytest black wget xz
conda activate recore-env

pip install -r requirements.txt
```

### 3. Download and Extract Nuclear Data
You must download the OpenMC cross section data (ENDF/B-VII.1 HDF5):
```sh
mkdir -p nuclear_data
wget -O nuclear_data/cross_sections.tar.gz "https://anl.box.com/shared/static/9igk353zpy8fn9ttvtrqgzvw1vtejoz6.xz"
tar -xJf nuclear_data/cross_sections.tar.gz -C nuclear_data
```

Set the environment variable so OpenMC can find the data:
```sh
export OPENMC_CROSS_SECTIONS="$PWD/nuclear_data/endfb-vii.1-hdf5/cross_sections.xml"
```

### 4. Run the OpenMC Simulation (Smoke Test)
From the project root:
```sh
python recore/smoke_openmc.py
```
This will run a minimalist fast-spectrum pin-cell simulation and produce a statepoint file (e.g., `statepoint.020.h5`).

### 5. Run the Analysis
```sh
python analyze.py
```
This will process the simulation output. You can also run additional tests:
```sh
pytest recore/test_data.py
```

### 6. Run the Dashboard (Optional)
From the project root:
```sh
PYTHONPATH=$(pwd) python3 dashboards/app.py
```

Then open your browser to [http://localhost:8051](http://localhost:8051)

### 7. Run the Kinetics Solver Tests (Optional)
```sh
pytest recore/test_kinetics.py
```

## Project Structure
- `recore/openmc_run.py` — Minimalist OpenMC pin-cell simulation setup and execution
- `recore/smoke_openmc.py` — Smoke test entry point for OpenMC simulation
- `analyze.py` — Analysis of OpenMC simulation results
- `recore/test_data.py` — Tests for analysis output
- `recore/kinetics.py` — Point-reactor kinetics solver
- `recore/test_kinetics.py` — Unit tests for the solver
- `dashboards/app.py` — Dash web app for interactive exploration

## CI/CD Pipeline
This project uses GitLab CI/CD to ensure code quality and scientific reproducibility. The pipeline includes:
- **lint**: Checks Python code formatting with Black
- **tests**: Runs all unit tests in `recore/` with pytest
- **smoke_run**: Runs a minimal OpenMC simulation (`smoke_openmc.py`)
- **analyze_data**: Runs analysis (`analyze.py`) and further tests (`recore/test_data.py`)

## Troubleshooting
- If you see `ModuleNotFoundError: No module named 'recore'`, make sure to set `PYTHONPATH` to the project root when running scripts:
  ```sh
  export PYTHONPATH=$(pwd)
  # or, for a one-off command:
  PYTHONPATH=$(pwd) python3 dashboards/app.py
  ```
- If OpenMC cannot find `cross_sections.xml`, ensure you have downloaded and extracted the nuclear data, and set the `OPENMC_CROSS_SECTIONS` environment variable to the correct path (see above):
  ```sh
  mkdir -p nuclear_data
  wget -O nuclear_data/cross_sections.tar.gz "https://anl.box.com/shared/static/9igk353zpy8fn9ttvtrqgzvw1vtejoz6.xz"
  tar -xJf nuclear_data/cross_sections.tar.gz -C nuclear_data
  export OPENMC_CROSS_SECTIONS="$PWD/nuclear_data/endfb-vii.1-hdf5/cross_sections.xml"
  ```
- For OpenMC build issues on Apple Silicon, ensure you use Homebrew GCC and follow the build steps:
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

---