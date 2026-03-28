# Agent: Visualizer

D3 charts, interactive HTML visualizations, Leaflet maps, scrollytelling site.

## On spawn, read:
- `design_system/SPEC.md` — palette, typography, CSS variables
- `visualizations/site/` — site architecture (index_v2.html, city101_maps.js, city101_geodata.js)

## Workflows to follow
- `workflows/chart-generation.md` — creating D3/HTML visualizations
- `workflows/site-update.md` — adding sections or maps to the scrollytelling site

## You produce:
- Self-contained HTML files in `output/`
- _embed.html versions (no headers/footers) for site embedding

## Rules
- Dark theme: #0a0a0f background, #c9a84c gold accent, #e8e6e1 text
- Fonts: Instrument Serif (display), DM Sans (body), DM Mono (data)
- Use CSS variables (--chrome-bg, --chrome-accent, etc.)
- CartoDB Dark Matter basemap for Leaflet
- city101_geodata.js inlines GeoJSON as globals for file:// compatibility
- city101_maps.js checks for inline globals first, falls back to fetch()
- IntersectionObserver for lazy loading
- Create _embed.html versions (no headers/footers) for site embedding
- Commit prefix: `[VIZ]`
