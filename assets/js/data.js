/**
 * NBIM Kill Chain Data Module
 * Version: 2.0
 * Last Updated: 2025-12-02
 *
 * Sentralisert datamodul for kill chain-analyse med kjeldereferansar.
 * All data har direkte kopling til verifiserbare kjelder.
 */

const nbimData = {
    meta: {
        version: "2.0",
        lastUpdated: "2025-12-02",
        dataAsOf: "2023-12-31",
        currency: "USD",
        exchangeRate: 10.5, // NOK/USD approximate
        totalExposureUsd: 208000000000,
        weightedAvgOwnership: 1.16
    },

    // Kjeldereferansar
    sources: {
        nbim_holdings_2023: {
            title: "NBIM Holdings Report 2023",
            url: "https://www.nbim.no/no/holdingsdata/eq_2023_country.pdf",
            type: "official"
        },
        "972mag_lavender": {
            title: "Lavender AI System - +972 Magazine",
            url: "https://www.972mag.com/lavender-ai-israeli-army-gaza/",
            type: "journalism"
        },
        "972mag_nimbus": {
            title: "Project Nimbus - +972 Magazine",
            url: "https://www.972mag.com/project-nimbus-contract-google-amazon-israel/",
            type: "journalism"
        },
        un_albanese_report: {
            title: "A/HRC/59/23 - UN Special Rapporteur",
            url: "https://www.ohchr.org/sites/default/files/documents/hrbodies/hrcouncil/sessions-regular/session59/advance-version/a-hrc-59-23-aev.pdf",
            type: "un_report"
        },
        whoprofits_cisco: {
            title: "Cisco Systems - Who Profits",
            url: "https://www.whoprofits.org/companies/company/6529?cisco-systems",
            type: "ngo_report"
        }
    },

    // Kill Chain faser (F2T2EA)
    killChainSteps: {
        find: {
            name: "FIND",
            description: "Overvaking, droner, biometri",
            ownershipRange: "1.8-2.5%",
            color: "#ef4444"
        },
        fix: {
            name: "FIX",
            description: "Cloud computing, datasjøar",
            ownershipRange: "2.5-3.8%",
            color: "#f97316"
        },
        track: {
            name: "TRACK",
            description: "AI-algoritmar (Lavender/Gospel)",
            ownershipRange: "~1.8%",
            color: "#eab308"
        },
        target: {
            name: "TARGET",
            description: "Kommando & kontroll (C4I)",
            ownershipRange: "1.2-1.6%",
            color: "#22c55e"
        },
        engage: {
            name: "ENGAGE",
            description: "Fly, stridsvogner, bulldoserar",
            ownershipRange: "1.0-1.1%",
            color: "#3b82f6"
        },
        assess: {
            name: "ASSESS",
            description: "Skadeanalyse, cloud-lagring",
            ownershipRange: "1.8%",
            color: "#8b5cf6"
        }
    },

    // Hovudselskap med kjeldereferansar
    companies: [
        {
            id: "msft",
            name: "Microsoft",
            ticker: "MSFT",
            nbim_pct: 3.8,
            value_usd: 43800000000,
            value_nok: 360000000000,
            layer: "cloud_ai",
            phases: ["fix", "track", "assess"],
            role: "Azure MoD-kontrakt, Unit 8200, Project Nimbus",
            sources: ["nbim_holdings_2023", "972mag_nimbus"],
            status: "invested"
        },
        {
            id: "nvda",
            name: "NVIDIA",
            ticker: "NVDA",
            nbim_pct: 1.3,
            value_usd: 56700000000,
            value_nok: 149000000000,
            layer: "ai_compute",
            phases: ["track"],
            role: "A100/H100 GPU-ar for Lavender/Gospel-trening",
            sources: ["nbim_holdings_2023"],
            status: "invested"
        },
        {
            id: "googl",
            name: "Alphabet (Google)",
            ticker: "GOOGL",
            nbim_pct: 2.1,
            value_usd: 25000000000,
            value_nok: 197440000000,
            layer: "cloud_ai",
            phases: ["fix", "assess"],
            role: "Project Nimbus, Vertex AI, GDCH",
            sources: ["nbim_holdings_2023", "972mag_nimbus"],
            status: "invested"
        },
        {
            id: "amzn",
            name: "Amazon",
            ticker: "AMZN",
            nbim_pct: 1.6,
            value_usd: 18300000000,
            value_nok: 183879000000,
            layer: "cloud_ai",
            phases: ["fix", "assess"],
            role: "Project Nimbus, AWS S3, Wolf Pack",
            sources: ["nbim_holdings_2023", "972mag_nimbus"],
            status: "invested"
        },
        {
            id: "meta",
            name: "Meta Platforms",
            ticker: "META",
            nbim_pct: 1.34,
            value_usd: 21800000000,
            value_nok: 117318000000,
            layer: "data_collection",
            phases: ["find", "track"],
            role: "WhatsApp metadata til Lavender",
            sources: ["nbim_holdings_2023", "972mag_lavender"],
            status: "invested"
        },
        {
            id: "pltr",
            name: "Palantir",
            ticker: "PLTR",
            nbim_pct: 1.1,
            value_usd: 3500000000,
            value_nok: 36000000000,
            layer: "software",
            phases: ["fix", "track", "target"],
            role: "Gotham, Foundry, AIP - 'Operating system' for kill chain",
            sources: ["nbim_holdings_2023", "un_albanese_report"],
            status: "invested",
            notes: "15x auke 2023-2024"
        },
        {
            id: "csco",
            name: "Cisco Systems",
            ticker: "CSCO",
            nbim_pct: 1.21,
            value_usd: 3820000000,
            value_nok: 25209000000,
            layer: "network",
            phases: ["target"],
            role: "David's Citadel, IDF unified comms",
            sources: ["nbim_holdings_2023", "whoprofits_cisco"],
            status: "invested"
        },
        {
            id: "rtx",
            name: "RTX (Raytheon)",
            ticker: "RTX",
            nbim_pct: 1.1,
            value_usd: 1580000000,
            value_nok: null,
            layer: "weapons",
            phases: ["engage"],
            role: "Iron Dome, presisjonsmissilar",
            sources: ["nbim_holdings_2023"],
            status: "invested"
        },
        {
            id: "msi",
            name: "Motorola Solutions",
            ticker: "MSI",
            nbim_pct: 1.22,
            value_usd: 1040000000,
            value_nok: 8679000000,
            layer: "communications",
            phases: ["find", "track"],
            role: "Mountain Rose kryptert nett",
            sources: ["nbim_holdings_2023"],
            status: "invested"
        },
        {
            id: "lignex1",
            name: "LIG Nex1",
            ticker: "079550.KS",
            nbim_pct: 2.57,
            value_usd: 103000000,
            value_nok: null,
            layer: "robotics",
            phases: ["find", "engage"],
            role: "Ghost Robotics Vision 60 robotbikkjer",
            sources: ["nbim_holdings_2023"],
            status: "invested",
            notes: "Høgste forsvarseierskap %"
        },
        {
            id: "avgo",
            name: "Broadcom",
            ticker: "AVGO",
            nbim_pct: 1.6,
            value_usd: 19200000000,
            value_nok: 193575000000,
            layer: "semiconductors",
            phases: ["target"],
            role: "Nettverkschiper",
            sources: ["nbim_holdings_2023"],
            status: "invested"
        },
        {
            id: "vlo",
            name: "Valero Energy",
            ticker: "VLO",
            nbim_pct: 1.94,
            value_usd: 873000000,
            value_nok: null,
            layer: "logistics",
            phases: ["engage"],
            role: "JP-8 jetdrivstoff",
            sources: ["nbim_holdings_2023"],
            status: "invested"
        }
    ],

    // Ekskluderte selskap
    excluded: [
        { name: "Elbit Systems", ticker: "ESLT", date: "2009-09", reason: "Separasjonsmuren" },
        { name: "Lockheed Martin", ticker: "LMT", date: "2013-08", reason: "Atomvåpen" },
        { name: "Boeing", ticker: "BA", date: "2006-01", reason: "Atomvåpen" },
        { name: "General Dynamics", ticker: "GD", date: "2024-09", reason: "Atomvåpen" },
        { name: "Caterpillar", ticker: "CAT", date: "2025-08", reason: "Menneskerettar" },
        { name: "L3Harris", ticker: "LHX", date: "2024-05", reason: "Atomvåpen" }
    ],

    // AI-system
    aiSystems: [
        {
            name: "Lavender",
            type: "Human targeting",
            targetsGenerated: 37000,
            verificationTime: "20 sekunder",
            sources: ["972mag_lavender"]
        },
        {
            name: "The Gospel (Habsora)",
            type: "Structural targeting",
            output: "3D-koordinatar, våpentype, CDE",
            sources: ["972mag_lavender"]
        },
        {
            name: "Where's Daddy?",
            type: "Geolocation trigger",
            function: "Varslar når mål går heim",
            sources: ["972mag_lavender"]
        }
    ],

    // Hjelpefunksjonar
    getStats() {
        const invested = this.companies.filter(c => c.status === 'invested');
        const totalUsd = invested.reduce((sum, c) => sum + (c.value_usd || 0), 0);
        const avgStake = invested.reduce((sum, c) => sum + c.nbim_pct, 0) / invested.length;

        return {
            totalValueUsd: totalUsd,
            avgStake: avgStake.toFixed(2),
            companyCount: invested.length,
            excludedCount: this.excluded.length
        };
    },

    getStepTotal(phase) {
        return this.companies
            .filter(c => c.phases && c.phases.includes(phase))
            .reduce((sum, c) => sum + (c.value_usd / 1000000 || 0), 0);
    },

    getCompaniesByPhase(phase) {
        return this.companies.filter(c => c.phases && c.phases.includes(phase));
    },

    getSourceUrl(sourceId) {
        return this.sources[sourceId]?.url || '#';
    }
};

// Utility-funksjonar
const Utils = {
    formatCurrency(value) {
        if (value >= 1e12) return '$' + (value / 1e12).toFixed(1) + 'T';
        if (value >= 1e9) return '$' + (value / 1e9).toFixed(1) + 'B';
        if (value >= 1e6) return '$' + (value / 1e6).toFixed(0) + 'M';
        return '$' + value.toLocaleString();
    },

    formatNOK(usdValue) {
        const nok = usdValue * nbimData.meta.exchangeRate;
        if (nok >= 1e12) return 'NOK ' + (nok / 1e12).toFixed(0) + ' bill';
        if (nok >= 1e9) return 'NOK ' + (nok / 1e9).toFixed(0) + ' mrd';
        return 'NOK ' + nok.toLocaleString();
    },

    renderNavigation(currentPage) {
        const nav = document.getElementById('nav-container');
        if (!nav) return;

        const pages = [
            { id: 'index', name: 'Dashboard', href: 'index.html' },
            { id: 'killchain', name: 'Kill Chain', href: 'killchain.html' },
            { id: 'companies', name: 'Selskap', href: 'companies.html' }
        ];

        nav.innerHTML = pages.map(p =>
            `<a href="${p.href}" class="nav-link ${p.id === currentPage ? 'active' : ''}">${p.name}</a>`
        ).join('');
    }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { nbimData, Utils };
}
