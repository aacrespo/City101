# Workflow: Map Generation

## Objective
Create a new map, either as a Leaflet web map or a QGIS print map.

## When to use
When creating any new map for the project.

## Required inputs
- Data to map (dataset path)
- Map type: web (Leaflet) or print (QGIS)
- What the map should show (layer, symbology intent)

## Steps — Leaflet (web)
1. **Read `design_system/SPEC.md`** for visual identity
2. **Load base layers** using `tools/maps/load_base_layers.py` (lake, train lines, communes)
3. **Apply design system** via `tools/maps/apply_design_system.py`: CartoDB Dark Matter tiles, gold accent, DM Sans font
4. **Add data layer**: load GeoJSON from `datasets/` or generate via `tools/util/csv_to_geojson.py`
5. **Configure popups and legend** — use CSS variables from SPEC.md
6. **Add to `city101_geodata.js`** if the map will be in the scrollytelling site (for file:// compatibility)
7. **Test** — verify lazy loading with IntersectionObserver if embedding in site

## Steps — QGIS (print)
1. **Read `design_system/SPEC.md`** for visual identity
2. **Open CITY101_WORKING.qgz** (check LOCKBOARD.md first!)
3. **Set CRS**: EPSG:2056
4. **Dark background**: page bg rgb(10, 10, 15)
5. **Add data layer** — style with design system colors
6. **Labels**: DM Sans, white, dark halo
7. **Create print layout** — A1 landscape standard

## Expected output
- Leaflet: self-contained HTML file in `visualizations/` or section in site
- QGIS: layout ready for export via `workflows/map-export.md`

## Edge cases
- Data has WGS84 coords but QGIS needs LV95: use `tools/data/convert_coordinates.py`
- Large dataset (>5000 points): consider clustering for Leaflet, simplification for print

## History
- 10 March 2026: Created (v7 repo setup)
