import os
import glob
import mne
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def analyze_small_number_trial_counts():
    """
    Scans the derivatives folder to count usable trials for conditions where
    both primed and target numbers are small (1-3), and generates a plot.
    """
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    except NameError:
        base_dir = os.path.abspath('eeg_acc=1')
        
    derivatives_dir = os.path.join(base_dir, 'derivatives')
    script_name = '00_check_small_number_trial_counts'
    output_dir = os.path.join(derivatives_dir, 'group', 'figures', script_name)
    os.makedirs(output_dir, exist_ok=True)

    print(f"--- Scanning for trial counts in: {derivatives_dir} ---")

    subject_dirs = sorted(glob.glob(os.path.join(derivatives_dir, 'sub-*')))
    if not subject_dirs:
        print("Error: No subject directories found.")
        return

    condition_counts = defaultdict(int)
    for subject_dir in subject_dirs:
        epoch_files = glob.glob(os.path.join(subject_dir, '*_epo.fif'))
        for epoch_file in epoch_files:
            try:
                filename = os.path.basename(epoch_file)
                condition = filename.split('cond-')[1].split('_')[0]
                epochs = mne.read_epochs(epoch_file, preload=False, verbose=False)
                condition_counts[condition] += len(epochs)
            except Exception as e:
                print(f"Could not process file {epoch_file}: {e}")

    if not condition_counts:
        print("Error: No condition epoch files found.")
        return

    # --- 2. Filter for small-to-small conditions and organize for plotting ---
    small_conditions = ['12', '13', '21', '23', '31', '32']
    small_conditions_only = {
        k: v for k, v in condition_counts.items() 
        if k in small_conditions
    }

    landing_on = {'1': defaultdict(int), '2': defaultdict(int), '3': defaultdict(int)}
    for condition, count in sorted(small_conditions_only.items()):
        target_num = condition[1]
        if target_num in landing_on:
            landing_on[target_num][condition] = count
            
    # --- 3. Print summary table ---
    print("\n--- Summary of Usable Trials (Small Numbers Only) ---")
    
    # By creating the DataFrame with a defined index, we ensure all rows appear
    df = pd.DataFrame(landing_on, index=small_conditions).fillna(0).astype(int)
    
    df = df.reindex(sorted(df.columns), axis=1)
    df.index.name = 'Condition (Primed -> Target)'
    df.columns.name = 'Landing On Number'
    df['Total Trials'] = df.sum(axis=1)
    df.loc['TOTAL'] = df.sum()
    print(df)

    # --- 4. Generate and save the plot ---
    # Drop the 'TOTAL' row before plotting and remove the 'Total Trials' column
    plot_df = df.drop('TOTAL').drop('Total Trials', axis=1)
    # Remove any other rows that might be all zeros, just in case
    plot_df = plot_df.loc[(plot_df.sum(axis=1) != 0)]

    fig, ax = plt.subplots(figsize=(10, 7))
    
    # --- Custom Color Theming Logic ---
    color_map_families = {'1': plt.cm.Blues, '2': plt.cm.Greens, '3': plt.cm.Reds}
    color_dict = {}
    for target_num_str, conditions_dict in landing_on.items():
        if not conditions_dict: continue
        colormap = color_map_families[target_num_str]
        num_conditions = len(conditions_dict)
        shades = [colormap(i) for i in np.linspace(0.4, 0.8, num_conditions)]
        for condition, color in zip(sorted(conditions_dict.keys()), shades):
            color_dict[condition] = color
    
    plot_order_conditions = plot_df.index
    final_colors = [color_dict.get(cond, 'black') for cond in plot_order_conditions]
    
    plot_df.T.plot(kind='bar', stacked=True, ax=ax, color=final_colors)
    
    ax.set_title('Total Usable Trial Counts for Small-to-Small Transitions (Dataset: acc=1)', fontsize=16)
    ax.set_xlabel('Target Number ("Landing On")', fontsize=12)
    ax.set_ylabel('Total Number of Usable Trials', fontsize=12)
    ax.tick_params(axis='x', rotation=0)
    ax.get_legend().remove()

    for i, total in enumerate(df.loc['TOTAL'].drop('Total Trials')):
        ax.text(i, total + 5, str(int(total)), ha='center', fontweight='bold')
        
    for container in ax.containers:
        condition_name = container.get_label()
        labels = [condition_name if v > 0 else '' for v in container.datavalues]
        ax.bar_label(container, labels=labels, label_type='center', color='white', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    
    fig_path = os.path.join(output_dir, f'{script_name}.png')
    plt.savefig(fig_path)
    plt.close(fig)
    
    print(f"\n--- Analysis complete. Plot saved to: {fig_path} ---")

if __name__ == '__main__':
    analyze_small_number_trial_counts() 