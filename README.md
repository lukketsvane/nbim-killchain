# IDF Kill Chain Ownership Analysis

## Prosjektskildring

Dette prosjektet dokumenterer eigarskapsstrukturar i den militære infrastrukturen som nyttast av Israel Defense Forces (IDF) i militære operasjonar mot Gaza. Målet er å etablere transparens rundt kven som profitterer på og har eigarskap i selskapa som produserer våpen, fly, missil, etterretningssystem og anna militært utstyr.

## Datastruktur

### Hovudfiler

#### 1. `data/military_systems.csv`
Dokumenterer alle hovudsystem i IDF sin militære infrastruktur:
- **Kolumner**: system_id, system_name, system_type, manufacturer, country, role_in_killchain, used_in_gaza_2023_2024
- **Eksempel**: F-35I Adir, F-16I Sufa, JDAM bomber, SPICE-missil, UAV-system
- **40 system** dokumentert

#### 2. `data/manufacturers.csv`
Alle produsenter av militært utstyr:
- **Kolumner**: manufacturer_id, manufacturer_name, country, stock_ticker, stock_exchange, sector, primary_products
- **Hovudselskap**: Lockheed Martin, Boeing, Raytheon, Northrop Grumman, Elbit Systems, IAI, Rafael
- **20 selskap** dokumentert

#### 3. `data/major_shareholders.csv`
Hovudinvestorar og aksjonærar:
- **Kolumner**: shareholder_id, shareholder_name, shareholder_type, country, total_aum_usd_billions
- **Typar**: Asset managers, pensjonsfond, statlige fond, bankar
- **30 investorar** dokumentert
- **Totalt AUM**: Over $50 billionar USD

#### 4. `data/ownership_stakes.csv`
Detaljert eigarskap i kvart selskap:
- **Kolumner**: ownership_id, shareholder_id, shareholder_name, manufacturer_id, manufacturer_name, stock_ticker, shares_held_millions, ownership_percentage, market_value_usd_millions, as_of_date
- **63 eigarskapsforhold** dokumentert
- **Dato**: Per 30. juni 2024

#### 5. `data/system_components.csv`
Komponentnivå for kvar våpensystem:
- **Kolumner**: component_id, system_id, system_name, component_name, manufacturer_id, manufacturer_name, component_role, estimated_value_per_unit_usd_millions
- **Eksempel**: F-35 består av airframe (Lockheed Martin), motor (Pratt & Whitney), radar (Northrop Grumman), israelske system (Elbit)
- **66 komponentar** dokumentert

#### 6. `data/infrastructure_ownership_analysis.csv`
**HOVUDANALYSE**: Berekna eigarskapsandel i heile kill chain-infrastrukturen:
- **Kolumner**:
  - investor_name, investor_type, country
  - total_investment_usd_millions
  - pct_ownership_f35_infrastructure
  - pct_ownership_f16_infrastructure
  - pct_ownership_f15_infrastructure
  - pct_ownership_munitions_infrastructure
  - pct_ownership_isr_uav_infrastructure
  - pct_ownership_targeting_infrastructure
  - pct_ownership_c4isr_infrastructure
  - pct_ownership_ground_systems_infrastructure
  - weighted_avg_killchain_ownership_pct
  - nbim_excluded_status

**Hovudfunn**:
- **BlackRock**: 9.39% gjennomsnittleg eigarskap i heile infrastrukturen
- **Vanguard**: 8.49% gjennomsnittleg eigarskap
- **State Street**: 6.02% gjennomsnittleg eigarskap
- **Norges Bank (NBIM)**: 1.12% gjennomsnittleg eigarskap (ekskluderer Elbit Systems)

#### 7. `data/gaza_operations_data.csv`
Dokumenterte militære operasjonar i Gaza med våpensystem:
- **Kolumner**: date, operation_type, munition_type, system_id, system_name, manufacturer_primary, estimated_units_used, estimated_cost_usd_millions, target_type, location_gaza, casualties_reported
- **Periode**: Oktober 2023 - november 2024
- **51 operasjonar** dokumentert
- **Inkluderer**: Antal våpen brukt, kostnad, mål, lokasjon, rapporterte ofre

## Hovudfunn

### Top 5 Investorar i Kill Chain-infrastrukturen

| Investor | Type | Land | Gjennomsnittleg eigarskap | Total investering (millionar USD) |
|----------|------|------|---------------------------|-----------------------------------|
| BlackRock | Asset Manager | USA | 9.39% | $137,335 |
| Vanguard Group | Asset Manager | USA | 8.49% | $127,725 |
| State Street | Asset Manager | USA | 6.02% | $79,152 |
| Capital Group | Asset Manager | USA | 5.88% | $72,340 |
| Fidelity | Asset Manager | USA | 2.89% | $37,730 |

### NBIM (Norges Bank Investment Management)

- **Gjennomsnittleg eigarskap**: 1.12% av heile kill chain-infrastrukturen
- **Total investering**: $15,344 millionar USD
- **Status**: Ekskluderer Elbit Systems (0% eigarskap)
- **Eigarskap i nøkkelselskap**:
  - Lockheed Martin (F-35, F-16): 1.14%
  - Boeing (F-15, Apache, JDAM): 1.6%
  - Raytheon (missil, radar): 1.26%
  - Northrop Grumman (radar, elektronikk): 1.38%
  - Caterpillar (D9 bulldozers): 1.29%

## Metodologi

### Berekning av eigarskapsandel

Eigarskapsandelen i infrastrukturen er berekna ved:

1. **Komponentvekting**: Kvar våpensystem er dekomponert i komponentar (airframe, motor, radar, etc.)
2. **Verdivekting**: Kvar komponent er vekta etter estimert verdi
3. **Eigarskapsmapping**: Eigarskapsandel i produsenten av kvar komponent
4. **Aggregering**: Samla eigarskap på tvers av alle system

**Eksempel - F-35I Adir**:
- Airframe (Lockheed Martin): $85M - 60.7%
- Motor (Pratt & Whitney/RTX): $18M - 12.9%
- Radar (Northrop Grumman): $12M - 8.6%
- Avionikk (Collins/RTX): $8.5M - 6.1%
- Targeting (Lockheed Martin): $4.2M - 3.0%
- Israelske system (Elbit): $5M - 3.6%

For ein investor med 8% eigarskap i Lockheed Martin, 9% i RTX, og 12% i Northrop Grumman:
- F-35 eigarskap = (0.607 × 0.08) + (0.036 × 0.00) + (0.129+0.061) × 0.09 + (0.086 × 0.12) = 7.66%

### Datakjelder

- **Eigarskapdata**: SEC 13F filings, Bloomberg, FactSet (per Q2 2024)
- **Våpensystemdata**: SIPRI, Jane's Defence, IDF offentlege kjeder
- **Gaza-operasjonar**: Dokumenterte hendingar frå FN, OCHA, B'Tselem, menneskeretstilsyn
- **Kontraktar**: US Foreign Military Sales (FMS), israelske forsvarsbudsjett

## Viktige presiseringar

### Limitasjonar

1. **Israelske statsselskap**: IAI og Rafael er statseigna - eigarskapsstruktur ikkje offentleg
2. **Indirekte eigarskap**: ETF-ar og indeksfond gir indirekte eksponering
3. **Dynamiske data**: Eigarskap endrar seg kvartalsvis
4. **Estimat**: Våpenbruk og komponentverdi er estimat basert på offentleg tilgjengeleg info

### Etiske konsiderasjonar

Dette prosjektet er ikkje:
- Ein investeringsråd
- Ein politisk kampanje mot spesifikke selskap
- Ein uttømmande juridisk analyse

Dette prosjektet **er**:
- Eit forsøk på transparens om kven som profitterer på krig
- Grunnlag for informerte avgjerder for investorar, pensjonsfond og politikarar
- Dokumentasjon av samanheng mellom finans og militær infrastruktur

## Vidare analyse

### Planlagde tillegg

1. **Tidsserieanalyse**: Eigarskap over tid (2020-2024)
2. **Kontraktsanalyse**: FMS-kontraktar og leveransar til Israel
3. **Profittanalyse**: Aksjekurs og profitt for produsenter under Gaza-krigen
4. **Leverandørkjede**: Sub-kontraktørar og leverandørar
5. **Lobbyisme**: Politiske bidrag og lobbyverksemd

### Visualiseringar (planlagt)

- Sankey-diagram: Investorflyt til produsenter til våpensystem
- Nettverk-graf: Eigarskapsnettverket
- Interaktiv tabell: Filtrer etter investor/produsent/våpen
- Tidslinje: Gaza-operasjonar med våpenbruk

## Kjøre analysane

### Python-script (under utvikling)

```bash
# Installere dependencies
pip install -r requirements.txt

# Kjøre hovudanalyse
python scripts/analyze_ownership.py

# Generere visualiseringar
python scripts/generate_visualizations.py

# Eksportere rapportar
python scripts/export_reports.py
```

## Bidrag

Dette er open source research. Bidrag er velkomne:

1. **Dataforbetring**: Oppdaterte eigarskapstal, fleire våpensystem
2. **Metodologi**: Forbetra berekningsmodelar
3. **Kjelder**: Ytterlegare verifisering av data
4. **Oversettingar**: Dokumentasjon på fleire språk

## Lisens

Data: CC BY 4.0 (krev attribusjon)
Kode: MIT License

## Kontakt

For spørsmål om metodologi eller data, ver vennleg å opprette eit issue på GitHub.

---

*Sist oppdatert: desember 2024*
*Datagrunnlag: Per 30. juni 2024*
