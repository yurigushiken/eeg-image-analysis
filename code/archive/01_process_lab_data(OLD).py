import mne
import os
import argparse
import numpy as np
import pandas as pd
import glob

# --- 0. Configuration ---
# The hardcoded USABLE_SUBJECTS list is no longer needed.
# The script will now discover subjects automatically.
CONDITIONS = {
    "iSS": "iSS (Correct)", "dSS": "dSS (Correct)",
    "iLL": "iLL (Correct)", "dLL": "dLL (Correct)",
    "iSL": "iSL (Correct)", "dLS": "dLS (Correct)",
    "NoChg": "NoChg (Correct)"
}

# --- Main Processing Function ---
def process_data(subjects_to_run):
    """
    This function loads EEG and behavioral data, merges them, processes them, 
    and saves the Evoked and Source Time Course data.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # Define paths to the cleanly named data files
    eeg_data_dir = os.path.join(base_dir, 'lab_data', '5 - processed')
    behavioral_data_dir = os.path.join(base_dir, 'lab_data', 'Final Behavioral Data Files', 'data_UTF8')
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    assets_dir = os.path.join(base_dir, 'assets')
    sfp_file = os.path.join(assets_dir, 'Channel Location - Net128_v1.sfp', 'AdultAverageNet128_v1.sfp')
    
    print(f"--- STARTING PROCESSING PIPELINE FOR {len(subjects_to_run)} SUBJECTS ---")

    for subject_id_str in subjects_to_run:
        subject_id = int(subject_id_str)
        print(f"\n{'='*50}\nProcessing Subject: {subject_id}\n{'='*50}")
        try:
            # --- Part 1: Construct Paths to Standardized Files ---
            set_file_path = os.path.join(eeg_data_dir, f"Subject{subject_id_str}.set")
            behavioral_file_path = os.path.join(behavioral_data_dir, f"Subject{subject_id_str}.csv")

            # Check that the files exist
            if not os.path.exists(set_file_path) or not os.path.exists(behavioral_file_path):
                print(f" ERROR: Data file(s) not found for subject {subject_id_str}. Skipping.")
                continue
            
            subject_output_dir = os.path.join(derivatives_dir, f'sub-{subject_id_str}')
            os.makedirs(subject_output_dir, exist_ok=True)
            
            # --- Part 2: Load Data ---
            print(f"  Loading EEG data from: {set_file_path}")
            epochs = mne.io.read_epochs_eeglab(set_file_path)
            epochs.set_montage(mne.channels.read_custom_montage(sfp_file))
            
            print(f"  Loading behavioral data from: {behavioral_file_path}")
            behavioral_df = pd.read_csv(behavioral_file_path, encoding='utf-8', delimiter='\t')

            # --- Part 3: The Correct Merging and Filtering Sequence ---
            # The HAPPE pipeline has already rejected bad trials from the EEG data.
            # We must now filter the behavioral data to match the trials that remain in the EEG.
            # We assume trials with incorrect responses were rejected.
            
            print("  Filtering behavioral data for correct trials to align with EEG...")
            # Using 'V1.ACC' as the accuracy column based on file inspection.
            behavioral_df_correct = behavioral_df[behavioral_df['V1.ACC'] == 1].copy()

            # A. New Validation: The number of epochs in the .set file should now match
            #    the number of correct trials in the behavioral file.
            if len(epochs) != len(behavioral_df_correct):
                raise ValueError(
                    f"Trial count mismatch after filtering for accuracy! "
                    f"EEG epochs ({len(epochs)}) != Correct behavioral trials ({len(behavioral_df_correct)})"
                )
            print("  Trial counts validated successfully after accuracy filtering.")

            # B. Attach the correctly filtered metadata
            epochs.metadata = behavioral_df_correct.reset_index(drop=True)
            
            # C. & D. The data is now fully aligned and clean. No further filtering of the epochs object is needed.
            epochs_correct = epochs
            print(f"  Data cleaned and aligned: {len(epochs_correct)} correct trials remain.")

            # --- Part 4: Proceed with Analysis ---
            # All subsequent analysis uses the `epochs_correct` object.
            fs_dir = mne.datasets.fetch_fsaverage(verbose=False)
            src = os.path.join(fs_dir, 'bem', 'fsaverage-ico-5-src.fif')
            bem = os.path.join(fs_dir, 'bem', 'fsaverage-5120-5120-5120-bem-sol.fif')
            fwd = mne.make_forward_solution(epochs_correct.info, trans='fsaverage', src=src, bem=bem, meg=False, eeg=True, mindist=5.0)
            noise_cov = mne.compute_covariance(epochs_correct, tmax=0.0, method=['shrunk', 'empirical'])
            inverse_operator = mne.minimum_norm.make_inverse_operator(epochs_correct.info, fwd, noise_cov, loose=0.2, depth=0.8)

            evokeds_to_save = []
            for short_name in CONDITIONS.keys():
                print(f"  Calculating ERP and LORETA for condition: {short_name}")
                # The metadata column for condition is 'condition', not 'change_group'
                condition_query = f"condition == '{short_name}'"
                evoked = epochs_correct[condition_query].average()
                evoked.comment = short_name
                evokeds_to_save.append(evoked)

                stc = mne.minimum_norm.apply_inverse(evoked, inverse_operator, lambda2=1.0/9.0, method='eLORETA')
                stc_fname = os.path.join(subject_output_dir, f'sub-{subject_id_str}_cond-{short_name}_loretas-stc.h5')
                stc.save(stc_fname, ftype='h5', overwrite=True)
            
            evokeds_fname = os.path.join(subject_output_dir, f'sub-{subject_id_str}_evokeds.fif')
            mne.write_evokeds(evokeds_fname, evokeds_to_save, overwrite=True)
            print(f"Successfully processed and saved all derivatives for subject {subject_id}")

        except Exception as e:
            print(f"--- FAILED to process Subject {subject_id}. Error: {e} ---")
            continue
            
    print("\n--- PROCESSING PIPELINE COMPLETE ---")

# --- Main execution block ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process EEG data by merging with behavioral files.")
    parser.add_argument('--subjects', nargs='*', default=None, help='Optional: Specific list of subject IDs to process. If not provided, all subjects found in the data directory will be processed.')
    args = parser.parse_args()
    
    subjects_to_process = args.subjects

    if subjects_to_process is None:
        # Dynamically discover subjects from the EEG data directory
        print("No specific subjects provided. Discovering subjects automatically...")
        eeg_data_dir = os.path.join(os.path.dirname(__file__), '..', 'lab_data', '5 - processed')
        all_set_files = glob.glob(os.path.join(eeg_data_dir, 'Subject*.set'))
        
        # Extract subject ID from filenames
        subjects_to_process = sorted([os.path.basename(f).replace('Subject', '').replace('.set', '') for f in all_set_files])
        
        if not subjects_to_process:
            print("No subject data files found. Exiting.")
            exit()
        
        print(f"Found {len(subjects_to_process)} subjects to process: {', '.join(subjects_to_process)}")

    process_data(subjects_to_process) 