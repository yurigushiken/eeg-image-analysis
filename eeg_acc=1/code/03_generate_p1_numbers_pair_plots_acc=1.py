import mne
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# --- 1. CONFIGURATION ---
NUMBER_PAIRS = [
    ("12", "21"), ("13", "31"), ("14", "41"),
    ("23", "32"), ("24", "42"), ("25", "52"),
    ("34", "43"), ("35", "53"), ("36", "63"),
    ("45", "54"), ("46", "64"), ("56", "65")
]

CONDITION_COLORS = {
    'inc': '#1f77b4',
    'dec': '#e41a1c',
}

P1_ELECTRODES = ['E71', 'E75', 'E76', 'E70', 'E83', 'E74', 'E81', 'E82']
PEAK_TMIN, PEAK_TMAX = 0.080, 0.130
NON_SCALP_CHANNELS = [
    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E43', 'E44', 'E48',
    'E49', 'E113', 'E114', 'E119', 'E120', 'E121', 'E125', 'E126', 'E127', 'E128'
]

def generate_p1_pair_plots():
    base_dir = "eeg_acc=1"
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    subject_dirs = sorted(glob.glob(os.path.join(derivatives_dir, 'sub-*')))
    subjects_to_process = [os.path.basename(d).split('-')[1] for d in subject_dirs]

    for inc_cond, dec_cond in NUMBER_PAIRS:
        print(f"\n--- Generating P1 group plot for {inc_cond} vs {dec_cond} (ACC=1) ---")
        
        all_subject_evokeds = {inc_cond: [], dec_cond: []}

        for subject_id in subjects_to_process:
            subject_dir = os.path.join(derivatives_dir, f"sub-{subject_id}")
            try:
                inc_epo_path = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{inc_cond}_epo.fif')
                dec_epo_path = os.path.join(subject_dir, f'sub-{subject_id}_task-numbers_cond-{dec_cond}_epo.fif')

                if os.path.exists(inc_epo_path):
                    all_subject_evokeds[inc_cond].append(mne.read_epochs(inc_epo_path, preload=True, verbose=False).average())
                if os.path.exists(dec_epo_path):
                    all_subject_evokeds[dec_cond].append(mne.read_epochs(dec_epo_path, preload=True, verbose=False).average())
            except Exception as e:
                print(f"  - Error processing subject {subject_id} for pair {inc_cond}/{dec_cond}: {e}")
        
        grand_averages_base = {cond: mne.grand_average(evoked_list) for cond, evoked_list in all_subject_evokeds.items() if evoked_list}
        
        if len(grand_averages_base) < 2:
            print(f"  - Insufficient data for pair {inc_cond} vs {dec_cond}. Skipping plot.")
            continue

        inc_pair_str = f"{inc_cond[0]} to {inc_cond[1]}"
        dec_pair_str = f"{dec_cond[0]} to {dec_cond[1]}"
        grand_averages_key = {
            f'{inc_pair_str} (Inc)': grand_averages_base[inc_cond],
            f'{dec_pair_str} (Dec)': grand_averages_base[dec_cond]
        }
        
        script_name = f"03_generate_p1_numbers_pair_plot_inc{inc_cond}_vs_dec{dec_cond}_acc=1"
        group_figure_dir = os.path.join(derivatives_dir, 'group', 'figures', script_name)
        os.makedirs(group_figure_dir, exist_ok=True)
        
        fig_grp = plt.figure(figsize=(10, 8))
        fig_grp.suptitle(f'Grand Average: P1 ({inc_pair_str} vs {dec_pair_str}, ACC=1)', fontsize=16)
        gs_grp = gridspec.GridSpec(2, 2, height_ratios=[2, 1.5])
        ax_erp_grp = fig_grp.add_subplot(gs_grp[0, :])

        plot_colors = {
            f'{inc_pair_str} (Inc)': CONDITION_COLORS['inc'],
            f'{dec_pair_str} (Dec)': CONDITION_COLORS['dec']
        }
        mne.viz.plot_compare_evokeds(
            grand_averages_key, picks=P1_ELECTRODES, combine='mean', axes=ax_erp_grp,
            title='Grand Average Mean ERP over Oz Region', show=False, legend='upper left', ci=0.95,
            colors=plot_colors
        )
        
        peak_times_grp = {}
        for i, (cond_name, evoked) in enumerate(grand_averages_key.items()):
            try:
                roi_data = evoked.get_data(picks=P1_ELECTRODES).mean(axis=0)
                info = mne.create_info(['ROI'], evoked.info['sfreq'], ch_types='eeg')
                roi_evoked = mne.EvokedArray(roi_data[np.newaxis, :], info, tmin=evoked.tmin)
                _, peak_time = roi_evoked.get_peak(tmin=PEAK_TMIN, tmax=PEAK_TMAX, mode='pos')
                peak_times_grp[cond_name] = peak_time
            except ValueError:
                peak_times_grp[cond_name] = (PEAK_TMIN + PEAK_TMAX) / 2

            ax_topo_grp = fig_grp.add_subplot(gs_grp[1, i])
            plot_time = peak_times_grp[cond_name]
            title_text = f"{cond_name}\n{int(plot_time*1000)} ms"
            color = CONDITION_COLORS['inc'] if '(Inc)' in cond_name else CONDITION_COLORS['dec']
            ax_erp_grp.axvline(x=plot_time, color=color, linestyle='--', linewidth=1.5, alpha=0.8)
            scalp_evoked = evoked.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
            scalp_evoked.plot_topomap(times=plot_time, axes=ax_topo_grp, show=False, vlim=(-6, 6), colorbar=False)
            ax_topo_grp.set_title(title_text, color=color)

        fig_grp.subplots_adjust(right=0.85, bottom=0.1, top=0.9, hspace=0.4)
        cbar_ax_g = fig_grp.add_axes([0.88, 0.15, 0.02, 0.2])
        plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6, vmax=6), cmap='RdBu_r'), cax=cbar_ax_g, label='µV')
        
        grp_fig_path = os.path.join(group_figure_dir, f'group_{script_name}.png')
        fig_grp.savefig(grp_fig_path, bbox_inches='tight')
        plt.close(fig_grp)
        print(f"  - Saved group P1 plot to {grp_fig_path}")

if __name__ == '__main__':
    generate_p1_pair_plots()