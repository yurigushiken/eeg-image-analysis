# Script to copy datasets to the lab shared drive, excluding figures directories.

# Define source and destination paths
$source_base_path = "D:\numbers_eeg"
$destination_base_path = "D:\numbers_eeg\FOR-LAB-SHARED-DRIVE"

# Define dataset directories to copy
$datasets = @(
    "eeg_acc=1",
    "eeg_all",
    "eeg_ds_acc=1",
    "eeg_ds_all"
)

# Create the destination directory if it doesn't exist
if (-not (Test-Path -Path $destination_base_path -PathType Container)) {
    New-Item -ItemType Directory -Path $destination_base_path
}

# Loop through each dataset and copy it
foreach ($dataset in $datasets) {
    $source_dir = Join-Path -Path $source_base_path -ChildPath $dataset
    $destination_dir = Join-Path -Path $destination_base_path -ChildPath $dataset

    Write-Host "Copying $source_dir to $destination_dir (excluding figures)..."
    
    # robocopy <Source> <Destination> [File[ ...]] [Options]
    # /E :: copy subdirectories, including Empty ones.
    # /XD :: eXclude Directories matching given names/paths.
    robocopy $source_dir $destination_dir /E /XD figures
}

Write-Host "All datasets copied successfully." 