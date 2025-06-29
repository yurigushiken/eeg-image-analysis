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
BASE_CONDITIONS = ["iSS", "dSS", "iLL", "dLL", "NoChg"]

# How to combine base conditions into key conditions
KEY_CONDITIONS_MAP = {
    "Small-Change": ["iSS", "dSS"],
    "Large-Change": ["iLL", "dLL"],
    "No-Change": ["NoChg"],
}

# Define colors for plots
CONDITION_COLORS = {"Small-Change": "blue", "Large-Change": "red", "No-Change": "grey"}

# Electrodes of interest for N1 waveform (Left and Right hemispheres)
N1_ELECTRODES_L = ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70']
N1_ELECTRODES_R = ['E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83']
# Combine into a single bilateral list
N1_ELECTRODES_BILATERAL = N1_ELECTRODES_L + N1_ELECTRODES_R

# Time of interest for topomap (peak of N1)
TOPO_TIME = 0.175  # 175 ms

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
    
    all_subject_evokeds = {cond: [] for cond in BASE_CONDITIONS}

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects for N1 plots: {subjects_to_process} ---")

    # --- Individual Subject Plots ---
    for subject_id in subjects_to_process:
        # ... setup directories ...
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        subject_figure_dir = os.path.join(subject_dir, 'figures')
        os.makedirs(subject_figure_dir, exist_ok=True)
        print(f"\nProcessing Subject {subject_id}...")
        
        try:
            # ... load data and create key evokeds ...
            base_evokeds = {cond: mne.read_epochs(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'), preload=True, verbose=False).average() for cond in BASE_CONDITIONS if os.path.exists(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'))}
            for cond, evoked in base_evokeds.items(): all_subject_evokeds[cond].append(evoked)
            if not base_evokeds: print(f"  - No data found for Subject {subject_id}. Skipping."); continue
            key_evokeds = {key_cond: mne.combine_evoked([base_evokeds[bc] for bc in bcl if bc in base_evokeds], 'equal') for key_cond, bcl in KEY_CONDITIONS_MAP.items() if any(bc in base_evokeds for bc in bcl)}
            if not key_evokeds: print(f"  - Not enough data for key conditions for Subject {subject_id}. Skipping."); continue

            # --- Create the plot ---
            fig = plt.figure(figsize=(12, 8))
            fig.suptitle(f'Subject {subject_id}: N1 Analysis', fontsize=16)
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

            # Manually add vline and text
            ax_erp.axvline(x=TOPO_TIME, color='k', linestyle='--', linewidth=1)
            y_pos = ax_erp.get_ylim()[1] * 0.9 # Position at 90% of plot height
            ax_erp.text(x=TOPO_TIME, y=y_pos, s=f' {str(TOPO_TIME)}', va='bottom', ha='left')

            # Plot Topomaps
            for i, (cond_name, evoked) in enumerate(key_evokeds.items()):
                ax_topo = fig.add_subplot(gs[1, i])
                scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
                scalp_evoked.plot_topomap(times=TOPO_TIME, axes=ax_topo, show=False, vlim=(-6, 6), colorbar=False)
                ax_topo.set_title(f"{cond_name}\n{int(TOPO_TIME*1000)} ms", color=CONDITION_COLORS.get(cond_name, 'black'))
            
            # Shared colorbar
            fig.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
            cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.2])
            plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax, label='µV')

            fig_path = os.path.join(subject_figure_dir, f'sub-{subject_id}_n1_plot.png')
            fig.savefig(fig_path, bbox_inches='tight'); plt.close(fig)
            print(f"    - Saved N1 plot to {fig_path}")

        except Exception as e:
            print(f"--- FAILED to generate N1 plot for Subject {subject_id}. Error: {e} ---")

    # --- Group-Level Plot ---
    group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures')
    os.makedirs(group_figure_dir, exist_ok=True)
    
    grand_averages_base = {cond: mne.grand_average(evoked_list) for cond, evoked_list in all_subject_evokeds.items() if evoked_list}
    if not grand_averages_base: print("\n--- No data for group plot. ---"); return

    grand_averages_key = {key_cond: mne.combine_evoked([grand_averages_base[bc] for bc in bcl if bc in grand_averages_base], 'equal') for key_cond, bcl in KEY_CONDITIONS_MAP.items() if any(bc in grand_averages_base for bc in bcl)}
    if not grand_averages_key: print("\n--- Not enough data for group key conditions. ---"); return

    print("\n--- Generating group-level grand average N1 plot ---")
    fig_grp = plt.figure(figsize=(12, 8))
    fig_grp.suptitle('Grand Average: N1 Analysis', fontsize=16)
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
    
    ax_erp_grp.axvline(x=TOPO_TIME, color='k', linestyle='--', linewidth=1)
    y_pos_grp = ax_erp_grp.get_ylim()[1] * 0.9 # Position at 90% of plot height
    ax_erp_grp.text(x=TOPO_TIME, y=y_pos_grp, s=f' {str(TOPO_TIME)}', va='bottom', ha='left')
    
    for i, (cond_name, evoked) in enumerate(grand_averages_key.items()):
        ax_topo_grp = fig_grp.add_subplot(gs_grp[1, i])
        scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
        scalp_evoked.plot_topomap(times=TOPO_TIME, axes=ax_topo_grp, show=False, vlim=(-6, 6), colorbar=False)
        ax_topo_grp.set_title(f"{cond_name}\n{int(TOPO_TIME*1000)} ms", color=CONDITION_COLORS.get(cond_name, 'black'))

    fig_grp.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
    cbar_ax_grp = fig_grp.add_axes([0.88, 0.15, 0.02, 0.2])
    plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax_grp, label='µV')
    
    fig_path_grp = os.path.join(group_figure_dir, 'group_n1_plot.png')
    fig_grp.savefig(fig_path_grp, bbox_inches='tight'); plt.close(fig_grp)
    print(f"  - Saved grand average N1 plot to {fig_path_grp}")

    print("\n--- N1 plot generation complete. ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate EEG N1 waveform and topomap plots.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process. If not provided, all subjects will be processed.')
    args = parser.parse_args()
    generate_n1_plots(args.subjects) 