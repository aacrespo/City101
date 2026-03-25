# HANDOFF — 02-03 Session 1

## Last action
Replaced all 7 static QGIS map images with interactive Leaflet maps in the "Still on the Line" scrollytelling site (`index_v2.html`). Fixed QGIS print layout backgrounds from white to dark (#0a0a0f) and re-exported all 7 PNGs (150 DPI) + 7 PDFs (300 DPI). Fixed file:// GeoJSON loading issue by inlining all geodata as JS variables.

## Current state

### "Still on the Line" scrollytelling site — interactive maps: ✅ COMPLETE
All 7 static map PNGs replaced with interactive Leaflet maps (zoom, pan, popups, layer toggles). Verified via Preview MCP — zero console errors, all maps render, all data loads.

| Map ID | Chapter | Content | Status |
|--------|---------|---------|--------|
| `map7-sync` | ch2 The Index | All layers + toggle control | ✅ |
| `map1-wci` | ch3 The Fracture | WCI graduated circles + legend | ✅ |
| `map3-lavaux` | ch3 The Fracture | Lavaux zoom, fracture visible | ✅ |
| `map6-transit` | ch4 Two Corridors | Train frequency graduated | ✅ |
| `map4-geneva` | ch6 The Clock | Geneva zoom, multi-layer | ✅ |
| `map5-lausanne` | ch6 The Clock | Lausanne zoom, multi-layer | ✅ |
| `map2-remote` | ch7 Phase Transition | Remote work categorized | ✅ |

### Print exports: ✅ COMPLETE
7 PNGs + 7 PDFs re-exported with dark page backgrounds (#0a0a0f). No more white borders.

### iframe diagrams: ✅ COMPLETE
3 `_embed` copies created (clock, marey, spacetime). Headers/footers/backlinks removed. iframe heights increased.

### file:// compatibility fix: ✅ COMPLETE
Created `city101_geodata.js` (1.1 MB) — all 6 GeoJSON datasets inlined as JS variables. `city101_maps.js` checks for inline globals first, falls back to `fetch()` for server deployments.

### QGIS project
- `CITY101_WORKING.qgz` — 60 layers loaded, EPSG:2056
- 7 A02_MAP layouts with dark backgrounds confirmed
- Backup at `CITY101_WORKING.qgz.backup_before_bgfix`

### Previous work still intact
- All 7 interactive visualizations (viz_01 through viz_07): verified
- All datasets in `datasets/`: untouched
- Original `index.html`: untouched (v2 is the modified copy)

## Open threads
1. **index_v2.html not yet renamed to index.html** — user hasn't confirmed replacing the original. Both exist side by side.
2. **Missing symbols on some maps when opened locally** — fixed with geodata inlining, but user should re-verify in their browser.
3. **Fix B (missing QGIS symbols)** from original plan was not needed — interactive maps replaced the static images entirely for web.

## Key decisions made (cumulative)
- Static QGIS maps → interactive Leaflet maps for web; static exports kept only for print
- All modifications in `index_v2.html` — original `index.html` untouched
- Original viz files not modified — `_embed` copies created for iframe integration
- CartoDB Dark Matter basemap tiles
- Data loading: inline JS globals (from `city101_geodata.js`) with fetch() fallback
- IntersectionObserver lazy loading for maps (same pattern as existing charts)
- QGIS page backgrounds: #0a0a0f (rgb 10,10,15)
- GeoJSON simplification: lake 100m tolerance (→20KB), train lines filtered+dissolved+simplified 100m (→552KB), communes 100m (→312KB)
- Shared mobility pre-filtered: within 2km of 49 station coords, reduced from 200K+ to 1,716 points
- Context layer styling: communes=faint white borders, lake=dark blue fill, trains=gold accent
- Color scales: WCI red→yellow→green (0→0.65+), frequency red→green (0→16+), segment colors unchanged from viz system
- All previous decisions from S1–S11 remain valid

## Technical notes

### File paths — new files this session
```
visualizations/site/
├── index_v2.html                    (85 KB — interactive maps version)
├── city101_maps.js                  (16 KB — shared Leaflet map module)
├── city101_geodata.js               (1.1 MB — inlined GeoJSON for file:// compat)
├── data/
│   ├── lake_leman.geojson           (20 KB — 1 polygon, simplified 100m)
│   ├── train_lines.geojson          (552 KB — active lines, dissolved, simplified)
│   ├── communes.geojson             (312 KB — 150 polygons, simplified)
│   ├── ev_charging.geojson          (63 KB — 194 points from CSV)
│   ├── wifi_hotspots.geojson        (23 KB — 81 points from CSV)
│   └── shared_mobility.geojson      (336 KB — 1,716 points, pre-filtered)
├── city101_clock_diagram_embed.html (8 KB)
├── city101_marey_diagram_embed.html (13 KB)
├── city101_spacetime_diagram_embed.html (11 KB)
└── maps/
    ├── map1_wci.png … map7_synchronicity.png (7 PNGs, 150 DPI, dark bg)
    └── print/
        └── map1_wci.pdf … map7_synchronicity.pdf (7 PDFs, 300 DPI, dark bg)
```

### CRS
- QGIS project: EPSG:2056 (Swiss LV95)
- Web maps: EPSG:4326 (WGS84) — all GeoJSON exported/converted to 4326
- Bounds presets: `FULL_CORRIDOR [[46.15,6.05],[46.56,7.02]]`, `LAVAUX_ZOOM [[46.44,6.66],[46.53,6.90]]`, `GENEVA_ZOOM [[46.16,6.06],[46.29,6.22]]`, `LAUSANNE_ZOOM [[46.49,6.53],[46.56,6.70]]`

### Key architecture
- `city101_geodata.js` defines 6 globals: `GEODATA_LAKE`, `GEODATA_TRAINS`, `GEODATA_COMMUNES`, `GEODATA_EV`, `GEODATA_WIFI`, `GEODATA_MOBILITY`
- `city101_maps.js` is an IIFE returning `City101Maps` object with `init()`, layer factories, color scales, popup builders
- Script load order: `city101_geodata.js` → `city101_maps.js` → inline `<script>` (contains STATIONS/REMOTE_WORK/LATE_NIGHT arrays + mapConfigs + IntersectionObserver)
- `export_maps_print.py` saved at project root — standalone PyQGIS script for re-exporting if needed

### Errors encountered and fixed
1. `QgsCoordinateTransform` not defined → added explicit import from qgis.core
2. `processing` not defined → added `import processing`
3. Train lines GeoJSON 3.7MB → filtered active lines, dissolved, simplified 100m → 552KB
4. Lake GeoJSON 1MB → simplified 100m → 20KB
5. QGIS page background `page.setPageStyleSymbol(sym)` IndexError → fixed by editing project XML directly (modified BackgroundColor + symbol fill color in .qgs inside .qgz)
6. PDF export timeout → QGIS continued exporting in background, all 7 completed
7. Maps not showing points when opened via file:// → created `city101_geodata.js` with inlined data, modified `city101_maps.js` to check globals before fetch()

## Data sources (this session)
- Context GeoJSON: exported from QGIS layers (City101_LakeLeman, City101_TrainLines, City101_Communes_SURFACE)
- EV charging GeoJSON: converted from `datasets/ev_charging/city101_ev_charging_ENRICHED_v3.csv`
- WiFi GeoJSON: converted from `datasets/remote_work/city101_wifi_MERGEDv.2.csv`
- Shared mobility GeoJSON: converted from `datasets/transit/city101_shared_mobility.csv` (pre-filtered by proximity to 49 stations)

---

*Signed: Claude Code (terminal) · 2026-03-02*
