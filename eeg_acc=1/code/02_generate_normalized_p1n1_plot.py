import mne
import os
import glob
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION ---
KEY_CONDITIONS_MAP = {
    "Landing on 1": ["21", "31", "41"],
    "Landing on 2": ["32", "42", "52"],
    "Landing on 3": ["43", "53", "63"],
}

BASE_CONDITIONS = [cond for sublist in KEY_CONDITIONS_MAP.values() for cond in sublist]

# Define colors for plots
CONDITION_COLORS = {
    "Landing on 1": '#1f77b4',  # Muted Blue
    "Landing on 2": '#ff7f0e',  # Safety Orange
    "Landing on 3": '#2ca02c',  # Cooked Asparagus Green
}

# --- ROIs and Time Windows ---
P1_ROI = ['E71', 'E75', 'E76', 'E70', 'E83', 'E74', 'E81', 'E82']
P1_TMIN, P1_TMAX = 0.080, 0.130

N1_ROI_L = ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70']
N1_ROI_R = ['E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83']
N1_ROI = N1_ROI_L + N1_ROI_R
N1_TMIN, N1_TMAX = 0.150, 0.200

# Plotting time range
PLOT_TMIN, PLOT_TMAX = -0.1, 0.4

def generate_normalized_plot(subjects_to_process):
    """
    Generates a grand-average plot of P1-N1 normalized ERP waveforms.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    output_dir = os.path.join(derivatives_dir, '02_p1n1_normalized_plot')
    os.makedirs(output_dir, exist_ok=True)

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Generating P1-N1 Normalized Plot for subjects: {subjects_to_process} ---")

    all_normalized_evokeds = {cond: [] for cond in KEY_CONDITIONS_MAP.keys()}

    for subject_id in subjects_to_process:
        try:
            subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
            print(f"Processing sub-{subject_id}...")

            base_evokeds = {}
            for cond in BASE_CONDITIONS:
                epoch_file = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif')
                if os.path.exists(epoch_file):
                    base_evokeds[cond] = mne.read_epochs(epoch_file, preload=True, verbose=False).average()
            
            if not base_evokeds:
                print(f"  > No data found for sub-{subject_id}. Skipping.")
                continue

            for key_cond, base_cond_list in KEY_CONDITIONS_MAP.items():
                evokeds_to_combine = [base_evokeds[bc] for bc in base_cond_list if bc in base_evokeds]
                if not evokeds_to_combine:
                    continue

                evoked = mne.combine_evoked(evokeds_to_combine, 'equal')
                
                # --- Normalization ---
                # 1. Get P1 and N1 peak amplitudes from their respective ROIs
                _, _, p1_amp = evoked.copy().pick(P1_ROI).get_peak(tmin=P1_TMIN, tmax=P1_TMAX, mode='pos', return_amplitude=True)
                _, _, n1_amp = evoked.copy().pick(N1_ROI).get_peak(tmin=N1_TMIN, tmax=N1_TMAX, mode='neg', return_amplitude=True)
                
                # 2. Apply linear transformation
                amplitude_range = p1_amp - n1_amp
                print(f"  > {key_cond}: P1 Amp={p1_amp:.6f}, N1 Amp={n1_amp:.6f}, Range={amplitude_range:.6f}")
                if np.isclose(amplitude_range, 0):
                    print(f"  > P1-N1 amplitude range is zero for {key_cond}. Skipping normalization.")
                    continue
                
                # Create a new evoked object representing the MEAN of the ROI
                roi_evoked_mean = evoked.copy().pick(N1_ROI)
                roi_evoked_mean.comment = key_cond
                # Manually average the data across channels
                roi_data_mean = roi_evoked_mean.data.mean(axis=0, keepdims=True)
                
                # Apply normalization to the single averaged waveform
                normalized_data = -1 + 2 * (roi_data_mean - n1_amp) / amplitude_range

                # Create a new info object for our single virtual channel
                info = mne.create_info(ch_names=['normalized_roi_mean'], sfreq=evoked.info['sfreq'], ch_types=['eeg'])
                
                # Create the final EvokedArray object to be plotted
                normalized_evoked = mne.EvokedArray(normalized_data, info, tmin=evoked.tmin, comment=key_cond)

                all_normalized_evokeds[key_cond].append(normalized_evoked)

        except Exception as e:
            print(f"--- FAILED to process Subject {subject_id}. Error: {e} ---")

    # --- Create Group-Level Plot ---
    grand_averages = {
        cond: mne.grand_average(evoked_list) 
        for cond, evoked_list in all_normalized_evokeds.items() if evoked_list
    }

    if not grand_averages:
        print("\n--- No data available to generate a group plot. ---")
        return

    print("\n--- Generating group-level normalized plot ---")
    
    fig, ax = plt.subplots(figsize=(12, 8))

    for cond_name, evoked in grand_averages.items():
        ax.plot(
            evoked.times, 
            evoked.data.T, 
            label=cond_name, 
            color=CONDITION_COLORS.get(cond_name)
        )

    ax.set_title('Grand Average P1-N1 Normalized Waveforms (Bilateral N1 ROI)')
    ax.set_xlim([PLOT_TMIN, PLOT_TMAX])
    ax.set_ylim([-1.2, 1.2])
    ax.axhline(0, linestyle='--', color='grey', linewidth=0.8)
    ax.axhline(1, linestyle='--', color='grey', linewidth=0.8)
    ax.set_ylabel("Normalized Amplitude (a.u.)")
    ax.set_xlabel("Time (s)")
    ax.legend(loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    fig_path = os.path.join(output_dir, '02_grand_average_p1n1_normalized_plot.png')
    if os.path.exists(fig_path):
        os.remove(fig_path)
    fig.savefig(fig_path, bbox_inches='tight')
    plt.close(fig)

    print(f"\n--- Plot saved to: {fig_path} ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a grand-average plot of P1-N1 normalized ERPs.')
    parser.add_argument('--subjects', nargs='*', default=[], help='Specific subject ID(s) to process. If not provided, all subjects will be processed.')
    args = parser.parse_args()
    generate_normalized_plot(args.subjects) 