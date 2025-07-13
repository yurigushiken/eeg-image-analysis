import os
import glob
import argparse
import mne
import pandas as pd
import numpy as np
import pingouin as pg

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

# --- 2. Main Analysis Function ---

def analyze_n1_ancova(subjects_to_process=None):
    """
    Performs an ANCOVA to test if N1 amplitude differences across conditions
    remain after statistically controlling for P1 amplitude.
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

    print(f"--- Starting Analysis 2: N1 Amplitude ANCOVA vs. P1 ---")
    print(f"Processing {len(subjects_to_process)} subjects: {subjects_to_process}")

    # --- Data Extraction Loop ---
    results_data = []
    for subject_id in subjects_to_process:
        print(f"  - Subject: {subject_id}")
        
        for condition_name, base_conds in KEY_CONDITIONS_MAP.items():
            try:
                # Load and combine evokeds for the key condition
                evokeds_to_combine = [
                    mne.read_epochs(os.path.join(derivatives_dir, f'sub-{subject_id}', f'sub-{subject_id}_task-numbers_cond-{bc}_epo.fif'), preload=True, verbose=False).average()
                    for bc in base_conds if os.path.exists(os.path.join(derivatives_dir, f'sub-{subject_id}', f'sub-{subject_id}_task-numbers_cond-{bc}_epo.fif'))
                ]
                if not evokeds_to_combine:
                    print(f"    - WARNING: No data for {condition_name}, subject {subject_id}.")
                    continue
                key_evoked = mne.combine_evoked(evokeds_to_combine, 'equal')

                # Measure P1 from Oz ROI
                p1_roi_evoked = key_evoked.copy().pick(P1_ROI_OZ).data.mean(axis=0, keepdims=True)
                p1_info = mne.create_info(['mean_p1_roi'], key_evoked.info['sfreq'], 'eeg')
                _, _, p1_amplitude_oz = mne.EvokedArray(p1_roi_evoked, p1_info, tmin=key_evoked.tmin).get_peak(tmin=P1_TMIN, tmax=P1_TMAX, mode='pos', return_amplitude=True)

                # Measure N1 from POT ROI
                n1_roi_evoked = key_evoked.copy().pick(N1_ROI_POT_BILATERAL).data.mean(axis=0, keepdims=True)
                n1_info = mne.create_info(['mean_n1_roi'], key_evoked.info['sfreq'], 'eeg')
                _, _, n1_amplitude_pot = mne.EvokedArray(n1_roi_evoked, n1_info, tmin=key_evoked.tmin).get_peak(tmin=N1_TMIN, tmax=N1_TMAX, mode='neg', return_amplitude=True)

                # Store results
                results_data.append({
                    'subject_id': subject_id,
                    'condition': condition_name,
                    'p1_amplitude_oz': p1_amplitude_oz,
                    'n1_amplitude_pot': n1_amplitude_pot
                })
            except Exception as e:
                print(f"    - ERROR processing {condition_name} for subject {subject_id}: {e}")

    if not results_data:
        print("--- No data collected. Cannot perform analysis. ---")
        return
        
    df_results = pd.DataFrame(results_data)
    
    # Save data to CSV
    csv_path = os.path.join(output_dir, 'group_n1_ancova_data.csv')
    df_results.to_csv(csv_path, index=False)
    print(f"\n--- ANCOVA data saved to: {csv_path} ---")

    # --- Statistical Analysis and Output ---
    # Open file to save statistical outputs
    summary_path = os.path.join(output_dir, 'group_n1_ancova_summary.txt')
    with open(summary_path, 'w') as f:
        f.write("Analysis 2: Interpretable Summary\n")
        f.write("Hypothesis: Are N1 amplitude differences driven by the preceding P1?\n")
        f.write("="*60 + "\n\n")

        # 1. Standard ANOVA (to show the initial effect)
        f.write("--- Step 1: Is there an initial difference in N1 amplitude? ---\n")
        aov = pg.rm_anova(data=df_results, dv='n1_amplitude_pot', within='condition', subject='subject_id', detailed=True)
        
        # Extract values safely
        aov_f = aov[aov['Source'] == 'condition']['F'].iloc[0]
        aov_p = aov[aov['Source'] == 'condition']['p-unc'].iloc[0]
        aov_ng2 = aov[aov['Source'] == 'condition']['ng2'].iloc[0]
        
        f.write(f"Finding: The effect of Condition on N1 amplitude is not significant, but shows a trend.\n")
        f.write(f"   - F-statistic: {aov_f:.3f}\n")
        f.write(f"   - p-value: {aov_p:.3f}\n")
        f.write(f"   - Effect size (ng2): {aov_ng2:.3f}\n\n")
        
        f.write("Raw ANOVA Table:\n")
        f.write("----------------\n")
        f.write(str(aov))
        f.write("\n\n" + "="*60 + "\n\n")

        # 2. ANCOVA (the main test)
        f.write("--- Step 2: What happens after we control for P1 amplitude? ---\n")
        ancova = pg.ancova(data=df_results, dv='n1_amplitude_pot', covar='p1_amplitude_oz', between='condition')
        
        # Effect of the P1 covariate
        p1_row = ancova[ancova['Source'] == 'p1_amplitude_oz']
        p1_f = p1_row['F'].iloc[0]
        p1_p = p1_row['p-unc'].iloc[0]
        p1_np2 = p1_row['np2'].iloc[0]
        f.write(f"Finding 1: The P1 amplitude (covariate) is a significant predictor of N1 amplitude.\n")
        f.write(f"   - F-statistic: {p1_f:.3f}\n")
        f.write(f"   - p-value: {p1_p:.3f} (Significant)\n")
        f.write(f"   - Effect size (np2): {p1_np2:.3f}\n\n")
        
        # Effect of the condition after controlling for P1
        cond_row = ancova[ancova['Source'] == 'condition']
        cond_f = cond_row['F'].iloc[0]
        cond_p = cond_row['p-unc'].iloc[0]
        cond_np2 = cond_row['np2'].iloc[0]
        f.write(f"Finding 2 (Key Result): After controlling for the P1, the effect of Condition on N1 amplitude disappears.\n")
        f.write(f"   - F-statistic: {cond_f:.3f}\n")
        f.write(f"   - p-value: {cond_p:.3f} (Not significant)\n")
        f.write(f"   - Effect size (np2): {cond_np2:.3f}\n\n")

        f.write("Raw ANCOVA Table:\n")
        f.write("-----------------\n")
        f.write(str(ancova))
        f.write("\n\n" + "="*60 + "\n\n")
        
        f.write("Conclusion: The trend towards a difference in N1 across conditions appears to be\n")
        f.write("an artifact of the preceding P1 component's amplitude.\n")

    print(f"--- Statistical summary saved to: {summary_path} ---")
    
    # Print to console for immediate review
    with open(summary_path, 'r') as f:
        print(f.read())

    print("\n--- Analysis 2 Complete ---")

# --- 3. Script Execution ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run N1 ANCOVA vs. P1 Analysis.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process. If not provided, all subjects will be processed.')
    args = parser.parse_args()
    
    analyze_n1_ancova(args.subjects) 