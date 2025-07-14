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
BASE_CONDITIONS = ['31', '42', '53', '64']

# How to combine base conditions into key conditions
KEY_CONDITIONS_MAP = {
    "3 to 1": ["31"],
    "4 to 2": ["42"],
    "5 to 3": ["53"],
    "6 to 4": ["64"],
}

# Define colors for plots
CONDITION_COLORS = {
    "3 to 1": '#e41a1c',  # Red
    "4 to 2": '#377eb8',  # Blue
    "5 to 3": '#4daf4a',  # Green
    "6 to 4": '#984ea3',  # Purple
}

# Electrodes of interest for N1 waveform (Bilateral Posterior-Occipito-Temporal)
N1_ELECTRODES_L = ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70']
N1_ELECTRODES_R = ['E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83']
N1_ELECTRODES_BILATERAL = N1_ELECTRODES_L + N1_ELECTRODES_R

# Time window for N1 peak search
PEAK_TMIN, PEAK_TMAX = 0.080, 0.200

# Standard list of non-scalp channels to exclude
NON_SCALP_CHANNELS = [
    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E43', 'E44', 'E48', 
    'E49', 'E113', 'E114', 'E119', 'E120', 'E121', 'E125', 'E126', 'E127', 'E128'
]

def generate_n1_contrast_plots(subjects_to_process):
    """
    Generates combined ERP and topomap plots for the N1 "decreasing minus 2" contrast for all trials.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    script_name = os.path.basename(__file__).replace('.py', '')
    
    all_subject_evokeds = {cond: [] for cond in BASE_CONDITIONS}

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects for N1 Contrast plots (All Trials): {subjects_to_process} ---")

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
            fig.suptitle(f'Subject {subject_id}: N1 Contrast - Decreasing -2 (ALL)', fontsize=16)
            gs = gridspec.GridSpec(2, len(key_evokeds), height_ratios=[2, 1.5])
            ax_erp = fig.add_subplot(gs[0, :])

            mne.viz.plot_compare_evokeds(key_evokeds, picks=N1_ELECTRODES_BILATERAL, combine='mean', axes=ax_erp, title="Mean ERP over Bilateral Posterior-Occipital Region", show=False, legend='upper left', ci=False, colors={cond: color for cond, color in CONDITION_COLORS.items() if cond in key_evokeds})

            # --- Find Peaks and Plot Topomaps ---
            peak_times = {}
            for cond_name, evoked in key_evokeds.items():
                try:
                    roi_evoked = evoked.copy().pick(N1_ELECTRODES_BILATERAL)
                    mean_data = roi_evoked.data.mean(axis=0, keepdims=True)
                    mean_info = mne.create_info(ch_names=['mean_roi'], sfreq=evoked.info['sfreq'], ch_types='eeg')
                    mean_roi_evoked = mne.EvokedArray(mean_data, mean_info, tmin=evoked.tmin)
                    _, peak_time, _ = mean_roi_evoked.get_peak(tmin=PEAK_TMIN, tmax=PEAK_TMAX, mode='neg', return_amplitude=True)
                    peak_times[cond_name] = peak_time
                except ValueError:
                    peak_times[cond_name] = None
                    print(f"    - No negative peak found for '{cond_name}' in subject {subject_id}. Skipping annotation.")

            for i, (cond_name, evoked) in enumerate(key_evokeds.items()):
                ax_topo = fig.add_subplot(gs[1, i])
                peak_time = peak_times.get(cond_name)
                
                if peak_time is not None:
                    ax_erp.axvline(x=peak_time, color=CONDITION_COLORS.get(cond_name, 'k'), linestyle='--', linewidth=1.5, alpha=0.8)
                    scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
                    scalp_evoked.plot_topomap(times=peak_time, axes=ax_topo, show=False, vlim=(-6, 6), colorbar=False)
                    ax_topo.set_title(f"{cond_name}\nPeak at {int(peak_time*1000)} ms", color=CONDITION_COLORS.get(cond_name, 'black'))
                else:
                    ax_topo.set_title(f"{cond_name}\n(No peak found)")
                    ax_topo.axis('off')


            fig.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
            cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.2])
            plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax, label='µV')
            
            fig_path = os.path.join(subject_figure_dir, f'sub-{subject_id}_{script_name}.png')
            if os.path.exists(fig_path): os.remove(fig_path)
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

    print("\n--- Generating group-level grand average N1 contrast plot (All Trials) ---")

    fig_grp = plt.figure(figsize=(12, 8))
    fig_grp.suptitle('Grand Average: N1 Contrast - Decreasing -2 (ALL)', fontsize=16)
    gs_grp = gridspec.GridSpec(2, len(grand_averages_key), height_ratios=[2, 1.5])
    ax_erp_grp = fig_grp.add_subplot(gs_grp[0, :])

    mne.viz.plot_compare_evokeds(
        grand_averages_key, picks=N1_ELECTRODES_BILATERAL, combine='mean', axes=ax_erp_grp,
        title="Grand Average Mean ERP over Bilateral Posterior-Occipital Region", show=False, legend='upper left',
        ci=0.95, colors={cond: color for cond, color in CONDITION_COLORS.items() if cond in grand_averages_key}
    )
    
    # --- Find N1 peaks for each condition for topomaps ---
    peak_times_grp = {}
    for cond_name, evoked in grand_averages_key.items():
        try:
            roi_evoked = evoked.copy().pick(N1_ELECTRODES_BILATERAL)
            mean_data = roi_evoked.data.mean(axis=0, keepdims=True)
            mean_info = mne.create_info(ch_names=['mean_roi'], sfreq=evoked.info['sfreq'], ch_types='eeg')
            mean_roi_evoked = mne.EvokedArray(mean_data, mean_info, tmin=evoked.tmin)
            _, peak_time, _ = mean_roi_evoked.get_peak(tmin=PEAK_TMIN, tmax=PEAK_TMAX, mode='neg', return_amplitude=True)
            peak_times_grp[cond_name] = peak_time
        except ValueError:
            peak_times_grp[cond_name] = None
            print(f"    - No group-level negative peak found for '{cond_name}'. Skipping annotation.")

    for i, (cond_name, evoked) in enumerate(grand_averages_key.items()):
        ax_topo_grp = fig_grp.add_subplot(gs_grp[1, i])
        peak_time = peak_times_grp.get(cond_name)
        
        if peak_time is not None:
            ax_erp_grp.axvline(x=peak_time, color=CONDITION_COLORS.get(cond_name, 'k'), linestyle='--', linewidth=1.5, alpha=0.8)
            scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
            scalp_evoked.plot_topomap(times=peak_time, axes=ax_topo_grp, show=False, vlim=(-6, 6), colorbar=False)
            ax_topo_grp.set_title(f"{cond_name}\nPeak at {int(peak_time*1000)} ms", color=CONDITION_COLORS.get(cond_name, 'black'))
        else:
            ax_topo_grp.set_title(f"{cond_name}\n(No peak found)")
            ax_topo_grp.axis('off')

    fig_grp.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
    cbar_ax_grp = fig_grp.add_axes([0.88, 0.15, 0.02, 0.2])
    plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax_grp, label='µV')
    
    grp_fig_path = os.path.join(group_figure_dir, f'group_{script_name}.png')
    if os.path.exists(grp_fig_path): os.remove(grp_fig_path)
    fig_grp.savefig(grp_fig_path, bbox_inches='tight'); plt.close(fig_grp)
    print(f"  - Saved grand average N1 plot to {grp_fig_path}")

    print("\n--- N1 contrast plot generation complete. ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate EEG N1 contrast plots for decreasing minus 2 (all trials).')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process. If not provided, all subjects will be processed.')
    args = parser.parse_args()
    generate_n1_contrast_plots(args.subjects) 