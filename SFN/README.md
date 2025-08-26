# SFN Project Workflow

This directory contains a flexible, configuration-driven workflow for generating ERP plots for the Society for Neuroscience (SFN) conference project.

## Overview

Instead of relying on dozens of individual, hard-coded scripts, this system uses a single, powerful master script (`generate_plots.py`) that is controlled by simple YAML (`.yaml`) configuration files. This approach is highly efficient, flexible, and reduces code redundancy, making it easy to create new analyses without writing new Python code.

## File Structure

-   `SFN/code/generate_plots.py`: The master script. **You should not need to edit this file.** It is designed to be generic and adaptable to any analysis defined in a config file.
-   `SFN/code/utils.py`: A utility module containing shared constants (like electrode groups and color palettes) and helper functions. This is the primary file to update if you need to add a new ERP component, electrode selection, or color scheme.
-   `SFN/configs/`: This directory holds all the analysis configuration files. Each `.yaml` file defines a single analysis.
-   `SFN/derivatives/`: This is the output directory where all generated plots are saved.

## How to Run an Analysis

All analyses are run from the root directory of the project using a single command structure:

```bash
python SFN/code/generate_plots.py --config <path_to_config_file> --accuracy <dataset>
```

**Arguments:**

-   `--config`: The path to the `.yaml` file that defines the analysis you want to run.
-   `--accuracy`: The dataset to use.
    -   `correct`: Use the `eeg_acc=1` dataset (only correct trials).
    -   `all`: Use the `eeg_all` dataset (all trials).

**Example:**

To run the P1 "Landing Digit (Change)" analysis on all trials, you would use:

```bash
python SFN/code/generate_plots.py --config SFN/configs/p1_landing_digit_change.yaml --accuracy all
```

## How to Create a New Analysis

Creating a new analysis is simple and does not require writing new Python code.

1.  **Copy an Existing Config:** The easiest way to start is to copy an existing `.yaml` file from the `SFN/configs/` directory (e.g., `p1_landing_digit_change.yaml`).
2.  **Rename the File:** Give your new file a descriptive name, like `n1_my_new_contrast.yaml`.
3.  **Edit the Contents:** Open the new file in a text editor and modify the parameters as needed.

### Key Configuration Parameters (`.yaml` file)

-   `analysis_name`: A unique name for your analysis (e.g., `"N1_My_New_Contrast"`). This will be used in the output filename.
-   `erp_component`: The ERP component to analyze (e.g., `"P1"`, `"N1"`). This must match a key in the `ELECTRODE_GROUPS` dictionary in `utils.py`.
-   `electrode_group_for_erp`: The specific electrode selection to use (e.g., `"Oz"`, `"bilateral"`). This must be a key within the `erp_component`'s entry in `utils.py`.
-   `time_window_peak_detection`: (Optional) The time range `[start, end]` in seconds for the automatic peak detection algorithm to search within.
-   `time_window_half_width_ms`: (Optional) The duration in milliseconds to add and subtract from the detected peak to create the final analysis window.
-   `fixed_analysis_window`: (Optional) A manual override `[start, end]` in seconds for the analysis window. If this parameter is present, the automatic peak detection will be skipped.
-   `conditions`: A dictionary defining how to group raw condition numbers into the conditions for your plot. The keys are the names that will appear in the plot legend.
-   `plot_title`: The main title that will appear on the final generated plot.
-   `generate_individual_plots`: Set to `false` for this project to only generate the group-level plot.
