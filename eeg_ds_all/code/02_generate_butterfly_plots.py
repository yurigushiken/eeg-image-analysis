import mne
import os
import glob
import argparse
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION ---
CONDITIONS = ["iSS", "dSS", "iLL", "dLL", "iSL", "dLS", "NoChg"]
PZ_ELECTRODE = 'E62'

def generate_butterfly_plots(subjects_to_process):
    """
    Loads processed data for specified subjects and generates individual and
    group-level butterfly plots.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    
    all_subject_evokeds = {cond: [] for cond in CONDITIONS}

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects for butterfly plots: {subjects_to_process} ---")

    for subject_id in subjects_to_process:
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        subject_figure_dir = os.path.join(subject_dir, 'figures')
        os.makedirs(subject_figure_dir, exist_ok=True)
        
        print(f"\nProcessing Subject {subject_id}...")
        
        try:
            evokeds = {}
            for cond in CONDITIONS:
                epo_file = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif')
                if os.path.exists(epo_file):
                    epochs = mne.read_epochs(epo_file, preload=True, verbose=False)
                    evoked = epochs.average()
                    evokeds[cond] = evoked
                    all_subject_evokeds[cond].append(evoked)
                    print(f"  - Loaded {len(epochs)} epochs for condition '{cond}'.")

            if not evokeds:
                print(f"  - No data found for Subject {subject_id}. Skipping.")
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
            print(f"--- FAILED to generate butterfly plot for Subject {subject_id}. Error: {e} ---")

    # --- Group-Level Plots ---
    group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures')
    os.makedirs(group_figure_dir, exist_ok=True)
    
    grand_averages = { cond: mne.grand_average(evoked_list) for cond, evoked_list in all_subject_evokeds.items() if evoked_list }
    
    if not grand_averages:
        print("\n--- No data available for any subject. Skipping group plots. ---")
    else:
        print("\n--- Generating group-level grand average butterfly plots ---")
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

    print("\n--- Butterfly plot generation complete. ---")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate EEG butterfly plots.')
    parser.add_argument('--subjects', nargs='*', help='Specific subject ID(s) to process (e.g., 02 03). If not provided, all subjects will be processed.')
    args = parser.parse_args()
    generate_butterfly_plots(args.subjects) 