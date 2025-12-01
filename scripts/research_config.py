"""
NBIM Kill Chain Research Configuration
=====================================
Konfigurasjon for automatisert research og datainnsamling.
Bruk dette som grunnlag for parallelle research-agentar.

Versjon: 2.0
Sist oppdatert: 2025-12-02
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class SourceType(Enum):
    OFFICIAL = "official"           # NBIM, SEC, regjeringen.no
    UN_REPORT = "un_report"         # FN-rapportar
    JOURNALISM = "journalism"        # +972, Guardian, Intercept
    NGO_REPORT = "ngo_report"        # Who Profits, Amnesty, HRW
    CORPORATE = "corporate"          # Selskapsdokumentasjon
    ACADEMIC = "academic"            # Akademiske kjelder

class KillChainPhase(Enum):
    FIND = "find"       # Collection, surveillance
    FIX = "fix"         # Processing, cloud
    TRACK = "track"     # AI targeting
    TARGET = "target"   # C4I, authorization
    ENGAGE = "engage"   # Kinetic action
    ASSESS = "assess"   # BDA, analytics

@dataclass
class ResearchQuery:
    """Definerer ein research-oppgåve"""
    id: str
    description: str
    keywords: List[str]
    target_sources: List[SourceType]
    kill_chain_phase: Optional[KillChainPhase]
    priority: int  # 1-5, 1 = høgast

# Primære research-oppgåver for parallelle agentar
RESEARCH_QUERIES = [
    # EIGARSKAPSDATA
    ResearchQuery(
        id="nbim_holdings_update",
        description="Hent oppdaterte NBIM eigarskapsdata for alle kill chain-selskap",
        keywords=["NBIM holdings", "Government Pension Fund Global", "equity holdings"],
        target_sources=[SourceType.OFFICIAL],
        kill_chain_phase=None,
        priority=1
    ),
    ResearchQuery(
        id="sec_13f_filings",
        description="Verifiser NBIM aksjeposisjonar via SEC 13F-filings",
        keywords=["SEC 13F", "Norges Bank", "institutional holdings"],
        target_sources=[SourceType.OFFICIAL],
        kill_chain_phase=None,
        priority=1
    ),

    # PROJECT NIMBUS
    ResearchQuery(
        id="nimbus_contract_details",
        description="Detaljar om Project Nimbus-kontrakten og militær bruk",
        keywords=["Project Nimbus", "Google Israel", "AWS Israel", "IDF cloud"],
        target_sources=[SourceType.JOURNALISM, SourceType.NGO_REPORT],
        kill_chain_phase=KillChainPhase.FIX,
        priority=1
    ),

    # AI TARGETING SYSTEMS
    ResearchQuery(
        id="lavender_technical",
        description="Tekniske detaljar om Lavender AI-systemet",
        keywords=["Lavender AI", "IDF targeting", "machine learning Gaza"],
        target_sources=[SourceType.JOURNALISM, SourceType.ACADEMIC],
        kill_chain_phase=KillChainPhase.TRACK,
        priority=1
    ),
    ResearchQuery(
        id="gospel_system",
        description="The Gospel (Habsora) strukturell målgenerering",
        keywords=["Gospel Habsora", "AI targeting buildings", "Unit 8200"],
        target_sources=[SourceType.JOURNALISM],
        kill_chain_phase=KillChainPhase.TRACK,
        priority=2
    ),

    # PALANTIR
    ResearchQuery(
        id="palantir_idf_partnership",
        description="Palantir strategisk partnarskap med IDF",
        keywords=["Palantir Israel", "Gotham IDF", "AIP military"],
        target_sources=[SourceType.JOURNALISM, SourceType.CORPORATE],
        kill_chain_phase=KillChainPhase.TARGET,
        priority=1
    ),

    # BIOMETRIC SURVEILLANCE
    ResearchQuery(
        id="wolf_pack_systems",
        description="Wolf Pack biometriske overvakingssystem",
        keywords=["Blue Wolf", "Red Wolf", "Wolf Pack database", "facial recognition Gaza"],
        target_sources=[SourceType.NGO_REPORT, SourceType.JOURNALISM],
        kill_chain_phase=KillChainPhase.FIND,
        priority=2
    ),

    # NETWORK INFRASTRUCTURE
    ResearchQuery(
        id="cisco_idf_infrastructure",
        description="Cisco nettverksinfrastruktur for IDF",
        keywords=["Cisco IDF", "David's Citadel", "Israel Rises platform"],
        target_sources=[SourceType.NGO_REPORT],
        kill_chain_phase=KillChainPhase.TARGET,
        priority=2
    ),
    ResearchQuery(
        id="motorola_mountain_rose",
        description="Motorola Mountain Rose kryptert kommunikasjon",
        keywords=["Mountain Rose", "Vered Harim", "Motorola IDF", "encrypted cellular"],
        target_sources=[SourceType.NGO_REPORT],
        kill_chain_phase=KillChainPhase.FIND,
        priority=2
    ),

    # ROBOTICS
    ResearchQuery(
        id="ghost_robotics_gaza",
        description="Ghost Robotics Vision 60 i Gaza-tunnellar",
        keywords=["Ghost Robotics", "Vision 60", "LIG Nex1", "robot dog Gaza"],
        target_sources=[SourceType.JOURNALISM],
        kill_chain_phase=KillChainPhase.FIND,
        priority=2
    ),

    # EXCLUSIONS
    ResearchQuery(
        id="nbim_exclusion_decisions",
        description="NBIM eksklusjonsbeslutningar og grunngjeving",
        keywords=["NBIM exclusion", "Council on Ethics", "divestment Israel"],
        target_sources=[SourceType.OFFICIAL],
        kill_chain_phase=None,
        priority=1
    ),

    # SUPPLY CHAIN
    ResearchQuery(
        id="semiconductor_supply_chain",
        description="Halvleiar-forsyningskjede til IDF-system",
        keywords=["NVIDIA Israel", "Intel Mobileye", "chip supply IDF"],
        target_sources=[SourceType.JOURNALISM, SourceType.CORPORATE],
        kill_chain_phase=KillChainPhase.TRACK,
        priority=3
    ),

    # FUEL/LOGISTICS
    ResearchQuery(
        id="jet_fuel_supply",
        description="Drivstoffleveransar til IDF luftoperasjonar",
        keywords=["JP-8 Israel", "jet fuel IDF", "Valero Israel"],
        target_sources=[SourceType.JOURNALISM],
        kill_chain_phase=KillChainPhase.ENGAGE,
        priority=3
    ),

    # FN-RAPPORTAR
    ResearchQuery(
        id="un_albanese_companies",
        description="Selskap identifisert i Albanese-rapporten A/HRC/59/23",
        keywords=["Albanese report", "A/HRC/59/23", "corporate complicity genocide"],
        target_sources=[SourceType.UN_REPORT],
        kill_chain_phase=None,
        priority=1
    ),

    # COMPARATIVE
    ResearchQuery(
        id="storebrand_divestments",
        description="Storebrand/KLP divesterings-beslutningar for samanlikning",
        keywords=["Storebrand Palantir", "KLP divestment", "Norwegian investors Israel"],
        target_sources=[SourceType.JOURNALISM],
        kill_chain_phase=None,
        priority=2
    )
]

# API-endepunkt for automatisert datainnsamling
DATA_SOURCES = {
    "nbim_holdings": {
        "base_url": "https://www.nbim.no/hr/report/",
        "params": {"category": "eq", "sortby": "country", "filetype": "xlsx"},
        "update_frequency": "quarterly"
    },
    "sec_edgar": {
        "base_url": "https://www.sec.gov/cgi-bin/browse-edgar",
        "params": {"action": "getcompany", "company": "norges bank", "type": "13F"},
        "update_frequency": "quarterly"
    }
}

# Selskap som treng oppdatert research
COMPANIES_TO_TRACK = [
    "MSFT", "NVDA", "GOOGL", "AMZN", "META", "PLTR",
    "CSCO", "IBM", "RTX", "AVGO", "MSI", "079550.KS",
    "APH", "VLO", "INTC", "GE", "DELL", "HPQ", "HPE"
]

def get_priority_queries(max_priority: int = 2) -> List[ResearchQuery]:
    """Hent research-oppgåver med prioritet <= max_priority"""
    return [q for q in RESEARCH_QUERIES if q.priority <= max_priority]

def get_queries_by_phase(phase: KillChainPhase) -> List[ResearchQuery]:
    """Hent alle research-oppgåver for ein gitt kill chain-fase"""
    return [q for q in RESEARCH_QUERIES if q.kill_chain_phase == phase]

def export_research_plan(filename: str = "research_plan.json"):
    """Eksporter research-plan til JSON for agent-bruk"""
    plan = {
        "meta": {
            "version": "2.0",
            "generated": "2025-12-02",
            "total_queries": len(RESEARCH_QUERIES)
        },
        "queries": [
            {
                "id": q.id,
                "description": q.description,
                "keywords": q.keywords,
                "sources": [s.value for s in q.target_sources],
                "phase": q.kill_chain_phase.value if q.kill_chain_phase else None,
                "priority": q.priority
            }
            for q in RESEARCH_QUERIES
        ],
        "companies": COMPANIES_TO_TRACK,
        "data_sources": DATA_SOURCES
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    print(f"Research plan eksportert til {filename}")
    return plan

if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(script_dir), "data")
    output_path = os.path.join(data_dir, "research_plan.json")

    # Eksporter research-plan
    plan = export_research_plan(output_path)

    print(f"\n=== NBIM Kill Chain Research Plan ===")
    print(f"Totalt {len(RESEARCH_QUERIES)} research-oppgåver")
    print(f"Prioritet 1: {len(get_priority_queries(1))} oppgåver")
    print(f"Prioritet 1-2: {len(get_priority_queries(2))} oppgåver")
    print(f"\nSelskap å spore: {len(COMPANIES_TO_TRACK)}")
