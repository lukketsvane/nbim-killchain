/**
 * Main JavaScript for NBIM Kill Chain
 * Handles shared logic like formatting, navigation rendering, and icon initialization.
 */

const Utils = {
    formatCurrency: (valueUSD) => {
        if (valueUSD >= 1000) {
            return `$${(valueUSD / 1000).toFixed(1)} MRD`;
        }
        return `$${valueUSD} M`;
    },

    formatNOK: (valueUSD) => {
        const nok = valueUSD * 11; // Approx exchange rate
        if (nok >= 1000) {
            return `${(nok / 1000).toFixed(0)} MRD NOK`;
        }
        return `${nok.toFixed(0)} M NOK`;
    },

    renderNavigation: (activePage) => {
        const navContainer = document.getElementById('nav-container');
        if (!navContainer) return;

        const pages = [
            { id: 'index', label: 'DASHBOARD', url: 'index.html' },
            { id: 'killchain', label: 'KILL CHAIN', url: 'killchain.html' },
            { id: 'companies', label: 'SELSKAPSLISTE', url: 'companies.html' }
        ];

        let html = '<div class="tab-group">';
        pages.forEach(page => {
            const isActive = activePage === page.id ? 'active' : '';
            html += `<a href="${page.url}" class="tab-btn ${isActive}">${page.label}</a>`;
        });
        html += '</div>';

        navContainer.innerHTML = html;
    },

    initIcons: () => {
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Utils.initIcons();
});
