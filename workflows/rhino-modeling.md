# Workflow: Rhino Modeling

## Objective
Create or modify 3D geometry in Rhino via MCP.

## When to use
When modeling spatial plan geometry, massing studies, or 3D print preparation.

## Required inputs
- Design intent (what to model)
- Location coordinates (LV95 or WGS84 — will be converted)
- LOG level target (100-500)

## Steps
1. **Read `00_Workflow_v04.md` Section 3.2** — scale conventions, box() helper, LOG levels
2. **Convert coordinates** if needed: use `tools/data/convert_coordinates.py` for WGS84 → LV95
3. **Set LOG level** for the task:
   - LOG 100: massing (boxes, footprints)
   - LOG 200: envelope (roofs, facades as surfaces)
   - LOG 300: structure (columns, slabs, walls)
   - LOG 400: detail (windows, doors, stairs)
   - LOG 500: furnishing (furniture, fixtures)
4. **Use box() helper** for spatial plan geometry — defined in 00_Workflow_v04.md
5. **Model in Rhino via MCP** — create geometry, set layers, organize by building/element
6. **Verify** — screenshot viewport, check scale and position

## Expected output
- Updated Rhino file (.3dm)
- Viewport screenshot for documentation

## Edge cases
- Coordinate precision loss: LV95 → Rhino units may drift at sub-meter scale. Acceptable for LOG 100-200, verify for LOG 300+.
- MCP connection lost: save work, reconnect, verify state before continuing
- LOI before LOG: don't model detail until design decisions are certain

## History
- 10 March 2026: Created (v7 repo setup)
