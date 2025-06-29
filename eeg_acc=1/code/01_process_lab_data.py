import os
import re
import pandas as pd
import mne
import numpy as np

# --- 1. CONFIGURATION ---
# Please adjust these paths to match your directory structure.
BASE_DATA_DIR = r"D:\numbers_eeg\lab_data"
DERIVATIVES_DIR = r"D:\numbers_eeg\eeg_acc=1\derivatives"

# Input file paths
BEHAVIORAL_DATA_DIR = os.path.join(BASE_DATA_DIR, "Final Behavioral Data Files", "data_UTF8")
HAPPE_SET_DIR = os.path.join(BASE_DATA_DIR, "5 - processed")
HAPPE_USABLE_TRIALS_FILE = os.path.join(BASE_DATA_DIR, "HAPPE_Usable_Trials.csv")
ELECTRODE_LOC_FILE = r"D:\numbers_eeg\assets\Channel Location - Net128_v1.sfp\AdultAverageNet128_v1.sfp"

# Create derivatives directory if it doesn't exist
os.makedirs(DERIVATIVES_DIR, exist_ok=True)

# List of participants to process
PARTICIPANT_LIST = [
    "02", "03", "04", "05", "08", "09", "10", "11", "12", "13", "14", "15",
    "17", "21", "22", "23", "25", "26", "27", "28", "29", "31", "32", "33"
]

# --- 2. DATA PROCESSING ---

print("Starting data processing script for ACC=1, by CellNumber...")

# Load the HAPPE usable trials master file once
try:
    usable_trials_df = pd.read_csv(HAPPE_USABLE_TRIALS_FILE)
    usable_trials_df.rename(columns={usable_trials_df.columns[0]: 'SessionInfo'}, inplace=True)
except FileNotFoundError:
    print(f"ERROR: Cannot find HAPPE usable trials file at: {HAPPE_USABLE_TRIALS_FILE}")
    exit()

# Loop through each participant
for subject_id in PARTICIPANT_LIST:
    print(f"\n{'='*20} Processing Subject {subject_id} {'='*20}")

    try:
        # --- 3. Find and Parse Usable Trial Indices from HAPPE file ---
        print("Step 1: Finding usable trials from HAPPE output...")
        subject_row = None
        pattern = re.compile(f'(?:Subject|Subj){int(subject_id)}')
        subject_row = usable_trials_df[usable_trials_df['SessionInfo'].str.contains(pattern, na=False)].iloc[0]

        kept_indices_str = subject_row['Kept_Segs_Indxs']
        kept_indices_1based = [int(i.strip()) for i in kept_indices_str.split(',')]
        print(f"Found {len(kept_indices_1based)} usable trials kept by HAPPE.")

        # --- 4. Load, Process, and Map Behavioral Data ---
        print("Step 2: Loading and processing behavioral data...")
        behavioral_file = os.path.join(BEHAVIORAL_DATA_DIR, f"Subject{subject_id}.csv")
        behavioral_df = pd.read_csv(behavioral_file)

        # Filter out practice trials
        behavioral_df = behavioral_df[behavioral_df['Procedure[Block]'] != "Practiceproc"].copy()
        behavioral_df.reset_index(drop=True, inplace=True)

        # Replicate R script logic to create continuous trial numbers (1-300)
        block_correction = (behavioral_df.index // 60) * 60
        behavioral_df['Trial_Continuous'] = behavioral_df['Trial'] + block_correction
        
        # Filter behavioral data to only include trials that were kept by HAPPE
        behavioral_df_kept = behavioral_df[behavioral_df['Trial_Continuous'].isin(kept_indices_1based)].copy()
        
        # Use the 'CellNumber' as the condition label
        behavioral_df_kept['condition_label'] = behavioral_df_kept['CellNumber'].astype(str)
        
        behavioral_df_kept.reset_index(drop=True, inplace=True)
        print(f"Matched and labeled {len(behavioral_df_kept)} trials in the behavioral file.")

        # --- 5. Load EEG Data (.set file) ---
        print("Step 3: Loading cleaned EEG data (.set file)...")
        set_file_path = os.path.join(HAPPE_SET_DIR, f"Subject{subject_id}.set")
        epochs = mne.io.read_epochs_eeglab(set_file_path, verbose=False)
        epochs.apply_baseline(baseline=(None, 0))

        if len(epochs) != len(behavioral_df_kept):
            print(f"CRITICAL WARNING: Mismatch for Subject {subject_id}!")
            print(f"Epochs in .set file: {len(epochs)}")
            print(f"Kept trials in behavioral file: {len(behavioral_df_kept)}")
            print("Skipping this subject due to data mismatch.")
            continue
            
        print(f"Loaded {len(epochs)} epochs from .set file.")

        # --- 6. Merge EEG with Behavioral Data and Filter for Correct Trials ---
        print("Step 4: Merging behavioral metadata and filtering for correct trials...")
        epochs.metadata = behavioral_df_kept
        
        acc_cols = [col for col in epochs.metadata.columns if 'Target' in col and 'ACC' in col]
        query = " or ".join([f"`{col}` == 1" for col in acc_cols])
        
        correct_epochs = epochs[query]

        # Also filter out trials that do not have a condition label (shouldn't happen here, but good practice)
        correct_epochs = correct_epochs[correct_epochs.metadata['condition_label'].notna()]
        
        n_correct = len(correct_epochs)
        n_total_kept = len(epochs)
        print(f"Filtered epochs: Kept {n_correct} out of {n_total_kept} HAPPE-usable trials ({n_correct/n_total_kept:.2%}).")

        # --- 7. Apply Electrode Locations & Set Average Reference ---
        print("Step 5: Applying electrode locations and setting average reference...")
        montage = mne.channels.read_custom_montage(ELECTRODE_LOC_FILE)
        correct_epochs.set_montage(montage, on_missing='warn')
        correct_epochs.set_eeg_reference('average', projection=True)

        # --- 8. Save Output Files (One per Condition) ---
        print("Step 6: Saving .fif and .h5 files for each condition (CellNumber)...")
        subject_output_dir = os.path.join(DERIVATIVES_DIR, f"sub-{subject_id}")
        os.makedirs(subject_output_dir, exist_ok=True)

        unique_conditions = sorted(correct_epochs.metadata['condition_label'].unique())
        print(f"Found conditions to save: {unique_conditions}")

        for cond_label in unique_conditions:
            epochs_this_cond = correct_epochs[correct_epochs.metadata['condition_label'] == cond_label]

            if len(epochs_this_cond) == 0:
                print(f"  - No correct trials for condition '{cond_label}'. Skipping file save.")
                continue

            fif_output_path = os.path.join(subject_output_dir, f"sub-{subject_id}_task-numbers_cond-{cond_label}_epo.fif")
            h5_output_path = os.path.join(subject_output_dir, f"sub-{subject_id}_task-numbers_cond-{cond_label}_metadata.h5")

            epochs_this_cond.save(fif_output_path, overwrite=True)
            epochs_this_cond.metadata.to_hdf(h5_output_path, key='metadata', mode='w')

            print(f"  - Saved {len(epochs_this_cond)} epochs for '{cond_label}' to {fif_output_path}")

    except FileNotFoundError as e:
        print(f"ERROR for Subject {subject_id}: A required file was not found: {e}")
        print("Skipping this subject.")
    except IndexError:
        print(f"ERROR: Could not find entry for Subject {subject_id} in {HAPPE_USABLE_TRIALS_FILE}. Skipping.")
    except Exception as e:
        print(f"An unexpected error occurred while processing Subject {subject_id}: {e}")
        print("Skipping this subject.")

print(f"\nProcessing complete. All output files saved in: {DERIVATIVES_DIR}") 