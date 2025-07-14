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

# Electrodes of interest for N1 waveform (Bilateral Posterior-Occipito-Temporal)
N1_ELECTRODES_L = ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70']
N1_ELECTRODES_R = ['E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83']
POT_ROI_BILATERAL = N1_ELECTRODES_L + N1_ELECTRODES_R

# Time windows for peak detection
P1_TMIN, P1_TMAX = 0.080, 0.130
N1_TMIN, N1_TMAX = 0.150, 0.200

# --- 2. Generic Analysis Function ---

def run_p2p_analysis(output_dir, analysis_name, roi_electrodes, roi_name, subjects_to_process=None):
    """
    Performs a generic Peak-to-Peak (P2P) analysis for a given ROI.
    
    Args:
        output_dir (str): The directory to save all output files.
        analysis_name (str): A unique name for the analysis (used for file prefixes).
        roi_electrodes (list): List of electrode names for the ROI.
        roi_name (str): A display name for the ROI (e.g., 'Oz', 'POT Bilateral').
        subjects_to_process (list, optional): List of subjects to process. Defaults to all.
    Returns:
        pd.DataFrame: The ANOVA results table.
    """
    # Get subjects if not specified
    if not subjects_to_process:
        try:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        except NameError:
            base_dir = os.path.abspath('eeg_acc=1')
        derivatives_dir = os.path.join(base_dir, 'derivatives')
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Starting Analysis: {analysis_name} over {roi_name} ROI ---")
    print(f"Processing {len(subjects_to_process)} subjects: {subjects_to_process}")

    # --- Data Extraction Loop ---
    results_data = []
    for subject_id in subjects_to_process:
        print(f"  - Subject: {subject_id}")
        
        for condition_name, base_conds in KEY_CONDITIONS_MAP.items():
            try:
                # Setup paths
                try:
                    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                except NameError:
                    base_dir = os.path.abspath('eeg_acc=1')
                derivatives_dir = os.path.join(base_dir, 'derivatives')

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

                # Create a virtual channel by averaging over the specified ROI
                roi_evoked = key_evoked.copy().pick(roi_electrodes)
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
        print(f"--- No data collected for {analysis_name}. Cannot perform analysis. ---")
        return None
        
    df_results = pd.DataFrame(results_data)
    
    # Save data to CSV
    csv_path = os.path.join(output_dir, f'group_{analysis_name}_data.csv')
    df_results.to_csv(csv_path, index=False)
    print(f"\n--- P2P data for {analysis_name} saved to: {csv_path} ---")

    # Perform repeated measures ANOVA
    print(f"\n--- Performing Repeated Measures ANOVA on P2P Amplitude for {analysis_name} ---")
    rm_anova = pg.rm_anova(data=df_results, dv='p2p_amp', within='condition', subject='subject_id', detailed=True)
    print(rm_anova)
    
    # Generate and save plot
    print(f"\n--- Generating P2P Amplitude Plot for {analysis_name} ---")
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Define the desired order for the x-axis
    plot_order = ["Landing on 1", "Landing on 2", "Landing on 3"]
    
    sns.boxplot(data=df_results, x='condition', y='p2p_amp', ax=ax, order=plot_order)
    sns.stripplot(data=df_results, x='condition', y='p2p_amp', ax=ax, color='black', alpha=0.5, order=plot_order)
    
    ax.set_title(f'P1-N1 Peak-to-Peak Amplitude over {roi_name} ROI', fontsize=16)
    ax.set_xlabel('Condition', fontsize=12)
    ax.set_ylabel('P2P Amplitude (μV)', fontsize=12)
    
    plot_path = os.path.join(output_dir, f'group_{analysis_name}_plot.png')
    fig.savefig(plot_path, bbox_inches='tight')
    plt.close(fig)
    print(f"--- Plot for {analysis_name} saved to: {plot_path} ---")
    print(f"\n--- Analysis '{analysis_name}' Complete ---\n")

    return rm_anova

# --- 3. Script Execution ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run P1-N1 Peak-to-Peak Analysis for different ROIs.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process. If not provided, all subjects will be processed.')
    args = parser.parse_args()
    
    # --- Setup Output Directory ---
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    except NameError:
        base_dir = os.path.abspath('eeg_acc=1')
    
    script_name = os.path.basename(__file__).replace('.py', '')
    output_dir = os.path.join(base_dir, 'derivatives', 'group', 'results', script_name)
    os.makedirs(output_dir, exist_ok=True)

    # --- Run Analyses ---
    all_anova_results = {}

    # Analysis 1: Original Oz ROI
    analysis_1_name = f"{script_name}_oz_roi"
    anova_oz = run_p2p_analysis(
        output_dir=output_dir,
        analysis_name=analysis_1_name,
        roi_electrodes=OZ_ROI,
        roi_name='Oz',
        subjects_to_process=args.subjects
    )
    if anova_oz is not None:
        all_anova_results['P1-N1 P2P Amplitude (Oz ROI)'] = anova_oz

    # Analysis 2: New POT Bilateral ROI
    analysis_2_name = f"{script_name}_pot_roi"
    anova_pot = run_p2p_analysis(
        output_dir=output_dir,
        analysis_name=analysis_2_name,
        roi_electrodes=POT_ROI_BILATERAL,
        roi_name='POT Bilateral',
        subjects_to_process=args.subjects
    )
    if anova_pot is not None:
        all_anova_results['P1-N1 P2P Amplitude (POT Bilateral ROI)'] = anova_pot

    # --- Save Combined ANOVA Results ---
    if all_anova_results:
        anova_output_path = os.path.join(output_dir, f'{script_name}_anova_summary.txt')
        with open(anova_output_path, 'w') as f:
            for title, anova_table in all_anova_results.items():
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n")
                f.write(str(anova_table))
                f.write("\n\n")
        print(f"--- Combined ANOVA results saved to: {anova_output_path} ---") 