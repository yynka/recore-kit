# Dockerfile for ReCore-Kit: Nuclear Physics Simulation & Analysis

FROM mambaorg/micromamba:1.5.3

# Install dependencies in the base environment
RUN micromamba install -y -n base -c conda-forge \
    python=3.12 openmc pyarrow polars numba dash plotly pytest black wget xz && \
    micromamba clean --all --yes

# Set working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Download and extract nuclear data
RUN mkdir -p /app/nuclear_data && \
    wget -O /app/nuclear_data/cross_sections.tar.gz "https://anl.box.com/shared/static/9igk353zpy8fn9ttvtrqgzvw1vtejoz6.xz" && \
    tar -xJf /app/nuclear_data/cross_sections.tar.gz -C /app/nuclear_data

# Set environment variable for OpenMC
ENV OPENMC_CROSS_SECTIONS=/app/nuclear_data/endfb-vii.1-hdf5/cross_sections.xml

# Set PYTHONPATH so scripts can find recore
ENV PYTHONPATH=/app

# Default command: run the OpenMC smoke test
CMD ["python", "recore/smoke_openmc.py"] 