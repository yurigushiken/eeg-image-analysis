// This file will contain the main JavaScript logic for the results page. 

document.addEventListener('DOMContentLoaded', () => {
    // Get references to the containers
    const plotsContainer = document.getElementById('plots-container');
    const tabsContainer = document.querySelector('.results-tabs');
    const comparisonControls = document.getElementById('comparison-controls');
    const compareBtn = document.getElementById('compare-btn');

    // --- 1. DATA PROCESSING AND INITIALIZATION ---

    // Get unique categories from plotData to create tabs
    const categories = [...new Set(plotData.map(p => p.category))];

    // --- 2. DYNAMIC ELEMENT CREATION ---

    // Function to render plots for a given category
    function renderPlots(category) {
        plotsContainer.innerHTML = ''; // Clear existing plots
        const plotsToRender = plotData.filter(p => p.category === category);

        // Group plots by dataset (e.g., ACC=1, ALL)
        const plotsByDataset = plotsToRender.reduce((acc, plot) => {
            const key = plot.dataset || 'General';
            if (!acc[key]) acc[key] = [];
            acc[key].push(plot);
            return acc;
        }, {});

        // Create HTML for each dataset group
        for (const [dataset, plots] of Object.entries(plotsByDataset)) {
            const section = document.createElement('section');
            section.innerHTML = `<h3>${dataset}</h3>`;
            
            plots.forEach(plot => {
                const plotDiv = document.createElement('div');
                plotDiv.className = 'plot-container';
                plotDiv.id = plot.id;
                plotDiv.innerHTML = `<h4>${plot.name}</h4><img src="${plot.image}" alt="${plot.name}">`;
                section.appendChild(plotDiv);
            });
            plotsContainer.appendChild(section);
        }
    }

    // Function to create tab buttons
    function createTabs() {
        categories.forEach((category, index) => {
            const tab = document.createElement('button');
            tab.className = 'tab-link';
            if (index === 0) tab.classList.add('active'); // Set first tab as active
            tab.textContent = category;
            tab.dataset.category = category;
            tabsContainer.appendChild(tab);
        });
    }

    // Function to create checkboxes for comparison
    function createComparisonCheckboxes() {
        let html = '';
        categories.forEach(category => {
            html += `<div class="sidebar-category"><strong>${category}</strong></div>`;
            const plotsInCategory = plotData.filter(p => p.category === category);
            plotsInCategory.forEach(plot => {
                html += `
                    <div class="checkbox-container">
                        <input type="checkbox" id="cb-${plot.id}" data-plot-id="${plot.id}">
                        <a href="#${plot.id}" class="jump-link">${plot.dataset} - ${plot.name}</a>
                    </div>`;
            });
        });
        comparisonControls.innerHTML = html;
    }

    // --- 3. EVENT LISTENERS ---

    // Event listener for jump-to links to enable cross-tab jumping
    comparisonControls.addEventListener('click', (e) => {
        if (e.target.classList.contains('jump-link')) {
            e.preventDefault(); // Prevent default anchor behavior

            const plotId = e.target.hash.substring(1);
            const targetPlot = plotData.find(p => p.id === plotId);
            if (!targetPlot) return;

            // Check if the plot is in the currently active tab
            const activeTab = tabsContainer.querySelector('.tab-link.active');
            if (activeTab.dataset.category !== targetPlot.category) {
                // If not, find the correct tab and click it
                const targetTab = tabsContainer.querySelector(`.tab-link[data-category="${targetPlot.category}"]`);
                if (targetTab) {
                    targetTab.click(); // This triggers the renderPlots function
                }
            }
            
            // The plot's element should now be in the DOM.
            // We use a small timeout to ensure the DOM has updated before we scroll.
            setTimeout(() => {
                const elementToScrollTo = document.getElementById(plotId);
                if (elementToScrollTo) {
                    elementToScrollTo.scrollIntoView({ behavior: 'smooth' });
                }
            }, 50);
        }
    });

    // Event listener for tab clicks
    tabsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('tab-link')) {
            // Update active tab style
            tabsContainer.querySelector('.active').classList.remove('active');
            e.target.classList.add('active');
            // Render plots for the selected category
            renderPlots(e.target.dataset.category);
        }
    });

    // Event listener for the compare button
    compareBtn.addEventListener('click', () => {
        const selectedIds = [];
        document.querySelectorAll('#comparison-controls input:checked').forEach(checkbox => {
            selectedIds.push(checkbox.dataset.plotId);
        });

        if (selectedIds.length > 0) {
            const url = `comparison.html?plots=${selectedIds.join(',')}`;
            window.open(url, '_blank');
        } else {
            alert('Please select at least one plot to compare.');
        }
    });

    // --- 4. INITIAL PAGE LOAD ---
    createTabs();
    createComparisonCheckboxes();
    renderPlots(categories[0]); // Render plots for the first category by default
}); 