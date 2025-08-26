import mne
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from utils import (
    load_config, get_subject_list, save_figure, 
    ELECTRODE_GROUPS, CONDITION_COLORS, NON_SCALP_CHANNELS, ELECTRODE_LOC_FILE
)

def main(config_path, accuracy):
    """
    Main function to generate plots based on a configuration file.
    """
    # --- Step 1: Load Configuration and Set Up Paths ---
    config = load_config(config_path)
    if not config:
        return

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    source_dir_name = "eeg_acc=1" if accuracy == 'correct' else "eeg_all"
    derivatives_dir = os.path.join(base_dir, source_dir_name, 'derivatives')
    # Updated output_dir to save directly in the 'figures' folder
    output_dir = os.path.join(base_dir, 'SFN', 'derivatives', 'group', 'figures')

    # --- Step 2: Load All Subject Data ---
    print(f"--- Loading data from: {source_dir_name} ---")
    base_conditions_to_load = sorted(list(set([item for sublist in config['conditions'].values() for item in sublist])))
    all_subject_evokeds = {cond: [] for cond in base_conditions_to_load}
    
    subject_list = get_subject_list(derivatives_dir)
    for subject_id in subject_list:
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        for cond in base_conditions_to_load:
            file_path = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif')
            if os.path.exists(file_path):
                # We read epochs and average them to create an Evoked object
                evoked = mne.read_epochs(file_path, preload=True, verbose=False).average()
                all_subject_evokeds[cond].append(evoked)

    # --- Step 3: Compute Grand Average and Time Window ---
    print("--- Calculating grand average and analysis window ---")
    grand_averages_base = {cond: mne.grand_average(evoked_list) for cond, evoked_list in all_subject_evokeds.items() if evoked_list}
    if not grand_averages_base:
        print("--- No data found for any condition. Aborting. ---")
        return

    grand_averages_key = {key_cond: mne.combine_evoked([grand_averages_base[bc] for bc in bcl if bc in grand_averages_base], 'equal') for key_cond, bcl in config['conditions'].items()}

    # This must be defined BEFORE the if/else block to be in the correct scope.
    electrode_group_info = ELECTRODE_GROUPS[config['erp_component']][config['electrode_group_for_erp']]
    electrodes_for_erp = electrode_group_info['electrodes']

    # Check for a manual override window in the config
    if 'fixed_analysis_window' in config and config['fixed_analysis_window'] is not None:
        fixed_tmin, fixed_tmax = config['fixed_analysis_window']
        window_type_str = "Fixed"
        filename_suffix = "_fixed_window"
        print(f"--- Using MANUAL analysis window: {int(fixed_tmin*1000)}–{int(fixed_tmax*1000)} ms ---")
    else:
        # Perform automatic peak detection if no manual window is provided
        print("--- Performing automatic peak detection to determine analysis window ---")
        window_type_str = "Detected"
        filename_suffix = "_detected_window"
        tmin_peak, tmax_peak = config['time_window_peak_detection']
        half_width_s = config['time_window_half_width_ms'] / 1000.0
        
        collapsed_evoked = mne.combine_evoked(list(grand_averages_key.values()), 'equal')
        
        # Determine if we are looking for a positive (P) or negative (N) peak
        peak_mode = 'pos' if config['erp_component'].startswith('P') else 'neg'
        
        _, fixed_center = collapsed_evoked.copy().pick(electrodes_for_erp).get_peak(
            tmin=tmin_peak, tmax=tmax_peak, mode=peak_mode, return_amplitude=False
        )
        fixed_tmin = fixed_center - half_width_s
        fixed_tmax = fixed_center + half_width_s
        print(f"  - AUTOMATIC window found: {int(fixed_tmin*1000)}–{int(fixed_tmax*1000)} ms")
    
    # --- Step 4: Generate the Group Plot ---
    print("--- Generating final group plot ---")
    fig_grp = plt.figure(figsize=(14, 8))
    title = f"{config['plot_title']}\n{window_type_str} window: {int(fixed_tmin*1000)}–{int(fixed_tmax*1000)} ms"
    fig_grp.suptitle(title, fontsize=16)
    gs_grp = gridspec.GridSpec(2, len(grand_averages_key), height_ratios=[2, 1.5])
    ax_erp_grp = fig_grp.add_subplot(gs_grp[0, :])

    # Filter the global colors dict to only include colors for conditions in this analysis
    plot_colors = {cond: color for cond, color in CONDITION_COLORS.items() if cond in grand_averages_key}

    mne.viz.plot_compare_evokeds(
        grand_averages_key, picks=electrodes_for_erp, combine='mean', axes=ax_erp_grp,
        title=f"Grand Average Mean ERP over {electrode_group_info['description']}",
        show=False, legend='upper left', ci=0.95, colors=plot_colors
    )
    ax_erp_grp.axvspan(fixed_tmin, fixed_tmax, color='gray', alpha=0.15)

    # Set montage and calculate global color limits for topomaps
    montage = mne.channels.read_custom_montage(ELECTRODE_LOC_FILE)
    for evoked in grand_averages_key.values():
        evoked.set_montage(montage, on_missing='warn')

    all_means = [ev.copy().pick('eeg', exclude=NON_SCALP_CHANNELS).crop(fixed_tmin, fixed_tmax).data.mean(axis=1) for ev in grand_averages_key.values()]
    if all_means:
        global_max = np.max(np.abs(all_means))
        vlim = (-global_max, global_max)
    else:
        vlim = (-1, 1) # Fallback

    # Plot topomaps
    for i, (cond_name, evoked) in enumerate(grand_averages_key.items()):
        ax_topo_grp = fig_grp.add_subplot(gs_grp[1, i])
        
        # Create a temporary Evoked object with ONLY scalp channels
        scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
        
        # Get the info from this scalp-only object
        info_with_montage = scalp_evoked.info
        
        # Calculate the mean ONLY from the scalp channels
        window_mean = scalp_evoked.crop(fixed_tmin, fixed_tmax).data.mean(axis=1)
        
        mne.viz.plot_topomap(
            window_mean, info_with_montage, axes=ax_topo_grp, show=False, vlim=vlim,
            cmap='RdBu_r', contours=6, image_interp='cubic', sensors=False
        )
        ax_topo_grp.set_title(f"{cond_name}\n{int(fixed_tmin*1000)}–{int(fixed_tmax*1000)} ms", color=plot_colors.get(cond_name, 'black'))

    # Add colorbar
    fig_grp.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4, wspace=0.4)
    cbar_ax_grp = fig_grp.add_axes([0.88, 0.15, 0.02, 0.2])
    norm = plt.Normalize(vmin=vlim[0], vmax=vlim[1])
    sm = plt.cm.ScalarMappable(cmap='RdBu_r', norm=norm)
    plt.colorbar(sm, cax=cbar_ax_grp, label='µV')

    # --- Step 5: Save the Figure ---
    save_figure(fig_grp, config['analysis_name'] + filename_suffix, output_dir)
    print("\n--- Plot generation complete. ---")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate EEG plots based on a configuration file.')
    parser.add_argument('--config', type=str, required=True, help='Path to the YAML configuration file.')
    parser.add_argument('--accuracy', type=str, required=True, choices=['correct', 'all'], help="Specify the dataset to use ('correct' for acc=1, 'all' for all trials).")
    args = parser.parse_args()
    main(args.config, args.accuracy)
