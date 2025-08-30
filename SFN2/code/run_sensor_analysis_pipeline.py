"""
SFN2 Sensor-Space Analysis Pipeline

This script serves as the main entrypoint for running the data-driven,
cluster-based permutation testing analysis on sensor-space EEG data.
"""
import argparse
import logging
from pathlib import Path
import mne

# It's crucial to import the utility modules we've created.
# The `SFN2.code.utils` part assumes you run this as a module from the project root.
from SFN2.code.utils import data_loader, cluster_stats, plotting, reporter

# Setup basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()


def main():
    """
    Main function to orchestrate the sensor-space analysis pipeline.
    """
    parser = argparse.ArgumentParser(description="Run SFN2 Sensor-Space Analysis Pipeline")
    parser.add_argument("--config", type=str, required=True,
                        help="Path to the analysis configuration YAML file.")
    parser.add_argument("--accuracy", type=str, required=True, choices=['all', 'acc1'],
                        help="Dataset to use ('all' for all trials, 'acc1' for correct trials).")
    args = parser.parse_args()

    # --- 1. Load Configuration and Setup ---
    config = data_loader.load_config(args.config)
    analysis_name = config['analysis_name']
    output_dir = Path("SFN2/derivatives/sensor") / analysis_name
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Output directory created at: {output_dir}")

    # --- 2. Load Data and Compute Contrasts for Each Subject ---
    subject_dirs = data_loader.get_subject_dirs(args.accuracy)
    if not subject_dirs:
        log.error("No subject directories found. Exiting.")
        return

    log.info("Creating contrasts for each subject...")
    contrasts = []
    for subject_dir in subject_dirs:
        log.info(f"  - {subject_dir.name}")
        # Unpack the tuple; we only need the Evoked contrast for sensor analysis
        contrast_evoked, _ = data_loader.create_subject_contrast(subject_dir, config)
        if contrast_evoked is not None:
            contrasts.append(contrast_evoked)

    if not contrasts:
        log.error("No valid contrasts could be created. Aborting analysis.")
        return
    log.info(f"Successfully created contrasts for {len(contrasts)} subjects.")

    # --- 3. Compute Grand Average ---
    log.info("Computing grand average contrast...")
    grand_average = mne.grand_average(contrasts)
    ga_fname = output_dir / f"{analysis_name}_grand_average-ave.fif"
    grand_average.save(ga_fname, overwrite=True)
    log.info(f"Grand average saved to {ga_fname}")

    # --- 4. Run Group-Level Cluster Statistics ---
    stats_results, ch_names = cluster_stats.run_sensor_cluster_test(contrasts, config)

    # --- 5. Generate Report and Visualizations ---
    log.info("Generating report and plots...")
    # The `times` vector is needed for the report and plots
    times = grand_average.times

    # Generate text report
    reporter.generate_report(stats_results, times, ch_names, config, output_dir)

    # Generate ERP plot
    plotting.plot_contrast_erp(grand_average, stats_results, config, output_dir, ch_names)

    # Generate topomap plot
    plotting.plot_t_value_topomap(grand_average, stats_results, config, output_dir, ch_names)

    log.info("-" * 80)
    log.info(f"Pipeline finished successfully for '{analysis_name}'.")
    log.info(f"All outputs are saved in: {output_dir}")
    log.info("-" * 80)


if __name__ == "__main__":
    main()
