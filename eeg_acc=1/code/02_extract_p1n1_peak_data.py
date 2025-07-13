import mne
import os
import glob
import argparse
import pandas as pd
import numpy as np

# --- 1. CONFIGURATION ---
# Conditions to load, corresponding to the "Landing on" groups
BASE_CONDITIONS = ['21', '31', '41', '32', '42', '52', '43', '53', '63']

KEY_CONDITIONS_MAP = {
    "Landing on 1": ["21", "31", "41"],
    "Landing on 2": ["32", "42", "52"],
    "Landing on 3": ["43", "53", "63"],
}

# --- ROIs and Time Windows ---
# P1 Component
P1_ROI = ['E71', 'E75', 'E76', 'E70', 'E83', 'E74', 'E81', 'E82']
P1_TMIN, P1_TMAX = 0.080, 0.130 # 80-130ms

# N1 Component
N1_ROI_L = ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70']
N1_ROI_R = ['E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83']
N1_ROI = N1_ROI_L + N1_ROI_R
N1_TMIN, N1_TMAX = 0.150, 0.200 # 150-200ms

def extract_p1n1_peak_data(subjects_to_process):
    """
    Extracts P1 and N1 peak amplitude and latency for specified conditions.

    This script loops through each subject, combines base EEG conditions into
    key "Landing on" conditions, and then for each of these, it identifies the
    P1 and N1 peaks within predefined time windows and regions of interest (ROIs).
    The resulting metrics, including peak-to-peak differences, are saved to a
    single CSV file for further analysis.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    output_dir = os.path.join(derivatives_dir, '02_p1n1_peak_analysis')
    os.makedirs(output_dir, exist_ok=True)
    
    results = []

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Starting P1/N1 Peak Extraction for subjects: {subjects_to_process} ---")

    # --- 4. Main Processing Loop ---
    for subject_id in subjects_to_process:
        try:
            subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
            print(f"Processing sub-{subject_id}...")

            # Load evoked for base conditions from epoch files
            base_evokeds = {}
            for cond in BASE_CONDITIONS:
                epoch_file = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif')
                if os.path.exists(epoch_file):
                    base_evokeds[cond] = mne.read_epochs(epoch_file, preload=True, verbose=False).average()

            if not base_evokeds:
                print(f"  > Warning: No base condition files found for sub-{subject_id}. Skipping.")
                continue

            # Combine base evokeds into key conditions
            key_evokeds = {}
            for key_cond, base_cond_list in KEY_CONDITIONS_MAP.items():
                evokeds_to_combine = [base_evokeds[bc] for bc in base_cond_list if bc in base_evokeds]
                if evokeds_to_combine:
                    key_evokeds[key_cond] = mne.combine_evoked(evokeds_to_combine, 'equal')

            if not key_evokeds:
                print(f"  > Warning: Not enough data for key conditions for sub-{subject_id}. Skipping.")
                continue

            # Process each key condition
            for condition_name, evoked in key_evokeds.items():
                # Find P1 peak (positive) in the Oz ROI
                _, p1_lat, p1_amp = evoked.copy().pick(P1_ROI).get_peak(
                    tmin=P1_TMIN, tmax=P1_TMAX, mode='pos', return_amplitude=True
                )

                # Find N1 peak (negative) in the Bilateral N1 ROI
                _, n1_lat, n1_amp = evoked.copy().pick(N1_ROI).get_peak(
                    tmin=N1_TMIN, tmax=N1_TMAX, mode='neg', return_amplitude=True
                )

                # --- 5. Calculate Peak-to-Peak Metrics ---
                p2p_amp = p1_amp - n1_amp
                p2p_lat = n1_lat - p1_lat

                # Store results
                results.append({
                    'subject_id': subject_id,
                    'condition': condition_name,
                    'p1_lat': p1_lat,
                    'p1_amp': p1_amp,
                    'n1_lat': n1_lat,
                    'n1_amp': n1_amp,
                    'p2p_lat': p2p_lat,
                    'p2p_amp': p2p_amp,
                })
            print(f"    - Successfully extracted peaks for sub-{subject_id}.")

        except Exception as e:
            print(f"--- FAILED to process Subject {subject_id}. Error: {e} ---")
    
    if not results:
        print("\n--- No results were generated. CSV file will not be created. ---")
        return

    # --- Save results to CSV ---
    results_df = pd.DataFrame(results)
    output_path = os.path.join(output_dir, 'p1_n1_peak_analysis_results.csv')
    results_df.to_csv(output_path, index=False, float_format='%.6f')

    print(f"\n--- Extraction complete. Results saved to: {output_path} ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract P1 and N1 peak data from EEG derivatives.')
    parser.add_argument('--subjects', nargs='*', default=[], help='Specific subject ID(s) to process. If not provided, all subjects will be processed.')
    args = parser.parse_args()
    extract_p1n1_peak_data(args.subjects) 