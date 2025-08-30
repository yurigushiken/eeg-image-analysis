"""
SFN2 Reporting Utilities
"""
import logging
import numpy as np

log = logging.getLogger()


def generate_report(stats_results, times, ch_names, config, output_dir):
    """
    Generates a text report summarizing the cluster statistics results.

    Args:
        stats_results (tuple): The output from the MNE cluster test.
        times (np.ndarray): The time vector.
        ch_names (list): The list of channel names.
        config (dict): The analysis configuration dictionary.
        output_dir (Path): The directory to save the report in.
    """
    t_obs, clusters, cluster_p_values, _ = stats_results
    alpha = config['stats']['cluster_alpha']

    report_path = output_dir / f"{config['analysis_name']}_report.txt"
    log.info(f"Generating statistical report at: {report_path}")

    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write(f"Cluster Analysis Report: {config['analysis_name']}\n")
        f.write("=" * 80 + "\n\n")

        f.write("Analysis Parameters:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Contrast: {config['contrast']['name']}\n")
        f.write(f"  Condition A set: {config['contrast']['condition_A']['condition_set_name']}\n")
        f.write(f"  Condition B set: {config['contrast']['condition_B']['condition_set_name']}\n")
        f.write(f"Time Window: {config['tmin']}s to {config['tmax']}s\n")
        f.write(f"Baseline: {config['baseline'][0]}s to {config['baseline'][1]}s\n")
        f.write("\n")

        f.write("Statistical Parameters:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Cluster-forming p-value (initial): {config['stats']['p_threshold']}\n")
        f.write(f"Cluster significance alpha: {alpha}\n")
        f.write(f"Number of permutations: {config['stats']['n_permutations']}\n")
        f.write(f"Test tail: {'two-sided' if config['stats']['tail'] == 0 else ('positive' if config['stats']['tail'] == 1 else 'negative')}\n")
        f.write("\n")

        f.write("=" * 80 + "\n")
        f.write("RESULTS\n")
        f.write("=" * 80 + "\n\n")

        sig_cluster_indices = np.where(cluster_p_values < alpha)[0]
        if not sig_cluster_indices.size:
            f.write("No significant clusters found.\n")
            log.info("Reported no significant clusters.")
        else:
            f.write(f"Found {len(sig_cluster_indices)} significant cluster(s).\n\n")
            log.info(f"Reporting on {len(sig_cluster_indices)} significant cluster(s).")
            
            # Sort clusters by p-value for reporting
            sorted_indices = sig_cluster_indices[np.argsort(cluster_p_values[sig_cluster_indices])]

            for i, idx in enumerate(sorted_indices):
                p_val = cluster_p_values[idx]
                mask = clusters[idx]
                
                # Get time window of the cluster
                time_mask = mask.any(axis=1)
                cluster_times = times[time_mask]
                tmin, tmax = cluster_times[0], cluster_times[-1]

                # Get channels in the cluster
                ch_mask = mask.any(axis=0)
                cluster_ch_names = [ch_names[c_idx] for c_idx, in_cluster in enumerate(ch_mask) if in_cluster]

                f.write("-" * 40 + "\n")
                f.write(f"Cluster #{i+1} (p-value = {p_val:.4f})\n")
                f.write("-" * 40 + "\n")
                f.write(f"  Time window: {tmin*1000:.1f} ms to {tmax*1000:.1f} ms\n")
                f.write(f"  Number of channels: {len(cluster_ch_names)}\n")
                f.write(f"  Channels involved: {', '.join(cluster_ch_names)}\n\n")

    log.info("Report generation complete.")


def generate_source_report(stats_results, stc_grand_average, config, output_dir):
    """
    Generates a text report summarizing the source-space cluster results.
    """
    _, clusters, cluster_p_values, _ = stats_results
    alpha = config['stats']['cluster_alpha']
    times = stc_grand_average.times

    report_path = output_dir / f"{config['analysis_name']}_report.txt"
    log.info(f"Generating source statistical report at: {report_path}")

    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write(f"Source Cluster Analysis Report: {config['analysis_name']}\n")
        f.write("=" * 80 + "\n\n")

        # Reuse some sensor params, add source-specific ones
        f.write("Analysis Parameters:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Contrast: {config['contrast']['name']}\n")
        f.write(f"  Condition A set: {config['contrast']['condition_A']['condition_set_name']}\n")
        f.write(f"  Condition B set: {config['contrast']['condition_B']['condition_set_name']}\n")
        f.write(f"Time Window: {config['tmin']}s to {config['tmax']}s\n")
        f.write(f"Source Method: {config['source']['method']}\n")
        f.write(f"Source SNR: {config['source']['snr']}\n")
        f.write("\n")

        f.write("Statistical Parameters:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Cluster-forming p-value (initial): {config['stats']['p_threshold']}\n")
        f.write(f"Cluster significance alpha: {alpha}\n")
        f.write(f"Number of permutations: {config['stats']['n_permutations']}\n")
        f.write("\n")

        f.write("=" * 80 + "\n")
        f.write("RESULTS\n")
        f.write("=" * 80 + "\n\n")

        sig_cluster_indices = np.where(cluster_p_values < alpha)[0]
        if not sig_cluster_indices.size:
            f.write("No significant clusters found.\n")
        else:
            f.write(f"Found {len(sig_cluster_indices)} significant cluster(s).\n\n")
            sorted_indices = sig_cluster_indices[np.argsort(cluster_p_values[sig_cluster_indices])]
            for i, idx in enumerate(sorted_indices):
                p_val = cluster_p_values[idx]
                clu = clusters[idx]
                
                # Adapt for both 'mask' and 'indices' out_type from the cluster test
                if isinstance(clu, tuple):  # 'indices' format
                    t_inds, v_inds = clu
                    tmin_cluster, tmax_cluster = times[t_inds[0]], times[t_inds[-1]]
                    n_verts = len(v_inds)
                else:  # 'mask' format
                    time_mask = clu.any(axis=1)
                    tmin_cluster, tmax_cluster = times[time_mask][[0, -1]]
                    n_verts = clu.any(axis=0).sum()

                f.write("-" * 40 + "\n")
                f.write(f"Cluster #{i+1} (p-value = {p_val:.4f})\n")
                f.write("-" * 40 + "\n")
                f.write(f"  Time window: {tmin_cluster*1000:.1f} ms to {tmax_cluster*1000:.1f} ms\n")
                f.write(f"  Number of vertices: {n_verts}\n\n")
    
    log.info("Source report generation complete.")
