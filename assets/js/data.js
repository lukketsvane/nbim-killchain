/**
 * NBIM KILLCHAIN - CENTRAL DATA REPOSITORY
 * Single Source of Truth for all pages.
 * 
 * Updates here will reflect across Dashboard, Kill Chain view, and Company list.
 */

const nbimData = {
    meta: {
        lastUpdated: "2024-12-02",
        totalOperations: 52,
        source: "SEC Filings, Albanese Report, SIPRI, Leaked Contracts (Nimbus)"
    },
    
    // Kategoriar for Kill Chain
    killChainSteps: {
        find: {
            id: "01",
            name: "FIND",
            alias: "SURVEILLANCE & CLOUD",
            description: "Digital overvaking, datainnsamling og infrastruktur som muliggjør sanntids etterretning.",
            icon: "eye"
        },
        fix: {
            id: "02",
            name: "FIX",
            alias: "AI TARGETING",
            description: "AI-prosessering (Lavender/Gospel) for å identifisere og generere mål frå rådata.",
            icon: "cpu"
        },
        track: {
            id: "03",
            name: "TRACK",
            alias: "LOGISTICS & FUEL",
            description: "Fysisk forflytting, drivstoff til fly, og sensor-låsing på mål.",
            icon: "fuel"
        },
        target: {
            id: "04",
            name: "TARGET",
            alias: "C4ISR & LOCK-ON",
            description: "Kommando, kontroll og presisjonsstyring før angrep.",
            icon: "crosshair"
        },
        engage: {
            id: "05",
            name: "ENGAGE",
            alias: "KINETIC STRIKE",
            description: "Den fysiske øydelegginga. Bomber, flykroppar, artilleri og stridsvogner.",
            icon: "explosion"
        }
    },

    // KOMPLETT SELSKAPSLISTE (Basert på research)
    companies: [
        // --- DIGITAL / CLOUD (FIND/FIX) ---
        {
            name: "Alphabet Inc. (Google)",
            ticker: "GOOGL",
            step: "find",
            role: "Project Nimbus Cloud",
            description: "Leverer 'Project Nimbus' ($1.2mrd) skytjenester til IDF. Gir infrastruktur for AI-overvaking og datalagring. Kontrakten forbyr nekting av tjenester.",
            nbim_pct: 1.84,
            nbim_val_usd_m: 35000,
            flags: ["Project Nimbus", "AI Infrastructure"]
        },
        {
            name: "Microsoft",
            ticker: "MSFT",
            step: "find",
            role: "Azure Cloud / AI",
            description: "Integrert i IDFs digitale infrastruktur. Leverer OS og sky-løsninger som støtter militære operasjoner.",
            nbim_pct: 1.35,
            nbim_val_usd_m: 45000,
            flags: ["Cloud Infrastructure"]
        },
        {
            name: "Amazon",
            ticker: "AMZN",
            step: "find",
            role: "AWS Cloud (Nimbus)",
            description: "Partner i Project Nimbus. Leverer AWS-servere for lagring av massiv overvakingsdata.",
            nbim_pct: 1.13,
            nbim_val_usd_m: 22000,
            flags: ["Project Nimbus"]
        },
        {
            name: "Palantir Technologies",
            ticker: "PLTR",
            step: "fix",
            role: "AI Targeting Systems",
            description: "Inngikk strategisk partnerskap med IDF jan. 2024 for 'war-related missions'. Leverer analyseverktøy for målutvelgelse.",
            nbim_pct: 1.03,
            nbim_val_usd_m: 3307,
            flags: ["Strategic Partnership 2024", "AI Targeting"]
        },
        {
            name: "NVIDIA",
            ticker: "NVDA",
            step: "fix",
            role: "AI Hardware",
            description: "Leverer GPU-ene som trener og kjører IDFs AI-modeller (Lavender/Gospel).",
            nbim_pct: 1.10,
            nbim_val_usd_m: 28000, // Estimat basert på portefølje
            flags: ["AI Hardware"]
        },

        // --- LOGISTICS / TRACK (TRACK) ---
        {
            name: "Valero Energy",
            ticker: "VLO",
            step: "track",
            role: "Military Jet Fuel (JP-8)",
            description: "Hovedleverandør av JP-8 flybensin fra Texas til Israel. Fyller F-35 og Apache-helikoptre. NBIM kjøpte seg opp i 2025.",
            nbim_pct: 1.98,
            nbim_val_usd_m: 827,
            flags: ["Jet Fuel Supplier", "Increased Stake"]
        },
        {
            name: "Volvo Group",
            ticker: "VOLV-B",
            step: "track",
            role: "Heavy Transport",
            description: "Leverer tungtransport og lastebiler brukt til logistikk og troppeforflytning.",
            nbim_pct: 2.02,
            nbim_val_usd_m: 1000,
            flags: ["Logistics"]
        },
        {
            name: "Caterpillar",
            ticker: "CAT",
            step: "track",
            role: "D9 Bulldozers",
            description: "Produserer D9-bulldoserne som brukes til riving av sivil infrastruktur og baning av vei for bakkestyrker.",
            nbim_pct: 1.29,
            nbim_val_usd_m: 2372,
            flags: ["Demolition", "Ground Invasion"]
        },
        {
            name: "HD Hyundai",
            ticker: "267250",
            step: "track",
            role: "Excavators",
            description: "Leverer gravemaskiner brukt i militære ingeniøroperasjoner.",
            nbim_pct: 1.54,
            nbim_val_usd_m: 500,
            flags: ["Engineering"]
        },

        // --- KINETIC / ENGAGE (ENGAGE/TARGET) ---
        {
            name: "Lockheed Martin",
            ticker: "LMT",
            step: "engage",
            role: "F-35I / F-16I Platform",
            description: "Produserer hovedplattformene for luftangrep (F-35, F-16) og Hellfire-missiler.",
            nbim_pct: 1.14,
            nbim_val_usd_m: 4210,
            flags: ["Primary Platform"]
        },
        {
            name: "Boeing",
            ticker: "BA",
            step: "engage",
            role: "F-15I / JDAM Munitions",
            description: "Leverer F-15 jagerfly, Apache-helikoptre og JDAM-halekits som gjør 'dumme' bomber smarte.",
            nbim_pct: 1.60,
            nbim_val_usd_m: 1733,
            flags: ["Munitions", "Aircraft"]
        },
        {
            name: "General Dynamics",
            ticker: "GD",
            step: "engage",
            role: "MK84 Bomb Bodies",
            description: "Produserer selve bomben (MK80-serien) som fylles med eksplosiver. Leveranser godkjent 2024/25.",
            nbim_pct: 1.15,
            nbim_val_usd_m: 928,
            flags: ["Bomb Bodies", "Artillery"]
        },
        {
            name: "Rheinmetall",
            ticker: "RHM",
            step: "engage",
            role: "155mm Artillery",
            description: "Tysk gigant. Leverer 120mm stridsvogn-ammunisjon og 155mm artillerigranater.",
            nbim_pct: 1.88,
            nbim_val_usd_m: 420,
            flags: ["Artillery", "Tank Ammo"]
        },
        {
            name: "Northrop Grumman",
            ticker: "NOC",
            step: "target",
            role: "F-35 Radar / Sensors",
            description: "Leverer AN/APG-81 radaren til F-35 og sensorsystemer for mållåsing.",
            nbim_pct: 1.38,
            nbim_val_usd_m: 1003,
            flags: ["Sensors"]
        },
        {
            name: "Raytheon (RTX)",
            ticker: "RTX",
            step: "engage",
            role: "Paveway / Iron Dome",
            description: "Produserer laserstyrte Paveway-bomber og interceptorer til Iron Dome.",
            nbim_pct: 1.26,
            nbim_val_usd_m: 2120,
            flags: ["Guided Munitions"]
        },
        {
            name: "Leonardo",
            ticker: "LDO",
            step: "target",
            role: "Naval Guns / Electronics",
            description: "Leverer 76mm kanoner til israelske korvetter som beskyter kysten av Gaza.",
            nbim_pct: 1.10,
            nbim_val_usd_m: 180, // Estimat
            flags: ["Naval"]
        },
        {
            name: "BAE Systems",
            ticker: "BA",
            step: "engage",
            role: "M109 Artillery Components",
            description: "Leverer komponenter til howitzers og marinekanoner.",
            nbim_pct: 1.97,
            nbim_val_usd_m: 2005,
            flags: ["Components"]
        },
        {
            name: "L3Harris",
            ticker: "LHX",
            step: "target",
            role: "Comms & Bomb Racks",
            description: "Leverer bombemekanismer til F-35.",
            nbim_pct: 1.35,
            nbim_val_usd_m: 616,
            flags: ["Components"]
        }
    ],

    // Hjelpefunksjonar for å hente data
    getStats: function() {
        const totalVal = this.companies.reduce((acc, curr) => acc + curr.nbim_val_usd_m, 0);
        const avgStake = this.companies.reduce((acc, curr) => acc + curr.nbim_pct, 0) / this.companies.length;
        
        return {
            totalValueUsd: totalVal,
            totalValueNok: totalVal * 11, // Ca kurs
            avgStake: avgStake.toFixed(2),
            companyCount: this.companies.length
        };
    },

    getCompaniesByStep: function(stepId) {
        return this.companies.filter(c => c.step === stepId).sort((a, b) => b.nbim_val_usd_m - a.nbim_val_usd_m);
    },

    getStepTotal: function(stepId) {
        return this.companies
            .filter(c => c.step === stepId)
            .reduce((acc, curr) => acc + curr.nbim_val_usd_m, 0);
    }
};

// Export for browser
if (typeof window !== 'undefined') {
    window.nbimData = nbimData;
}
