# ReCore: Nuclear Physics Simulation & Analysis Toolkit

A Python toolkit for nuclear physics simulation and analysis, built on top of OpenMC.

## Running the GUI

```bash
recore-gui
```
The dashboard will open in your browser automatically.

## Features

- **Smoke Testing**: Verify your OpenMC installation
- **Data Analysis**: Process and analyze nuclear simulation data
- **Interactive Dashboard**: Visualize results with an easy-to-use interface
- **Automatic Setup**: Downloads required nuclear data automatically

## Installation

```bash
# Create virtual environment
python -m venv recore-env

# Activate virtual environment
source recore-env/bin/activate  # On Unix/macOS
# OR
.\recore-env\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

```bash
# Clone the repository
git clone https://github.com/yynka/recore-kit.git
cd recore-kit

# Set up environment (if not done already)
conda create -n recore python=3.13.4
conda activate recore-env

# Install the package in development mode
pip install -e .
```

## Using ReCore

1. **Launch the GUI**:
   ```bash
   recore-gui
   ```
   This will:
   - Download required nuclear data if not present
   - Open the dashboard in your browser
   - Guide you through the analysis process

2. **Run the Smoke Test**:
   - Open the "Smoke Test" tab
   - Click "Run Smoke Test" to verify your installation

3. **Analyze Data**:
   - Open the "Analysis" tab
   - Upload your simulation data
   - Click "Run Analysis" to process your data

4. **View Results**:
   - Open the "Dashboard" tab
   - View your analysis results
   - Export results as needed

## Project Structure

```
recore/
├── analyze.py      # Analysis tools
├── gui.py         # Interactive dashboard
├── smoke_openmc.py # Smoke test for OpenMC
└── utils.py       # Utility functions
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request