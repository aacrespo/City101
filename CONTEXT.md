# CONTEXT — City101 Working State
**Last updated:** 2026-03-18 (Cairn Code — concept update post-crit + v2 paper)
**Read this first every session.**

---

## What is this project?

EPFL BA6 Architecture studio (AR-302k, Studio Huang — "Sentient Cities"). Andrea analyzes the Geneva–Villeneuve corridor (City101) through the lens of "flow of people" — what makes people stop, where infrastructure creates behavior, and whether this 101km strip functions as one continuous city.

Teammate: Henna Rafik (transit ridership, psycho-comfort, thermal flows, gap hours, healthcare sites). She also uses the handoff system.

## Current phase

- **A01** (data collection): ✅ complete
- **A02** (data synchronicity): ✅ submitted March 3rd. Crit happened March 2nd.
- **A03** (field data): ✅ complete. All 7 sites visited March 10. On-site interviews blocked (staff referred to central offices). Deliverables submitted.
- **A04** (forms of sentience): ⚠️ active — due March 30 (midterm). Rhino MCP prototypology. AI workflow diagram v1 built. **March 16 crit: green light from Huang + assistants. Called it cutting edge, offered to fund Max subscription.** Now in full production toward midterm.

See `briefs/` for full assignment specs and PPTX template.

## Current narrative direction

### A02 narrative: The Archipelago
**"Infrastructure for working continuity as a flow."** Teacher-endorsed as of 24-02.

The linear city doesn't exist. It's an **archipelago** — only 11 of 49 stations (22%) maintain full working continuity. Five key findings:

1. **Three structural gaps**: Nyon→Gland (19.3km), Gland→Morges (20km), Lavaux Fracture (17.5km)
2. **Two corridors on same tracks**: IC = workable office; S-Bahn = fragmented villages. 85% of connections not workable.
3. **Different city depending on who you are**: GA holders (CHF 10.50/day) vs full price (CHF 26 GE→LS). ~160k frontaliers can't buy GA.
4. **Diversity creates unity** (quadruple-validated): Religious, modal, cuisine, economic Shannon all correlate (r = 0.63–0.71). Phase transition at Shannon ≈ 1.0.
5. **160,000 ghost citizens**: Frontaliers exceed Lausanne's population, invisible in every metric, vanish at 18:00.

**Narrative deliverables**:
- `deliverables/A02_NARRATIVE_DRAFT.md` (731 words, "The Archipelago")
- `deliverables/A02_SPEECH_UNIFIED.md`
- Karim's diary (`karim_diary_v4.md` — Henna/Cadence, stream-of-consciousness narrative device)

### A04 narrative: The Horizontal Elevator — Infrastructure That Holds the Gap

**Core thesis**: The vertical elevator is anti-architecture (changes the relationship of proportionality — a small elevator enables radically different usage per floor, beyond what architectural proportions consider realistic). The horizontal elevator is **anti-urban**: it changes hierarchy along the corridor. What "breaks" a vertical elevator is a power outage. What breaks the horizontal elevator is **the gap in the 24hr chain** (01:30–03:30, zero public transport on weekdays).

**The chamber is NOT a backup generator.** A generator restores the same thing. The chamber is the **missing link** — it doesn't restore, it fills. Unlike technology that eliminates gaps or makes things faster/obsolete, **this typology holds the gap**. It designs the experience of waiting. Infrastructure that doesn't want to skip the gap, doesn't want to make it disappear. The equalizer.

**Chamber = waiting infrastructure** that transports/holds people AND expresses the information and coordination between nodes. A threshold space managing transition between two states, using the canal lock's 5-stage sequence (entry, sealing, equalization, level-matching, exit). The dwell time IS the architecture.

**Prototypology: The Relay-Lock**
- **Relay** (system level): chain of 9 nodes along corridor (~11km spacing, caravanserai logic)
- **Lock** (building level): architecture managing threshold between two states
- **Chamber**: the architectural space where transition happens (01:30–03:30 dead window)
- **Four circulations**: staff + patient + cargo + home care (AVASAD/IMAD field workers doing 6–10 stops per shift)

**Beyond healthcare**: The typology is "infrastructure for waiting" — applies to ANY community with breaks in the 24hr chain. Healthcare is the proof-of-concept. Other communities: bakeries (early shifts, lab-to-shop transport), any industry with non-standard working hours at the 01:30–03:30 breaking point. The interface/app vision extends the typology to any community, any region, eventually any city with equivalent data.

### The 9-node healthcare circuit (v2, scored)

v2 introduced a quantitative scoring framework: 24 candidate sites evaluated on 5 criteria (night worker count, healthcare chain criticality, modal collapse severity, gap distance, infrastructure readiness). Top 9 scored above 3.0.

| Node | Site | km | Lock type | Chamber program |
|------|------|----|-----------|-----------------|
| 1 | **Lancy-Pont-Rouge** | 4 | Border lock | Frontalier equalization + cross-border dispatch |
| 2 | **Geneva North Industrial Belt** | 8 | Cargo ↔ Visibility | Logistics interface + pharma + airport |
| 3 | **Nyon + Genolier** | 25 | Altitude lock | Valley–hilltop connector + staff/patient dual use |
| 4 | **Morges** | 48 | Temporal lock | Dead window shelter (01:07–04:01) + Nine Hours Hotel model |
| 5 | **Crissier-Bussigny-Ecublens** | 58–62 | Logistics engine | Machine room exposed as civic infrastructure |
| 6 | **Lausanne CHUV** | 65 | Sky lobby + gradient | Dispatcher + income-transport paradox corrector |
| 7 | **Vevey** | 80 | Gap relay | Intermediate lock (Panama water-saving basin) |
| 8 | **Montreux-Glion** | 85 | Altitude lock | Funicular base + family/rehab access |
| 9 | **Rennaz** | 89 | Bridge lock | Off-rail corrective (2.1km from Villeneuve station) |

**Why 9 (brief says 3–5):** One healthcare circuit, not 9 separate projects. Remove any node and the chain breaks. Three permanent geographic voids: Nyon→Gland (19.3km, no-ER zone), Gland→Morges (20km, La Côte blind spot), Lavaux Fracture (17.5km, UNESCO-constrained, permanent TOTAL RUPTURE — explicitly not solved by chambers, routed around).

**Key references**: Koolhaas (anti-architecture, programmatic discontinuity), canal locks (5-stage threshold sequence), caravanserai spacing (~11km for motorized travel), airlock asymmetry (fast in, slow out = dwell time), genkan (GA tap-in as entry marking).

### What's defined vs open (as of March 18)

**Defined**: 9 node locations + scoring framework, lock-sequence logic, four circulation types, healthcare chain failures mapped (emergency, pharmacy, staffing), weekday dead window (01:30–03:30), income-transport paradox at CHUV, frontalier dual inversion, three permanent geographic voids.

**Open**: Exact architectural form of chambers, how nodes coordinate/dispatch, bus bay integration, pharmaceutical micro-dispensing, power source (solar/water/electric/fuel), construction logistics (vents, water, drainage, electricity), cadastre integration for buildable land, is it actual transport or just a place, what are fixed vs flexible variables in the typology.

## TODOs and session logs

Per-person priorities, TODOs, data gaps, and session logs live in:
- **CONTEXT_ANDREA.md** — Andrea's working context
- **CONTEXT_HENNA.md** — Henna's working context

This avoids merge conflicts and keeps this file focused on shared project state.

## Visualizations — complete set

### Interactive HTML (standalone, in `visualizations/`)
| Viz | File | Status |
|-----|------|--------|
| GA Cost Curve | viz_01_ga_cost.html | ✅ |
| Temporal Pulse | viz_02_temporal_pulse.html | ✅ |
| Diversity | viz_03_diversity.html | ✅ |
| Zurich Comparison | viz_04_zurich.html | ✅ |
| Station Explorer | viz_05_station_explorer.html | ✅ |
| Journey Workability | viz_06_journey_workability.html | ✅ |
| Narrative Scroll | viz_07_narrative_scroll.html | ✅ |
| Presentation | viz_08_presentation.html | ✅ |
| Demographics | viz_09_demographics.html | ✅ |

### Diagrams (in `visualizations/`)
- `city101_clock_diagram.html` — 24h clock
- `city101_marey_diagram.html` — Marey train diagram
- `city101_spacetime_diagram.html` — space-time

### Scrollytelling site (in `visualizations/site/`)
- `index_v2.html` — 7 interactive Leaflet maps replacing static QGIS images
- `city101_maps.js` — shared map module
- `city101_geodata.js` — inlined GeoJSON for file:// compatibility
- 7 PNGs (150 DPI) + 7 PDFs (300 DPI) in `site/maps/`

### Animation maps (in `deliverables/A03/`)
- `train_pulse_24h.html` — 24h train animation (v1, rail only, 860 trips)
- `map2_passenger_flow.html` — ridership-sized train dots
- `city101_standalone.html` — standalone corridor map

### Transport Pulse v3 (in `output/transport_pulse_v2/`, pending promotion)
- `transport_pulse_24h_v2.html` — **multimodal** 24h animation (29,135 trips)
- All modes: rail, bus, tram, metro, ferry, funicular, noctambus
- MapLibre GL JS with 3D terrain, two render modes (dot/vector)
- Collapsible analytics sidebar (donut, sparkline, mode bars, direction, pulse)
- Shape-coded symbology, keyboard-driven interactivity
- Feature log: `output/transport_pulse_v2/FEATURES_LOG.md`
- Known issue: basemap tile transparency creates distracting terrain patches

## Animation data pipeline

Phase 1 data validated, promoted to `source/animation/`:

| File | Rows | Key info | Version |
|------|------|----------|---------|
| `gtfs_corridor_trains_interpolated.csv` | 39,695 | 860 trips, per-minute positions, 5 line categories | v2 |
| `station_ridership_v2.csv` | 49 | 49 unique hourly curves, 10 profiles | v2 |
| `corridor_demographics_v2.csv` | 49 | 42 unique age profiles, commune-level | v2 |
| `corridor_rail_lines_v3.geojson` | 19 features | CEVA included, Genève=standard_gauge | v3 |
| `corridor_station_distances_v3.csv` | 49 | 0–105km, monotonic, snap quality classified | v3 |
| `gtfs_corridor_stops.csv` | 49 | Station coords | v1 |

Agent scripts in `scripts/animation/` (12 files). Known limitations:
- Ridership hourly curves are **modeled** (no public SBB hourly data exists)
- Bex snap=14km, Aigle snap=6.3km (SwissTLM3D doesn't extend there)
- Demographics commute mode may be Strukturerhebung estimates

## Maps — current state

7 print layouts in QGIS (A1 landscape), exported with dark backgrounds (#0a0a0f):
- WCI hero map (the archipelago)
- Remote work infrastructure
- Lavaux Fracture zoom
- Geneva pole
- Lausanne pole
- Transit backbone
- Data synchronicity (all layers)

Still need: GA cost gradient, classmate crossref / station richness, break point classification, temporal WCI, **7-site relay-lock network map**.

## Datasets — what exists

### Corridor analysis (the core)
| Dataset | File | Rows × Cols | Key info |
|---------|------|-------------|----------|
| WCI segments | corridor_segments_WCI.csv | 49×10 | Working Continuity Index. Range: 0.0003 (St-Saphorin) → 0.6431 (Genève) |
| Break points | break_points.csv | 49×~15 | 5 break dimensions, severity classification. Only 11/49 continuous. |
| Journey workability | journey_workability.csv | 618×~20 | 15% PRIME, 12% WORKABLE, 39% MARGINAL, 32% NOT_WORKABLE |
| Journey summary | journey_workability_summary.csv | 35×~10 | OD pair aggregates |
| Train workability | train_workability.csv | 49×~8 | IC/IR vs R/S ratio per station |
| Classmate crossref | station_crossref_classmates.csv | 49×46 | 2,093 points from 33 datasets. Station richness, religious Shannon. |
| GA cost OD pairs | ga_cost_od_pairs.csv | 35×11 | Full/halbtax/GA prices for 35 OD pairs |
| GA cost corridor | ga_cost_corridor.csv | 49×14 | Cumulative cost from Geneva per station |
| Zurich comparison | zurich_sbahn_comparison.csv | 12×18 | 12 S8 lakeside stations with City101 analogs |
| Zurich metrics | zurich_comparison_metrics.csv | 15×5 | 15 structural comparison metrics |
| Temporal frequency | city101_temporal_frequency.csv | 49×28 | 7 time slots, trains/hr + IC + deps per slot |
| Temporal WCI | city101_temporal_WCI.csv | 49×~50 | TWCI per station × 7 slots + first/last trains |
| Temporal summary | city101_temporal_summary.csv | 7×16 | Per-slot aggregates, workable counts |
| First/last trains | city101_first_last_trains.csv | 49×10 | Service windows: 0h (St-Saphorin) to 21.3h (Genève) |
| Modal diversity | city101_modal_diversity.csv | 49×17 | 11 transport mode types, modal Shannon |

### EV charging
| Dataset | File | Rows | Key info |
|---------|------|------|----------|
| Enriched v3 | ev_charging_ENRICHED_v3.csv | 194 | 53 cols, DIEMO + distances + context |
| Reviews | ev_charging_REVIEWS.csv | 109 | Sentiment-tagged |
| National stats | swiss_charging_keyfigures_monthly.csv | 63mo | Monthly cantonal/national stats 2020-2026 |

### Remote work / connectivity
| Dataset | File | Rows | Key info |
|---------|------|------|----------|
| Places | remote_work_places.csv | 68 | Google-sourced with place_ids |
| Hours | remote_work_HOURS.csv | 63 | Opening hours, 14 are 24h, 18 weekdays-only |
| Reviews | remote_work_REVIEWS.csv | 109 | Work-relevance tagged |
| Crossref | remote_work_CROSSREF.csv | 68 | 31 cols: nearest train, frequency, ridership, WiFi, acoustics |
| WiFi | wifi_MERGEDv.2.csv | 81 | Quality scores, categories, clusters |
| Cell towers | cell_towers.csv | 3,218 | 3G/4G/5G BAKOM |
| International anchors | international_anchors.csv | 15 | CERN, UN, IOC, etc. |

### Transit
| Dataset | File | Rows | Key info |
|---------|------|------|----------|
| Service frequency v2 | service_frequency_v2.csv | 49 | Trains/hr, IC vs regional. 42x variation. |
| Ridership | ridership_sbb.csv | 174 | Daily pax, commuter index |
| Shared mobility | shared_mobility.csv | 2,062 | 8 providers, Geneva-heavy |
| Raw SBB | sbb_passagierfrequenz_raw.csv | ~800 | Source file |

### Stations
| Dataset | File | Rows | Key info |
|---------|------|------|----------|
| Ratings | station_ratings.csv | 37 | M2, M1, Léman Express, CGN with Google ratings |
| Reviews | station_REVIEWS.csv | 71 | Tagged by theme. Zero "work_friendly" mentions. |

### Henna's datasets (in source/)
- Late-night venues v3 (133), nocturnal transport stops (146), night workers (51)
- Population distribution 24h, work locations (73), residencies/professions/neighbourhoods (147)
- Buildings classified (218,437), healthcare sites JSX
- UHI zones (203), thermal comfort (33), psycho-comfort, local traditions, cultural circuits

### Classmate data in source/ (33 datasets integrated into crossref)
- **Charlene Dejean**: gig work (50), rooftops (27)
- **Thomas Riegert**: hospitals (23), clinics (68), GPs (110), specialists (188), religious buildings (204), religious communities (274), esoteric (43)
- **Siméon Pavicevic**: industrial zones (25), companies (195)
- **Marek Waeber**: schools (199), grocery stores (121)
- **Vladislav Belov**: acoustic ecology (49)
- **Henna Rafik**: UHI zones (203), thermal comfort (33)
- **Mohamad Ali**: restaurants (150), informal learning (132)

### WMS layers in QGIS
Rail noise day/night, road noise day/night, EV 2035 projections (3 scenarios), home charging 2035 (3 scenarios), EV fleet 2035, electricity demand.

## Key numbers

- **42x frequency variation**: Lausanne 28.5 tr/hr → St-Saphorin 0.0
- **11/49 stations continuous** (22%): the rest are break points
- **85% of connections not workable**: IC = office, S-Bahn = fragmented
- **277 vs 0**: Lausanne-Flon classmate features within 1km vs Palézieux
- **Shannon 1.0 threshold**: Below it, avg richness 8.8. Above it, 70.5 (8× jump)
- **r = 0.63–0.71**: All four diversity indices correlate with station richness
- **160,000 frontaliers**: Ghost citizens, exceed Lausanne population
- **CHF 26 vs CHF 10.50**: GE→LS full price vs GA daily (2.5x)
- **CHF 20 budget = 41km city**: Corridor ends at St-Prex
- **6x short-hop penalty**: CHF 2.57/km for Lancy hops vs CHF 0.39/km full corridor
- **42× vs 12×**: City101 frequency variation 3.5× wider than Zurich's S8
- **14/49 at peak, 13/49 at 11pm**: Archipelago barely pulses
- **01:00–05:00**: The thin window — NOT dead. 188 trips active (38 Noctambus, 83 buses, 31 trams, trains). Real dead zone only ~01:30–03:30
- **21.3h vs 0h**: Geneva vs St-Saphorin service windows

## Repo structure

```
city101/                              (git-tracked, GitHub: aacrespo/City101)
├── CLAUDE.md                         ← router (auto-loaded)
├── CONTEXT.md                        ← YOU ARE HERE — living project state
├── LEARNINGS.md                      ← accumulated pitfalls
├── LOCKBOARD.md                      ← who's doing what
├── CITY101_WORKING.qgz               ← QGIS project (60 layers, EPSG:2056)
├── 00_Workflow_v04.md                ← scale conventions, Rhino rules
├── briefs/                           ← assignment specs (A01-A04) + PPTX template
├── datasets/                         ← verified production data (INVENTORY.md inside)
│   ├── corridor_analysis/
│   ├── ev_charging/
│   ├── remote_work/
│   ├── transit/
│   ├── stations/
│   └── zurich_comparison/
├── source/                           ← FROZEN inputs (classmate data, GeoPackages, animation data)
│   ├── 00-datasets 2/               ← classmate datasets
│   ├── animation/                    ← promoted animation pipeline data (v2/v3)
│   └── ...
├── deliverables/                     ← submission documents
│   ├── A02_NARRATIVE_DRAFT.md
│   ├── A02_SPEECH_UNIFIED.md
│   └── A03/                          ← field visit materials, JSX artifacts, maps
├── handoffs/                         ← all session handoffs (Andrea S1-S11, Henna, team)
├── prompts/                          ← Claude/LLM execution prompts
├── scripts/                          ← processing scripts
│   ├── animation/                    ← 12 agent pipeline scripts
│   └── *.py                          ← ad-hoc processing
├── visualizations/                   ← all interactive viz
│   ├── site/                         ← scrollytelling site (index_v2.html)
│   └── viz_01 through viz_09 + diagrams
├── observations/                     ← INDEX.md + research/ subfolder
├── design_system/                    ← SPEC.md — visual identity
├── tools/                            ← reusable scripts
├── workflows/                        ← step-by-step SOPs
├── output/                           ← staging (hospital research, vertical transport)
├── archive/                          ← historical (system architecture, old outputs, screenshots, QA logs)
└── .claude/                          ← commands, rules, agents
```

## Infrastructure — how we work

### Accounts
| Account | Owner | Type | Capabilities |
|---------|-------|------|-------------|
| Cairn | Andrea | Personal, Max | Primary workhorse. Desktop with MCP. |
| Cairn Code | Andrea | Claude Code CLI | Git-tracked repo. Terminal operations. |
| Lumen | Andrea | School team | Overflow / parallel tasks |
| Meridian | Henna | School | Analytical work (built 24-site artifact) |
| Cadence | Henna | Personal, Pro | Narrative work (Karim's diary) |

### Key files for any new session
1. This file (CONTEXT.md)
2. LEARNINGS.md
3. LOCKBOARD.md
4. Assignment briefs in `briefs/`
5. Latest handoffs — `handoffs/HANDOFF_09-03_S2.md` (latest)

### Coordinate system
Always LV95 / EPSG:2056. Web maps use WGS84. Source data often WGS84 — convert before QGIS.

## Theoretical references

- **Comtesse**: diversity × accessibility × time = urban vitality. Quadruple-validated (r = 0.63–0.71). Phase transition at Shannon ≈ 1.0.
- **Deleuze**: significance of surface — data flows ARE the urban reality
- **Fractal principle**: every part expresses the whole — one station = corridor logic
- **"Infrastructure creates behavior"**: charge speed dictates dwell time, WiFi determines work locations, temporal accessibility shapes spatial programs
- **Horizontal elevator** (Huang): on-demand rail, autonomous module, repurposed tracks. Teacher loves this concept.

