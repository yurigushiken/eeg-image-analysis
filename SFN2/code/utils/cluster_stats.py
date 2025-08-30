"""
SFN2 Cluster Statistics Utilities
"""
import logging
import mne
import numpy as np
from scipy.stats import t as t_dist
from scipy.sparse import csr_matrix
from scipy.spatial.distance import pdist, squareform

log = logging.getLogger()


def _distance_adjacency(info, threshold=0.04):
    """
    Computes adjacency matrix based on channel positions and a distance threshold.
    """
    picks = mne.pick_types(info, meg=False, eeg=True)
    ch_names = [info['ch_names'][p] for p in picks]
    pos = np.array([info['chs'][p]['loc'][:3] for p in picks])

    if not np.isfinite(pos).all() or np.allclose(pos, 0):
        raise RuntimeError(
            "Channel positions are invalid or absent. "
            "Please ensure a montage is set on your data."
        )

    # Calculate pairwise distances and apply threshold
    dist_matrix = squareform(pdist(pos))
    adjacency_matrix = dist_matrix <= threshold
    
    # Convert to sparse matrix format expected by MNE
    adjacency = csr_matrix(adjacency_matrix)
    return adjacency, ch_names


def run_sensor_cluster_test(contrasts, config):
    """
    Runs a sensor-space cluster permutation test on a list of evoked contrasts.
    """
    # 1. Prepare data for MNE stats function
    log.info("Preparing data for sensor-space cluster analysis...")
    X = np.array([c.get_data() for c in contrasts])
    X = X.transpose(0, 2, 1)  # (n_subjects, n_times, n_channels)
    log.info(f"Data stacked into shape: {X.shape}")

    # 2. Get channel adjacency
    log.info("Finding channel adjacency...")
    info_ref = contrasts[0].info
    conn_cfg = config['stats'].get('connectivity', 'eeg')

    if isinstance(conn_cfg, str):
        adjacency, ch_names = mne.channels.find_ch_adjacency(info_ref, ch_type=conn_cfg)
    elif isinstance(conn_cfg, dict) and conn_cfg.get('method') == 'distance':
        adjacency, ch_names = _distance_adjacency(
            info_ref, threshold=conn_cfg.get('threshold', 0.04)
        )
    else:
        raise ValueError(f"Invalid connectivity configuration: {conn_cfg!r}")

    # 3. Define the statistical threshold
    p_threshold = config['stats']['p_threshold']
    t_threshold = t_dist.ppf(1.0 - p_threshold / 2., len(contrasts) - 1)
    log.info(f"Calculated t-threshold for cluster formation: {t_threshold:.3f} (for p < {p_threshold})")

    # 4. Run the cluster permutation test
    log.info(f"Running cluster permutation test with {config['stats']['n_permutations']} permutations...")
    stat_results = mne.stats.spatio_temporal_cluster_1samp_test(
        X,
        adjacency=adjacency,
        threshold=t_threshold,
        tail=config['stats']['tail'],
        n_permutations=config['stats']['n_permutations'],
        out_type='mask',  # Return boolean masks for easy visualization
        n_jobs=-1,        # Use all available CPU cores
        verbose=False
    )
    log.info("Cluster analysis complete.")

    t_obs, clusters, cluster_p_values, H0 = stat_results
    return (t_obs, clusters, cluster_p_values, H0), ch_names


def run_source_cluster_test(stcs, fsaverage_src, config):
    """
    Runs a spatio-temporal cluster 1-sample t-test on source-space contrasts.
    """
    if len(stcs) < 2:
        raise ValueError("Cannot run source cluster test with fewer than 2 subjects.")

    log.info("Preparing data for source-space cluster analysis...")
    # Stack data into a (n_subjects, n_times, n_vertices) array
    # Data is transposed from (n_vertices, n_times) to (n_times, n_vertices)
    X = np.stack([stc.data.T for stc in stcs], axis=0)
    log.info(f"Data stacked into shape: {X.shape}")

    # Get source space adjacency
    log.info("Calculating source space adjacency for fsaverage...")
    source_adjacency = mne.spatial_src_adjacency(fsaverage_src)

    # Calculate t-threshold from the p-value in the config
    n_subjects = X.shape[0]
    p_init = config['stats']['p_threshold']
    t_threshold = t_dist.ppf(1 - p_init / 2, df=n_subjects - 1)
    log.info(f"Calculated t-threshold for cluster formation: {t_threshold:.3f} (for p < {p_init})")

    # Run the cluster permutation test
    log.info(f"Running source cluster permutation test with {config['stats']['n_permutations']} permutations...")
    stat_results = mne.stats.spatio_temporal_cluster_1samp_test(
        X,
        adjacency=source_adjacency,
        threshold=t_threshold,
        tail=config['stats']['tail'],
        n_permutations=config['stats']['n_permutations'],
        out_type='indices',  # Ensure output is indices for plotting
        max_step=1,          # Recommended for spatio-temporal clustering
        n_jobs=-1,
        seed=config['stats'].get('seed', None),
        verbose=False
    )
    log.info("Source cluster analysis complete.")
    return stat_results
