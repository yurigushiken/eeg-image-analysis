import mne
import os
import glob
import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# --- 1. CONFIGURATION ---
# Base conditions to load from the processed files
BASE_CONDITIONS = ["iSS", "dSS", "iLL", "dLL", "NoChg"]

# How to combine base conditions into key conditions for the plot
KEY_CONDITIONS_MAP = {
    "Small-Change": ["iSS", "dSS"],
    "Large-Change": ["iLL", "dLL"],
    "No-Change": ["NoChg"],
}

# Define colors for plots and text
CONDITION_COLORS = {"Small-Change": "blue", "Large-Change": "red", "No-Change": "grey"}

# Electrodes of interest for P3b waveform (Pz and surrounding region)
P3B_ELECTRODES = ['E62', 'E78', 'E77', 'E72', 'E67', 'E61', 'E54', 'E55', 'E79']

# Time of interest for topomap (peak of P3b)
TOPO_TIME = 0.485  # 485 ms

# Standard list of non-scalp channels to exclude for better topomap interpolation
NON_SCALP_CHANNELS = [
    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E43', 'E44', 'E48', 
    'E49', 'E113', 'E114', 'E119', 'E120', 'E121', 'E125', 'E126', 'E127', 'E128'
]

def generate_p3b_plots(subjects_to_process):
    """
    Generates combined ERP waveform and topomap plots for P3b analysis for
    specified subjects and the group average.
    """
    # Dynamically find the project root and derivatives directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    
    # Dictionary to hold evoked data for all subjects for group analysis
    all_subject_evokeds = {cond: [] for cond in BASE_CONDITIONS}

    # If no subjects are specified, process all available subjects
    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects for P3b plots: {subjects_to_process} ---")

    # --- Individual Subject Plots ---
    for subject_id in subjects_to_process:
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        subject_figure_dir = os.path.join(subject_dir, 'figures')
        os.makedirs(subject_figure_dir, exist_ok=True)
        
        print(f"\nProcessing Subject {subject_id}...")
        
        try:
            # Load all necessary base evokeds for this subject
            base_evokeds = {}
            for cond in BASE_CONDITIONS:
                epo_file = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif')
                if os.path.exists(epo_file):
                    epochs = mne.read_epochs(epo_file, preload=True, verbose=False)
                    evoked = epochs.average()
                    base_evokeds[cond] = evoked
                    all_subject_evokeds[cond].append(evoked) # Add to list for group plot

            if not base_evokeds:
                print(f"  - No data found for Subject {subject_id}. Skipping.")
                continue

            # Combine base evokeds into the key conditions (Small-Change, etc.)
            key_evokeds = {}
            for key_cond, base_cond_list in KEY_CONDITIONS_MAP.items():
                evokeds_to_combine = [base_evokeds[bc] for bc in base_cond_list if bc in base_evokeds]
                if evokeds_to_combine:
                    key_evokeds[key_cond] = mne.combine_evoked(evokeds_to_combine, weights='equal')

            if not key_evokeds:
                print(f"  - Not enough data to create key conditions for Subject {subject_id}. Skipping.")
                continue
            
            # --- Create the plot for the individual subject ---
            fig = plt.figure(figsize=(12, 8))
            fig.suptitle(f'Subject {subject_id}: P3b Analysis', fontsize=16)
            # Create a grid for the waveform plot (top) and topomaps (bottom)
            gs = gridspec.GridSpec(2, len(key_evokeds), height_ratios=[2, 1.5])
            
            ax_erp = fig.add_subplot(gs[0, :])
            mne.viz.plot_compare_evokeds(
                key_evokeds, picks=P3B_ELECTRODES, axes=ax_erp,
                combine='mean',  # THIS IS THE FIX: Calculate mean, not GFP
                title="Mean ERP over P3b Region", show=False, legend='upper left',
                ci=False, # No confidence interval for single subject
                colors=CONDITION_COLORS
            )
            # Manually add vline and text to control position
            ax_erp.axvline(x=TOPO_TIME, color='k', linestyle='--', linewidth=1)
            ax_erp.text(x=TOPO_TIME, y=ax_erp.get_ylim()[1], s=f' {str(TOPO_TIME)}',
                        va='bottom', ha='left')

            # Create the topomaps on the bottom row
            for i, (cond_name, evoked) in enumerate(key_evokeds.items()):
                ax_topo = fig.add_subplot(gs[1, i])
                scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
                scalp_evoked.plot_topomap(
                    times=TOPO_TIME, axes=ax_topo, show=False,
                    vlim=(-6, 6), colorbar=False
                )
                ax_topo.set_title(
                    f"{cond_name}\n{int(TOPO_TIME*1000)} ms",
                    color=CONDITION_COLORS.get(cond_name, 'black')
                )

            # Add a single, shared colorbar for all topomaps
            fig.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
            cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.2])
            sm = plt.cm.ScalarMappable(cmap='RdBu_r', norm=plt.Normalize(vmin=-6, vmax=6))
            cbar = fig.colorbar(sm, cax=cbar_ax, label='µV')

            # Save the figure
            fig_path = os.path.join(subject_figure_dir, f'sub-{subject_id}_p3b_plot.png')
            fig.savefig(fig_path, bbox_inches='tight')
            plt.close(fig)
            print(f"    - Saved P3b plot to {fig_path}")

        except Exception as e:
            print(f"--- FAILED to generate P3b plot for Subject {subject_id}. Error: {e} ---")

    # --- Group-Level Plot ---
    group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures')
    os.makedirs(group_figure_dir, exist_ok=True)
    
    # Calculate grand averages for base conditions first
    grand_averages_base = { cond: mne.grand_average(evoked_list) 
                            for cond, evoked_list in all_subject_evokeds.items() if evoked_list }

    if not grand_averages_base:
        print("\n--- No data available for any subject. Skipping group plot. ---")
        return

    # Combine grand averages into key conditions
    grand_averages_key = {}
    for key_cond, base_cond_list in KEY_CONDITIONS_MAP.items():
        evokeds_to_combine = [grand_averages_base[bc] for bc in base_cond_list if bc in grand_averages_base]
        if evokeds_to_combine:
            grand_averages_key[key_cond] = mne.combine_evoked(evokeds_to_combine, weights='equal')
    
    if not grand_averages_key:
        print("\n--- Not enough data to create group-level key conditions. Skipping group plot. ---")
        return

    print("\n--- Generating group-level grand average P3b plot ---")
    
    fig_grp = plt.figure(figsize=(12, 8))
    fig_grp.suptitle('Grand Average: P3b Analysis', fontsize=16)
    gs_grp = gridspec.GridSpec(2, len(grand_averages_key), height_ratios=[2, 1.5])

    ax_erp_grp = fig_grp.add_subplot(gs_grp[0, :])
    mne.viz.plot_compare_evokeds(
        grand_averages_key, picks=P3B_ELECTRODES, axes=ax_erp_grp,
        combine='mean',  # THIS IS THE FIX: Calculate mean, not GFP
        title="Grand Average Mean ERP over P3b Region", show=False, legend='upper left',
        ci=True, # Show confidence interval for group plot
        colors=CONDITION_COLORS
    )
    # Manually add vline and text to control position
    ax_erp_grp.axvline(x=TOPO_TIME, color='k', linestyle='--', linewidth=1)
    ax_erp_grp.text(x=TOPO_TIME, y=ax_erp_grp.get_ylim()[1], s=f' {str(TOPO_TIME)}',
                    va='bottom', ha='left')

    for i, (cond_name, evoked) in enumerate(grand_averages_key.items()):
        ax_topo_grp = fig_grp.add_subplot(gs_grp[1, i])
        scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
        scalp_evoked.plot_topomap(
            times=TOPO_TIME, axes=ax_topo_grp, show=False,
            vlim=(-6, 6), colorbar=False # Use a consistent range for grand average
        )
        ax_topo_grp.set_title(
            f"{cond_name}\n{int(TOPO_TIME*1000)} ms",
            color=CONDITION_COLORS.get(cond_name, 'black')
        )

    fig_grp.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
    cbar_ax_grp = fig_grp.add_axes([0.88, 0.15, 0.02, 0.2])
    sm_grp = plt.cm.ScalarMappable(cmap='RdBu_r', norm=plt.Normalize(vmin=-6, vmax=6))
    cbar_grp = fig_grp.colorbar(sm_grp, cax=cbar_ax_grp, label='µV')

    fig_path_grp = os.path.join(group_figure_dir, 'group_p3b_plot.png')
    fig_grp.savefig(fig_path_grp, bbox_inches='tight')
    plt.close(fig_grp)
    print(f"  - Saved grand average P3b plot to {fig_path_grp}")

    print("\n--- P3b plot generation complete. ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate EEG P3b waveform and topomap plots.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process (e.g., 02 03). If not provided, all subjects will be processed.')
    args = parser.parse_args()
    generate_p3b_plots(args.subjects) 