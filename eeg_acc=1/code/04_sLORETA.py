import mne
import os
import numpy as np
from mne.minimum_norm import make_inverse_operator, apply_inverse

# --- CONFIGURATION ---
# All 30 specific conditions for Tasks 1 & 2
ALL_30_CONDITIONS = [
    "21", "31", "32", "41", "42", "43", "52", "53", "54", "63", "64", "65",  # decrease
    "12", "13", "14", "23", "24", "25", "34", "35", "36", "45", "46", "56",  # increase
    "11", "22", "33", "44", "55", "66"  # no change (cardinalities 1-6)
]

# 6 cardinality conditions for Task 3
CARDINALITY_CONDITIONS = ["11", "22", "33", "44", "55", "66"]

# All subjects to process
ALL_SUBJECTS = [f"{i:02d}" for i in [2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 17, 21, 22, 23, 25, 26, 27, 28, 29, 31, 32, 33]]

# Analysis configuration
ANALYSIS_MODE = 'individual'  # 'individual' for Task 1, 'grand_average' for Tasks 2 & 3
SUBJECT = "02"  # For individual analysis
TASK = 1  # 1: individual all conditions, 2: grand average all conditions, 3: grand average cardinalities

def setup_source_space_and_forward_solution(derivatives_dir, subjects_dir, subject_fs):
    """
    Set up source space and forward solution for sLORETA analysis.
    """
    print("\n--- Setting up source space and forward solution ---")
    
    # Ensure FreeSurfer average brain is available
    mne.datasets.fetch_fsaverage(subjects_dir=subjects_dir, verbose=False)
    
    fwd_fname = os.path.join(derivatives_dir, f'{subject_fs}-fwd.fif')
    src_fname = os.path.join(derivatives_dir, f'{subject_fs}-src.fif')
    
    if not os.path.exists(fwd_fname):
        print(f"Forward solution not found. Computing and saving to {fwd_fname}...")
        
        # Create source space
        src = mne.setup_source_space(
            subject_fs, 
            spacing='ico5', 
            add_dist=False, 
            subjects_dir=subjects_dir
        )
        mne.write_source_spaces(src_fname, src, overwrite=True)
        
        # Create BEM model
        conductivity = (0.3, 0.006, 0.3)  # scalp, skull, brain
        model = mne.make_bem_model(
            subject=subject_fs, 
            ico=3, 
            conductivity=conductivity, 
            subjects_dir=subjects_dir
        )
        bem = mne.make_bem_solution(model)
        
        # Set up EEG montage
        montage = mne.channels.make_standard_montage('GSN-HydroCel-128')
        info_gen = mne.create_info(
            ch_names=montage.ch_names, 
            sfreq=250, 
            ch_types='eeg'
        )
        info_gen.set_montage(montage)
        
        # Create forward solution
        trans = 'fsaverage'
        fwd = mne.make_forward_solution(
            info_gen, 
            trans=trans, 
            src=src, 
            bem=bem, 
            eeg=True, 
            mindist=5.0
        )
        mne.write_forward_solution(fwd_fname, fwd, overwrite=True)
    else:
        print(f"Loading existing forward solution from {fwd_fname}")
        fwd = mne.read_forward_solution(fwd_fname)
    
    return fwd, fwd['src']

def load_single_condition_epochs(subject_dir, subject_id, condition):
    """
    Load epochs for a single condition.
    
    Parameters:
    -----------
    subject_dir : str
        Path to subject directory
    subject_id : str
        Subject identifier
    condition : str
        Condition code (e.g., '21', '12', etc.)
    
    Returns:
    --------
    epochs : Epochs object or None if not found
    """
    epo_file = os.path.join(
        subject_dir, 
        f'sub-{subject_id}_task-numbers_cond-{condition}_epo.fif'
    )
    
    if os.path.exists(epo_file):
        epochs = mne.read_epochs(epo_file, preload=True, verbose=False)
        print(f"  - Loaded {len(epochs)} epochs for condition '{condition}'")
        return epochs
    else:
        print(f"  - WARNING: Epochs file not found for condition '{condition}'. Skipping.")
        return None

def compute_inverse_operator_from_epochs(epochs, fwd):
    """
    Compute inverse operator for source localization.
    """
    print("Computing noise covariance and inverse operator...")
    
    # Use baseline period for noise covariance
    noise_cov = mne.compute_covariance(
        epochs, 
        tmax=0.0, 
        method='shrunk', 
        rank=None, 
        verbose=False
    )
    
    inverse_operator = make_inverse_operator(
        epochs.info, 
        forward=fwd, 
        noise_cov=noise_cov, 
        loose=0.2, 
        depth=0.8, 
        verbose=False
    )
    
    return inverse_operator

def task1_individual_all_conditions(subject_id, conditions):
    """
    Task 1: Individual subject LORETA for all 30 conditions
    """
    # Setup directories
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    subjects_dir = os.path.join(derivatives_dir, 'fs_subjects_dir')
    subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
    
    os.makedirs(subjects_dir, exist_ok=True)
    
    print(f"\n--- TASK 1: Individual sLORETA Analysis for Subject {subject_id} ---")
    print(f"Processing {len(conditions)} conditions")
    
    try:
        # Setup source space and forward solution
        subject_fs = 'fsaverage'
        fwd, src = setup_source_space_and_forward_solution(
            derivatives_dir, subjects_dir, subject_fs
        )
        
        # Process each condition individually
        for condition in conditions:
            print(f"\n--- Processing condition: {condition} ---")
            
            # Load epochs for this condition
            epochs = load_single_condition_epochs(subject_dir, subject_id, condition)
            
            if epochs is None:
                continue
                
            # Compute inverse operator
            inverse_operator = compute_inverse_operator_from_epochs(epochs, fwd)
            
            # Average epochs to get evoked response
            evoked = epochs.average()
            
            # Apply inverse solution (sLORETA)
            lambda2 = 1.0 / 9.0  # SNR^2 regularization parameter
            stc = apply_inverse(
                evoked, 
                inverse_operator, 
                lambda2, 
                method="sLORETA", 
                pick_ori=None, 
                verbose=False
            )
            
            # Find peak activation time
            peak_time = stc.get_peak()[1]
            print(f"  - Peak activation at {peak_time*1000:.1f}ms")
            
            # Create interactive brain plot
            brain = stc.plot(
                subjects_dir=subjects_dir,
                subject=subject_fs,
                hemi='both',
                views=['lat', 'med'],
                time_viewer=True,
                backend='pyvistaqt',
                initial_time=peak_time,
                time_label=f'sub-{subject_id} - Condition {condition} sLORETA ({len(epochs)} epochs, peak: {peak_time*1000:.1f}ms)'
            )
            
            # Wait for user input before closing
            input(f"Press ENTER to close the plot for condition '{condition}' and continue...")
        
        print(f"\n--- TASK 1: Individual analysis complete for Subject {subject_id} ---")
        
    except Exception as e:
        print(f"\n--- ERROR: Failed to process Subject {subject_id} ---")
        print(f"Error details: {e}")
        raise

def task2_grand_average_all_conditions(subjects_list, conditions):
    """
    Task 2: Grand average LORETA for all 30 conditions
    """
    # Setup directories
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    subjects_dir = os.path.join(derivatives_dir, 'fs_subjects_dir')
    
    os.makedirs(subjects_dir, exist_ok=True)
    
    print(f"\n--- TASK 2: Grand Average sLORETA Analysis ---")
    print(f"Subjects to include: {subjects_list}")
    print(f"Processing {len(conditions)} conditions")
    
    try:
        # Setup source space and forward solution
        subject_fs = 'fsaverage'
        fwd, src = setup_source_space_and_forward_solution(
            derivatives_dir, subjects_dir, subject_fs
        )
        
        # Process each condition
        for condition in conditions:
            print(f"\n--- Processing condition: {condition} ---")
            
            # Collect evoked responses from all subjects for this condition
            condition_evokeds = []
            successful_subjects = []
            
            for subject_id in subjects_list:
                try:
                    subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
                    epochs = load_single_condition_epochs(subject_dir, subject_id, condition)
                    
                    if epochs is not None:
                        evoked = epochs.average()
                        condition_evokeds.append(evoked)
                        successful_subjects.append(subject_id)
                        print(f"  - Subject {subject_id}: {len(epochs)} epochs averaged")
                    
                except Exception as e:
                    print(f"  - ERROR loading Subject {subject_id}: {e}")
                    continue
            
            if not condition_evokeds:
                print(f"  - No valid data found for condition '{condition}'. Skipping.")
                continue
            
            # Compute grand average
            print(f"  - Computing grand average across {len(condition_evokeds)} subjects...")
            grand_avg_evoked = mne.grand_average(condition_evokeds)
            
            # Use the first successful subject's data to compute inverse operator
            first_subject_dir = os.path.join(derivatives_dir, f'sub-{successful_subjects[0]}')
            first_subject_epochs = load_single_condition_epochs(first_subject_dir, successful_subjects[0], condition)
            inverse_operator = compute_inverse_operator_from_epochs(first_subject_epochs, fwd)
            
            # Apply inverse solution (sLORETA)
            lambda2 = 1.0 / 9.0
            stc = apply_inverse(
                grand_avg_evoked, 
                inverse_operator, 
                lambda2, 
                method="sLORETA", 
                pick_ori=None, 
                verbose=False
            )
            
            # Find peak activation time
            peak_time = stc.get_peak()[1]
            print(f"  - Peak activation at {peak_time*1000:.1f}ms")
            
            # Create interactive brain plot
            brain = stc.plot(
                subjects_dir=subjects_dir,
                subject=subject_fs,
                hemi='both',
                views=['lat', 'med'],
                time_viewer=True,
                backend='pyvistaqt',
                initial_time=peak_time,
                time_label=f'Grand Average - Condition {condition} sLORETA (n={len(successful_subjects)}, peak: {peak_time*1000:.1f}ms)'
            )
            
            # Wait for user input before closing
            input(f"Press ENTER to close the plot for condition '{condition}' and continue...")
        
        print(f"\n--- TASK 2: Grand Average analysis complete ---")
        
    except Exception as e:
        print(f"\n--- ERROR: Failed to complete grand average analysis ---")
        print(f"Error details: {e}")
        raise

def task3_grand_average_cardinalities(subjects_list, cardinality_conditions):
    """
    Task 3: Grand average LORETA for 6 cardinality conditions (1, 2, 3, 4, 5, 6)
    """
    # Setup directories
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    subjects_dir = os.path.join(derivatives_dir, 'fs_subjects_dir')
    
    os.makedirs(subjects_dir, exist_ok=True)
    
    print(f"\n--- TASK 3: Grand Average Cardinality sLORETA Analysis ---")
    print(f"Subjects to include: {subjects_list}")
    print(f"Cardinality conditions: {cardinality_conditions}")
    
    try:
        # Setup source space and forward solution
        subject_fs = 'fsaverage'
        fwd, src = setup_source_space_and_forward_solution(
            derivatives_dir, subjects_dir, subject_fs
        )
        
        # Process each cardinality condition
        for i, condition in enumerate(cardinality_conditions, 1):
            print(f"\n--- Processing cardinality {i} (condition {condition}) ---")
            
            # Collect evoked responses from all subjects for this cardinality
            cardinality_evokeds = []
            successful_subjects = []
            
            for subject_id in subjects_list:
                try:
                    subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
                    epochs = load_single_condition_epochs(subject_dir, subject_id, condition)
                    
                    if epochs is not None:
                        evoked = epochs.average()
                        cardinality_evokeds.append(evoked)
                        successful_subjects.append(subject_id)
                        print(f"  - Subject {subject_id}: {len(epochs)} epochs averaged")
                    
                except Exception as e:
                    print(f"  - ERROR loading Subject {subject_id}: {e}")
                    continue
            
            if not cardinality_evokeds:
                print(f"  - No valid data found for cardinality {i}. Skipping.")
                continue
            
            # Compute grand average
            print(f"  - Computing grand average across {len(cardinality_evokeds)} subjects...")
            grand_avg_evoked = mne.grand_average(cardinality_evokeds)
            
            # Use the first successful subject's data to compute inverse operator
            first_subject_dir = os.path.join(derivatives_dir, f'sub-{successful_subjects[0]}')
            first_subject_epochs = load_single_condition_epochs(first_subject_dir, successful_subjects[0], condition)
            inverse_operator = compute_inverse_operator_from_epochs(first_subject_epochs, fwd)
            
            # Apply inverse solution (sLORETA)
            lambda2 = 1.0 / 9.0
            stc = apply_inverse(
                grand_avg_evoked, 
                inverse_operator, 
                lambda2, 
                method="sLORETA", 
                pick_ori=None, 
                verbose=False
            )
            
            # Find peak activation time
            peak_time = stc.get_peak()[1]
            print(f"  - Peak activation at {peak_time*1000:.1f}ms")
            
            # Create interactive brain plot
            brain = stc.plot(
                subjects_dir=subjects_dir,
                subject=subject_fs,
                hemi='both',
                views=['lat', 'med'],
                time_viewer=True,
                backend='pyvistaqt',
                initial_time=peak_time,
                time_label=f'Grand Average - Cardinality {i} sLORETA (n={len(successful_subjects)}, peak: {peak_time*1000:.1f}ms)'
            )
            
            # Wait for user input before closing
            input(f"Press ENTER to close the plot for cardinality {i} and continue...")
        
        print(f"\n--- TASK 3: Grand Average cardinality analysis complete ---")
        
    except Exception as e:
        print(f"\n--- ERROR: Failed to complete cardinality analysis ---")
        print(f"Error details: {e}")
        raise

def main():
    """
    Main function to run sLORETA analysis for Tasks 1, 2, and 3.
    """
    print("=" * 60)
    print("sLORETA Analysis Tool - Tasks 1, 2, 3")
    print("=" * 60)
    
    if TASK == 1:
        # Task 1: Individual subject analysis for all 30 conditions
        task1_individual_all_conditions(SUBJECT, ALL_30_CONDITIONS)
    elif TASK == 2:
        # Task 2: Grand average analysis for all 30 conditions
        task2_grand_average_all_conditions(ALL_SUBJECTS, ALL_30_CONDITIONS)
    elif TASK == 3:
        # Task 3: Grand average analysis for 6 cardinality conditions
        task3_grand_average_cardinalities(ALL_SUBJECTS, CARDINALITY_CONDITIONS)
    else:
        print("ERROR: Invalid TASK number. Use 1, 2, or 3")

if __name__ == '__main__':
    main()