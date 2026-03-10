# TEAM HANDOFF — Andrea + Henna (v2)
**Date**: 2026-03-02, early AM
**From**: Andrea (via Cairn, S10)
**To**: Henna (via Meridian or Cadence)
**Context**: A02 desk crit: **Monday March 2nd, 1pm** · Submission deadline March 3rd

---

## THE SITUATION — 10 hours to crit

All four analytical investigations are complete. The data foundation is deep — 17 datasets in corridor_analysis alone, plus 7 remote work datasets, 4 transit datasets, 3 EV datasets, a full Zurich comparison, and diversity research across four independent indices. We are in the **curation and presentation** phase: what do we print, what do we show live, what's the 2-minute pitch?

### A02 Brief Requirements — Status
| Requirement | Status | Where |
|-------------|--------|-------|
| Clear narrative for your flows | 🟡 Draft exists (731 words), needs v2 with new findings | `deliverables/A02_NARRATIVE_DRAFT.md` |
| Updated maps according to narrative/index | 🟡 7 QGIS layouts ready, need visual check + export + new layers | CITY101_WORKING.qgz |
| Formula for urban potential index | ✅ WCI computed, 5 components, weights justified | `research/city101_WCI_summary.md` |
| Comparison metrics to Zurich | ✅ 12 S8 stations, 15 structural metrics | `datasets/zurich_comparison/` |
| Point Cloud Sections | 🔴 Week 2 deliverable — but need intervention sites identified NOW | — |

---

## OVERLAP AUDIT — What we duplicated and how to handle it

### ⚠️ First/Last Train Per Station
- **Henna was assigned this** in Team Handoff S1 (Priority 1)
- **Cairn completed it** in S9 using transport.opendata.ch API
- **Result**: `city101_first_last_trains.csv` (49 stations × 10 cols — weekday + weekend, service windows 0h to 21.3h)
- **Henna action**: Don't redo this. Use Andrea's data. The "dead window" per station is already computed.

### ⚠️ Temporal Frequency / 24h Analysis
- **Henna planned** a "dead window" map (when the line dies) as part of Night City
- **Cairn completed** full temporal analysis: 49 stations × 7 time slots, temporal WCI per slot
- **Result**: `city101_temporal_WCI.csv`, `city101_temporal_frequency.csv`, `city101_temporal_summary.csv`
- **Key finding**: The archipelago is structural, not temporal — 14/49 workable at peak, 13/49 at 11pm. Almost no variation.
- **Henna action**: This covers the "when does the city die" question from the working continuity side. Henna's unique contribution is the OTHER side: **what happens in the dead window** — night workers, shift patterns, stranded populations, environmental quality. Andrea's data says "13 stations at 11pm." Henna's data should say "and here's who's still out there and what they need."

### ⚠️ Index Overlap
- **Andrea**: Working Continuity Index (WCI) — 5 components, transit-workspace-temporal-connectivity-mobility
- **Henna planned**: 24-Hour Line Vitality Score — daytime workspace quality, evening accessibility, night gap-hour coverage
- **Resolution**: These are complementary, not competing. WCI measures "can you work here?" Henna's vitality score measures "is there life here?" The WCI already has a temporal version (TWCI across 7 slots). Henna's contribution is the environmental/comfort dimension the WCI doesn't capture: thermal comfort, acoustic quality, lighting, safety perception.

### ✅ No Overlap — Henna's Unique Contributions
These are things ONLY Henna has and Andrea hasn't touched:
- **Thermal comfort / UHI data** (203 zones + 33 comfort points) — environmental quality layer
- **Cold air drainage** — nighttime phenomenon, complements temporal analysis
- **Psycho-comfort data** — subjective quality that WCI doesn't measure
- **Night-specific populations** — hospital shift workers, hospitality staff, stranded nightlife (none of this is in Andrea's data)
- **Noctambus / night bus routes** — the alternative network when trains stop
- **Station ridership** (22 CFF stations, daily + workday averages) — already partially integrated

---

## WHAT ANDREA HAS BUILT — Complete Inventory

### The 4 Investigations (all ✅)

**Point 1 — Break Point Map**: 49 stations classified by severity across 5 dimensions. Only 11/49 maintain full continuity. Three structural gaps: Nyon→Gland (19.3km), Gland→Morges (20km), Lavaux Fracture (17.5km). Cross-referenced with 2,093 classmate data points from 33 datasets → station richness scoring.

**Point 2 — Temporal Corridor**: 49 stations × 7 time slots from transport.opendata.ch. First/last trains computed. Temporal WCI shows the archipelago is structural, not temporal. The 11pm city = 13 stations. IC trains halve at night (128→72). Weekend 10% less workable. Lavaux Fracture never opens — even at peak, Rivaz TWCI = 0.013.

**Point 3 — GA Hypothesis**: Distance-based tariff estimation for 35 OD pairs × 3 ticket types. CHF 20 budget = 41km city (St-Prex, 12km short of Lausanne). GA breakeven: 85 trips. 2.1–2.5× cost ratio. Short-hop penalty 6×. ~100k frontaliers can't buy GA = ghost citizens. Zurich comparison: same country, same operator, radial compresses variation (12×) vs linear amplifies it (42×).

**Point 4 — Station Reviews**: 37 stations rated via Google, 71 reviews tagged. Zero "work_friendly" mentions. The station-as-workspace is invisible to users.

### Diversity Research (Lumen, 3 sessions)

Quadruple-validated Comtesse thesis — four independent diversity indices converge:

| Pair | r | Meaning |
|------|---|---------|
| Economic categories vs Religious Shannon | **0.708** | Strongest. Economic monoculture = social monoculture |
| Religious Shannon vs Station richness | **0.632** | Diversity predicts amenities 3.6× better than transit frequency |
| Modal Shannon vs Religious Shannon | **0.626** | Transport diversity tracks social diversity |
| Trains/hr vs Station richness | 0.176 | Frequency alone is a poor predictor |

Phase transition at Shannon ≈ 1.0: below it, avg richness 8.8; above, 70.5 (8× jump). The Lavaux Fracture is a systemic diversity collapse — not just transit, but economic, modal, demographic.

Additional research: 160k frontaliers (ghost citizens), cuisine-migration correlation, anomaly sites (Vernier-Blandonnet: diversity without programming; Coppet: programming without diversity).

### Key Numbers (for the crit)
- **42×** frequency variation (Lausanne 28.5 tr/hr → St-Saphorin 0)
- **11/49** stations continuous (22%) — the rest are break points
- **85%** of train connections not workable (IC vs S-Bahn divide)
- **2,000×** WCI variation (Geneva 0.64 → St-Saphorin 0.0003)
- **CHF 20 budget = 41km city** — ends at St-Prex, 12km short of Lausanne
- **14/49 at peak, 13/49 at 11pm** — the archipelago barely pulses
- **160,000 frontaliers** — larger than Lausanne, invisible in every metric
- **r = 0.63–0.71** — four diversity indices converge on Comtesse's thesis
- **Shannon 1.0 threshold** — below: richness 8.8 avg; above: 70.5 (8× jump)
- **277 vs 0** — Lausanne-Flon classmate features vs Palézieux within 1km

---

## METHODOLOGY — How Each Dataset Was Produced

This section documents reproducibility for the crit and the booklet.

### Working Continuity Index (WCI)
**Formula**: `WCI = 0.30×transit + 0.25×workspace + 0.20×temporal + 0.15×connectivity + 0.10×mobility`
**Unit of analysis**: 49 train stations along the Geneva–Villeneuve corridor
**Sub-scores**: All min-max normalized (0–1) across the 49 stations

| Component | Weight | Data source | Method |
|-----------|--------|-------------|--------|
| Transit score | 0.30 | transport.opendata.ch `/v1/stationboard` | Departures counted in 2h window (07:00–09:00 weekday), divided by 2 = trains/hr. IC/IR counted separately for workability classification. |
| Workspace density | 0.25 | Google Places API (68 remote work places) | Count of workspaces within 1km of each station. Types: coworking, café, library, hotel lobby. Verified with reviews for work-relevance. |
| Temporal coverage | 0.20 | Google Places API (opening hours) | Hours score: 24h access = 1.0, extended hours (>12h) = 0.7, standard business = 0.5, limited = 0.3, unknown = 0.2. Weighted average of nearby workspaces. |
| Connectivity | 0.15 | WiFi MERGED v2 (81 hotspots) + BAKOM cell towers (3,218) | Composite: WiFi quality score of nearest hotspot + 5G tower density within 500m. Normalized. |
| Mobility | 0.10 | sharedmobility.ch API (2,062 stations) | Count of shared mobility stations (e-bikes, scooters, carshare) within 1km of each station. |

### Temporal WCI (TWCI)
Same formula, recomputed per time slot. Transit score changes (frequency varies by hour). Workspace score changes (some close at 17h, others 24h). Connectivity and mobility held constant.
**Time slots**: 05–07, 07–09, 11–13, 16–18, 19–21, 21–23, Sat 11–13
**API calls**: 343 for frequency (49 stations × 7 slots) + 196 for first/last trains = 539 total
**Bug fixed**: "Last train" query initially wrapped into next morning for busy stations. Fixed by querying from 20:00 with limit=200 and filtering to same calendar date (allowing past-midnight up to 01:30).

### GA Cost Estimation
**Method**: Distance-based tariff, not SBB API (pricing API doesn't exist publicly)
**Formula**: `price = base_fare + (distance_km × per_km_rate) × rail_multiplier`
- Rail multiplier: 1.05 (rail km > road km due to routing)
- Base fare: CHF 3.60 (full) / CHF 1.80 (Halbtax)
- Per-km rate: CHF 0.39 (0–30km), CHF 0.31 (30–60km), CHF 0.25 (60–100km) — degressive
- Calibrated against known prices: Geneva–Lausanne ≈ CHF 20 (model: CHF 21.80). Accuracy ±CHF 2–3.
- GA daily: CHF 3,860/365 = CHF 10.58

### Classmate Cross-Reference
**Method**: For each of 49 stations, count features from 33 classmate datasets within radii (500m for fine-grain, 1000m for amenities). Haversine distance on WGS84 coordinates.
**Datasets integrated**: gig work (50), hospitals (23), clinics (68), GPs (110), specialists (188), religious buildings (204), religious communities (274), esoteric (43), industrial zones (25), companies (195), schools (199), grocery stores (121), acoustic ecology (49), UHI zones (203), thermal comfort (33), restaurants (150), informal learning (132) — 2,093 points total.
**Shannon diversity**: Computed per station using religious community counts across 10+ denomination categories. H = -Σ(p_i × ln(p_i)).

### Diversity Research (Lumen)
**Correlation method**: Pearson r computed across 49-station dataset. All correlations reported are between station-level metrics (Shannon index, station richness, modal count, economic categories, trains/hr).
**Cuisine diversity**: 6 stations sampled, ~10 restaurants each, classified by cuisine origin type. Shannon computed per station.
**Modal diversity**: 11 transport mode types inventoried (CFF regional, CFF longdist, Léman Express, metro, tram, urban bus, regional bus, CGN boat, funicular, narrow gauge, shared bikes). Boolean per station, then Shannon computed.
**Nationality/language data**: Statistique Vaud 2024 + OCSTAT Geneva 2024 — commune-level, not station-level. Used as contextual evidence.
**Frontalier data**: OCSTAT Feb 2025 (GE: 114,900) + OFS Q2 2024 (VD: 45,230). Combined ≈ 160,000.

### Zurich Comparison
**Method**: 12 stations selected along Zurich S8 lakeside line (Zürich HB → Horgen Oberdorf). Same metrics computed: frequency from ZVV timetable data, workspace count from Google Places, analog station pairings by distance from center and function.
**Key structural difference**: Radial (Zurich) vs linear (City101). Distance from center = maximum variation distance.

### Journey Workability
**Data**: transport.opendata.ch `/v1/connections` API — 618 connections across 35 OD pairs × 3 time slots
**Classification**: PRIME_WORK (IC/IR, >20min, direct), WORKABLE (IC/IR, >15min or 1 change), MARGINAL (regional, >10min), NOT_WORKABLE (short, crowded, frequent stops), BROKEN (no connection found)

---

## NARRATIVE — Current State and What v2 Needs

### Current draft (deliverables/A02_NARRATIVE_DRAFT.md)
731 words, title "The Archipelago." Written by Lumen BEFORE temporal findings, diversity convergence, and frontalier research. Strong on: the archipelago metaphor, two-corridors argument, GA pricing, Zurich comparison, frequency-amenity paradox.

### What v2 should add
1. **Temporal confirmation**: "We tested whether the archipelago pulses — it doesn't. 14 stations at peak, 13 at 11pm. The fracture is structural, not temporal."
2. **Diversity convergence**: "Four independent diversity indices — religious, modal, cuisine, economic — converge on the same pattern. The Lavaux Fracture isn't a transit gap. It's a systemic diversity collapse."
3. **Frontalier paragraph**: "160,000 people cross the corridor daily, larger than Lausanne's population, invisible in every metric we computed, unable to buy the travelcard that makes the corridor function as one city."
4. **Architectural inversion**: "The prototypology at break points introduces difference, not deficit-filling. A break point becomes a node by offering what hubs can't."

### Who writes it
Andrea + Henna refine together Monday morning. Or delegate to Lumen with all findings docs as context. Target: 800–1000 words.

---

## VISUALIZATION PLAN — Print vs Interactive

### Methodology note for the booklet/crit
Every visualization traces back to a specific dataset with a documented production method (see Methodology section above). The choice of print vs interactive follows this logic:

**PRINT** when: the data is geographic and benefits from precise spatial reading; the audience will pin it up and annotate; the argument is a single snapshot.
**INTERACTIVE** when: the data is temporal (needs animation); multi-dimensional (needs filtering/sorting); cross-geographic (two maps can't share one sheet); relational (hover/click reveals connections).

### Print Maps (QGIS, A1 landscape PDF)
| Map | Data source | What it shows | Argument |
|-----|-------------|---------------|----------|
| MAP1: The Archipelago | corridor_segments_WCI.csv | WCI graduated color, 49 stations, 3 gaps dimensioned | The linear city doesn't exist |
| MAP2: Remote Work Infrastructure | remote_work_CROSSREF.csv + wifi | 68 workspaces + WiFi + hours | The workspace dimension |
| MAP3: Lavaux Fracture zoom | WCI + frequency + workspaces | The wound up close | Is this a failure or a refuge? |
| MAP4: Geneva Pole | WCI + all layers | Western anchor detail | What "continuous" looks like |
| MAP5: Lausanne Pole | WCI + all layers | Second anchor detail | University-boosted continuity |
| MAP6: Transit Backbone | service_frequency_v2 + ridership | Frequency gradient + ridership bubbles | 42× variation |
| MAP7: Data Synchronicity | All layers composite | Full dataset overlay | Research depth |
| MAP8 (new): GA Cost Gradient | ga_cost_corridor.csv | 49 stations colored by price from Geneva | Your city depends on your wallet |
| MAP9 (new): Shannon Diversity | station_crossref_classmates.csv | Stations colored by Shannon, sized by richness | Diversity = completeness |
| MAP10 (new): Temporal Triptych | temporal_WCI.csv | 3 snapshots: 7am / 1pm / 11pm same corridor | It doesn't pulse |

### Interactive HTML Visualizations (Claude Code, standalone .html)
Full spec in `prompts/VIZ_SPEC_CLAUDE_CODE.md`. Build order:

| # | Artifact | Data source | Why interactive |
|---|----------|-------------|-----------------|
| 1 | **Temporal WCI Pulse** | temporal_WCI.csv | Time slider animates 7 slots — can't do on paper. Punchline: counter barely moves (14→13). |
| 2 | **GA Cost Curve** | ga_cost_corridor.csv | Budget slider lets viewer set their own daily budget → "your city ends here." |
| 3 | **Diversity Dashboard** | crossref + modal_diversity.csv | Multi-panel: scatter (Shannon vs richness) + correlation bars + 5 mini-maps. Click highlights across panels. |
| 4 | **Zurich Comparison** | zurich_sbahn_comparison.csv | Two geographies side-by-side with same color scale. Can't share one print map. |
| 5 | **Station Explorer** | crossref + temporal + GA | 49 stations × 12 dimensions. Search, sort, radar charts, compare mode. |
| 6 | Journey Workability | journey_workability.csv | 618 connections — OD matrix heatmap, too dense for print. |
| 7 | Narrative Scroll | All | Scrollytelling version of the full argument. Portfolio piece, only if time. |

### Technical spec (for Claude Code)
- Standalone .html, embedded JS/CSS, no server
- Leaflet.js for maps (Swiss topo tiles: `wmts.geo.admin.ch`)
- D3.js for charts. Dark theme. System fonts or Inter/Space Mono.
- Data embedded as JS objects (datasets are small: <50 rows)
- Real WGS84 coordinates from CSVs — no approximations
- Output to `~/CLAUDE/City101_ClaudeCode/visualizations/`

---

## TASK SPLIT — Monday Morning

### HENNA — Focus on YOUR unique data
Don't redo temporal analysis or first/last trains — that's done. Focus on what only you have:

**Priority 1 — Bring your data for integration** ⏰ BEFORE CRIT
- Thermal comfort / UHI zones → QGIS layer (environmental quality overlay on WCI map)
- Cold air drainage → nighttime environmental layer
- Psycho-comfort → station quality annotation
- Your ridership data (22 stations) — verify it's integrated

**Priority 2 — Night-specific populations** (for narrative, not maps)
- Hospital shift patterns: who is stranded when trains stop at 01:00?
- What exists at night along the corridor? (Noctambus, 24h venues, night taxis)
- This is what makes our narrative *specific* per the assistant feedback: "not night, but night nurses"

**Priority 3 — Environmental quality argument** (1 paragraph for narrative)
- How does thermal comfort relate to WCI? Do the highest-WCI stations also have the worst UHI?
- If the Lavaux Fracture is the quietest, coolest segment — is it simultaneously the worst for work and the best for rest?
- This is the "is the fracture a failure or a refuge?" question

**Priority 4 — Intervention site proposals** (for week 2 point clouds)
- From our combined data: which 3–5 sites should get the prototypology?
- Candidates: frequency-amenity paradox stations (Bussigny, Lancy-Bachet, Aigle), Lavaux Fracture nodes (Cully, Rivaz), anomaly sites (Vernier-Blandonnet, Coppet)

### ANDREA — Map export + viz + narrative
**Priority 1 — QGIS visual check + export** ⏰ FIRST THING
- Open each of 7 layouts, verify labels aren't truncated
- Load new layers: temporal WCI, modal diversity, GA cost
- Create MAP8/MAP9/MAP10 if time
- Export all as PDF to `maps/`

**Priority 2 — Interactive visualizations** (Claude Code)
- Hand `VIZ_SPEC_CLAUDE_CODE.md` to Claude Code
- Priority: temporal pulse (#1) and GA cost curve (#2) — fastest impact
- Open on laptop during crit

**Priority 3 — Narrative v2** (with Henna)
- Integrate temporal, diversity, frontalier findings into draft
- Add Henna's night/environmental paragraph
- Target 800–1000 words

### TOGETHER — Before 1pm
- Final map selection: which 3–5 maps are THE ARGUMENT, rest are EVIDENCE
- Identify 3–5 intervention sites for week 2 point clouds
- Write/refine the 2-minute opening pitch
- Upload to team Drive

---

## THE 2-MINUTE PITCH (updated draft)

"We tested whether City101 functions as a linear city for knowledge workers. We built a Working Continuity Index — transit frequency, workspace, temporal access, connectivity, mobility — and computed it at every station.

The answer: it doesn't. Only 11 of 49 stations maintain continuity. The corridor is an archipelago — functional islands separated by infrastructure deserts. Three gaps: Nyon to Gland, Gland to Morges, and the 17.5-kilometer Lavaux Fracture where the WCI drops 2,000-fold.

We tested whether it pulses — whether the archipelago opens at rush hour. It doesn't. Fourteen stations at peak, thirteen at eleven PM. The fracture is structural, not temporal.

We tested whether everyone experiences the same corridor. They don't. A GA holder traverses 101 kilometers at zero marginal cost. A full-price traveler's city ends at St-Prex — 41 kilometers, twelve short of Lausanne. And 160,000 frontaliers can't buy a GA at all. Same tracks, different cities.

Then we tested Comtesse's thesis: does diversity create vitality? Four independent indices — religious, modal, economic, culinary — converge. Below a Shannon diversity of 1.0, stations average 9 amenities. Above it, 71. The Lavaux Fracture isn't a transit gap. It's a systemic diversity collapse.

Zurich proves the structure matters. Same country, same operator — but radial topology compresses frequency variation to 12×. City101's linear corridor amplifies it to 42×. The worst Zurich lakeside station gets 2 trains per hour. The worst City101 station gets zero.

The data prescribes the architecture. The prototypology targets the break points — not to fill deficits, but to introduce difference."

---

## FILES TO SHARE ON DRIVE

### Henna needs:
- `city101_first_last_trains.csv` — the data she was going to produce (already done)
- `city101_temporal_WCI.csv` — temporal analysis for her night city narrative
- `city101_temporal_summary.csv` — per-slot aggregates
- `city101_break_points.csv` — where continuity ruptures
- `city101_station_crossref_classmates.csv` — the 49-station × 46-column master dataset
- `city101_modal_diversity.csv` — modal Shannon per station
- `TEMPORAL_CORRIDOR_FINDINGS.md` — narrative-ready findings
- This handoff

### Documentation:
- `TEAM_HANDOFF_01-03_S2.md` (this file)
- `TODO_4_POINTS.md` — the 4 investigations framework
- `research/DIVERSITY_RESEARCH_FINDINGS.md` — Lumen's diversity research
- `research/DIVERSITY_NEW_ANGLES.md` — frontaliers, anomalies, cuisine-migration

---

*Signed: Andrea (via Cairn) · 2026-03-02*
