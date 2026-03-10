# Workflow: Chart Generation

## Objective
Create a self-contained D3/HTML interactive visualization.

## When to use
When creating any data visualization (chart, diagram, interactive graphic).

## Required inputs
- Data source (dataset path or inline data)
- What the visualization should show
- Whether it will be standalone or embedded in the site

## Steps
1. **Read `design_system/SPEC.md`** for visual identity
2. **Create self-contained HTML file**:
   - Dark background (#0a0a0f)
   - Gold accent (#c9a84c) for highlights
   - DM Sans body, Instrument Serif headings, DM Mono for data
   - Use CSS variables from SPEC.md
3. **Inline data** or use fetch() with fallback for file:// compatibility
4. **Save to `visualizations/`** as `viz_[NN]_[name].html`
5. **If embedding in site**: create `city101_[name]_embed.html` version (strip headers/footers/navigation)
6. **Test** — open in browser, check responsiveness, verify data displays correctly

## Expected output
- `visualizations/viz_[NN]_[name].html` — standalone version
- `visualizations/site/city101_[name]_embed.html` — embed version (if needed)

## Edge cases
- Large dataset: aggregate or sample for visualization, link to full data
- Mobile: ensure responsive layout, touch-friendly interactions
- Print: D3 charts are screen-only; for print versions, export as SVG/PNG

## History
- 10 March 2026: Created (v7 repo setup)
