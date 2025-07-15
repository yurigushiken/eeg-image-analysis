import mne
import os
import glob
import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# --- 1. CONFIGURATION ---
BASE_CONDITIONS = ['12', '21']

KEY_CONDITIONS_MAP = {
    '1 to 2 (Inc)': ['12'],
    '2 to 1 (Dec)': ['21'],
}

CONDITION_COLORS = {
    '1 to 2 (Inc)': '#1f77b4',  # Blue
    '2 to 1 (Dec)': '#e41a1c',  # Red
}

# Electrodes of interest for P1 (Oz region)
P1_ELECTRODES = ['E71', 'E75', 'E76', 'E70', 'E83', 'E74', 'E81', 'E82']

# Time window for P1 peak search
PEAK_TMIN, PEAK_TMAX = 0.080, 0.130

NON_SCALP_CHANNELS = [
    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E43', 'E44', 'E48',
    'E49', 'E113', 'E114', 'E119', 'E120', 'E121', 'E125', 'E126', 'E127', 'E128'
]


def generate_p1_inc12_dec21_plots(subjects_to_process):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    script_name = os.path.basename(__file__).replace('.py', '')

    all_subject_evokeds = {cond: [] for cond in BASE_CONDITIONS}

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- Processing subjects for P1 inc12 vs dec21 plots: {subjects_to_process} ---")

    # --- Individual Subject Plots ---
    for subject_id in subjects_to_process:
        subject_dir = os.path.join(derivatives_dir, f'sub-{subject_id}')
        subject_figure_dir = os.path.join(subject_dir, 'figures', script_name)
        os.makedirs(subject_figure_dir, exist_ok=True)
        print(f"\nProcessing Subject {subject_id}...")

        try:
            base_evokeds = {
                cond: mne.read_epochs(
                    os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'),
                    preload=True, verbose=False
                ).average()
                for cond in BASE_CONDITIONS
                if os.path.exists(os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{cond}_epo.fif'))
            }
            for cond, evoked in base_evokeds.items():
                all_subject_evokeds[cond].append(evoked)
            if not base_evokeds:
                print("  - No data found. Skipping.")
                continue

            key_evokeds = {
                key: mne.combine_evoked([base_evokeds[bc] for bc in bcl if bc in base_evokeds], 'equal')
                for key, bcl in KEY_CONDITIONS_MAP.items()
                if any(bc in base_evokeds for bc in bcl)
            }
            if len(key_evokeds) < 2:
                print("  - Not enough data for both conditions. Skipping.")
                continue

            # Peak detection
            peak_times = {}
            for cond_name, evoked in key_evokeds.items():
                roi_data = evoked.get_data(picks=P1_ELECTRODES).mean(axis=0)
                info = mne.create_info(['ROI'], evoked.info['sfreq'], ch_types='eeg')
                roi_evoked = mne.EvokedArray(roi_data[np.newaxis, :], info, tmin=evoked.tmin)
                _, peak_time = roi_evoked.get_peak(tmin=PEAK_TMIN, tmax=PEAK_TMAX, mode='pos')
                peak_times[cond_name] = peak_time

            # Plot
            fig = plt.figure(figsize=(10, 6))
            fig.suptitle(f'Sub-{subject_id}: P1 Numbers Pair (Inc12 vs Dec21, ACC=1)', fontsize=14)
            gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1.5])
            ax_erp = fig.add_subplot(gs[0, :])

            mne.viz.plot_compare_evokeds(
                key_evokeds, picks=P1_ELECTRODES, combine='mean', axes=ax_erp,
                title='Mean ERP over Oz', show=False, legend='upper left', ci=False,
                colors=CONDITION_COLORS
            )

            for cname, ptime in peak_times.items():
                ax_erp.axvline(x=ptime, color=CONDITION_COLORS[cname], linestyle='--', linewidth=1)

            for i, (cname, evoked) in enumerate(key_evokeds.items()):
                ax_topo = fig.add_subplot(gs[1, i])
                scalp = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
                scalp.plot_topomap(times=peak_times[cname], axes=ax_topo, show=False, vlim=(-6, 6), colorbar=False)
                ax_topo.set_title(f"{cname}\n{int(peak_times[cname]*1000)} ms", color=CONDITION_COLORS[cname])

            fig.subplots_adjust(right=0.85, hspace=0.4)
            cbar_ax = fig.add_axes([0.88, 0.2, 0.02, 0.3])
            plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax, label='µV')

            out_path = os.path.join(subject_figure_dir, f'sub-{subject_id}_{script_name}.png')
            if os.path.exists(out_path):
                os.remove(out_path)
            fig.savefig(out_path, bbox_inches='tight'); plt.close(fig)
            print(f"    - Saved P1 plot to {out_path}")

        except Exception as e:
            print(f"--- FAILED for subject {subject_id}: {e} ---")

    # Group level
    group_dir = os.path.join(derivatives_dir, 'group', 'figures', script_name)
    os.makedirs(group_dir, exist_ok=True)
    grand_avg_base = {
        cond: mne.grand_average(evs) for cond, evs in all_subject_evokeds.items() if evs
    }
    if len(grand_avg_base) < 2:
        print("\n--- Not enough data for group plot. ---")
        return

    grand_avg_key = {
        key: mne.combine_evoked([grand_avg_base[bc] for bc in bcl if bc in grand_avg_base], 'equal')
        for key, bcl in KEY_CONDITIONS_MAP.items()
    }

    # Peak times group
    peak_times_grp = {}
    for cname, evoked in grand_avg_key.items():
        roi_data = evoked.get_data(picks=P1_ELECTRODES).mean(axis=0)
        info = mne.create_info(['ROI'], evoked.info['sfreq'], ch_types='eeg')
        roi_evoked = mne.EvokedArray(roi_data[np.newaxis, :], info, tmin=evoked.tmin)
        _, ptime = roi_evoked.get_peak(tmin=PEAK_TMIN, tmax=PEAK_TMAX, mode='pos')
        peak_times_grp[cname] = ptime

    fig_g = plt.figure(figsize=(10, 6))
    fig_g.suptitle('Grand Avg P1 Numbers Pair (Inc12 vs Dec21, ACC=1)', fontsize=14)
    gs_g = gridspec.GridSpec(2, 2, height_ratios=[2, 1.5])
    ax_erp_g = fig_g.add_subplot(gs_g[0, :])

    mne.viz.plot_compare_evokeds(
        grand_avg_key, picks=P1_ELECTRODES, combine='mean', axes=ax_erp_g,
        title='Grand Avg ERP Oz', show=False, legend='upper left', ci=0.95,
        colors=CONDITION_COLORS
    )

    for cname, ptime in peak_times_grp.items():
        ax_erp_g.axvline(x=ptime, color=CONDITION_COLORS[cname], linestyle='--', linewidth=1)

    for i, (cname, evoked) in enumerate(grand_avg_key.items()):
        ax_topo_g = fig_g.add_subplot(gs_g[1, i])
        scalp = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
        scalp.plot_topomap(times=peak_times_grp[cname], axes=ax_topo_g, show=False, vlim=(-6, 6), colorbar=False)
        ax_topo_g.set_title(f"{cname}\n{int(peak_times_grp[cname]*1000)} ms", color=CONDITION_COLORS[cname])

    fig_g.subplots_adjust(right=0.85, hspace=0.4)
    cbar_ax_g = fig_g.add_axes([0.88, 0.2, 0.02, 0.3])
    plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax_g, label='µV')

    out_grp = os.path.join(group_dir, 'group_' + script_name + '.png')
    if os.path.exists(out_grp):
        os.remove(out_grp)
    fig_g.savefig(out_grp, bbox_inches='tight'); plt.close(fig_g)
    print(f"  - Saved group P1 plot to {out_grp}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate P1 plots for Inc12 vs Dec21 (ACC=1)')
    parser.add_argument('--subjects', nargs='*', help='Specific subject IDs to process (default: all)')
    args = parser.parse_args()
    generate_p1_inc12_dec21_plots(args.subjects) 