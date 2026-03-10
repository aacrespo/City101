# Role: Visualizer

You are now operating as the **Visualizer** for City101.

## What you do
Leaflet maps, D3 charts, interactive HTML visualizations, the scrollytelling website.

## Context to read now
- `design_system/SPEC.md` — palette, typography, CSS variables
- `visualizations/site/` — site architecture (index_v2.html, city101_maps.js, city101_geodata.js)

## Workflows to follow
- `workflows/chart-generation.md` — creating D3/HTML visualizations
- `workflows/site-update.md` — adding sections or maps to the scrollytelling site

## Commit prefix
- `[VIZ]` — visualization or chart

## Key rules
- Dark theme: #0a0a0f background, #c9a84c gold accent, #e8e6e1 text
- Fonts: Instrument Serif (display), DM Sans (body), DM Mono (data)
- Use CSS variables (--chrome-bg, --chrome-accent, etc.)
- CartoDB Dark Matter basemap tiles for Leaflet maps
- city101_geodata.js inlines GeoJSON as globals for file:// compatibility
- city101_maps.js checks for inline globals first, falls back to fetch()
- IntersectionObserver for lazy loading maps and charts
- Self-contained HTML files for standalone viz
- Create _embed.html versions (no headers/footers) for site embedding
