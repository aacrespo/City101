# Geodata Pipeline — How to Use It

**Written by**: Henna + Claude (Cadence), 2026-03-26
**For**: Andrea (or anyone on the team)

This guide explains the swisstopo extraction pipeline we built. It extracts terrain, 3D buildings, roads, railways, and water for any site along the Arc Lemanique, then imports everything into Rhino via MCP.

---

## What you need on your computer

### 1. Google Shared Drive mounted

The raw swisstopo data lives on our shared drive:
```
Shared drives / City 101 / Swisstopo /
```

On Henna's machine this is `H:\Shared drives\City 101\Swisstopo\`
On Andrea's machine it could be `A:\` or any other letter — the script auto-detects it.

**How to check**: open File Explorer, go to "Shared drives" in Google Drive. You should see "City 101" with a "Swisstopo" folder inside. If you don't see it, make sure Google Drive for Desktop is installed and you have access to the shared drive.

If your drive letter is weird or it doesn't auto-detect, you can set an environment variable instead:
```
set SWISSTOPO_PATH=A:\Shared drives\City 101\Swisstopo
```

### 2. What files should be on the shared drive

The `Swisstopo/` folder should contain these files:

| File | Size | What it is |
|------|------|------------|
| `swissalti3d_*.tif` (many) | ~3,200 files | 2m terrain elevation tiles |
| `swissimage-dop10_*.tif` (many) | ~3,200 files | 0.5m aerial photo tiles |
| `*.vrt` (2 files) | small | Virtual mosaics that reference all tiles |
| `swissbuildings3d_2_2024-05_2056_5728.gdb.zip` | ~2 GB | 3D building models (LOD2) |
| `swisstlm3d_2026-02-24_2056_5728.gpkg.zip` | ~2.5 GB | Roads, railways, water, land use |

If any file is missing, download it from [swisstopo.ch](https://www.swisstopo.admin.ch/) and put it in the Swisstopo folder. The terrain and imagery tiles + VRT files were downloaded by Henna. The GDB and GPKG were added later.

### 3. Python packages

Run this once in your terminal:
```bash
pip install rasterio geopandas fiona shapely Pillow numpy
```

Or from the project folder:
```bash
pip install -r geodata/scripts/requirements.txt
```

### 4. Rhino MCP (for importing into Rhino)

If you want to import the extracted data into Rhino:
1. Open Rhino
2. Type `mcpstart` in Rhino command line
3. Enter the port number (e.g., `9002`)
4. Make sure your `.mcp.json` in the project root points to the right port

---

## How to extract a site

### Option A: Just give Claude a region (easiest)

Type this in Claude Code:
```
/site-select Find the best site for a temporal lock near Morges
```

Claude will analyze corridor data, pick the optimal location, extract everything, and tell you how to import it into Rhino.

### Option B: Extract a specific location

In your terminal:
```bash
# By place name (auto-resolves coordinates)
python geodata/scripts/extract_site.py --name "Morges" --radius 750

# By lock node ID (1-7)
python geodata/scripts/extract_site.py --name "morges_hospital" --node 3 --radius 750

# By exact LV95 coordinates
python geodata/scripts/extract_site.py --name "custom_site" --center 2527500 1151500 --radius 750

# With a custom bounding box
python geodata/scripts/extract_site.py --name "big_site" --bbox 2526000 1150000 2529000 1153000
```

### Option C: Ask Claude to do it

Just say:
```
Extract the site around Vevey with a 500m radius
```

or:
```
/site-context node 5
```

---

## What you get

After extraction, a folder appears in `geodata/sites/{name}/`:

```
geodata/sites/morges/
  terrain.json          10 MB   elevation grid (2m resolution)
  buildings.json         4 MB   3D building meshes (LOD2 with roofs)
  infrastructure.json    0.3 MB railways, roads, water features
  context.jpg            0.2 MB aerial photo
  config.json            1 KB   site metadata (bbox, center, etc.)
```

---

## How to import into Rhino

### Option A: Ask Claude (easiest)

With Rhino MCP running, say:
```
/import-terrain morges
```

Claude will create the terrain mesh, building meshes, and infrastructure curves on the right layers.

### Option B: Run the reference script

Open `geodata/scripts/build_site_rhino.py`, change `SITE_NAME` at the top, and run it in Rhino's Python editor.

### What gets created in Rhino

| Layer | Color | Content |
|-------|-------|---------|
| TERRAIN | warm gray | Elevation mesh |
| BUILDINGS_CONTEXT | light gray | 3D building meshes (LOD2 roof geometry) |
| RAILWAYS | dark gray | Rail line curves |
| ROADS | medium gray | Road network curves |
| WATER | blue-gray | Rivers and water bodies |
| SITE_BOUNDARY | red | Site limits |
| DESIGN | blue | Your design goes here |

---

## Available sites (reference points)

These names auto-resolve to coordinates:

| Name | Works with `--name` |
|------|-------------------|
| Geneva | `--name "Geneva"` |
| Nyon | `--name "Nyon"` |
| Morges | `--name "Morges"` |
| Lausanne | `--name "Lausanne_Ouchy"` |
| Lutry | `--name "Lutry"` |
| Vevey | `--name "Vevey"` |
| Montreux | `--name "Montreux"` |
| Villeneuve | `--name "Villeneuve"` |

Lock nodes 1-7 also auto-resolve with `--node ID`.

---

## Skip flags

If something is slow or you don't need it:
```bash
python geodata/scripts/extract_site.py --name "test" --node 3 --radius 500 \
    --skip-terrain \
    --skip-buildings \
    --skip-imagery \
    --skip-infrastructure
```

Infrastructure (roads/railways/water) reads from a 2.5 GB GeoPackage over the network, so it's the slowest step (~30-60s). Skip it if you just want terrain + buildings.

---

## Troubleshooting

| Problem | What to do |
|---------|-----------|
| "Could not find swisstopo data" | Mount Google Drive, or set `SWISSTOPO_PATH` env var |
| "VRT not found" | The script auto-falls back to individual tiles. If no tiles either, check the drive is connected |
| "GDB not found" / "GPKG not found" | The file isn't on the shared drive yet. Copy it there |
| Very slow extraction | GeoPackage reads from network are slow. Use `--skip-infrastructure` for faster runs |
| Buildings look like triangles in Rhino | You're using an old import method. The current `build_site_rhino.py` and `/import-terrain` import buildings as meshes (correct). Never extrude from footprint |
| Terrain and buildings don't line up | They must use the same bbox. Re-extract everything together (don't mix old terrain with new buildings) |
| Python import errors | Run `pip install -r geodata/scripts/requirements.txt` |
| "No module named rasterio" | `pip install rasterio` (may need conda on some systems) |
| Coordinates look wrong | Make sure you're using EPSG:2056 (LV95), not WGS84. LV95 eastings are ~2,500,000 |

---

## Quick test to verify everything works

Run these three commands:

```bash
# 1. Check drive access
python geodata/scripts/find_drive.py

# 2. Extract a small test site (500m radius = fast)
python geodata/scripts/extract_site.py --name "test_vevey" --name "Vevey" --radius 250

# 3. Check output
ls geodata/sites/test_vevey/
```

You should see terrain.json, buildings.json, infrastructure.json, context.jpg, and config.json.

---

## File structure

```
geodata/
  config.json              dataset metadata + reference points
  README.md                full pipeline documentation
  scripts/
    extract_site.py        main extraction script
    build_site_rhino.py    reference Rhino import script
    find_drive.py          auto-detect shared drive
    requirements.txt       Python dependencies
  sites/                   extracted site data (one folder per site)
    morges/
    Vevey/
    ...
```
