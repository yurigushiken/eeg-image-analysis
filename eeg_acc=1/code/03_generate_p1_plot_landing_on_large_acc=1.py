import mne
import os
import glob
import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import numpy as np

# --- 1. CONFIGURATION ---
# Base conditions to load
BASE_CONDITIONS = ['14', '24', '34', '25', '35', '45', '36', '46', '56']

# How to combine base conditions into key conditions
KEY_CONDITIONS_MAP = {
    "Landing on 4": ["14", "24", "34"],
    "Landing on 5": ["25", "35", "45"],
    "Landing on 6": ["36", "46", "56"],
}

# Define colors for plots
CONDITION_COLORS = {
    "Landing on 4": '#d62728',  # Red
    "Landing on 5": '#ff7f0e',  # Orange
    "Landing on 6": '#8c564b',  # Copper
}

# Electrodes of interest for P1 waveform (Oz area)
P1_ELECTRODES = ['E71', 'E75', 'E76', 'E70', 'E83', 'E74', 'E81', 'E82']

# Time window for P1 peak search
P1_TMIN, P1_TMAX = 0.080, 0.130

# Standard list of non-scalp channels to exclude
NON_SCALP_CHANNELS = [
    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E43', 'E44', 'E48', 
    'E49', 'E113', 'E114', 'E119', 'E120', 'E121', 'E125', 'E126', 'E127', 'E128'
]

def generate_p1_plots(subjects_to_process):
    """
    Generates combined bilateral ERP waveform and topomap plots for P1 analysis
    with dynamic peak detection for topomaps.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    
    all_subject_evokeds = {cond: [] for cond in BASE_CONDITIONS}

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects for P1 plots: {subjects_to_process} ---")

    for subject_id in subjects_to_process:
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        
        # We collect base evokeds for the group plot, no individual plots generated in this script.
        try:
            for cond in BASE_CONDITIONS:
                epo_file = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif')
                if os.path.exists(epo_file):
                    evoked = mne.read_epochs(epo_file, preload=True, verbose=False).average()
                    all_subject_evokeds[cond].append(evoked)
        except Exception as e:
            print(f"--- FAILED to load data for Subject {subject_id}. Error: {e} ---")

    # --- Group-Level Plot ---
    group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures')
    os.makedirs(group_figure_dir, exist_ok=True)
    
    grand_averages_base = {cond: mne.grand_average(evoked_list) for cond, evoked_list in all_subject_evokeds.items() if evoked_list}
    if not grand_averages_base: print("\n--- No data for group plot. ---"); return

    grand_averages_key = {key_cond: mne.combine_evoked([grand_averages_base[bc] for bc in bcl if bc in grand_averages_base], 'equal') for key_cond, bcl in KEY_CONDITIONS_MAP.items() if any(bc in grand_averages_base for bc in bcl)}
    if not grand_averages_key: print("\n--- Not enough data for group key conditions. ---"); return

    print("\n--- Generating group-level grand average P1 plot ---")
    fig_grp = plt.figure(figsize=(12, 8))
    fig_grp.suptitle('Grand Average: P1 Analysis (Landing on Large, ACC=1)', fontsize=16)
    gs_grp = gridspec.GridSpec(2, len(grand_averages_key), height_ratios=[2, 1.5])
    ax_erp_grp = fig_grp.add_subplot(gs_grp[0, :])

    mne.viz.plot_compare_evokeds(
        grand_averages_key,
        picks=P1_ELECTRODES,
        combine='mean',
        axes=ax_erp_grp,
        title="Grand Average Mean ERP over Oz Region",
        show=False,
        legend='upper left',
        ci=0.95,
        colors=CONDITION_COLORS
    )
    
    for i, (cond_name, evoked) in enumerate(grand_averages_key.items()):
        ax_topo_grp = fig_grp.add_subplot(gs_grp[1, i])
        
        # --- Dynamic peak detection on the MEAN of the ROI ---
        # 1. Isolate the ROI and manually average the data
        roi_evoked = evoked.copy().pick(P1_ELECTRODES)
        mean_data = roi_evoked.data.mean(axis=0, keepdims=True)
        
        # 2. Create a temporary Evoked object for the mean waveform
        mean_info = mne.create_info(ch_names=['mean_roi'], sfreq=evoked.info['sfreq'], ch_types='eeg')
        mean_roi_evoked = mne.EvokedArray(mean_data, mean_info, tmin=evoked.tmin)
        
        # 3. Find the peak on the single-channel (mean) object
        _, peak_time, _ = mean_roi_evoked.get_peak(tmin=P1_TMIN, tmax=P1_TMAX, mode='pos', return_amplitude=True)
        
        # 4. Draw the vertical line on the main ERP plot
        ax_erp_grp.axvline(x=peak_time, color=CONDITION_COLORS.get(cond_name, 'k'), linestyle='--', linewidth=1.5, alpha=0.8)

        # 5. Plot the topomap using the detected peak time
        scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
        scalp_evoked.plot_topomap(times=peak_time, axes=ax_topo_grp, show=False, vlim=(-6, 6), colorbar=False)
        ax_topo_grp.set_title(f"{cond_name}\nPeak at {int(peak_time*1000)} ms", color=CONDITION_COLORS.get(cond_name, 'black'))

    fig_grp.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
    cbar_ax_grp = fig_grp.add_axes([0.88, 0.15, 0.02, 0.2])
    plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax_grp, label='µV')
    
    fig_path_grp = os.path.join(group_figure_dir, 'group_p1_plot_landing_on_large_acc=1.png')
    fig_grp.savefig(fig_path_grp, bbox_inches='tight'); plt.close(fig_grp)
    print(f"  - Saved grand average P1 plot to {fig_path_grp}")

    print("\n--- P1 plot generation complete. ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate EEG P1 waveform and topomap plots with dynamic peak detection.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process. If not provided, all subjects will be processed.')
    args = parser.parse_args()
    generate_p1_plots(args.subjects) 