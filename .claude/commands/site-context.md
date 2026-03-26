# Skill: Site Context

Extract site context (terrain, buildings, railways, roads, water) for a lock node or any location along the Arc Lemanique.

## Input
Argument: node ID (1-7), a place name (e.g., "Morges"), or LV95 coordinates. If not provided, ask.

## Process

### Preferred path: Swisstopo extraction pipeline

For any site with raw swisstopo data on the shared drive:

1. **Run extraction**:
```bash
# By node ID
python geodata/scripts/extract_site.py --name "node_03" --node 3 --radius 750

# By place name
python geodata/scripts/extract_site.py --name "morges" --radius 750

# By coordinates
python geodata/scripts/extract_site.py --name "custom_site" --center 2527500 1151500 --radius 750
```

2. **Check output** in `geodata/sites/{name}/`:
   - `terrain.json` — elevation grid (2m resolution)
   - `buildings.json` — LOD2 3D building meshes (vertices + faces)
   - `infrastructure.json` — railways, roads, water features
   - `context.jpg` — aerial photo
   - `config.json` — site metadata

3. **Import to Rhino** via `/import-terrain` or use `build_site_rhino.py` as reference.

### Skip flags

Skip any step if data is unavailable or not needed:
```bash
--skip-terrain --skip-buildings --skip-imagery --skip-infrastructure
```

### Fallback path: Legacy GIS data

If the shared drive isn't available, check for existing GIS data in:
- `source/00-datasets 2/lhiamrossier/GPKG/190226_TLM3D_City101_v3_EN.gpkg`
- `source/WORK copy/`
- `source/Documents copy/`
- `output/city101_hub/terrain/` (already processed)

## Output
- Extracted site data in `geodata/sites/{name}/`
- Print summary: what was found, feature counts, any errors or missing data

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Drive not found" | Mount Google Shared Drive "City 101", or set `SWISSTOPO_PATH` env var |
| "VRT not found" | Script falls back to individual tiles automatically |
| "GDB/GPKG not found" | Copy the file to the `Swisstopo/` folder on the shared drive |
| Buildings appear as triangles | Use the mesh import path (vertices + faces), not the extrusion path |
| Slow extraction | GeoPackage reads from network drive take 30-60s — be patient |
| Coordinates look wrong | Verify you're using EPSG:2056 (LV95), not WGS84 |

## Dependencies
- Python with rasterio, geopandas, fiona, shapely, Pillow, numpy
- Install: `pip install -r geodata/scripts/requirements.txt`
