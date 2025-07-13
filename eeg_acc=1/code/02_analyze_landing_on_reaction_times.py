import os
import pandas as pd
import glob
from statsmodels.stats.anova import AnovaRM
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# --- 1. CONFIGURATION ---
# This is the base directory where the raw behavioral files are located.
BEHAVIORAL_DATA_DIR = r"D:\numbers_eeg\lab_data\Final Behavioral Data Files\data_UTF8"

# Mapping from CellNumber to our key "Landing on" conditions
# This defines which trials we are interested in.
LANDING_ON_MAP = {
    1: ['21', '31', '41'],
    2: ['32', '42', '52'],
    3: ['43', '53', '63']
}

# List of all subjects to be included in the analysis.
PARTICIPANT_LIST = [
    "02", "03", "04", "05", "08", "09", "10", "11", "12", "13", "14", "15",
    "17", "21", "22", "23", "25", "26", "27", "28", "29", "31", "32", "33"
]

def analyze_reaction_times():
    """
    Analyzes reaction times for "Landing on" conditions.

    This function loads behavioral data for each subject, filters for correct
    trials based on the LANDING_ON_MAP, calculates the mean reaction time for
    each condition per subject, generates a violin plot to visualize the
    distributions, and performs a one-way repeated-measures ANOVA to test
    for statistical significance.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    output_dir = os.path.join(base_dir, 'derivatives', '02_reaction_time_analysis')
    os.makedirs(output_dir, exist_ok=True)
    
    all_subjects_rt_data = []

    print(f"--- Starting Reaction Time Analysis for {len(PARTICIPANT_LIST)} subjects ---")

    for subject_id in PARTICIPANT_LIST:
        try:
            behavioral_file = os.path.join(BEHAVIORAL_DATA_DIR, f"Subject{subject_id}.csv")
            if not os.path.exists(behavioral_file):
                print(f"  > Warning: Behavioral file not found for Subject {subject_id}. Skipping.")
                continue

            df = pd.read_csv(behavioral_file)
            
            # Filter out practice trials
            df = df[df['Procedure[Block]'] != "Practiceproc"].copy()
            
            # --- Filter for correct trials in our conditions of interest ---
            # Use 'Target.ACC' as the primary accuracy column
            correct_trials_df = df[df['Target.ACC'] == 1].copy()
            
            # Map CellNumber to the "Landing on" condition
            # First, convert CellNumber to string to match the map keys
            correct_trials_df['CellNumber_str'] = correct_trials_df['CellNumber'].astype(str)
            
            # Create a reverse map for easier lookup
            cell_to_landing_map = {cell: f"Landing on {land_num}" 
                                   for land_num, cells in LANDING_ON_MAP.items() 
                                   for cell in cells}
            
            correct_trials_df['condition'] = correct_trials_df['CellNumber_str'].map(cell_to_landing_map)
            
            # Drop trials that don't belong to our conditions of interest
            correct_trials_df.dropna(subset=['condition'], inplace=True)

            if correct_trials_df.empty:
                print(f"  > Warning: No correct trials found for the specified conditions for Subject {subject_id}. Skipping.")
                continue

            # --- Calculate mean RT per condition for this subject ---
            mean_rt = correct_trials_df.groupby('condition')['Target.RT'].mean().reset_index()
            mean_rt['subject_id'] = subject_id
            
            all_subjects_rt_data.append(mean_rt)

        except Exception as e:
            print(f"--- FAILED to process Subject {subject_id}. Error: {e} ---")

    if not all_subjects_rt_data:
        print("\n--- No data processed. Cannot perform analysis or plotting. ---")
        return

    # Concatenate all data into a single DataFrame
    rt_df = pd.concat(all_subjects_rt_data, ignore_index=True)

    # --- 1. Generate Violin Plot ---
    print("\n--- Generating violin plot of reaction times ---")
    plt.figure(figsize=(10, 7))
    sns.violinplot(data=rt_df, x='condition', y='Target.RT', order=['Landing on 1', 'Landing on 2', 'Landing on 3'], inner='point')
    plt.title('Distribution of Mean Reaction Times by "Landing on" Condition', fontsize=16)
    plt.ylabel('Mean Reaction Time (ms)', fontsize=12)
    plt.xlabel('Condition', fontsize=12)
    plt.tight_layout()
    
    plot_path = os.path.join(output_dir, '02_reaction_time_violin_plot.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"  > Plot saved to: {plot_path}")

    # --- 2. Perform Repeated Measures ANOVA ---
    print("\n--- Performing one-way repeated-measures ANOVA ---")
    try:
        aov = AnovaRM(data=rt_df, depvar='Target.RT', subject='subject_id', within=['condition'])
        res = aov.fit()
        
        anova_results_path = os.path.join(output_dir, '02_reaction_time_anova_results.txt')
        with open(anova_results_path, 'w') as f:
            f.write("One-Way Repeated Measures ANOVA Results for Reaction Times\n")
            f.write("="*60 + "\n")
            f.write(str(res))

        print(f"  > ANOVA results saved to: {anova_results_path}")
        print(res)

    except Exception as e:
        print(f"--- FAILED to perform ANOVA. Error: {e} ---")

    print("\n--- Behavioral analysis complete. ---")


if __name__ == '__main__':
    analyze_reaction_times() 