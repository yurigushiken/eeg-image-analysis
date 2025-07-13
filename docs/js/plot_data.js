
const plotData = [
    // Topomaps - ACC=1
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on Small (Preceding: 4, 5, 6)',
        dataset: 'ACC=1',
        name: 'N1 (Descending)',
        id: 'acc1_n1_small_desc',
        image: 'images/group_n1_plot_landing_on_small_descending_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_plot_landing_on_small_descending_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on Large (Preceding: 1, 2, 3)',
        dataset: 'ACC=1',
        name: 'N1 (Ascending)',
        id: 'acc1_n1_large_asc',
        image: 'images/group_n1_plot_landing_on_large_ascending_acc=1.png'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on Small (Preceding: 4, 5, 6)',
        dataset: 'ACC=1',
        name: 'P1 (Descending)',
        id: 'acc1_p1_small_desc',
        image: 'images/group_p1_plot_landing_on_small_descending_acc=1.png'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on Large (Preceding: 1, 2, 3)',
        dataset: 'ACC=1',
        name: 'P1 (Ascending)',
        id: 'acc1_p1_large_asc',
        image: 'images/group_p1_plot_landing_on_large_ascending_acc=1.png'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 1 (Contrast)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_contrast',
        image: 'images/group_n1_plot_landing_on_1_contrast_acc=1.png'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 1 (Contrast)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_contrast',
        image: 'images/group_p1_plot_landing_on_1_contrast_acc=1.png'
    },
    // Topomaps - ALL
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on Small (Preceding: 4, 5, 6)',
        dataset: 'ALL',
        name: 'N1 (Descending)',
        id: 'all_n1_small_desc',
        image: 'images/group_n1_plot_landing_on_small_descending_all.png'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on Large (Preceding: 1, 2, 3)',
        dataset: 'ALL',
        name: 'N1 (Ascending)',
        id: 'all_n1_large_asc',
        image: 'images/group_n1_plot_landing_on_large_ascending_all.png'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on Small (Preceding: 4, 5, 6)',
        dataset: 'ALL',
        name: 'P1 (Descending)',
        id: 'all_p1_small_desc',
        image: 'images/group_p1_plot_landing_on_small_descending_all.png'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on Large (Preceding: 1, 2, 3)',
        dataset: 'ALL',
        name: 'P1 (Ascending)',
        id: 'all_p1_large_asc',
        image: 'images/group_p1_plot_landing_on_large_ascending_all.png'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 1 (Contrast)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_contrast',
        image: 'images/group_n1_plot_landing_on_1_contrast_all.png'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 1 (Contrast)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_contrast',
        image: 'images/group_p1_plot_landing_on_1_contrast_all.png'
    },
    // P1 vs N1 Analysis
    {
        category: 'P1 vs. N1 Analysis',
        dataset: 'ACC=1',
        name: 'P1-N1 Peak-to-Peak Amplitude',
        id: 'p1n1_p2p_plot',
        image: 'images/group_p1n1_p2p_plot.png'
    },
    {
        category: 'P1 vs. N1 Analysis',
        dataset: 'ACC=1',
        name: 'ANCOVA Summary: N1 vs. P1',
        id: 'n1_ancova_summary',
        type: 'text',
        path: 'results/group_n1_ancova_summary.txt'
    },
    {
        category: 'P1 vs. N1 Analysis',
        dataset: 'ACC=1',
        name: 'P1-Normalized N1 Waveforms ("Flattening")',
        id: 'flattened_n1_plot',
        image: 'images/group_flattened_n1_plot.png'
    },
    // ERP Waveforms
    {
        category: 'ERP Waveforms',
        dataset: 'ds_all',
        name: 'Stimulus Comparison',
        id: 'stimulus_comparison',
        image: 'images/group_Stimulus_comparison.png'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ds_all',
        name: 'Interaction Comparison',
        id: 'interaction_comparison',
        image: 'images/group_Interaction_comparison.png'
    },
    // LORETA
    {
        category: 'LORETA',
        dataset: 'ds_all',
        name: 'LORETA Contrast: N1',
        id: 'loreta_n1',
        image: 'images/group_loreta_core_systems_contrast_N1.png'
    },
    {
        category: 'LORETA',
        dataset: 'ds_all',
        name: 'LORETA Contrast: P3b',
        id: 'loreta_p3b',
        image: 'images/group_loreta_core_systems_contrast_P3b.png'
    }
]; 