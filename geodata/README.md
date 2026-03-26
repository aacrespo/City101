# Geodata Pipeline

Extract terrain, buildings, infrastructure, and aerial imagery from swisstopo data for any site along the Arc Lemanique (Geneva-Villeneuve), then build 3D site models in Rhino.

## Quick start

```bash
# 1. Install dependencies
pip install -r geodata/scripts/requirements.txt

# 2. Check data access
python geodata/scripts/find_drive.py

# 3. Extract a site (e.g., 1.5km box around Lausanne Ouchy)
python geodata/scripts/extract_site.py --name "lausanne_ouchy" --center 2534400 1151600 --radius 750

# Or use a lock node ID (1-7)
python geodata/scripts/extract_site.py --name "morges" --node 3 --radius 750

# Or just a known place name
python geodata/scripts/extract_site.py --name "Morges" --radius 750
```

Output lands in `geodata/sites/{name}/`:
- `terrain.json` — elevation grid (2m resolution)
- `buildings.json` — LOD2 3D building meshes (vertices + face indices + footprint)
- `infrastructure.json` — railways, roads, water features (3D polylines)
- `context.jpg` — aerial photo
- `config.json` — site metadata

## Data source

Raw swisstopo data on Google Shared Drive **City 101** -> `Swisstopo/` subfolder.
The drive letter varies per machine (auto-detected by `find_drive.py`).

Override with: `set SWISSTOPO_PATH=C:\path\to\swisstopo`

### Datasets

| Dataset | What | Format | Resolution |
|---------|------|--------|------------|
| swissALTI3D | Bare terrain elevation (DTM) | GeoTIFF + VRT mosaic | 2m |
| SWISSIMAGE | Aerial orthophotos | GeoTIFF + VRT mosaic | 0.5m |
| swissBUILDINGS3D | 3D building models (LOD2 TIN) | FileGDB (.gdb.zip) | vector |
| swissTLM3D | Topographic landscape (roads, rails, water) | GeoPackage (.gpkg.zip) | vector |

All data uses **EPSG:2056 (Swiss LV95)** coordinates.

## Skip flags

Skip any extraction step if you don't need it or if the data isn't available:

```bash
python geodata/scripts/extract_site.py --name "test" --node 3 --radius 500 \
    --skip-terrain --skip-buildings --skip-imagery --skip-infrastructure
```

## Reference points

| Location | Easting | Northing |
|----------|---------|----------|
| Geneva (Jet d'eau) | 2500200 | 1118400 |
| Nyon | 2508600 | 1137700 |
| Morges | 2526800 | 1151700 |
| Lausanne (Ouchy) | 2534400 | 1151600 |
| Lutry | 2539500 | 1150200 |
| Vevey | 2553500 | 1145500 |
| Montreux | 2558000 | 1142800 |
| Villeneuve | 2561500 | 1137500 |

Use `--center E N --radius 750` with any of these coordinates, or just `--name Morges`.

## Lock nodes (1-7)

Use `--node ID` to extract around a healthcare lock site:

| Node | Location | Easting | Northing |
|------|----------|---------|----------|
| 1 | Geneva North Industrial Belt | 2496500 | 1122500 |
| 2 | Nyon Hospital + Genolier | 2507500 | 1139500 |
| 3 | Morges Hospital Gap | 2527500 | 1151500 |
| 4 | Crissier-Bussigny | 2533500 | 1153500 |
| 5 | CHUV Lausanne | 2538500 | 1152500 |
| 6 | Montreux-Glion | 2560500 | 1143500 |
| 7 | Rennaz | 2560000 | 1137500 |

## Building in Rhino

After extraction, use `build_site_rhino.py` as a reference for Rhino MCP agents, or run `/import-terrain` to import via Claude.

### Rhino layers

| Layer | Content | Color RGB |
|-------|---------|-----------|
| TERRAIN | Elevation mesh | (160, 155, 140) |
| BUILDINGS_CONTEXT | 3D building meshes | (200, 195, 185) |
| RAILWAYS | Rail line curves | (100, 100, 110) |
| ROADS | Road network curves | (170, 170, 165) |
| WATER | Rivers and water bodies | (100, 150, 200) |
| SITE_BOUNDARY | Chosen site limits | (255, 100, 100) |
| DESIGN | New architectural design | (100, 150, 255) |
| STRUCTURE | Structural elements | (180, 180, 175) |
| LANDSCAPE | Landscape design | (120, 170, 100) |

## Output format details

### buildings.json

Each building is a full LOD2 3D mesh from swissBUILDINGS3D (not a simple footprint):

```json
{
  "footprint": [[x, y], ...],
  "ground_z": 372.5,
  "roof_z": 385.2,
  "vertices": [[x, y, z], ...],
  "faces": [[i0, i1, i2], ...],
  "type": "Gebaeude Einzelhaus"
}
```

Import as Rhino meshes (not extrusions) to preserve roof geometry.

### infrastructure.json

```json
{
  "railways": [{"geometry": [[x, y, z], ...], "type": "Eisenbahn", "name": "..."}, ...],
  "roads": [{"geometry": [[x, y, z], ...], "type": "Strasse", "level": "..."}, ...],
  "water": [{"geometry": [[x, y, z], ...], "type": "Fliessgewaesser", "water_type": "flowing"}, ...]
}
```

Import as Rhino polyline curves on separate layers.

## Error handling

| Error | What happens | Fix |
|-------|-------------|-----|
| VRT not found | Falls back to individual GeoTIFF tiles | Check drive connection |
| GDB/GPKG not found | Skips that step, prints path to copy file to | Copy file to shared drive |
| No tiles match bbox | Prints error, continues | Check coordinates are in Arc Lemanique bounds |
| Building has degenerate geometry | Skipped silently | Normal — some GDB records are invalid |
| Drive not found | Raises error with instructions | Set SWISSTOPO_PATH or mount shared drive |
| Layer not found in GDB | Tries to list available layers | Check dataset version matches config.json |

## Notes

- Lake Geneva surface: ~372m above sea level
- Building heights are absolute (meters ASL), not relative to ground
- Buildings are LOD2 TIN meshes (30-70 triangle faces per building, not simple footprints)
- Typical site size: 1-3 km per side
- 1km x 1km at 2m resolution = 500x500 grid = 250,000 points
- GeoPackage reads from shared drive can be slow (30-60s) — be patient
