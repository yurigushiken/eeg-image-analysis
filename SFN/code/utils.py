import os
import glob
import yaml
import mne
import numpy as np
import matplotlib.pyplot as plt

# --- 1. SHARED CONSTANTS ---

# This dictionary holds all electrode selections for different ERP components.
# Verified from the ..._contrast_decreasing_minus_1_acc=1.py scripts.
ELECTRODE_GROUPS = {
    "N1": {
        "L": {
            "electrodes": ['E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70'],
            "description": "Left N1 Region"
        },
        "R": {
            "electrodes": ['E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83'],
            "description": "Right N1 Region"
        },
        "bilateral": {
            "electrodes": [
                'E66', 'E65', 'E59', 'E60', 'E67', 'E71', 'E70',
                'E84', 'E76', 'E77', 'E85', 'E91', 'E90', 'E83'
            ],
            "description": "Bilateral N1 Regions"
        }
    },
    "P1": {
        "Oz": {
            "electrodes": ['E71', 'E75', 'E76', 'E70', 'E83', 'E74', 'E81', 'E82'],
            "description": "Parieto-Occipital Region"
        }
    },
    "P3b": {
        "midline": {
            "electrodes": ['E62', 'E78', 'E77', 'E72', 'E67', 'E61', 'E54', 'E55', 'E79'],
            "description": "Centro-Parietal Region"
        }
    }
}

# Standardized color mapping for different experimental conditions.
# This can be expanded as more analyses are added.
CONDITION_COLORS = {
    # N1 Analysis Colors
    "Landing on 1 (from 2,3,4)": '#1f77b4',
    "Landing on 2 (from 3,4,5)": '#2ca02c',
    "Landing on 3 (from 4,5,6)": '#9467bd',
    # P1 Analysis Colors - Updated for high contrast
    "Landing on 1": '#1f77b4',  # Blue
    "Landing on 2": '#2ca02c',  # Green
    "Landing on 3": '#d62728',  # Red
    "Landing on 4": '#9467bd',  # Purple
    "Landing on 5": '#ff7f0e',  # Orange
    "Landing on 6": '#8c564b',  # Brown
    # Contrast Analysis Colors
    "2 to 1": '#e41a1c',
    "3 to 2": '#377eb8',
    "4 to 3": '#4daf4a',
    "5 to 4": '#984ea3',
    "6 to 5": '#ff7f00',
}

# A standard list of non-scalp channels to exclude from topographic plots.
NON_SCALP_CHANNELS = [
    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E43', 'E44', 'E48', 
    'E49', 'E113', 'E114', 'E119', 'E120', 'E121', 'E125', 'E126', 'E127', 'E128'
]

# Path to the electrode location file. Centralized for easy updating.
ELECTRODE_LOC_FILE = r"D:\numbers_eeg\assets\Channel Location - Net128_v1.sfp\AdultAverageNet128_v1.sfp"

# --- 2. HELPER FUNCTIONS ---

def load_config(config_path):
    """
    Loads a YAML configuration file.

    Args:
        config_path (str): The full path to the .yaml file.

    Returns:
        dict: The configuration parameters.
    """
    print(f"--- Loading configuration from: {config_path} ---")
    with open(config_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
            # The file is a list of analyses, so we take the first item.
            return config[0] 
        except yaml.YAMLError as e:
            print(f"Error loading YAML file: {e}")
            return None

def get_subject_list(derivatives_dir):
    """
    Finds all subject IDs in a given derivatives directory.

    Args:
        derivatives_dir (str): Path to the derivatives folder.

    Returns:
        list: A sorted list of subject ID strings.
    """
    subject_dirs = glob.glob(os.path.join(derivatives_dir, 'sub-*'))
    return sorted([os.path.basename(d).split('-')[1] for d in subject_dirs])

def save_figure(fig, analysis_name, output_dir):
    """
    Saves a Matplotlib figure with a standardized naming convention.

    Args:
        fig (matplotlib.figure.Figure): The figure object to save.
        analysis_name (str): The name of the analysis (from config).
        output_dir (str): The directory to save the figure in.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"group_{analysis_name}.png")
    fig.savefig(file_path, bbox_inches='tight')
    plt.close(fig)
    print(f"--- Saved final plot to: {file_path} ---")
