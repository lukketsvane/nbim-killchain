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
    data['ownership_timeseries'] = pd.read_csv(DATA_DIR / 'ownership_timeseries.csv')
    data['fms_contracts'] = pd.read_csv(DATA_DIR / 'fms_contracts.csv')
    data['stock_performance'] = pd.read_csv(DATA_DIR / 'stock_performance_gaza_war.csv')
    data['lobbying'] = pd.read_csv(DATA_DIR / 'lobbying_political_contributions.csv')
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

def plot_stock_performance_war(data):
    """
    Aksjekursutvikling for produsenter under Gaza-krigen
    """
    stock = data['stock_performance'].copy()
    stock['date'] = pd.to_datetime(stock['date'])

    # Focus on key manufacturers
    key_manufacturers = ['Lockheed Martin', 'Boeing', 'Raytheon Technologies', 'Elbit Systems', 'Northrop Grumman']
    stock_filtered = stock[stock['manufacturer_name'].isin(key_manufacturers)]

    fig = px.line(
        stock_filtered,
        x='date',
        y='closing_price_usd',
        color='manufacturer_name',
        title='Aksjekursutvikling under Gaza-krigen (okt 2023 - jun 2024)',
        labels={'date': 'Dato', 'closing_price_usd': 'Aksjekurs (USD)', 'manufacturer_name': 'Produsent'}
    )

    # Add vertical line for Oct 7
    oct7_timestamp = pd.Timestamp('2023-10-07').timestamp() * 1000
    fig.add_vline(x=oct7_timestamp, line_dash="dash", line_color="red",
                  annotation_text="7. oktober 2023", annotation_position="top left")

    fig.update_layout(height=600, hovermode='x unified')
    fig.write_html(VIZ_DIR / 'stock_performance_war.html')

    print("✓ Genererte: stock_performance_war")

def plot_fms_contracts_timeline(data):
    """
    FMS-kontraktar til Israel over tid
    """
    fms = data['fms_contracts'].copy()
    fms['date_announced'] = pd.to_datetime(fms['date_announced'])
    fms['fiscal_year'] = fms['fiscal_year'].astype(int)

    # Aggregate by fiscal year
    by_year = fms.groupby('fiscal_year').agg({
        'contract_value_usd_millions': 'sum',
        'contract_id': 'count'
    }).reset_index()

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Total kontraktverdi per år', 'Antal kontraktar per år'),
        vertical_spacing=0.15
    )

    fig.add_trace(
        go.Bar(x=by_year['fiscal_year'], y=by_year['contract_value_usd_millions'],
               name='Kontraktverdi (millionar USD)', marker_color='#E63946'),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=by_year['fiscal_year'], y=by_year['contract_id'],
               name='Antal kontraktar', marker_color='#457B9D'),
        row=2, col=1
    )

    fig.update_xaxes(title_text="Fiscal Year", row=2, col=1)
    fig.update_yaxes(title_text="USD Millionar", row=1, col=1)
    fig.update_yaxes(title_text="Antal kontraktar", row=2, col=1)

    fig.update_layout(
        title_text='US Foreign Military Sales til Israel (2019-2024)',
        height=700,
        showlegend=False
    )

    fig.write_html(VIZ_DIR / 'fms_contracts_timeline.html')

    print("✓ Genererte: fms_contracts_timeline")

def plot_lobbying_trends(data):
    """
    Lobbyisme-trend 2020-2024
    """
    lobbying = data['lobbying'].copy()

    # Top 5 manufacturers by total lobbying
    top5_mfr = lobbying.groupby('manufacturer_name')['total_lobbying_usd_millions'].sum().nlargest(5).index
    lobbying_top5 = lobbying[lobbying['manufacturer_name'].isin(top5_mfr)]

    fig = go.Figure()

    for mfr in top5_mfr:
        mfr_data = lobbying_top5[lobbying_top5['manufacturer_name'] == mfr]
        fig.add_trace(go.Scatter(
            x=mfr_data['year'],
            y=mfr_data['total_lobbying_usd_millions'],
            mode='lines+markers',
            name=mfr,
            line=dict(width=3)
        ))

    # Add shaded region for Gaza war
    fig.add_vrect(x0=2023, x1=2024, fillcolor="red", opacity=0.1,
                  annotation_text="Gaza-krigen", annotation_position="top left")

    fig.update_layout(
        title='Lobbyisme-utgifter for våpenprodusenter (2020-2024)',
        xaxis_title='År',
        yaxis_title='Lobbyisme (millionar USD)',
        height=600,
        hovermode='x unified'
    )

    fig.write_html(VIZ_DIR / 'lobbying_trends.html')

    print("✓ Genererte: lobbying_trends")

def plot_nbim_timeseries(data):
    """
    NBIM eigarskap over tid
    """
    timeseries = data['ownership_timeseries'].copy()
    timeseries['date'] = pd.to_datetime(timeseries['date'])

    nbim_ts = timeseries[timeseries['shareholder_name'] == 'Norges Bank (NBIM)']

    # Total value over time
    by_date = nbim_ts.groupby('date')['market_value_usd_millions'].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=by_date['date'],
        y=by_date['market_value_usd_millions'],
        mode='lines+markers',
        name='NBIM total investering',
        line=dict(color='#E63946', width=3),
        fill='tozeroy'
    ))

    # Add vertical line for Oct 7
    oct7_timestamp = pd.Timestamp('2023-10-07').timestamp() * 1000
    fig.add_vline(x=oct7_timestamp, line_dash="dash", line_color="black",
                  annotation_text="7. oktober 2023")

    fig.update_layout(
        title='NBIM sitt eigarskap i kill chain-selskap over tid',
        xaxis_title='Dato',
        yaxis_title='Marknadsverdi (millionar USD)',
        height=600
    )

    fig.write_html(VIZ_DIR / 'nbim_timeseries.html')

    print("✓ Genererte: nbim_timeseries")

def plot_stock_performance_comparison(data):
    """
    Samanlikning av aksjekurs før/etter 7. oktober
    """
    stock = data['stock_performance'].copy()
    stock['date'] = pd.to_datetime(stock['date'])

    # Get Oct 6 and Dec 31 prices
    oct6 = stock[stock['date'] == '2023-10-06'][['manufacturer_name', 'closing_price_usd']]
    dec31 = stock[stock['date'] == '2023-12-31'][['manufacturer_name', 'closing_price_usd']]

    comparison = oct6.merge(dec31, on='manufacturer_name', suffixes=('_oct6', '_dec31'))
    comparison['pct_change'] = ((comparison['closing_price_usd_dec31'] - comparison['closing_price_usd_oct6']) /
                                 comparison['closing_price_usd_oct6'] * 100)
    comparison = comparison.sort_values('pct_change', ascending=True)

    fig = go.Figure()

    colors = ['#2A9D8F' if x >= 0 else '#E76F51' for x in comparison['pct_change']]

    fig.add_trace(go.Bar(
        y=comparison['manufacturer_name'],
        x=comparison['pct_change'],
        orientation='h',
        marker_color=colors,
        text=comparison['pct_change'].round(2),
        texttemplate='%{text}%',
        textposition='outside'
    ))

    fig.update_layout(
        title='Aksjekursendring 6. oktober - 31. desember 2023 (%)',
        xaxis_title='Endring (%)',
        yaxis_title='Produsent',
        height=600
    )

    fig.write_html(VIZ_DIR / 'stock_performance_comparison.html')

    print("✓ Genererte: stock_performance_comparison")

def main():
    """Hovudfunksjon"""
    print("Lastar data...")
    data = load_data()

    print("\nGenererer visualiseringar...\n")

    # Original visualizations
    plot_top_investors_bar(data)
    plot_ownership_heatmap(data)
    plot_nbim_comparison(data)
    plot_manufacturer_ownership_pie(data)
    plot_operations_timeline(data)
    plot_munition_types_breakdown(data)
    plot_system_types_distribution(data)
    generate_interactive_table(data)

    # New visualizations
    plot_stock_performance_war(data)
    plot_fms_contracts_timeline(data)
    plot_lobbying_trends(data)
    plot_nbim_timeseries(data)
    plot_stock_performance_comparison(data)

    print(f"\n✓ Alle visualiseringar genererte i {VIZ_DIR}")
    print("\nFiler:")
    for file in sorted(VIZ_DIR.glob('*')):
        print(f"  - {file.name}")

if __name__ == '__main__':
    main()
