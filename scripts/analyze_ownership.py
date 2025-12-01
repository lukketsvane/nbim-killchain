#!/usr/bin/env python3
"""
IDF Kill Chain Ownership Analysis
Analyser eigarskapsstruktur i militær infrastruktur
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Paths
DATA_DIR = Path(__file__).parent.parent / 'data'
OUTPUT_DIR = Path(__file__).parent.parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

def load_data():
    """Last inn alle CSV-filer"""
    data = {}
    data['systems'] = pd.read_csv(DATA_DIR / 'military_systems.csv')
    data['manufacturers'] = pd.read_csv(DATA_DIR / 'manufacturers.csv')
    data['shareholders'] = pd.read_csv(DATA_DIR / 'major_shareholders.csv')
    data['ownership'] = pd.read_csv(DATA_DIR / 'ownership_stakes.csv')
    data['components'] = pd.read_csv(DATA_DIR / 'system_components.csv')
    data['infrastructure'] = pd.read_csv(DATA_DIR / 'infrastructure_ownership_analysis.csv')
    data['operations'] = pd.read_csv(DATA_DIR / 'gaza_operations_data.csv')
    return data

def calculate_total_ownership_by_system(data):
    """
    Berekn kva investor eig kor mykje av kvart våpensystem
    basert på komponentnivå
    """
    components = data['components']
    ownership = data['ownership']

    # Merge komponenter med eigarskap
    component_ownership = components.merge(
        ownership,
        on='manufacturer_id',
        how='left',
        suffixes=('_comp', '_own')
    )

    # Berekn eigarskapsandel for kvar komponent
    component_ownership['component_ownership_value'] = (
        component_ownership['estimated_value_per_unit_usd_millions'] *
        component_ownership['ownership_percentage'] / 100
    )

    # Aggreger per system og investor
    system_ownership = component_ownership.groupby(
        ['system_id', 'system_name_comp', 'shareholder_name']
    ).agg({
        'component_ownership_value': 'sum',
        'estimated_value_per_unit_usd_millions': 'sum'
    }).reset_index()

    # Berekn prosentandel eigarskap i systemet
    system_ownership['system_ownership_pct'] = (
        system_ownership['component_ownership_value'] /
        system_ownership['estimated_value_per_unit_usd_millions'] * 100
    )

    system_ownership = system_ownership.rename(columns={
        'system_name_comp': 'system_name',
        'estimated_value_per_unit_usd_millions': 'total_system_value_usd_millions'
    })

    return system_ownership

def calculate_munitions_used_by_investor(data):
    """
    Berekn kor mange våpen brukt i Gaza som kan tilskrivast kvar investor
    """
    operations = data['operations'].copy()

    # Fjern rader utan estimated_units_used
    operations = operations[operations['estimated_units_used'].notna()]

    # Finn system-eigarskap
    system_ownership = calculate_total_ownership_by_system(data)

    # Merge operasjonar med eigarskap
    ops_ownership = operations.merge(
        system_ownership,
        on='system_id',
        how='left'
    )

    # Berekn våpen tilskrive kvar investor
    ops_ownership['units_attributed_to_investor'] = (
        ops_ownership['estimated_units_used'] *
        ops_ownership['system_ownership_pct'] / 100
    )

    ops_ownership['cost_attributed_to_investor_usd_millions'] = (
        ops_ownership['estimated_cost_usd_millions'] *
        ops_ownership['system_ownership_pct'] / 100
    )

    # Aggreger per investor
    investor_munitions = ops_ownership.groupby('shareholder_name').agg({
        'units_attributed_to_investor': 'sum',
        'cost_attributed_to_investor_usd_millions': 'sum',
        'estimated_units_used': 'sum'  # Total for referanse
    }).reset_index()

    investor_munitions = investor_munitions.sort_values(
        'cost_attributed_to_investor_usd_millions',
        ascending=False
    )

    return investor_munitions

def calculate_nbim_specific_analysis(data):
    """
    Spesifikk analyse for NBIM/Oljefondet
    """
    infrastructure = data['infrastructure']
    nbim_row = infrastructure[infrastructure['investor_name'] == 'Norges Bank (NBIM)'].iloc[0]

    ownership = data['ownership']
    nbim_ownership = ownership[ownership['shareholder_name'] == 'Norges Bank (NBIM)']

    # Berekn totale marknadsverdi
    total_market_value = nbim_ownership['market_value_usd_millions'].sum()

    # Breakdon per selskap
    company_breakdown = nbim_ownership[['manufacturer_name', 'ownership_percentage',
                                        'market_value_usd_millions']].sort_values(
        'market_value_usd_millions', ascending=False
    )

    analysis = {
        'total_investment_usd_millions': total_market_value,
        'avg_killchain_ownership_pct': nbim_row['weighted_avg_killchain_ownership_pct'],
        'elbit_excluded': True,
        'top_holdings': company_breakdown.to_dict('records')
    }

    return analysis

def generate_summary_statistics(data):
    """
    Generer oppsummerande statistikk
    """
    stats = {}

    # Antal system, produsenter, investorar
    stats['total_systems'] = len(data['systems'])
    stats['total_manufacturers'] = len(data['manufacturers'])
    stats['total_shareholders'] = len(data['shareholders'])
    stats['total_operations_documented'] = len(data['operations'])

    # Total investering
    infrastructure = data['infrastructure']
    stats['total_investment_all_investors_usd_billions'] = (
        infrastructure['total_investment_usd_millions'].sum() / 1000
    )

    # Top investors
    top5 = infrastructure.nlargest(5, 'weighted_avg_killchain_ownership_pct')[
        ['investor_name', 'weighted_avg_killchain_ownership_pct', 'total_investment_usd_millions']
    ]
    stats['top_5_investors'] = top5.to_dict('records')

    # NBIM
    nbim_data = calculate_nbim_specific_analysis(data)
    stats['nbim_analysis'] = nbim_data

    # Munitions
    munitions = calculate_munitions_used_by_investor(data)
    stats['top_5_munitions_investors'] = munitions.head(5).to_dict('records')

    return stats

def export_analysis_results(data, stats):
    """
    Eksporter analyseresultat til JSON og CSV
    """
    # Export summary as JSON
    with open(OUTPUT_DIR / 'summary_statistics.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    # Export system ownership
    system_ownership = calculate_total_ownership_by_system(data)
    system_ownership.to_csv(OUTPUT_DIR / 'system_ownership_by_investor.csv', index=False)

    # Export munitions attribution
    munitions = calculate_munitions_used_by_investor(data)
    munitions.to_csv(OUTPUT_DIR / 'munitions_attributed_to_investors.csv', index=False)

    # Export infrastructure analysis (copy from data)
    data['infrastructure'].to_csv(OUTPUT_DIR / 'infrastructure_ownership_summary.csv', index=False)

    print(f"✓ Eksporterte analyseresultat til {OUTPUT_DIR}")

def print_summary(stats):
    """
    Print oppsummering til konsoll
    """
    print("\n" + "="*80)
    print("IDF KILL CHAIN OWNERSHIP ANALYSIS - SUMMARY")
    print("="*80 + "\n")

    print(f"Totalt antal system dokumentert: {stats['total_systems']}")
    print(f"Totalt antal produsenter: {stats['total_manufacturers']}")
    print(f"Totalt antal investorar: {stats['total_shareholders']}")
    print(f"Totalt antal Gaza-operasjonar: {stats['total_operations_documented']}")
    print(f"\nTotal investering (alle investorar): ${stats['total_investment_all_investors_usd_billions']:.1f} milliardar USD\n")

    print("\nTOP 5 INVESTORAR I KILL CHAIN-INFRASTRUKTUREN:")
    print("-" * 80)
    for i, inv in enumerate(stats['top_5_investors'], 1):
        print(f"{i}. {inv['investor_name']}")
        print(f"   Gjennomsnittleg eigarskap: {inv['weighted_avg_killchain_ownership_pct']:.2f}%")
        print(f"   Total investering: ${inv['total_investment_usd_millions']:,.0f} millionar USD\n")

    print("\nNBIM (OLJEFONDET) ANALYSE:")
    print("-" * 80)
    nbim = stats['nbim_analysis']
    print(f"Total investering: ${nbim['total_investment_usd_millions']:,.0f} millionar USD")
    print(f"Gjennomsnittleg eigarskap i kill chain: {nbim['avg_killchain_ownership_pct']:.2f}%")
    print(f"Elbit Systems ekskludert: {'Ja' if nbim['elbit_excluded'] else 'Nei'}\n")
    print("Top behaldningar:")
    for holding in nbim['top_holdings'][:5]:
        print(f"  - {holding['manufacturer_name']}: {holding['ownership_percentage']:.2f}% "
              f"(${holding['market_value_usd_millions']:,.0f}M)")

    print("\n" + "="*80)
    print("VÅPEN BRUKT I GAZA - TILSKRIVING TIL INVESTORAR")
    print("="*80 + "\n")
    print("Top 5 investorar etter tilskriven våpenbruk:\n")
    for i, inv in enumerate(stats['top_5_munitions_investors'], 1):
        print(f"{i}. {inv['shareholder_name']}")
        print(f"   Tilskrivne våpen: {inv['units_attributed_to_investor']:.0f} einingar")
        print(f"   Tilskriven kostnad: ${inv['cost_attributed_to_investor_usd_millions']:.2f}M USD\n")

    print("="*80 + "\n")

def main():
    """Hovudfunksjon"""
    print("Lastar data...")
    data = load_data()

    print("Bereknar eigarskapsanalyse...")
    stats = generate_summary_statistics(data)

    print("Eksporterer resultat...")
    export_analysis_results(data, stats)

    print_summary(stats)

    print(f"\n✓ Analyse fullført. Sjå {OUTPUT_DIR} for detaljerte resultat.")

if __name__ == '__main__':
    main()
