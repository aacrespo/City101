# Workflow: Site Update

## Objective
Add a section or map to the scrollytelling site (`visualizations/site/index_v2.html`).

## When to use
When adding new content to the main website.

## Required inputs
- Content to add (map, chart, narrative section)
- Where it should appear in the scroll sequence

## Steps
1. **Read current site architecture**:
   - `visualizations/site/index_v2.html` — main page structure
   - `visualizations/site/city101_maps.js` — shared map module
   - `visualizations/site/city101_geodata.js` — inlined GeoJSON data
2. **Add section HTML** to index_v2.html at the correct scroll position
3. **If adding a map**:
   - Add GeoJSON data to `city101_geodata.js` as a new `GEODATA_[NAME]` global
   - Add map config to `city101_maps.js`
   - Configure IntersectionObserver for lazy loading
4. **If adding a chart**:
   - Create as `city101_[name]_embed.html` (no headers/footers)
   - Embed via iframe in index_v2.html
5. **Apply design system** — dark bg, gold accent, correct fonts, CSS variables
6. **Test locally** — open via file:// to verify geodata globals work without server

## Expected output
- Updated `index_v2.html` with new section
- Any new supporting files (geodata, embed HTML)

## Edge cases
- GeoJSON too large for inline: consider simplification or separate file with fetch() fallback
- Script load order matters: geodata.js → maps.js → inline scripts

## History
- 10 March 2026: Created (v7 repo setup)
