# NBIM Kill Chain Analysis

**Kartlegging av Oljefondets (SPU/NBIM) strukturelle eigarskap i Gaza Kill Chain-infrastrukturen**

> Versjon 2.0 | Sist oppdatert: Desember 2025

## Samandrag

Dette prosjektet dokumenterer korleis Statens pensjonsfond utland (SPU), verdens største statlege investeringsfond med ein verdi på $1,9 billionar, eig mellom **1,0% og 3,8%** av selskapa som utgjer den integrerte "kill chain"-infrastrukturen brukt i Gaza-krigen sidan 7. oktober 2023.

### Nøkkeltal

| Metrikk | Verdi |
|---------|-------|
| Total eksponering | ~$208 milliardar |
| Vekta gjennomsnittleg eigarskap | ~1,16% |
| Høgaste eigarposisjon | Microsoft: 3,8% ($43,8 mrd) |
| Identifiserte selskap | 48+ |
| Ekskluderte selskap (markedsverdi) | ~$732 milliardar |
| Palantir-auke 2023-2024 | 15x |

### Det strukturelle paradokset

SPU eig nesten **4 gonger meir** av sky-infrastrukturen (Microsoft) som husar måldataene enn det fondet eide av bulldoserane (Caterpillar) som jevna heimane med jorda.

## Kill Chain-arkitekturen (F2T2EA)

```
FIND → FIX → TRACK → TARGET → ENGAGE → ASSESS
 │      │      │        │        │        │
 │      │      │        │        │        └─ Cloud Analytics
 │      │      │        │        └─ Våpen, Fly, Bulldoserar
 │      │      │        └─ Kommando & Kontroll (C4I)
 │      │      └─ AI-algoritmar (Lavender, Gospel)
 │      └─ Cloud Computing, Datasjøar
 └─ Overvaking, Droner, Biometri
```

### SPU-eigarskap per fase

| Fase | Funksjon | Hovudselskap | SPU-eigarskap |
|------|----------|--------------|---------------|
| **FIND** | Overvaking, biometri | Motorola, LIG Nex1, Meta | 1,8-2,5% |
| **FIX** | Cloud computing | Microsoft, Google, Amazon | **2,5-3,8%** |
| **TRACK** | AI-targeting | Microsoft, Palantir, NVIDIA | ~1,8% |
| **TARGET** | C4I | Cisco, Broadcom | 1,2-1,6% |
| **ENGAGE** | Kinetisk | RTX, Valero | 1,0-1,1% |
| **ASSESS** | Analyse | Google, Amazon | 1,8% |

## Prosjektstruktur

```
nbim-killchain/
├── data/
│   ├── companies.json      # Selskapsdata med kjeldereferansar
│   ├── kill_chain.json     # Kill chain-faser og system
│   ├── sources.json        # Kjelderegister
│   └── research_plan.json  # Automatisert research-plan
├── scripts/
│   ├── analyze_ownership.py        # Eigarskapsanalyse
│   ├── research_config.py          # Research-konfigurasjon
│   └── generate_visualizations.py  # Visualiseringar
├── assets/js/
│   ├── data.js             # Frontend-data med kjelder
│   └── main.js             # Applikasjonslogikk
├── ressursar/              # PDF-ar og diagram
├── index.html              # Dashboard
├── killchain.html          # Kill chain-visualisering
└── companies.html          # Selskapsoversikt
```

## Datastruktur med kjeldereferansar

All data i prosjektet har direkte kopling til verifiserbare kjelder:

```json
{
  "id": "msft",
  "name": "Microsoft",
  "nbim_pct": 3.8,
  "value_usd": 43800000000,
  "role": "Azure MoD-kontrakt, Unit 8200, Project Nimbus",
  "sources": ["nbim_holdings_2023", "972mag_nimbus"]
}
```

## Hovudkjelder

### Offisielle kjelder
- [NBIM Årsrapport 2023](https://www.nbim.no/en/news-and-insights/reports/2023/annual-report-2023/)
- [NBIM Eksklusjonsliste](https://www.nbim.no/en/responsible-investment/exclusion-of-companies/)
- [SEC EDGAR 13F-filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=norges+bank&type=13F)

### FN-dokumentar
- [A/HRC/59/23 "From Economy of Occupation to Economy of Genocide"](https://www.ohchr.org/sites/default/files/documents/hrbodies/hrcouncil/sessions-regular/session59/advance-version/a-hrc-59-23-aev.pdf) - Francesca Albanese, juni 2025

### Undersøkande journalistikk
- [+972 Magazine: Lavender AI-system](https://www.972mag.com/lavender-ai-israeli-army-gaza/)
- [+972 Magazine: Project Nimbus](https://www.972mag.com/project-nimbus-contract-google-amazon-israel/)
- [The Guardian: The Gospel](https://www.theguardian.com/world/2023/dec/01/the-gospel-how-israel-uses-ai-to-select-bombing-targets)

### NGO-rapportar
- [Who Profits: Cisco Systems](https://www.whoprofits.org/companies/company/6529?cisco-systems)
- [Who Profits: Motorola Solutions](https://www.whoprofits.org/companies/company/3808)
- [Amnesty: Facial Recognition](https://www.amnesty.org/en/latest/news/2023/05/israel-opt-israeli-authorities-are-using-facial-recognition-technology-to-entrench-apartheid/)
- [Human Rights Watch: Digital Tools in Gaza](https://www.hrw.org/news/2024/09/10/questions-and-answers-israeli-militarys-use-digital-tools-gaza)

## Nøkkelsystem

### AI-målsystem

| System | Funksjon | Mål generert | Kjelde |
|--------|----------|--------------|--------|
| **Lavender** | Menneske-targeting | 37,000+ | [+972](https://www.972mag.com/lavender-ai-israeli-army-gaza/) |
| **The Gospel** | Struktur-targeting | N/A | [Guardian](https://www.theguardian.com/world/2023/dec/01/the-gospel-how-israel-uses-ai-to-select-bombing-targets) |
| **Where's Daddy?** | Geolokalisering | N/A | [+972](https://www.972mag.com/lavender-ai-israeli-army-gaza/) |

### Project Nimbus

$1,2 milliardar-kontrakt mellom Google/Amazon og israelske myndigheiter for sky-infrastruktur.

- **Leverandørar**: Google Cloud, AWS
- **SPU-eigarskap**: Google 2,1%, Amazon 1,6%
- **Kjelde**: [Wikipedia](https://en.wikipedia.org/wiki/Project_Nimbus), [+972 Magazine](https://www.972mag.com/project-nimbus-contract-google-amazon-israel/)

## Research-automatisering

Prosjektet inkluderer konfigurasjon for automatisert research:

```python
# scripts/research_config.py
from research_config import get_priority_queries, export_research_plan

# Hent høgprioritets research-oppgåver
queries = get_priority_queries(max_priority=1)

# Eksporter plan for parallelle agentar
export_research_plan("data/research_plan.json")
```

### Research-prioritetar

1. **Prioritet 1**: NBIM holdings, SEC 13F, Project Nimbus, Lavender, Palantir
2. **Prioritet 2**: Wolf Pack, Cisco, Motorola, Ghost Robotics
3. **Prioritet 3**: Halvleiar-forsyningskjede, drivstoff

## Installasjon og bruk

```bash
# Klon repo
git clone https://github.com/[username]/nbim-killchain.git
cd nbim-killchain

# Installer avhengigheiter (Python)
pip install -r requirements.txt

# Køyr eigarskapsanalyse
python scripts/analyze_ownership.py

# Generer research-plan
python scripts/research_config.py
```

## Metodologi

### Eigarskapsberekningar

1. **Direkte eigarskap**: SPU prosentdel av utestående aksjar
2. **Verdi**: Aksjeposisjon × aksjekurs
3. **Kill chain-mapping**: Selskap → Produkt → Fase i kill chain

### Begrensningar

1. **Attribusjonusikkerheit**: Kva produkt brukast faktisk i targeting?
2. **Inntektsallokering**: Project Nimbus er ~0,05% av Google Cloud-omsetning
3. **Dual-use**: Hardware tener sivile/militære formål globalt
4. **Kapitalfungibilitet**: Om SPU sel, overtek andre investorar

## Tidslinje

| Dato | Hending |
|------|---------|
| Apr 2021 | Project Nimbus signert |
| Sep 2009 | Elbit ekskludert |
| 7. okt 2023 | Gaza-krigen startar |
| Jan 2024 | Palantir-IDF partnarskap |
| Sep 2024 | General Dynamics ekskludert |
| Okt 2024 | Storebrand sel Palantir |
| Aug 2025 | Caterpillar ekskludert |
| Nov 2025 | Etikkrammeverket suspendert |

## Lisens

MIT License - Sjå [LICENSE](LICENSE)

## Bidrag

Bidrag er velkomne! Sjå [CONTRIBUTING.md](CONTRIBUTING.md) for retningslinjer.

## Kontakt

For spørsmål eller samarbeid, opne ein issue på GitHub.

---

*Dette dokumentet er meint som ei oversikt for forskingsformål. Alle tal er estimat basert på tilgjengelege kjelder.*
