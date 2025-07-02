import mne
import os
import glob
import argparse
import matplotlib.pyplot as plt
from mne.minimum_norm import make_inverse_operator, apply_inverse

# --- 1. CONFIGURATION ---
CONDITIONS = ["iSS", "dSS", "iLL", "dLL", "iSL", "dLS", "NoChg"]

def generate_loreta_plots(subjects_to_process, group_only):
    """
    Loads processed data for specified subjects, generates individual and
    group-level LORETA source estimate plots.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    fsaverage_dir = os.path.join(derivatives_dir, 'fsaverage')
    os.makedirs(fsaverage_dir, exist_ok=True)
    
    # --- Part 0: Setup for Source Localization ---
    print("\n--- Setting up for source localization ---")
    subjects_dir = os.path.join(fsaverage_dir, 'fs_subjects_dir')
    os.makedirs(subjects_dir, exist_ok=True)
    mne.datasets.fetch_fsaverage(subjects_dir=subjects_dir, verbose=False)
    
    subject_fs = 'fsaverage'
    fwd_fname = os.path.join(fsaverage_dir, f'{subject_fs}-fwd.fif')
    src_fname = os.path.join(fsaverage_dir, f'{subject_fs}-src.fif')

    if not os.path.exists(fwd_fname):
        print(f"Forward solution not found. Computing and saving to {fwd_fname}...")
        src = mne.setup_source_space(subject_fs, spacing='ico5', add_dist=False, subjects_dir=subjects_dir)
        mne.write_source_spaces(src_fname, src, overwrite=True)

        conductivity = (0.3, 0.006, 0.3)  # for 3-layer model
        model = mne.make_bem_model(subject=subject_fs, ico=3, conductivity=conductivity, subjects_dir=subjects_dir)
        bem = mne.make_bem_solution(model)
        
        montage = mne.channels.make_standard_montage('GSN-HydroCel-128')
        info_gen = mne.create_info(ch_names=montage.ch_names, sfreq=250, ch_types='eeg')
        info_gen.set_montage(montage)
        
        trans = 'fsaverage'
        
        fwd = mne.make_forward_solution(info_gen, trans=trans, src=src, bem=bem, eeg=True, mindist=5.0)
        mne.write_forward_solution(fwd_fname, fwd, overwrite=True)
    else:
        print(f"Loading existing forward solution from {fwd_fname}")

    fwd = mne.read_forward_solution(fwd_fname)
    src = fwd['src'] # More robust to load from fwd to ensure consistency

    # Dictionaries to hold all objects for grand averaging
    all_subject_stcs = {cond: [] for cond in CONDITIONS}

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects for LORETA plots: {subjects_to_process} ---")

    for subject_id in subjects_to_process:
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        subject_figure_dir = os.path.join(subject_dir, 'figures')
        os.makedirs(subject_figure_dir, exist_ok=True)
        
        print(f"\nProcessing Subject {subject_id}...")
        
        try:
            # Load all epochs for this subject to compute a noise covariance matrix.
            all_epochs_list = []
            subject_epochs_files = glob.glob(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-*_epo.fif'))
            for epo_file in subject_epochs_files:
                all_epochs_list.append(mne.read_epochs(epo_file, preload=True, verbose=False))
            
            if not all_epochs_list:
                print(f"  - No data files found for Subject {subject_id}. Skipping.")
                continue
                
            all_epochs = mne.concatenate_epochs(all_epochs_list)

            # --- Subject-level Inverse model setup ---
            noise_cov = mne.compute_covariance(all_epochs, tmax=0.0, method='shrunk', rank=None, verbose=False)
            inverse_operator = make_inverse_operator(all_epochs.info, forward=fwd, noise_cov=noise_cov, loose=0.2, depth=0.8, verbose=False)

            for cond in CONDITIONS:
                epo_file = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif')
                if os.path.exists(epo_file):
                    epochs = mne.read_epochs(epo_file, preload=True, verbose=False)
                    evoked = epochs.average()
                    print(f"  - Loaded {len(epochs)} epochs for condition '{cond}'.")
                    
                    # --- Source-level analysis (eLORETA) ---
                    snr = 3.0
                    lambda2 = 1.0 / snr ** 2
                    stc = apply_inverse(evoked, inverse_operator, lambda2, method="eLORETA", pick_ori=None, verbose=False)
                    all_subject_stcs[cond].append(stc)
                    
                    # This entire block for plotting and saving is now conditional
                    if not group_only:
                        times_to_plot = [0.150, 0.250, 0.450, 0.500]
                        for t in times_to_plot:
                            brain = stc.plot(
                                subjects_dir=subjects_dir, subject=subject_fs, hemi='both',
                                views=['lat', 'med'], initial_time=t,
                                time_label=f'sub-{subject_id} - {cond} eLORETA ({t*1000:.0f}ms)',
                                backend='pyvistaqt'
                            )
                            fig_path_stc = os.path.join(subject_figure_dir, f'sub-{subject_id}_stc_{cond}_{t*1000:.0f}ms.png')
                            if os.path.exists(fig_path_stc):
                                os.remove(fig_path_stc)
                            brain.save_image(fig_path_stc)
                            brain.close()
                            print(f"    - Saved LORETA plot for {t*1000:.0f}ms to {fig_path_stc}")

        except Exception as e:
            print(f"--- FAILED to generate LORETA plot for Subject {subject_id}. Error: {e} ---")

    # --- Group-Level Plots ---
    group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures')
    os.makedirs(group_figure_dir, exist_ok=True)
    
    if any(all_subject_stcs.values()):
        print("\n--- Generating group-level source plots (LORETA) ---")
        grand_average_stcs = {}
        for cond, stc_list in all_subject_stcs.items():
            if stc_list:
                # Correct way to average SourceEstimate objects: sum and divide.
                grand_average_stcs[cond] = sum(stc_list) / len(stc_list)

        if grand_average_stcs:
            times_to_plot = [0.150, 0.250, 0.450, 0.500]
            for cond, stc in grand_average_stcs.items():
                for t in times_to_plot:
                    brain = stc.plot(
                        subjects_dir=subjects_dir, subject=subject_fs, hemi='both',
                        views=['lat', 'med'], initial_time=t,
                        time_label=f'Group - {cond} eLORETA ({t*1000:.0f}ms)',
                        backend='pyvistaqt'
                    )
                    fig_path_stc = os.path.join(group_figure_dir, f'group_stc_{cond}_{t*1000:.0f}ms.png')
                    if os.path.exists(fig_path_stc):
                        os.remove(fig_path_stc)
                    brain.save_image(fig_path_stc)
                    brain.close()
                    print(f"  - Saved group LORETA plot for {cond} at {t*1000:.0f}ms")
    else:
        print("\n--- No source data available. Skipping group source plots. ---")

    print("\n--- LORETA plot generation complete. ---")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate eLORETA source estimate plots.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process (e.g., 02 03). If not provided, all subjects will be processed.')
    parser.add_argument('--group_only', action='store_true', help='Skip generating individual plots and only generate group plots.')
    args = parser.parse_args()
    
    generate_loreta_plots(args.subjects, args.group_only) 