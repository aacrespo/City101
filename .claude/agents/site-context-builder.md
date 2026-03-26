# Agent: Site Context Builder

Places real site context (terrain, buildings, rail, roads, water) around lock models in Rhino via MCP.

## On spawn, read:
- `geodata/sites/` — extracted site data (terrain.json, buildings.json, infrastructure.json, context.jpg) — preferred source
- `geodata/README.md` — pipeline docs, layer specs, output format details
- `output/city101_hub/context/` — metadata JSONs from terrain researcher (legacy)
- `output/city101_hub/terrain/` — DXF files per site (legacy)
- `output/city101_hub/prototypology_content.json` — node definitions with coordinates
- `workflows/log-400-checklist.md` — layer convention

## You produce:
- Site context geometry in Rhino on proper layers
- Alignment verification screenshots
- Notes on issues in `output/city101_hub/`

## Process

For each site:

1. **Check for extracted data** in `geodata/sites/{name}/`
   - If missing, run `python geodata/scripts/extract_site.py --name "{name}" --node {ID} --radius 750`

2. **Import terrain** via Rhino MCP:
   - Read `terrain.json` grid (origin, resolution, elevations)
   - Build mesh: vertices row-major (north to south), quad faces
   - Place on `TERRAIN` layer, color (160, 155, 140)

3. **Import buildings** via Rhino MCP:
   - Read `buildings.json` — each building has `vertices` + `faces` arrays
   - Create one Rhino mesh per building (NOT extrusions — these are LOD2 TIN meshes)
   - Place on `BUILDINGS_CONTEXT` layer, color (200, 195, 185)

4. **Import infrastructure** via Rhino MCP:
   - Read `infrastructure.json` — railways, roads, water features
   - Create polyline curves from 3D coordinate arrays
   - `RAILWAYS` layer, color (100, 100, 110)
   - `ROADS` layer, color (170, 170, 165)
   - `WATER` layer, color (100, 150, 200)

5. **Lock all context layers** (reference only, not editable)

6. **Capture viewport** — site model from aerial perspective

7. **Verify alignment** — all layers share real LV95 coordinates, no offset needed

## Legacy fallback

If `geodata/sites/` doesn't exist for a site, fall back to:
1. Import site DXF from `output/city101_hub/terrain/node_XX_context.dxf`
2. Read metadata from `output/city101_hub/context/node_XX_metadata.json`
3. Organize into `Site_XX::` sublayer structure (Terrain, Buildings, Rail, Roads)

## Rules
- All coordinates in LV95 / EPSG:2056 — no offsets or transformations needed
- All context layers are locked and dimmed — context only, not editable
- Never move or modify lock geometry — only place context around it
- Buildings are meshes, not extrusions — use vertices + faces from JSON
- Commit prefix: `[MODEL]`
