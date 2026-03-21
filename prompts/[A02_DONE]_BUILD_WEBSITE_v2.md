# PROMPT: Build the Full A02 Website — "The Archipelago" (v2)

## What you're building
A comprehensive single-page scrollytelling website that IS the A02 deliverable. One URL, open on a laptop at crit, scroll through everything. It combines:

1. **Narrative text** — 10 chapters, unified voice, no Henna/Andrea attribution until colophon
2. **D3 charts** — WCI bars, workability donut, cost curve, temporal bars, diversity scatter, nightlife bars, service window lollipop
3. **3 temporal visualizations** — Clock Diagram, Marey Diagram, Space-Time Heatmap (already built, integrate inline)
4. **QGIS map renders** — 7 layouts exported as high-res PNGs (fix labels first)
5. **Leaflet interactive corridor map** — 49 stations + 134 venues + 68 workspaces
6. **Links to 7+3 standalone interactive vizs** — working relative paths

## File Structure
```
~/CLAUDE/City101_ClaudeCode/visualizations/site/
  index.html                          (the mega page, ~200KB)
  maps/                               (rendered QGIS layouts)
    map1_wci.png
    map2_remote_work.png
    map3_lavaux.png
    map4_geneva.png
    map5_lausanne.png
    map6_transit.png
    map7_synchronicity.png
  city101_clock_diagram.html          (copy from parent)
  city101_marey_diagram.html          (copy)
  city101_spacetime_diagram.html      (copy)
  viz_01_ga_cost.html                 (copy from parent)
  viz_02_temporal_pulse.html
  viz_03_diversity.html
  viz_04_zurich.html
  viz_05_station_explorer.html
  viz_06_journey_workability.html
  viz_07_narrative_scroll.html
```

---

## PHASE 1: Fix & Export QGIS Layouts

### 1A. Fix truncated labels + credits

All 7 layouts have labels cut off by their bounding boxes. For each `A02_MAP*` layout:

```python
from qgis.core import QgsProject, QgsLayoutItemLabel
from PyQt5.QtGui import QFont

proj = QgsProject.instance()
manager = proj.layoutManager()

for layout in manager.printLayouts():
    name = layout.name()
    if not name.startswith('A02_'): continue
    
    for item in layout.items():
        if isinstance(item, QgsLayoutItemLabel):
            text = item.text()
            
            # Fix credit line: add Henna
            if 'Andrea Crespo' in text and 'Henna' not in text:
                new_text = text.replace('Andrea Crespo', 'Andrea Crespo + Henna Rafik')
                item.setText(new_text)
                print(f"  [{name}] Updated credit: {new_text[:80]}")
            
            # Auto-resize labels to fit content
            item.adjustSizeToText()
    
    print(f"  {name}: labels fixed")
```

**Review each layout after fixing** — check that adjustSizeToText() didn't break positioning. If it did, manually set sizes.

### 1B. Export as PNG

```python
from qgis.core import QgsProject, QgsLayoutExporter
import os

out_dir = os.path.expanduser('~/CLAUDE/City101_ClaudeCode/visualizations/site/maps/')
os.makedirs(out_dir, exist_ok=True)

layouts_to_export = {
    'A02_MAP1_Working_Continuity_Index': 'map1_wci.png',
    'A02_MAP2_Remote_Work_Infrastructure': 'map2_remote_work.png',
    'A02_MAP3_Lavaux_Fracture': 'map3_lavaux.png',
    'A02_MAP4_Geneva_Pole': 'map4_geneva.png',
    'A02_MAP5_Lausanne_Pole': 'map5_lausanne.png',
    'A02_MAP6_Transit_Backbone': 'map6_transit.png',
    'A02_MAP7_Data_Synchronicity': 'map7_synchronicity.png',
}

for layout_name, filename in layouts_to_export.items():
    layout = manager.layoutByName(layout_name)
    if not layout:
        print(f"  MISSING: {layout_name}")
        continue
    exporter = QgsLayoutExporter(layout)
    settings = QgsLayoutExporter.ImageExportSettings()
    settings.dpi = 150  # Good for web. 300 for print.
    path = os.path.join(out_dir, filename)
    result = exporter.exportToImage(path, settings)
    size = os.path.getsize(path) // 1024 if os.path.exists(path) else 0
    print(f"  {layout_name} → {filename}: {'OK' if result == 0 else 'FAILED'} ({size} KB)")
```

### 1C. Optional: Improve layouts

If you have time, Claude Code can enhance the layouts:

**Typography**: Check font consistency. QGIS defaults are often ugly — consider switching labels to DM Sans or similar.

**Missing maps**: There are NO layouts for:
- GA cost gradient (finding 3)
- Diversity / Shannon indices (finding 5) 
- Temporal frequency (finding 4)
- Station richness / crossref heatmap

Claude Code could create new layouts for these if time permits. But the D3 charts in the HTML already cover them well.

**Inset maps**: The corridor layouts (MAP1, MAP2, MAP6, MAP7) could benefit from a Switzerland inset showing where the corridor is.

---

## PHASE 2: Gather Data

Read all CSVs and build compact JS data objects. The pattern: read → filter → embed as `const DATA = [{...}]` in the HTML.

### Data files to read

```
~/CLAUDE/City101_ClaudeCode/datasets/corridor_analysis/
  city101_corridor_segments_WCI.csv          → 49 stations: WCI, lat, lon
  city101_station_crossref_classmates.csv    → 49 stations: richness, shannon diversity
  city101_ga_cost_corridor.csv               → 49 stations: rail_km, price_full, price_halbtax, ga_daily
  city101_first_last_trains.csv              → 49 stations: service_window_weekday_hrs
  city101_modal_diversity.csv                → 49 stations: modal_shannon, n_modes
  city101_temporal_summary.csv               → 7 slots: workable count, IC trains, avg TWCI
  city101_journey_workability.csv            → 618 connections: workability_class
  city101_break_points.csv                   → 49 stations: break severity

~/CLAUDE/City101_ClaudeCode/datasets/24h_venues/
  city101_late_night_venues_v3.csv           → 134 venues: name, lat, lon, amenity_type, corridor_segment

~/CLAUDE/City101_ClaudeCode/datasets/remote_work/
  remote_work_places.csv                     → 68 places: name, lat, lon, place_type

~/CLAUDE/City101_ClaudeCode/datasets/zurich_comparison/
  zurich_comparison_metrics.csv              → 15 comparison metrics
```

### Segment classification (by rail_km from Geneva)
```
0–10 km    → Geneva     → #e74c3c
10–35 km   → La Côte    → #e67e22
35–55 km   → Lausanne   → #3498db
55–63 km   → Lavaux     → #9b59b6
63+ km     → Riviera    → #2ecc71
```

Station order: ALWAYS sorted by `rail_km_est_from_geneva`, never alphabetical.

---

## PHASE 3: Build the HTML

### Design System

```css
/* Background */
--bg: #0a0a0f;
--bg2: #111118;
--bg3: #1a1a24;

/* Text */
--text: #e8e6e1;
--text-dim: #8a8880;
--text-bright: #ffffff;

/* Accent */
--accent: #c8a86e;
--accent-dim: #8a7548;

/* Segments */
--geneva: #e74c3c;
--lacote: #e67e22;
--lausanne: #3498db;
--lavaux: #9b59b6;
--riviera: #2ecc71;

/* Fonts — import from Google */
Instrument Serif  → display headings
DM Sans           → body text
DM Mono           → data labels, stats, monospace elements

/* Libraries (CDN) */
D3 v7:        https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js
Leaflet 1.9:  https://unpkg.com/leaflet@1.9.4/dist/leaflet.js + CSS
Tiles:        https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png
```

### Page Structure

**CRITICAL**: Everything is one continuous scroll. No separate pages. Chapters fade in via IntersectionObserver (threshold 0.15). Charts animate once on first visibility. Fixed thin nav bar at top.

```
┌─────────────────────────────────────────────────┐
│ FIXED NAV: The Archipelago  01 02 ... 10  Explore│
├─────────────────────────────────────────────────┤
│                                                 │
│  HERO                                           │
│  "The Archipelago"                              │
│  101 km · 49 stations · one question            │
│  Does this rail line make a city?               │
│                                                 │
├─────── scroll ──────────────────────────────────┤
│                                                 │
│  CH 01 — THE QUESTION                           │
│  [narrative text only]                          │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  CH 02 — THE INDEX                              │
│  [stat cards: 49 / 32 / 8,000+ / 7]            │
│  [IMAGE: map7_synchronicity.png]                │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  CH 03 — THE FRACTURE                           │
│  [D3: WCI bar chart, 49 stations]               │
│  [IMAGES: map1_wci.png + map3_lavaux.png]       │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  CH 04 — TWO CORRIDORS                          │
│  [D3: workability donut]                        │
│  [IMAGE: map6_transit.png]                      │
│  [EMBED: Marey diagram — inline canvas or       │
│   iframe to city101_marey_diagram.html]         │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  CH 05 — THE PRICE                              │
│  [D3: cost curve with GA + CHF 20 lines]        │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  CH 06 — THE CLOCK                              │
│  [D3: temporal bars — 7 time slots]             │
│  [D3: service window lollipop — 49 stations]    │
│  [EMBED: spacetime heatmap — inline or iframe   │
│   to city101_spacetime_diagram.html]            │
│  [EMBED: clock diagram — inline or iframe       │
│   to city101_clock_diagram.html]                │
│  [IMAGES: map4_geneva.png + map5_lausanne.png]  │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  CH 07 — THE PHASE TRANSITION                   │
│  [D3: diversity scatter + phase transition line] │
│  [IMAGE: map2_remote_work.png]                  │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  CH 08 — THE PROOF                              │
│  [comparison cards: City101 vs Zurich]          │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  CH 09 — THE DARK HOURS                         │
│  [D3: nightlife bars by segment]                │
│  [LEAFLET: interactive corridor map —           │
│   49 stations + 134 venues + 68 workspaces]     │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  CH 10 — THE PROPOSITION                        │
│  [timeline grid: 4 program cards]               │
│  [pull quote]                                   │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  EXPLORE — 10 interactive visualizations        │
│  [grid of cards linking to standalone HTMLs]     │
│                                                 │
├─────────────────────────────────────────────────┤
│  COLOPHON                                       │
└─────────────────────────────────────────────────┘
```

### Integrating the 3 Temporal Vizs

The clock, Marey, and spacetime diagrams are each standalone HTML files with embedded canvas/grid rendering. Two integration strategies:

**Option A — iframe** (simpler, keeps them independent):
```html
<div class="viz-embed">
  <iframe src="city101_marey_diagram.html" width="100%" height="800" frameborder="0"></iframe>
</div>
```
Style the container with matching background. The Marey has a light theme — consider adding a wrapper that inverts or just accept the contrast as intentional (it IS a different kind of document — a classical transportation diagram).

**Option B — inline** (more seamless, but requires adapting each viz's JS/CSS):
Port the canvas/grid code directly into index.html sections. More work but no iframe borders.

**Recommendation**: Use iframes for Marey (light theme, canvas-based, complex) and inline the spacetime heatmap (it's just a grid, easy to port, dark theme matches). Clock diagram can go either way — it's canvas-based but dark themed.

### Leaflet Map Spec

For Chapter 09, build an interactive map showing the corridor's nighttime landscape:

```javascript
// Tile layer
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png')

// Station markers — circle markers sized by WCI
STATIONS.forEach(s => {
  L.circleMarker([s.lat, s.lon], {
    radius: Math.max(3, s.wci * 20),
    fillColor: SEG_COLORS[s.segment],
    fillOpacity: 0.8,
    stroke: true,
    weight: 1,
    color: 'rgba(255,255,255,0.2)'
  }).bindPopup(`<b>${s.name}</b><br>WCI: ${s.wci}<br>Service: ${s.service_hrs}h`)
});

// Late-night venues — small purple dots
LATE_NIGHT.forEach(v => {
  L.circleMarker([v.lat, v.lon], {
    radius: 3, fillColor: '#9b59b6', fillOpacity: 0.6, stroke: false
  }).bindPopup(v.name)
});

// Remote work places — small orange dots
REMOTE_WORK.forEach(w => {
  L.circleMarker([w.lat, w.lon], {
    radius: 3, fillColor: '#e67e22', fillOpacity: 0.6, stroke: false
  }).bindPopup(w.name)
});

// Layer toggle control
L.control.layers(null, {
  'Stations (WCI)': stationLayer,
  'Late-night venues (134)': venueLayer,
  'Remote workspaces (68)': workLayer
}).addTo(map);

// Fit bounds: Geneva to Villeneuve
map.fitBounds([[46.18, 6.07], [46.55, 7.01]]);
```

### D3 Charts — Summary Specs

All charts use the same pattern: SVG inside a `.chart-wrap` container, animate on first visibility via IntersectionObserver.

| Chart | Chapter | X axis | Y axis | Key feature |
|-------|---------|--------|--------|-------------|
| WCI bars | 03 | 49 stations by rail_km | WCI 0–0.7 | Color by segment |
| Workability donut | 04 | — | — | 5 categories, 618 total |
| Cost curve | 05 | rail_km 0–101 | CHF 0–35 | GA line + CHF 20 line + St-Prex marker |
| Temporal bars | 06 | 7 time slots | 0–49 stations | Ghost bars at 49, gold at workable |
| Service lollipop | 06 | service_hrs 0–21.3 | 49 stations sorted | Color by segment. NEW chart. |
| Diversity scatter | 07 | Shannon 0–2.3 | richness 0–280 | Dot size ∝ √freq, phase line at 1.0 |
| Nightlife bars | 09 | count 0–80 | segments | Horizontal, Geneva red, Lausanne blue |
| Zurich comparison | 08 | — | — | Side-by-side metric cards |

### Explore Section — 10 Vizs

```html
<div class="viz-grid">
  <!-- Original 7 -->
  <a href="viz_01_ga_cost.html" class="viz-link">
    <span class="viz-num">01</span>
    <span class="viz-title">GA Cost Curve</span>
    <span class="viz-desc">How ticket type reshapes the corridor</span>
  </a>
  <!-- ... viz_02 through viz_07 ... -->
  
  <!-- 3 new temporal vizs -->
  <a href="city101_clock_diagram.html" class="viz-link">
    <span class="viz-num">08</span>
    <span class="viz-title">24h Clock</span>
    <span class="viz-desc">The dead wedge — radial time × space</span>
  </a>
  <a href="city101_marey_diagram.html" class="viz-link">
    <span class="viz-num">09</span>
    <span class="viz-title">Marey Diagram</span>
    <span class="viz-desc">Every train, one day — after Marey (1885)</span>
  </a>
  <a href="city101_spacetime_diagram.html" class="viz-link">
    <span class="viz-num">10</span>
    <span class="viz-title">Space-Time Grid</span>
    <span class="viz-desc">29 stations × 24 hours — when the line dies</span>
  </a>
</div>
```

---

## PHASE 4: Narrative Text

Use exactly as written. This is the complete text for all 10 chapters + hero + colophon.

### Hero
- Title: **"The Archipelago"**
- Subtitle: `101 kilometers of lake · 49 stations · one question`
- Big line: `Does this rail line make a city?`

### Ch 01 — The Question
The Geneva–Villeneuve corridor stretches 101 kilometers along Lac Léman, connecting a million inhabitants across a continuous lakefront rail line. Xavier Comtesse, Jeffrey Huang, and Adam Cohen proposed it functions as a *linear city* — one urban entity without government, without boundary, without name. They also said: we sorely lack indicators.

So we tested it. Not by asking whether people live along the line — they do, with one of the highest retention rates in Switzerland. But by asking something more demanding: can this rail line sustain continuous human activity across the full 24-hour cycle?

During operating hours: can a knowledge worker maintain an unbroken work session while moving through the corridor? During the gap hours — roughly 1:00 to 5:00 AM, when trains stop — what happens to the people who still need the line?

If the line holds, it's a city. If it breaks, the question becomes spatial: where, when, and for whom?

### Ch 02 — The Index
We constructed a **Working Continuity Index** — a composite metric that measures, at each of the corridor's 49 train stations, whether the infrastructure for sustained activity exists. Five dimensions, each normalized 0–1: transit frequency, workspace availability, connectivity infrastructure, temporal coverage, and mobility options.

Every piece of infrastructure knows its neighbors — every workspace knows its nearest train station, its noise level, its grocery access. The data is relational, not flat.

[dim] Sources include 194 EV charging stations (53 attributes), 68 remote work locations with opening hours and reviews, 81 WiFi hotspots, 3,218 cell towers, 2,062 shared mobility stations, 618 analyzed train connections, 134 late-night venues, first/last train times for all 49 stations, and 2,093 data points from 33 classmate datasets integrated into a station-level cross-reference matrix.

### Ch 03 — The Fracture
The WCI ranges from **0.64 in Geneva** to **0.0003 at St-Saphorin**. Of 49 stations, only 11 maintain full working continuity — 22%. Three structural gaps rupture the line into islands.

The corridor is not a gradient. It is binary: Lausanne-Flon counts 277 amenity features within one kilometer. Palézieux counts zero. Three fracture zones: Nyon–Gland (19.3 km), Gland–Morges (20 km), and the Lavaux Fracture (17.5 km between Lutry and Vevey), where UNESCO protection creates an infrastructure void.

> The corridor is not a city. It is an archipelago.

### Ch 04 — Two Corridors, One Track
An IC passenger traveling Geneva–Lausanne gets onboard WiFi, fold-down tables, a quiet car. Forty minutes of unbroken productivity. An S-Bahn passenger on the same rails gets doors every ninety seconds, no WiFi, standing room.

Of 618 analyzed connections: 15% are PRIME for working. 85% are NOT WORKABLE. Every Prime connection is a long-distance IC or IR train. Short-hop S-Bahn is never Prime. The service category — not the infrastructure — determines whether you're in a city or between cities.

The Marey diagram below makes this visible: steep diagonal lines are fast IC trains (40 minutes Geneva–Montreux). Shallow lines are slow S-Bahn. Where there are no lines, there are no trains.

### Ch 05 — The Price of the Line
The corridor costs different amounts depending on who you are. A GA annual travelcard — amortized to roughly CHF 10.50 per day — collapses the entire 101 km into one city at zero marginal cost. A full-price ticket to Lausanne costs CHF 23. On a CHF 20 daily budget, the city ends at St-Prex: 41 km from Geneva.

Short hops suffer a **6× per-kilometer penalty** compared to the full run — precisely the connections that would make the corridor function as one city. And roughly 160,000 cross-border workers in Geneva and Vaud — more people than the population of Lausanne — cannot purchase a GA, cannot access Halbtax, and vanish from the corridor at 18:00. Ghost citizens.

### Ch 06 — The Clock
We expected the corridor to breathe — wide during rush hour, narrow at midnight. Instead: **the archipelago is structurally invariant.**

14 stations at peak. 13 at 11 PM. The three structural gaps persist at every hour. IC trains halve at night (128 → 72), but the geography of the archipelago doesn't change. Interventions can't rely on "it works during rush hour." The deficit is permanent.

Service windows range from **21.3 hours** (Geneva) to **zero** (St-Saphorin). Between roughly 1:00 and 5:00 AM, the rail line dies entirely. But the people it serves don't disappear. Hospital shift workers finish at 2 AM. Geneva airport staff start at 4 AM. The gap hours reveal who the corridor's "city" promise excludes.

### Ch 07 — The Phase Transition
Following Comtesse's formula — diversity × accessibility × time = urban vitality — we tested four independent Shannon entropy indices: religious diversity, modal transport diversity, cuisine variety, economic category diversity. All four converge — correlations between r = 0.63 and r = 0.71.

There is a **phase transition at Shannon ≈ 1.0.** Below it, average station richness is 8.8 amenities. Above it, 70.5 — an **8× jump.** The Lavaux Fracture scores zero on all four indices. It isn't just a transit gap. It's a systemic diversity collapse.

The frequency-amenity paradox: stations with low frequency *need* amenities most — a 30-minute wait needs a café, a power outlet, shelter. But no one opens a café next to a 2-train-per-hour station. Infrastructure follows frequency, not need. The intervention sites are exactly where the market refuses to go.

### Ch 08 — The Proof
Same country, same operator, same rolling stock. Zurich's radial S-Bahn compresses frequency variation to **12×**. City101 produces **42×** — 3.5 times wider. Zurich's worst lakeside station gets **2 trains per hour at 11 km from center**. City101's worst gets **zero at 74 km**.

The radial topology doesn't just raise the floor — it compresses the entire distribution toward a usable minimum. The linear corridor amplifies every variation that a radial network absorbs.

> A linear city must construct the continuity that a radial city inherits from geometry.

### Ch 09 — The Dark Hours
Of 134 late-night venues: 76 in Geneva, 34 in Lausanne. Between the two poles: 24 venues across 60 kilometers. Stranded at Cully at 1 AM, the nearest open anything is 20 km east or 15 km west.

The gap hours don't reveal an inconvenience. They reveal a population. Night-shift nurses. Airport staff. Hotel night reception. Industrial zone workers. Bakery production lines launching at 3 AM. The corridor's "city" promise is a daytime-only promise — and even then, as the WCI shows, it's broken.

### Ch 10 — The Proposition
The corridor's rail spine runs through every break point. It connects every gap. The infrastructure exists — but it operates as a commuter pipeline, designed for a single user profile.

What if the rail line functioned as **24-hour living infrastructure** — not just transit, but workspace, shelter, service, lifeline?

An adaptive rail-mounted module — the *"horizontal elevator"* — transforms its program across the 24-hour cycle:

**06–09 · Work Pod** — Sound-isolated, WiFi-enabled workspace. Deploys at break-point stations where 30-minute waits are currently dead time.

**09–18 · Mobile Office** — Slow shuttles across structural gaps — Nyon↔Gland, the Lavaux Fracture. IC-quality short-hop connections.

**18–01 · Social Module** — Café car. Introduces program where diversity is below Shannon 1.0 — the difference that triggers the phase transition.

**01–05 · Lifeline** — Emergency shuttle + rest shelter. Connects hospitals, airport, industrial zones during the dead window.

Each program state answers a specific finding. The module introduces multiple programs simultaneously — crossing the Shannon 1.0 threshold. The fractal principle says: design one module, prove the system for all 38 break points.

> The data says the linear city doesn't exist. The architecture asks: can we build it?

### Colophon
The Archipelago — City101 Data Narrative
A02 Data Synchronicity · Studio Huang AR-302(k) · EPFL Spring 2026
Andrea Crespo + Henna Rafik

32 datasets · 8,000+ data points · 49 stations × 7 time slots
618 connections · 4 diversity indices · Zurich comparison
10 interactive visualizations · 7 QGIS print layouts

---

## CRITICAL NOTES

1. **One voice.** No "Andrea did" / "Henna did" anywhere except colophon.
2. **Dark theme.** #0a0a0f background throughout (except Marey iframe which has its own light theme — that contrast is intentional).
3. **Embed all chart data as JS.** No fetch() calls. Must work offline (except Leaflet tiles).
4. **Maps are static PNGs** from QGIS. The Leaflet map is the interactive geographic element.
5. **Don't modify the QGIS project layers/styles** — only fix labels and export.
6. **Don't overwrite existing viz files** — copy them into site/.
7. **Test locally:** `cd ~/CLAUDE/City101_ClaudeCode/visualizations/site && python3 -m http.server 8080`
8. **Station order:** Always by rail_km, never alphabetical.
9. **Image lightbox:** Optional click-to-zoom on QGIS map images (simple JS overlay).
10. **Nav highlighting:** The fixed top nav should highlight current chapter on scroll.
