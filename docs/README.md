# Project Website Source

This directory contains the source files for the project's public-facing website, hosted via GitHub Pages.

**Live Site:** [https://yurigushiken.github.io/eeg-image-analysis/](https://yurigushiken.github.io/eeg-image-analysis/)

## Architecture Overview

The website has been redesigned as a dynamic, single-page application to provide a more interactive and seamless user experience. This architecture is powered by JavaScript and a centralized data source.

### Core Components

*   **`index.html`**: The main landing page of the website.
*   **`results.html`**: The primary hub for all visualizations. This page uses JavaScript to dynamically display different categories of plots (Topomaps, ERP Waveforms, LORETA) without requiring a full page reload.
*   **`comparison.html`**: A special page that generates a side-by-side comparison view of selected plots.
*   **`js/plot_data.js`**: The single source of truth for all plots displayed on the site. All plot information (category, name, image path, etc.) is stored here in a structured JavaScript array.
*   **`js/main.js`**: The core script that brings `results.html` to life. It reads data from `plot_data.js` to build the tabs, render the plots, and handle all user interactions like tab switching and plot comparison.
*   **`css/style.css`**: The stylesheet that defines the visual appearance of the entire website.
*   **`images/`**: The directory where all plot images are stored.

## How to Update the Website

### Adding or Modifying Plots

To add a new plot, remove an old one, or change a plot's title, you only need to edit **one file**:

1.  **Open `docs/js/plot_data.js`**.
2.  Find the `plotData` array.
3.  To add a new plot, copy an existing plot's object and paste it as a new item in the array. Then, update its properties (`category`, `dataset`, `name`, `id`, and `image`).
    *   `category`: Must match one of the existing tab names ('Topomaps', 'ERP Waveforms', 'LORETA') or be a new one (which will create a new tab).
    *   `dataset`: The group the plot belongs to (e.g., 'ACC=1', 'ALL', 'ds_all').
    *   `name`: The title of the plot.
    *   `id`: A unique identifier for the plot.
    *   `image`: The relative path to the image file from the `docs` directory (e.g., `images/my_new_plot.png`).
4.  To remove a plot, simply delete its corresponding object from the array.
5.  To change a plot's title or group, just edit the `name` or `dataset` properties.

The website will automatically reflect these changes once they are committed and pushed to the `main` branch.

## The Plot Comparison Feature

The website includes a powerful feature for comparing plots side-by-side:

1.  On the [Results](https://yurigushiken.github.io/eeg-image-analysis/results.html) page, the sidebar on the left lists all available plots.
2.  Click the checkbox next to any plot name to select it for comparison.
3.  Clicking the plot's text link will jump to that plot on the page, automatically switching tabs if necessary.
4.  Once you have selected two or more plots, click the "Compare Selected" button.
5.  A new browser tab will open displaying only the selected plots in a 2-column grid for easy comparison. 