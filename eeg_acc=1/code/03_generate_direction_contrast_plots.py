import mne
import os
import glob
import re
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION ---
CONDITION_PAIRS = {
    "1v2": ("12", "21"), "1v3": ("13", "31"), "1v4": ("14", "41"),
    "2v3": ("23", "32"), "2v4": ("24", "42"), "2v5": ("25", "52"),
    "3v4": ("34", "43"), "3v5": ("35", "53"), "3v6": ("36", "63"),
    "4v5": ("45", "54"), "4v6": ("46", "64"),
    "5v6": ("56", "65"),
}
DIRECTION_COLORS = {"inc": "#2ca02c", "dec": "#d62728"}
ELECTRODE_MONTAGES = {
    "LeftPOcc": ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70'],
    "RightPOcc": ['E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83'],
}
ELECTRODE_MONTAGES["GrandPOcc"] = ELECTRODE_MONTAGES["LeftPOcc"] + ELECTRODE_MONTAGES["RightPOcc"]

def generate_all_in_one():
    """
    Calculates grand average from scratch and generates ERP waveform plots.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    script_name = os.path.basename(__file__).replace('.py', '')

    # --- 1. FIND AND LOAD ALL SUBJECT DATA ---
    subject_dirs = sorted(glob.glob(os.path.join(derivatives_dir, 'sub-*')))
    if not subject_dirs:
        print("No subject directories found. Exiting.")
        return
    print(f"Found {len(subject_dirs)} subject directories. Starting data load.")

    all_subject_evokeds = {}
    for subject_dir in subject_dirs:
        subject_id = os.path.basename(subject_dir)
        try:
            all_files_in_dir = os.listdir(subject_dir)
            epoch_files = [os.path.join(subject_dir, f) for f in all_files_in_dir if f.endswith('_epo.fif')]
            for epoch_file in epoch_files:
                match = re.search(r'_cond-(\w+)_epo\.fif', epoch_file)
                if not match: continue
                cond = match.group(1)
                if cond not in all_subject_evokeds: all_subject_evokeds[cond] = []
                evoked = mne.read_epochs(epoch_file, preload=True, verbose=False).average()
                all_subject_evokeds[cond].append(evoked)
        except FileNotFoundError:
            print(f" - WARNING: Directory not found for {subject_id}. Skipping.")
            continue
    
    if not all_subject_evokeds:
        print("ERROR: No evoked data could be loaded. Cannot generate plots.")
        return
    
    # --- 2. COMPUTE GRAND AVERAGES IN MEMORY ---
    print("\nCalculating grand averages in memory...")
    grand_averages_dict = {}
    for cond, evk_list in all_subject_evokeds.items():
        if evk_list: grand_averages_dict[cond] = mne.grand_average(evk_list)

    if not grand_averages_dict:
        print("ERROR: Grand average calculation failed. No data.")
        return
    print(f"Successfully calculated {len(grand_averages_dict)} grand average conditions.")

    # --- 3. GENERATE AND SAVE PLOTS ---
    output_dir = os.path.join(derivatives_dir, 'group', 'figures', script_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nSaving plots to: {output_dir}")

    plot_count = 0
    for pair_name, (inc_cond, dec_cond) in CONDITION_PAIRS.items():
        if inc_cond not in grand_averages_dict or dec_cond not in grand_averages_dict:
            continue
        for montage_name, montage_picks in ELECTRODE_MONTAGES.items():
            inc_label, dec_label = f"INC{inc_cond}", f"DEC{dec_cond}"
            evokeds_to_compare = {inc_label: grand_averages_dict[inc_cond], dec_label: grand_averages_dict[dec_cond]}
            
            figs = mne.viz.plot_compare_evokeds(evokeds_to_compare, picks=montage_picks, combine='mean',
                title=f"{inc_label} vs. {dec_label} {montage_name} Montage (ACC=1)",
                show=False, legend='upper right', ci=False,
                colors={inc_label: DIRECTION_COLORS["inc"], dec_label: DIRECTION_COLORS["dec"]},
                styles={inc_label: {"linewidth": 1.5}, dec_label: {"linewidth": 1.5}})
            
            # Ensure figs is a list to handle all cases
            if not isinstance(figs, list):
                figs = [figs]

            # Save the figure(s)
            for i, fig in enumerate(figs):
                plot_filename = f"group_{inc_label}_vs_{dec_label}_{montage_name}.png"
                if len(figs) > 1:
                    plot_filename = f"group_{inc_label}_vs_{dec_label}_{montage_name}_{i}.png"
                fig.savefig(os.path.join(output_dir, plot_filename), dpi=150)
                plt.close(fig)
            
            plot_count += len(figs)

    print(f"\n--- Successfully generated {plot_count} plots. ---")

if __name__ == '__main__':
    generate_all_in_one() 