import mne
import os
import glob
import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import numpy as np
from scipy.signal import find_peaks

# --- 1. CONFIGURATION ---
# Base conditions to load
BASE_CONDITIONS = ['43', '53', '63']

# How to combine base conditions into key conditions
KEY_CONDITIONS_MAP = {
    "4 to 3": ["43"],
    "5 to 3": ["53"],
    "6 to 3": ["63"],
}

# Define colors for plots
CONDITION_COLORS = {
    "4 to 3": '#4daf4a',  # Green
    "5 to 3": '#984ea3',  # Purple
    "6 to 3": '#ff7f00',  # Orange
}

# Electrodes of interest for P1 waveform (Oz area)
P1_ELECTRODES = ['E71', 'E75', 'E76', 'E70', 'E83', 'E74', 'E81', 'E82']

# Time window for P1 peak search
PEAK_TMIN, PEAK_TMAX = 0.080, 0.130

# Standard list of non-scalp channels to exclude
NON_SCALP_CHANNELS = [
    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E43', 'E44', 'E48', 
    'E49', 'E113', 'E114', 'E119', 'E120', 'E121', 'E125', 'E126', 'E127', 'E128'
]

def generate_p1_contrast_plots(subjects_to_process):
    """
    Generates combined ERP and topomap plots for the P1 "landing on 3, decreasing" contrast.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    script_name = os.path.basename(__file__).replace('.py', '')
    
    all_subject_evokeds = {cond: [] for cond in BASE_CONDITIONS}

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects for P1 Contrast plots: {subjects_to_process} ---")

    # --- Individual Subject Plots ---
    for subject_id in subjects_to_process:
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        subject_figure_dir = os.path.join(subject_dir, 'figures', script_name)
        os.makedirs(subject_figure_dir, exist_ok=True)
        print(f"\nProcessing Subject {subject_id}...")
        
        try:
            # Load and collect evokeds
            base_evokeds = {cond: mne.read_epochs(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'), preload=True, verbose=False).average() for cond in BASE_CONDITIONS if os.path.exists(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'))}
            for cond, evoked in base_evokeds.items(): all_subject_evokeds[cond].append(evoked)
            if not base_evokeds: print(f"  - No data found. Skipping."); continue
            
            key_evokeds = {key_cond: mne.combine_evoked([base_evokeds[bc] for bc in bcl if bc in base_evokeds], 'equal') for key_cond, bcl in KEY_CONDITIONS_MAP.items() if any(bc in base_evokeds for bc in bcl)}
            if not key_evokeds: print(f"  - Not enough data for key conditions. Skipping."); continue

            # --- Create Plot ---
            fig = plt.figure(figsize=(12, 8))
            fig.suptitle(f'Subject {subject_id}: P1 Contrast - Landing on "3" (Decreasing, ALL)', fontsize=16)
            gs = gridspec.GridSpec(2, len(key_evokeds), height_ratios=[2, 1.5])
            ax_erp = fig.add_subplot(gs[0, :])

            mne.viz.plot_compare_evokeds(key_evokeds, picks=P1_ELECTRODES, combine='mean', axes=ax_erp, title="Mean ERP over Oz Region", show=False, legend='upper left', ci=False, colors=CONDITION_COLORS)

            # --- Find Peaks and Plot Topomaps ---
            peak_times = {}
            peak_found_info = {}
            sfreq = key_evokeds[list(key_evokeds.keys())[0]].info["sfreq"]

            for condition in key_evokeds:
                # Find the peak in the P1 time window
                data = key_evokeds[condition].get_data(picks=P1_ELECTRODES)
                data = data.mean(axis=0)
                times = key_evokeds[condition].times * 1000  # convert to ms

                # Find peak using scipy's find_peaks
                peaks, properties = find_peaks(
                    data,
                    height=0,
                    prominence=1.2,
                    distance=sfreq * 0.05,
                )

                # Filter peaks to be in the P1 time window (e.g., 80-130 ms)
                time_min, time_max = 80, 130
                peak_indices_in_window = [
                    p
                    for p in peaks
                    if time_min <= times[p] <= time_max
                ]

                if len(peak_indices_in_window) > 0:
                    # Find the peak with the highest prominence
                    prominences = properties["prominences"][
                        [np.where(peaks == p)[0][0] for p in peak_indices_in_window]
                    ]
                    max_prominence_index = np.argmax(prominences)
                    peak_index = peak_indices_in_window[max_prominence_index]
                    peak_time = times[peak_index] / 1000 # convert back to seconds
                    peak_times[condition] = peak_time
                    peak_found_info[condition] = True
                else:
                    peak_times[condition] = None
                    peak_found_info[condition] = False

            # If any peak time is None, use the average of the other peak times
            valid_peak_times = [t for t in peak_times.values() if t is not None]
            if len(valid_peak_times) > 0:
                average_peak_time = np.mean(valid_peak_times)
            else:
                average_peak_time = 0.112  # Fallback if no peaks are found in any condition

            for condition in peak_times:
                if peak_times[condition] is None:
                    peak_times[condition] = average_peak_time

            for i, (cond_name, evoked) in enumerate(key_evokeds.items()):
                ax_topo = fig.add_subplot(gs[1, i])
                plot_time = peak_times.get(cond_name)
                
                peak_found = peak_found_info[cond_name]

                if peak_found:
                    title = f"{cond_name}\\nPeak at {int(plot_time*1000)} ms"
                    ax_erp.axvline(x=plot_time, color=CONDITION_COLORS.get(cond_name, 'k'), linestyle='--', linewidth=1.5, alpha=0.8)
                else:
                    title = f"{cond_name}\\n({int(plot_time*1000)} ms)"
                    ax_erp.axvline(x=plot_time, color=CONDITION_COLORS.get(cond_name, 'k'), linestyle=':', linewidth=1.5, alpha=0.6)

                scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
                scalp_evoked.plot_topomap(times=plot_time, axes=ax_topo, show=False, vlim=(-6, 6), colorbar=False)
                ax_topo.set_title(title, color=CONDITION_COLORS.get(cond_name, 'black'))

            fig.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
            cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.2])
            plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax, label='µV')
            
            fig_path = os.path.join(subject_figure_dir, f'sub-{subject_id}_p1_contrast_landing_on_3_decreasing_all.png')
            fig.savefig(fig_path, bbox_inches='tight'); plt.close(fig)
            print(f"    - Saved P1 plot to {fig_path}")

        except Exception as e:
            print(f"--- FAILED to generate P1 plot for Subject {subject_id}. Error: {e} ---")

    # --- Group-Level Plot ---
    group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures', script_name)
    os.makedirs(group_figure_dir, exist_ok=True)
    
    grand_averages_base = {cond: mne.grand_average(evoked_list) for cond, evoked_list in all_subject_evokeds.items() if evoked_list}
    if not grand_averages_base: print("\n--- No data for group plot. ---"); return

    grand_averages_key = {key_cond: mne.combine_evoked([grand_averages_base[bc] for bc in bcl if bc in grand_averages_base], 'equal') for key_cond, bcl in KEY_CONDITIONS_MAP.items() if any(bc in grand_averages_base for bc in bcl)}
    if not grand_averages_key: print("\n--- Not enough data for group key conditions. ---"); return

    print("\n--- Generating group-level grand average P1 contrast plot ---")

    fig_grp = plt.figure(figsize=(12, 8))
    fig_grp.suptitle('Grand Average: P1 Contrast - Landing on "3" (Decreasing, ALL)', fontsize=16)
    gs_grp = gridspec.GridSpec(2, len(grand_averages_key), height_ratios=[2, 1.5])
    ax_erp_grp = fig_grp.add_subplot(gs_grp[0, :])

    mne.viz.plot_compare_evokeds(
        grand_averages_key, picks=P1_ELECTRODES, combine='mean', axes=ax_erp_grp,
        title="Grand Average Mean ERP over Oz Region", show=False, legend='upper left',
        ci=0.95, colors=CONDITION_COLORS
    )
    
    # --- Find P1 peaks for each condition for topomaps ---
    peak_times_grp = {}
    peak_found_info_grp = {}
    sfreq = grand_averages_key[list(grand_averages_key.keys())[0]].info["sfreq"]

    for condition in grand_averages_key:
        # Find the peak in the P1 time window
        data = grand_averages_key[condition].get_data(picks=P1_ELECTRODES)
        data = data.mean(axis=0)
        times = grand_averages_key[condition].times * 1000  # convert to ms

        # Find peak using scipy's find_peaks
        peaks, properties = find_peaks(
            data,
            height=0,
            prominence=1.2,
            distance=sfreq * 0.05,
        )

        # Filter peaks to be in the P1 time window (e.g., 80-130 ms)
        time_min, time_max = 80, 130
        peak_indices_in_window = [
            p
            for p in peaks
            if time_min <= times[p] <= time_max
        ]

        if len(peak_indices_in_window) > 0:
            # Find the peak with the highest prominence
            prominences = properties["prominences"][
                [np.where(peaks == p)[0][0] for p in peak_indices_in_window]
            ]
            max_prominence_index = np.argmax(prominences)
            peak_index = peak_indices_in_window[max_prominence_index]
            peak_time = times[peak_index] / 1000 # convert back to seconds
            peak_times_grp[condition] = peak_time
            peak_found_info_grp[condition] = True
        else:
            peak_times_grp[condition] = None
            peak_found_info_grp[condition] = False

    # If any peak time is None, use the average of the other peak times
    valid_peak_times = [t for t in peak_times_grp.values() if t is not None]
    if len(valid_peak_times) > 0:
        average_peak_time = np.mean(valid_peak_times)
    else:
        average_peak_time = 0.112  # Fallback if no peaks are found in any condition

    for condition in peak_times_grp:
        if peak_times_grp[condition] is None:
            peak_times_grp[condition] = average_peak_time

    for i, (cond_name, evoked) in enumerate(grand_averages_key.items()):
        ax_topo_grp = fig_grp.add_subplot(gs_grp[1, i])
        plot_time = peak_times_grp.get(cond_name)
        
        peak_found = peak_found_info_grp[cond_name]
        
        if peak_found:
            title = f"{cond_name}\\nPeak at {int(plot_time*1000)} ms"
            ax_erp_grp.axvline(x=plot_time, color=CONDITION_COLORS.get(cond_name, 'k'), linestyle='--', linewidth=1.5, alpha=0.8)
        else:
            title = f"{cond_name}\\n({int(plot_time*1000)} ms)"
            ax_erp_grp.axvline(x=plot_time, color=CONDITION_COLORS.get(cond_name, 'k'), linestyle=':', linewidth=1.5, alpha=0.6)
        
        scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
        scalp_evoked.plot_topomap(times=plot_time, axes=ax_topo_grp, show=False, vlim=(-6, 6), colorbar=False)
        ax_topo_grp.set_title(title, color=CONDITION_COLORS.get(cond_name, 'black'))

    fig_grp.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
    cbar_ax_grp = fig_grp.add_axes([0.88, 0.15, 0.02, 0.2])
    plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax_grp, label='µV')
    
    fig_path_grp = os.path.join(group_figure_dir, 'group_p1_contrast_landing_on_3_decreasing_all.png')
    fig_grp.savefig(fig_path_grp, bbox_inches='tight'); plt.close(fig_grp)
    print(f"  - Saved grand average P1 plot to {fig_path_grp}")

    print("\n--- P1 contrast plot generation complete. ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate EEG P1 contrast plots for landing on 3 (decreasing).')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process. If not provided, all subjects will be processed.')
    args = parser.parse_args()
    generate_p1_contrast_plots(args.subjects)