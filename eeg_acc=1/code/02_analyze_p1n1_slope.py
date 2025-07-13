import os
import pandas as pd
import numpy as np
import glob
import mne
from statsmodels.stats.anova import AnovaRM
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# --- 1. CONFIGURATION ---
KEY_CONDITIONS_MAP = {
    "Landing on 1": ["21", "31", "41"],
    "Landing on 2": ["32", "42", "52"],
    "Landing on 3": ["43", "53", "63"],
}

BASE_CONDITIONS = [cond for sublist in KEY_CONDITIONS_MAP.values() for cond in sublist]

PARTICIPANT_LIST = [
    "02", "03", "04", "05", "08", "09", "10", "11", "12", "13", "14", "15",
    "17", "21", "22", "23", "25", "26", "27", "28", "29", "31", "32", "33"
]

# --- ROIs and Time Windows for Peak Detection ---
P1_ROI = ['E71', 'E75', 'E76', 'E70', 'E83', 'E74', 'E81', 'E82']
P1_TMIN, P1_TMAX = 0.080, 0.130

N1_ROI_L = ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70']
N1_ROI_R = ['E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83']
N1_ROI = N1_ROI_L + N1_ROI_R
N1_TMIN, N1_TMAX = 0.150, 0.200


def analyze_p1n1_slope():
    """
    Calculates the P1-N1 slope for each subject and condition, runs an
    ANOVA on the results, and generates a bar plot.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    output_dir = os.path.join(derivatives_dir, '02_p1n1_slope_analysis')
    os.makedirs(output_dir, exist_ok=True)

    all_slopes = []

    print(f"--- Starting P1-N1 Slope Analysis for {len(PARTICIPANT_LIST)} subjects ---")

    for subject_id in PARTICIPANT_LIST:
        try:
            subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
            print(f"Processing sub-{subject_id}...")

            base_evokeds = {
                cond: mne.read_epochs(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'), preload=True, verbose=False).average()
                for cond in BASE_CONDITIONS if os.path.exists(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'))
            }
            if not base_evokeds:
                print(f"  > No base condition files found for sub-{subject_id}. Skipping.")
                continue

            for key_cond, base_cond_list in KEY_CONDITIONS_MAP.items():
                evokeds_to_combine = [base_evokeds[bc] for bc in base_cond_list if bc in base_evokeds]
                if not evokeds_to_combine:
                    continue
                
                evoked = mne.combine_evoked(evokeds_to_combine, 'equal')

                # --- Find Peak Latencies ---
                _, p1_lat, _ = evoked.copy().pick(P1_ROI).get_peak(tmin=P1_TMIN, tmax=P1_TMAX, mode='pos', return_amplitude=True)
                _, n1_lat, _ = evoked.copy().pick(N1_ROI).get_peak(tmin=N1_TMIN, tmax=N1_TMAX, mode='neg', return_amplitude=True)

                # --- Calculate Slope on N1_ROI waveform ---
                roi_evoked = evoked.copy().pick(N1_ROI)
                roi_data_mean = roi_evoked.data.mean(axis=0)
                
                t_start_idx, t_end_idx = roi_evoked.time_as_index([p1_lat, n1_lat])
                
                # Ensure start is before end
                if t_start_idx >= t_end_idx:
                    print(f"  > P1 peak found after N1 peak for {key_cond}. Skipping slope calculation.")
                    continue
                
                time_segment = roi_evoked.times[t_start_idx:t_end_idx+1]
                data_segment = roi_data_mean[t_start_idx:t_end_idx+1]

                if len(time_segment) < 2:
                    print(f"  > Not enough data points between P1 and N1 for {key_cond}. Skipping.")
                    continue

                # Use numpy.polyfit to get the slope of the linear regression
                slope, _ = np.polyfit(time_segment, data_segment, 1)

                all_slopes.append({
                    'subject_id': subject_id,
                    'condition': key_cond,
                    'slope': slope
                })
        except Exception as e:
            print(f"--- FAILED to process Subject {subject_id}. Error: {e} ---")

    if not all_slopes:
        print("\n--- No slope data was generated. Cannot perform analysis or plotting. ---")
        return

    slope_df = pd.DataFrame(all_slopes)
    
    # --- 1. Perform Repeated Measures ANOVA ---
    print("\n--- Performing one-way repeated-measures ANOVA on slopes ---")
    try:
        # Filter for subjects who have data for all 3 conditions for a balanced ANOVA
        counts = slope_df['subject_id'].value_counts()
        complete_subjects = counts[counts == 3].index
        balanced_df = slope_df[slope_df['subject_id'].isin(complete_subjects)]

        if balanced_df.empty or len(balanced_df['subject_id'].unique()) < 2:
            raise ValueError("Not enough subjects with complete data for ANOVA.")

        aov = AnovaRM(data=balanced_df, depvar='slope', subject='subject_id', within=['condition'])
        res = aov.fit()
        
        anova_results_path = os.path.join(output_dir, '02_p1n1_slope_anova_results.txt')
        with open(anova_results_path, 'w') as f:
            f.write("One-Way Repeated Measures ANOVA Results for P1-N1 Slopes\n")
            f.write("="*60 + "\n")
            f.write(str(res))

        print(f"  > ANOVA results saved to: {anova_results_path}")
        print(res)

    except Exception as e:
        print(f"--- FAILED to perform ANOVA. Error: {e} ---")

    # --- 2. Generate Bar Plot ---
    print("\n--- Generating bar plot of P1-N1 slopes ---")
    plt.figure(figsize=(10, 7))
    sns.barplot(data=slope_df, x='condition', y='slope', order=['Landing on 1', 'Landing on 2', 'Landing on 3'], capsize=.1, errorbar='se')
    sns.stripplot(data=slope_df, x='condition', y='slope', order=['Landing on 1', 'Landing on 2', 'Landing on 3'], color='black', alpha=0.5, jitter=0.1)
    
    plt.title('Mean P1-N1 Slope by "Landing on" Condition', fontsize=16)
    plt.ylabel('Slope (Amplitude / Time)', fontsize=12)
    plt.xlabel('Condition', fontsize=12)
    plt.tight_layout()
    
    plot_path = os.path.join(output_dir, '02_p1n1_slope_barplot.png')
    if os.path.exists(plot_path):
        os.remove(plot_path)
    plt.savefig(plot_path)
    plt.close()
    print(f"  > Plot saved to: {plot_path}")

    print("\n--- Slope analysis complete. ---")


if __name__ == '__main__':
    analyze_p1n1_slope() 