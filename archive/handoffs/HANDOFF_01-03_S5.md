# HANDOFF — 01-03 Session 5
**From**: Cairn (claude.ai browser)  
**To**: Next session (desktop with QGIS MCP preferred)  
**Date**: 2025-03-01  
**Status**: Rail history timeline v3 complete, ready for geometry upgrade

---

## What was accomplished this session

### Rail History Timeline v3 (`rail_history_v3.html`)
Interactive Leaflet.js + OSM dark basemap showing 170 years of rail network evolution (1847–2025).

**Features:**
- Full-screen map with CartoDB dark tiles
- 18 corridor lines with real coordinates (corrected from Google Places data)
- 16 Swiss network context lines (muted) showing national connectivity
- 6 ghost stations (La Côte, killed 2004 by Rail 2000) with red ✕ markers
- 15 key corridor stations + 15 Swiss context cities labeled
- 35 timeline events with play/pause, speed control (1×/2×/4×), keyboard shortcuts
- Running stats: active lines, closed, ghost stations, corridor km, Swiss connections
- Click any line for popup with description and dates
- Legend distinguishing: active, closed, heritage, demolished, Swiss network

**File location**: `/mnt/user-data/outputs/rail_history_v3.html` (works when opened locally in Chrome)

**Known limitation**: Line coordinates are approximate — placed by station positions with manual waypoints. Not pixel-perfect to actual rail geometry. This is what the next task fixes.

### Google Places Map
Used the places_search + places_map_display tools to create an interactive Google Maps view of all corridor stations (21 locations including 6 ghost stations). This is the same feature Andrea's teacher demonstrated. Andrea now knows this tool is available.

---

## Task for next session: Overpass API rail geometry

### Goal
Replace the approximate polyline coordinates in `rail_history_v3.html` with actual OSM rail geometries for pixel-perfect accuracy.

### Approach
1. **Query Overpass API** for all railway lines in the corridor bounding box
   - Bbox: roughly `[46.15, 6.05, 47.55, 9.40]` (corridor + Swiss context)
   - Query for `railway=rail`, `railway=narrow_gauge`, `railway=light_rail`, `railway=funicular`, `railway=subway`
   - Also get `railway=abandoned` and `railway=disused` for closed lines
   
2. **Filter by line/route relations** — OSM groups rail segments into route relations. Key ones:
   - CFF mainline Geneva–Lausanne–Villeneuve–Brig
   - CEV/MVR Vevey–Blonay–Les Pléiades
   - MOB Montreux–Zweisimmen
   - Montreux–Glion–Rochers-de-Naye
   - NStCM Nyon–St-Cergue
   - Lausanne M2
   - CEVA/Léman Express
   - Bern–Fribourg–Lausanne
   - Gotthard axis (for context)
   - Basel–Olten–Bern/Zürich (for context)

3. **Extract GeoJSON linestrings** for each route

4. **Integrate into the HTML** — replace the hardcoded `coords` arrays with the actual OSM geometries. Can either:
   - Embed as inline GeoJSON (simplest)
   - Use Leaflet's `L.geoJSON()` instead of `L.polyline()`
   - Simplify geometry (Douglas-Peucker) to keep file size reasonable

5. **For abandoned/demolished lines** — OSM may have `railway=abandoned` or `railway=disused` tags. These are gold for the CCB tramway route and St-Légier–Châtel-St-Denis.

### Overpass query template
```
[out:json][timeout:60];
(
  // Corridor mainline
  relation["route"="train"]["operator"~"CFF|SBB"]["ref"~"S1|S2|IR|IC"]["network"~"Léman"];
  
  // Or simpler: all rail in the bounding box
  way["railway"~"rail|narrow_gauge|light_rail|funicular|subway|abandoned|disused"](46.15,6.05,47.55,9.40);
);
out geom;
```

### Network note
`overpass-api.de` is NOT in the claude.ai allowed domains. This MUST be done via QGIS MCP (Python `requests` library) or Claude Code on desktop, which have unrestricted network access.

### Script approach
Write a monolithic Python script that:
1. Queries Overpass API
2. Parses the JSON response
3. Groups ways by route/operator
4. Extracts coordinate arrays per line
5. Simplifies geometry to reduce point count
6. Outputs a JSON file with all line geometries
7. Generates updated HTML with real geometries embedded

Save as `fetch_rail_geometries.py` in the project scripts folder.

---

## Files created this session
- `/mnt/user-data/outputs/rail_history_v3.html` — current timeline (approximate coords)
- `/mnt/user-data/outputs/rail_history_map.html` — v1 (superseded by v3)
- `/mnt/user-data/outputs/HANDOFF_01-03_S5.md` — this file

## Files from previous sessions still relevant
- `/mnt/user-data/outputs/HANDOFF_01-03_S4.md` — rail history research findings
- `~/CLAUDE/City101_ClaudeCode/CITY101_WORKING.qgz` — QGIS project (50 layers, 9 layouts)
- `~/CLAUDE/City101_ClaudeCode/city101_corridor_segments_WCI.csv` — WCI scores
- `~/CLAUDE/City101_ClaudeCode/city101_remote_work_CROSSREF.csv` — workspace data

## A02 status (due 03.03)
**PARKED** — 7 A1 print layouts 95% complete in QGIS. Still need:
- Legend cleanup (hide basemap entries)
- PDF export (300dpi)
- Narrative document
- This should be prioritized over the Overpass task

## Key decisions
- Rail timeline is a research/design tool, not an A02 deliverable (yet)
- The Overpass geometry upgrade is a quality improvement, not blocking anything
- A02 finalization should come first tomorrow
