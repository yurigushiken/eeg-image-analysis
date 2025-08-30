# SFN2 Project: Data-Driven EEG Analysis Pipeline

This directory contains a modernized, flexible, and reproducible workflow for conducting sensor-space and source-space EEG analyses, inspired by the methods in Jas et al. (2018).

## Overview

This project moves away from traditional ERP component analysis (e.g., measuring P1 or N1 amplitude in a pre-defined window) towards a data-driven, hypothesis-testing framework using non-parametric cluster-based permutation tests.

**The core philosophy is to let the data reveal statistically significant differences without a priori assumptions about when or where effects will occur.** This method robustly controls for multiple comparisons across all time points, sensors, and source vertices.

## How it Works

The analysis is controlled by a single, comprehensive YAML (`.yaml`) configuration file and executed by a single Python script. The pipeline performs the following steps automatically:

1.  **Load Config:** Parses the specified `.yaml` file.
2.  **Load Data:** Gathers all required subject epoch files.
3.  **Compute Contrasts:** For each subject, calculates the difference wave between the two conditions of interest (e.g., "Change" vs. "No Change").
4.  **(Source Analysis Only) Generate Inverse Solution:** If a subject's inverse operator file (`-inv.fif`) is not found, the pipeline will automatically generate one using the `fsaverage` template brain.
5.  **Run Group Statistics:** Performs a spatio-temporal cluster permutation test on the contrasts from all subjects.
6.  **Generate Outputs:** Creates a dedicated output directory containing:
    *   A detailed statistical report (`..._report.txt`).
    *   Visualizations of the results (ERP plots and topomaps for sensor space; brain surface plots for source space).
    *   The grand average contrast file (`...-ave.fif` or `...-stc.h5`).

## Project Structure

-   `SFN2/code/`: Contains all Python analysis scripts.
    -   `run_sensor_analysis_pipeline.py`: Main entrypoint for sensor-space analyses.
    -   `run_source_analysis_pipeline.py`: Main entrypoint for source-space analyses.
    -   `utils/`: Helper modules for data loading, statistics, plotting, and reporting.
-   `SFN2/configs/`: Contains all analysis configuration files.
-   `SFN2/derivatives/`: The output directory for all generated figures and reports, organized by analysis name and domain (sensor/source).

## How to Run an Analysis

All scripts are executed as Python modules from the **root directory of the project** (e.g., `D:/numbers_eeg/`). Ensure the `numbers-eeg` conda environment is active.

**Command Structure:**

```bash
# General format for sensor space
conda activate numbers-eeg; python -m SFN2.code.run_sensor_analysis_pipeline --config <path_to_config> --accuracy <dataset>

# General format for source space
conda activate numbers-eeg; python -m SFN2.code.run_source_analysis_pipeline --config <path_to_config> --accuracy <dataset>
```

**Example Analyses:**

```bash
# Example 1: Run the 'change vs. no-change' sensor-space analysis
conda activate numbers-eeg; python -m SFN2.code.run_sensor_analysis_pipeline --config SFN2/configs/sensor_change_vs_no-change.yaml --accuracy all

# Example 2: Run the 'prime 1 vs prime 3' source-space analysis
conda activate numbers-eeg; python -m SFN2.code.run_source_analysis_pipeline --config SFN2/configs/source_prime1-land3_vs_prime3-land1.yaml --accuracy all
```

**Arguments:**

-   `--config`: The path to the `.yaml` file defining the entire analysis from contrast to statistics.
-   `--accuracy`: The dataset to use (`acc1` for correct trials, `all` for all trials).
