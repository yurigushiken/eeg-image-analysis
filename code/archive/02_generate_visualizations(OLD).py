import mne
import os
import argparse
import matplotlib.pyplot as plt

# --- 0. Configuration ---
USABLE_SUBJECTS = [
    '02', '03', '04', '05', '08', '09', '10', '11', '12', '13', '14',
    '15', '17', '21', '22', '23', '25', '26', '27', '28', '29', '31', 
    '32', '33'
]
CONDITIONS = ["iSS", "dSS", "iLL", "dLL", "iSL", "dLS", "NoChg"]

# --- Main Visualization Function ---
def generate_visualizations(subjects_to_run):
    """
    This function loads processed data and generates individual and group-level plots.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    
    all_subject_evokeds = {cond: [] for cond in CONDITIONS}

    # --- Part 1: Individual Visualizations ---
    print(f"--- STARTING VISUALIZATION PIPELINE FOR {len(subjects_to_run)} SUBJECTS ---")
    for subject_id in subjects_to_run:
        print(f"\n{'='*50}\nGenerating figures for Subject: {subject_id}\n{'='*50}")
        try:
            subject_data_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
            subject_figure_dir = os.path.join(subject_data_dir, 'figures')
            os.makedirs(subject_figure_dir, exist_ok=True)

            evokeds_fname = os.path.join(subject_data_dir, f'sub-{subject_id}_evokeds.fif')
            evokeds = mne.read_evokeds(evokeds_fname)
            
            # Generate plots for each condition
            for cond in CONDITIONS:
                evoked = next((e for e in evokeds if e.comment == cond), None)
                if evoked is None: continue

                # Load LORETA and plot 3D brain
                stc_fname = os.path.join(subject_data_dir, f'sub-{subject_id}_cond-{cond}_loretas-stc.h5')
                if os.path.exists(stc_fname):
                    stc = mne.read_source_estimate(stc_fname)
                    brain = stc.plot(surface='pial', hemi='both', backend='pyvistaqt', show=False)
                    brain.save_image(os.path.join(subject_figure_dir, f'sub-{subject_id}_eloreta_{cond}_3D.png'))
                    brain.close()

                # Topography plot for each condition
                fig = evoked.plot_topomap(times=[0.150, 0.250, 0.400], show=False, title=f'sub-{subject_id} - {cond} Topography')
                fig.savefig(os.path.join(subject_figure_dir, f'sub-{subject_id}_topomap_{cond}.png'))
                plt.close(fig)

                # Add this evoked to the list for grand averaging
                all_subject_evokeds[cond].append(evoked)

            print(f"Successfully generated individual figures for subject {subject_id}")

        except Exception as e:
            print(f"--- FAILED to generate figures for Subject {subject_id}. Error: {e} ---")
            continue

    # --- Part 2: Group-Level (Grand Average) Visualizations ---
    if len(all_subject_evokeds["iSS"]) < 2:
        print("\nSkipping Grand Average plots: need at least 2 subjects.")
    else:
        print(f"\n{'='*50}\nCreating Grand Average visualizations...\n{'='*50}")
        group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures')
        os.makedirs(group_figure_dir, exist_ok=True)

        # Calculate all grand averages
        grand_averages = {cond: mne.grand_average(all_subject_evokeds[cond]) for cond in CONDITIONS}

        # Create new comparison plots
        # Plot 1: Small Number Direction Effect
        mne.viz.plot_compare_evokeds(
            {'Increasing (iSS)': grand_averages['iSS'], 'Decreasing (dSS)': grand_averages['dSS']},
            picks='E62', show=False, title='Grand Average: Small Number Direction Effect (Pz)'
        ).savefig(os.path.join(group_figure_dir, 'ga_compare_small_direction.png'))

        # Plot 2: Large Number Direction Effect
        mne.viz.plot_compare_evokeds(
            {'Increasing (iLL)': grand_averages['iLL'], 'Decreasing (dLL)': grand_averages['dLL']},
            picks='E62', show=False, title='Grand Average: Large Number Direction Effect (Pz)'
        ).savefig(os.path.join(group_figure_dir, 'ga_compare_large_direction.png'))
        
        # Plot 3: Crossover Effect
        mne.viz.plot_compare_evokeds(
            {'Small-to-Large (iSL)': grand_averages['iSL'], 'Large-to-Small (dLS)': grand_averages['dLS']},
            picks='E62', show=False, title='Grand Average: Crossover Effect (Pz)'
        ).savefig(os.path.join(group_figure_dir, 'ga_compare_crossover.png'))

        plt.close('all')
        print("Successfully generated all group-level figures.")

    print("\n--- VISUALIZATION PIPELINE COMPLETE ---")

# --- Main execution block ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate visualizations from processed data.")
    parser.add_argument('--subjects', nargs='*', default=None, help='Optional: List of subject IDs to process.')
    args = parser.parse_args()
    subjects_to_process = args.subjects if args.subjects else USABLE_SUBJECTS
    generate_visualizations(subjects_to_process) 