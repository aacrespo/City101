# Execute: Build the A02 "Archipelago" Website

## Context
You're working on Andrea's EPFL architecture project — City101, a 101km corridor analysis (Geneva–Villeneuve). The A02 deliverable is a scrollytelling website that presents all findings as one unified narrative.

## Your instructions

Read this file completely before doing anything:
```
~/CLAUDE/City101_ClaudeCode/prompts/PROMPT_BUILD_A02_WEBSITE_v3.md
```

It contains:
1. **Design Language Reference** — the exact visual identity (fonts, colors, components, animations). Extracted from `viz_08_presentation.html`, which is the gold standard. Every file you touch must match it.
2. **Phase 0** — Unify the 10 existing standalone HTML vizs to the theme (CSS-only, copy to `site/`, don't break functionality)
3. **Phase 1** — Fix QGIS print layout labels + export as PNGs
4. **Phase 2** — Read all CSVs and embed data as JS constants
5. **Phase 3** — Build `index.html` — the mega scrollytelling page with D3 charts, Leaflet map, embedded QGIS maps, and links to standalone vizs
6. **Phase 4** — Narrative text (all 10 chapters provided verbatim)

## Key files

- **Design reference**: `~/CLAUDE/City101_ClaudeCode/visualizations/viz_08_presentation.html`
- **Data**: `~/CLAUDE/City101_ClaudeCode/datasets/` (corridor_analysis/, 24h_venues/, remote_work/, transit/, zurich_comparison/)
- **Existing vizs**: `~/CLAUDE/City101_ClaudeCode/visualizations/*.html` (11 files)
- **Output**: `~/CLAUDE/City101_ClaudeCode/visualizations/site/` (index.html + maps/ + copied viz files)
- **QGIS project**: `~/CLAUDE/City101_ClaudeCode/CITY101_WORKING.qgz` (7 layouts named A02_MAP*)

## Execution order

1. Read the full v3 prompt
2. Phase 0 first (unify vizs) — this is fast and sets the visual baseline
3. Phase 1 (QGIS exports) — if QGIS MCP is available; skip if not
4. Phase 2 + 3 together (data → HTML)
5. Test with `python3 -m http.server 8080` in the site/ directory

## Rules
- **Never overwrite original files** — always copy to site/ first
- **Never modify the QGIS project layers/styles** without asking
- Station order is ALWAYS by rail_km from Geneva, never alphabetical
- All chart data embedded as JS (no fetch calls — must work offline except Leaflet tiles)
- Marey diagram keeps its light theme — that's intentional
- One voice throughout — no "Andrea did" / "Henna did" except colophon
