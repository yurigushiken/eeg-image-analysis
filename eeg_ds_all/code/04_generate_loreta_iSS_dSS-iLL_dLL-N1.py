# --- 1. CONFIGURATION ---
import os
import numpy as np
import mne
import sys

# --- Paths and Directories ---
# This setup assumes the script is executed from the 'eeg_ds_all/code' directory.
try:
    # Get the parent directory of the script's directory (e.g., 'eeg_ds_all')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    # Fallback for interactive environments where __file__ is not defined
    BASE_DIR = r"D:\numbers_eeg\eeg_ds_all"

DERIVATIVES_DIR = os.path.join(BASE_DIR, "derivatives")
FBAVERAGE_DIR = os.path.join(DERIVATIVES_DIR, "fsaverage")
FS_SUBJECTS_DIR = os.path.join(FBAVERAGE_DIR, "fs_subjects_dir")
FIGURES_DIR = os.path.join(DERIVATIVES_DIR, "group", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# --- Participant List ---
PARTICIPANT_LIST = [
    "02", "03", "04", "05", "08", "09", "10", "11", "12", "13", "14", "15",
    "17", "21", "22", "23", "25", "26", "27", "28", "29", "31", "32", "33"
]

# --- Condition Definitions ---
SMALL_NUM_CONDITIONS = ['iSS', 'dSS']
LARGE_NUM_CONDITIONS = ['iLL', 'dLL']

# --- Analysis Parameters for N1 ---
TMIN_STATS, TMAX_STATS = 0.125, 0.200
METHOD = "eLORETA"
LAMBDA2 = 1.0 / 9.0  # Corresponds to SNR=3

print("--- Starting LORETA Core Systems Contrast Analysis (N1 window: 125-200ms) ---")
print(f"Derivatives directory: {DERIVATIVES_DIR}")
print(f"Freesurfer subjects directory: {FS_SUBJECTS_DIR}")

# --- 2. PER-SUBJECT PROCESSING LOOP ---
all_stcs_small = []
all_stcs_large = []
src_for_adjacency = None  # We'll capture the correct source space here

# Load forward solution and source space (common for all subjects)
fwd_path = os.path.join(FBAVERAGE_DIR, "fsaverage-fwd.fif")
src_path = os.path.join(FBAVERAGE_DIR, "fsaverage-src.fif")

try:
    forward = mne.read_forward_solution(fwd_path)
    src = mne.read_source_spaces(src_path)
except FileNotFoundError:
    print(f"ERROR: Could not find forward solution '{fwd_path}' or source space '{src_path}'.")
    print("Please ensure that these files have been generated and are in the correct directory.")
    sys.exit(1)


print("Processing participants...")
for subject_id in PARTICIPANT_LIST:
    print(f"  - Subject {subject_id}")
    subject_dir = os.path.join(DERIVATIVES_DIR, f"sub-{subject_id}")

    try:
        # Load epochs for all relevant conditions first
        epochs_small_list = []
        for cond in SMALL_NUM_CONDITIONS:
             fname = os.path.join(subject_dir, f"sub-{subject_id}_task-numbers_cond-{cond}_epo.fif")
             epochs_small_list.append(mne.read_epochs(fname, verbose=False))

        epochs_large_list = []
        for cond in LARGE_NUM_CONDITIONS:
            fname = os.path.join(subject_dir, f"sub-{subject_id}_task-numbers_cond-{cond}_epo.fif")
            epochs_large_list.append(mne.read_epochs(fname, verbose=False))

        epochs_small = mne.concatenate_epochs(epochs_small_list)
        epochs_large = mne.concatenate_epochs(epochs_large_list)

        # Compute noise covariance from all combined trials for robustness
        all_epochs = mne.concatenate_epochs([epochs_small, epochs_large])
        noise_cov = mne.compute_covariance(all_epochs, tmax=0.0, method='shrunk', rank=None, verbose=False)

        # Calculate evoked responses first, as they are needed for the inverse operator
        evoked_small = epochs_small.average()
        evoked_large = epochs_large.average()

        # Create the inverse operator using the evoked info
        inverse_operator = mne.minimum_norm.make_inverse_operator(
            evoked_small.info,
            forward=forward,
            noise_cov=noise_cov,
            loose='auto',
            depth=0.8,
            fixed=True,
            verbose=False
        )

        # Capture the source space from the first subject's inverse operator.
        # This is the most reliable way to get the source space that corresponds
        # to the data, as some vertices may have been excluded.
        if src_for_adjacency is None:
            src_for_adjacency = inverse_operator['src']

        # Apply inverse operator to get STCs using eLORETA
        stc_small = mne.minimum_norm.apply_inverse(
            evoked_small, inverse_operator, lambda2=LAMBDA2, method=METHOD, pick_ori=None
        )
        stc_large = mne.minimum_norm.apply_inverse(
            evoked_large, inverse_operator, lambda2=LAMBDA2, method=METHOD, pick_ori=None
        )

        # Crop and append for group analysis
        all_stcs_small.append(stc_small.crop(tmin=TMIN_STATS, tmax=TMAX_STATS))
        all_stcs_large.append(stc_large.crop(tmin=TMIN_STATS, tmax=TMAX_STATS))

    except FileNotFoundError as e:
        print(f"    - WARNING: Could not find an epochs file for subject {subject_id}. Skipping. Details: {e}")
        continue
    except Exception as e:
        print(f"    - WARNING: An unexpected error occurred for subject {subject_id}. Skipping. Details: {e}")
        continue

if not all_stcs_small or not all_stcs_large:
    print("ERROR: No STC data was loaded. Cannot proceed with statistical analysis.")
    sys.exit(1)

print("\n--- Starting Group-Level Statistics ---")
# --- 3. GROUP-LEVEL STATISTICS ---
# Create the data array for the statistical test (subjects x timepoints x vertices)
X = np.array([s1.data - s2.data for s1, s2 in zip(all_stcs_small, all_stcs_large)])

# Transpose the data to be (subjects, timepoints, vertices) which is required by the function
X = np.transpose(X, (0, 2, 1))

# The permutation test requires knowing which data points are adjacent (in space)
print("  - Computing source space adjacency...")
# Use the source space from the inverse operator to ensure dimensions match
if src_for_adjacency is None:
    raise RuntimeError("Source space for adjacency was not captured from inverse operator.")
adjacency = mne.spatial_src_adjacency(src_for_adjacency)

# Run the cluster-based permutation test (1-sample t-test on the difference waves)
print("  - Running cluster-based permutation test... (this may take a while)")
t_obs, clusters, cluster_p_values, H0 = mne.stats.spatio_temporal_cluster_1samp_test(
    X,
    adjacency=adjacency,
    n_jobs=-1,
    n_permutations=1024,
    out_type='indices',
    verbose=True
)

print("\n--- Visualizing Results ---")
# --- 4. VISUALIZATION ---
alpha = 0.05
significant_cluster_indices = np.where(cluster_p_values < alpha)[0]

# Use the vertices from the first subject's STC as a template
stc_template = all_stcs_small[0]

if not significant_cluster_indices.any():
    print(f"No significant clusters found at p < {alpha}.")
    t_obs_summary = np.mean(t_obs, axis=0) # Average T-stat over the N1 time window
    stc_plot = mne.SourceEstimate(t_obs_summary, vertices=stc_template.vertices, tmin=stc_template.tmin, tstep=stc_template.tstep, subject='fsaverage')
    stc_title = "Small vs. Large Numbers (Unthresholded T-values, N1: 125-200ms)"
else:
    print(f"Found {len(significant_cluster_indices)} significant clusters.")
    t_obs_summary = np.mean(t_obs, axis=0)
    sig_mask = np.zeros_like(t_obs_summary, dtype=bool)
    
    for cluster_idx in significant_cluster_indices:
        v_inds, _ = clusters[cluster_idx]
        sig_mask[v_inds] = True

    stc_summary_data = t_obs_summary
    stc_summary_data[~sig_mask] = 0.0
    stc_plot = mne.SourceEstimate(stc_summary_data, vertices=stc_template.vertices, tmin=stc_template.tmin, tstep=stc_template.tstep, subject='fsaverage')
    stc_title = f'Small vs. Large Numbers (p<{alpha}, N1: 125-200ms)'


# Generate the brain plot
print("  - Generating brain plot...")
brain = stc_plot.plot(
    hemi='both', views=['lat', 'med'], subject='fsaverage',
    subjects_dir=FS_SUBJECTS_DIR,
    title=stc_title,
    time_label='T-statistic (Small vs. Large)',
    size=(800, 600)
)

# Save the figure
output_figure_path = os.path.join(FIGURES_DIR, "group_loreta_core_systems_contrast_N1.png")
try:
    # Manually remove the file if it exists, as save_image doesn't have an overwrite option
    if os.path.exists(output_figure_path):
        os.remove(output_figure_path)
    brain.save_image(output_figure_path)
    print(f"  - Saved contrast plot to: {output_figure_path}")
except Exception as e:
    print(f"  - ERROR saving figure: {e}")

print("\n--- Analysis Complete ---") 