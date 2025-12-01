#!/usr/bin/env python3
"""
Generer visualiseringar for kill chain ownership analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Paths
DATA_DIR = Path(__file__).parent.parent / 'data'
OUTPUT_DIR = Path(__file__).parent.parent / 'output'
VIZ_DIR = OUTPUT_DIR / 'visualizations'
VIZ_DIR.mkdir(exist_ok=True, parents=True)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def load_data():
    """Last inn alle data"""
    data = {}
    data['systems'] = pd.read_csv(DATA_DIR / 'military_systems.csv')
    data['manufacturers'] = pd.read_csv(DATA_DIR / 'manufacturers.csv')
    data['shareholders'] = pd.read_csv(DATA_DIR / 'major_shareholders.csv')
    data['ownership'] = pd.read_csv(DATA_DIR / 'ownership_stakes.csv')
    data['infrastructure'] = pd.read_csv(DATA_DIR / 'infrastructure_ownership_analysis.csv')
    data['operations'] = pd.read_csv(DATA_DIR / 'gaza_operations_data.csv')
    return data

def plot_top_investors_bar(data):
    """
    Bar chart av top investorar i kill chain-infrastrukturen
    """
    infrastructure = data['infrastructure']
    top10 = infrastructure.nlargest(10, 'weighted_avg_killchain_ownership_pct')

    fig = px.bar(
        top10,
        x='investor_name',
        y='weighted_avg_killchain_ownership_pct',
        color='investor_type',
        title='Top 10 Investorar - Gjennomsnittleg eigarskap i IDF Kill Chain-infrastruktur',
        labels={
            'investor_name': 'Investor',
            'weighted_avg_killchain_ownership_pct': 'Eigarskap (%)',
            'investor_type': 'Investortype'
        },
        text='weighted_avg_killchain_ownership_pct'
    )

    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45, height=600)

    fig.write_html(VIZ_DIR / 'top_investors_bar.html')
    fig.write_image(VIZ_DIR / 'top_investors_bar.png', width=1200, height=800)

    print("✓ Genererte: top_investors_bar")

def plot_ownership_heatmap(data):
    """
    Heatmap av eigarskap på tvers av ulike infrastrukturtypar
    """
    infrastructure = data['infrastructure']
    top10 = infrastructure.nlargest(10, 'weighted_avg_killchain_ownership_pct')

    # Velg eigarskapkolumner
    ownership_cols = [col for col in infrastructure.columns if col.startswith('pct_ownership_')]
    ownership_data = top10[['investor_name'] + ownership_cols].set_index('investor_name')

    # Rename columns for betre labels
    ownership_data.columns = [
        col.replace('pct_ownership_', '').replace('_infrastructure', '').replace('_', ' ').title()
        for col in ownership_data.columns
    ]

    fig = px.imshow(
        ownership_data,
        labels=dict(x="Infrastrukturtype", y="Investor", color="Eigarskap (%)"),
        x=ownership_data.columns,
        y=ownership_data.index,
        color_continuous_scale='Reds',
        title='Eigarskap på tvers av ulike infrastrukturtypar - Top 10 investorar'
    )

    fig.update_xaxes(side="bottom")
    fig.update_layout(height=600)

    fig.write_html(VIZ_DIR / 'ownership_heatmap.html')

    print("✓ Genererte: ownership_heatmap")

def plot_nbim_comparison(data):
    """
    Samanlikn NBIM med andre investorar
    """
    infrastructure = data['infrastructure']

    # Velg NBIM og top 5 andre
    others_top5 = infrastructure[infrastructure['investor_name'] != 'Norges Bank (NBIM)'].nlargest(
        5, 'weighted_avg_killchain_ownership_pct'
    )
    nbim = infrastructure[infrastructure['investor_name'] == 'Norges Bank (NBIM)']

    comparison = pd.concat([nbim, others_top5])

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=comparison['investor_name'],
        y=comparison['weighted_avg_killchain_ownership_pct'],
        marker_color=['#FF6B6B' if x == 'Norges Bank (NBIM)' else '#4ECDC4'
                      for x in comparison['investor_name']],
        text=comparison['weighted_avg_killchain_ownership_pct'],
        texttemplate='%{text:.2f}%',
        textposition='outside',
    ))

    fig.update_layout(
        title='NBIM samanlikna med andre store investorar i kill chain-infrastruktur',
        xaxis_title='Investor',
        yaxis_title='Gjennomsnittleg eigarskap (%)',
        xaxis_tickangle=-45,
        height=600,
        showlegend=False
    )

    fig.write_html(VIZ_DIR / 'nbim_comparison.html')

    print("✓ Genererte: nbim_comparison")

def plot_manufacturer_ownership_pie(data):
    """
    Pie chart av eigarskap i nøkkelprodusenter
    """
    ownership = data['ownership']

    # Fokuser på Lockheed Martin (F-35 produsent)
    lmt_ownership = ownership[ownership['manufacturer_name'] == 'Lockheed Martin'].nlargest(
        8, 'ownership_percentage'
    )

    # Legg til "Others"
    total_top8 = lmt_ownership['ownership_percentage'].sum()
    others_pct = 100 - total_top8

    labels = list(lmt_ownership['shareholder_name']) + ['Others']
    values = list(lmt_ownership['ownership_percentage']) + [others_pct]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    fig.update_layout(
        title='Eigarskap i Lockheed Martin (F-35 produsent)',
        height=600
    )

    fig.write_html(VIZ_DIR / 'lockheed_ownership_pie.html')

    print("✓ Genererte: lockheed_ownership_pie")

def plot_operations_timeline(data):
    """
    Tidslinje av Gaza-operasjonar med våpenkostnad
    """
    operations = data['operations'].copy()
    operations['date'] = pd.to_datetime(operations['date'])

    # Aggreger per månad
    operations['year_month'] = operations['date'].dt.to_period('M')
    monthly = operations.groupby('year_month').agg({
        'estimated_cost_usd_millions': 'sum',
        'estimated_units_used': 'sum'
    }).reset_index()
    monthly['year_month'] = monthly['year_month'].dt.to_timestamp()

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Total våpenkostnad per månad', 'Antal våpen brukt per månad'),
        vertical_spacing=0.12
    )

    fig.add_trace(
        go.Bar(x=monthly['year_month'], y=monthly['estimated_cost_usd_millions'],
               name='Kostnad (millionar USD)', marker_color='#E63946'),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=monthly['year_month'], y=monthly['estimated_units_used'],
               name='Antal våpen', marker_color='#457B9D'),
        row=2, col=1
    )

    fig.update_xaxes(title_text="Månad", row=2, col=1)
    fig.update_yaxes(title_text="USD Millionar", row=1, col=1)
    fig.update_yaxes(title_text="Antal våpen", row=2, col=1)

    fig.update_layout(
        title_text='Gaza-operasjonar: Våpenbruk over tid (okt 2023 - nov 2024)',
        height=800,
        showlegend=False
    )

    fig.write_html(VIZ_DIR / 'operations_timeline.html')

    print("✓ Genererte: operations_timeline")

def plot_munition_types_breakdown(data):
    """
    Breakdown av ulike våpentypar brukt
    """
    operations = data['operations'].copy()

    # Aggreger per munition type
    munition_summary = operations.groupby('munition_type').agg({
        'estimated_units_used': 'sum',
        'estimated_cost_usd_millions': 'sum'
    }).reset_index()

    munition_summary = munition_summary.sort_values('estimated_cost_usd_millions', ascending=False)

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Antal våpen brukt', 'Total kostnad'),
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )

    fig.add_trace(
        go.Pie(labels=munition_summary['munition_type'],
               values=munition_summary['estimated_units_used'],
               name='Antal'),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(labels=munition_summary['munition_type'],
               values=munition_summary['estimated_cost_usd_millions'],
               name='Kostnad'),
        row=1, col=2
    )

    fig.update_layout(
        title_text='Våpentypar brukt i Gaza: Antal vs. Kostnad',
        height=500
    )

    fig.write_html(VIZ_DIR / 'munition_types_breakdown.html')

    print("✓ Genererte: munition_types_breakdown")

def plot_system_types_distribution(data):
    """
    Distribusjon av systemtypar i infrastrukturen
    """
    systems = data['systems']

    system_counts = systems['system_type'].value_counts()

    fig = px.bar(
        x=system_counts.index,
        y=system_counts.values,
        title='Distribusjon av systemtypar i IDF-infrastrukturen',
        labels={'x': 'Systemtype', 'y': 'Antal system'},
        color=system_counts.values,
        color_continuous_scale='Viridis'
    )

    fig.update_layout(xaxis_tickangle=-45, height=600, showlegend=False)

    fig.write_html(VIZ_DIR / 'system_types_distribution.html')

    print("✓ Genererte: system_types_distribution")

def generate_interactive_table(data):
    """
    Interaktiv tabell med all eigarskapdata
    """
    infrastructure = data['infrastructure']

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Investor', 'Type', 'Land', 'F-35 (%)', 'F-16 (%)', 'F-15 (%)',
                    'Munitions (%)', 'ISR/UAV (%)', 'Targeting (%)', 'Gj.snitt (%)'],
            fill_color='#1D3557',
            font=dict(color='white', size=12),
            align='left'
        ),
        cells=dict(
            values=[
                infrastructure['investor_name'],
                infrastructure['investor_type'],
                infrastructure['country'],
                infrastructure['pct_ownership_f35_infrastructure'].round(2),
                infrastructure['pct_ownership_f16_infrastructure'].round(2),
                infrastructure['pct_ownership_f15_infrastructure'].round(2),
                infrastructure['pct_ownership_munitions_infrastructure'].round(2),
                infrastructure['pct_ownership_isr_uav_infrastructure'].fillna(0).round(2),
                infrastructure['pct_ownership_targeting_infrastructure'].round(2),
                infrastructure['weighted_avg_killchain_ownership_pct'].round(2)
            ],
            fill_color=[['#F1FAEE', '#E9F5F2'] * (len(infrastructure)//2 + 1)],
            align='left',
            font=dict(size=11)
        )
    )])

    fig.update_layout(
        title='Komplett eigarskapstabell - Alle investorar og infrastrukturtypar',
        height=800
    )

    fig.write_html(VIZ_DIR / 'interactive_ownership_table.html')

    print("✓ Genererte: interactive_ownership_table")

def main():
    """Hovudfunksjon"""
    print("Lastar data...")
    data = load_data()

    print("\nGenererer visualiseringar...\n")

    plot_top_investors_bar(data)
    plot_ownership_heatmap(data)
    plot_nbim_comparison(data)
    plot_manufacturer_ownership_pie(data)
    plot_operations_timeline(data)
    plot_munition_types_breakdown(data)
    plot_system_types_distribution(data)
    generate_interactive_table(data)

    print(f"\n✓ Alle visualiseringar genererte i {VIZ_DIR}")
    print("\nFiler:")
    for file in sorted(VIZ_DIR.glob('*')):
        print(f"  - {file.name}")

if __name__ == '__main__':
    main()
