"""
SFN2 Plotting Utilities for Cluster Analysis
"""
import logging
import matplotlib.pyplot as plt
import numpy as np
import mne

log = logging.getLogger()


def plot_contrast_erp(grand_average, stats_results, config, output_dir, ch_names):
    """
    Plots the grand average contrast ERP, averaged over channels in the most
    significant cluster, with the cluster's time window shaded.
    """
    t_obs, clusters, cluster_p_values, _ = stats_results
    alpha = config['stats']['cluster_alpha']
    
    # Find significant clusters and select the one with the smallest p-value
    sig_cluster_indices = np.where(cluster_p_values < alpha)[0]
    if not sig_cluster_indices.size:
        log.info("No significant clusters found. Skipping ERP plot.")
        return

    # Select the most significant cluster
    most_sig_idx = sig_cluster_indices[cluster_p_values[sig_cluster_indices].argmin()]
    log.info(f"Plotting ERP for most significant cluster (p={cluster_p_values[most_sig_idx]:.4f})")

    # Get the boolean mask for the cluster (shape: n_times, n_channels)
    mask = clusters[most_sig_idx]
    
    # Find the channels and time points belonging to this cluster
    ch_mask = mask.any(axis=0)
    time_mask = mask.any(axis=1)
    
    cluster_ch_names = [ch_names[i] for i, in_cluster in enumerate(ch_mask) if in_cluster]
    cluster_times = grand_average.times[time_mask]
    tmin, tmax = cluster_times[0], cluster_times[-1]

    # Create a spatial selection for the channels in the cluster
    picks = mne.pick_channels(grand_average.info['ch_names'], include=cluster_ch_names)

    # Average the grand average data over the selected channels
    roi_data = grand_average.get_data(picks=picks).mean(axis=0)

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(grand_average.times * 1000, roi_data * 1e6, lw=2, label='Grand Average Contrast')
    ax.axvspan(tmin * 1000, tmax * 1000, alpha=0.2, color='red', label=f'Significant Cluster (p={cluster_p_values[most_sig_idx]:.3f})')
    
    ax.axhline(0, ls='--', color='black', lw=1)
    ax.axvline(0, ls='-', color='black', lw=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(f"Contrast: {config['contrast']['name']}\n(Channels averaged over cluster)")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Amplitude (µV)")
    ax.legend(loc='lower left')
    plt.tight_layout()

    # Save figure
    fname = output_dir / f"{config['analysis_name']}_erp_cluster.png"
    fig.savefig(fname, dpi=300)
    log.info(f"Saved ERP cluster plot to {fname}")
    plt.close(fig)


def plot_t_value_topomap(grand_average, stats_results, config, output_dir, ch_names):
    """
    Plots a topomap of the t-values, averaged over the time window of the most
    significant cluster.
    """
    t_obs, clusters, cluster_p_values, _ = stats_results
    alpha = config['stats']['cluster_alpha']

    sig_cluster_indices = np.where(cluster_p_values < alpha)[0]
    if not sig_cluster_indices.size:
        log.info("No significant clusters found. Skipping topomap plot.")
        return

    most_sig_idx = sig_cluster_indices[cluster_p_values[sig_cluster_indices].argmin()]
    log.info(f"Plotting topomap for most significant cluster (p={cluster_p_values[most_sig_idx]:.4f})")

    # Reshape t-values to (n_times, n_channels)
    t_obs_tc = t_obs.reshape(len(grand_average.times), len(ch_names))

    # Get time mask for the significant cluster
    time_mask = clusters[most_sig_idx].any(axis=1)
    cluster_times = grand_average.times[time_mask]
    tmin, tmax = cluster_times[0], cluster_times[-1]

    # Average t-values across the cluster's time window
    t_topo = t_obs_tc[time_mask, :].mean(axis=0)

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 5))
    title = (f"T-Values ({tmin*1000:.0f} - {tmax*1000:.0f} ms)\n"
             f"p = {cluster_p_values[most_sig_idx]:.4f}")
    
    im, _ = mne.viz.plot_topomap(t_topo, grand_average.info, axes=ax, show=False,
                                 cmap='RdBu_r', contours=6)
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("T-Value")
    ax.set_title(title)
    
    # Save figure
    fname = output_dir / f"{config['analysis_name']}_topomap_cluster.png"
    fig.savefig(fname, dpi=300)
    log.info(f"Saved T-value topomap to {fname}")
    plt.close(fig)


def plot_source_clusters(stats_results, stc_grand_average, config, output_dir):
    """
    Plots significant source-space clusters on the fsaverage brain.
    """
    alpha = config['stats']['cluster_alpha']
    p_values = stats_results[2]
    
    if np.min(p_values) >= alpha:
        log.info("No significant source clusters to plot.")
        return

    log.info("Visualizing significant source clusters...")
    
    # Use MNE's utility to summarize clusters into a SourceEstimate object
    # This makes plotting results on the brain surface straightforward
    stc_cluster_summary = mne.stats.summarize_clusters_stc(
        stats_results,
        p_thresh=alpha,
        tstep=stc_grand_average.tstep,
        tmin=stc_grand_average.tmin,  # Ensure time axis is correct
        vertices=stc_grand_average.vertices,
        subject='fsaverage'
    )

    # Optional: make the overlay visible if activation values are small
    data = np.abs(stc_cluster_summary.data)
    if data.any():
        lims = np.percentile(data[data > 0], [85, 97, 99.5])
        clim = dict(kind='value', lims=lims)
    else:
        clim = 'auto'

    # Plot the summary STC
    # MNE's plot function for STCs is powerful and can handle brain visualization
    subjects_dir = mne.get_config('SUBJECTS_DIR')
    if subjects_dir is None:
        log.error("Freesurfer subjects directory not found. Cannot plot source clusters. "
                  "Please set the SUBJECTS_DIR environment variable.")
        return

    # Get the time point of maximum activation in the summary STC to center the plot
    # Use try-except block for robustness if no peak is found
    try:
        initial_time = stc_cluster_summary.get_peak(mode='abs')[1]
    except IndexError:
        initial_time = None  # No peak found, let MNE decide

    brain = stc_cluster_summary.plot(
        subjects_dir=subjects_dir,
        subject='fsaverage',
        surface='inflated',
        hemi='both',
        time_label='Significant Clusters',
        initial_time=initial_time,
        size=(800, 600),
        views=['lat', 'med'],
        clim=clim,  # Use calculated color limits for better visibility
        time_viewer=False  # Recommended for scripting to avoid GUI issues
    )

    # Save the brain visualization to a file
    fname = output_dir / f"{config['analysis_name']}_source_cluster.png"
    brain.save_image(fname)
    brain.close()
    log.info(f"Saved source cluster plot to {fname}")
