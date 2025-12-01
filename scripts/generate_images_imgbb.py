#!/usr/bin/env python3
"""
Generer visualiseringar (PNG) for kill chain ownership analysis,
lastar opp til ImgBB, og oppdaterer docs/index.html.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
import requests
import base64
import re
import sys

# ImgBB API Key
IMGBB_API_KEY = "67bc9085dfd47a9a6df5409995e66874"

# Paths
DATA_DIR = Path(__file__).parent.parent / 'data'
OUTPUT_DIR = Path(__file__).parent.parent / 'output'
VIZ_DIR = OUTPUT_DIR / 'visualizations'
DOCS_DIR = Path(__file__).parent.parent / 'docs'
INDEX_HTML_PATH = DOCS_DIR / 'index.html'

VIZ_DIR.mkdir(exist_ok=True, parents=True)

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

def upload_to_imgbb(image_path):
    """Upload image to ImgBB and return direct link"""
    print(f"Uploading {image_path.name} to ImgBB...")
    with open(image_path, "rb") as file:
        payload = {
            "key": IMGBB_API_KEY,
            "image": base64.b64encode(file.read()),
        }
        res = requests.post("https://api.imgbb.com/1/upload", data=payload)
        if res.status_code == 200:
            url = res.json()['data']['url']
            print(f"Success: {url}")
            return url
        else:
            print(f"Error uploading {image_path.name}: {res.text}")
            return None

# Visualization Functions (modified to return filename)

def generate_top_investors_bar(data):
    infrastructure = data['infrastructure']
    top10 = infrastructure.nlargest(10, 'weighted_avg_killchain_ownership_pct')
    fig = px.bar(
        top10, x='investor_name', y='weighted_avg_killchain_ownership_pct',
        color='investor_type', title='Top 10 Investorar',
        text='weighted_avg_killchain_ownership_pct'
    )
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45, height=600)
    filename = "top_investors_bar.png"
    fig.write_image(VIZ_DIR / filename, width=1200, height=800)
    return filename

def generate_ownership_heatmap(data):
    infrastructure = data['infrastructure']
    top10 = infrastructure.nlargest(10, 'weighted_avg_killchain_ownership_pct')
    ownership_cols = [col for col in infrastructure.columns if col.startswith('pct_ownership_')]
    ownership_data = top10[['investor_name'] + ownership_cols].set_index('investor_name')
    ownership_data.columns = [col.replace('pct_ownership_', '').replace('_infrastructure', '').replace('_', ' ').title() for col in ownership_data.columns]
    fig = px.imshow(
        ownership_data, labels=dict(x="Type", y="Investor", color="Eigarskap (%)"),
        color_continuous_scale='Reds', title='Eigarskap Heatmap'
    )
    fig.update_layout(height=600)
    filename = "ownership_heatmap.png"
    fig.write_image(VIZ_DIR / filename, width=1200, height=800)
    return filename

def generate_nbim_comparison(data):
    infrastructure = data['infrastructure']
    others_top5 = infrastructure[infrastructure['investor_name'] != 'Norges Bank (NBIM)'].nlargest(5, 'weighted_avg_killchain_ownership_pct')
    nbim = infrastructure[infrastructure['investor_name'] == 'Norges Bank (NBIM)']
    comparison = pd.concat([nbim, others_top5])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=comparison['investor_name'], y=comparison['weighted_avg_killchain_ownership_pct'],
        marker_color=['#FF6B6B' if x == 'Norges Bank (NBIM)' else '#4ECDC4' for x in comparison['investor_name']],
        text=comparison['weighted_avg_killchain_ownership_pct'], texttemplate='%{text:.2f}%', textposition='outside'
    ))
    fig.update_layout(title='NBIM vs. Andre', height=600)
    filename = "nbim_comparison.png"
    fig.write_image(VIZ_DIR / filename, width=1200, height=800)
    return filename

def generate_lockheed_pie(data):
    ownership = data['ownership']
    lmt_ownership = ownership[ownership['manufacturer_name'] == 'Lockheed Martin'].nlargest(8, 'ownership_percentage')
    total_top8 = lmt_ownership['ownership_percentage'].sum()
    others_pct = 100 - total_top8
    labels = list(lmt_ownership['shareholder_name']) + ['Others']
    values = list(lmt_ownership['ownership_percentage']) + [others_pct]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title='Lockheed Martin Eigarskap', height=600)
    filename = "lockheed_ownership_pie.png"
    fig.write_image(VIZ_DIR / filename, width=1200, height=800)
    return filename

def generate_operations_timeline(data):
    operations = data['operations'].copy()
    operations['date'] = pd.to_datetime(operations['date'])
    operations['year_month'] = operations['date'].dt.to_period('M')
    monthly = operations.groupby('year_month').agg({'estimated_cost_usd_millions': 'sum', 'estimated_units_used': 'sum'}).reset_index()
    monthly['year_month'] = monthly['year_month'].dt.to_timestamp()
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Våpenkostnad', 'Antal våpen'))
    fig.add_trace(go.Bar(x=monthly['year_month'], y=monthly['estimated_cost_usd_millions'], name='Kostnad', marker_color='#E63946'), row=1, col=1)
    fig.add_trace(go.Bar(x=monthly['year_month'], y=monthly['estimated_units_used'], name='Antal', marker_color='#457B9D'), row=2, col=1)
    fig.update_layout(title='Gaza-operasjonar Tidsserie', height=800, showlegend=False)
    filename = "operations_timeline.png"
    fig.write_image(VIZ_DIR / filename, width=1200, height=1000)
    return filename

def generate_munition_breakdown(data):
    operations = data['operations'].copy()
    summary = operations.groupby('munition_type').agg({'estimated_units_used': 'sum', 'estimated_cost_usd_millions': 'sum'}).reset_index()
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]], subplot_titles=('Antal', 'Kostnad'))
    fig.add_trace(go.Pie(labels=summary['munition_type'], values=summary['estimated_units_used'], name='Antal'), row=1, col=1)
    fig.add_trace(go.Pie(labels=summary['munition_type'], values=summary['estimated_cost_usd_millions'], name='Kostnad'), row=1, col=2)
    fig.update_layout(title='Våpentypar', height=500)
    filename = "munition_types_breakdown.png"
    fig.write_image(VIZ_DIR / filename, width=1200, height=600)
    return filename

def generate_system_dist(data):
    systems = data['systems']
    counts = systems['system_type'].value_counts()
    fig = px.bar(x=counts.index, y=counts.values, title='Systemtypar', color=counts.values)
    fig.update_layout(height=600, xaxis_tickangle=-45)
    filename = "system_types_distribution.png"
    fig.write_image(VIZ_DIR / filename, width=1200, height=800)
    return filename

def generate_table_image(data):
    # Plotly tables export poorly to PNG sometimes, but let's try
    infrastructure = data['infrastructure']
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Investor', 'Type', 'Land', 'Avg (%)'], fill_color='#1D3557', font=dict(color='white')),
        cells=dict(values=[infrastructure['investor_name'], infrastructure['investor_type'], infrastructure['country'], infrastructure['weighted_avg_killchain_ownership_pct'].round(2)], fill_color='#F1FAEE')
    )])
    fig.update_layout(title='Oversikt', height=800)
    filename = "interactive_ownership_table.png"
    fig.write_image(VIZ_DIR / filename, width=1000, height=1200)
    return filename

def update_html(image_map):
    """Update index.html with new image URLs"""
    if not INDEX_HTML_PATH.exists():
        print("Error: index.html not found")
        return

    with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # Map html filename (viz/xxx.html) to key in image_map (xxx.png)
    # We need to find which image corresponds to which iframe
    
    replacements = {
        "top_investors_bar.html": "top_investors_bar.png",
        "nbim_comparison.html": "nbim_comparison.png",
        "lockheed_ownership_pie.html": "lockheed_ownership_pie.png",
        "operations_timeline.html": "operations_timeline.png",
        "munition_types_breakdown.html": "munition_types_breakdown.png",
        "system_types_distribution.html": "system_types_distribution.png",
        "ownership_heatmap.html": "ownership_heatmap.png",
        "interactive_ownership_table.html": "interactive_ownership_table.png"
    }

    for html_file, png_file in replacements.items():
        if png_file in image_map:
            url = image_map[png_file]
            # Regex to replace the specific iframe
            pattern = r'<iframe src="viz/' + re.escape(html_file) + r'"[^>]*></iframe>'
            replacement = f'<a href="{url}" target="_blank"><img src="{url}" alt="{png_file}" style="width:100%; height:auto; border-radius:4px;"></a>'
            html = re.sub(pattern, replacement, html)
            print(f"Replaced {html_file} with image")

    with open(INDEX_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html")

def main():
    print("Loading data...")
    data = load_data()
    
    print("Generating images...")
    generated_files = []
    generated_files.append(generate_top_investors_bar(data))
    generated_files.append(generate_ownership_heatmap(data))
    generated_files.append(generate_nbim_comparison(data))
    generated_files.append(generate_lockheed_pie(data))
    generated_files.append(generate_operations_timeline(data))
    generated_files.append(generate_munition_breakdown(data))
    generated_files.append(generate_system_dist(data))
    generated_files.append(generate_table_image(data))

    print("Uploading to ImgBB...")
    image_map = {}
    for filename in generated_files:
        url = upload_to_imgbb(VIZ_DIR / filename)
        if url:
            image_map[filename] = url

    print("Updating HTML...")
    update_html(image_map)

if __name__ == "__main__":
    main()
