// This file will contain the main JavaScript logic for the results page. 

document.addEventListener('DOMContentLoaded', () => {
    // Get references to the containers
    const plotsContainer = document.getElementById('plots-container');
    const tabsContainer = document.querySelector('.results-tabs');
    const comparisonControls = document.getElementById('comparison-controls');
    const compareBtn = document.getElementById('compare-btn');

    /* Floating compare bar */
    const floatingBar = document.createElement('div');
    floatingBar.id = 'compare-bar';
    floatingBar.className = 'compare-bar hidden';
    floatingBar.innerHTML = `
        <span id="compare-count">0 selected</span>
        <button id="floating-compare-btn">Compare Selected</button>
    `;
    const sidebarElement = document.querySelector('.sidebar');
    sidebarElement.appendChild(floatingBar);

    const floatingCompareBtn = document.getElementById('floating-compare-btn');

    function getSelectedPlotIds() {
        const ids = [];
        document.querySelectorAll('#comparison-controls input:checked').forEach(cb => ids.push(cb.dataset.plotId));
        return ids;
    }

    function updateFloatingBar() {
        const ids = getSelectedPlotIds();
        const countSpan = document.getElementById('compare-count');
        countSpan.textContent = `${ids.length} selected`;
        if (ids.length > 0) {
            floatingBar.classList.remove('hidden');
        } else {
            floatingBar.classList.add('hidden');
        }
    }

    // Listen for checkbox changes to update bar
    comparisonControls.addEventListener('change', (e) => {
        if (e.target.matches('input[type="checkbox"]')) {
            updateFloatingBar();
        }
    });

    function openComparison(ids) {
        if (ids.length > 0) {
            window.open(`comparison.html?plots=${ids.join(',')}`, '_blank');
        } else {
            alert('Please select at least one plot to compare.');
        }
    }

    // Hook buttons to comparison action
    compareBtn.addEventListener('click', () => openComparison(getSelectedPlotIds()));
    floatingCompareBtn.addEventListener('click', () => openComparison(getSelectedPlotIds()));

    // --- 1. DATA PROCESSING AND INITIALIZATION ---

    // Get unique categories from plotData to create tabs
    const categories = [...new Set(plotData.map(p => p.category))];

    // --- 2. DYNAMIC ELEMENT CREATION ---

    // Function to render plots for a given category
    function renderPlots(category) {
        plotsContainer.innerHTML = ''; // Clear existing plots
        const plotsToRender = plotData.filter(p => p.category === category);

        // Group plots by subcategory
        const plotsBySubcategory = plotsToRender.reduce((acc, plot) => {
            const key = plot.subcategory || 'General';
            if (!acc[key]) acc[key] = [];
            acc[key].push(plot);
            return acc;
        }, {});

        // Create HTML for each subcategory group
        for (const [subcategory, plots] of Object.entries(plotsBySubcategory)) {
            const section = document.createElement('section');
            if (subcategory !== 'General') {
                section.innerHTML = `<h3>${subcategory}</h3>`;
            }
            
            plots.forEach(plot => {
                const plotDiv = document.createElement('div');
                plotDiv.className = 'plot-container';
                plotDiv.id = plot.id;

                // Check if the plot type is 'text'
                if (plot.type === 'text') {
                    plotDiv.innerHTML = `<h4>${plot.name}</h4>`;
                    const pre = document.createElement('pre');
                    pre.className = 'text-content-container';
                    plotDiv.appendChild(pre);

                    // Fetch and display the text content
                    fetch(plot.path)
                        .then(response => response.text())
                        .then(text => pre.textContent = text)
                        .catch(err => pre.textContent = `Error loading content: ${err}`);

                } else {
                    // Default to image rendering
                    plotDiv.innerHTML = `<h4>${plot.name}</h4><img src="${plot.image}" alt="${plot.name}">`;
                }

                // Add the source script link if it exists
                if (plot.scriptUrl) {
                    const link = document.createElement('a');
                    link.href = plot.scriptUrl;
                    link.textContent = 'View Source Script';
                    link.className = 'source-script-link';
                    link.target = '_blank'; // Open in new tab
                    plotDiv.appendChild(link);
                }

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
            
            // Group plots by subcategory
            const plotsBySubcategory = plotsInCategory.reduce((acc, plot) => {
                const key = plot.subcategory || 'General';
                if (!acc[key]) acc[key] = [];
                acc[key].push(plot);
                return acc;
            }, {});

            for (const [subcategory, plots] of Object.entries(plotsBySubcategory)) {
                if (subcategory !== 'General') {
                    html += `<div class="sidebar-subcategory">${subcategory}</div>`;
                }
                plots.forEach(plot => {
                    html += `
                        <div class="checkbox-container">
                            <input type="checkbox" id="cb-${plot.id}" data-plot-id="${plot.id}">
                            <a href="#${plot.id}" class="jump-link">${plot.dataset} - ${plot.name}</a>
                        </div>`;
                });
            }
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

    // --- 4. INITIAL PAGE LOAD ---
    createTabs();
    createComparisonCheckboxes();
    renderPlots(categories[0]); // Render plots for the first category by default
}); 