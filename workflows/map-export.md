# Workflow: Map Export

## Objective
Export maps for print and web use.

## When to use
When a map is ready for output — either from QGIS layouts or Leaflet screenshots.

## Required inputs
- Completed map (QGIS layout or Leaflet map)
- Export destination

## Steps
1. **Print export (QGIS)**:
   - Export as PDF at 300 DPI → save to `maps/`
   - Export as PNG at 150 DPI → save to `visualizations/site/maps/`
   - Use `tools/maps/export_map.py` if available, or QGIS layout manager
2. **Web export (Leaflet)**:
   - PNG screenshot at 150 DPI → `visualizations/site/maps/`
   - PDF version at 300 DPI → `maps/print/`
3. **Always export both formats** — PDF for print, PNG for web/site
4. **Verify exports** — check resolution, text legibility, no clipped labels

## Expected output
- `maps/[name].pdf` — 300 DPI print version
- `visualizations/site/maps/[name].png` — 150 DPI web version

## Edge cases
- QGIS labels truncated in export: adjust label placement in layout, re-export
- Large file size: PNG compression, PDF optimization
- Dark background prints poorly: this is by design — our maps are for screen and dark-bg print

## History
- 10 March 2026: Created (v7 repo setup)
