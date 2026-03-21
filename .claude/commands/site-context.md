# Skill: Site Context

Extract site context (buildings, rail, roads, terrain) for a lock node.

## Input
Argument: node ID (1–7). If not provided, ask.

## Process

1. **Read coordinates** from `output/city101_hub/prototypology_content.json` for the given node.

2. **Check for existing GIS data** in:
   - `source/00-datasets 2/lhiamrossier/GPKG/190226_TLM3D_City101_v3_EN.gpkg`
   - `source/WORK copy/`
   - `source/Documents copy/`
   - `output/city101_hub/terrain/` (already processed)

3. **Extract 500m radius** around the node's LV95 coordinates:
   - Buildings (with heights if available)
   - Rail lines
   - Roads
   - Terrain (from swissALTI3D if available)

4. **Convert to DXF** for Rhino import, with layers:
   - `Buildings` — extruded footprints (heights from attribute or default 10m)
   - `Rail` — polylines
   - `Roads` — polylines (edges)
   - `Terrain` — mesh or contours

5. **Write metadata JSON** with:
   - Source files used
   - CRS (must be LV95 / EPSG:2056)
   - Layer list and feature counts
   - Any data gaps or quality notes

## Output
- `output/city101_hub/terrain/node_XX_context.dxf`
- `output/city101_hub/context/node_XX_metadata.json`
- Print summary: what was found, what's missing, quality assessment

## Dependencies
- Python with geopandas, fiona, ezdxf (or equivalent)
- Coordinate converter: `tools/data/convert_coordinates.py`
