import mne
import os
import glob
import argparse
import matplotlib.pyplot as plt
import numpy as np
from mne.minimum_norm import make_inverse_operator, apply_inverse

# --- 1. CONFIGURATION ---
# Conditions based on the previous script's mapping. The script is robust
# to conditions not being present for a given subject.
CONDITIONS = ["iSS", "dSS", "iLL", "dLL", "iSL", "dLS", "NoChg"]
# Electrode to use for butterfly plots
PZ_ELECTRODE = 'E62' 

# --- 2. MAIN VISUALIZATION FUNCTION ---
def generate_visualizations(subjects_to_process, skip_source=False):
    """
    Loads processed data for specified subjects, generates individual topomaps,
    and creates group-level grand average comparison plots.
    """
    # Get project root and derivatives directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    
    # --- Part 0: Setup for Source Localization ---
    if not skip_source:
        print("\n--- Setting up for source localization ---")
        # The 'fsaverage' dataset is used as a template brain model.
        # MNE will automatically download it if it's not found.
        subjects_dir = os.path.join(derivatives_dir, 'fs_subjects_dir')
        os.makedirs(subjects_dir, exist_ok=True)
        mne.datasets.fetch_fsaverage(subjects_dir=subjects_dir, verbose=False) # Download fsaverage
        
        # Path to the forward solution file
        subject_fs = 'fsaverage'
        fwd_fname = os.path.join(derivatives_dir, f'{subject_fs}-fwd.fif')
        src_fname = os.path.join(derivatives_dir, f'{subject_fs}-src.fif')

        if not os.path.exists(fwd_fname):
            print(f"Forward solution not found. Computing and saving to {fwd_fname}...")
            # We need a source space, which describes the locations of the dipoles.
            src = mne.setup_source_space(subject_fs, spacing='ico5', add_dist=False, subjects_dir=subjects_dir)
            mne.write_source_spaces(src_fname, src, overwrite=True)

            # We need a BEM model, which describes the conductivity of the head.
            conductivity = (0.3, 0.006, 0.3)  # for 3-layer model
            model = mne.make_bem_model(subject=subject_fs, ico=3, conductivity=conductivity, subjects_dir=subjects_dir)
            bem = mne.make_bem_solution(model)
            
            # We need the transformation matrix from MRI to head coordinates
            # We use a generic info object for the forward model computation
            montage = mne.channels.make_standard_montage('GSN-HydroCel-128')
            info_gen = mne.create_info(ch_names=montage.ch_names, sfreq=250, ch_types='eeg')
            info_gen.set_montage(montage)
            
            trans = 'fsaverage'  # MNE's built-in fsaverage transformation
            
            fwd = mne.make_forward_solution(info_gen, trans=trans, src=src, bem=bem, eeg=True, mindist=5.0)
            mne.write_forward_solution(fwd_fname, fwd, overwrite=True)
        else:
            print(f"Loading existing forward solution from {fwd_fname}")

        fwd = mne.read_forward_solution(fwd_fname)
        src = mne.read_source_spaces(src_fname)

    # Dictionaries to hold all objects for grand averaging
    all_subject_evokeds = {cond: [] for cond in CONDITIONS}
    all_subject_stcs = {cond: [] for cond in CONDITIONS} # For source estimates

    # --- Part 1: Process each subject individually ---
    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects: {subjects_to_process} ---")

    for subject_id in subjects_to_process:
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        subject_figure_dir = os.path.join(subject_dir, 'figures')
        os.makedirs(subject_figure_dir, exist_ok=True)
        
        print(f"\nProcessing Subject {subject_id}...")

        try:
            # --- Subject-level Inverse model setup ---
            # Load all epochs for this subject to compute a noise covariance matrix.
            all_epochs_list = []
            subject_epochs_files = glob.glob(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-*_epo.fif'))
            for epo_file in subject_epochs_files:
                all_epochs_list.append(mne.read_epochs(epo_file, preload=True, verbose=False))
            
            if not all_epochs_list:
                print(f"  - No data files found for Subject {subject_id}. Skipping.")
                continue
                
            all_epochs = mne.concatenate_epochs(all_epochs_list)

            # --- Initialize variables ---
            evokeds = {}
            stcs = {} # For source estimates of this subject

            # --- Sensor-level processing (always runs) ---
            for cond in CONDITIONS:
                epo_file = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif')
                if os.path.exists(epo_file):
                    epochs = mne.read_epochs(epo_file, preload=True, verbose=False)
                    evoked = epochs.average()
                    evokeds[cond] = evoked
                    all_subject_evokeds[cond].append(evoked)
                    print(f"  - Loaded {len(epochs)} epochs for condition '{cond}'.")

                    # Generate and save topography plot with improved settings
                    fig_topo = evoked.plot_topomap(
                        times=[0.150, 0.250, 0.485],
                        ch_type='eeg',
                        units=dict(eeg='µV'),
                        scalings=dict(eeg=1e6),
                        vlim=(-6, 6),
                        outlines='head',
                        show=False
                    )
                    fig_topo.suptitle(f'sub-{subject_id} - {cond} Topography')
                    fig_path = os.path.join(subject_figure_dir, f'sub-{subject_id}_topomap_{cond}.png')
                    if os.path.exists(fig_path):
                        os.remove(fig_path)
                    fig_topo.savefig(fig_path)
                    plt.close(fig_topo)
                    print(f"    - Saved topomap to {fig_path}")

            # --- Source-level processing (optional) ---
            if not skip_source:
                # We need the inverse operator for this subject
                noise_cov = mne.compute_covariance(all_epochs, tmax=0.0, method='shrunk', rank=None, verbose=False)
                inverse_operator = make_inverse_operator(all_epochs.info, forward=fwd, noise_cov=noise_cov, loose=0.2, depth=0.8, verbose=False)
                
                for cond, evoked in evokeds.items():
                    # --- Source-level analysis (eLORETA) ---
                    snr = 3.0
                    lambda2 = 1.0 / snr ** 2
                    stc = apply_inverse(evoked, inverse_operator, lambda2, method="eLORETA", pick_ori=None, verbose=False)
                    all_subject_stcs[cond].append(stc)
                    
                    brain = stc.plot(subjects_dir=subjects_dir, subject=subject_fs, hemi='both', views=['lat', 'med'], initial_time=0.4, backend='matplotlib')
                    fig_stc = brain.get_figure()
                    fig_stc.suptitle(f'sub-{subject_id} - {cond} eLORETA (400ms)')
                    fig_path_stc = os.path.join(subject_figure_dir, f'sub-{subject_id}_stc_{cond}.png')
                    if os.path.exists(fig_path_stc):
                        os.remove(fig_path_stc)
                    fig_stc.savefig(fig_path_stc)
                    plt.close(fig_stc)
                    print(f"    - Saved LORETA plot to {fig_path_stc}")

            if not evokeds:
                continue
            
            # --- Subject-level butterfly plot ---
            fig_bfly = mne.viz.plot_compare_evokeds(evokeds, picks=PZ_ELECTRODE, show=False)[0]
            fig_bfly.suptitle(f'sub-{subject_id}: ERP at {PZ_ELECTRODE}')
            fig_path_bfly = os.path.join(subject_figure_dir, f'sub-{subject_id}_erp_butterfly.png')
            if os.path.exists(fig_path_bfly):
                os.remove(fig_path_bfly)
            fig_bfly.savefig(fig_path_bfly)
            plt.close(fig_bfly)
            print(f"  - Saved ERP butterfly plot to {fig_path_bfly}")

        except Exception as e:
            print(f"--- FAILED to generate figures for Subject {subject_id}. Error: {e} ---")

    # --- Part 2: Generate Group-Level Sensor Plots ---
    group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures')
    os.makedirs(group_figure_dir, exist_ok=True)
    
    grand_averages = { cond: mne.grand_average(evoked_list) for cond, evoked_list in all_subject_evokeds.items() if evoked_list }
    
    if not grand_averages:
        print("\n--- No data available for any subject. Skipping group plots. ---")
    else:
        print("\n--- Generating group-level grand average sensor plots ---")
        all_evokeds = {k: v for k, v in grand_averages.items()}
        fig_grp_bfly = mne.viz.plot_compare_evokeds(all_evokeds, picks=PZ_ELECTRODE, show=False)[0]
        fig_grp_bfly.suptitle('Grand Average over all Conditions at ' + PZ_ELECTRODE)
        fig_path = os.path.join(group_figure_dir, 'group_all_conditions_butterfly.png')
        if os.path.exists(fig_path):
            os.remove(fig_path)
        fig_grp_bfly.savefig(fig_path)
        plt.close(fig_grp_bfly)
        print(f"  - Saved butterfly plot to {fig_path}")

        comparisons = {'Distance': ['dSS', 'dLL'], 'Stimulus': ['dSS', 'iSS'], 'Interaction': ['dSS', 'iLL', 'dLL', 'iSS']}
        for name, conds in comparisons.items():
            evokeds_to_plot = {c: all_evokeds[c] for c in conds if c in all_evokeds}
            if len(evokeds_to_plot) > 1:
                fig_comp = mne.viz.plot_compare_evokeds(evokeds_to_plot, picks=PZ_ELECTRODE, show=False)[0]
                fig_comp.suptitle(f'Grand Average Comparison: {name}')
                fig_path_comp = os.path.join(group_figure_dir, f'group_{name}_comparison.png')
                if os.path.exists(fig_path_comp):
                    os.remove(fig_path_comp)
                fig_comp.savefig(fig_path_comp)
                plt.close(fig_comp)
                print(f"  - Saved {name} comparison plot to {fig_path_comp}")

        # --- Create individual grand average topomaps for each condition ---
        for cond, evoked in grand_averages.items():
            fig_topo_grp = evoked.plot_topomap(
                times=[0.150, 0.250, 0.485],
                ch_type='eeg',
                units=dict(eeg='µV'),
                scalings=dict(eeg=1e6),
                vlim=(-6, 6),
                outlines='head',
                show=False
            )
            fig_topo_grp.suptitle(f'Grand Average Topomap: {cond}')
            fig_path_topo_grp = os.path.join(group_figure_dir, f'group_topomap_{cond}.png')
            if os.path.exists(fig_path_topo_grp):
                os.remove(fig_path_topo_grp)
            fig_topo_grp.savefig(fig_path_topo_grp)
            plt.close(fig_topo_grp)
            print(f"  - Saved grand average topomap for {cond} to {fig_path_topo_grp}")

    # --- Part 3: Generate Group-Level Source Plots ---
    if skip_source:
        print("\n--- Skipping group-level source plots (LORETA) ---")
    else:
        print("\n--- Generating group-level source plots (LORETA) ---")
        grand_average_stcs = { cond: mne.grand_average(stc_list) for cond, stc_list in all_subject_stcs.items() if stc_list }

        if not grand_average_stcs:
            print("\n--- No source data available. Skipping group source plots. ---")
        else:
            for name, conds in comparisons.items():
                stcs_to_compare = [grand_average_stcs.get(c) for c in conds if c in grand_average_stcs]
                if len(stcs_to_compare) > 1:
                    stc_diff = stcs_to_compare[0] - stcs_to_compare[1]
                    brain = stc_diff.plot(subjects_dir=subjects_dir, subject=subject_fs, hemi='both', views=['lat', 'med'], backend='matplotlib')
                    fig_stc_grp = brain.get_figure()
                    fig_stc_grp.suptitle(f'Grand Average LORETA: {conds[0]} vs {conds[1]}')
                    fig_path_stc_group = os.path.join(group_figure_dir, f'group_stc_{name}_comparison.png')
                    if os.path.exists(fig_path_stc_group):
                        os.remove(fig_path_stc_group)
                    fig_stc_grp.savefig(fig_path_stc_group)
                    plt.close(fig_stc_grp)
                    print(f"  - Saved LORETA comparison plot for {name} to {fig_path_stc_group}")

    print("\n--- Visualization complete. Figures saved in 'derivatives' directory. ---")


# --- 3. SCRIPT EXECUTION ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate EEG visualizations.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process (e.g., 02 03). If not provided, all subjects will be processed.')
    parser.add_argument('--skip-source', action='store_true', help='Skip the source localization (LORETA) steps.')
    args = parser.parse_args()
    
    generate_visualizations(args.subjects, args.skip_source) 