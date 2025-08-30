"""
SFN2 Source-Space Analysis Pipeline
"""
import argparse
import logging
from pathlib import Path
import mne
import numpy as np

from SFN2.code.utils import data_loader, cluster_stats, plotting, reporter

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()


def main():
    parser = argparse.ArgumentParser(description="Run SFN2 Source-Space Analysis Pipeline")
    parser.add_argument("--config", type=str, required=True, help="Path to the config YAML file.")
    parser.add_argument("--accuracy", type=str, required=True, choices=['all', 'acc1'], help="Dataset to use.")
    args = parser.parse_args()

    # --- 1. Load Config and Setup ---
    config = data_loader.load_config(args.config)
    analysis_name = config['analysis_name']
    output_dir = Path("SFN2/derivatives/source") / analysis_name
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Output directory created at: {output_dir}")

    # --- 2. Load Data and Compute Source Contrasts ---
    subject_dirs = data_loader.get_subject_dirs(args.accuracy)
    fsaverage_src = data_loader.get_fsaverage_src()

    all_source_contrasts = []
    log.info("Processing subjects for source analysis...")
    for subject_dir in subject_dirs:
        log.info(f"  - {subject_dir.name}")
        contrast_evoked, epochs_for_cov = data_loader.create_subject_contrast(subject_dir, config)
        if contrast_evoked is None:
            continue

        inv_operator = None
        try:
            inv_operator = data_loader.get_inverse_operator(subject_dir)
        except FileNotFoundError:
            log.warning(
                f"Inverse operator not found for {subject_dir.name}. "
                "Attempting to generate one using fsaverage template..."
            )
            try:
                inv_operator = data_loader.generate_template_inverse_operator_from_epochs(
                    epochs_for_cov, subject_dir
                )
            except Exception as e:
                log.error(
                    f"Failed to generate template inverse operator for {subject_dir.name}: {e}"
                )
                continue  # Skip subject if generation fails

        if inv_operator is None:
            log.warning(f"Could not load or generate inverse operator for {subject_dir.name}. Skipping subject.")
            continue

        stc = data_loader.compute_subject_source_contrast(
            contrast_evoked, inv_operator, config
        )
        all_source_contrasts.append(stc)

    if not all_source_contrasts:
        log.error("No valid source data found for any subject. Cannot proceed.")
        return
    log.info(f"Successfully created source contrasts for {len(all_source_contrasts)} subjects.")

    # --- 3. Compute Grand Average Source Estimate ---
    log.info("Computing grand average source estimate...")
    # Sum all STCs and divide by N for the grand average
    stc_grand_average = np.sum(all_source_contrasts) / len(all_source_contrasts)
    ga_fname = output_dir / f"{analysis_name}_grand_average-stc.h5"
    stc_grand_average.save(ga_fname, overwrite=True)

    # --- 4. Run Group-Level Cluster Statistics ---
    stats_results = cluster_stats.run_source_cluster_test(all_source_contrasts, fsaverage_src, config)

    # --- 5. Generate Report and Visualizations ---
    log.info("Generating source report and plots...")
    reporter.generate_source_report(stats_results, stc_grand_average, config, output_dir)
    plotting.plot_source_clusters(stats_results, stc_grand_average, config, output_dir)
    
    log.info("-" * 80)
    log.info(f"Source pipeline finished successfully for '{analysis_name}'.")
    log.info(f"All outputs are saved in: {output_dir}")
    log.info("-" * 80)


if __name__ == "__main__":
    main()

