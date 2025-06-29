import mne
import os
import glob
import argparse
import matplotlib.pyplot as plt
import numpy as np

# --- 1. CONFIGURATION ---
CONDITIONS = [
    "21","31","32","41","42","43","52","53","54","63","64","65",
    "12","13","14","23","24","25","34","35","36","45","46","56",
    "11","22","33","44","55","66"
]

NON_SCALP_CHANNELS = [
    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E43', 'E44', 'E48', 
    'E49', 'E113', 'E114', 'E119', 'E120', 'E121', 'E125', 'E126', 'E127', 'E128'
]


def generate_topomaps(subjects_to_process):
    """
    Loads processed data for specified subjects and generates individual and
    group-level topomaps.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    
    all_subject_evokeds = {cond: [] for cond in CONDITIONS}

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects for topomaps: {subjects_to_process} ---")

    for subject_id in subjects_to_process:
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        subject_figure_dir = os.path.join(subject_dir, 'figures')
        os.makedirs(subject_figure_dir, exist_ok=True)
        
        print(f"\nProcessing Subject {subject_id}...")
        
        try:
            evokeds_this_subject = {}
            for cond in CONDITIONS:
                epo_file = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif')
                if os.path.exists(epo_file):
                    epochs = mne.read_epochs(epo_file, preload=True, verbose=False)
                    evoked = epochs.average()
                    evokeds_this_subject[cond] = evoked
                    all_subject_evokeds[cond].append(evoked)
                    print(f"  - Loaded {len(epochs)} epochs for condition '{cond}'.")

                    scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)

                    fig_topo = scalp_evoked.plot_topomap(
                        times=[0.150, 0.250, 0.485],
                        units=dict(eeg='µV'),
                        vlim=(-6, 6),
                        show=False
                    )
                    fig_topo.suptitle(f'sub-{subject_id} - {cond} Topography')
                    fig_path = os.path.join(subject_figure_dir, f'sub-{subject_id}_topomap_{cond}.png')
                    if os.path.exists(fig_path):
                        os.remove(fig_path)
                    fig_topo.savefig(fig_path)
                    plt.close(fig_topo)
                    print(f"    - Saved topomap to {fig_path}")

            if not evokeds_this_subject:
                print(f"  - No data found for Subject {subject_id}. Skipping.")
                continue

        except Exception as e:
            print(f"--- FAILED to generate topomaps for Subject {subject_id}. Error: {e} ---")

    # --- Group-Level Plots ---
    group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures')
    os.makedirs(group_figure_dir, exist_ok=True)
    
    grand_averages = { cond: mne.grand_average(evoked_list) for cond, evoked_list in all_subject_evokeds.items() if evoked_list }
    
    if not grand_averages:
        print("\n--- No data available for any subject. Skipping group plots. ---")
    else:
        print("\n--- Generating group-level grand average topomaps ---")
        for cond, evoked in grand_averages.items():
            scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)

            fig_topo_grp = scalp_evoked.plot_topomap(
                times=[0.150, 0.250, 0.485],
                units=dict(eeg='µV'),
                vlim=(-6, 6),
                show=False
            )
            fig_topo_grp.suptitle(f'Grand Average Topomap: {cond}')
            fig_path_topo_grp = os.path.join(group_figure_dir, f'group_topomap_{cond}.png')
            if os.path.exists(fig_path_topo_grp):
                os.remove(fig_path_topo_grp)
            fig_topo_grp.savefig(fig_path_topo_grp)
            plt.close(fig_topo_grp)
            print(f"  - Saved grand average topomap for {cond} to {fig_path_topo_grp}")

    print("\n--- Topomap generation complete. ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate EEG topomaps.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process (e.g., 02 03). If not provided, all subjects will be processed.')
    args = parser.parse_args()
    generate_topomaps(args.subjects) 