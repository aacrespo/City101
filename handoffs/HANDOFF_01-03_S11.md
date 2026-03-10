# HANDOFF — 01-03 Session 11
**Date**: 2026-03-02, early AM
**Account**: Claude Code (terminal)
**Platform**: Terminal + Preview MCP (port 8080)
**Continues from**: HANDOFF_01-03_S10 (Cairn)

---

## What happened this session

### 1. Built viz_05 — Station Profile Explorer
49 stations × 8 radar dimensions (transit frequency, station richness, religious Shannon, modal diversity, TWCI peak, service window, cost accessibility, healthcare). Sortable/searchable table with segment color dots. D3 radar chart with concentric guides. Compare mode overlays up to 3 stations. Segment filter.

Data joined from 5 CSVs: crossref, modal diversity, temporal WCI, first/last trains, GA cost. Key normalization maxes: `{fr:84, ri:277, rs:2.123, ms:2.079, tw:0.6732, sw:21.3, pr:26.54, hc:92}`. Cost axis inverted (1 − price/max) so cheaper = higher.

**Bug fixed**: Title text "Comparing 3 Stations" persisted after disabling compare mode. Added cleanup in the `else` branch of `updateRadar()` to clear title/subtitle before early return.

### 2. Built viz_06 — Journey Workability Explorer
25×25 OD matrix heatmap. 35 unique station pairs aggregated from 618 raw connections in `city101_journey_workability.csv`. Cells colored by best workability class: Prime (#2ecc71), Workable (#f1c40f), Marginal (#e67e22), Not Workable (#e74c3c). Click cell → detail panel with duration, comfort stars, distance.

Corridor summary: 8 Prime, 5 Workable, 18 Marginal, 4 Not Workable (37% workable). Key finding: all Prime connections are long-distance IC/IR trains; short-hop S-Bahn = never prime.

### 3. Built viz_07 — Narrative Scroll (scrollytelling)
5-chapter scrollytelling page combining key charts from viz_01–05:
- **Ch.1 The Corridor**: Leaflet map, 49 staggered markers by segment
- **Ch.2 Two Corridors**: Zurich vs City101 comparison cards (2/hr at 11km vs 0/hr at 61km)
- **Ch.3 Price of Distance**: Animated D3 cost curve + GA daily threshold line
- **Ch.4 Diversity Fracture**: D3 scatter (Shannon vs Richness) + phase transition at 1.0
- **Ch.5 Temporal Invariance**: Multi-line TWCI chart — 6 stations, 7 time periods, parallel lines that never cross
- **Conclusion**: "This is not a natural pattern. It is a design choice." + 4 summary stats

Scroll-triggered fade-in animations via IntersectionObserver (threshold 0.15). Each chart animates once on first visibility.

### 4. Updated CONTEXT.md
Line 198: "All 7 viz built" → marked COMPLETE.

---

## Files created/modified

| File | Action | Location |
|------|--------|----------|
| viz_01_ga_cost.html | BUILT (earlier session) | visualizations/ |
| viz_02_temporal_pulse.html | BUILT (earlier session) | visualizations/ |
| viz_03_diversity.html | BUILT (earlier session) | visualizations/ |
| viz_04_zurich.html | BUILT (earlier session) | visualizations/ |
| viz_05_station_explorer.html | NEW + BUGFIX (this session) | visualizations/ |
| viz_06_journey_workability.html | NEW (this session) | visualizations/ |
| viz_07_narrative_scroll.html | NEW (this session) | visualizations/ |
| CONTEXT.md | UPDATED | root |
| HANDOFF_01-03_S11.md | NEW | handoffs/ |

---

## Current state

### All 7 interactive visualizations: COMPLETE

| Viz | File | Argument | Status |
|-----|------|----------|--------|
| 01 | viz_01_ga_cost.html | GA creates a binary: have-pass vs pay-per-trip | verified |
| 02 | viz_02_temporal_pulse.html | The archipelago is structural, not temporal | verified |
| 03 | viz_03_diversity.html | Four diversity indices converge at the Lavaux Fracture | verified |
| 04 | viz_04_zurich.html | Same country, same operator, radically different outcomes | verified |
| 05 | viz_05_station_explorer.html | 49 stations, 8 dimensions — every station has a profile | verified |
| 06 | viz_06_journey_workability.html | 85% of short-hop connections are not workable | verified |
| 07 | viz_07_narrative_scroll.html | The full story as scrollytelling | verified |

All 7 verified via Preview MCP: zero console errors, all interactivity functional, all data rendering correctly.

### Remaining for Monday crit
1. **QGIS**: Check 7 layouts visually, export PDFs. Load temporal + modal + GA layers.
2. **Narrative v2**: Integrate temporal, diversity, frontalier findings. With Henna.
3. **Upload**: Team Drive (see research/DRIVE_STRUCTURE.md)
4. **Interactive HTML**: DONE — all 7 built and verified.

---

## Key decisions made (cumulative)

- All data embedded as JS objects — no fetch() calls, no external CSV loading
- Dark design system: #1a1a2e bg, #16213e panels, #2a2a4a borders, Inter + Space Mono fonts
- Segment colors: Geneva=#e74c3c, La Côte=#e67e22, Lausanne=#3498db, Lavaux=#9b59b6, Riviera=#2ecc71
- Segment boundaries from rail_km: 0–10 Geneva, 10–35 La Côte, 35–55 Lausanne, 55–63 Lavaux, 63+ Riviera
- Station order: always sorted by rail_km_est_from_geneva, never alphabetically
- D3 v7 for charts, Leaflet 1.9.4 for maps, Carto Dark tiles (fallback from Swiss topo)
- viz_07 uses IntersectionObserver for scroll triggers, not a library (scrollama etc.)

---

## Technical notes

- **Preview server**: `python -m http.server 8080` serving from `visualizations/` directory. ServerId: `dd8a5064-14f9-4e38-920d-547a917d00f4`
- **GA cost CSV**: uses `station` column (not `station_name`). Must normalize when joining with crossref/temporal CSVs.
- **Vernier-Blandonnet**: 84 tph (tram hub anomaly). Distorts frequency axis — handled by per-viz capping.
- **Lausanne-Flon**: 277 richness (highest). Compresses scatter Y-axis — kept intentionally to show Lavaux Fracture.
- **St-Saphorin**: 0 frequency, 0 service window. Displays as collapsed center on radar.
- **viz_05 radar normalization**: each axis normalized 0–1 against corridor maximum
- **viz_06 OD matrix**: 618 raw rows → 35 unique pairs. Best workability class per pair used for cell color.
- **viz_07 data**: single JS array of 49 stations with all fields, plus TEMPORAL array for 6 stations × 7 periods.

---

## Data sources (this session)

- viz_05 data: city101_temporal_WCI.csv + city101_first_last_trains.csv + city101_station_crossref_classmates.csv + city101_modal_diversity.csv + city101_ga_cost_corridor.csv (all pre-existing, from S8–S9)
- viz_06 data: city101_journey_workability.csv (618 rows × 16 cols, pre-existing from S8)
- viz_07 data: subset of above CSVs, embedded as compact JS arrays

---

*Signed: Claude Code (terminal) · 2026-03-02*
