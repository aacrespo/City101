# Skill: Import Terrain

Import terrain and site context into Rhino via MCP for a given lock node.

## Input
Argument: node ID (1–7). If not provided, ask.

## Prerequisites
- Rhino MCP must be running
- Site context DXF must exist: `output/city101_hub/terrain/node_XX_context.dxf`
- Metadata JSON must exist: `output/city101_hub/context/node_XX_metadata.json`

If prerequisites not met, run `/site-context` first.

## Process

1. **Read metadata** from `output/city101_hub/context/node_XX_metadata.json`
   - Get LV95 coordinates for the node center
   - Get layer list and feature counts

2. **Calculate offset** for Rhino placement:
   - Lock models are at local origin (0,0,0)
   - Site context uses real LV95 coordinates
   - Offset = node's LV95 coords (will be applied during import)

3. **Import DXF** via Rhino MCP:
   - Use `execute_rhinoscript_python_code` to import the DXF
   - Apply coordinate offset so lock sits at correct position in context

4. **Organize layers** via Rhino MCP:
   - Create parent layer: `Site_XX`
   - Move imported geometry to sublayers:
     - `Site_XX::Terrain` — dimmed 50%
     - `Site_XX::Buildings` — dimmed 30%
     - `Site_XX::Rail` — dimmed 50%
     - `Site_XX::Roads` — dimmed 70%
   - Lock all Site layers (reference only)

5. **Set layer colors:**
   - Terrain: (160, 155, 140)
   - Buildings: (200, 195, 185)
   - Rail: (100, 100, 110)
   - Roads: (170, 170, 165)

6. **Verify alignment:**
   - Capture aerial viewport
   - Check that buildings/rail are at correct positions relative to lock

## Output
- Site context in Rhino file on proper layers
- Viewport screenshot for verification
- Print: layers created, object counts, any alignment issues
