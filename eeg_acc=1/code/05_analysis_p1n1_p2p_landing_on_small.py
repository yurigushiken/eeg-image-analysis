import os
import glob
import argparse
import mne
import pandas as pd
import numpy as np
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Configuration ---

# Base conditions to load, limited to small-to-small transitions
BASE_CONDITIONS = ['21', '31', '12', '32', '13', '23']

# How to combine base conditions into key conditions
KEY_CONDITIONS_MAP = {
    "Landing on 1": ["21", "31"],
    "Landing on 2": ["12", "32"],
    "Landing on 3": ["13", "23"]
}

# Single ROI for this analysis (Oz area)
OZ_ROI = ['E71', 'E75', 'E76', 'E70', 'E83', 'E74', 'E81', 'E82']

# Time windows for peak detection
P1_TMIN, P1_TMAX = 0.080, 0.130
N1_TMIN, N1_TMAX = 0.150, 0.200

# --- 2. Main Analysis Function ---

def analyze_p1n1_p2p(subjects_to_process=None):
    """
    Performs a Peak-to-Peak (P2P) analysis of the P1-N1 complex.
    """
    # Setup paths
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    except NameError:
        base_dir = os.path.abspath('eeg_acc=1')
        
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    script_name = os.path.basename(__file__).replace('.py', '')
    output_dir = os.path.join(derivatives_dir, 'group', 'results', script_name)
    os.makedirs(output_dir, exist_ok=True)

    # Get subjects if not specified
    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Starting Analysis 1: P1-N1 Peak-to-Peak ---")
    print(f"Processing {len(subjects_to_process)} subjects: {subjects_to_process}")

    # --- Data Extraction Loop ---
    results_data = []
    for subject_id in subjects_to_process:
        print(f"  - Subject: {subject_id}")
        
        for condition_name, base_conds in KEY_CONDITIONS_MAP.items():
            try:
                # Load all available base evokeds for this subject and condition
                evokeds_to_combine = []
                for bc in base_conds:
                    fpath = os.path.join(derivatives_dir, f'sub-{subject_id}', f'sub-{subject_id}_task-numbers_cond-{bc}_epo.fif')
                    if os.path.exists(fpath):
                        evokeds_to_combine.append(mne.read_epochs(fpath, preload=True, verbose=False).average())
                
                if not evokeds_to_combine:
                    print(f"    - WARNING: No data for {condition_name} for subject {subject_id}. Skipping.")
                    continue
                
                # Combine evokeds into the key condition
                key_evoked = mne.combine_evoked(evokeds_to_combine, 'equal')

                # Create a virtual channel by averaging over the Oz ROI
                roi_evoked = key_evoked.copy().pick(OZ_ROI)
                mean_data = roi_evoked.data.mean(axis=0, keepdims=True)
                mean_info = mne.create_info(ch_names=['mean_roi'], sfreq=key_evoked.info['sfreq'], ch_types='eeg')
                mean_roi_evoked = mne.EvokedArray(mean_data, mean_info, tmin=key_evoked.tmin)

                # Find P1 and N1 peaks on the virtual channel
                _, p1_lat, p1_amp = mean_roi_evoked.get_peak(tmin=P1_TMIN, tmax=P1_TMAX, mode='pos', return_amplitude=True)
                _, n1_lat, n1_amp = mean_roi_evoked.get_peak(tmin=N1_TMIN, tmax=N1_TMAX, mode='neg', return_amplitude=True)

                # Calculate P2P amplitude
                p2p_amplitude = p1_amp - n1_amp

                # Store results
                results_data.append({
                    'subject_id': subject_id,
                    'condition': condition_name,
                    'p1_amp': p1_amp,
                    'n1_amp': n1_amp,
                    'p2p_amp': p2p_amplitude
                })
            except Exception as e:
                print(f"    - ERROR processing {condition_name} for subject {subject_id}: {e}")

    # --- Statistical Analysis and Output ---
    if not results_data:
        print("--- No data collected. Cannot perform analysis. ---")
        return
        
    df_results = pd.DataFrame(results_data)
    
    # Save data to CSV
    csv_path = os.path.join(output_dir, 'group_p1n1_p2p_data.csv')
    df_results.to_csv(csv_path, index=False)
    print(f"\n--- P2P data saved to: {csv_path} ---")

    # Perform repeated measures ANOVA
    print("\n--- Performing Repeated Measures ANOVA on P2P Amplitude ---")
    rm_anova = pg.rm_anova(data=df_results, dv='p2p_amp', within='condition', subject='subject_id', detailed=True)
    print(rm_anova)
    
    # Generate and save plot
    print("\n--- Generating P2P Amplitude Plot ---")
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Define the desired order for the x-axis
    plot_order = ["Landing on 1", "Landing on 2", "Landing on 3"]
    
    sns.boxplot(data=df_results, x='condition', y='p2p_amp', ax=ax, order=plot_order)
    sns.stripplot(data=df_results, x='condition', y='p2p_amp', ax=ax, color='black', alpha=0.5, order=plot_order)
    
    ax.set_title('P1-N1 Peak-to-Peak Amplitude over Oz ROI', fontsize=16)
    ax.set_xlabel('Condition', fontsize=12)
    ax.set_ylabel('P2P Amplitude (μV)', fontsize=12)
    
    plot_path = os.path.join(output_dir, 'group_p1n1_p2p_plot.png')
    fig.savefig(plot_path, bbox_inches='tight')
    plt.close(fig)
    print(f"--- Plot saved to: {plot_path} ---")
    print("\n--- Analysis 1 Complete ---")

# --- 3. Script Execution ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run P1-N1 Peak-to-Peak Analysis.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process. If not provided, all subjects will be processed.')
    args = parser.parse_args()
    
    analyze_p1n1_p2p(args.subjects) 