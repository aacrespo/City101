# CONTEXT — City101 Working State
**Last updated:** 2026-03-02 early AM (Cairn, Session 10 — post S9 + Lumen S8.1-S8.3)
**Read this first every session.**

---

## What is this project?

EPFL BA6 Architecture studio (AR-302k, Studio Huang — "Sentient Cities"). Andrea analyzes the Geneva–Villeneuve corridor (City101) through the lens of "flow of people" — what makes people stop, where infrastructure creates behavior, and whether this 101km strip functions as one continuous city.

Teammate: Henna Rafik (transit ridership, psycho-comfort, thermal flows, gap hours). She also uses the handoff system.

## Current narrative direction

**"Infrastructure for working continuity as a flow."** Teacher-endorsed as of 24-02.

The argument: City101's status as a city can be tested by whether a knowledge worker can maintain an unbroken work session while traversing the corridor. Five dimensions of breakage: connectivity drops, no workspace, temporal lockout, transit gaps, comfort failure.

**Key finding (01-03):** The linear city doesn't exist. It's an **archipelago** — only 11 of 49 stations (22%) maintain full working continuity. Three structural gaps: Nyon→Gland (19.3km), Gland→Morges (20km), and the Lavaux Fracture (17.5km).

**Second finding:** There are **two corridors on the same tracks**. IC passengers experience a workable linear city (WiFi, tables, quiet car). S-Bahn passengers experience fragmented villages (doors every 90sec, no WiFi). 85% of connections are not workable.

**Third finding (new S6-S7):** The corridor is a **different city depending on who you are**. GA holders treat 101km as one city (CHF 10.50/day). Non-GA holders experience fragmentation (CHF 26 Geneva→Lausanne). Frontaliers (~100k in Geneva canton) can't even buy GA. The gig economy follows tourists, not commuters. Religious diversity correlates with urban completeness. The frequency-amenity paradox stations are the intervention sites.

**EV charging = supporting evidence only.** The working continuity narrative is about the universal commuter/knowledge worker, not the EV driver subset.

**Fourth finding (confirmed, S8.1-S8.3 — Lumen):** **Diversity creates unity — quadruple-validated.** Religious Shannon, modal Shannon, cuisine Shannon, and economic category diversity ALL converge on the same pattern (r = 0.63–0.71). Phase transition at Shannon ≈ 1.0: below it, avg richness 8.8; above, 70.5 (8× jump). Four independent indices prove the Lavaux Fracture is a *systemic diversity collapse*, not just a transit gap. Architectural inversion: prototypology at break points should introduce *difference*, not fill deficits. The deficit is the asset. Two anomaly sites identified: Vernier-Blandonnet (diversity without programming) and Coppet (programming without diversity) — potential intervention sites.

**Fifth finding (S8.3 — Lumen):** **160,000 ghost citizens.** Combined GE + VD frontaliers exceed Lausanne's population. Present in daytime economy, invisible in every diversity metric, can't buy GA, vanish at 18:00. The corridor's diversity is time-dependent — Henna's night city is literally a city without its daytime workforce. The frontalier blind spot connects GA pricing (Point 3), temporal analysis (Point 2), and diversity (Point 4) into a single argument.

**Narrative draft exists:** `deliverables/A02_NARRATIVE_DRAFT.md` (Lumen, 731 words). Title: "The Archipelago." Needs Andrea + Henna refinement tomorrow AM.

## ⚠️ TODO — Monday March 2nd morning

1. **CHECK LAYOUTS VISUALLY** — all 7 A02 layouts ready to export but labels may be truncated. Open each in QGIS layout manager, verify text isn't cut off, export as PDF to `maps/`
2. Decide: add GA_Cost_Corridor + temporal layers to existing layouts or create MAP8/MAP9?
3. **Refine narrative draft** with Henna — current draft (731 words) needs: diversity findings, temporal confirmation, frontalier argument. Consider v2 or integrated update.
4. ~~Get first/last train data~~ ✅ Done in S9
5. Upload final PDFs + narrative to team Drive (see `research/DRIVE_STRUCTURE.md`)
6. **Build interactive HTML visualizations** via Claude Code (see spec in `prompts/VIZ_SPEC_CLAUDE_CODE.md`)
7. Load temporal WCI + modal diversity into QGIS as layers

## Visualization Plan — Interactive Artifacts (last step, after all data is computed)

**Purpose**: Data too relational, temporal, or multi-dimensional for print maps gets presented as interactive HTML/React. For the desk crit: open on a laptop alongside printed maps.

**Candidates** (in priority order):
1. **Temporal WCI pulse** — time-slider showing corridor at 7 time slots. THE signature piece if Point 2 delivers.
2. **GA cost curve** — price vs distance with budget threshold lines (CHF 10/15/20). Clearer than colored map dots.
3. **Zurich comparison dashboard** — side-by-side metrics. Two geographies can't share a map but can share a visualization.
4. **Station crossref heatmap** — 49 stations × 12 classmate dimensions. Sortable, hoverable, filterable.
5. **Shannon vs richness/CI scatter** — interactive scatter with station labels on hover. Quick to build.
6. **Journey workability explorer** — 618 connections, filterable by departure station. Too dense for print.
7. **Interactive corridor map** — if we do this, use EXACT coordinates and correct geometry (not schematic). Leaflet.js or similar with real basemap.

**Format decision**: Standalone HTML files (single .html with embedded JS/CSS). Reasons:
- Portable: open in any browser, no server needed
- Presentable: works at crit on a laptop
- Archivable: one file, no dependencies
- Can embed real map tiles (Leaflet + Swiss topo) for geographic accuracy
- React artifacts are faster to prototype but less portable

**When**: After Point 2 (temporal) data exists and all analysis is done. This is presentation layer, not analysis.

## Active assignment

**A02 — Data Synchronicity** — Desk crit: **Monday March 2nd, 1pm**. Submission deadline March 3rd.
Deliverables: narrative + index formula + updated maps + Zurich comparison + point cloud sections (week 2)

## Folder structure

```
~/CLAUDE/City101_ClaudeCode/
├── CONTEXT.md, LEARNINGS.md, TODO_4_POINTS.md   (entry points)
├── CITY101_WORKING.qgz                          (QGIS project, 52 layers)
├── datasets/                                     (OUR produced data — share from here)
│   ├── corridor_analysis/  (WCI, break points, journey workability, crossref, GA cost, temporal, modal diversity + findings)
│   ├── ev_charging/        (enriched v3, reviews, national stats)
│   ├── remote_work/        (places, hours, reviews, crossref, wifi, cell towers, anchors)
│   ├── transit/            (frequency, ridership, shared mobility, raw SBB)
│   ├── stations/           (ratings, reviews)
│   └── zurich_comparison/  (S8 lakeside comparison, metrics, findings — Lumen)
├── handoffs/               (ONLY handoffs: S1-S9 + S8.0-S8.3 Lumen + team handoff)
├── prompts/                (execution prompts for Cairn/Lumen sessions)
├── deliverables/           (A02 narrative draft, final submission documents)
├── scripts/                (7 monolithic Python scripts)
├── research/               (trawl data, inventory, diversity research docs — Lumen, layout review, drive structure)
├── maps/                   (empty — for exported PDFs tomorrow morning)
├── archive/                (old screenshots, obsolete outputs, old session states)
├── source/                 (FROZEN — classmate data, GeoPackages, raw inputs)
└── output/                 (staging — empty when clean)
```

See `research/DRIVE_STRUCTURE.md` for team Drive upload checklist.

## Datasets — what exists

### Corridor analysis (the core)
| Dataset | File | Rows × Cols | Key info |
|---------|------|-------------|----------|
| WCI segments | corridor_segments_WCI.csv | 49×10 | Working Continuity Index. Range: 0.0003 (St-Saphorin) → 0.6431 (Genève) |
| Break points | break_points.csv | 49×~15 | 5 break dimensions, severity classification. Only 11/49 continuous. |
| Journey workability | journey_workability.csv | 618×~20 | Per-connection: 15% PRIME, 12% WORKABLE, 39% MARGINAL, 32% NOT_WORKABLE |
| Journey summary | journey_workability_summary.csv | 35×~10 | OD pair aggregates |
| Train workability | train_workability.csv | 49×~8 | IC/IR vs R/S ratio per station |
| **Classmate crossref** | station_crossref_classmates.csv | 49×46 | **NEW S7.** 2,093 points from 33 datasets. Station richness, religious Shannon diversity. |
| **GA cost OD pairs** | ga_cost_od_pairs.csv | 35×11 | **NEW S8.** Full/halbtax/GA prices for 35 OD pairs. Cost ratio vs GA. |
| **GA cost corridor** | ga_cost_corridor.csv | 49×14 | **NEW S8.** Cumulative cost from Geneva per station. Budget threshold flags (CHF 10/15/20). |
| **Zurich comparison** | zurich_sbahn_comparison.csv | 12×18 | **NEW S8 (Lumen).** 12 S8 lakeside stations with City101 analog pairings. |
| **Zurich metrics** | zurich_comparison_metrics.csv | 15×5 | **NEW S8 (Lumen).** 15 structural comparison metrics. |
| **Temporal frequency** | city101_temporal_frequency.csv | 49×28 | **NEW Cairn S9.** 7 time slots, trains/hr + IC + deps per slot. |
| **Temporal WCI** | city101_temporal_WCI.csv | 49×~50 | **NEW Cairn S9.** TWCI per station × 7 slots + first/last trains. |
| **Temporal summary** | city101_temporal_summary.csv | 7×16 | **NEW Cairn S9.** Per-slot aggregates, workable counts. |
| **First/last trains** | city101_first_last_trains.csv | 49×10 | **NEW Cairn S9.** Service windows: 0h (St-Saphorin) to 21.3h (Genève). |
| **Modal diversity** | city101_modal_diversity.csv | 49×17 | **NEW Lumen S8.2.** 11 transport mode types, modal Shannon. r=0.626 vs religious Shannon. |

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

### WMS layers in QGIS (national coverage incl. Zurich)
Rail noise day/night, road noise day/night, EV 2035 projections (3 scenarios), home charging 2035 (3 scenarios), EV fleet 2035, electricity demand.

### Classmate data in source/ (33 datasets integrated into crossref)
- **Charlene Dejean**: gig work (50), rooftops (27)
- **Thomas Riegert**: hospitals (23), clinics (68), GPs (110), specialists (188), religious buildings (204), religious communities (274), esoteric (43)
- **Siméon Pavicevic**: industrial zones (25), companies (195)
- **Marek Waeber**: schools (199), grocery stores (121)
- **Vladislav Belov**: acoustic ecology (49)
- **Henna Rafik**: UHI zones (203), thermal comfort (33)
- **Mohamad Ali**: restaurants (150), informal learning (132)

## Key numbers

- **42x frequency variation**: Lausanne 28.5 tr/hr (2 min wait) → St-Saphorin 0.0
- **11/49 stations continuous** (22%): the rest are break points of varying severity
- **85% of connections not workable**: IC = office, S-Bahn = fragmented
- **277 vs 0**: Lausanne-Flon classmate features within 1km vs Palézieux
- **All 10 denominations** at Genève-Champel (Shannon 2.12) — diversity = completeness
- **Vernier Blandonnet**: 84 trains/hr, richness = 7. Busiest nothing.
- **CHF 26 vs CHF 10.50**: Geneva→Lausanne full price vs GA daily amortized (2.5x)
- **~100k frontaliers**: Ghost citizens who can't buy GA
- **CHF 20 budget = 41km city**: Corridor ends at St-Prex, 12km short of Lausanne
- **GA breakeven: 85 trips (4.2 months)**: Geneva-Lausanne daily commuters
- **2.1–2.5x cost ratio**: Full price vs GA across the corridor
- **6x short-hop penalty**: CHF 2.57/km for Lancy hops vs CHF 0.39/km for full corridor
- **42× vs 12×**: City101 frequency variation is 3.5× wider than Zurich's S8 lakeside line
- **0 vs 2/hr**: City101 minimum frequency (St-Saphorin) vs Zurich minimum (Oberrieden, 11km from center)
- **14/49 at peak, 13/49 at 11pm**: The archipelago barely pulses — structural, not temporal
- **21.3h vs 0h**: Geneva service window vs St-Saphorin — total temporal inequality
- **128 → 72 IC trains**: Peak vs late-night — the fast corridor halves
- **0.90×**: Weekend-to-weekday WCI ratio — the corridor shrinks on Saturday
- **r = 0.632**: Shannon diversity vs station richness — diversity predicts amenities 3.6× better than transit frequency
- **r = 0.708**: Economic categories vs Shannon — strongest correlation in the analysis
- **r = 0.626**: Modal Shannon vs religious Shannon — transport diversity tracks social diversity
- **Shannon 1.0 threshold**: Below it, avg richness 8.8. Above it, 70.5 (8× jump). Phase transition.
- **160,000 frontaliers**: Combined GE + VD daily crossings — larger than Lausanne's population
- **Geneva 50% → Rivaz 12.5%**: Foreign resident share collapse along corridor (3.4×)
- **Cuisine Shannon 2.03 (Geneva) → 1.50 (Chexbres)**: Diversity visible on the plate

## Critical gaps (priority order)

1. ~~GA cost map~~ — ✅ DONE (S8)
2. ~~First/last train~~ — ✅ DONE (S9)
3. ~~Zurich comparison~~ — ✅ DONE (S8, Lumen)
4. ~~Temporal corridor~~ — ✅ DONE (S9)
5. ~~Diversity research~~ — ✅ DONE (Lumen S8.1-S8.3)
6. **QGIS map export** — 7 layouts exist, need visual check + export + new layouts for temporal/GA/crossref. 🟡 MONDAY AM
7. **Narrative v2** — draft exists (731 words), needs temporal + diversity + frontalier integration. 🟡 WITH HENNA
8. **Interactive visualizations** — All 7 viz built ✅ (viz_01 GA Cost, viz_02 Temporal Pulse, viz_03 Diversity, viz_04 Zurich, viz_05 Station Explorer, viz_06 Journey Workability, viz_07 Narrative Scroll). 🟢 COMPLETE
9. **Load new layers** — temporal WCI, modal diversity, GA cost need QGIS styling. 🟡 CAIRN NEXT

## Maps — current state

7 print layouts in QGIS (A1 landscape), **not yet reviewed or exported**:
- WCI hero map (the archipelago)
- Remote work infrastructure
- Lavaux Fracture zoom
- Geneva pole
- Lausanne pole
- Transit backbone
- Data synchronicity (all layers)

Need to add: GA cost gradient, classmate cross-reference / station richness, break point classification, temporal WCI (7-slot series or temporal pie charts).

## The 4 investigations (from TODO_4_POINTS.md)

### Point 1: Break Point Map ✅ DONE
49 stations classified by severity. Five break dimensions. Frequency-amenity paradox identified. Classmate crossref adds 33-dataset richness scoring.

### Point 2: Temporal Corridor ✅ DONE
Multi-slot frequency (49 stations × 7 time slots), first/last trains (service windows), temporal WCI computed. Key finding: the archipelago is structural, not temporal — only 13-14 stations workable regardless of time. 11pm city = 13 stations. IC trains halve at night (128→72). Weekend 10% less workable. Lavaux Fracture never opens. St-Saphorin has zero service.

### Point 3: GA Hypothesis ✅ DONE
Cost map computed (distance-based tariff, ±CHF 2-3). CHF 20 budget = 41km city. GA breakeven at 85 trips. 2.1-2.5x cost ratio. Short-hop penalty 6x. Frontalier blind spot documented. Zurich comparison completed (Lumen).

### Point 4: Station Reviews ✅ DONE
37 new stations rated, 71 reviews tagged. Key finding: zero "work_friendly" mentions — the station-as-workspace is invisible to users.

### How they connect
Reviews (4) → break quality (1) → varies by time (2) → experienced by ticket type (3). Together: "If you are THIS person at THIS time, here is where the city breaks."

## Infrastructure — how we work

### Accounts
- **Cairn** (personal, Max plan): Primary workhorse. Usually on desktop with MCP.
- **Lumen** (school team): Lower limits. Overflow / parallel tasks.
- Both have Google Places access as of 28-02.

### Henna's accounts
- **Meridian** (school): Henna's analytical work
- **Cadence** (personal, Pro): Not yet used

### Key files for any new session
1. This file (CONTEXT.md)
2. LEARNINGS.md — accumulated insights
3. Latest handoff — `handoffs/HANDOFF_01-03_S10.md` (Cairn) + `S8.3` (Lumen)
6. Layout review — `research/LAYOUT_REVIEW_01-03.md`
7. Prompts for next sessions — in `prompts/` folder
4. Team handoff — `handoffs/TEAM_HANDOFF_01-03_S1.md`
5. TODO_4_POINTS.md — the 4 investigations framework

### Coordinate system
Always LV95 / EPSG:2056. Source data often WGS84 — convert before QGIS loading.

## Theoretical references

- **Comtesse**: diversity × accessibility × time = urban vitality. **Quadruple-validated** — religious, modal, cuisine, and economic diversity all correlate with station richness (r = 0.63–0.71). Phase transition at Shannon ≈ 1.0.
- **Deleuze**: significance of surface — data flows ARE the urban reality
- **Fractal principle**: every part expresses the whole — one station = corridor logic
- **"Infrastructure creates behavior"**: charge speed dictates dwell time, WiFi coverage determines work locations, temporal accessibility shapes spatial programs
