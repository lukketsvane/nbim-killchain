/**
 * NBIM Kill Chain - Main Application Logic
 * Initializes Lucide icons and common UI components
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Add source tooltips
    document.querySelectorAll('[data-source]').forEach(el => {
        const sourceId = el.getAttribute('data-source');
        const source = nbimData.sources[sourceId];
        if (source) {
            el.title = `Kjelde: ${source.title}`;
            el.style.cursor = 'help';
            el.addEventListener('click', () => {
                window.open(source.url, '_blank');
            });
        }
    });

    console.log('NBIM Kill Chain v' + nbimData.meta.version + ' loaded');
});

/**
 * Generate company table HTML
 */
function renderCompanyTable(companies, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const rows = companies.map(c => `
        <tr>
            <td class="company-name">${c.name}</td>
            <td>${c.ticker}</td>
            <td class="text-right">${c.nbim_pct}%</td>
            <td class="text-right">${Utils.formatCurrency(c.value_usd)}</td>
            <td>${c.role}</td>
            <td>
                ${c.sources.map(s =>
                    `<a href="${nbimData.getSourceUrl(s)}" target="_blank" class="source-link">[${s}]</a>`
                ).join(' ')}
            </td>
        </tr>
    `).join('');

    container.innerHTML = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>Selskap</th>
                    <th>Ticker</th>
                    <th>NBIM %</th>
                    <th>Verdi (USD)</th>
                    <th>Rolle i Kill Chain</th>
                    <th>Kjelder</th>
                </tr>
            </thead>
            <tbody>${rows}</tbody>
        </table>
    `;
}

/**
 * Generate kill chain phase visualization
 */
function renderKillChainPhases(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const phases = Object.entries(nbimData.killChainSteps).map(([key, phase]) => {
        const companies = nbimData.getCompaniesByPhase(key);
        const total = nbimData.getStepTotal(key);

        return `
            <div class="phase-card" style="border-left: 4px solid ${phase.color}">
                <div class="phase-header">
                    <span class="phase-name">${phase.name}</span>
                    <span class="phase-ownership">${phase.ownershipRange}</span>
                </div>
                <div class="phase-description">${phase.description}</div>
                <div class="phase-total">${Utils.formatCurrency(total * 1000000)}</div>
                <div class="phase-companies">
                    ${companies.slice(0, 3).map(c => c.name).join(', ')}
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = phases;
}
