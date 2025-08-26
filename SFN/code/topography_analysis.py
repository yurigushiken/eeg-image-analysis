# SFN/code/topography_analysis.py

import argparse
import yaml
import mne
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import itertools

from utils import get_subject_list, NON_SCALP_CHANNELS, ELECTRODE_LOC_FILE

def load_source_config(config_path):
    """Loads the source YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)[0]

def find_top_electrodes(evoked, time_window, n_electrodes, component_type):
    """Finds the N electrodes with the highest mean amplitude in a given time window."""
    evoked_copy = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
    evoked_copy.crop(tmin=time_window[0], tmax=time_window[1])
    mean_amplitudes = evoked_copy.data.mean(axis=1)
    
    sort_order = np.argsort(mean_amplitudes)
    if component_type != "N1":
        sort_order = sort_order[::-1]
        
    top_indices = sort_order[:n_electrodes]
    return [evoked_copy.ch_names[i] for i in top_indices]

def run_topography_analysis(config_path, accuracy):
    """Main function to run the flexible topography analysis."""
    # --- 1. Load Configuration ---
    print(f"--- Loading topography config from: {config_path} ---")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)[0]
    
    base_dir = Path(__file__).resolve().parent.parent.parent
    source_config = load_source_config(base_dir / config['source_config_file'])
    
    # --- 2. Setup Output Directory & Filenames based on accuracy ---
    analysis_name = config['analysis_name']
    
    if accuracy == 'acc1':
        source_dir_name = "eeg_acc=1"
        accuracy_suffix = "_acc1"
        accuracy_title_str = "(ACC=1)"
    else: # accuracy == 'all'
        source_dir_name = "eeg_all"
        accuracy_suffix = "_all"
        accuracy_title_str = "(ALL)"

    analysis_name_with_suffix = analysis_name + accuracy_suffix
    output_dir = base_dir / 'SFN' / 'derivatives' / 'topography_analysis' / analysis_name_with_suffix
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"{analysis_name_with_suffix}_report.txt"
    summary_plot_path = output_dir / f"{analysis_name_with_suffix}_summary.png"
    print(f"--- Outputs will be saved to: {output_dir} ---")

    # --- 3. Load Data ---
    derivatives_dir = base_dir / source_dir_name / 'derivatives'
    print(f"--- Loading data from: {source_dir_name} ---")

    conditions_flat = set(item for sublist in source_config['conditions'].values() for item in sublist)
    evokeds_data = {cond: [] for cond in conditions_flat}
    
    for subject_id in get_subject_list(str(derivatives_dir)):
        for cond in conditions_flat:
            fpath = derivatives_dir / f'sub-{subject_id}' / f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'
            if fpath.exists():
                evokeds_data[cond].append(mne.read_epochs(fpath, preload=True, verbose=False).average())

    # --- 4. Compute Grand Averages ---
    grand_avg_base = {cond: mne.grand_average(ev_list) for cond, ev_list in evokeds_data.items() if ev_list}
    grand_avg_key = {k: mne.combine_evoked([grand_avg_base[bc] for bc in bcl if bc in grand_avg_base], 'equal') 
                     for k, bcl in source_config['conditions'].items()}

    # --- 5. Perform Analysis ---
    report_lines = [f"Topographical Analysis Report: {analysis_name} {accuracy_title_str}\n" + "="*50]
    electrode_sets = {}
    montage = mne.channels.read_custom_montage(ELECTRODE_LOC_FILE)

    conditions_to_compare = config['conditions_to_compare']
    for cond_name in conditions_to_compare:
        if cond_name not in grand_avg_key:
            print(f"Warning: '{cond_name}' not found. Skipping.")
            continue
        evoked = grand_avg_key[cond_name]
        evoked.set_montage(montage, on_missing='warn')
        
        top_electrodes = find_top_electrodes(evoked, config['time_window'], config['n_top_electrodes'], config['erp_component'])
        electrode_sets[cond_name] = set(top_electrodes)
        
        report_lines.append(f"\nTop {config['n_top_electrodes']} electrodes for '{cond_name}':\n" + ", ".join(top_electrodes))

    # --- 6. Generate Pairwise Overlap Matrix ---
    report_lines.append("\n\nPairwise Overlap Matrix (# of overlapping electrodes):")
    header = f"{'':<18}" + "".join([f"{name:<18}" for name in conditions_to_compare])
    report_lines.append(header)
    for cond1 in conditions_to_compare:
        row_str = f"{cond1:<18}"
        for cond2 in conditions_to_compare:
            if cond1 == cond2:
                overlap_str = "-"
            else:
                overlap = len(electrode_sets.get(cond1, set()).intersection(electrode_sets.get(cond2, set())))
                overlap_str = str(overlap)
            row_str += f"{overlap_str:<18}"
        report_lines.append(row_str)

    # --- 7. Generate Summary Plot ---
    fig, axes = plt.subplots(1, len(conditions_to_compare), figsize=(5 * len(conditions_to_compare), 5), squeeze=False)
    fig.suptitle(f"Topographical Comparison for {analysis_name}\n{accuracy_title_str}", fontsize=16)
    
    for i, cond_name in enumerate(conditions_to_compare):
        ax = axes[0, i]
        evoked = grand_avg_key.get(cond_name)
        if not evoked: continue

        top_electrodes = electrode_sets.get(cond_name, set())
        mask = np.array([ch in top_electrodes for ch in evoked.ch_names])
        
        evoked_for_plot = evoked.copy().crop(tmin=config['time_window'][0], tmax=config['time_window'][1])
        data_for_plot = evoked_for_plot.data.mean(axis=1)

        mne.viz.plot_topomap(data_for_plot, evoked.info, axes=ax, show=False, cmap='RdBu_r', contours=6,
                             mask=mask, mask_params=dict(marker='o', markerfacecolor='w', markeredgecolor='k', linewidth=0, markersize=4))
        ax.set_title(f"{cond_name}\n{config['time_window'][0]*1000:.0f}-{config['time_window'][1]*1000:.0f} ms")

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(summary_plot_path)
    plt.close(fig)
    print(f"--- Saved summary plot to: {summary_plot_path} ---")

    # --- 8. Write Report ---
    with open(report_path, 'w') as f:
        f.write("\n".join(report_lines))
    print(f"--- Saved analysis report to: {report_path} ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform flexible topographic analysis of ERP data.")
    parser.add_argument('--config', type=str, required=True, help='Path to the topography analysis YAML config.')
    parser.add_argument('--accuracy', type=str, required=True, choices=['acc1', 'all'], help="Dataset to use ('acc1' for correct, 'all' for all trials).")
    args = parser.parse_args()
    run_topography_analysis(args.config, args.accuracy)
