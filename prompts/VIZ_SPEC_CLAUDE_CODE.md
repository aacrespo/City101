# VIZ_SPEC_CLAUDE_CODE.md
## Interactive Visualization Spec for Claude Code
**Date**: 2026-03-02 (revised)
**For**: Claude Code — build standalone HTML files
**Project**: City101 Geneva-Villeneuve corridor analysis, EPFL BA6 Studio Huang

---

## Session Batching

Build artifacts across multiple Claude Code sessions to avoid context limits:

| Session | Artifacts | Type |
|---------|-----------|------|
| 1 | viz_01 (GA cost curve) + viz_02 (temporal pulse) | D3 chart + Leaflet map |
| 2 | viz_03 (diversity dashboard) + viz_04 (Zurich comparison) | Multi-panel + side-by-side maps |
| 3 | viz_05 (station explorer) + viz_06/07 if time | Table + radar charts |

---

## Methodology — How the Data Was Produced

Each visualization traces to a specific dataset with documented production methodology. Claude Code should display methodology notes as hover/click info or footnotes in each artifact so the crit audience can interrogate the data.

### WCI (Working Continuity Index)
`WCI = 0.30×transit + 0.25×workspace + 0.20×temporal + 0.15×connectivity + 0.10×mobility`
All sub-scores min-max normalized (0–1) across 49 stations. Transit: trains/hr from transport.opendata.ch (departures in 2h window ÷ 2). Workspace: Google Places within 1km (68 coworking/café/library). Temporal: opening hours score (24h=1.0, standard=0.5). Connectivity: WiFi quality + 5G density within 500m. Mobility: shared mobility stations within 1km.

### Temporal WCI (TWCI)
Same formula recomputed per time slot. 7 slots: 05–07, 07–09, 11–13, 16–18, 19–21, 21–23, Sat 11–13. Transit changes by hour. Workspace changes (closures). Connectivity/mobility held constant. 539 API calls to transport.opendata.ch.

### GA Cost
Distance-based tariff estimation (no public SBB pricing API). Formula: base_fare + (distance × per_km_rate × rail_multiplier). Degressive per-km: CHF 0.39 (0–30km), 0.31 (30–60km), 0.25 (60–100km). Rail multiplier 1.05. Calibrated against Geneva–Lausanne (model CHF 21.80 vs actual ~CHF 20). Accuracy ±CHF 2–3. GA daily = CHF 3,860/365 = CHF 10.58.

### Shannon Diversity
H = −Σ(pᵢ × ln(pᵢ)) where pᵢ = proportion of category i. Applied to: religious communities (10+ denominations), transport modes (11 types), cuisine types (8+ categories), economic sectors. Computed per station from classmate crossref data (2,093 points, 33 datasets).

### Zurich Comparison
12 S8 lakeside stations. Same metrics computed. Structural comparison: radial (Zurich) vs linear (City101). Key difference: distance amplifies inequality on a linear network.

### Correlation Values
All Pearson r computed across the 49-station dataset. Station-level metrics only.

### Journey Workability
transport.opendata.ch `/v1/connections` API — 618 connections, 35 OD pairs × 3 time slots. Classification by service type + duration + changes: PRIME_WORK (IC/IR, >20min, direct), WORKABLE, MARGINAL, NOT_WORKABLE, BROKEN.

---

## General Requirements

### Format
- **Standalone .html files** — single file with embedded CSS + JS, no external dependencies except CDN links
- Open in any browser, no server needed
- Responsive but optimized for laptop screen (1440x900)

### Libraries (CDN only)
- **Leaflet.js** for maps: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js` + CSS
- **D3.js** for charts: `https://d3js.org/d3.v7.min.js`
- No React, no build tools, no npm — vanilla JS only

### Output location
- Save to `~/CLAUDE/City101_ClaudeCode/visualizations/` (create folder if needed)
- Name pattern: `viz_01_ga_cost.html`, `viz_02_temporal_pulse.html`, etc.

### Verification (after each artifact)
1. Serve the file via Preview MCP or `python3 -m http.server 8080`
2. Take a screenshot
3. Check: correct station count (49 for corridor, 12 for Zurich), tooltips render, colors match spec, no console errors
4. Print `DONE: viz_0X_name.html` when verified

---

## Shared Design System

Use these tokens in ALL artifacts for visual consistency.

### Colors

```javascript
const COLORS = {
  // Surface
  bg: '#1a1a2e',
  panel: '#16213e',
  border: '#2a2a4a',

  // Text
  text: '#e0e0e0',
  textSecondary: '#8892a0',
  textAccent: '#ffffff',

  // Sequential scale (WCI, frequency, diversity)
  scaleRed: '#e74c3c',
  scaleOrange: '#e67e22',
  scaleYellow: '#f1c40f',
  scaleGreen: '#2ecc71',

  // Corridor segments
  segGeneva: '#e74c3c',
  segLaCote: '#e67e22',
  segLausanne: '#3498db',
  segLavaux: '#9b59b6',
  segRiviera: '#2ecc71',

  // GA cost specific
  fullPrice: '#e74c3c',
  halbtax: '#2ecc71',
  gaThreshold: '#3498db',

  // Workability classes
  prime: '#2ecc71',
  workable: '#f1c40f',
  marginal: '#e67e22',
  notWorkable: '#e74c3c',

  // Accent
  accent: '#3498db',
};
```

### Typography

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap');

body {
  font-family: 'Inter', -apple-system, sans-serif;
  background: #1a1a2e;
  color: #e0e0e0;
  margin: 0;
  font-size: 14px;
}
.stat-number {
  font-family: 'Space Mono', 'SF Mono', monospace;
  font-size: 28px;
  font-weight: 700;
  color: #ffffff;
}
.data-label {
  font-family: 'Space Mono', 'SF Mono', monospace;
  font-size: 12px;
  color: #8892a0;
}
```

### Tooltip (reuse everywhere)

```css
.tooltip {
  position: absolute;
  background: #16213e;
  border: 1px solid #3498db;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 13px;
  color: #e0e0e0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
  pointer-events: none;
  z-index: 1000;
}
.tooltip .station-name { font-weight: 600; color: #fff; }
.tooltip .stat-value { font-family: 'Space Mono', monospace; color: #3498db; }
```

### Map tiles

```javascript
// Primary: Swiss Federal topo
const SWISS_TILES = 'https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg';

// Fallback: Carto dark (matches dark UI better than standard OSM)
const CARTO_DARK = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';

// Corridor extent (WGS84 bounds)
const CORRIDOR_BOUNDS = [[46.19, 6.05], [46.45, 7.02]];
```

---

## Data Preparation

### Canonical station join key
All CSVs use `station_name` EXCEPT the GA cost file which uses `station`. When joining data, map `station` -> `station_name`.

### Station corridor ordering
The file `city101_ga_cost_corridor.csv` contains `rail_km_est_from_geneva` for all 49 stations. Use this as the canonical ordering (Geneva = 0 km, Villeneuve = end). Other CSVs do not have this column — join via station name to get the ordering.

### Known data issues
- **Comma-in-name**: `"Vernier, Blandonnet"` is quoted in CSVs because it contains a comma. Use proper CSV parsing (not naive comma-split).
- **Service window bug**: `service_window_wd` in `city101_temporal_WCI.csv` has incorrect values (Lausanne shows 1.0h instead of 19.9h). For service window display, use `city101_first_last_trains.csv` instead. The TWCI scores per time slot are correct.
- **UTF-8**: Station names include French accents (Geneve, Secheron, Palezieux). Set `<meta charset="UTF-8">`.

### Workable threshold
A station is "workable" when its TWCI > 0.10. This produces the ~14 workable stations at peak that appear in the narrative.

### Corridor segments (for coloring by geography)
Assign stations to segments based on `rail_km_est_from_geneva`:
- **Geneva** (0-10 km): Geneve through Versoix
- **La Cote** (10-40 km): Coppet through Allaman
- **Lausanne** (40-65 km): St-Prex through Puidoux-Chexbres
- **Lavaux** (65-85 km): Lutry through St-Saphorin
- **Riviera** (85-101 km): Vevey through Villeneuve

---

## Print vs Interactive — Decision Matrix

### PRINT (QGIS maps, A1 landscape PDF):
Best for: geographic data that benefits from precise positioning, static snapshots, things critics pin up and annotate during the crit. The 7 existing A02 layouts handle this well.

**Print candidates (QGIS, existing or new layouts):**
- MAP1-MAP7: already built, export tomorrow
- MAP8: GA cost gradient (49 stations colored by price from Geneva)
- MAP9: Station richness / Shannon diversity map (from crossref data)
- MAP10: Temporal WCI series (3 snapshots: 7am / 1pm / 11pm on same A1 sheet)

### INTERACTIVE HTML (laptop at crit):
Best for: temporal animation, multi-dimensional exploration, cross-geography comparison, filterable datasets, the "let me show you something" moments during discussion.

---

## Artifact #1: GA Cost Curve (BUILD FIRST)

**File**: `viz_01_ga_cost.html`
**The argument**: "How far is YOUR city? Depends on your wallet."
**Why build first**: Pure D3 chart, no map complexity. Establishes the visual language (dark theme, tooltips, fonts) before tackling Leaflet maps.

### What it shows
A chart showing ticket price (Y-axis) vs distance from Geneva (X-axis). 49 stations plotted as dots along two curves (full price + Halbtax). Horizontal threshold lines at CHF 10, 15, 20. Horizontal GA daily cost line (CHF 10.58).

### Data source
**File**: `datasets/corridor_analysis/city101_ga_cost_corridor.csv` (49 rows x 14 cols)

**Columns needed**:
| Column | Type | Use |
|--------|------|-----|
| `station` | string | Station name (note: this file uses `station`, not `station_name`) |
| `rail_km_est_from_geneva` | float | X-axis position |
| `price_full_from_gva` | float | Full price Y value |
| `price_halbtax_from_gva` | float | Halbtax Y value |
| `ga_daily_cost` | float | Horizontal threshold (10.58 for all) |
| `trains_per_hour` | float | Dot size |
| `lat_wgs84` | float | Not needed for this chart |
| `lon_wgs84` | float | Not needed for this chart |

### Interactions
- **Hover on station dot**: tooltip with station name, exact price (full + halbtax), km from Geneva, trains/hr
- **Toggle button**: show/hide Halbtax curve
- **Budget slider**: drag CHF 5-30 to set daily transport budget. Stations beyond budget shown as faded/gray. Text updates: "On a CHF XX budget, your city reaches [station] — YY km from Geneva."
- **Key city annotations**: vertical dashed lines + labels at Geneva (0km), Nyon (~25km), Lausanne (~60km), Vevey (~80km), Montreux (~90km)

### Visual design
- D3 line chart on dark background (`#1a1a2e`)
- Full price: solid line in `#e74c3c`, dots sized by `trains_per_hour`
- Halbtax: dashed line in `#2ecc71`
- GA daily: horizontal dashed line in `#3498db` at CHF 10.58
- Budget zones shaded: CHF 0-10 green tint, 10-20 yellow tint, 20+ red tint (very subtle, ~10% opacity)
- X-axis: "Distance from Geneva (km)". Y-axis: "Single ticket price (CHF)"

### Key insight to surface
Static annotation at bottom: "On a CHF 20 budget, your city ends at St-Prex — 12 km short of Lausanne."

---

## Artifact #2: Temporal WCI Pulse (THE SIGNATURE PIECE)

**File**: `viz_02_temporal_pulse.html`
**The argument**: "The corridor doesn't pulse — it's structurally broken at all hours."

### What it shows
A Leaflet map of the 49 stations with a time slider (7 slots). As you drag the slider, station markers change color and size based on their TWCI score at that time. The three structural gaps (Nyon-Gland, Gland-Morges, Lavaux) remain dark at every time slot.

### Data sources

**Primary**: `datasets/corridor_analysis/city101_temporal_WCI.csv` (49 rows x ~55 cols)

| Column | Type | Use |
|--------|------|-----|
| `station_name` | string | Label |
| `lat_wgs84` | float | Map position |
| `lon_wgs84` | float | Map position |
| `twci_early_morning` | float | TWCI for 05-07 slot |
| `twci_am_peak` | float | TWCI for 07-09 slot |
| `twci_midday` | float | TWCI for 11-13 slot |
| `twci_pm_peak` | float | TWCI for 16-18 slot |
| `twci_evening` | float | TWCI for 19-21 slot |
| `twci_late_night` | float | TWCI for 21-23 slot |
| `twci_weekend_mid` | float | TWCI for Sat 11-13 slot |
| `freq_am_peak` | float | Trains/hr for tooltip (similar `freq_*` cols for other slots) |
| `ws_open_am_peak` | int | Workspaces open for tooltip (similar `ws_open_*` cols for other slots) |
| `ic_am_peak` | int | IC departures for summary panel (similar `ic_*` cols for other slots) |

**Service windows** (join by `station_name`): `datasets/corridor_analysis/city101_first_last_trains.csv` (49 rows x 10 cols)

| Column | Type | Use |
|--------|------|-----|
| `station_name` | string | Join key |
| `first_train_weekday` | time | Tooltip |
| `last_train_weekday` | time | Tooltip |
| `service_window_weekday_hrs` | float | Tooltip display. DO NOT use the service_window columns from temporal_WCI.csv (they have a data bug). |

**Station ordering** (join by station name): use `rail_km_est_from_geneva` from `city101_ga_cost_corridor.csv` to draw the corridor polyline in geographic order.

### Time slots mapping
```javascript
const TIME_SLOTS = [
  { key: 'early_morning', label: '05:00 - 07:00', subtitle: 'Early Morning' },
  { key: 'am_peak',       label: '07:00 - 09:00', subtitle: 'AM Peak' },
  { key: 'midday',        label: '11:00 - 13:00', subtitle: 'Midday' },
  { key: 'pm_peak',       label: '16:00 - 18:00', subtitle: 'PM Peak' },
  { key: 'evening',       label: '19:00 - 21:00', subtitle: 'Evening' },
  { key: 'late_night',    label: '21:00 - 23:00', subtitle: 'Late Night' },
  { key: 'weekend_mid',   label: '11:00 - 13:00', subtitle: 'Saturday Midday' },
];
```

### Interactions
- **Time slider**: 7 discrete positions. Drag or click to change.
- **Play button**: auto-animate through all 7 slots (1.5s per frame, loop)
- **Station hover**: tooltip with station name, TWCI score, trains/hr, workspaces open, service window
- **Bottom summary panel**: for current slot show: "XX/49 workable (TWCI > 0.10)", average TWCI, total IC departures

### Visual design
- Station markers: circles. Radius = `Math.max(3, twci * 30)` (so 0.01 -> 3px, 0.6 -> 18px)
- Color: red `#e74c3c` (TWCI < 0.05) -> orange `#e67e22` (0.05-0.15) -> yellow `#f1c40f` (0.15-0.3) -> green `#2ecc71` (> 0.3)
- Corridor polyline: thin gray line connecting all 49 stations in geographic order (sorted by `rail_km_est_from_geneva`)
- Current time slot: large overlay text in top-right corner, e.g. "07:00 - 09:00 AM Peak"
- Counter next to slider: "14/49 workable" (recalculated per slot)

### Key insight to surface
The counter barely changes: 14 at peak, 13 at late night. The near-zero variation is the punchline.

---

## Artifact #3: Diversity Convergence Dashboard

**File**: `viz_03_diversity_dashboard.html`
**The argument**: "Four independent diversity indices tell the same story. The Lavaux Fracture is a systemic diversity collapse."

### What it shows
A 3-panel dashboard:
- **Panel A** (left, 50% width): Scatter plot — religious Shannon (X) vs station richness (Y). Dots colored by corridor segment. Phase transition line at Shannon = 1.0.
- **Panel B** (right-top, 50% width): Horizontal bar chart — 10 pairwise correlations sorted by strength
- **Panel C** (right-bottom): 4 mini Leaflet maps of the corridor, each colored by a different diversity metric. Visual proof they all show the same spatial pattern.

### Data sources

**Crossref**: `datasets/corridor_analysis/city101_station_crossref_classmates.csv` (49 rows x 46 cols)

| Column | Type | Use |
|--------|------|-----|
| `station_name` | string | Label + join key |
| `lat_wgs84` | float | Mini-map position |
| `lon_wgs84` | float | Mini-map position |
| `religious_shannon_diversity` | float | Panel A X-axis, Panel C map 1 |
| `station_richness_1000m` | int | Panel A Y-axis, Panel C map 4 |
| `trains_per_hour` | float | Tooltip context |

**Modal diversity**: `datasets/corridor_analysis/city101_modal_diversity.csv` (49 rows x 17 cols)

| Column | Type | Use |
|--------|------|-----|
| `station_name` | string | Join key |
| `modal_shannon` | float | Panel C map 2 |
| `n_modes` | int | Tooltip |

**Embedded constants** (from Lumen S8.2 analysis):
```javascript
const CORRELATIONS = [
  { pair: 'Economic categories vs Shannon', r: 0.708 },
  { pair: 'Cuisine Shannon vs Shannon', r: 0.71 },
  { pair: 'Station richness vs Shannon', r: 0.632 },
  { pair: 'Modal Shannon vs Shannon', r: 0.626 },
  { pair: 'Richness vs modal Shannon', r: 0.58 },
  { pair: 'Economic vs modal Shannon', r: 0.55 },
  { pair: 'Richness vs economic categories', r: 0.52 },
  { pair: 'Cuisine vs modal Shannon', r: 0.48 },
  { pair: 'Cuisine vs richness', r: 0.45 },
  { pair: 'Cuisine vs economic', r: 0.42 },
];

const CUISINE_SHANNON = [
  { station: 'Geneve', value: 2.03 },
  { station: 'Lausanne', value: 1.92 },
  { station: 'Nyon', value: 1.75 },
  { station: 'Vevey', value: 1.68 },
  { station: 'Montreux', value: 1.61 },
  { station: 'Chexbres', value: 1.50 },
];
```

### Interactions
- **Click station dot in scatter (Panel A)**: highlight same station across all panels with a ring/pulse
- **Hover any station**: tooltip with station name, religious Shannon, modal Shannon, richness, segment
- **Toggle regression line** in Panel A: show/hide with r-squared label

### Visual design
- Scatter dots colored by corridor segment (use `COLORS.seg*` from design system)
- Phase transition at Shannon = 1.0: vertical dashed line with label "Phase transition: below 1.0 avg richness 8.8, above 70.5"
- Anomaly stations labeled directly: Vernier-Blandonnet, Coppet
- Mini-maps in Panel C: same Leaflet setup as viz_02, but smaller (300x200px each), station dots colored by the metric (sequential red-green scale)

---

## Artifact #4: Zurich Comparison

**File**: `viz_04_zurich_comparison.html`
**The argument**: "Same country, same operator, same trains. Radial compresses variation, linear amplifies it."

### What it shows
Side-by-side maps (City101 left, Zurich S8 right) + comparison metrics table + analog pairings table.

### Data sources

**Zurich stations**: `datasets/zurich_comparison/zurich_sbahn_comparison.csv` (12 rows x 18 cols)

| Column | Type | Use |
|--------|------|-----|
| `station_name` | string | Label |
| `lat_wgs84` | float | Map position |
| `lon_wgs84` | float | Map position |
| `trains_per_hour_peak_approx` | float | Dot color/size |
| `dist_from_hub_km` | float | Tooltip |
| `city101_analog_station` | string | Pairing table |
| `city101_analog_trains_per_hr` | float | Pairing table |
| `frequency_ratio_zh_over_c101` | float | Pairing table |
| `argument_role` | string | Label context |

**City101 frequency**: `datasets/corridor_analysis/city101_temporal_frequency.csv` (49 rows x 25 cols)

| Column | Type | Use |
|--------|------|-----|
| `station_name` | string | Label |
| `lat_wgs84` | float | Map position |
| `lon_wgs84` | float | Map position |
| `freq_am_peak` | float | Dot color/size (same scale as Zurich) |

**Metrics**: `datasets/zurich_comparison/zurich_comparison_metrics.csv` (15 rows x 5 cols)

| Column | Type | Use |
|--------|------|-----|
| `metric` | string | Row label |
| `zurich_s8_lakeside` | string | Left column |
| `city101_geneva_villeneuve` | string | Right column |
| `ratio_or_comparison` | string | Comparison column |
| `significance` | string | Tooltip/expand detail |

### Layout
- **Top row**: Two Leaflet maps side-by-side, each ~50% width
  - Left: City101 corridor, stations colored by `freq_am_peak`, same sequential color scale
  - Right: Zurich S8 lakeside, stations colored by `trains_per_hour_peak_approx`, same scale
  - IMPORTANT: Use the same color scale for both maps so they're visually comparable
  - Zurich map extent: roughly [47.28, 8.48] to [47.40, 8.80]
- **Middle row**: Key metrics comparison table (styled, not raw). Highlight the 3 most impactful: 42x vs 12x variation, 0 vs 2/hr minimum, 83% vs 45% above 4/hr threshold
- **Bottom row**: Analog pairings table. Each row: Zurich station | City101 analog | frequency ratio | structural note. No cross-map lines (visually confusing at different scales).

### Key insight to surface
Text callout: "The minimum Zurich station (Oberrieden, 2/hr) is 11 km from center. The equivalent City101 station (Grandvaux, 2/hr) is 56 km from Geneva."

---

## Artifact #5: Station Profile Explorer

**File**: `viz_05_station_explorer.html`
**The argument**: "Every station is a different city. Explore 49 stations across 12 dimensions."

### What it shows
A searchable/sortable table of all 49 stations. Clicking a station opens a radar chart showing its multi-dimensional profile. Compare mode lets you overlay 2-3 stations.

### Data sources
Join these files by `station_name` (GA cost file uses `station` — map to `station_name`):
- `datasets/corridor_analysis/city101_station_crossref_classmates.csv` — richness, Shannon, healthcare, restaurants, etc.
- `datasets/corridor_analysis/city101_temporal_WCI.csv` — TWCI scores (use `twci_am_peak` as default)
- `datasets/corridor_analysis/city101_ga_cost_corridor.csv` — cost from Geneva, trains/hr, km from Geneva
- `datasets/corridor_analysis/city101_modal_diversity.csv` — modal Shannon, n_modes
- `datasets/corridor_analysis/city101_first_last_trains.csv` — service window hours

### Radar chart axes (8 dimensions, all normalized 0-1)
1. Transit frequency (`trains_per_hour` / max)
2. Station richness (`station_richness_1000m` / max)
3. Religious Shannon (`religious_shannon_diversity` / max)
4. Modal diversity (`modal_shannon` / max)
5. TWCI at peak (`twci_am_peak` / max)
6. Service window (`service_window_weekday_hrs` from first_last_trains / max)
7. Cost accessibility (inverted: 1 - `price_full_from_gva` / max, so cheaper = better)
8. Healthcare access (`healthcare_total_1000m` / max)

### Interactions
- **Search**: filter by station name (fuzzy match)
- **Sort table**: click column header to sort by any dimension
- **Click station row**: expands to show radar chart
- **Compare mode**: checkbox to select 2-3 stations, show overlaid radar charts
- **Segment filter**: dropdown to filter by corridor segment

---

## Artifact #6: Journey Workability Explorer (LOW PRIORITY)

**File**: `viz_06_journey_workability.html`
**The argument**: "85% of connections are not workable."

### Data source
- `datasets/corridor_analysis/city101_journey_workability.csv` (618 rows x 16 cols)
- Key columns: `from_station`, `to_station`, `workability_class`, `duration_min`, `comfort_score`, `primary_category`

### What it shows
OD matrix heatmap. Rows = origin stations (sorted by corridor order), Cols = destination stations. Color by best workability class for each pair: `#2ecc71` PRIME, `#f1c40f` WORKABLE, `#e67e22` MARGINAL, `#e74c3c` NOT_WORKABLE. Click a cell to see connection details.

---

## Artifact #7: Narrative Scroll (OPTIONAL)

**File**: `viz_07_narrative_scroll.html`
**The argument**: The full story as a scrollytelling page.

Combines key charts from artifacts 1-5 into a guided narrative. As user scrolls, maps/charts animate to illustrate findings in sequence: archipelago -> two corridors -> who pays what -> diversity creates unity -> temporal invariance. Build only if time allows.

---

## Notes for Claude Code

- **Read CSVs before building** — verify column names match this spec. If a column name doesn't match, check the actual file and adapt.
- **Embed data as JS objects** — datasets are small (49 rows max for corridor, 618 for journeys). No need for fetch() calls.
- **Swiss topo tiles**: should work without CORS issues. If blocked, use Carto dark fallback.
- **Station order**: always sort by `rail_km_est_from_geneva` (join from GA cost file), never alphabetically.
- **Print `DONE: viz_0X_name.html`** after each file is created and verified.
