import os
import glob
import argparse
import mne
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Configuration ---

# Base conditions to load, limited to small-to-small transitions
BASE_CONDITIONS = ['21', '31', '12', '32', '13', '23']

# How to combine base conditions into key conditions
KEY_CONDITIONS_MAP = {
    "Landing on 1": ["21", "31"],
    "Landing on 2": ["12", "32"],
    "Landing on 3": ["13", "23"]
}

# Define the two distinct ROIs for this analysis
P1_ROI_OZ = ['E71', 'E75', 'E76', 'E70', 'E83', 'E74', 'E81', 'E82']
N1_ROI_POT_L = ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70']
N1_ROI_POT_R = ['E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83']
N1_ROI_POT_BILATERAL = N1_ROI_POT_L + N1_ROI_POT_R

# Time windows for peak detection
P1_TMIN, P1_TMAX = 0.080, 0.130
N1_TMIN, N1_TMAX = 0.150, 0.200

# Colors for plotting
CONDITION_COLORS = {
    "Landing on 1": '#377eb8',  # Blue
    "Landing on 2": '#4daf4a',  # Green
    "Landing on 3": '#e41a1c',  # Red
}

# --- 2. Main Visualization Function ---

def visualize_flattened_n1(subjects_to_process=None):
    """
    Generates a plot showing N1 waveforms before and after "flattening"
    based on the preceding P1 amplitude.
    """
    # Setup paths
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    except NameError:
        base_dir = os.path.abspath('eeg_acc=1')
        
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    script_name = os.path.basename(__file__).replace('.py', '')
    output_dir = os.path.join(derivatives_dir, 'group', 'figures', script_name)
    os.makedirs(output_dir, exist_ok=True)

    # Get subjects if not specified
    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Starting Analysis 3: 'Flattening' Visualization ---")

    # --- 1. Load data and calculate grand averages ---
    all_subject_evokeds = {cond: [] for cond in BASE_CONDITIONS}
    for subject_id in subjects_to_process:
        for bc in BASE_CONDITIONS:
            fpath = os.path.join(derivatives_dir, f'sub-{subject_id}', f'sub-{subject_id}_task-numbers_cond-{bc}_epo.fif')
            if os.path.exists(fpath):
                all_subject_evokeds[bc].append(mne.read_epochs(fpath, preload=True, verbose=False).average())
    
    grand_averages_base = {cond: mne.grand_average(evoked_list) for cond, evoked_list in all_subject_evokeds.items() if evoked_list}
    grand_averages_key = {key: mne.combine_evoked([grand_averages_base[bc] for bc in bclist if bc in grand_averages_base], 'equal') for key, bclist in KEY_CONDITIONS_MAP.items()}

    # --- 2. Find the "Shift" Value ---
    # To get a single, stable P1 peak time, we average all key conditions together
    combined_ga = mne.grand_average(list(grand_averages_key.values()))
    _, p1_peak_time, _ = combined_ga.copy().pick(P1_ROI_OZ).get_peak(tmin=P1_TMIN, tmax=P1_TMAX, mode='pos', return_amplitude=True)
    print(f"Using a single P1 peak time for normalization: {p1_peak_time*1000:.0f} ms")

    # --- 3. Prepare data for plotting ---
    plot_data = {}
    times_array = grand_averages_key["Landing on 1"].times

    # Find the sample index closest to the P1 peak time for robust lookup
    p1_peak_sample_idx = np.argmin(np.abs(times_array - p1_peak_time))

    for cond_name, evoked in grand_averages_key.items():
        # Get the N1 waveform from the POT ROI
        pot_waveform = evoked.copy().pick(N1_ROI_POT_BILATERAL).data.mean(axis=0)
        
        # Get the amplitude at the P1 peak sample index. This is the "shift" value.
        shift_value = pot_waveform[p1_peak_sample_idx]
        
        # Create the "flattened" waveform
        flattened_waveform = pot_waveform - shift_value
        
        plot_data[cond_name] = {
            'original': pot_waveform,
            'flattened': flattened_waveform,
            'shift': shift_value
        }

    # --- 4. Create the Plot ---
    print("--- Generating plot ---")
    times = grand_averages_key["Landing on 1"].times * 1000  # in ms
    fig, ax = plt.subplots(figsize=(10, 7))

    for cond_name, data in plot_data.items():
        color = CONDITION_COLORS[cond_name]
        # Plot original waveform (dashed)
        ax.plot(times, data['original'] * 1e6, color=color, linestyle='--', alpha=0.8, label=f"{cond_name} (Original)")
        # Plot flattened waveform (solid)
        ax.plot(times, data['flattened'] * 1e6, color=color, linestyle='-', linewidth=2.5, label=f"{cond_name} (P1-Normalized)")

    ax.axvline(x=p1_peak_time * 1000, color='grey', linestyle=':', label=f'P1 Norm. Time ({p1_peak_time*1000:.0f} ms)')
    ax.set_title('N1 Waveforms Before and After P1-Based Normalization', fontsize=16)
    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_ylabel('Amplitude (μV)', fontsize=12)
    ax.legend(loc='lower left')
    ax.grid(True, linestyle=':', alpha=0.6)
    # ax.invert_yaxis() # Removed to restore standard (positive-up) orientation
    ax.set_xlim(-100, 300)

    # --- Save the plot ---
    plot_path = os.path.join(output_dir, 'group_flattened_n1_plot.png')
    fig.savefig(plot_path, bbox_inches='tight')
    plt.close(fig)

    print(f"--- Plot saved to: {plot_path} ---")
    print("\n--- Analysis 3 Complete ---")


# --- 3. Script Execution ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate 'flattened' N1 visualization.")
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process.')
    args = parser.parse_args()
    
    visualize_flattened_n1(args.subjects) 