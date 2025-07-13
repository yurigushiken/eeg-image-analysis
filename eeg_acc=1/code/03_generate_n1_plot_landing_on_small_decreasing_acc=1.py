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
BASE_CONDITIONS = ['21', '31', '41', '32', '42', '52', '43', '53', '63']

# How to combine base conditions into key conditions
KEY_CONDITIONS_MAP = {
    "Landing on 1 (from 2,3,4)": ["21", "31", "41"],
    "Landing on 2 (from 3,4,5)": ["32", "42", "52"],
    "Landing on 3 (from 4,5,6)": ["43", "53", "63"],
}

# Define colors for plots
CONDITION_COLORS = {
    "Landing on 1 (from 2,3,4)": '#1f77b4',  # Blue
    "Landing on 2 (from 3,4,5)": '#2ca02c',  # Green
    "Landing on 3 (from 4,5,6)": '#9467bd',  # Purple
}

# Electrodes of interest for N1 waveform (Left and Right hemispheres)
N1_ELECTRODES_L = ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70']
N1_ELECTRODES_R = ['E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83']
# Combine into a single bilateral list
N1_ELECTRODES_BILATERAL = N1_ELECTRODES_L + N1_ELECTRODES_R

# Time window of interest for N1 peak detection
PEAK_TMIN, PEAK_TMAX = 0.125, 0.225

# Standard list of non-scalp channels to exclude
NON_SCALP_CHANNELS = [
    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E43', 'E44', 'E48', 
    'E49', 'E113', 'E114', 'E119', 'E120', 'E121', 'E125', 'E126', 'E127', 'E128'
]

def generate_n1_plots(subjects_to_process):
    """
    Generates combined bilateral ERP waveform and topomap plots for N1 analysis.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    script_name = os.path.basename(__file__).replace('.py', '')
    
    all_subject_evokeds = {cond: [] for cond in BASE_CONDITIONS}

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects for N1 plots: {subjects_to_process} ---")

    # --- Individual Subject Plots ---
    for subject_id in subjects_to_process:
        # ... setup directories ...
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        subject_figure_dir = os.path.join(subject_dir, 'figures', script_name)
        os.makedirs(subject_figure_dir, exist_ok=True)
        print(f"\nProcessing Subject {subject_id}...")
        
        try:
            # ... load data and create key evokeds ...
            base_evokeds = {cond: mne.read_epochs(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'), preload=True, verbose=False).average() for cond in BASE_CONDITIONS if os.path.exists(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'))}
            for cond, evoked in base_evokeds.items(): all_subject_evokeds[cond].append(evoked)
            if not base_evokeds: print(f"  - No data found for Subject {subject_id}. Skipping."); continue
            key_evokeds = {key_cond: mne.combine_evoked([base_evokeds[bc] for bc in bcl if bc in base_evokeds], 'equal') for key_cond, bcl in KEY_CONDITIONS_MAP.items() if any(bc in base_evokeds for bc in bcl)}
            if not key_evokeds: print(f"  - Not enough data for key conditions for Subject {subject_id}. Skipping."); continue

            # --- Find N1 peaks for each condition ---
            peak_times = {}
            for cond_name, evoked in key_evokeds.items():
                # Create a temporary evoked object with just the average of the ROI
                roi_evoked_data = evoked.get_data(picks=N1_ELECTRODES_BILATERAL).mean(axis=0)
                # Create a minimal info object for the single ROI channel
                info = mne.create_info(['ROI_AVG'], evoked.info['sfreq'], ch_types='eeg')
                roi_evoked = mne.EvokedArray(roi_evoked_data[np.newaxis, :], info, tmin=evoked.tmin)
                # Find the peak in the specified time window for the ROI average
                _, peak_time = roi_evoked.get_peak(tmin=PEAK_TMIN, tmax=PEAK_TMAX, mode='neg')
                peak_times[cond_name] = peak_time

            # --- Create the plot ---
            fig = plt.figure(figsize=(14, 8))
            fig.suptitle(f'Subject {subject_id}: N1 Analysis (Landing on Small, Decreasing, ACC=1)', fontsize=16)
            gs = gridspec.GridSpec(2, len(key_evokeds), height_ratios=[2, 1.5])
            ax_erp = fig.add_subplot(gs[0, :])

            # Plot Bilateral average on the axes
            mne.viz.plot_compare_evokeds(
                key_evokeds,
                picks=N1_ELECTRODES_BILATERAL,
                combine='mean',
                axes=ax_erp,
                title="Mean ERP over Bilateral N1 Regions",
                show=False,
                legend='upper left',
                ci=False,
                colors=CONDITION_COLORS
            )

            # Manually add vlines and text for each condition's peak
            y_bounds = ax_erp.get_ylim()
            for cond_name, peak_time in peak_times.items():
                color = CONDITION_COLORS.get(cond_name, 'k')
                ax_erp.axvline(x=peak_time, color=color, linestyle='--', linewidth=1)

            # Plot Topomaps at detected peak times
            for i, (cond_name, evoked) in enumerate(key_evokeds.items()):
                ax_topo = fig.add_subplot(gs[1, i])
                peak_time = peak_times[cond_name]
                scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
                scalp_evoked.plot_topomap(times=peak_time, axes=ax_topo, show=False, vlim=(-6, 6), colorbar=False)
                ax_topo.set_title(f"{cond_name}\n{int(peak_time*1000)} ms", color=CONDITION_COLORS.get(cond_name, 'black'))
            
            # Shared colorbar
            fig.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
            cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.2])
            plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax, label='µV')

            fig_path = os.path.join(subject_figure_dir, f'sub-{subject_id}_n1_plot_landing_on_small_decreasing_acc=1.png')
            fig.savefig(fig_path, bbox_inches='tight'); plt.close(fig)
            print(f"    - Saved N1 plot to {fig_path}")

        except Exception as e:
            print(f"--- FAILED to generate N1 plot for Subject {subject_id}. Error: {e} ---")

    # --- Group-Level Plot ---
    group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures', script_name)
    os.makedirs(group_figure_dir, exist_ok=True)
    
    grand_averages_base = {cond: mne.grand_average(evoked_list) for cond, evoked_list in all_subject_evokeds.items() if evoked_list}
    if not grand_averages_base: print("\n--- No data for group plot. ---"); return

    grand_averages_key = {key_cond: mne.combine_evoked([grand_averages_base[bc] for bc in bcl if bc in grand_averages_base], 'equal') for key_cond, bcl in KEY_CONDITIONS_MAP.items() if any(bc in grand_averages_base for bc in bcl)}
    if not grand_averages_key: print("\n--- Not enough data for group key conditions. ---"); return

    print("\n--- Generating group-level grand average N1 plot ---")

    # --- Find N1 peaks for group grand average ---
    group_peak_times = {}
    for cond_name, evoked in grand_averages_key.items():
        roi_evoked_data = evoked.get_data(picks=N1_ELECTRODES_BILATERAL).mean(axis=0)
        info = mne.create_info(['ROI_AVG'], evoked.info['sfreq'], ch_types='eeg')
        roi_evoked = mne.EvokedArray(roi_evoked_data[np.newaxis, :], info, tmin=evoked.tmin)
        _, peak_time = roi_evoked.get_peak(tmin=PEAK_TMIN, tmax=PEAK_TMAX, mode='neg')
        group_peak_times[cond_name] = peak_time

    fig_grp = plt.figure(figsize=(14, 8))
    fig_grp.suptitle('Grand Average: N1 Analysis (Landing on Small, Decreasing, ACC=1)', fontsize=16)
    gs_grp = gridspec.GridSpec(2, len(grand_averages_key), height_ratios=[2, 1.5])
    ax_erp_grp = fig_grp.add_subplot(gs_grp[0, :])

    mne.viz.plot_compare_evokeds(
        grand_averages_key,
        picks=N1_ELECTRODES_BILATERAL,
        combine='mean',
        axes=ax_erp_grp,
        title="Grand Average Mean ERP over Bilateral N1 Regions",
        show=False,
        legend='upper left',
        ci=0.95,
        colors=CONDITION_COLORS
    )
    
    y_bounds_grp = ax_erp_grp.get_ylim()
    for cond_name, peak_time in group_peak_times.items():
        color = CONDITION_COLORS.get(cond_name, 'k')
        ax_erp_grp.axvline(x=peak_time, color=color, linestyle='--', linewidth=1)

    for i, (cond_name, evoked) in enumerate(grand_averages_key.items()):
        ax_topo_grp = fig_grp.add_subplot(gs_grp[1, i])
        peak_time = group_peak_times[cond_name]
        scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
        scalp_evoked.plot_topomap(times=peak_time, axes=ax_topo_grp, show=False, vlim=(-6, 6), colorbar=False)
        ax_topo_grp.set_title(f"{cond_name}\n{int(peak_time*1000)} ms", color=CONDITION_COLORS.get(cond_name, 'black'))

    fig_grp.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4, wspace=0.4)
    cbar_ax_grp = fig_grp.add_axes([0.88, 0.15, 0.02, 0.2])
    plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax_grp, label='µV')
    
    fig_path_grp = os.path.join(group_figure_dir, 'group_n1_plot_landing_on_small_decreasing_acc=1.png')
    fig_grp.savefig(fig_path_grp, bbox_inches='tight'); plt.close(fig_grp)
    print(f"  - Saved grand average N1 plot to {fig_path_grp}")

    print("\n--- N1 plot generation complete. ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate EEG N1 waveform and topomap plots.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process. If not provided, all subjects will be processed.')
    args = parser.parse_args()
    generate_n1_plots(args.subjects) 