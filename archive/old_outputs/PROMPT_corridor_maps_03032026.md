# Build: Corridor Train Animation Maps

## Read first
- CLAUDE.md (project conventions)
- PLAN_corridor_animation_maps.md (full spec)

## What to build
Two interactive animated maps of the Geneva–Villeneuve rail corridor (101km, 49 stations).
These support a design argument for aerial gondola placement by showing WHERE trains run, WHEN they're busiest, and WHO is on them.

## Phase 1: Data Research (use agent teams — run in parallel)

### Agent 1: GTFS Timetable
Search and download Swiss GTFS data from opentransportdata.swiss or transport.opendata.ch.
Extract stop_times, trips, routes, stops, shapes, calendar for the corridor.
Filter: rail only (route_type 2), bounding box lat 46.15–46.55, lon 6.10–6.95.
For a typical weekday, compute: for every minute of 24h, which trains are moving and where (interpolate position between stations using arrival/departure times).
Output: `source/animation/gtfs_corridor_trains.csv` with columns: trip_id, route_name, minute_of_day, lat, lon, direction, line_name
Also output: `source/animation/gtfs_corridor_stops.csv` — all corridor rail stops with coordinates.
Respect rate limits: 0.35s minimum between API calls.

### Agent 2: Passenger Counts & Ridership
Search data.sbb.ch for Passagierfrequenz (station passenger frequency) dataset.
Search opentransportdata.swiss for ridership/occupancy data.
Search BFS (bfs.admin.ch) for public transport statistics.
Cross-reference with existing city101_transport_frequency.csv in the project.
Check if SBB publishes hourly distribution curves or load factors per line.
Output: `source/animation/station_ridership.csv` with columns: station_name, lat, lon, daily_passengers, source, peak_morning_pct, peak_evening_pct, off_peak_pct

### Agent 3: Demographics
Search BFS STATPOP for commune-level population along the corridor.
Search BFS structural survey for age distribution, profession categories, commute mode per commune.
Search for frontalier (cross-border commuter) statistics by commune.
Search for pendlermobilität origin-destination data.
Get commune boundary GeoJSON for the corridor extent.
Output: `source/animation/corridor_demographics.csv` with columns: commune_name, population, lat, lon, pct_age_18_30, pct_age_30_50, pct_age_50_plus, pct_commute_train, pct_commute_car, pct_commute_bike, pct_tertiary_sector, frontaliers_count

### Agent 4: Route Geometry
Extract rail line geometries from OSM or existing QGIS project data.
Match to GTFS routes if possible.
Include: main SBB line, Geneva CEVA, Lausanne-Villeneuve, any branch lines.
Simplify geometry for web use (Douglas-Peucker).
Output: `source/animation/corridor_rail_lines.geojson` — GeoJSON FeatureCollection with line geometries and properties (line_name, operator, type).

All agents: save outputs to `~/CLAUDE/City101_ClaudeCode/source/animation/`. Create the directory if needed. Print a summary of what was found, what's missing, and data quality notes.

## Phase 2: Build Map 1 — Train Pulse (24h frequency animation)

Use the frontend-design skill. This must look like a data artwork, not a dashboard.

### Three visual layers — CRITICAL distinction:

**Layer 1 — BACKGROUND (sky canvas):** Atmospheric colors simulating real daylight cycle. NOT themed. Hardcoded.
- 00:00-05:30 → deep navy (#0c1445)
- 05:30-06:30 → navy → violet (#2d1b4e) → first warm (#4a2040)
- 06:30-07:30 → coral/pink (#e8927c) → warm amber (#f0a868)
- 07:30-10:00 → brightening to pale sky (#a8d0e6 → #87ceeb)
- 10:00-14:00 → full daylight (#87ceeb slight warm white)
- 14:00-17:00 → warm golden creep (#c4b484)
- 17:00-18:30 → golden hour amber (#d4a04a → #d4764e)
- 18:30-19:30 → sunset (#d4764e → #c45c7c → #6b3a6b)
- 19:30-20:30 → dusk violet (#2d1b4e) → deep blue
- 20:30-24:00 → night navy (#0c1445)
These should transition smoothly, not in steps. Use interpolation.

**Layer 2 — DATA (trains):** White (#ffffff) dots and trails at varying opacity.
- Each active train = a white dot moving along its route
- The dot leaves a fading trail behind it (opacity decays over ~2 minutes of map-time)
- Where multiple trails overlap, the brightness accumulates — "long exposure" glow effect
- Busier track segments naturally glow brighter through trail accumulation
- This MUST read against all sky states (white works on both dark night and bright day)
- Use Canvas overlay on Leaflet for performance (not SVG — too many animated elements)

**Layer 3 — CHROME (UI controls):** Built entirely with CSS variables so it adapts to any theme.
```css
:root {
  --chrome-bg: #0a0a0f;
  --chrome-text: #e8e6e1;
  --chrome-accent: #c8a86e;
  --chrome-muted: #8a8880;
  --chrome-surface: rgba(10, 10, 15, 0.85);
  --font-display: 'Instrument Serif', serif;
  --font-body: 'DM Sans', sans-serif;
  --font-mono: 'DM Mono', monospace;
}
/* Swap to this block for light theme — everything adapts */
/*
:root {
  --chrome-bg: #faf8f4;
  --chrome-text: #1a1a1a;
  --chrome-accent: #eb0000;
  --chrome-muted: #666666;
  --chrome-surface: rgba(250, 248, 244, 0.9);
  --font-display: 'Cormorant Garamond', serif;
  --font-body: 'Libre Franklin', sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
}
*/
```

### UI Elements (all using CSS variables):
- **Time scrubber** at bottom: horizontal slider showing 00:00–24:00, draggable. Current time displayed in --font-mono. Play/pause button.
- **Speed control**: 1x / 2x / 5x / 10x
- **Live counters** (top-right corner): current time (large, --font-mono), active trains count, trains/hour this period
- **Period label**: "Morning Rush" / "Midday" / "Evening Rush" / "Late Night" etc. — in --font-display
- **Layer toggles**: Trains / S-Bahn / Metro / Tram (each toggleable, different trail colors if shown)
- **Title**: "Train Pulse" in --font-display, subtitle "24 hours on the Geneva–Villeneuve corridor" in --font-body

### Technical:
- Leaflet.js for the base map (no tiles — the sky color IS the background, or use a very subtle terrain outline)
- Canvas overlay for all train animation (requestAnimationFrame loop)
- Corridor geometry from the GeoJSON (agent 4 output)
- Station positions as subtle dots with labels appearing on hover
- Full viewport, no scroll — the map IS the page
- Responsive — works on laptop screens (1440px+) and projector
- Single self-contained HTML file with embedded CSS/JS
- Load data from the Phase 1 CSV/GeoJSON outputs

### If GTFS data isn't available yet:
Use the existing city101_transport_frequency.csv to build a synthetic schedule:
- For each of the 49 stations, use the trains_per_hour values to generate plausible departure times
- Interpolate train positions between consecutive stations
- This gives a working prototype while real GTFS data is being sourced

## Phase 3: Build Map 2 — Passenger Flow

Same framework as Map 1 (same sky transitions, same CSS variables, same controls).
Differences:
- Train dots sized proportionally to estimated passenger count
- Stations show accumulation: a pulsing ring whose radius = passengers waiting/boarding
- Optional: corridor cross-section bar at bottom showing volume distribution along the line
- Demographic layer toggle: communes colored by dominant commute mode (choropleth, low opacity)

Build as a separate HTML file. Same structure, shares the CSS variables.

## Output locations
- Data: `~/CLAUDE/City101_ClaudeCode/source/animation/`
- Map 1 HTML: `~/CLAUDE/City101_ClaudeCode/visualizations/train_pulse_24h.html`
- Map 2 HTML: `~/CLAUDE/City101_ClaudeCode/visualizations/passenger_flow_24h.html`
- Do NOT modify any existing files. Write only to new paths.

## Coordinate system
- Web maps: WGS84 (Leaflet native)
- Keep LV95 columns in all CSVs for QGIS cross-reference
