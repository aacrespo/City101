# Skill: Import Terrain

Import terrain, buildings, and infrastructure into Rhino via MCP for a given site.

## Input
Argument: site name (matching a folder in `geodata/sites/`) or node ID (1-7). If not provided, ask.

## Prerequisites
- Rhino MCP must be running
- Site data must be extracted first. Run `/site-context` or:
  ```bash
  python geodata/scripts/extract_site.py --name "{site}" --node {ID} --radius 750
  ```

## Process

1. **Locate site data** in `geodata/sites/{name}/`
   - Required: `terrain.json` and/or `buildings.json`
   - Optional: `infrastructure.json`, `context.jpg`

2. **Read site config** from `geodata/sites/{name}/config.json`
   - Get LV95 bbox and center coordinates
   - Note: all coordinates are real LV95 (no offset applied)

3. **Create layers** via Rhino MCP:
   | Layer | Color RGB | Content |
   |-------|-----------|---------|
   | TERRAIN | (160, 155, 140) | Elevation mesh |
   | BUILDINGS_CONTEXT | (200, 195, 185) | 3D building meshes |
   | RAILWAYS | (100, 100, 110) | Rail line curves |
   | ROADS | (170, 170, 165) | Road network curves |
   | WATER | (100, 150, 200) | Rivers and water bodies |
   | SITE_BOUNDARY | (255, 100, 100) | Site limits |
   | DESIGN | (100, 150, 255) | New architecture |

4. **Import terrain** from `terrain.json`:
   - Read elevation grid (origin, resolution, rows, cols)
   - Create Rhino mesh: vertex per grid cell, quad faces
   - Origin is top-left (north-west), Y decreases going south
   - Place on TERRAIN layer

5. **Import buildings** from `buildings.json`:
   - Each building has `vertices` + `faces` arrays (LOD2 TIN mesh)
   - Create one Rhino mesh per building using `Mesh.Vertices.Add()` + `Mesh.Faces.AddFace()`
   - Do NOT use extrusion — buildings are full 3D meshes with roof geometry
   - Place on BUILDINGS_CONTEXT layer
   - Fallback: if no vertices/faces, extrude from footprint using ground_z/roof_z

6. **Import infrastructure** from `infrastructure.json` (if exists):
   - Railways: create polyline curves on RAILWAYS layer
   - Roads: create polyline curves on ROADS layer
   - Water: create polyline curves on WATER layer
   - All features have 3D coordinates (x, y, z)

7. **Zoom extents** and set shaded display mode

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Buildings appear as triangles | You're using the old extrusion method. Use mesh import (vertices + faces) |
| Terrain and buildings don't align | Both must use real LV95 coordinates (no offset). Re-extract with same bbox |
| Objects too small / invisible | Zoom extents. Check coordinate ranges match (both should be ~2500000, ~1150000) |
| "Layer not found" | Create layers first with `rs.AddLayer()` |
| MCP connection refused | Check Rhino has `mcpstart` running on the correct port |

## Output
- Site context geometry in Rhino on proper layers
- Print: layers created, object counts per layer, any issues
