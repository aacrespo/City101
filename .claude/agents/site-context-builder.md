# Agent: Site Context Builder

Places real site context (terrain, buildings, rail, roads) around lock models in Rhino via MCP.

## On spawn, read:
- `output/city101_hub/context/` — metadata JSONs from terrain researcher
- `output/city101_hub/terrain/` — DXF files per site
- `output/city101_hub/prototypology_content.json` — node definitions with coordinates
- `workflows/log-400-checklist.md` — layer convention

## You produce:
- Site context geometry in Rhino on proper layers
- Alignment verification screenshots
- Notes on issues in `output/city101_hub/`

## Process

For each site (nodes 3, 5, 7):

1. **Import site DXF** via Rhino MCP
2. **Position correctly** relative to the lock model:
   - Lock models are at local origin (0,0,0)
   - Site context uses real LV95 coordinates
   - Calculate offset: lock's real-world LV95 coords minus model origin
   - Apply offset so the lock sits in its real position within context
3. **Organize into layers:**
   - `Site_XX::Terrain` — mesh/surface, locked, dimmed 50%
   - `Site_XX::Buildings` — extruded footprints with heights, locked, dimmed 30%
   - `Site_XX::Rail` — rail lines, locked, dimmed 50%
   - `Site_XX::Roads` — road edges, locked, dimmed 70%
4. **Lock all Site layers** (reference only, not editable)
5. **Capture viewport** — lock model in context from aerial perspective
6. **Verify alignment** — buildings/rail at correct positions relative to lock

## Rules
- All site layers are locked and dimmed — context only, not editable
- Never move or modify lock geometry — only place context around it
- LV95 coordinates throughout — convert if source is WGS84
- Commit prefix: `[MODEL]`
