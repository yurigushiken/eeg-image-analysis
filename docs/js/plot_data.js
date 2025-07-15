const plotData = [
    // Topomaps - ACC=1
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on Small (decreasing)',
        dataset: 'ACC=1',
        name: 'P1 (Decreasing)',
        id: 'acc1_p1_small_desc',
        image: 'images/group_p1_plot_landing_on_small_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_plot_landing_on_small_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on Small (decreasing)',
        dataset: 'ACC=1',
        name: 'N1 (Decreasing)',
        id: 'acc1_n1_small_desc',
        image: 'images/group_n1_plot_landing_on_small_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_plot_landing_on_small_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on Large (increasing)',
        dataset: 'ACC=1',
        name: 'P1 (Increasing)',
        id: 'acc1_p1_large_asc',
        image: 'images/group_p1_plot_landing_on_large_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_plot_landing_on_large_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on Large (increasing)',
        dataset: 'ACC=1',
        name: 'N1 (Increasing)',
        id: 'acc1_n1_large_asc',
        image: 'images/group_n1_plot_landing_on_large_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_plot_landing_on_large_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 1 (Decreasing)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land1_decreasing',
        image: 'images/group_p1_contrast_landing_on_1_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_1_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 1 (Decreasing)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land1_decreasing',
        image: 'images/group_n1_contrast_landing_on_1_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_1_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing Within Small Numbers',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_within_small',
        image: 'images/group_p1_plot_within_small_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_plot_within_small_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing Within Small Numbers',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_within_small',
        image: 'images/group_n1_plot_within_small_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_plot_within_small_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 2 (Decreasing)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land2_decreasing',
        image: 'images/group_p1_contrast_landing_on_2_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_2_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 2 (Decreasing)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land2_decreasing',
        image: 'images/group_n1_contrast_landing_on_2_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_2_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 2 (Any Preceding)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land2_any',
        image: 'images/group_p1_contrast_landing_on_2_any_preceding_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_2_any_preceding_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 2 (Any Preceding)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land2_any',
        image: 'images/group_n1_contrast_landing_on_2_any_preceding_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_2_any_preceding_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 3 (Decreasing)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land3_decreasing',
        image: 'images/group_p1_contrast_landing_on_3_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_3_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 3 (Decreasing)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land3_decreasing',
        image: 'images/group_n1_contrast_landing_on_3_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_3_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 3 (Any Preceding)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land3_any',
        image: 'images/group_p1_contrast_landing_on_3_any_preceding_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_3_any_preceding_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 3 (Any Preceding)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land3_any',
        image: 'images/group_n1_contrast_landing_on_3_any_preceding_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_3_any_preceding_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 2 (Increasing)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land2_increasing',
        image: 'images/group_p1_contrast_landing_on_2_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_2_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 2 (Increasing)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land2_increasing',
        image: 'images/group_n1_contrast_landing_on_2_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_2_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 3 (Increasing)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land3_increasing',
        image: 'images/group_p1_contrast_landing_on_3_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_3_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 3 (Increasing)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land3_increasing',
        image: 'images/group_n1_contrast_landing_on_3_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_3_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 4 (Decreasing)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land4_decreasing',
        image: 'images/group_p1_contrast_landing_on_4_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_4_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 4 (Decreasing)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land4_decreasing',
        image: 'images/group_n1_contrast_landing_on_4_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_4_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 4 (Any Preceding)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land4_any',
        image: 'images/group_p1_contrast_landing_on_4_any_preceding_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_4_any_preceding_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 4 (Any Preceding)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land4_any',
        image: 'images/group_n1_contrast_landing_on_4_any_preceding_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_4_any_preceding_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 4 (Increasing)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land4_increasing',
        image: 'images/group_p1_contrast_landing_on_4_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_4_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 4 (Increasing)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land4_increasing',
        image: 'images/group_n1_contrast_landing_on_4_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_4_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 5 (Decreasing)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land5_decreasing',
        image: 'images/group_p1_contrast_landing_on_5_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_5_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 5 (Decreasing)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land5_decreasing',
        image: 'images/group_n1_contrast_landing_on_5_decreasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_5_decreasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 5 (Any Preceding)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land5_any',
        image: 'images/group_p1_contrast_landing_on_5_any_preceding_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_5_any_preceding_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 5 (Any Preceding)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land5_any',
        image: 'images/group_n1_contrast_landing_on_5_any_preceding_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_5_any_preceding_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 5 (Increasing)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land5_increasing',
        image: 'images/group_p1_contrast_landing_on_5_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_5_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 5 (Increasing)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land5_increasing',
        image: 'images/group_n1_contrast_landing_on_5_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_5_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 6 (Any Preceding)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land6_any',
        image: 'images/group_p1_contrast_landing_on_6_any_preceding_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_6_any_preceding_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 6 (Any Preceding)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land6_any',
        image: 'images/group_n1_contrast_landing_on_6_any_preceding_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_6_any_preceding_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 6 (Increasing)',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_land6_increasing',
        image: 'images/group_p1_contrast_landing_on_6_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_landing_on_6_increasing_acc%3D1.py'
    },
    {
        category: 'Topomaps (ACC=1)',
        subcategory: 'Landing on 6 (Increasing)',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_land6_increasing',
        image: 'images/group_n1_contrast_landing_on_6_increasing_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_landing_on_6_increasing_acc%3D1.py'
    },
    // Topomaps - ALL
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on Small (decreasing)',
        dataset: 'ALL',
        name: 'P1 (Decreasing)',
        id: 'all_p1_small_desc',
        image: 'images/group_p1_plot_landing_on_small_decreasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_plot_landing_on_small_decreasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on Large (increasing)',
        dataset: 'ALL',
        name: 'P1 (Increasing)',
        id: 'all_p1_large_asc',
        image: 'images/group_p1_plot_landing_on_large_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_plot_landing_on_large_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on Large (increasing)',
        dataset: 'ALL',
        name: 'N1 (Increasing)',
        id: 'all_n1_large_asc',
        image: 'images/group_n1_plot_landing_on_large_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_plot_landing_on_large_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 1 (Any Preceding)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land1_any',
        image: 'images/group_p1_contrast_landing_on_1_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_1_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 1 (Any Preceding)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land1_any',
        image: 'images/group_n1_contrast_landing_on_1_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_1_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing Within Small Numbers',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_within_small',
        image: 'images/group_p1_plot_within_small_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_plot_within_small_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing Within Small Numbers',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_within_small',
        image: 'images/group_n1_plot_within_small_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_plot_within_small_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 2 (Decreasing)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land2_decreasing',
        image: 'images/group_p1_contrast_landing_on_2_decreasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_2_decreasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 2 (Decreasing)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land2_decreasing',
        image: 'images/group_n1_contrast_landing_on_2_decreasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_2_decreasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 2 (Any Preceding)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land2_any',
        image: 'images/group_p1_contrast_landing_on_2_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_2_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 2 (Any Preceding)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land2_any',
        image: 'images/group_n1_contrast_landing_on_2_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_2_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 3 (Decreasing)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land3_decreasing',
        image: 'images/group_p1_contrast_landing_on_3_decreasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_3_decreasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 3 (Decreasing)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land3_decreasing',
        image: 'images/group_n1_contrast_landing_on_3_decreasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_3_decreasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 3 (Any Preceding)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land3_any',
        image: 'images/group_p1_contrast_landing_on_3_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_3_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 3 (Any Preceding)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land3_any',
        image: 'images/group_n1_contrast_landing_on_3_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_3_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 2 (Increasing)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land2_increasing',
        image: 'images/group_p1_contrast_landing_on_2_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_2_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 2 (Increasing)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land2_increasing',
        image: 'images/group_n1_contrast_landing_on_2_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_2_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 3 (Increasing)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land3_increasing',
        image: 'images/group_p1_contrast_landing_on_3_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_3_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 3 (Increasing)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land3_increasing',
        image: 'images/group_n1_contrast_landing_on_3_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_3_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 4 (Decreasing)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land4_decreasing',
        image: 'images/group_p1_contrast_landing_on_4_decreasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_4_decreasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 4 (Decreasing)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land4_decreasing',
        image: 'images/group_n1_contrast_landing_on_4_decreasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_4_decreasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 4 (Any Preceding)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land4_any',
        image: 'images/group_p1_contrast_landing_on_4_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_4_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 4 (Any Preceding)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land4_any',
        image: 'images/group_n1_contrast_landing_on_4_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_4_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 4 (Increasing)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land4_increasing',
        image: 'images/group_p1_contrast_landing_on_4_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_4_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 4 (Increasing)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land4_increasing',
        image: 'images/group_n1_contrast_landing_on_4_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_4_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 5 (Decreasing)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land5_decreasing',
        image: 'images/group_p1_contrast_landing_on_5_decreasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_5_decreasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 5 (Decreasing)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land5_decreasing',
        image: 'images/group_n1_contrast_landing_on_5_decreasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_5_decreasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 5 (Any Preceding)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land5_any',
        image: 'images/group_p1_contrast_landing_on_5_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_5_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 5 (Any Preceding)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land5_any',
        image: 'images/group_n1_contrast_landing_on_5_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_5_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 5 (Increasing)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land5_increasing',
        image: 'images/group_p1_contrast_landing_on_5_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_5_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 5 (Increasing)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land5_increasing',
        image: 'images/group_n1_contrast_landing_on_5_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_5_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 6 (Any Preceding)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land6_any',
        image: 'images/group_p1_contrast_landing_on_6_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_6_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 6 (Any Preceding)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land6_any',
        image: 'images/group_n1_contrast_landing_on_6_any_preceding_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_6_any_preceding_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 6 (Increasing)',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_land6_increasing',
        image: 'images/group_p1_contrast_landing_on_6_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_landing_on_6_increasing_all.py'
    },
    {
        category: 'Topomaps (ALL)',
        subcategory: 'Landing on 6 (Increasing)',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_land6_increasing',
        image: 'images/group_n1_contrast_landing_on_6_increasing_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_landing_on_6_increasing_all.py'
    },
    // P1 vs N1 Analysis
    {
        category: 'P1 vs. N1 Analysis',
        dataset: 'ACC=1',
        name: 'P1-N1 Peak-to-Peak Amplitude',
        id: 'p1n1_p2p_plot',
        image: 'images/group_p1n1_p2p_plot.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/05_analysis_p1n1_p2p_landing_on_small.py'
    },
    {
        category: 'P1 vs. N1 Analysis',
        dataset: 'ACC=1',
        name: 'P1-N1 Peak-to-Peak Amplitude (POT ROI)',
        id: 'p1n1_p2p_pot_plot',
        image: 'images/group_p1n1_p2p_pot_roi_plot.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/05_analysis_p1n1_p2p_landing_on_small.py'
    },
    // Combined ANOVA summary text
    {
        category: 'P1 vs. N1 Analysis',
        dataset: 'ACC=1',
        name: 'ANOVA Summary: P1-N1 P2P (Oz & POT ROIs)',
        id: 'p1n1_p2p_anova_summary',
        type: 'text',
        path: 'results/group_p1n1_p2p_anova_summary.txt',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/05_analysis_p1n1_p2p_landing_on_small.py'
    },
    {
        category: 'P1 vs. N1 Analysis',
        dataset: 'ACC=1',
        name: 'ANCOVA Summary: N1 vs. P1',
        id: 'n1_ancova_summary',
        type: 'text',
        path: 'results/group_n1_ancova_summary.txt',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/05_analysis_n1_ancova_vs_p1_landing_on_small.py'
    },
    {
        category: 'P1 vs. N1 Analysis',
        dataset: 'ACC=1',
        name: 'P1-Normalized N1 Waveforms ("Flattening")',
        id: 'flattened_n1_plot',
        image: 'images/group_flattened_n1_plot.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/05_viz_flattened_n1_landing_on_small.py'
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
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'P1 Contrast (Decreasing) -1',
        id: 'all_p1_contrast_dec_minus_1',
        subcategory: 'P1 Contrast (Decreasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_p1_contrast_decreasing_minus_1_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_decreasing_minus_1_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'P1 Contrast (Decreasing) -2',
        id: 'all_p1_contrast_dec_minus_2',
        subcategory: 'P1 Contrast (Decreasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_p1_contrast_decreasing_minus_2_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_decreasing_minus_2_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'P1 Contrast (Decreasing) -3',
        id: 'all_p1_contrast_dec_minus_3',
        subcategory: 'P1 Contrast (Decreasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_p1_contrast_decreasing_minus_3_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_decreasing_minus_3_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'P1 Contrast (Increasing) +1',
        id: 'all_p1_contrast_inc_plus_1',
        subcategory: 'P1 Contrast (Increasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_p1_contrast_increasing_plus_1_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_increasing_plus_1_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'P1 Contrast (Increasing) +2',
        id: 'all_p1_contrast_inc_plus_2',
        subcategory: 'P1 Contrast (Increasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_p1_contrast_increasing_plus_2_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_increasing_plus_2_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'P1 Contrast (Increasing) +3',
        id: 'all_p1_contrast_inc_plus_3',
        subcategory: 'P1 Contrast (Increasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_p1_contrast_increasing_plus_3_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_contrast_increasing_plus_3_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'P1 Contrast (Decreasing) -1',
        id: 'acc1_p1_contrast_dec_minus_1',
        subcategory: 'P1 Contrast (Decreasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_p1_contrast_decreasing_minus_1_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_decreasing_minus_1_acc%3D1.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'P1 Contrast (Decreasing) -2',
        id: 'acc1_p1_contrast_dec_minus_2',
        subcategory: 'P1 Contrast (Decreasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_p1_contrast_decreasing_minus_2_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_decreasing_minus_2_acc%3D1.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'P1 Contrast (Decreasing) -3',
        id: 'acc1_p1_contrast_dec_minus_3',
        subcategory: 'P1 Contrast (Decreasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_p1_contrast_decreasing_minus_3_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_decreasing_minus_3_acc%3D1.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'P1 Contrast (Increasing) +1',
        id: 'acc1_p1_contrast_inc_plus_1',
        subcategory: 'P1 Contrast (Increasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_p1_contrast_increasing_plus_1_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_increasing_plus_1_acc%3D1.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'P1 Contrast (Increasing) +2',
        id: 'acc1_p1_contrast_inc_plus_2',
        subcategory: 'P1 Contrast (Increasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_p1_contrast_increasing_plus_2_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_increasing_plus_2_acc%3D1.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'P1 Contrast (Increasing) +3',
        id: 'acc1_p1_contrast_inc_plus_3',
        subcategory: 'P1 Contrast (Increasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_p1_contrast_increasing_plus_3_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_contrast_increasing_plus_3_acc%3D1.py'
    },
    // N1 Contrast Topomaps
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'N1 Contrast (Decreasing) -1',
        id: 'all_n1_contrast_dec_minus_1',
        subcategory: 'N1 Contrast (Decreasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_n1_contrast_decreasing_minus_1_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_decreasing_minus_1_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'N1 Contrast (Decreasing) -2',
        id: 'all_n1_contrast_dec_minus_2',
        subcategory: 'N1 Contrast (Decreasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_n1_contrast_decreasing_minus_2_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_decreasing_minus_2_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'N1 Contrast (Decreasing) -3',
        id: 'all_n1_contrast_dec_minus_3',
        subcategory: 'N1 Contrast (Decreasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_n1_contrast_decreasing_minus_3_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_decreasing_minus_3_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'N1 Contrast (Increasing) +1',
        id: 'all_n1_contrast_inc_plus_1',
        subcategory: 'N1 Contrast (Increasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_n1_contrast_increasing_plus_1_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_increasing_plus_1_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'N1 Contrast (Increasing) +2',
        id: 'all_n1_contrast_inc_plus_2',
        subcategory: 'N1 Contrast (Increasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_n1_contrast_increasing_plus_2_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_increasing_plus_2_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ALL',
        name: 'N1 Contrast (Increasing) +3',
        id: 'all_n1_contrast_inc_plus_3',
        subcategory: 'N1 Contrast (Increasing)',
        category: 'Topomaps (ALL)',
        image: 'images/group_03_generate_n1_contrast_increasing_plus_3_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_contrast_increasing_plus_3_all.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'N1 Contrast (Decreasing) -1',
        id: 'acc1_n1_contrast_dec_minus_1',
        subcategory: 'N1 Contrast (Decreasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_n1_contrast_decreasing_minus_1_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_decreasing_minus_1_acc%3D1.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'N1 Contrast (Decreasing) -2',
        id: 'acc1_n1_contrast_dec_minus_2',
        subcategory: 'N1 Contrast (Decreasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_n1_contrast_decreasing_minus_2_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_decreasing_minus_2_acc%3D1.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'N1 Contrast (Decreasing) -3',
        id: 'acc1_n1_contrast_dec_minus_3',
        subcategory: 'N1 Contrast (Decreasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_n1_contrast_decreasing_minus_3_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_decreasing_minus_3_acc%3D1.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'N1 Contrast (Increasing) +1',
        id: 'acc1_n1_contrast_inc_plus_1',
        subcategory: 'N1 Contrast (Increasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_n1_contrast_increasing_plus_1_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_increasing_plus_1_acc%3D1.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'N1 Contrast (Increasing) +2',
        id: 'acc1_n1_contrast_inc_plus_2',
        subcategory: 'N1 Contrast (Increasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_n1_contrast_increasing_plus_2_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_increasing_plus_2_acc%3D1.py'
    },
    {
        category: 'ERP Waveforms',
        dataset: 'ACC=1',
        name: 'N1 Contrast (Increasing) +3',
        id: 'acc1_n1_contrast_inc_plus_3',
        subcategory: 'N1 Contrast (Increasing)',
        category: 'Topomaps (ACC=1)',
        image: 'images/group_03_generate_n1_contrast_increasing_plus_3_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_contrast_increasing_plus_3_acc%3D1.py'
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
    },
    // Numbers Pair Analysis (ACC=1)
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '12 vs 21',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc12_vs_dec21',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc12_vs_dec21_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '12 vs 21',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc12_vs_dec21',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc12_vs_dec21_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '12 vs 21',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc12_vs_dec21',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc12_vs_dec21_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '13 vs 31',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc13_vs_dec31',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc13_vs_dec31_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '13 vs 31',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc13_vs_dec31',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc13_vs_dec31_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '13 vs 31',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc13_vs_dec31',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc13_vs_dec31_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '14 vs 41',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc14_vs_dec41',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc14_vs_dec41_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '14 vs 41',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc14_vs_dec41',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc14_vs_dec41_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '14 vs 41',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc14_vs_dec41',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc14_vs_dec41_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '23 vs 32',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc23_vs_dec32',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc23_vs_dec32_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '23 vs 32',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc23_vs_dec32',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc23_vs_dec32_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '23 vs 32',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc23_vs_dec32',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc23_vs_dec32_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '24 vs 42',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc24_vs_dec42',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc24_vs_dec42_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '24 vs 42',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc24_vs_dec42',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc24_vs_dec42_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '24 vs 42',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc24_vs_dec42',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc24_vs_dec42_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '25 vs 52',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc25_vs_dec52',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc25_vs_dec52_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '25 vs 52',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc25_vs_dec52',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc25_vs_dec52_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '25 vs 52',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc25_vs_dec52',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc25_vs_dec52_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '34 vs 43',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc34_vs_dec43',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc34_vs_dec43_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '34 vs 43',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc34_vs_dec43',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc34_vs_dec43_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '34 vs 43',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc34_vs_dec43',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc34_vs_dec43_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '35 vs 53',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc35_vs_dec53',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc35_vs_dec53_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '35 vs 53',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc35_vs_dec53',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc35_vs_dec53_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '35 vs 53',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc35_vs_dec53',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc35_vs_dec53_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '36 vs 63',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc36_vs_dec63',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc36_vs_dec63_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '36 vs 63',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc36_vs_dec63',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc36_vs_dec63_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '36 vs 63',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc36_vs_dec63',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc36_vs_dec63_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '45 vs 54',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc45_vs_dec54',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc45_vs_dec54_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '45 vs 54',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc45_vs_dec54',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc45_vs_dec54_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '45 vs 54',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc45_vs_dec54',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc45_vs_dec54_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '46 vs 64',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc46_vs_dec64',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc46_vs_dec64_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '46 vs 64',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc46_vs_dec64',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc46_vs_dec64_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '46 vs 64',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc46_vs_dec64',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc46_vs_dec64_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '56 vs 65',
        dataset: 'ACC=1',
        name: 'P1',
        id: 'acc1_p1_inc56_vs_dec65',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc56_vs_dec65_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '56 vs 65',
        dataset: 'ACC=1',
        name: 'N1',
        id: 'acc1_n1_inc56_vs_dec65',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc56_vs_dec65_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_n1_numbers_pair_plots_acc%3D1.py'
    },
    {
        category: 'Numbers Pair Analysis (ACC=1)',
        subcategory: '56 vs 65',
        dataset: 'ACC=1',
        name: 'P3B',
        id: 'acc1_p3b_inc56_vs_dec65',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc56_vs_dec65_acc=1.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_acc%3D1/code/03_generate_p3b_numbers_pair_plots_acc%3D1.py'
    },
    // Numbers Pair Analysis (ALL)
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '12 vs 21',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc12_vs_dec21',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc12_vs_dec21_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '12 vs 21',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc12_vs_dec21',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc12_vs_dec21_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '12 vs 21',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc12_vs_dec21',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc12_vs_dec21_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '13 vs 31',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc13_vs_dec31',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc13_vs_dec31_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '13 vs 31',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc13_vs_dec31',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc13_vs_dec31_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '13 vs 31',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc13_vs_dec31',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc13_vs_dec31_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '14 vs 41',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc14_vs_dec41',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc14_vs_dec41_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '14 vs 41',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc14_vs_dec41',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc14_vs_dec41_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '14 vs 41',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc14_vs_dec41',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc14_vs_dec41_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '23 vs 32',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc23_vs_dec32',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc23_vs_dec32_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '23 vs 32',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc23_vs_dec32',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc23_vs_dec32_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '23 vs 32',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc23_vs_dec32',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc23_vs_dec32_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '24 vs 42',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc24_vs_dec42',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc24_vs_dec42_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '24 vs 42',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc24_vs_dec42',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc24_vs_dec42_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '24 vs 42',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc24_vs_dec42',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc24_vs_dec42_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '25 vs 52',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc25_vs_dec52',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc25_vs_dec52_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '25 vs 52',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc25_vs_dec52',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc25_vs_dec52_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '25 vs 52',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc25_vs_dec52',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc25_vs_dec52_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '34 vs 43',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc34_vs_dec43',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc34_vs_dec43_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '34 vs 43',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc34_vs_dec43',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc34_vs_dec43_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '34 vs 43',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc34_vs_dec43',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc34_vs_dec43_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '35 vs 53',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc35_vs_dec53',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc35_vs_dec53_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '35 vs 53',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc35_vs_dec53',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc35_vs_dec53_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '35 vs 53',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc35_vs_dec53',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc35_vs_dec53_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '36 vs 63',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc36_vs_dec63',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc36_vs_dec63_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '36 vs 63',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc36_vs_dec63',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc36_vs_dec63_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '36 vs 63',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc36_vs_dec63',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc36_vs_dec63_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '45 vs 54',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc45_vs_dec54',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc45_vs_dec54_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '45 vs 54',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc45_vs_dec54',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc45_vs_dec54_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '45 vs 54',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc45_vs_dec54',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc45_vs_dec54_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '46 vs 64',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc46_vs_dec64',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc46_vs_dec64_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '46 vs 64',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc46_vs_dec64',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc46_vs_dec64_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '46 vs 64',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc46_vs_dec64',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc46_vs_dec64_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '56 vs 65',
        dataset: 'ALL',
        name: 'P1',
        id: 'all_p1_inc56_vs_dec65',
        image: 'images/group_03_generate_p1_numbers_pair_plot_inc56_vs_dec65_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '56 vs 65',
        dataset: 'ALL',
        name: 'N1',
        id: 'all_n1_inc56_vs_dec65',
        image: 'images/group_03_generate_n1_numbers_pair_plot_inc56_vs_dec65_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_n1_numbers_pair_plots_all.py'
    },
    {
        category: 'Numbers Pair Analysis (ALL)',
        subcategory: '56 vs 65',
        dataset: 'ALL',
        name: 'P3B',
        id: 'all_p3b_inc56_vs_dec65',
        image: 'images/group_03_generate_p3b_numbers_pair_plot_inc56_vs_dec65_all.png',
        scriptUrl: 'https://github.com/yurigushiken/eeg-image-analysis/blob/main/eeg_all/code/03_generate_p3b_numbers_pair_plots_all.py'
    }
]; 