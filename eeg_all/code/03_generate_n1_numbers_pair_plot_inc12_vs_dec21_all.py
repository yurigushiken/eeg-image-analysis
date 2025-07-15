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
    '1 to 2 (Inc)': '#1f77b4',
    '2 to 1 (Dec)': '#e41a1c',
}

N1_ELECTRODES = ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70', 'E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83']
PEAK_TMIN, PEAK_TMAX = 0.080, 0.200

NON_SCALP_CHANNELS = [
    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E43', 'E44', 'E48',
    'E49', 'E113', 'E114', 'E119', 'E120', 'E121', 'E125', 'E126', 'E127', 'E128'
]

def generate_n1_plots(subjects_to_process):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    script_name = os.path.basename(__file__).replace('.py', '')

    all_sub_evokeds = {c: [] for c in BASE_CONDITIONS}

    if not subjects_to_process:
        subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
        subjects_to_process = sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

    print(f"--- N1 numbers pair ALL: processing {subjects_to_process} ---")

    for sid in subjects_to_process:
        sdir = os.path.join(derivatives_dir, f'sub-{sid}')
        fig_dir = os.path.join(sdir, 'figures', script_name)
        os.makedirs(fig_dir, exist_ok=True)
        try:
            base_evks = {
                cond: mne.read_epochs(os.path.join(sdir, f'sub-{sid}_task-numbers_cond-{cond}_epo.fif'), preload=True, verbose=False).average()
                for cond in BASE_CONDITIONS if os.path.exists(os.path.join(sdir, f'sub-{sid}_task-numbers_cond-{cond}_epo.fif'))
            }
            for cond, evk in base_evks.items():
                all_sub_evokeds[cond].append(evk)
            if len(base_evks) < 2:
                continue
            key_evks = {k: mne.combine_evoked([base_evks[bc] for bc in bcl if bc in base_evks], 'equal') for k, bcl in KEY_CONDITIONS_MAP.items()}
            peak_times = {}
            for cname, evk in key_evks.items():
                try:
                    roi = evk.get_data(picks=N1_ELECTRODES).mean(axis=0)
                    info = mne.create_info(['ROI'], evk.info['sfreq'], ch_types='eeg')
                    roi_evk = mne.EvokedArray(roi[np.newaxis, :], info, tmin=evk.tmin)
                    _, pt, _ = roi_evk.get_peak(tmin=PEAK_TMIN, tmax=PEAK_TMAX, mode='neg', return_amplitude=True)
                    peak_times[cname] = pt
                except ValueError:
                    peak_times[cname] = None
            fig = plt.figure(figsize=(10,6))
            fig.suptitle(f'Sub-{sid}: N1 Numbers Pair (Inc12 vs Dec21, ALL)', fontsize=14)
            gs = gridspec.GridSpec(2,2, height_ratios=[2,1.5])
            ax_erp = fig.add_subplot(gs[0,:])
            mne.viz.plot_compare_evokeds(key_evks, picks=N1_ELECTRODES, combine='mean', axes=ax_erp, show=False, legend='upper left', ci=False, colors=CONDITION_COLORS, title="Mean ERP")
            for cname, pt in peak_times.items():
                if pt is not None:
                    ax_erp.axvline(x=pt, color=CONDITION_COLORS[cname], linestyle='--', linewidth=1)
            for i,(cname, evk) in enumerate(key_evks.items()):
                ax_topo = fig.add_subplot(gs[1,i])
                peak_time = peak_times.get(cname)
                if peak_time is not None:
                    scalp = evk.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
                    scalp.plot_topomap(times=peak_time, axes=ax_topo, show=False, vlim=(-6, 6), colorbar=False)
                    ax_topo.set_title(f"{cname}\n{int(peak_time * 1000)} ms", color=CONDITION_COLORS[cname])
                else:
                    ax_topo.set_title(f"{cname}\nPeak not found", color=CONDITION_COLORS[cname])
                    ax_topo.axis('off')
            fig.subplots_adjust(right=0.85, hspace=0.4)
            cax = fig.add_axes([0.88,0.2,0.02,0.3])
            plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6,vmax=6), cmap='RdBu_r'), cax=cax, label='µV')
            out_png = os.path.join(fig_dir, f'sub-{sid}_{script_name}.png')
            if os.path.exists(out_png): os.remove(out_png)
            fig.savefig(out_png, bbox_inches='tight'); plt.close(fig)
        except Exception as e:
            print(f"Subject {sid} FAILED: {e}")

    # group
    g_dir = os.path.join(derivatives_dir,'group','figures',script_name)
    os.makedirs(g_dir, exist_ok=True)
    g_base = {c: mne.grand_average(evs) for c,evs in all_sub_evokeds.items() if evs}
    if len(g_base)<2:
        print('Not enough data for group'); return
    g_key = {k: mne.combine_evoked([g_base[bc] for bc in bcl if bc in g_base], 'equal') for k,bcl in KEY_CONDITIONS_MAP.items()}
    peak_g = {}
    for cname, evk in g_key.items():
        try:
            roi = evk.get_data(picks=N1_ELECTRODES).mean(axis=0)
            info=mne.create_info(['ROI'], evk.info['sfreq'], ch_types='eeg')
            roi_evk=mne.EvokedArray(roi[np.newaxis,:], info, tmin=evk.tmin)
            _, pt, _ = roi_evk.get_peak(tmin=PEAK_TMIN, tmax=PEAK_TMAX, mode='neg', return_amplitude=True)
            peak_g[cname]=pt
        except ValueError:
            peak_g[cname] = None
    fig=plt.figure(figsize=(10,6))
    fig.suptitle('Grand Avg N1 Numbers Pair (Inc12 vs Dec21, ALL)', fontsize=14)
    gs=gridspec.GridSpec(2,2, height_ratios=[2,1.5])
    ax=fig.add_subplot(gs[0,:])
    mne.viz.plot_compare_evokeds(g_key, picks=N1_ELECTRODES, combine='mean', axes=ax, show=False, legend='upper left', ci=0.95, colors=CONDITION_COLORS, title="Grand Average ERP")
    for cname, pt in peak_g.items():
        if pt is not None:
            ax.axvline(x=pt, color=CONDITION_COLORS[cname], linestyle='--', linewidth=1)
    for i,(cname, evk) in enumerate(g_key.items()):
        ax_topo=fig.add_subplot(gs[1,i])
        peak_time = peak_g.get(cname)
        if peak_time is not None:
            scalp=evk.copy().pick('eeg', exclude=NON_SCALP_CHANNELS)
            scalp.plot_topomap(times=peak_time, axes=ax_topo, show=False, vlim=(-6,6), colorbar=False)
            ax_topo.set_title(f"{cname}\n{int(peak_time*1000)} ms", color=CONDITION_COLORS[cname])
        else:
            ax_topo.set_title(f"{cname}\nPeak not found",color=CONDITION_COLORS[cname])
            ax_topo.axis('off')
    fig.subplots_adjust(right=0.85, hspace=0.4)
    caxg=fig.add_axes([0.88,0.2,0.02,0.3])
    plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin=-6,vmax=6), cmap='RdBu_r'), cax=caxg, label='µV')
    out_grp=os.path.join(g_dir, 'group_'+script_name+'.png')
    if os.path.exists(out_grp): os.remove(out_grp)
    fig.savefig(out_grp, bbox_inches='tight'); plt.close(fig)
    print('Saved group N1 ALL plot to', out_grp)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Generate N1 numbers pair plots (ALL)')
    parser.add_argument('--subjects', nargs='*')
    args=parser.parse_args()
    generate_n1_plots(args.subjects) 