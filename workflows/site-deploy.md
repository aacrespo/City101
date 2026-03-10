# Workflow: Site Deploy

## Objective
Deploy the scrollytelling site for viewing.

## When to use
When the site needs to be accessible (for desk crit, review, or sharing).

## Required inputs
- `visualizations/site/` with all assets

## Steps
1. **Verify all referenced assets exist**:
   - All GeoJSON files referenced in city101_geodata.js
   - All embed HTML files referenced as iframes
   - All map PNGs in maps/ directory
2. **Check city101_geodata.js** — all needed GeoJSON must be inlined for file:// compatibility
3. **Test locally**:
   - Open `index_v2.html` directly via file:// — verify maps load
   - Or start local server: `python -m http.server 8000` from `visualizations/site/`
4. **Deploy** — method TBD (currently manual file sharing or local server)

## Expected output
- Working site accessible via browser

## Edge cases
- Maps don't load via file://: check that geodata.js globals are properly defined and loaded before maps.js
- Missing basemap tiles: CartoDB requires internet connection
- Large page load: check that IntersectionObserver lazy loading is active

## History
- 10 March 2026: Created (v7 repo setup)
